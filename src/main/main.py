import strategies
import lock
import datas

import subprocess
import time
import os
import flet as ft
import tkinter as tk
from tkinter import filedialog


password_disturbance = 'BIWBGUIWBUI1' # lock的加密密钥是静态的，但我们的密码是动态的，所以取一串固定的随机字符来加密文件


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
            focused_border_color=ft.colors.BLUE_600,
            password=True,  # 密码模式
            can_reveal_password=True  # 显示明文开关
        )

        self.submit_btn = ft.ElevatedButton(
            text="提交",
            width=70,
            height=40,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                bgcolor=ft.colors.BLUE_600,
                color=ft.colors.WHITE,
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
            bgcolor=ft.colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLUE_100
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
            bgcolor=ft.colors.RED_300
        )
        self.page.open(snack_bar)
        self.page.update()
    
    def encrypt_after_close(self,file_path: str, password: str):
    
        if os.name == 'nt':  # Windows
            process = subprocess.Popen(['start',file_path], shell=True)
        elif os.name == 'posix':  # macOS 和 Linux
            process = subprocess.Popen(['open', file_path])
        
        # 检测文件是否关闭
        while True:
            time.sleep(1)  # 每秒检测一次
            if process.poll() is not None:  # 文件已关闭
                lock.encrypt_file(file_path, password)  # 加密文件
                break

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





def Trigger_password():
    target_file_path = select_file()
    if target_file_path:
        ft.app(target=lambda page: create_page(page, target_file_path))

    

'''
目前使用方法：

select_and_encrypt(这里填策略编号,这里填附加参数)
可以实现选择一个文件，并且按照填好的加密方法加密它（目前选择txt或者docx文件会比较稳定）

Trigger_password()
运行后选择被加密过的文件，模拟双击被加密文件的情况
输入正确的密码即可解密并打开文件

目前已实现的重要功能：
加密文件，使其访问时变为乱码
加密的方式存储在本地的json文件中，可随时更改，删除
输入正确的密码即可解密文件，并自动打开文件
关闭文件之后自动将文件再加密回去

未实现：
双击文件自动拦截，弹出输入密码框

'''

#select_and_encrypt(12,7)
#Trigger_password()