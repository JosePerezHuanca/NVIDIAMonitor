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
	script_description=_("If pressed twice, copies this information to the clipboard.")
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		# Initialize gpu_util here
		self.gpu=GPUMonitor()

	def execute_command(self, command, cb):
		self.gpu.execute_command(command, cb)

	#For translators
	@script(description=_("Announces the GPU name. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+g",category=script_category)
	def script_gpu_name(self, gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("name",ui.message)
			else:
				self.execute_command("name",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the GPU UUID. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+u",category=script_category)
	def script_gpu_uuid(self, gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("uuid",ui.message)
			else:
				self.execute_command("uuid",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the driver version. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+v",category=script_category)
	def script_driver_version(self, gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("driver_version",ui.message)
			else:
				self.execute_command("driver_version",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the BIOS version. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+control+v",category=script_category)
	def script_bios_version(self, gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("bios_version",ui.message)
			else:
				self.execute_command("bios_version",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the GPU load. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+1",category=script_category)
	def script_gpu_load(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("load",ui.message)
			else:
				self.execute_command("load",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the memory load. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+2",category=script_category)
	def script_memory_load(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("memory_load",ui.message)
			else:
				self.execute_command("memory_load",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the free memory. {desc}").format(desc=script_description),gesture="kb:NVDA+alt+3",category=script_category)
	def script_free_memory(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("memory_free",ui.message)
			else:
				self.execute_command("memory_free",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the used memory. {desc}").format(desc=script_description),gesture="kb:NVDA+alt+4",category=script_category)
	def script_used_memory(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("memory_used",ui.message)
			else:
				self.execute_command("memory_used",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the total memory. {desc}").format(desc=script_description),gesture="kb:NVDA+alt+5",category=script_category)
	def script_total_memory(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("memory_total",ui.message)
			else:
				self.execute_command("memory_total",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the temperature. {desc}").format(desc=script_description),gesture="kb:NVDA+alt+6", category=script_category)
	def script_temperature(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("temperature",ui.message)
			else:
				self.execute_command("temperature",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the power consumption. {desc}").format(desc=script_description),gesture="kb:NVDA+alt+7", category=script_category)
	def script_power_usage(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("power_usage",ui.message)
			else:
				self.execute_command("power_usage",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the power limit. {desc}").format(desc=script_description),gesture="kb:NVDA+alt+8", category=script_category)
	def script_power_limit(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("power_limit",ui.message)
			else:
				self.execute_command("power_limit",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the number of CUDA processes. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+9", category=script_category)
	def script_cuda_processes(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("cuda_processes",ui.message)
			else:
				self.execute_command("cuda_processes",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the memory used by processes. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+0", category=script_category)
	def script_process_memory(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("process_memory",ui.message)
			else:
				self.execute_command("process_memory",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the fan speed. {desc}").format(desc=script_description),gesture="kb:NVDA+alt+control+1", category=script_category)
	def script_fan_speed(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("fan_speed",ui.message)
			else:
				self.execute_command("fan_speed",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the GPU clock frequency. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+control+2",category=script_category)
	def script_gpu_clock(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("clock_frequency",ui.message)
			else:
				self.execute_command("clock_frequency",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the maximum GPU clock frequency. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+control+3",category=script_category)
	def script_max_gpu_clock(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("max_clock_frequency",ui.message)
			else:
				self.execute_command("max_clock_frequency",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the SM clock frequency. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+control+4",category=script_category)
	def script_sm_clock(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("sm_clock_frequency",ui.message)
			else:
				self.execute_command("sm_clock_frequency",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the maximum SM clock frequency. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+control+5",category=script_category)
	def script_max_sm_clock(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("max_sm_clock_frequency",ui.message)
			else:
				self.execute_command("max_sm_clock_frequency",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the memory clock frequency. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+control+6",category=script_category)
	def script_memory_clock(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("memory_clock_frequency",ui.message)
			else:
				self.execute_command("memory_clock_frequency",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the maximum memory clock frequency. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+control+7",category=script_category)
	def script_max_memory_clock(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("max_memory_clock_frequency",ui.message)
			else:
				self.execute_command("max_memory_clock_frequency",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the TX throughput. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+control+8",category=script_category)
	def script_tx_throughput(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("tx_throughput",ui.message)
			else:
				self.execute_command("tx_throughput",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the RX throughput. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+control+9",category=script_category)
	def script_rx_throughput(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("rx_throughput",ui.message)
			else:
				self.execute_command("rx_throughput",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	#For translators
	@script(description=_("Announces the power state. {desc}").format(desc=script_description), gesture="kb:NVDA+alt+control+0",category=script_category)
	def script_power_state(self,gesture):
		if winVersion.getWinVer().processorArchitecture=="AMD64":
			if getLastScriptRepeatCount() ==0:
				self.execute_command("power_state",ui.message)
			else:
				self.execute_command("power_state",lambda result: api.copyToClip(result,notify=True))
		else:
			ui.message(_("Error: your processor architecture is not compatible"))

	def terminate(self):
		# Use terminate from gpu-util class here
		self.gpu.terminate()
