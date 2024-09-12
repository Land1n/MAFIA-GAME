import flet as ft

from src.utils import on_change_obj

from src.home.view.ui.player_card import PlayerCard

from src.home.view.ui.class_dialog import ClassDialog


class HomeView(ft.View):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.route = "/home"
        self.page = page
        if not self.page.client_storage.contains_key("class_list"):
            self.page.client_storage.set("class_list",[])
        if not self.page.client_storage.contains_key("player_list"):
            self.page.client_storage.set("player_list",[])
        self.class_list = self.page.client_storage.get("class_list")
        self.player_list = self.page.client_storage.get("player_list")
        print(f"{self.player_list=}")
        print(f"{self.class_list=}")
        self.dd = ft.Ref[ft.Dropdown]()
        self.tf = ft.Ref[ft.TextField]()

        self.dlg_add_class = ClassDialog(page=self.page)

        self.dlg_add_player = ft.AlertDialog(
            title=ft.Text("Добавить человека"),
            content=ft.Column(
                tight=True,
                controls=[
                    ft.TextField(
                        ref=self.tf,
                        label="Имя игрока",
                        on_change=on_change_obj
                    ),
                    ft.Divider(),
                    ft.Dropdown(
                        ref=self.dd,
                        data=[tuple(cls_dict.values()) for cls_dict in self.class_list],
                        options=[ft.dropdown.Option(cls["name"],data=['qwe']) for cls in self.class_list],
                        on_change=on_change_obj,
                    )
                ]
            ),
            actions=[
                ft.CupertinoFilledButton(
                    on_click=self.add_player,
                    opacity_on_click=0.3,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Icon("ADD"),
                            ft.Text("Добавить человека")
                        ]
                    )
                )
            ]
        )

        self.appbar = ft.AppBar(
            title = ft.Text("MAFIA",size=30,font_family="Dimkin Regular"),
            center_title = True,
            leading=ft.IconButton('ADD',scale=0.8,on_click=lambda _: self.page.open(self.dlg_add_player)),
            actions = [
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            content=ft.Row(
                                [
                                    ft.Icon("ADD"),
                                    ft.Text("Добавить роль"),
                                ]
                            ),
                            on_click=lambda _: self.page.open(self.dlg_add_class)
                        ),
                    ]
                )
            ]
        )    

        self.lv = ft.ListView(expand=1,spacing=5)

        self.controls = [
            self.lv,
        ]

        for player in self.player_list:
            self.lv.controls.append(PlayerCard(player_data=player))

    def add_player(self,e:ft.ControlEvent = None):
        def cheak_obj(obj):
            if not obj.value:
                obj.error_text = 'Обязательно поле'
                obj.update()
                return False
            return True

        if all([cheak_obj(self.dd.current),cheak_obj(self.tf.current)]):
            player = {"pos":len(self.player_list)+1,"name":self.tf.current.value,"cls":self.dd.current.value,"color":dict(self.dd.current.data)[self.dd.current.value]}
            self.player_list += [player]
            self.page.client_storage.set("player_list",self.player_list)
            self.lv.controls.append(PlayerCard(player_data=player))
            self.lv.update()

