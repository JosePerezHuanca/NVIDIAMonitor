# 英伟达监视器

本插件允许您监控英伟达（NVIDIA）显卡的各项参数，例如名称、已用显存、可用显存、总显存、功耗、温度等。

## 快捷键

注意：某些信息参数可能会因显卡型号的不同而不兼容或不受支持。
以下所有快捷键都可以在“输入手势”中的“英伟达监视器 (NVIDIAMonitor)”类别进行自定义。连续按两次快捷键可将该信息复制到剪贴板。

* NVDA + alt + g：播报 GPU 名称/型号。

* NVDA + alt + u：播报 GPU UUID。

* NVDA + alt + v：播报驱动程序版本。

* NVDA + ctrl + alt + v：播报 BIOS 版本。

* NVDA + alt + 1：播报 GPU 负载。

* NVDA + alt + 2：播报显存负载。

* NVDA + alt + 3：播报可用显存。

* NVDA + alt + 4：播报已用显存。

* NVDA + alt + 5：播报总显存。

* NVDA + alt + 6：播报 GPU 温度。

* NVDA + alt + 7：播报功耗。

* NVDA + alt + 8：播报功耗限制。

* NVDA + alt + 9：播报 CUDA 进程数量。

* NVDA + alt + 0：播报进程占用的显存。

* NVDA + ctrl + alt + 1：播报风扇转速。

* NVDA + ctrl + alt + 2：播报 GPU 核心时钟频率。

* NVDA + ctrl + alt + 3：播报最高 GPU 核心时钟频率。

* NVDA + ctrl + alt + 4：播报 SM 时钟频率。

* NVDA + ctrl + alt + 5：播报最高 SM 时钟频率。

* NVDA + ctrl + alt + 6：播报显存时钟频率。

* NVDA + ctrl + alt + 7：播报最高显存时钟频率。

* NVDA + ctrl + alt + 8：播报发送 (TX) 吞吐量。

* NVDA + ctrl + alt + 9：播报接收 (RX) 吞吐量。

* NVDA + ctrl + alt + 0：播报电源状态。

## 更新日志

### 版本 2.1

* 修复了直接调用 pynvml 出现的问题。

### 版本 2.0

* 兼容 NVDA 2026.1。

* 从此版本开始，在最新版本的 NVDA 上运行时，插件将直接调用 pynvml 库，而不是使用外部工具。

### 版本 1.0

* 对信息检索脚本进行了多项更改、修复和改进。

* 错误现在会记录在位于 NVDA 配置文件夹中名为 NVIDIAMonitor.log 的文件中。

* 兼容 NVDA 2025.1。

* 重新分配了部分现有的快捷键。

* 添加了新的快捷键：

  * GPU UUID：NVDA + alt + u

  * 驱动程序版本：NVDA + alt + v

  * BIOS 版本：NVDA + ctrl + alt + v

  * 显存负载：NVDA + alt + 2

  * 功耗限制：NVDA + alt + 8

  * 进程占用的显存：NVDA + alt + 0

  * 最高 GPU 核心时钟频率：NVDA + ctrl + alt + 3

  * SM 时钟频率：NVDA + ctrl + alt + 4

  * 最高 SM 时钟频率：NVDA + ctrl + alt + 5

  * 显存时钟频率：NVDA + ctrl + alt + 6

  * 最高显存时钟频率：NVDA + ctrl + alt + 7

  * 发送 (TX) 吞吐量：NVDA + ctrl + alt + 8

  * 接收 (RX) 吞吐量：NVDA + ctrl + alt + 9

  * 电源状态：NVDA + ctrl + alt + 0

### 版本 0.2

* 连续按两次快捷键现在可将信息复制到剪贴板。

* 进行了各项改进和优化。

### 版本 0.1

* 插件初始版本。
