import pynvml

#commands: name, uuid, driver_version, load, memory_load, memory_free, memory_used, memory_total, temperature, power_usage, power_limit, fan_speed, cuda_processes, process_memory, clock_frequency, sm_clock_frequency, memory_clock_frequency, max_clock_frequency, max_sm_clock_frequency, max_memory_clock_frequency, tx_throughput, rx_throughput, bios_version, power_state

def get_gpu_info(info_type,handle):
    if info_type == "name":
        gpu_name = pynvml.nvmlDeviceGetName(handle)
        return gpu_name.strip()

    elif info_type=="uuid":
        return pynvml.nvmlDeviceGetUUID(handle)

    elif info_type=="driver_version":
        return pynvml.nvmlSystemGetDriverVersion()

    elif info_type == "load":
        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
        return str(utilization.gpu)

    elif info_type=="memory_load":
        utilization_memory=pynvml.nvmlDeviceGetUtilizationRates(handle)
        return str(utilization_memory.memory)

    elif info_type == "memory_free":
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        return str(memory_info.free)

    elif info_type == "memory_used":
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        return str(memory_info.used)

    elif info_type == "memory_total":
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        return str(memory_info.total)

    elif info_type == "temperature":
        temperature = pynvml.nvmlDeviceGetTemperature(
            handle, pynvml.NVML_TEMPERATURE_GPU
        )
        return str(temperature)

    elif info_type == "power_usage":
        power_usage = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
        return f"{power_usage:.2f}"

    elif info_type=="power_limit":
        power_limit=pynvml.nvmlDeviceGetPowerManagementLimit(handle) / 1000.0
        return f"{power_limit:.2f}"

    elif info_type == "fan_speed":
        fan_speed = pynvml.nvmlDeviceGetFanSpeed(handle)
        return str(fan_speed)

    elif info_type == "cuda_processes":
        cuda_processes = pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
        return str(len(cuda_processes))

    elif info_type=="process_memory":
        processes=pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
        total_process_memory = 0
        for proc in processes:
            if proc.usedGpuMemory is not None:
                total_process_memory += proc.usedGpuMemory
        return str(total_process_memory)

    elif info_type == "clock_frequency":
        clock_graphics_current = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
        return str(clock_graphics_current)

    elif info_type=="sm_clock_frequency":
        clock_SM=pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_SM)
        return str(clock_SM)

    elif info_type=="memory_clock_frequency":
        clock_memory=pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_MEM)
        return str(clock_memory)

    elif info_type=="max_clock_frequency":
        clock_max=pynvml.nvmlDeviceGetMaxClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
        return str(clock_max)

    elif info_type=="max_sm_clock_frequency":
        clock_sm_max=pynvml.nvmlDeviceGetMaxClockInfo(handle, pynvml.NVML_CLOCK_SM)
        return str(clock_sm_max)

    elif info_type=="max_memory_clock_frequency":
        clock_memory_max=pynvml.nvmlDeviceGetMaxClockInfo(handle, pynvml.NVML_CLOCK_MEM)
        return str(clock_memory_max)

    elif info_type=="tx_throughput":
        tx=pynvml.nvmlDeviceGetPcieThroughput(handle, pynvml.NVML_PCIE_UTIL_TX_BYTES)
        return str(tx)

    elif info_type=="rx_throughput":
        rx=pynvml.nvmlDeviceGetPcieThroughput(handle, pynvml.NVML_PCIE_UTIL_RX_BYTES)
        return str(rx)

    elif info_type=="bios_version":
        bios_version=pynvml.nvmlDeviceGetVbiosVersion(handle)
        return bios_version

    elif info_type=="power_state":
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
