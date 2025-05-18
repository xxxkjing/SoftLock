import flet as ft
import os
import tkinter as tk
from tkinter import filedialog
import time

class FilePathList:
    def __init__(self):
        self.file_paths = []  # 存储文件路径的列表

    def add_path(self, path):
        """添加文件路径到列表"""
        if path:  # 确保路径不为空
            self.file_paths.append({"path": path, "strategy": None, "param": None, "encrypted": False})

    def remove_path(self, path):
        """从列表中删除指定的文件路径"""
        self.file_paths = [file for file in self.file_paths if file["path"] != path]

    def toggle_encryption(self, path):
        """切换指定文件的加密状态"""
        for file in self.file_paths:
            if file["path"] == path:
                file["encrypted"] = not file["encrypted"]
                break

def main(page: ft.Page):
    # 创建一个文件路径列表对象
    file_list = FilePathList()

    # 创建一个 ListView 控件用于显示文件列表
    list_view = ft.ListView(expand=True, spacing=10)

    # 定义文件类型的图标映射
    icon_mapping = {
        ".txt": ft.icons.TEXT_FORMAT,
        ".pdf": ft.icons.PICTURE_AS_PDF,
        ".png": ft.icons.IMAGE,
        ".docx": ft.icons.DOCUMENT_SCANNER
    }

    # 用于存储当前选中的项索引
    selected_index = None

    # 用于双击检测的变量
    last_click_time = 0
    double_click_threshold = 0.3  # 双击时间阈值（秒）

    # 遍历路径列表，为每个文件创建一个 ListTile 控件
    def update_list_view():
        nonlocal selected_index
        selected_index = None  # 重置选中索引
        list_view.controls = [
            ft.ListTile(
                leading=ft.Icon(icon_mapping.get(os.path.splitext(file["path"])[1].lower(), ft.icons.INSERT_DRIVE_FILE)),
                title=ft.Text(os.path.basename(file["path"]), color=ft.colors.BLUE),
                subtitle=ft.Text(
                    f"路径: {file['path']}  - 策略: {file['strategy']} - 参数: {file['param']}",
                    color=ft.colors.BLUE
                ),
                on_click=lambda e, idx=i: handle_click(e, idx),
                on_long_press=lambda e, idx=i: handle_long_press(e, idx)
            )
            for i, file in enumerate(file_list.file_paths)
        ]
        page.update()

    def handle_click(e, idx):
        nonlocal last_click_time, selected_index
        current_time = time.time()
        if current_time - last_click_time < double_click_threshold:
            open_file_details(idx)
        else:
            selected_index = idx  # 更新选中索引
        last_click_time = current_time

    def handle_long_press(e, idx):
        nonlocal selected_index
        selected_index = idx  # 更新选中索引

    def open_file_details(file_index):
        # 清空页面并显示文件详情界面
        page.clean()
        file = file_list.file_paths[file_index]
        file_name = os.path.basename(file["path"])
        file_path = file["path"]
        strategy = file["strategy"]
        param = file["param"]
        encrypted = "已加密" if file["encrypted"] else "未加密"

        # 创建文件详情界面
        details_view = ft.Column(
            controls=[
                ft.Text(f"文件名: {file_name}", size=20),
                ft.Text(f"文件路径: {file_path}", size=20),
                ft.Text(f"加密状态: {encrypted}", size=20),
                ft.Text(f"加密策略: {strategy}", size=20),
                ft.Text(f"加密参数: {param}", size=20),
                ft.ElevatedButton(
                    "修改加密",
                    on_click=lambda e: show_password_choices(file_index, True),  # 传递预填充标志
                    width=150,
                    height=40
                ),
                ft.ElevatedButton(
                    "返回",
                    on_click=go_back_to_main,
                    width=150,
                    height=40
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        page.add(details_view)
        page.update()

    def go_back_to_main(e):
        # 返回主界面并更新文件列表
        page.clean()
        page.add(button_row, list_view)
        update_list_view()
        page.update()

    # 创建添加按钮
    def add_file_path(e):
        # 创建隐藏的主窗口
        root = tk.Tk()
        root.withdraw()
        # 确保文件选择对话框置顶
        root.attributes('-topmost', True)

        # 弹出文件选择对话框
        file_path = filedialog.askopenfilename(
            title="选择文件",
            filetypes=[("所有文件", "*.*"), ("文本文件", "*.txt"), ("图片文件", ("*.png", "*.jpg"))]
        )
        if file_path:  # 确保用户选择了文件
            file_list.add_path(file_path)
            update_list_view()
            # 在文件选择确定后，打开复选框界面
            show_password_choices(len(file_list.file_paths) - 1, False)  # 传递预填充标志

    # 创建删除按钮
    def delete_selected_path(e):
        nonlocal selected_index
        if selected_index is not None:
            file_path = file_list.file_paths[selected_index]["path"]
            file_list.remove_path(file_path)
            update_list_view()
            selected_index = None  # 重置选中索引

    delete_button = ft.ElevatedButton(
        content=ft.Text(
            "删除", 
            size=20,
            color=ft.colors.BLUE,
            offset=ft.Offset(0, -0.1)
        ),
        width=120,
        height=40,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),  # 设置圆角
            bgcolor=ft.colors.WHITE,
            color=ft.colors.BLUE
        ),
        on_click=delete_selected_path
    )

    # 创建添加按钮
    add_button = ft.ElevatedButton(
        content=ft.Text(
            "+", 
            size=60,
            color=ft.colors.BLUE,
            offset=ft.Offset(0, -0.1)
        ),
        width=80,
        height=80,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=15),  # 设置圆角
            bgcolor=ft.colors.WHITE,
            color=ft.colors.BLUE
        ),
        on_click=add_file_path
    )

    # 将按钮和文件列表添加到页面
    button_row = ft.Row(
        controls=[
            delete_button,
            ft.Container(expand=True),  # 使用 expand 属性来分配空间
            add_button,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )
    page.add(button_row, list_view)

    # 初始更新列表视图
    update_list_view()

    # 创建一个复选框和文本框的组合控件
    def create_password_choice(label: str, hint_text: str = '', show_textfield: bool = True, number: int = 0):
        checkbox = ft.Checkbox(label=label)
        if show_textfield:
            textfield = ft.TextField(hint_text=hint_text, width=200, height=40, border_color=ft.colors.GREY_600, disabled=True)
        else:
            textfield = None

        def on_change(e):
            # 当复选框状态改变时，更新文本框的启用状态
            if show_textfield:
                textfield.disabled = not checkbox.value
            # 清除其他复选框的选中状态
            for cb, tf in checkboxes:
                if cb != checkbox:
                    cb.value = False
                    if tf:
                        tf.disabled = True
            page.update()

        checkbox.on_change = on_change
        if show_textfield:
            return checkbox, textfield
        else:
            return checkbox, None

    # 创建十二个复选框和文本框的组合
    checkboxes = [
        create_password_choice("Date×", '用户自定义实数', number=1),
        create_password_choice("若Dow为奇数，则取Date的奇数位若Dow为偶数，则取Date的偶数位在末尾连接Dow", show_textfield=False, number=2),
        create_password_choice("Hour×_________（用户自定义实数）", '用户自定义实数', number=3),
        create_password_choice("若Hour为奇数，则取Date的奇数位若Hour为偶数，则取Date的偶数位在末尾连接Hour", '用户自定义实数', number=4),
        create_password_choice("Hour×Dow在末尾连接Hour", show_textfield=False, number=5),
        create_password_choice("判断（包含且只包含Hour个Month字符的任意字符串）", show_textfield=False, number=6),
        create_password_choice("判断（包含且只包含_________（用户自定义实数）个Month字符的任意字符串）", '用户自定义实数', number=7),
        create_password_choice("判断（包含且只包含Hour个_________（用户自定义1位字符）的任意字符串）", '用户自定义实数', number=8),
        create_password_choice("判断（包含且只包含Hour个大写英文字母的任意字符串）", show_textfield=False, number=9),
        create_password_choice("判断（包含且只包含_________（用户自定义实数）个大写英文字母的任意字符串）",'用户自定义实数', number=10),
        create_password_choice("判断（密码中所有数字类字符加和=Hour（其余字符均不影响））", show_textfield=False, number=11),
        create_password_choice("判断（密码中所有数字类字符加和=_________（用户自定义实数）（其余字符均不影响））", '用户自定义实数', number=12),
    ]

    # 显示密码策略选择界面
    def show_password_choices(file_index, prefill=False):
        # 清空页面并显示密码策略选择界面
        page.clean()
        file = file_list.file_paths[file_index]
        strategy = file["strategy"]
        param = file["param"]

        # 重置所有复选框和文本框的状态
        for checkbox, textfield in checkboxes:
            checkbox.value = False  # 重置复选框状态
            if textfield:
                textfield.value = ""  # 重置文本框内容
                textfield.disabled = True  # 禁用文本框

        # 如果是预填充模式，设置当前文件的策略和参数
        if prefill and strategy:
            checkboxes[strategy - 1][0].value = True  # 设置对应的复选框为选中状态
            if checkboxes[strategy - 1][1]:  # 如果有文本框
                checkboxes[strategy - 1][1].value = param  # 设置文本框的值
                checkboxes[strategy - 1][1].disabled = False  # 启用文本框

        # 添加复选框和文本框到页面
        for checkbox, textfield in checkboxes:
            if textfield:
                page.add(ft.Row(controls=[checkbox, textfield], alignment=ft.MainAxisAlignment.START))
            else:
                page.add(checkbox)
        page.add(ft.ElevatedButton("确定", on_click=lambda e: on_confirm_click(e, file_index)))
        page.update()

    # 确认按钮的点击事件
    def on_confirm_click(e, file_index):
        # 遍历复选框，找到被选中的策略和参数
        for i, (checkbox, textfield) in enumerate(checkboxes):
            if checkbox.value:
                file_list.file_paths[file_index]["strategy"] = i + 1
                if textfield and textfield.value:
                    file_list.file_paths[file_index]["param"] = textfield.value
                break
        go_back_to_main(e)

# 运行应用
ft.app(target=main)
