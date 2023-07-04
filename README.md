# timerbackup
这是原创的脚本。使用 AGPLv3.0 协议，可以二创，但不能盈利。转载请注明原作者。

# 定时备份脚本

这是一个定时备份脚本，用于自动备份源目录到目标目录。

## 如果有任何疑问，请发邮件（jiyu.fu@outlook.~）给我，我会解答。

## 使用说明

1. 在运行脚本（main.py）之前，请确保已备份重要数据，并理解脚本的作用。
2. 运行脚本后，你将被要求输入源目录和目标目录的路径。
3. 脚本将生成一个备份脚本，并将其复制到适当的位置以实现开机自启。
4. 在 Linux 上，脚本将使用 `rsync` 命令进行备份；在 Windows 上，脚本将使用 `xcopy` 命令进行备份。
5. 如果在 Linux 上运行脚本时需要管理员权限，你将被要求输入管理员密码。

## 安装

1. 克隆仓库：
   git clone ～
   
2. 进入仓库目录：
   ```bash
   cd timerbackup
   ```
   
4. 运行安装命令：
   ```bash
   python setup.py install
   ```
请确保在运行安装命令之前已经安装了 Python 3.5 或更高版本。

## 定时自动备份

### Linux（systemd）

1. 创建一个服务单元文件（`backup.service`），并将以下内容复制到文件中：
   ```service
   [Unit]
   Description=Incremental Backup Service
   After=network.target

   [Service]
   Type=simple
   ExecStart=/usr/bin/python /path/to/your/main.py

   [Install]
   WantedBy=multi-user.target
   ```
   
   将 /path/to/your/main.py 替换为你实际的备份脚本路径。

   将该服务单元文件复制到 /etc/systemd/system/ 目录下：
   
   ```bash
   sudo cp backup.service /etc/systemd/system/
   ```
   使用以下命令启用服务:
   ```bash
   sudo systemctl enable backup.service
   ```
   重启系统，服务将在系统启动后自动运行。

### Windows
创建一个批处理文件（backup.bat），并将以下内容复制到文件中：
```bat
@echo off
start "" /min python C:\path\to\your\backup_script.py
```
将 C:\path\to\your\main.py 替换为你实际的备份脚本路径。

将批处理文件移动到以下文件夹中的一个：

  -`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`（只针对当前用户）
  -`%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs\StartUp`（对所有用户）

重新启动系统，脚本将在系统启动后自动运行。

请根据你的操作系统和实际情况选择适合的方法，并确保你的备份脚本路径正确。另外，对于 Linux 系统，请确保 Python 解释器的路径正确（可以使用 `which python` 命令来查找）。

这些方法将在系统启动后自动运行你的备份脚本，并在后台执行备份操作。请确保在自动运行备份之前备份你的数据，并仔细测试和验证自启动功能。

## 故障排除
以下是一些常见问题和解决方案：

问题：脚本无法在开机时自启。

- 解决方案：
  - 在 Linux 上，确保你的脚本位于 `~/.config/autostart/` 目录中，并具有可执行权限。
  - 在 Windows 上，确保你的脚本位于启动文件夹 (`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`) 中。

问题：备份失败。

- 可能原因：
  - 源目录不存在或没有足够的权限。
  - 目标目录不存在或没有足够的权限。
  - 备份命令执行失败。
- 解决方案：
  - 确保源目录和目标目录的路径正确，并且具有适当的权限。
  - 检查备份命令（`rsync` 或 `xcopy`）的输出或日志文件，以获取更详细的错误信息。

问题：格式化磁盘失败。

- 可能原因：
  - 没有足够的权限进行格式化。
  - 磁盘不可用或不存在。
- 解决方案：
  - 在 Linux 上，确保你有管理员权限，并且输入正确的管理员密码。
  - 确保磁盘可用，并检查磁盘格式化命令是否正确。

请记住，在解决问题之前，始终备份重要数据，并谨慎操作。
