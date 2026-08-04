# Script NVIDIA

Este script permite consultar varios parámetros de las tarjetas gráficas NVIDIA. Se utiliza para llamarlo mediante subprocess desde el complemento, ya que la DLL que se necesita (nvml.dll) es de 64 bits, mientras que NVDA es de 32 bits.

## Requisitos

- Python 3.11 o superior
- pynvml
- cx_Freeze

## Cómo compilar

Se recomienda utilizar un entorno virtual:
- Instalar las dependencias: `pip install -r requirements.txt`
- Compilar con: `python setup.py build`
- Luego de compilar copiar el contenido de la carpeta build a addon/globalPlugins/NVIDIAMonitor. Se recomienda renombrar la carpeta que contiene el ejecutable a data

## Cómo utilizar

Al ejecutar el script, se espera que se ingrese un comando como name, uuid, driver_version etc. El comando exit cierra el script.

## Lista de comandos

Nota: algúnos parámetros de información pueden no ser compatibles o estár soportados dependiendo de la tarjeta gráfica.

- `name`: Devuelve el nombre de la GPU
- `uuid`: Devuelve el UUID de la GPU
- `driver_version`: Devuelve la versión del driver
- `bios_version`: Devuelve la versión de la BIOS
- `load`: Devuelve la carga de la GPU. Ej: 5%
- `memory_load`: Devuelve la carga de la memoria
- `memory_free`: Memoria libre de la GPU. Ej: 3.84 GB
- `memory_used`: Memoria utilizada de la GPU. Ej: 1.00 GB
- `memory_total`: Memoria total de la GPU. Ej: 4.00 GB
- `temperature`: Temperatura de la GPU. Ej: 35°C
- `power_usage`: Consumo de la GPU. Ej: 17.89 W
- `power_limit`: Límite de energía
- `fan_speed`: Velocidad del ventilador en porcentaje.
- `cuda_processes`: Devuelve la cantidad de procesos CUDA.
- `process_memory`: Devuelve la memoria utilizada por los procesos
- `clock_frequency`: Devuelve la frecuencia del relojGPU. Ej: 1380 MHz
- `max_clock_frequency`: Devuelve la frecuencia máxima del reloj GPU
- `sm_clock_frequency`: Devuelve la frecuencia del reloj SM
- `max_sm_clock_frequency`: Devuelve la frecuencia máxima del reloj SM
- `memory_clock_frequency`: Devuelve la frecuencia del reloj memoria
- `max_memory_clock_frequency`: Devuelve la frecuencia máxima del reloj memoria
- `tx_throughput`: Devuelve el TX Throughput
- `rx_throughput`: Devuelve el RX Throughput
- `power_state`: Devuelve el estado de energía
- `exit`: Cierra el script
