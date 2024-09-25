# NVIDIA Monitor add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file LICENSE for more details.
# Copyright (C) 2024 José Perez <perezhuancajose@gmail.com> and ayoub <ayoubelbak13@gmail.com>

import globalPluginHandler
from scriptHandler import script,getLastScriptRepeatCount
import ui
import os
import subprocess
import globalVars
import api
import addonHandler
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
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        self.ruta = os.path.join(os.path.dirname(__file__), "scriptNvidia", "script.exe")


    #For translators
    script_category=_("NVIDIAMonitor")
    script_descripcion=_("Si se pulsa dos veces, copia esta información al portapapeles.")


    #For translators
    @script(description=_(f"Anuncia el nombre de la GPU. {script_descripcion}"), gesture="kb:NVDA+alt+g",category=script_category)
    def script_nombre_grafica(self, gesture):
        try:
            if getLastScriptRepeatCount() ==0:
                resultado = subprocess.run(
                    [self.ruta, "nombre"],check=True ,capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                ui.message(resultado.stdout)
            else:
                resultado = subprocess.run(
                    [self.ruta, "nombre"],check=True ,capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                api.copyToClip(resultado.stdout,notify=True)
        except Exception as e:
            ui.message("Ocurrió un error al obtener información sobre la GPU")


    #For translators
    @script(description=_(f"Anuncia la carga de la GPU. {script_descripcion}"), gesture="kb:NVDA+alt+1",category=script_category)
    def script_carga(self,gesture):
        try:
            if getLastScriptRepeatCount() ==0:
                resultado = subprocess.run(
                    [self.ruta, "carga"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                ui.message(resultado.stdout)
            else:
                resultado = subprocess.run(
                    [self.ruta, "carga"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                api.copyToClip(resultado.stdout,notify=True)
        except Exception as e:
            ui.message("Ocurrió un error al obtener información sobre la GPU")


    #For translators
    @script(description=_(f"Anuncia la memoria libre. {script_descripcion}"),gesture="kb:NVDA+alt+2",category=script_category)
    def script_memoria_libre(self,gesture):
        try:
            if getLastScriptRepeatCount() ==0:
                resultado = subprocess.run(
                    [self.ruta, "memoria_libre"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                ui.message(resultado.stdout)
            else:
                resultado = subprocess.run(
                    [self.ruta, "memoria_libre"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                api.copyToClip(resultado.stdout,notify=True)
        except Exception as e:
            ui.message("Ocurrió un error al obtener información sobre la GPU")


    #For translators
    @script(description=_(f"Anuncia la memoria utilizada. {script_descripcion}"),gesture="kb:NVDA+alt+3",category=script_category)
    def script_memoria_usada(self,gesture):
        try:
            if getLastScriptRepeatCount() ==0:
                resultado = subprocess.run(
                    [self.ruta, "memoria_usada"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                ui.message(resultado.stdout)
            else:
                resultado = subprocess.run(
                    [self.ruta, "memoria_usada"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                api.copyToClip(resultado.stdout,notify=True)
        except Exception as e:
            ui.message("Ocurrió un error al obtener información sobre la GPU")


    #For translators
    @script(description=_(f"Anuncia la memoria total. {script_descripcion}"),gesture="kb:NVDA+alt+4",category=script_category)
    def script_memoria_total(self,gesture):
        try:
            if getLastScriptRepeatCount() ==0:
                resultado = subprocess.run(
                    [self.ruta, "memoria_total"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                ui.message(resultado.stdout)
            else:
                resultado = subprocess.run(
                    [self.ruta, "memoria_total"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                api.copyToClip(resultado.stdout,notify=True)
        except Exception as e:
            ui.message("Ocurrió un error al obtener información sobre la GPU")


    #For translators
    @script(description=_(f"Anuncia la temperatura. {script_descripcion}"),gesture="kb:NVDA+alt+5", category=script_category)
    def script_temperatura(self,gesture):
        try:
            if getLastScriptRepeatCount() ==0:
                resultado = subprocess.run(
                    [self.ruta, "temperatura"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                ui.message(resultado.stdout)
            else:
                resultado = subprocess.run(
                    [self.ruta, "temperatura"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                api.copyToClip(resultado.stdout,notify=True)
        except Exception as e:
            ui.message("Ocurrió un error al obtener información sobre la GPU")


    #For translators
    @script(description=_(f"Anuncia el consumo de energía. {script_descripcion}"),gesture="kb:NVDA+alt+6", category=script_category)
    def script_consumo(self,gesture):
        try:
            if getLastScriptRepeatCount() ==0:
                resultado = subprocess.run(
                    [self.ruta, "consumo_energia"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                ui.message(resultado.stdout)
            else:
                resultado = subprocess.run(
                    [self.ruta, "consumo_energia"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                api.copyToClip(resultado.stdout,notify=True)
        except Exception as e:
            ui.message("Ocurrió un error al obtener información sobre la GPU")


    #For translators
    @script(description=_(f"Anuncia la velocidad del ventilador. {script_descripcion}"),gesture="kb:NVDA+alt+7", category=script_category)
    def script_ventilador(self,gesture):
        try:
            if getLastScriptRepeatCount() ==0:
                resultado = subprocess.run(
                    [self.ruta, "velocidad_ventilador"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                ui.message(resultado.stdout)
            else:
                resultado = subprocess.run(
                    [self.ruta, "velocidad_ventilador"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                api.copyToClip(resultado.stdout,notify=True)
        except Exception as e:
            ui.message("Ocurrió un error al obtener información sobre la GPU")


    #For translators
    @script(description=_(f"Anuncia la cantidad de procesos cuda. {script_descripcion}"), gesture="kb:NVDA+alt+8", category=script_category)
    def script_cudas(self,gesture):
        try:
            if getLastScriptRepeatCount() ==0:
                resultado = subprocess.run(
                    [self.ruta, "procesos_cuda"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                ui.message(resultado.stdout)
            else:
                resultado = subprocess.run(
                    [self.ruta, "procesos_cuda"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                api.copyToClip(resultado.stdout,notify=True)
        except Exception as e:
            ui.message("Ocurrió un error al obtener información sobre la GPU")


    #For translators
    @script(description=_(f"Anuncia la frecuencia del reloj. {script_descripcion}"), gesture="kb:NVDA+alt+9",category=script_category)
    def script_frecuencia(self,gesture):
        try:
            if getLastScriptRepeatCount() ==0:
                resultado = subprocess.run(
                    [self.ruta, "frecuencia_reloj"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                ui.message(resultado.stdout)
            else:
                resultado = subprocess.run(
                    [self.ruta, "frecuencia_reloj"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                api.copyToClip(resultado.stdout,notify=True)
        except Exception as e:
            ui.message("Ocurrió un error al obtener información sobre la GPU")
