import flet as ft
import os
import tkinter as tk
from tkinter import filedialog
import time
import json
import lock
import sys
from datas import add_data, modify_data, delete_data, load_data  



password_disturbance = 'BIWBGUIWBUI1'

class FilePathList:
    def __init__(self):
        self.file_paths = load_data()  # 初始化时直接从 data.json 加载数据

    def add_path(self, path):
        """添加文件路径到列表"""
        if path:  # 确保路径不为空
            add_data(path, None, None)  # 调用 datas.py 中的 add_data 函数
            self.file_paths = load_data()  # 重新加载数据
            lock.encrypt_file(path, password_disturbance)

    def remove_path(self, path):
        """从列表中删除指定的文件路径"""
        index = next((i for i, file in enumerate(self.file_paths) if file["file_path"] == path), None)
        if index is not None:
            delete_data(index)  # 调用 datas.py 中的 delete_data 函数
            lock.decrypt_file(path, password_disturbance)
            self.file_paths = load_data()  # 重新加载数据

def main(page: ft.Page):
    # 获取当前脚本的绝对路径
    script_dir = os.path.dirname(sys.executable)
    temp_file = os.path.join(script_dir, "temp.json")  # 使用绝对路径

    # 检查同目录中是否存在存密码的json文件
    if not os.path.exists(temp_file):
        # 如果不存在，弹出设置密码的界面
        def set_password(e):
            password = password_field.value
            if password:  # 确保密码不为空
                with open(temp_file, "w") as f:
                    json.dump({"password": password}, f)  # 创建json文件存储密码
                page.clean()  # 清空页面
                main(page)  # 重新进入主界面
            else:
                show_snackbar("密码不能为空！")

        password_field = ft.TextField(
            expand=True,  # 让密码框扩展填满可用空间
            height=40,  # 设置密码框高度
            hint_text="请设置您的密码...",  # 提示文本
            border_radius=8,  # 边框圆角
            filled=True,  # 填充背景
            content_padding=10,  # 内边距
            focused_border_color=ft.colors.BLUE_600,  # 聚焦时边框颜色
            password=True,  # 密码模式
            can_reveal_password=True  # 显示明文开关
        )
        set_password_button = ft.ElevatedButton(
            text="确认",  # 按钮文本
            width=70,  # 按钮宽度
            height=40,  # 按钮高度
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),  # 按钮边框圆角
                bgcolor=ft.colors.BLUE_600,  # 按钮背景颜色
                color=ft.colors.WHITE,  # 按钮文字颜色
                elevation={"pressed": 0, "": 2},  # 按钮阴影
                animation_duration=200  # 按钮动画时长
            ),
            on_click=set_password
        )

        # 创建一个 Row 容器，包含密码框和按钮
        password_row = ft.Row(
            controls=[password_field, set_password_button],
            spacing=15,  # 控件间距
            vertical_alignment=ft.CrossAxisAlignment.CENTER,  # 垂直居中
            width=500  # 设置 Row 容器宽度
        )

        # 创建一个 Container 容器，包裹 Row 容器
        password_container = ft.Container(
            content=password_row,
            padding=20,  # 容器内边距
            bgcolor=ft.colors.WHITE,  # 容器背景颜色
            border_radius=12,  # 容器边框圆角
            shadow=ft.BoxShadow(  # 容器阴影
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLUE_100
            ),
            alignment=ft.alignment.center,  # 内容居中
            expand=True  # 让容器扩展到整个页面
        )

        page.add(password_container)
        page.update()
        return

    def show_snackbar(message):
        """显示提示信息"""
        snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.colors.RED_300
        )
        page.open(snack_bar)
        page.update()

    # 如果存在json文件，进入安全界面
    def check_password(e):
        password = password_field.value
        with open(temp_file, "r") as f:
            stored_password = json.load(f)["password"]
        if password == stored_password:
            page.clean()  # 清空安全界面
            main_original(page)  # 调用原主界面逻辑
        else:
            show_snackbar("密码错误！")

    password_field = ft.TextField(
        expand=True,  # 让密码框扩展填满可用空间
        height=40,  # 设置密码框高度
        hint_text="请输入密码...",  # 提示文本
        border_radius=8,  # 边框圆角
        filled=True,  # 填充背景
        content_padding=10,  # 内边距
        focused_border_color=ft.colors.BLUE_600,  # 聚焦时边框颜色
        password=True,  # 密码模式
        can_reveal_password=True  # 显示明文开关
    )
    check_password_button = ft.ElevatedButton(
        text="确认",  # 按钮文本
        width=70,  # 按钮宽度
        height=40,  # 按钮高度
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),  # 按钮边框圆角
            bgcolor=ft.colors.BLUE_600,  # 按钮背景颜色
            color=ft.colors.WHITE,  # 按钮文字颜色
            elevation={"pressed": 0, "": 2},  # 按钮阴影
            animation_duration=200  # 按钮动画时长
        ),
        on_click=check_password
    )

    # 创建一个 Row 容器，包含密码框和按钮
    password_row = ft.Row(
        controls=[password_field, check_password_button],
        spacing=15,  # 控件间距
        vertical_alignment=ft.CrossAxisAlignment.CENTER,  # 垂直居中
        width=500  # 设置 Row 容器宽度
    )

    # 创建一个 Container 容器，包裹 Row 容器
    password_container = ft.Container(
        content=password_row,
        padding=20,  # 容器内边距
        bgcolor=ft.colors.WHITE,  # 容器背景颜色
        border_radius=12,  # 容器边框圆角
        shadow=ft.BoxShadow(  # 容器阴影
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.BLUE_100
        ),
        alignment=ft.alignment.center,  # 内容居中
        expand=True  # 让容器扩展到整个页面
    )

    page.add(password_container)
    page.update()

