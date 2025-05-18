import strategies
import lock
import datas

import subprocess
import time
import os
import flet as ft
import tkinter as tk
from tkinter import filedialog
import sys
import shlex



notepad_path = os.path.join(os.environ.get('SYSTEMROOT', r"C:\Windows"), "System32", "notepad.exe") #记事本路径
password_disturbance = 'BIWBGUIWBUI1' # lock的加密密钥是静态的，但我们的密码是动态的，所以取一串固定的随机字符来加密文，之后应该在管理端让用户设置


class PasswordApp():
    def __init__(self, page: ft.Page,target_file_path):
        self.page = page
        self._setup_page()
        self._create_controls()
        self._setup_events()
        self._build_layout()
        self.target_file_path = target_file_path

    def _setup_page(self):
        """初始化页面设置"""
        self.page.title = "输入框与提交按钮"
        self.page.window_width = 600
        self.page.window_height = 300
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def _create_controls(self):
        """创建界面控件"""
        self.text_input = ft.TextField(
            expand=True,
            height=40,
            hint_text="请输入密码...",
            border_radius=8,
            filled=True,
            content_padding=10,
            focused_border_color=ft.Colors.BLUE_600,
            password=True,  # 密码模式
            can_reveal_password=True  # 显示明文开关
        )

        self.submit_btn = ft.ElevatedButton(
            text="提交",
            width=70,
            height=40,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
                elevation={"pressed": 0, "": 2},
                animation_duration=200
            )
        )

    def _setup_events(self):
        """设置事件处理"""
        self.submit_btn.on_click = self._handle_submit
        self.text_input.on_submit = self._handle_submit

    def _build_layout(self):
        """构建界面布局"""
        container = ft.Container(
            content=ft.Row(
                controls=[
                    self.text_input,
                    self.submit_btn
                ],
                spacing=15,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                width=500
            ),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.BLUE_100
            )
        )
        self.page.add(container)

    def _handle_submit(self, e):
        """提交按钮事件处理"""
        if self.text_input.value.strip():
            checker=strategies.PasswordChecker()
            if checker.strategy(datas.find_data(self.target_file_path)["strategy_id"],datas.find_data(self.target_file_path)["additional_params"],self.text_input.value)==True:
                lock.decrypt_file(self.target_file_path, password_disturbance)
                self.page.window.destroy()
                self.encrypt_after_close(self.target_file_path, password_disturbance)
            else:
                self._show_snackbar("密码错误！")
            self.text_input.value = ""
            self.page.update()
        else:
            self._show_snackbar("密码不能为空！")

    def _show_snackbar(self, message):
        """显示提示信息"""
        snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.RED_300
        )
        self.page.open(snack_bar)
        self.page.update()
    
    def encrypt_after_close(self,file_path: str, password: str):
    
        if os.name == 'nt':  # Windows
            #process = subprocess.Popen(f'start "" "{file_path}"', shell=True)
            process = subprocess.Popen(['notepad.exe', file_path])

        elif os.name == 'posix':  # macOS 和 Linux
            process = subprocess.Popen(['open', file_path])
        
        # 检测文件是否关闭
        while True:
            time.sleep(1)  # 每秒检测一次
            try_count = 0
            if process.poll() is not None:
                lock.encrypt_file(file_path, password)
                break
            
                
# 下方函数大多都是将来会移到管理端文件里的函数

def create_page(page: ft.Page, target_file_path):
    app = PasswordApp(page, target_file_path)

    

def select_file():
    # 创建一个 Tkinter 窗口
    root = tk.Tk()
    # 隐藏主窗口
    root.withdraw()
    
    # 打开文件选择对话框
    file_path = filedialog.askopenfilename(
        title="选择文件",  # 对话框标题
        filetypes=[("所有文件", "*.*"), ("文本文件", "*.txt")]  # 文件类型过滤
    )
    
    # 如果用户选择了文件，返回文件路径
    if file_path:
        return file_path
    else:
        return None


def select_and_encrypt(strategy_id, additional_params):
    file_path=select_file()
    datas.add_data(file_path, strategy_id, additional_params)
    lock.encrypt_file(file_path, password_disturbance)

def select_and_decrypt():
    file_path=select_file()
    datas.find_and_delete_data(file_path)
    lock.decrypt_file(file_path, password_disturbance)


def Trigger_password():
    target_file_path = select_file()
    if target_file_path:
        ft.app(target=lambda page: create_page(page, target_file_path))

def bat(bat_filename):
    """
    创建一个 .bat 文件，并填充内容。
    :param bat_filename: 要创建的 .bat 文件名
    """
    # 获取当前运行的 .exe 文件路径
    exe_path = os.path.abspath(sys.argv[0])

    # 创建 .bat 文件的内容
    bat_content = f"""@echo off
chcp 65001
setlocal enabledelayedexpansion

:: 检查是否有参数传入
if "%~1"=="" (
    echo No file path provided.
    pause
    exit /b
)

:: 获取完整的文件路径
set "file_path=%~1"

:: 调用打包后的 .exe 文件并传递完整的文件路径
start /b "" "{exe_path}" "!file_path!"
"""

    # 写入 .bat 文件
    with open(bat_filename, 'w', encoding='utf-8') as bat_file:
        bat_file.write(bat_content)

def create_bat_file():
    # 获取当前运行的 .exe 文件所在的目录
    exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    bat_filename = os.path.join(exe_dir, "processing.bat")  # 动态生成 .bat 文件的路径

    # 检查 .bat 文件是否存在
    if  not os.path.exists(bat_filename):
        bat(bat_filename)

    

'''
目前使用方法：

创建一个文件夹（这一步只是方便管理软件，就像其它软件一样，最后我们的软件全部内容应该在一个文件夹中）
下载password.exe文件与main.py到文件夹中
运行Python文件，选择一个txt文件确认加密，这一步是替代方法，之后会在管理端中
双击exe运行
注意到生成一个processing.bat文件，在成品中，创建bat文件会由管理端程序实现，现在暂时是这个替代方法，也不影响
找到任意一个txt文件，右键打开方式，在电脑中查找文件，找到processing.bat，始终使用它打开txt
即可实现双击txt自动运行程序了


目前存在问题：
暂时不清楚这版exe文件运行时为什么不会隐藏cmd提示符窗口，之前都可以的，不过这个问题不大，不影响使用

'''

def trigger():
    target_file_path= sys.argv[1].replace('\\', '/')
    # 修改后会对所有txt影响，所以未加密的txt应该正常打开
    if datas.find_data(target_file_path)==None:
        if os.name == 'nt':  # Windows
            #process = subprocess.Popen(f'start "" "{file_path}"', shell=True)
            subprocess.Popen(f'start notepad "" "{target_file_path}"', shell=True)

        elif os.name == 'posix':  # macOS 和 Linux
            process = subprocess.Popen(['open', target_file_path])

    else:
        ft.app(target=lambda page: create_page(page, target_file_path))



def main():
    exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    bat_filename = os.path.join(exe_dir, "processing.bat")  # 动态生成 .bat 文件的路径
    if  os.path.exists(bat_filename):
        trigger()
    else:
        create_bat_file()

if __name__ == '__main__':
    select_and_encrypt(12,7)
    #Trigger_password()
    #select_and_decrypt()
    #create_bat_file()
    #main()
