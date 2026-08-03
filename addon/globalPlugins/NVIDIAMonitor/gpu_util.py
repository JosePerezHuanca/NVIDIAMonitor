import os
import subprocess
import threading
import time
import datetime
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
		self.path = os.path.join(os.path.dirname(__file__), "data", "NVIDIAScript.exe")
		self.running=False
		self.cached_results={}
		self.cache_expiry=1
		self.use_legacy_script=True
		if build_year >= 2026:
			from . import pynvml as _pynvml
			self.pynvml = _pynvml
			log.info(_("NVIDIAMonitor: NVDA 64 bits, utilizando pynvml"))
			self.use_legacy_script=False
		else:
			self.pynvml = None
			log.info(_("NVIDIAMonitor: NVDA versión menor a 2026.1, utilizando script externo"))

	def _format_memory(self, bytes, type):
		type_labels = {
			"libre": _("Memoria libre"),
			"utilizada": _("Memoria utilizada"),
			"total": _("Memoria total"),
			"utilizada por procesos": _("Memoria utilizada por procesos"),
		}
		label = type_labels.get(type, type)
		if bytes < 2**10:
			return _("{label}: {bytes} B").format(label=label, bytes=bytes)
		elif bytes < 2**20:
			return _("{label}: {bytes:.2f} KB").format(label=label, bytes=bytes / (2**10))
		elif bytes < 2**30:
			return _("{label}: {bytes:.2f} MB").format(label=label, bytes=bytes / (2**20))
		else:
			return _("{label}: {bytes:.2f} GB").format(label=label, bytes=bytes / (2**30))

	def _format_throughput(self, bytes, direction):
		if bytes < 2**20:
			return _("{direction} Throughput: {bytes:.2f} KB/s").format(direction=direction, bytes=bytes / (2**10))
		else:
			return _("{direction} Throughput: {bytes:.2f} MB/s").format(direction=direction, bytes=bytes / (2**20))

	def _get_power_state_description(self, power_state):
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

	def format_script_result(self, command, result):
		result=result.strip()
		if result.startswith("ERROR:"):
			error_msg=_("Error al obtener información: {error}").format(error=result[6:])
			self.write_log(error_msg)
			return error_msg
		elif result=="ERROR":
			return _("Error al obtener información de la GPU")
		if command=="nombre":
			return _("Nombre: {res}").format(res=result)
		elif command=="uuid":
			return _("UUID: {res}").format(res=result)
		elif command=="version_driver":
			return _("Versión del driver: {res}").format(res=result)
		elif command=="carga":
			return _("Carga de la GPU: {res}%").format(res=result)
		elif command=="carga_memoria":
			return _("Carga de la memoria: {res}%").format(res=result)
		elif command=="memoria_libre":
			return self._format_memory(int(result), "libre")
		elif command=="memoria_usada":
			return self._format_memory(int(result), "utilizada")
		elif command=="memoria_total":
			return self._format_memory(int(result), "total")
		elif command=="temperatura":
			return _("Temperatura: {res} °C").format(res=result)
		elif command=="consumo_energia":
			return _("Consumo: {res} W").format(res=result)
		elif command=="consumo_limite":
			return _("Límite: {res} W").format(res=result)
		elif command=="velocidad_ventilador":
			return _("Velocidad del ventilador: {res}%").format(res=result)
		elif command=="procesos_cuda":
			return _("Procesos cuda: {res}").format(res=result)
		elif command=="procesos_memoria":
			return self._format_memory(int(result), "utilizada por procesos")
		elif command=="frecuencia_reloj":
			return _("Frecuencia reloj GPU: {res} MHz").format(res=result)
		elif command=="frecuencia_reloj_sm":
			return _("Frecuencia reloj SM: {res} MHz").format(res=result)
		elif command=="frecuencia_reloj_memoria":
			return _("Frecuencia reloj memoria: {res} MHz").format(res=result)
		elif command=="frecuencia_max_reloj":
			return _("Frecuencia máxima reloj GPU: {res} MHz").format(res=result)
		elif command=="frecuencia_max_reloj_sm":
			return _("Frecuencia máxima reloj SM: {res} MHz").format(res=result)
		elif command=="frecuencia_max_reloj_memoria":
			return _("Frecuencia máxima reloj memoria: {res} MHz").format(res=result)
		elif command=="tx_throughput":
			return self._format_throughput(int(result), "TX")
		elif command=="rx_throughput":
			return self._format_throughput(int(result), "RX")
		elif command=="version_bios":
			return _("Versión de la BIOS: {res}").format(res=result)
		elif command=="estado_energia":
			power_state=int(result)
			return _("Estado de energía: {desc}").format(desc=self._get_power_state_description(power_state))
		else:
			return _("Tipo de información no válido")

	def write_log(self,message):
		log_path=os.path.join(globalVars.appArgs.configPath, "NVIDIAMonitor.log")
		with open(log_path, "a") as f:
			current_time=datetime.datetime.now()
			time_format=current_time.strftime("%Y-%m-%d %H:%M")
			f.write(f"{time_format} - {message}\n")

	def run_script(self):
		try:
			self.process = subprocess.Popen(
				[self.path],
				stdin=subprocess.PIPE,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				text=True,
				creationflags=subprocess.CREATE_NO_WINDOW
			)
			self.running=True
			return self.process
		except FileNotFoundError as e:
			self.running=False
			error_path=_("Error: El archivo no se encuentra en la ruta especificada: {path}").format(path=self.path)
			self.write_log(error_path)
			log.error(error_path)
			self.process=None
			return self.process
		except subprocess.CalledProcessError as e:
			self.running=False
			error_message=_("Error al iniciar el proceso: {code} {cmd}").format(code=e.returncode, cmd=e.cmd)
			self.write_log(error_message)
			log.error(error_message)
			self.process=None
			return self.process

	def execute_command(self,command,cb):
		if self.use_legacy_script:
			def command_thread():
				current_time=time.monotonic()
				if command in self.cached_results:
					result, timestamp=self.cached_results[command]
					if current_time - timestamp < self.cache_expiry:
						return cb(result)
				if not self.running or self.process.poll() is not None:
					self.run_script()
				try:
					self.process.stdin.write(f"{command}\n")
					self.process.stdin.flush()
					result = self.process.stdout.readline()
					if not result:
						error_result=f"No se recibió salida para el comando: {command}"
						self.write_log(error_result)
						log.error(error_result)
						return cb("Error al recibir respuesta del proceso.")
					#Format raw result from script
					formatted_result=self.format_script_result(command, result)
					#Save result to cache
					self.cached_results[command] = formatted_result, current_time
					return cb(formatted_result)
				except OSError as e:
					error_process=_("Error al escribir en el subprocess: {error}").format(error=e)
					self.write_log(error_process)
					log.error(error_process)
					return cb("Error al escribir en el proceso.")
			thread=threading.Thread(target=command_thread)
			thread.start()
		else:
			try:
				result=self.execute_pynvml(command)
				cb(result)
			except Exception as e:
				error_msg = _("Error al ejecutar comando con pynvml: {error}").format(error=e)
				log.error(error_msg)
				self.write_log(error_msg)
				cb(_("Error al obtener información de la GPU"))


	def execute_pynvml(self, info_type):
		try:
			self.pynvml.nvmlInit()
			handle = self.pynvml.nvmlDeviceGetHandleByIndex(0)
		except Exception as e:
			log.error(_("Error al inicializar pynvml: {error}").format(error=e))
			return _("Error al inicializar pynvml")
		try:
			if info_type == "nombre":
				gpu_name = self.pynvml.nvmlDeviceGetName(handle)
				full_name = gpu_name.strip()
				return _("Nombre: {name}").format(name=full_name)
			elif info_type=="uuid":
				return _("UUID: {uuid}").format(uuid=self.pynvml.nvmlDeviceGetUUID(handle))
			elif info_type=="version_driver":
				return _("Versión del driver: {ver}").format(ver=self.pynvml.nvmlSystemGetDriverVersion())
			elif info_type == "carga":
				utilization = self.pynvml.nvmlDeviceGetUtilizationRates(handle)
				return _("Carga de la GPU: {load}%").format(load=utilization.gpu)
			elif info_type=="carga_memoria":
				memory_utilization=self.pynvml.nvmlDeviceGetUtilizationRates(handle)
				return _("Carga de la memoria: {load}%").format(load=memory_utilization.memory)
			elif info_type == "memoria_libre":
				memory_info = self.pynvml.nvmlDeviceGetMemoryInfo(handle)
				return self._format_memory(memory_info.free, "libre")
			elif info_type == "memoria_usada":
				memory_info = self.pynvml.nvmlDeviceGetMemoryInfo(handle)
				return self._format_memory(memory_info.used, "utilizada")
			elif info_type == "memoria_total":
				memory_info = self.pynvml.nvmlDeviceGetMemoryInfo(handle)
				return self._format_memory(memory_info.total, "total")
			elif info_type == "temperatura":
				temperature = self.pynvml.nvmlDeviceGetTemperature(
					handle, self.pynvml.NVML_TEMPERATURE_GPU
				)
				return _("Temperatura: {temp} °C").format(temp=temperature)
			elif info_type == "consumo_energia":
				power_usage = self.pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
				return _("Consumo: {power:.2f} W").format(power=power_usage)
			elif info_type=="consumo_limite":
				power_limit=self.pynvml.nvmlDeviceGetPowerManagementLimit(handle) / 1000.0
				return _("Límite: {limit:.2f} W").format(limit=power_limit)
			elif info_type == "velocidad_ventilador":
				fan_speed = self.pynvml.nvmlDeviceGetFanSpeed(handle)
				return _("Velocidad del ventilador: {speed}%").format(speed=fan_speed)
			elif info_type == "procesos_cuda":
				cuda_processes = self.pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
				return _("Procesos cuda: {count}").format(count=len(cuda_processes))
			elif info_type=="procesos_memoria":
				processes=self.pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
				total_process_memory = 0
				for proc in processes:
					if proc.usedGpuMemory is not None:
						total_process_memory += proc.usedGpuMemory
				return self._format_memory(total_process_memory, "utilizada por procesos")
			elif info_type == "frecuencia_reloj":
				clock_graphics_current = self.pynvml.nvmlDeviceGetClockInfo(handle, self.pynvml.NVML_CLOCK_GRAPHICS)
				return _("Frecuencia reloj GPU: {clock} MHz").format(clock=clock_graphics_current)
			elif info_type=="frecuencia_reloj_sm":
				clock_sm=self.pynvml.nvmlDeviceGetClockInfo(handle, self.pynvml.NVML_CLOCK_SM)
				return _("Frecuencia reloj SM: {clock} MHz").format(clock=clock_sm)
			elif info_type=="frecuencia_reloj_memoria":
				clock_memory=self.pynvml.nvmlDeviceGetClockInfo(handle, self.pynvml.NVML_CLOCK_MEM)
				return _("Frecuencia reloj memoria: {clock} MHz").format(clock=clock_memory)
			elif info_type=="frecuencia_max_reloj":
				clock_max=self.pynvml.nvmlDeviceGetMaxClockInfo(handle, self.pynvml.NVML_CLOCK_GRAPHICS)
				return _("Frecuencia máxima reloj GPU: {clock} MHz").format(clock=clock_max)
			elif info_type=="frecuencia_max_reloj_sm":
				clock_sm_max=self.pynvml.nvmlDeviceGetMaxClockInfo(handle, self.pynvml.NVML_CLOCK_SM)
				return _("Frecuencia máxima reloj SM: {clock} MHz").format(clock=clock_sm_max)
			elif info_type=="frecuencia_max_reloj_memoria":
				clock_memory_max=self.pynvml.nvmlDeviceGetMaxClockInfo(handle, self.pynvml.NVML_CLOCK_MEM)
				return _("Frecuencia máxima reloj memoria: {clock} MHz").format(clock=clock_memory_max)
			elif info_type=="tx_throughput":
				tx=self.pynvml.nvmlDeviceGetPcieThroughput(handle, self.pynvml.NVML_PCIE_UTIL_TX_BYTES)
				return self._format_throughput(tx, "TX")
			elif info_type=="rx_throughput":
				rx=self.pynvml.nvmlDeviceGetPcieThroughput(handle, self.pynvml.NVML_PCIE_UTIL_RX_BYTES)
				return self._format_throughput(rx, "RX")
			elif info_type=="version_bios":
				bios_version=self.pynvml.nvmlDeviceGetVbiosVersion(handle)
				return _("Versión de la BIOS: {ver}").format(ver=bios_version)
			elif info_type=="estado_energia":
				power_state=self.pynvml.nvmlDeviceGetPowerState(handle)
				return _("Estado de energía: {desc}").format(desc=self._get_power_state_description(power_state))
			else:
				return _("Tipo de información no válido")
		finally:
			try:
				self.pynvml.nvmlShutdown()
			except Exception as e:
				log.error(_("Error al cerrar pynvml: {error}").format(error=e))
				pass

	def terminate(self):
		if build_year < 2026:
			if self.process:
				if self.process.poll() is not None:
					self.running=False
					return
				try:
					# Send exit command
					self.process.stdin.write("exit\n")
					self.process.stdin.flush()
					#Terminate process in controlled manner
					self.process.terminate()
					# Wait for complete termination
					self.process.wait()
					# Close stdin, stdout, stderr connections
					self.process.stdin.close()
					self.process.stdout.close()
					self.process.stderr.close()
					self.running=False
				except Exception as e:
					error_terminate=_("Error al intentar terminar el proceso: {error}").format(error=str(e))
					self.write_log(error_terminate)
					pass
