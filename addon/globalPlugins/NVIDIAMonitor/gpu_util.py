import os
import subprocess
import threading
import time
import datetime
from . import pynvml
import versionInfo
from logHandler import log
import globalVars
import addonHandler

#For translators
try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	log.warning("Unable to initialise translations. This may be because the addon is running from NVDA scratchpad.")

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

	def _formatear_memoria(self, bytes, tipo):
		tipo_labels = {
			"libre": _("Memoria libre"),
			"utilizada": _("Memoria utilizada"),
			"total": _("Memoria total"),
			"utilizada por procesos": _("Memoria utilizada por procesos"),
		}
		label = tipo_labels.get(tipo, tipo)
		if bytes < 2**10:
			return _("{label}: {bytes} B").format(label=label, bytes=bytes)
		elif bytes < 2**20:
			return _("{label}: {bytes:.2f} KB").format(label=label, bytes=bytes / (2**10))
		elif bytes < 2**30:
			return _("{label}: {bytes:.2f} MB").format(label=label, bytes=bytes / (2**20))
		else:
			return _("{label}: {bytes:.2f} GB").format(label=label, bytes=bytes / (2**30))

	def _formatear_throughput(self, bytes, direccion):
		if bytes < 2**20:
			return _("{direccion} Throughput: {bytes:.2f} KB/s").format(direccion=direccion, bytes=bytes / (2**10))
		else:
			return _("{direccion} Throughput: {bytes:.2f} MB/s").format(direccion=direccion, bytes=bytes / (2**20))

	def _obtener_descripcion_estado_energia(self, power_state):
		descriptions = {
			0: _("P0 - Máximo rendimiento"),
			1: _("P1 - Rendimiento muy alto"),
			2: _("P2 - Rendimiento alto"),
			3: _("P3 - Rendimiento moderado-alto"),
			4: _("P4 - Rendimiento moderado"),
			5: _("P5 - Bajo rendimiento"),
			6: _("P6 - Modo ahorro de energía"),
			7: _("P7 - Modo ahorro (intermedio)"),
			8: _("P8 - Estado de inactividad / muy bajo rendimiento"),
			9: _("P9 - (No documentado)"),
			10: _("P10 - (No documentado)"),
			11: _("P11 - (No documentado)"),
			12: _("P12 - (No documentado)"),
			13: _("P13 - (No documentado)"),
			14: _("P14 - (No documentado)"),
			15: _("P15 - Mínimo rendimiento / máximo ahorro"),
		}
		return descriptions.get(power_state, 'Desconocido')

	def formatear_resultado_script(self, comando, resultado):
		resultado=resultado.strip()
		if resultado.startswith("ERROR:"):
			error_msg=_("Error al obtener información: {error}").format(error=resultado[6:])
			self.escribir_log(error_msg)
			return error_msg
		elif resultado=="ERROR":
			return _("Error al obtener información de la GPU")
		if comando=="nombre":
			return _("Nombre: {res}").format(res=resultado)
		elif comando=="uuid":
			return _("UUID: {res}").format(res=resultado)
		elif comando=="version_driver":
			return _("Versión del driver: {res}").format(res=resultado)
		elif comando=="carga":
			return _("Carga de la GPU: {res}%").format(res=resultado)
		elif comando=="carga_memoria":
			return _("Carga de la memoria: {res}%").format(res=resultado)
		elif comando=="memoria_libre":
			return self._formatear_memoria(int(resultado), "libre")
		elif comando=="memoria_usada":
			return self._formatear_memoria(int(resultado), "utilizada")
		elif comando=="memoria_total":
			return self._formatear_memoria(int(resultado), "total")
		elif comando=="temperatura":
			return _("Temperatura: {res} °C").format(res=resultado)
		elif comando=="consumo_energia":
			return _("Consumo: {res} W").format(res=resultado)
		elif comando=="consumo_limite":
			return _("Límite: {res} W").format(res=resultado)
		elif comando=="velocidad_ventilador":
			return _("Velocidad del ventilador: {res}%").format(res=resultado)
		elif comando=="procesos_cuda":
			return _("Procesos cuda: {res}").format(res=resultado)
		elif comando=="procesos_memoria":
			return self._formatear_memoria(int(resultado), "utilizada por procesos")
		elif comando=="frecuencia_reloj":
			return _("Frecuencia reloj GPU: {res} MHz").format(res=resultado)
		elif comando=="frecuencia_reloj_sm":
			return _("Frecuencia reloj SM: {res} MHz").format(res=resultado)
		elif comando=="frecuencia_reloj_memoria":
			return _("Frecuencia reloj memoria: {res} MHz").format(res=resultado)
		elif comando=="frecuencia_max_reloj":
			return _("Frecuencia máxima reloj GPU: {res} MHz").format(res=resultado)
		elif comando=="frecuencia_max_reloj_sm":
			return _("Frecuencia máxima reloj SM: {res} MHz").format(res=resultado)
		elif comando=="frecuencia_max_reloj_memoria":
			return _("Frecuencia máxima reloj memoria: {res} MHz").format(res=resultado)
		elif comando=="tx_throughput":
			return self._formatear_throughput(int(resultado), "TX")
		elif comando=="rx_throughput":
			return self._formatear_throughput(int(resultado), "RX")
		elif comando=="version_bios":
			return _("Versión de la BIOS: {res}").format(res=resultado)
		elif comando=="estado_energia":
			power_state=int(resultado)
			return _("Estado de energía: {desc}").format(desc=self._obtener_descripcion_estado_energia(power_state))
		else:
			return _("Tipo de información no válido")

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
			error_ruta=_("Error: El archivo no se encuentra en la ruta especificada: {ruta}").format(ruta=self.ruta)
			self.escribir_log(error_ruta)
			log.error(error_ruta)
			self.proceso=None
			return self.proceso
		except subprocess.CalledProcessError as e:
			self.en_ejecucion=False
			error_mensaje=_("Error al iniciar el proceso: {code} {cmd}").format(code=e.returncode, cmd=e.cmd)
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
					#Formatear el resultado crudo del script
					resultado_formateado=self.formatear_resultado_script(comando, resultado)
					#Guardar el resultado en la caché
					self.resultados_cache[comando] = resultado_formateado, tiempo_actual
					return cb(resultado_formateado)
				except OSError as e:
					error_proceso=_("Error al escribir en el subprocess: {error}").format(error=e)
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
				error_msg = _("Error al ejecutar comando con pynvml: {error}").format(error=e)
				log.error(error_msg)
				self.escribir_log(error_msg)
				cb(_("Error al obtener información de la GPU"))


	def ejecutar_pynvml(self, info_type):
		try:
			pynvml.nvmlInit()
			handle = pynvml.nvmlDeviceGetHandleByIndex(0)
		except Exception as e:
			log.error(_("Error iniciando pynvml: {error}").format(error=e))
			return "Error al inicializar pynvml"
		try:
			if info_type == "nombre":
				gpu_name = pynvml.nvmlDeviceGetName(handle)
				full_name = gpu_name.strip()
				return _("Nombre: {name}").format(name=full_name)
			elif info_type=="uuid":
				return _("UUID: {uuid}").format(uuid=pynvml.nvmlDeviceGetUUID(handle))
			elif info_type=="version_driver":
				return _("Versión del driver: {ver}").format(ver=pynvml.nvmlSystemGetDriverVersion())
			elif info_type == "carga":
				utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
				return _("Carga de la GPU: {load}%").format(load=utilization.gpu)
			elif info_type=="carga_memoria":
				utilization_memory=pynvml.nvmlDeviceGetUtilizationRates(handle)
				return _("Carga de la memoria: {load}%").format(load=utilization_memory.memory)
			elif info_type == "memoria_libre":
				memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
				return self._formatear_memoria(memory_info.free, "libre")
			elif info_type == "memoria_usada":
				memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
				return self._formatear_memoria(memory_info.used, "utilizada")
			elif info_type == "memoria_total":
				memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
				return self._formatear_memoria(memory_info.total, "total")
			elif info_type == "temperatura":
				temperature = pynvml.nvmlDeviceGetTemperature(
					handle, pynvml.NVML_TEMPERATURE_GPU
				)
				return _("Temperatura: {temp} °C").format(temp=temperature)
			elif info_type == "consumo_energia":
				power_usage = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
				return _("Consumo: {power:.2f} W").format(power=power_usage)
			elif info_type=="consumo_limite":
				power_limit=pynvml.nvmlDeviceGetPowerManagementLimit(handle) / 1000.0
				return _("Límite: {limit:.2f} W").format(limit=power_limit)
			elif info_type == "velocidad_ventilador":
				fan_speed = pynvml.nvmlDeviceGetFanSpeed(handle)
				return _("Velocidad del ventilador: {speed}%").format(speed=fan_speed)
			elif info_type == "procesos_cuda":
				cuda_processes = pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
				return _("Procesos cuda: {count}").format(count=len(cuda_processes))
			elif info_type=="procesos_memoria":
				processes=pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
				total_process_memory = 0
				for proc in processes:
					if proc.usedGpuMemory is not None:
						total_process_memory += proc.usedGpuMemory
				return self._formatear_memoria(total_process_memory, "utilizada por procesos")
			elif info_type == "frecuencia_reloj":
				clock_graphics_current = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
				return _("Frecuencia reloj GPU: {clock} MHz").format(clock=clock_graphics_current)
			elif info_type=="frecuencia_reloj_sm":
				clock_SM=pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_SM)
				return _("Frecuencia reloj SM: {clock} MHz").format(clock=clock_SM)
			elif info_type=="frecuencia_reloj_memoria":
				clock_memory=pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_MEM)
				return _("Frecuencia reloj memoria: {clock} MHz").format(clock=clock_memory)
			elif info_type=="frecuencia_max_reloj":
				clock_max=pynvml.nvmlDeviceGetMaxClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
				return _("Frecuencia máxima reloj GPU: {clock} MHz").format(clock=clock_max)
			elif info_type=="frecuencia_max_reloj_sm":
				clock_sm_max=pynvml.nvmlDeviceGetMaxClockInfo(handle, pynvml.NVML_CLOCK_SM)
				return _("Frecuencia máxima reloj SM: {clock} MHz").format(clock=clock_sm_max)
			elif info_type=="frecuencia_max_reloj_memoria":
				clock_memory_max=pynvml.nvmlDeviceGetMaxClockInfo(handle, pynvml.NVML_CLOCK_MEM)
				return _("Frecuencia máxima reloj memoria: {clock} MHz").format(clock=clock_memory_max)
			elif info_type=="tx_throughput":
				tx=pynvml.nvmlDeviceGetPcieThroughput(handle, pynvml.NVML_PCIE_UTIL_TX_BYTES)
				return self._formatear_throughput(tx, "TX")
			elif info_type=="rx_throughput":
				rx=pynvml.nvmlDeviceGetPcieThroughput(handle, pynvml.NVML_PCIE_UTIL_RX_BYTES)
				return self._formatear_throughput(rx, "RX")
			elif info_type=="version_bios":
				bios_version=pynvml.nvmlDeviceGetVbiosVersion(handle)
				return _("Versión de la BIOS: {ver}").format(ver=bios_version)
			elif info_type=="estado_energia":
				power_state=pynvml.nvmlDeviceGetPowerState(handle)
				return _("Estado de energía: {desc}").format(desc=self._obtener_descripcion_estado_energia(power_state))
			else:
				return _("Tipo de información no válido")
		finally:
			try:
				pynvml.nvmlShutdown()
			except Exception as e:
				log.error(_("Error al cerrar pynvml: {error}").format(error=e))
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
					error_terminate=_("Error al intentar terminar el proceso: {error}").format(error=str(e))
					self.escribir_log(error_terminate)
					pass
