# 利用现有的界面测试日期码的获取与判断功能

#目前是面向过程的写法
from datetime import datetime
import flet as ft


# 获取当前日期
today = datetime.today()

# 格式化日期为年月日形式（8位字符串）
password = today.strftime("%Y%m%d")

def main(page: ft.Page):
    # ===== 页面基础设置 =====
    page.title = "输入框与提交按钮"
    page.window_width = 600
    page.window_height = 300
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  # 垂直居中
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # 水平居中

# ===== 控件定义 =====
    # 输入框组件
    text_input = ft.TextField(
        expand=True,              # 自动扩展剩余空间
        height=40,
        hint_text="请输入你的密码...(现在密码暂时就是日期码)",
        border_radius=8,
        filled=True,
        content_padding=10,
        focused_border_color=ft.colors.BLUE_600
    )

    # 提交按钮组件
    submit_btn = ft.ElevatedButton(
        text="提交",
        width=70,
        height=40,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            bgcolor=ft.colors.BLUE_600,
            color=ft.colors.WHITE
        )
    )

    # 按钮点击动画
    submit_btn.style = ft.ButtonStyle(
        elevation={"pressed": 0, "": 2},
        animation_duration=200
    )

    # ===== 交互逻辑 =====

    def handle_submit(e):
        page.snack_bar = ft.SnackBar(ft.Text("你好！"))
        if text_input.value.strip():
            print("提交内容:", text_input.value)
        
        
            if text_input.value==password:
                if len(page.controls) > 1:  
                    page.controls.pop()  # 删除最后一个控件（即之前的文本）
                note1 = ft.Text(value="正确", size=20, color="blue")
                page.add(note1)
                page.update()
            else:
                if len(page.controls) > 1:  
                    page.controls.pop()
                note1 = ft.Text(value="错误", size=20, color="blue")
                page.add(note1)
                page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("请输入有效内容！"))
            page.snack_bar.open = True
            page.update()

    submit_btn.on_click = handle_submit
    text_input.on_submit = handle_submit  # 支持回车提交

    # ===== 布局结构 =====
    page.add(
        ft.Container(
            content=ft.Row(
                controls=[
                    text_input,
                    submit_btn
                ],
                spacing=15,                # 控件间距
                vertical_alignment=ft.CrossAxisAlignment.CENTER,  # 垂直居中
                width=500                 # 固定行宽度
            ),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLUE_100,
                offset=ft.Offset(0, 0)
            )
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
