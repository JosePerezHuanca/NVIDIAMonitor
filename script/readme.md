# NVIDIA Script

This script allows querying various parameters of NVIDIA graphics cards. It is designed to be called via subprocess from the add-on, since the required DLL (nvml.dll) is 64-bit, while NVDA is 32-bit.

## Requirements

- Python 3.11 or higher
- pynvml
- cx_Freeze

## How to compile

It is recommended to use a virtual environment:
- Install dependencies: `pip install -r requirements.txt`
- Build with: `python setup.py build`
- After compiling, copy the contents of the build folder to addon/globalPlugins/NVIDIAMonitor. It is recommended to rename the folder containing the executable to `data`

## How to use

When running the script, a command such as name, uuid, driver_version, etc., is expected. The `exit` command closes the script.

## List of commands

Note: Some information parameters may not be compatible or supported depending on the graphics card.

- `name`: Returns the GPU name
- `uuid`: Returns the GPU UUID
- `driver_version`: Returns the driver version
- `bios_version`: Returns the BIOS version
- `load`: Returns the GPU load. E.g., 5%
- `memory_load`: Returns the memory load
- `memory_free`: Free GPU memory. E.g., 3.84 GB
- `memory_used`: Used GPU memory. E.g., 1.00 GB
- `memory_total`: Total GPU memory. E.g., 4.00 GB
- `temperature`: GPU temperature. E.g., 35°C
- `power_usage`: GPU power consumption. E.g., 17.89 W
- `power_limit`: Power limit
- `fan_speed`: Fan speed as a percentage
- `cuda_processes`: Returns the number of CUDA processes
- `process_memory`: Returns the memory used by processes
- `clock_frequency`: Returns the GPU clock frequency. E.g., 1380 MHz
- `max_clock_frequency`: Returns the maximum GPU clock frequency
- `sm_clock_frequency`: Returns the SM clock frequency
- `max_sm_clock_frequency`: Returns the maximum SM clock frequency
- `memory_clock_frequency`: Returns the memory clock frequency
- `max_memory_clock_frequency`: Returns the maximum memory clock frequency
- `tx_throughput`: Returns the TX Throughput
- `rx_throughput`: Returns the RX Throughput
- `power_state`: Returns the power state
- `exit`: Closes the script
