<!-- Auto-mirrored from upstream `documentation-main/tutorials/guide_to_obtaining_stack_traces.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# DolphinDB API 卡住获取栈信息指南

## 1. 前言

在通过 DolphinDB 的各类 API 进行程序开发时，可能遭遇应用程序无响应（卡死）的情况。这类问题可能源于网络连接的意外中断、 DolphinDB 服务器端的状态异常、 API 库的内部处理逻辑，甚至是应用程序其他部分的资源争用。由于此类问题往往具有偶发性，且难以通过常规的日志输出定位根因，使得排查工作充满挑战。

此时，获取程序卡死瞬间的函数调用栈（Stack Trace）信息，就成为找到问题根源的关键。它能清晰展示各个线程在当时所执行的代码路径，从而极大地缩小排查范围，指引我们直击问题核心。

本文将系统性地介绍，针对不同语言的 DolphinDB API（包括 C++ API 、ODBC 、Python API 、Java API/JDBC 及 Go API ），如何运用平台特有的工具和技术，安全、有效地获取运行中程序的线程栈信息，为快速诊断和解决程序卡死问题提供一套实用的方法论。

## 2. 各个语言 API 获取栈信息

### 2.1. C++ API / ODBC 获取栈信息

C++ API 和 ODBC 都是 C/C++ 程序，我们在 Linux 上可以通过 pstack 或者 GDB 的方法获取栈信息。

**方法一：使用 pstack / gstack**

pstack（或部分系统中名为 gstack）是用于打印指定进程所有线程调用栈的命令行工具，通常系统自带或可通过包管理器安装。

1. 获取对应程序的 pid：
   `ps aux | grep 进程名称`

   ![](image/guide_to_obtaining_stack_traces/1.PNG)
2. 通过 pstack/gstack 获取对应进程的线程调用栈（注意：打印时会暂停目标进程以获取函数栈，完成之后进程恢复运行）：
   `gstack pid`

   ![](image/guide_to_obtaining_stack_traces/2.PNG)

**方法二：使用 GDB**

GDB 是 GNU 软件系统的标准调试器，具有良好的移植性，现已广泛用于多种类 UNIX 操作系统。GDB 支持调试 C、C++、Pascal 和 FORTRAN 等编程语言。某些系统缺少 pstack 或 gstack 程序时，可用 GDB 获取函数栈信息。一般系统自带或可通过包管理器安装。

1. 获取对应程序的 pid：
   `ps aux | grep 进程名称`

   ![](image/guide_to_obtaining_stack_traces/1.PNG)
2. 通过 GDB 获取对应进程的线程调用栈（注意：附加时会暂停目标进程，退出 GDB 之后进程恢复运行 ）：先附加到对应 pid 进程中
   `gdb attach --pid pid`
   在 GDB 中打印全部线程调用栈
   `thread apply all bt`

   ![](image/guide_to_obtaining_stack_traces/3.PNG)
3. 退出 GDB：
   `quit`

### 2.2. Python API 获取栈信息

**通过 py-spy 获取 Python 部分的栈信息**

py-spy 是一款 Python 程序的采样分析工具。它无需重启程序或修改代码，即可直观展示 Python 程序的耗时分布。该工具采用 Rust 语言编写以实现高效能，其极低的开销特性源于与被分析程序分离的运行机制——不驻留在同一进程空间。这使得 py-spy 能够安全地用于生产环境的 Python 代码诊断。py-spy 支持 Windows 和 Linux ，可以跨平台获取 Python 部分的栈信息。

1. 安装 py-spy：
   `pip install py-spy`
2. 获取对应程序的 pid：Linux下面获取 pid 的方法：
   `ps aux | grep 进程名`

   ![](image/guide_to_obtaining_stack_traces/4.PNG)
   Windows 下面可以通过任务管理器获取 pid。
   ![](image/guide_to_obtaining_stack_traces/5.PNG)
3. 通过 py-spy 获取对应进程的线程调用栈（注意：打印时会暂停目标进程以获取函数栈，完成之后进程恢复运行）：
   `py-spy dump -p pid`

![](image/guide_to_obtaining_stack_traces/6.PNG)

**通过 pstack/gstack/GDB 获取 C++ 部分的栈信息**

Python API 是对 C++ API 的封装，如果通过上面的 py-spy 定位到是 Python API 调用内部，则需要进一步分析底层 C++ 部分。此时可以通过 pstack/gstack/GDB 等工具获取 C++ 部分的栈内容。具体方法可以查看C++API / ODBC 获取栈信息该节内容。因为 pstack/gstack/GDB 等工具是 Linux 专用工具，所以 Python API的 C++ 部分的栈信息在 Windows 上面无法获取。

通过 gstack 获取（注意：打印时会暂停目标进程以获取函数栈，完成之后进程恢复运行）：

```
gstack pid
```

![](image/guide_to_obtaining_stack_traces/7.PNG)

### 2.3. Java API / JDBC 获取栈信息

jstack 是 Java 虚拟机自带的一种堆栈跟踪工具，用于生成当前时刻的线程快照。线程快照是当前 Java 虚拟机内存中每一条线程正在执行的方法堆栈的集合。通过 jstack 命令可以获取运行中的 Java API / JDBC 的函数栈。jstack支持 Linux 和 Windows。

1. 执行 jps 获取对应 pid（Linux 和 Windows 通用）:
   `jps`

   ![](image/guide_to_obtaining_stack_traces/8.PNG)
2. 执行 jstack 获取对应 java 进程的函数栈（注意：打印时会暂停目标进程以获取函数栈，完成之后进程恢复运行）：
   `jstack pid`

   ![](image/guide_to_obtaining_stack_traces/9.PNG)

### 2.4. Go API 获取栈信息

Delve (dlv) 是 Go 语言的调试器，提供类似 GDB 的简单且功能齐全的调试工具。可以通过 dlv 命令查看运行中 Go API 的函数栈。

1. 安装 Delve(dlv)： `go install
   github.com/go-delve/delve/cmd/dlv@latest`
2. 获取对应程序的 pid：Linux下面获取 pid 的方法： `ps aux | grep 进程名`

   ![](image/guide_to_obtaining_stack_traces/10.PNG)
    Windows 下面可以通过任务管理器获取 pid。
3. dlv 附加到对应程序进程（注意：附加时会暂停目标进程，退出 dlv 之后进程恢复运行）： `dlv attach
   pid`
4. 显示所有 goroutine： `grs`

   ![](image/guide_to_obtaining_stack_traces/11.PNG)
5. 选择 goroutine 打印函数栈（通常 goroutine 1 中包含主函数及其相关代码）： `gr 1 bt`

   ![](image/guide_to_obtaining_stack_traces/12.PNG)
6. 退出 dlv： `quit`

## 3.需要获取栈信息的常见场景

在实际开发中，程序卡死可能发生在不同的阶段和场景下。了解这些常见场景有助于更准确地判断何时以及如何获取栈信息。以下是一些典型的需要打栈分析的情况：

1. **网络通信异常**：
   **场景描述**：程序在与 DolphinDB 服务器建立连接、发送查询请求或接收数据时长时间无响应。
   **表现**：客户端程序"挂起"，操作超时，但网络本身可能通畅（服务器能 Ping 通）。
   **打栈价值**：栈信息可以显示线程是否阻塞在 socket 读/写（
   `recv`
   ,
   `send`
   ）、连接（
   `connect`
   ）或等待锁的阶段，帮助区分是网络库问题、防火墙策略问题，还是服务器端处理缓慢。
2. **DolphinDB 服务器端处理卡顿或阻塞**：
   **场景描述**：DolphinDB 服务器可能因执行一个非常耗时的计算（如复杂分析、大数据量加载）、遭遇死锁或资源（CPU 、内存、磁盘 IO）不足，导致无法及时响应客户端请求。
   **表现**：多个客户端同时出现响应缓慢或卡死，或者单个客户端的某个特定请求一直无返回。
   **打栈价值**：客户端栈信息若显示阻塞在等待服务器响应（如网络读取调用），则说明问题很可能在服务器端。此时应结合 DolphinDB 服务器的日志和性能监控进行联合分析。
3. **API 库内部处理逻辑问题**：
   **场景描述**：API 库本身可能存在 Bug，例如在特定条件下触发死循环、资源清理不当导致死锁、或内存管理异常。
   **表现**：程序可能在执行某个特定 API 调用后卡死，或者在某些看似无关的操作后不定期卡死。
   **打栈价值**：栈信息能揭示卡死是否发生在 API 库的内部函数中，而非网络等待或应用程序逻辑。例如，栈显示停在不含 I/O 操作的纯计算函数或同步原语上，则可能指向 API 库的内部缺陷。
4. **与程序其他部分（非 DolphinDB API 相关代码）的交互问题**：
   **场景描述**：应用程序可能包含多线程、复杂的业务逻辑或使用了其他第三方库。这些部分可能与 DolphinDB API 的线程/资源交互产生冲突，例如共享资源的锁竞争、回调函数处理不当等。
   **表现**：程序整体失去响应，但并非所有操作都涉及 DolphinDB 。
   **打栈价值**：获取所有线程的栈信息至关重要。通过分析栈，可以识别出是哪个线程（DolphinDB API 的工作线程还是应用程序的其他线程）出了问题，以及问题的性质（如等待锁、执行耗时计算等）。这有助于将问题范围从 DolphinDB API 隔离出来，或确认其牵连性。
5. **资源耗尽**：
   **场景描述**：客户端程序可能因内存泄漏、文件句柄耗尽、或线程数过多导致系统资源不足，进而引发卡死。
   **表现**：程序运行一段时间后逐渐变慢直至卡死，可能伴随操作系统报警。
   **打栈价值**：栈信息可以辅助判断卡死时的行为，但通常需要结合系统监控工具（如
   `top`
   ,
   `htop`
   , 任务管理器）来确认资源使用情况。栈可能显示线程在等待资源（如内存分配）或处于无响应的状态。

**打栈时机建议**：一旦发现程序出现卡死或无响应，应尽快获取栈信息。理想情况下，可以在问题发生期间多次（如间隔几秒到几分钟）打栈，观察线程状态是否有变化，这对于诊断死锁或资源竞争尤其有帮助。

## 总结

当使用 DolphinDB 各类 API 开发的程序出现无响应的卡死问题时，定位根源往往比较困难。本文针对这一痛点，系统地介绍了如何利用不同平台和语言的诊断工具来获取运行中程序的函数栈信息以及需要获取栈信息的常见场景，从而快速缩小问题排查范围。

核心方法根据所用 API 的语言有所不同：

* 对于
  **C++ API 和 ODBC**
  ，可以直接使用操作系统层面的工具（如
  `pstack`
  /
  `gstack`
  ）或 GDB 来捕获原生线程的调用栈。
* 对于
  **Python API**
  ，问题可能出现在 Python 层面或底层 C++ 库。推荐先使用专门的 Python 性能分析工具
  `py-spy`
  获取 Python 代码的栈信息；若怀疑是底层问题，再辅以
  `pstack`
  或 GDB 进行深入分析。
* 对于
  **Java API 和 JDBC**
  ，利用 Java 开发工具包（JDK）自带的
  `jstack`
  命令是最直接有效的方式，它可以生成当前 JVM 中所有线程的详细堆栈跟踪。
* 对于
  **Go API**
  ，由于其独特的并发模型（Goroutine），推荐使用 Go 语言生态中专用的调试工具 Delve (dlv) 来进行栈信息分析。该工具能够很好地理解和展示 Goroutine 的调用栈信息。

通过掌握这些针对性的方法，开发者可以在程序发生卡死时，有效地获取关键的现场信息，准确判断问题是源于网络通信、 DolphinDB 服务器端，还是客户端 API 的特定环节，极大地提升了排查和解决此类复杂问题的效率。
