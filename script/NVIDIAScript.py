import pynvml

#comandos: nombre, uuid, version_driver, carga, carga_memoria ,memoria_libre, memoria_usada, memoria_total, temperatura, consumo_energia, consumo_limite, velocidad_ventilador, procesos_cuda, procesos_memoria, frecuencia_reloj, frecuencia_reloj_sm, frecuencia_reloj_memoria, frecuencia_max_reloj, frecuencia_max_reloj_sm, frecuencia_max_reloj_memoria, tx_throughput, rx_throughput, version_bios, estado_energia

def get_gpu_info(info_type,handle):
    if info_type == "nombre":
        gpu_name = pynvml.nvmlDeviceGetName(handle)
        return gpu_name.strip()

    elif info_type=="uuid":
        return pynvml.nvmlDeviceGetUUID(handle)

    elif info_type=="version_driver":
        return pynvml.nvmlSystemGetDriverVersion()

    elif info_type == "carga":
        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
        return str(utilization.gpu)

    elif info_type=="carga_memoria":
        utilization_memory=pynvml.nvmlDeviceGetUtilizationRates(handle)
        return str(utilization_memory.memory)

    elif info_type == "memoria_libre":
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        return str(memory_info.free)

    elif info_type == "memoria_usada":
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        return str(memory_info.used)

    elif info_type == "memoria_total":
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        return str(memory_info.total)

    elif info_type == "temperatura":
        temperature = pynvml.nvmlDeviceGetTemperature(
            handle, pynvml.NVML_TEMPERATURE_GPU
        )
        return str(temperature)

    elif info_type == "consumo_energia":
        power_usage = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
        return f"{power_usage:.2f}"

    elif info_type=="consumo_limite":
        power_limit=pynvml.nvmlDeviceGetPowerManagementLimit(handle) / 1000.0
        return f"{power_limit:.2f}"

    elif info_type == "velocidad_ventilador":
        fan_speed = pynvml.nvmlDeviceGetFanSpeed(handle)
        return str(fan_speed)

    elif info_type == "procesos_cuda":
        cuda_processes = pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
        return str(len(cuda_processes))

    elif info_type=="procesos_memoria":
        processes=pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
        total_process_memory = 0
        for proc in processes:
            if proc.usedGpuMemory is not None:
                total_process_memory += proc.usedGpuMemory
        return str(total_process_memory)

    elif info_type == "frecuencia_reloj":
        clock_graphics_current = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
        return str(clock_graphics_current)

    elif info_type=="frecuencia_reloj_sm":
        clock_SM=pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_SM)
        return str(clock_SM)

    elif info_type=="frecuencia_reloj_memoria":
        clock_memory=pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_MEM)
        return str(clock_memory)

    elif info_type=="frecuencia_max_reloj":
        clock_max=pynvml.nvmlDeviceGetMaxClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
        return str(clock_max)

    elif info_type=="frecuencia_max_reloj_sm":
        clock_sm_max=pynvml.nvmlDeviceGetMaxClockInfo(handle, pynvml.NVML_CLOCK_SM)
        return str(clock_sm_max)

    elif info_type=="frecuencia_max_reloj_memoria":
        clock_memory_max=pynvml.nvmlDeviceGetMaxClockInfo(handle, pynvml.NVML_CLOCK_MEM)
        return str(clock_memory_max)

    elif info_type=="tx_throughput":
        tx=pynvml.nvmlDeviceGetPcieThroughput(handle, pynvml.NVML_PCIE_UTIL_TX_BYTES)
        return str(tx)

    elif info_type=="rx_throughput":
        rx=pynvml.nvmlDeviceGetPcieThroughput(handle, pynvml.NVML_PCIE_UTIL_RX_BYTES)
        return str(rx)

    elif info_type=="version_bios":
        bios_version=pynvml.nvmlDeviceGetVbiosVersion(handle)
        return bios_version

    elif info_type=="estado_energia":
        power_state=pynvml.nvmlDeviceGetPowerState(handle)
        return str(power_state)

    else:
        return "ERROR"



if __name__ == "__main__":
    while True:
        user_input = input().strip().lower()
        if user_input == "exit":
            break
        try:
            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            result = get_gpu_info(user_input,handle)
            print(result)
        except pynvml.NVMLError as e:
            print(f"ERROR:{str(e)}")
        finally:
            pynvml.nvmlShutdown()
