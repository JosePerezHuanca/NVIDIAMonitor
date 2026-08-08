# NVIDIA 监视器

该插件允许您跟踪 NVIDIA 显卡的各种参数，例如名称、已用内存、可用内存和总内存、功耗、温度等。

## 快捷键

注意：根据显卡的不同，某些信息参数可能不受支持或兼容。
以下所有快捷键均可在输入手势/NVDIA 监视器 类别中自定义。双击将信息复制到剪贴板。

- NVDA + alt + g：报告 GPU 名称/型号。
- NVDA + alt + u：报告 GPU UUID。
- NVDA + alt + v：报告驱动程序版本。
- NVDA + ctrl + alt + v：报告 BIOS 版本。
- NVDA + alt + 1：报告 GPU 加载。
- NVDA + alt + 2：报告内存加载。
- NVDA + alt + 3：报告可用内存。
- NVDA + alt + 4：报告已使用的内存。
- NVDA + alt + 5：报告总内存。
- NVDA + alt + 6：报告 GPU 温度。
- NVDA + alt + 7：报告功耗。
- NVDA + alt + 8：报告功率限制。
- NVDA + alt + 9：报告 CUDA 进程的数量。
- NVDA + alt + 0：报告进程使用的内存。
- NVDA + ctrl + alt + 1：报告风扇速度。
- NVDA + ctrl + alt + 2：报告 GPU 时钟频率。
- NVDA + ctrl + alt + 3：报告最大 GPU 时钟频率。
- NVDA + ctrl + alt + 4：报告 SM 时钟频率。
- NVDA + ctrl + alt + 5：报告最大 SM 时钟频率。
- NVDA + ctrl + alt + 6：报告内存时钟频率。
- NVDA + ctrl + alt + 7：报告最大内存时钟频率。
- NVDA + ctrl + alt + 8：报告 TX 吞吐量。
- NVDA + ctrl + alt + 9：报告 RX 吞吐量。
- NVDA + ctrl + alt + 0：报告电源状态。


## 变更日志

### 1.0 版

- 对获取信息的脚本进行了几处更改、修正和改进。
- 现在如果发生错误，它将存储在位于 NVDA 配置文件夹中的名为 NVIDIAMonitor.log 的文件中。
- 支持 NVDA 2025.1
- 一些现有的快捷方式已被重新分配。
- 添加了新的快捷键：
- GPU UUID：NVDA + alt + u
- 驱动程序版本：NVDA + alt + v
- BIOS 版本：NVDA + ctrl + alt + v
- 加载内存：NVDA + alt + 2
- 功率限制：NVDA + Alt + 8
- 进程使用的内存：NVDA + alt + 0
- 最大 GPU 时钟速度：NVDA + ctrl + alt + 3
- SM 时钟速度：NVDA + ctrl + alt + 4
- 最大 SM 时钟频率：NVDA + ctrl + alt + 5
- 内存时钟频率：NVDA + ctrl + alt + 6
- 最大内存时钟频率：NVDA + ctrl + alt + 7
- TX 吞吐量：NVDA + ctrl + alt + 8
- RX 吞吐量：NVDA + ctrl + alt + 9
- 电源状态：NVDA + ctrl + alt + 0

### 0.2 版

- 现在，如果您按两次快捷键，它就会将信息复制到剪贴板。
- 各种改进和优化。

### 0.1 版

- 插件的初始版本。
