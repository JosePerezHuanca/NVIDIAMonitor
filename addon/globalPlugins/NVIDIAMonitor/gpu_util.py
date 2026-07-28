import os
import subprocess
import threading
import time
import datetime
from . import pynvml
import versionInfo
from logHandler import log
import globalVars


build_year=getattr(versionInfo,'version_year', 2026)

class GPUMonitor:
	def __init__(self):
		self.ruta = os.path.join(os.path.dirname(__file__), "data", "NVIDIAScript.exe")
		self.en_ejecucion=False
		self.resultados_cache={}
		self.cache_expiracion=1
		self.use_legacy_script=True
		if build_year >= 2026:
			log.info(_("NVIDIAMonitor: NVDA 64 bits, utilizando pynvml"))
			self.use_legacy_script=False
		else:
			log.info(_("NVIDIAMonitor: NVDA versión menor a 2026.1, utilizando script externo"))

	def escribir_log(self,mensaje):
		ruta_log=os.path.join(globalVars.appArgs.configPath, "NVIDIAMonitor.log")
		with open(ruta_log, "a") as f:
			tiempo_actual=datetime.datetime.now()
			tiempo_formato=tiempo_actual.strftime("%Y-%m-%d %H:%M")
			f.write(f"{tiempo_formato} - {mensaje}\n")

	def ejecutar_script(self):
		try:
			self.proceso = subprocess.Popen(
				[self.ruta],
				stdin=subprocess.PIPE,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				text=True,
				creationflags=subprocess.CREATE_NO_WINDOW
			)
			self.en_ejecucion=True
			return self.proceso
		except FileNotFoundError as e:
			self.en_ejecucion=False
			error_ruta=_(f"Error: El archivo no se encuentra en la ruta especificada: {self.ruta}")
			self.escribir_log(error_ruta)
			log.error(error_ruta)
			self.proceso=None
			return self.proceso
		except subprocess.CalledProcessError as e:
			self.en_ejecucion=False
			error_mensaje=_(f"Error al iniciar el proceso: {e.returncode} {e.cmd}")
			self.escribir_log(error_mensaje)
			log.error(error_mensaje)
			self.proceso=None
			return self.proceso

	def ejecutar_comando(self,comando,cb):
		if self.use_legacy_script:
			def comando_hilo():
				tiempo_actual=time.monotonic()
				if comando in self.resultados_cache:
					resultado, tiempo_marca=self.resultados_cache[comando]
					if tiempo_actual - tiempo_marca < self.cache_expiracion:
						return cb(resultado)
				if not self.en_ejecucion or self.proceso.poll() is not None:
					self.ejecutar_script()
				try:
					self.proceso.stdin.write(f"{comando}\n")
					self.proceso.stdin.flush()
					resultado = self.proceso.stdout.readline()
					if not resultado:
						error_resultado=f"No se recibió salida para el comando: {comando}"
						self.escribir_log(error_resultado)
						log.error(error_resultado)
						return cb("Error al recibir respuesta del proceso.")
					#Guardar el resultado en la caché
					self.resultados_cache[comando] = resultado, tiempo_actual
					return cb(resultado)
				except OSError as e:
					error_proceso=_(f"Error al escribir en el subprocess: {e}")
					self.escribir_log(error_proceso)
					log.error(error_proceso)
					return cb("Error al escribir en el proceso.")
			thread=threading.Thread(target=comando_hilo)
			thread.start()
		else:
			try:
				resultado=self.ejecutar_pynvml(comando)
				cb(resultado)
			except Exception as e:
				error_msg = _(f"Error al ejecutar comando con pynvml: {e}")
				log.error(error_msg)
				self.escribir_log(error_msg)
				cb("Error al obtener información de la GPU")


	def ejecutar_pynvml(self, info_type):
		try:
			pynvml.nvmlInit()
			handle = pynvml.nvmlDeviceGetHandleByIndex(0)
		except Exception as e:
			log.error(_(f"Error iniciando pynvml: {e}"))
			return "Error al inicializar pynvml"
		try:
			if info_type == "nombre":
				gpu_name = pynvml.nvmlDeviceGetName(handle)
				full_name = gpu_name.strip()
				return f"Nombre: {full_name}"
			elif info_type=="uuid":
				return f"UUID: {pynvml.nvmlDeviceGetUUID(handle)}"
			elif info_type=="version_driver":
				return f"Versión del driver: {pynvml.nvmlSystemGetDriverVersion()}"
			elif info_type == "carga":
				utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
				return f"Carga de la GPU: {utilization.gpu}%"
			elif info_type=="carga_memoria":
				utilization_memory=pynvml.nvmlDeviceGetUtilizationRates(handle)
				return f"Carga de la memoria: {utilization_memory.memory}%"
			elif info_type == "memoria_libre":
				memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
				free_memory=memory_info.free
				if free_memory < 2**10:
					return f"Memoria libre: {free_memory}B"
				elif free_memory < 2**20:
					return f"Memoria libre: {free_memory / (2**10):.2f}KB"
				elif free_memory < 2**30:
					return f"Memoria libre: {free_memory / (2**20):.2f}MB"
				else:
					return f"Memoria libre: {free_memory / (2**30):.2f}GB"
			elif info_type == "memoria_usada":
				memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
				used_memory=memory_info.used
				if used_memory < 2**10:
					return f"Memoria utilizada: {used_memory}B"
				elif used_memory < 2**20:
					return f"Memoria utilizada: {used_memory / (2**10):.2f}KB"
				elif used_memory < 2**30:
					return f"Memoria utilizada: {used_memory / (2**20):.2f}MB"
				else:
					return f"Memoria utilizada: {used_memory / (2**30):.2f}GB"
			elif info_type == "memoria_total":
				memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
				total_memory=memory_info.total
				if total_memory < 2**10:
					return f"Memoria total: {total_memory}B"
				elif total_memory < 2**20:
					return f"Memoria total: {total_memory / (2**10):.2f}KB"
				elif total_memory < 2**30:
					return f"Memoria total: {total_memory / (2**20):.2f}MB"
				else:
					return f"Memoria total: {total_memory / (2**30):.2f}GB"
			elif info_type == "temperatura":
				temperature = pynvml.nvmlDeviceGetTemperature(
					handle, pynvml.NVML_TEMPERATURE_GPU
				)
				return f"Temperatura: {temperature} °C"
			elif info_type == "consumo_energia":
				power_usage = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
				return f"Consumo: {power_usage:.2f} W"
			elif info_type=="consumo_limite":
				power_limit=pynvml.nvmlDeviceGetPowerManagementLimit(handle) / 1000.0
				return f"Límite: {power_limit:.2f} W"
			elif info_type == "velocidad_ventilador":
				fan_speed = pynvml.nvmlDeviceGetFanSpeed(handle)
				return f"Velocidad del ventilador: {fan_speed}%"
			elif info_type == "procesos_cuda":
				cuda_processes = pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
				return f"Procesos cuda: {len(cuda_processes)}"
			elif info_type=="procesos_memoria":
				processes=pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
				total_process_memory = 0
				for proc in processes:
					if proc.usedGpuMemory is not None:
						total_process_memory += proc.usedGpuMemory
				if total_process_memory < 2**10:
					return f"Memoria utilizada por procesos: {total_process_memory}B"
				elif total_process_memory < 2**20:
					return f"Memoria utilizada por procesos: {total_process_memory / (2**10):.2f}KB"
				elif total_process_memory < 2**30:
					return f"Memoria utilizada por procesos: {total_process_memory / (2**20):.2f}MB"
				else:
					return f"Memoria utilizada por procesos: {total_process_memory / (2**30):.2f}GB"
			elif info_type == "frecuencia_reloj":
				clock_graphics_current = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
				return f"Frecuencia reloj GPU: {clock_graphics_current} MHz"
			elif info_type=="frecuencia_reloj_sm":
				clock_SM=pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_SM)
				return f"Frecuencia reloj SM: {clock_SM} MHz"
			elif info_type=="frecuencia_reloj_memoria":
				clock_memory=pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_MEM)
				return f"Frecuencia reloj memoria: {clock_memory} MHz"
			elif info_type=="frecuencia_max_reloj":
				clock_max=pynvml.nvmlDeviceGetMaxClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
				return f"Frecuencia máxima reloj GPU: {clock_max} MHz"
			elif info_type=="frecuencia_max_reloj_sm":
				clock_sm_max=pynvml.nvmlDeviceGetMaxClockInfo(handle, pynvml.NVML_CLOCK_SM)
				return f"Frecuencia máxima reloj SM: {clock_sm_max} MHz"
			elif info_type=="frecuencia_max_reloj_memoria":
				clock_memory_max=pynvml.nvmlDeviceGetMaxClockInfo(handle, pynvml.NVML_CLOCK_MEM)
				return f"Frecuencia máxima reloj memoria: {clock_memory_max} MHz"
			elif info_type=="tx_throughput":
				tx=pynvml.nvmlDeviceGetPcieThroughput(handle, pynvml.NVML_PCIE_UTIL_TX_BYTES)
				if tx < 2**20:
					return f"TX Throughput: {tx / (2**10):.2f}KB/s"
				else:
					return f"TX Throughput: {tx / (2**20):.2f}MB/s"
			elif info_type=="rx_throughput":
				rx=pynvml.nvmlDeviceGetPcieThroughput(handle, pynvml.NVML_PCIE_UTIL_RX_BYTES)
				if rx < 2**20:
					return f"RX Throughput: {rx / (2**10):.2f}KB/s"
				else:
					return f"RX Throughput: {rx / (2**20):.2f}MB/s"
			elif info_type=="version_bios":
				bios_version=pynvml.nvmlDeviceGetVbiosVersion(handle)
				return f"Versión de la BIOS: {bios_version}"
			elif info_type=="estado_energia":
				power_state=pynvml.nvmlDeviceGetPowerState(handle)
				# Este mapeo es aproximado y puede necesitar ajustes según el modelo de GPU.
				descriptions = {
					0: "P0 - Máximo rendimiento",
					1: "P1 - Rendimiento muy alto",
					2: "P2 - Rendimiento alto",
					3: "P3 - Rendimiento moderado-alto",
					4: "P4 - Rendimiento moderado",
					5: "P5 - Bajo rendimiento",
					6: "P6 - Modo ahorro de energía",
					7: "P7 - Modo ahorro (intermedio)",
					8: "P8 - Estado de inactividad / muy bajo rendimiento",
					9: "P9 - (No documentado)",
					10: "P10 - (No documentado)",
					11: "P11 - (No documentado)",
					12: "P12 - (No documentado)",
					13: "P13 - (No documentado)",
					14: "P14 - (No documentado)",
					15: "P15 - Mínimo rendimiento / máximo ahorro",
				}
				return f"Estado de energía: {descriptions.get(power_state, 'Desconocido')}"
			else:
				return "Tipo de información no válido"
		finally:
			try:
				pynvml.nvmlShutdown()
			except Exception as e:
				log.error(_(f"Error al cerrar pynvml: {e}"))
				pass

	def terminate(self):
		if build_year < 2026:
			if self.proceso:
				if self.proceso.poll() is not None:
					self.en_ejecucion=False
					return
				try:
					# Enviamos el comando de salida
					self.proceso.stdin.write("exit\n")
					self.proceso.stdin.flush()
					#Terminar el proceso de manera controlada
					self.proceso.terminate()
					# Esperar a que termine completamente
					self.proceso.wait()
					# Cerramos las conexiones de stdin, stdout, stderr
					self.proceso.stdin.close()
					self.proceso.stdout.close()
					self.proceso.stderr.close()
					self.en_ejecucion=False
				except Exception as e:
					error_terminate=_(f"Error al intentar terminar el proceso: {str(e)}")
					self.escribir_log(error_terminate)
					pass