# 将原主界面逻辑封装到一个函数中
def main_original(page: ft.Page):
    file_list = FilePathList()  # 使用 FilePathList 类加载数据

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


    def show_snackbar(message):
        """显示提示信息"""
        snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.colors.RED_300
        )
        page.open(snack_bar)
        page.update()

    # 遍历路径列表，为每个文件创建一个 ListTile 控件
    def update_list_view():
        nonlocal selected_index
        selected_index = None  # 重置选中索引
        list_view.controls = [
            ft.ListTile(
                leading=ft.Icon(icon_mapping.get(os.path.splitext(file["file_path"])[1].lower(), ft.icons.INSERT_DRIVE_FILE)),
                title=ft.Text(os.path.basename(file["file_path"]), color=ft.colors.BLUE),
                subtitle=ft.Text(
                    f"路径: {file['file_path']}  - 策略: {file['strategy_id']} - 参数: {file['additional_params']}",
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
        file_name = os.path.basename(file["file_path"])
        file_path = file["file_path"]
        strategy = file["strategy_id"]
        param = file["additional_params"]

        # 创建文件详情界面
        details_view = ft.Container(
            content = ft.Column(
                controls=[
                    ft.Text(f"文件名: {file_name}", size=20),
                    ft.Text(f"文件路径: {file_path}", size=20),
                    ft.Text(f"加密策略: {strategy}", size=20),
                    ft.Text(f"加密参数: {param}", size=20),
                    ft.ElevatedButton(
                        content=ft.Text("修改加密",size=18),
                        on_click=lambda e: show_password_choices(file_index, True),  # 传递预填充标志
                        width=150,
                        height=50
                    ),
                    ft.ElevatedButton(
                        content=ft.Text("返回",size=18),
                        on_click=go_back_to_main,
                        width=150,
                        height=50
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center

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
            file_path = file_list.file_paths[selected_index]["file_path"]
            file_list.remove_path(file_path)
            update_list_view()
            selected_index = None  # 重置选中索引

    delete_button = ft.ElevatedButton(
        content=ft.Icon(
            name=ft.icons.DELETE,
            size=60,
            color=ft.colors.WHITE,
        ),
        width=80,
        height=80,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),  # 设置圆角
            bgcolor=ft.colors.RED,
            color=ft.colors.WHITE
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
        create_password_choice("  日期码  ×", '用户自定义实数', number=1),
        create_password_choice("若  星期X  为奇数，则取  日期码  的奇数位；若  星期  为偶数，则取  日期码  的偶数位在末尾连接  星期X", show_textfield=False, number=2),
        create_password_choice("  小时  ×_________", '用户自定义实数', number=3),
        create_password_choice("若  小时  为奇数，则取  日期码  的奇数位；若  小时  为偶数，则取  日期码  的偶数位在末尾连接  小时", show_textfield=False, number=4),
        create_password_choice("  日期码  ×  星期X  在末尾连接  小时  ", show_textfield=False, number=5),
        create_password_choice("判断（包含且只包含  小时  个  月份  字符的任意字符串）", show_textfield=False, number=6),
        create_password_choice("判断（包含且只包含_________个  月份  字符的任意字符串）", '用户自定义实数', number=7),
        create_password_choice("判断（包含且只包含  小时  个_________（1位字符）的任意字符串）", '用户自定义实数', number=8),
        create_password_choice("判断（包含且只包含  小时  个大写英文字母的任意字符串）", show_textfield=False, number=9),
        create_password_choice("判断（包含且只包含_________个大写英文字母的任意字符串）",'用户自定义实数', number=10),
        create_password_choice("判断（密码中所有数字类字符加和=  小时  （其余字符均不影响））", show_textfield=False, number=11),
        create_password_choice("判断（密码中所有数字类字符加和=_________（其余字符均不影响））", '用户自定义实数', number=12),
    ]

    # 显示密码策略选择界面
    def show_password_choices(file_index, prefill=False):
        # 清空页面并显示密码策略选择界面
        page.clean()
        file = file_list.file_paths[file_index]
        strategy = file["strategy_id"]
        param = file["additional_params"]

        # 添加文字说明
        instruction_text = ft.Text(
            "前置定义变量：\n"
            "日期码 = 8位的年+月+日\n"
            "星期X = 当日的星期X\n"
            "小时 =  取按24小时计时法现在处于X时\n"
            "月份 = 当前xxx月，将xxx转化为16进制，如xxx=10=a，xxx=12=C",
            size=20,
            color=ft.colors.BLACK,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.START,
            font_family="Microsoft YaHei"
        )
        page.add(instruction_text)  # 将文字说明添加到页面
        page.scroll = ft.ScrollMode.AUTO

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
        selected_strategy = None
        selected_param = None
        for i, (checkbox, textfield) in enumerate(checkboxes):
            if checkbox.value:
                selected_strategy = i + 1
                if textfield and textfield.value:
                    try:
                        selected_param = int(textfield.value)  
                    except ValueError:
                        show_snackbar("请输入有效的数字作为参数！")
                        return
                break

        # 更新文件的策略和参数
        modify_data(file_index, strategy_id=selected_strategy, additional_params=selected_param)
        file_list.file_paths = load_data()  # 重新加载数据
        go_back_to_main(e)

# 运行应用
ft.app(target=main)
