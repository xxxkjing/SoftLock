import flet as ft

class PasswordApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self._setup_page()
        self._create_controls()
        self._setup_events()
        self._build_layout()

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
            hint_text="请输入您的密码...",
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
            print("提交密码:", "*" * len(self.text_input.value))
            self.text_input.value = ""
            self.page.update()
        else:
            self._show_snackbar("密码不能为空！")

    def _show_snackbar(self, message):
        """显示提示信息"""
        self.page.snack_bar = ft.SnackBar(
            ft.Text(message),
            bgcolor=ft.colors.RED_300
        )
        self.page.snack_bar.open = True
        self.page.update()

def main(page: ft.Page):
    PasswordApp(page)

if __name__ == "__main__":
    ft.app(target=main)
    
