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
	script_descripcion=_("Si se pulsa dos veces, copia esta información al portapapeles.")
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		# Inicializar gpu_util aquí
		self.gpu=GPUMonitor()

	def ejecutar_comando(self, comando, cb):
		self.gpu.ejecutar_comando(comando, cb)

	#For translators
	@script(description=_("Anuncia el nombre de la GPU. {desc}").format(desc=script_descripcion), gesture="kb:NVDA+alt+g",category=script_category)
	def script_nombre_grafica(self, gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("nombre",ui.message)
			else:
				self.ejecutar_comando("nombre",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia el UUID de la GPU. {desc}").format(desc=script_descripcion), gesture="kb:NVDA+alt+u",category=script_category)
	def script_uuid_grafica(self, gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("uuid",ui.message)
			else:
				self.ejecutar_comando("uuid",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la versión del driver. {desc}").format(desc=script_descripcion), gesture="kb:NVDA+alt+v",category=script_category)
	def script_version_driver(self, gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("version_driver",ui.message)
			else:
				self.ejecutar_comando("version_driver",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la versión de la BIOS. {desc}").format(desc=script_descripcion), gesture="kb:NVDA+alt+control+v",category=script_category)
	def script_version_bios(self, gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("version_bios",ui.message)
			else:
				self.ejecutar_comando("version_bios",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la carga de la GPU. {desc}").format(desc=script_descripcion), gesture="kb:NVDA+alt+1",category=script_category)
	def script_carga(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("carga",ui.message)
			else:
				self.ejecutar_comando("carga",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la carga de la memoria. {desc}").format(desc=script_descripcion), gesture="kb:NVDA+alt+2",category=script_category)
	def script_carga_memoria(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("carga_memoria",ui.message)
			else:
				self.ejecutar_comando("carga_memoria",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la memoria libre. {desc}").format(desc=script_descripcion),gesture="kb:NVDA+alt+3",category=script_category)
	def script_memoria_libre(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("memoria_libre",ui.message)
			else:
				self.ejecutar_comando("memoria_libre",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la memoria utilizada. {desc}").format(desc=script_descripcion),gesture="kb:NVDA+alt+4",category=script_category)
	def script_memoria_usada(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("memoria_usada",ui.message)
			else:
				self.ejecutar_comando("memoria_usada",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la memoria total. {desc}").format(desc=script_descripcion),gesture="kb:NVDA+alt+5",category=script_category)
	def script_memoria_total(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("memoria_total",ui.message)
			else:
				self.ejecutar_comando("memoria_total",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la temperatura. {desc}").format(desc=script_descripcion),gesture="kb:NVDA+alt+6", category=script_category)
	def script_temperatura(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("temperatura",ui.message)
			else:
				self.ejecutar_comando("temperatura",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia el consumo de energía. {desc}").format(desc=script_descripcion),gesture="kb:NVDA+alt+7", category=script_category)
	def script_consumo(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("consumo_energia",ui.message)
			else:
				self.ejecutar_comando("consumo_energia",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia el límite de energía. {desc}").format(desc=script_descripcion),gesture="kb:NVDA+alt+8", category=script_category)
	def script_limite_energia(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("consumo_limite",ui.message)
			else:
				self.ejecutar_comando("consumo_limite",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la cantidad de procesos cuda. {desc}").format(desc=script_descripcion), gesture="kb:NVDA+alt+9", category=script_category)
	def script_cudas(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("procesos_cuda",ui.message)
			else:
				self.ejecutar_comando("procesos_cuda",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la memoria utilizada por procesos. {desc}").format(desc=script_descripcion), gesture="kb:NVDA+alt+0", category=script_category)
	def script_procesos_memoria(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("procesos_memoria",ui.message)
			else:
				self.ejecutar_comando("procesos_memoria",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la velocidad del ventilador. {desc}").format(desc=script_descripcion),gesture="kb:NVDA+alt+control+1", category=script_category)
	def script_ventilador(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("velocidad_ventilador",ui.message)
			else:
				self.ejecutar_comando("velocidad_ventilador",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la frecuencia del reloj GPU. {desc}").format(desc=script_descripcion), gesture="kb:NVDA+alt+control+2",category=script_category)
	def script_frecuencia(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("frecuencia_reloj",ui.message)
			else:
				self.ejecutar_comando("frecuencia_reloj",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la frecuencia máxima del reloj GPU. {desc}").format(desc=script_descripcion), gesture="kb:NVDA+alt+control+3",category=script_category)
	def script_frecuencia_max(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("frecuencia_max_reloj",ui.message)
			else:
				self.ejecutar_comando("frecuencia_max_reloj",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la frecuencia del reloj SM. {desc}").format(desc=script_descripcion), gesture="kb:NVDA+alt+control+4",category=script_category)
	def script_frecuencia_sm(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("frecuencia_reloj_sm",ui.message)
			else:
				self.ejecutar_comando("frecuencia_reloj_sm",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la frecuencia máxima del reloj SM. {desc}").format(desc=script_descripcion), gesture="kb:NVDA+alt+control+5",category=script_category)
	def script_frecuencia_max_sm(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("frecuencia_max_reloj_sm",ui.message)
			else:
				self.ejecutar_comando("frecuencia_max_reloj_sm",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la frecuencia del reloj memoria. {desc}").format(desc=script_descripcion), gesture="kb:NVDA+alt+control+6",category=script_category)
	def script_frecuencia_memoria(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("frecuencia_reloj_memoria",ui.message)
			else:
				self.ejecutar_comando("frecuencia_reloj_memoria",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia la frecuencia máxima del reloj memoria. {desc}").format(desc=script_descripcion), gesture="kb:NVDA+alt+control+7",category=script_category)
	def script_frecuencia_max_memoria(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("frecuencia_max_reloj_memoria",ui.message)
			else:
				self.ejecutar_comando("frecuencia_max_reloj_memoria",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia el TX Throughput. {desc}").format(desc=script_descripcion), gesture="kb:NVDA+alt+control+8",category=script_category)
	def script_tx_throughput(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("tx_throughput",ui.message)
			else:
				self.ejecutar_comando("tx_throughput",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia el RX Throughput. {desc}").format(desc=script_descripcion), gesture="kb:NVDA+alt+control+9",category=script_category)
	def script_rx_throughput(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("rx_throughput",ui.message)
			else:
				self.ejecutar_comando("rx_throughput",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	#For translators
	@script(description=_("Anuncia el estado de energía. {desc}").format(desc=script_descripcion), gesture="kb:NVDA+alt+control+0",category=script_category)
	def script_estado_energia(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.ejecutar_comando("estado_energia",ui.message)
			else:
				self.ejecutar_comando("estado_energia",lambda resultado: api.copyToClip(resultado,notify=True))
		else:
			ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

	def terminate(self):
		# utilizar terminate de la clase gpu-util aquí
		self.gpu.terminate()
