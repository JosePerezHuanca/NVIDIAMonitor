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
import threading
import winVersion
import time
import datetime
import tones
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
        self.ruta = os.path.join(os.path.dirname(__file__), "data", "NVIDIAScript.exe")
        self.resultados_cache={}
        self.cache_expiracion=1
        self.en_ejecucion=False
        self.proceso=None

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
            error_ruta=f"Error: El archivo no se encuentra en la ruta especificada: {self.ruta}"
            self.escribir_log(error_ruta)
            log.error(error_ruta)
            self.proceso=None
            return self.proceso
        except subprocess.CalledProcessError as e:
            self.en_ejecucion=False
            error_mensaje=f"Error al iniciar el proceso: {e.returncode} {e.cmd}"
            self.escribir_log(error_mensaje)
            log.error(error_mensaje)
            self.proceso=None
            return self.proceso



    #For translators
    script_category=_("NVIDIAMonitor")
    script_descripcion=_("Si se pulsa dos veces, copia esta información al portapapeles.")


    def ejecutar_comando(self,comando,cb):
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
                # Guardar el resultado en la caché
                self.resultados_cache[comando] = resultado, tiempo_actual
                return cb(resultado)
            except OSError as e:
                error_proceso=f"Error al escribir en el subprocess: {e}"
                self.escribir_log(error_proceso)
                log.error(error_proceso)
                return cb("Error al escribir en el proceso.")
        thread=threading.Thread(target=comando_hilo)
        thread.start()


    #For translators
    @script(description=_(f"Anuncia el nombre de la GPU. {script_descripcion}"), gesture="kb:NVDA+alt+g",category=script_category)
    def script_nombre_grafica(self, gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("nombre",ui.message)
            else:
                self.ejecutar_comando("nombre",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

    #For translators
    @script(description=_(f"Anuncia el UUID de la GPU. {script_descripcion}"), gesture="kb:NVDA+alt+u",category=script_category)
    def script_uuid_grafica(self, gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("uuid",ui.message)
            else:
                self.ejecutar_comando("uuid",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

    #For translators
    @script(description=_(f"Anuncia la versión del driver. {script_descripcion}"), gesture="kb:NVDA+alt+v",category=script_category)
    def script_version_driver(self, gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("version_driver",ui.message)
            else:
                self.ejecutar_comando("version_driver",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

    #For translators
    @script(description=_(f"Anuncia la versión de la BIOS. {script_descripcion}"), gesture="kb:NVDA+alt+control+v",category=script_category)
    def script_version_bios(self, gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("version_bios",ui.message)
            else:
                self.ejecutar_comando("version_bios",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

    #For translators
    @script(description=_(f"Anuncia la carga de la GPU. {script_descripcion}"), gesture="kb:NVDA+alt+1",category=script_category)
    def script_carga(self,gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("carga",ui.message)
            else:
                self.ejecutar_comando("carga",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

    #For translators
    @script(description=_(f"Anuncia la carga de la memoria. {script_descripcion}"), gesture="kb:NVDA+alt+2",category=script_category)
    def script_carga_memoria(self,gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("carga_memoria",ui.message)
            else:
                self.ejecutar_comando("carga_memoria",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

    #For translators
    @script(description=_(f"Anuncia la memoria libre. {script_descripcion}"),gesture="kb:NVDA+alt+3",category=script_category)
    def script_memoria_libre(self,gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("memoria_libre",ui.message)
            else:
                self.ejecutar_comando("memoria_libre",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))



    #For translators
    @script(description=_(f"Anuncia la memoria utilizada. {script_descripcion}"),gesture="kb:NVDA+alt+4",category=script_category)
    def script_memoria_usada(self,gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("memoria_usada",ui.message)
            else:
                self.ejecutar_comando("memoria_usada",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))



    #For translators
    @script(description=_(f"Anuncia la memoria total. {script_descripcion}"),gesture="kb:NVDA+alt+5",category=script_category)
    def script_memoria_total(self,gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("memoria_total",ui.message)
            else:
                self.ejecutar_comando("memoria_total",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))



    #For translators
    @script(description=_(f"Anuncia la temperatura. {script_descripcion}"),gesture="kb:NVDA+alt+6", category=script_category)
    def script_temperatura(self,gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("temperatura",ui.message)
            else:
                self.ejecutar_comando("temperatura",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))



    #For translators
    @script(description=_(f"Anuncia el consumo de energía. {script_descripcion}"),gesture="kb:NVDA+alt+7", category=script_category)
    def script_consumo(self,gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("consumo_energia",ui.message)
            else:
                self.ejecutar_comando("consumo_energia",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

    #For translators
    @script(description=_(f"Anuncia el límite de energía. {script_descripcion}"),gesture="kb:NVDA+alt+8", category=script_category)
    def script_limite_energia(self,gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("consumo_limite",ui.message)
            else:
                self.ejecutar_comando("consumo_limite",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

    #For translators
    @script(description=_(f"Anuncia la cantidad de procesos cuda. {script_descripcion}"), gesture="kb:NVDA+alt+9", category=script_category)
    def script_cudas(self,gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("procesos_cuda",ui.message)
            else:
                self.ejecutar_comando("procesos_cuda",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

    #For translators
    @script(description=_(f"Anuncia la memoria utilizada por procesos. {script_descripcion}"), gesture="kb:NVDA+alt+0", category=script_category)
    def script_procesos_memoria(self,gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("procesos_memoria",ui.message)
            else:
                self.ejecutar_comando("procesos_memoria",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

    #For translators
    @script(description=_(f"Anuncia la velocidad del ventilador. {script_descripcion}"),gesture="kb:NVDA+alt+control+1", category=script_category)
    def script_ventilador(self,gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("velocidad_ventilador",ui.message)
            else:
                self.ejecutar_comando("velocidad_ventilador",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

    #For translators
    @script(description=_(f"Anuncia la frecuencia del reloj GPU. {script_descripcion}"), gesture="kb:NVDA+alt+control+2",category=script_category)
    def script_frecuencia(self,gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("frecuencia_reloj",ui.message)
            else:
                resultado=self.ejecutar_comando("frecuencia_reloj",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

    #For translators
    @script(description=_(f"Anuncia la frecuencia máxima del reloj GPU. {script_descripcion}"), gesture="kb:NVDA+alt+control+3",category=script_category)
    def script_frecuencia_max(self,gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("frecuencia_max_reloj",ui.message)
            else:
                resultado=self.ejecutar_comando("frecuencia_max_reloj",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

    #For translators
    @script(description=_(f"Anuncia la frecuencia del reloj SM. {script_descripcion}"), gesture="kb:NVDA+alt+control+4",category=script_category)
    def script_frecuencia_sm(self,gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("frecuencia_reloj_sm",ui.message)
            else:
                resultado=self.ejecutar_comando("frecuencia_reloj_sm",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

    #For translators
    @script(description=_(f"Anuncia la frecuencia máxima del reloj SM. {script_descripcion}"), gesture="kb:NVDA+alt+control+5",category=script_category)
    def script_frecuencia_max_sm(self,gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("frecuencia_max_reloj_sm",ui.message)
            else:
                resultado=self.ejecutar_comando("frecuencia_max_reloj_sm",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

    #For translators
    @script(description=_(f"Anuncia la frecuencia del reloj memoria. {script_descripcion}"), gesture="kb:NVDA+alt+control+6",category=script_category)
    def script_frecuencia_memoria(self,gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("frecuencia_reloj_memoria",ui.message)
            else:
                resultado=self.ejecutar_comando("frecuencia_reloj_memoria",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

    #For translators
    @script(description=_(f"Anuncia la frecuencia máxima del reloj memoria. {script_descripcion}"), gesture="kb:NVDA+alt+control+7",category=script_category)
    def script_frecuencia_max_memoria(self,gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("frecuencia_max_reloj_memoria",ui.message)
            else:
                resultado=self.ejecutar_comando("frecuencia_max_reloj_memoria",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

    #For translators
    @script(description=_(f"Anuncia el TX Throughput. {script_descripcion}"), gesture="kb:NVDA+alt+control+8",category=script_category)
    def script_tx_throughput(self,gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("tx_throughput",ui.message)
            else:
                resultado=self.ejecutar_comando("tx_throughput",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

    #For translators
    @script(description=_(f"Anuncia el RX Throughput. {script_descripcion}"), gesture="kb:NVDA+alt+control+9",category=script_category)
    def script_rx_throughput(self,gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("rx_throughput",ui.message)
            else:
                resultado=self.ejecutar_comando("rx_throughput",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

    #For translators
    @script(description=_(f"Anuncia el estado de energía. {script_descripcion}"), gesture="kb:NVDA+alt+control+0",category=script_category)
    def script_estado_energia(self,gesture):
        if winVersion.getWinVer().processorArchitecture=="AMD64":
            if getLastScriptRepeatCount() ==0:
                self.ejecutar_comando("estado_energia",ui.message)
            else:
                resultado=self.ejecutar_comando("estado_energia",lambda resultado: api.copyToClip(resultado,notify=True))
        else:
            ui.message(_("Error: la arquitectura de tu procesador no es compatible"))

    def terminate(self):
        if self.proceso:
            if self.proceso.poll() is not None:
                self.en_ejecucion=False
                return
            try:
                # Enviamos el comando de salida
                self.proceso.stdin.write("exit\n")
                self.proceso.stdin.flush()
                # Terminar el proceso de manera controlada
                self.proceso.terminate()
                # Esperar a que termine completamente
                self.proceso.wait() 
                # Cerramos las conexiones de stdin, stdout, stderr
                self.proceso.stdin.close()
                self.proceso.stdout.close()
                self.proceso.stderr.close()
                self.en_ejecucion=False
            except Exception as e:
                error_terminate=f"Error al intentar terminar el proceso: {str(e)}"
                self.escribir_log(error_terminate)
                pass
