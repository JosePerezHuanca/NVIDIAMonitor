# NVIDIA Monitor add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file LICENSE for more details.
# Copyright (C) 2024 José Perez <perezhuancajose@gmail.com> and ayoub <ayoubelbak13@gmail.com>

import globalPluginHandler
from scriptHandler import script, getLastScriptRepeatCount
import ui
import api
import globalVars
import winVersion
import addonHandler
from .gpu_util import GPUMonitor
from logHandler import log


#For translators
try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	log.warning("Unable to initialise translations. This may be because the addon is running from NVDA scratchpad.")


def disableInSecureMode(decoratedCls):
	if globalVars.appArgs.secure:
		return globalPluginHandler.GlobalPlugin
	return decoratedCls


@disableInSecureMode
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	#For translators
	script_category=_("NVIDIAMonitor")
	script_description=_("Si se pulsa dos veces, copia esta información al portapapeles.")
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		# Initialize gpu_util here
		self.gpu=GPUMonitor()

	def execute_command(self, command, cb):
		self.gpu.execute_command(command, cb)

	#For translators
	@script(description=_("Anuncia el nombre de la GPU. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+g",category=script_category)
	def script_gpu_name(self, gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("nombre",ui.message)
			else:
				self.execute_command("nombre",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia el UUID de la GPU. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+u",category=script_category)
	def script_gpu_uuid(self, gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("uuid",ui.message)
			else:
				self.execute_command("uuid",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la versión del driver. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+v",category=script_category)
	def script_driver_version(self, gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("version_driver",ui.message)
			else:
				self.execute_command("version_driver",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la versión de la BIOS. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+control+v",category=script_category)
	def script_bios_version(self, gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("version_bios",ui.message)
			else:
				self.execute_command("version_bios",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la carga de la GPU. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+1",category=script_category)
	def script_gpu_load(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("carga",ui.message)
			else:
				self.execute_command("carga",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la carga de la memoria. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+2",category=script_category)
	def script_memory_load(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("carga_memoria",ui.message)
			else:
				self.execute_command("carga_memoria",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la memoria libre. {desc}").format(desc=script_description),gesture="kb:NVDA+alt+3",category=script_category)
	def script_free_memory(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("memoria_libre",ui.message)
			else:
				self.execute_command("memoria_libre",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la memoria utilizada. {desc}").format(desc=script_description),gesture="kb:NVDA+alt+4",category=script_category)
	def script_used_memory(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("memoria_usada",ui.message)
			else:
				self.execute_command("memoria_usada",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la memoria total. {desc}").format(desc=script_description),gesture="kb:NVDA+alt+5",category=script_category)
	def script_total_memory(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("memoria_total",ui.message)
			else:
				self.execute_command("memoria_total",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la temperatura. {desc}").format(desc=script_description),gesture="kb:NVDA+alt+6", category=script_category)
	def script_temperature(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("temperatura",ui.message)
			else:
				self.execute_command("temperatura",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia el consumo de energía. {desc}").format(desc=script_description),gesture="kb:NVDA+alt+7", category=script_category)
	def script_power_usage(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("consumo_energia",ui.message)
			else:
				self.execute_command("consumo_energia",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia el límite de energía. {desc}").format(desc=script_description),gesture="kb:NVDA+alt+8", category=script_category)
	def script_power_limit(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("consumo_limite",ui.message)
			else:
				self.execute_command("consumo_limite",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la cantidad de procesos cuda. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+9", category=script_category)
	def script_cuda_processes(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("procesos_cuda",ui.message)
			else:
				self.execute_command("procesos_cuda",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la memoria utilizada por procesos. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+0", category=script_category)
	def script_process_memory(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("procesos_memoria",ui.message)
			else:
				self.execute_command("procesos_memoria",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la velocidad del ventilador. {desc}").format(desc=script_description),gesture="kb:NVDA+alt+control+1", category=script_category)
	def script_fan_speed(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("velocidad_ventilador",ui.message)
			else:
				self.execute_command("velocidad_ventilador",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la frecuencia del reloj GPU. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+control+2",category=script_category)
	def script_gpu_clock(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("frecuencia_reloj",ui.message)
			else:
				self.execute_command("frecuencia_reloj",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la frecuencia máxima del reloj GPU. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+control+3",category=script_category)
	def script_max_gpu_clock(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("frecuencia_max_reloj",ui.message)
			else:
				self.execute_command("frecuencia_max_reloj",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la frecuencia del reloj SM. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+control+4",category=script_category)
	def script_sm_clock(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("frecuencia_reloj_sm",ui.message)
			else:
				self.execute_command("frecuencia_reloj_sm",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la frecuencia máxima del reloj SM. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+control+5",category=script_category)
	def script_max_sm_clock(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("frecuencia_max_reloj_sm",ui.message)
			else:
				self.execute_command("frecuencia_max_reloj_sm",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la frecuencia del reloj memoria. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+control+6",category=script_category)
	def script_memory_clock(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("frecuencia_reloj_memoria",ui.message)
			else:
				self.execute_command("frecuencia_reloj_memoria",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la frecuencia máxima del reloj memoria. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+control+7",category=script_category)
	def script_max_memory_clock(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("frecuencia_max_reloj_memoria",ui.message)
			else:
				self.execute_command("frecuencia_max_reloj_memoria",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia el TX Throughput. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+control+8",category=script_category)
	def script_tx_throughput(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("tx_throughput",ui.message)
			else:
				self.execute_command("tx_throughput",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia el RX Throughput. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+control+9",category=script_category)
	def script_rx_throughput(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("rx_throughput",ui.message)
			else:
				self.execute_command("rx_throughput",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia el estado de energía. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+control+0",category=script_category)
	def script_power_state(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("estado_energia",ui.message)
			else:
				self.execute_command("estado_energia",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	def terminate(self):
		# Use terminate from gpu-util class here
		self.gpu.terminate()
