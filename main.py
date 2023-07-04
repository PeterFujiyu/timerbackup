import os
import platform
import subprocess
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

# 设置日志文件路径
log_dir = os.path.dirname(os.path.realpath(__file__))
log_file = os.path.join(log_dir, 'backup.log')

# 设置日志级别和格式
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BackupHandler(FileSystemEventHandler):
    def __init__(self, source, destination, progress):
        self.source = source
        self.destination = destination
        self.progress = progress

    def on_modified(self, event):
        incremental_backup(self.source, self.destination, self.progress)

def incremental_backup(source, destination, progress):
    if not os.path.exists(destination):
        os.makedirs(destination)

    if platform.system() == "Windows":
        command = ["robocopy", source, destination, "/MIR"]
    else:
        command = ["rsync", "-arv", source, destination]

    try:
        progress.start()  # 开始进度条动画
        subprocess.Popen(command)
        logging.info(f"备份开始，源目录：{source}，目标目录：{destination}")
    except Exception as e:
        logging.error(f"备份失败: {e}", exc_info=True)
        messagebox.showerror("错误", f"备份失败: {e}")

def restore_backup(source, destination):
    if platform.system() == "Windows":
        command = ["xcopy", "/E", "/I", source, destination]
    else:
        command = ["cp", "-r", source, destination]

    try:
        subprocess.run(command, shell=True, check=True)
        logging.info(f"恢复成功，源目录：{source}，目标目录：{destination}")
    except subprocess.CalledProcessError as e:
        logging.error(f"恢复失败: {e}", exc_info=True)
        messagebox.showerror("错误", f"恢复失败: {e}")

def format_drive(drive_letter):
    if platform.system() == "Windows":
        format_command = f"format {drive_letter}: /FS:exFAT /Q /V:BackupDrive /Y"
    else:
        format_command = f"mkfs.exfat /dev/{drive_letter}"

    result = messagebox.askquestion("警告", f"你将要格式化磁盘 {drive_letter}. 所有数据将被删除. 确定要继续吗?", icon='warning')
    if result == 'yes':
        try:
            subprocess.run(format_command, shell=True, check=True)
            logging.info(f"磁盘成功格式化为exFAT: {drive_letter}")
        except subprocess.CalledProcessError as e:
            logging.error(f"磁盘格式化失败: {e}", exc_info=True)
            messagebox.showerror("错误", f"磁盘格式化失败: {e}")

def create_gui():
    window = tk.Tk()
    window.title('增量备份')

    source_label = tk.Label(window, text='源目录')
    source_label.pack()
    source_button = tk.Button(window, text='浏览', command=lambda: source_entry.insert(0, filedialog.askdirectory()))
    source_button.pack()
    source_entry = tk.Entry(window)
    source_entry.pack()

    dest_label = tk.Label(window, text='目标目录')
    dest_label.pack()
    dest_button = tk.Button(window, text='浏览', command=lambda: dest_entry.insert(0, filedialog.askdirectory()))
    dest_button.pack()
    dest_entry = tk.Entry(window)
    dest_entry.pack()

    format_label = tk.Label(window, text='要格式化的磁盘 (例如, D)')
    format_label.pack()
    format_entry = tk.Entry(window)
    format_entry.pack()
    format_button = tk.Button(window, text='格式化磁盘', command=lambda: format_drive(format_entry.get()))
    format_button.pack()

    progress = ttk.Progressbar(window, mode='indeterminate')
    progress.pack()

    backup_button = tk.Button(window, text='开始备份', command=lambda: incremental_backup(source_entry.get(), dest_entry.get(), progress))
    backup_button.pack()

    restore_button = tk.Button(window, text='恢复备份', command=lambda: restore_backup(source_entry.get(), dest_entry.get()))
    restore_button.pack()

    window.mainloop()

if __name__ == "__main__":
    create_gui()
