import flet as ft

from enum import Enum

from src.utils import on_change_obj


class TypeClassDialog(Enum):
    ADD="add"
    UPDATE="update"

class ClassDialog(ft.AlertDialog):
    def __init__(self,page:ft.Page,cls_data={},type=TypeClassDialog.ADD):
        self.page = page

        self.cls_data = cls_data

        self.tf_cls = ft.Ref[ft.TextField]()

        if type == TypeClassDialog.ADD:
            title = "Добавить роль"
        elif type == TypeClassDialog.UPDATE:
            title = "Изменить роль"
        else:
            title = "TitleError"

        self.option_dict = {
            ft.colors.GREEN: self.color_option_creator(ft.colors.GREEN),
            ft.colors.RED: self.color_option_creator(ft.colors.RED),
            ft.colors.WHITE: self.color_option_creator(ft.colors.WHITE),
            ft.colors.ORANGE: self.color_option_creator(ft.colors.ORANGE),
            ft.colors.PURPLE: self.color_option_creator(ft.colors.PURPLE),
            ft.colors.CYAN_500: self.color_option_creator(ft.colors.CYAN_500),
        }
        self.color_options = ft.GridView(runs_count=3, max_extent=40, data="", height=50)
        
        for _, v in self.option_dict.items():
            v.on_click = self.set_color
            self.color_options.controls.append(v)

        super().__init__(
            title=ft.Text(title),
            content=ft.Column(
                tight=True,
                controls=[
                    ft.TextField(
                        ref=self.tf_cls,
                        label="Название роли",
                        on_change=on_change_obj
                    ),
                    ft.Divider(),
                    self.color_options
                ]
            ),
            actions=[
                ft.CupertinoFilledButton(
                    on_click=self.add_class,
                    opacity_on_click=0.3,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Icon("ADD"),
                            ft.Text("Добавить Роль")
                        ]
                    )
                )
            ]
        )
    def set_color(self,e:ft.ControlEvent):
        for k, v in self.option_dict.items():
            if k == e.control.data:
                v.border = ft.border.all(3, ft.colors.BLACK26)
                self.color_options.data = v.bgcolor
                self.color_options.update()
            else:
                v.border = None
        self.update()
    
    def color_option_creator(self, color: str):
        return ft.Container(
            bgcolor=color,
            border_radius=ft.border_radius.all(50),
            height=10,
            width=10,
            padding=ft.padding.all(5),
            alignment=ft.alignment.center,
            data=color,
        )
    def add_class(self,e:ft.ControlEvent = None):
        if not self.tf_cls.current.value:
            self.tf_cls.current.error_text = "Это поле обязательно"
            self.tf_cls.current.update()
        if not self.color_options.data:
            self.color_options.data = "blue300"
            self.color_options.update()
        if all([self.tf_cls.current.value,self.color_options.data]):
            cls = {"name":self.tf_cls.current.value,"color":self.color_options.data}
            self.page.views[-1].class_list += [cls]
            self.page.views[-1].dd.current.update()
            self.page.client_storage.set("class_list",self.page.views[-1].class_list)