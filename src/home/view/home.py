import flet as ft

from flet import colors

class HomeView(ft.View):
    class PlayerCard(ft.Draggable):
        def __init__(self,player_data:dict):
            self.player_data = player_data
            self.ref_leading = ft.Ref[ft.Text]()
            self.ref_title = ft.Ref[ft.Text]()
            self.ref_subtitle = ft.Ref[ft.Text]()
            self.ref_title_f = ft.Ref[ft.Text]()
            self.ref_subtitle_f = ft.Ref[ft.Text]()
            super().__init__(
                group = "",
                content=ft.DragTarget(
                    on_accept=self.drag_accept,
                    content=ft.Container(
                        data=self.player_data,
                        content=ft.Card(
                            content=ft.ListTile(
                                leading=ft.Text(
                                    ref=self.ref_leading,
                                    value=self.player_data["pos"],
                                    size=15,
                                ),
                                title=ft.Text(
                                    ref=self.ref_title,
                                    value=self.player_data["name"],
                                    color=self.player_data["color"]
                                ),
                                subtitle=ft.Text(
                                    ref=self.ref_subtitle,
                                    value=self.player_data["cls"],
                                    color=self.player_data["color"]
                                ),
                                trailing=ft.PopupMenuButton(
                                    items=[
                                        ft.PopupMenuItem(
                                            icon="clear",
                                            text="Убить человека",
                                            on_click=self.kill_player
                                        ),
                                        ft.PopupMenuItem(
                                            icon="delete_rounded",
                                            text="Удалить человек",
                                            on_click=self.remove_player
                                        )
                                    ]
                                )   
                            )
                        )
                    )
                ),
                content_feedback=ft.Container(
                    padding=0,
                    border=ft.border.all(2,"black"),
                    border_radius=15,
                    width=300,
                    height=70,
                    content=ft.Card(
                        margin=0,
                        content=ft.ListTile(
                            leading=ft.Text(
                                value=self.player_data["pos"],
                                size=15,
                            ),
                            title=ft.Text(
                                ref=self.ref_title_f,
                                value=self.player_data["name"],
                                color=self.player_data["color"]
                            ),
                            subtitle=ft.Text(
                                ref=self.ref_subtitle_f,
                                value=self.player_data["cls"],
                                color=self.player_data["color"]
                            ),
                            trailing=ft.PopupMenuButton()
                        )
                    )
                )
            )
        def change_drag(self,data:dict = {},e:ft.ControlEvent=None):
            if data:
                self.player_data = data
                self.ref_leading.current.value = self.player_data["pos"]
                self.ref_title.current.value = self.player_data["name"]
                self.ref_title.current.color = self.player_data["color"]
                self.ref_subtitle.current.value = self.player_data["cls"]   
                self.ref_subtitle.current.color = self.player_data["color"]
                self.ref_title_f.current.value = self.player_data["name"]
                self.ref_title_f.current.color = self.player_data["color"]
                self.ref_subtitle_f.current.value = self.player_data["cls"]
                self.ref_subtitle_f.current.color = self.player_data["color"]
                for i,el in enumerate(self.parent.controls):
                    el.player_data["pos"] = i + 1
                    el.ref_leading.current.value = i + 1
                    el.ref_leading.current.update()
            self.ref_title.current.update()
            self.ref_subtitle.current.update()       
            self.ref_title_f.current.update()
            self.ref_subtitle_f.current.update()     
            self.update()            
        def kill_player(self,e:ft.ControlEvent=None):
            self.player_data["color"] = "grey"
            self.ref_leading.current.color = "grey"
            self.ref_title.current.color = "grey"
            self.ref_subtitle.current.color = "grey"
            self.ref_title_f.current.color = "grey"
            self.ref_subtitle_f.current.color = "grey"
            self.ref_leading.current.update()
            self.ref_title.current.update()
            self.ref_subtitle.current.update()       
            self.ref_title_f.current.update()
            self.ref_subtitle_f.current.update()     
            self.update()    
        def drag_accept(self,e: ft.DragTargetAcceptEvent):
            src = e.control.page.get_control(e.src_id)
            data_1 = src.player_data
            data_2 = e.control.parent.player_data
            src.change_drag(data_2)
            e.control.parent.change_drag(data_1)
        def remove_player(self,e:ft.ControlEvent=None):
            player_list:list = self.parent.parent.player_list
            player_list.remove(self.player_data)
            self.parent.controls.remove(self)
            for i,el in enumerate(self.parent.controls):
                el.player_data["pos"] = i + 1
                el.ref_leading.current.value = i + 1
                el.ref_leading.current.update()
            self.parent.update()
    def __init__(self,page:ft.Page):
        super().__init__()
        self.route = "/home"
        self.page = page
        self.player_list = []
        self.class_list = [
                {"name":"Мафия","color":"red"},
                {"name":"Якудзе","color":"red900"},
                {"name":"Адвокат","color":"red200"},
                {"name":"Маньяк","color":"orange"},
                {"name":"Мирный житель","color":"white"},
                {"name":"Комесар","color":"green200"},
                {"name":"Лунатик","color":"green200"},
                {"name":"Доктор","color":"green200"},
                {"name":"Джокер","color":"green200"},
            ]
        self.dd = ft.Ref[ft.Dropdown]()
        self.tf = ft.Ref[ft.TextField]()

        self.tf_cls = ft.Ref[ft.TextField]()

        self.option_dict = {
            colors.GREEN: self.color_option_creator(colors.GREEN),
            colors.RED: self.color_option_creator(colors.RED),
            colors.WHITE: self.color_option_creator(colors.WHITE),
            colors.ORANGE: self.color_option_creator(colors.ORANGE),
            colors.PURPLE: self.color_option_creator(colors.PURPLE),
            colors.CYAN_500: self.color_option_creator(colors.CYAN_500),
        }
        self.color_options = ft.GridView(
            runs_count=3, max_extent=40, data="", height=50)

        for _, v in self.option_dict.items():
            v.on_click = self.set_color
            self.color_options.controls.append(v)

        self.dlg_add_class = ft.AlertDialog(
            title=ft.Text("Добавить Роль"),
            content=ft.Column(
                tight=True,
                controls=[
                    ft.TextField(
                        ref=self.tf_cls,
                        label="Название роли",
                        on_change=self.on_change_obj
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

        self.dlg_add_player = ft.AlertDialog(
            title=ft.Text("Добавить человека"),
            content=ft.Column(
                tight=True,
                controls=[
                    ft.TextField(
                        ref=self.tf,
                        label="Имя игрока",
                        on_change=self.on_change_obj
                    ),
                    ft.Divider(),
                    ft.Dropdown(
                        ref=self.dd,
                        data=[tuple(cls_dict.values()) for cls_dict in self.class_list],
                        options=[ft.dropdown.Option(cls["name"],data=['qwe']) for cls in self.class_list],
                        on_change=self.on_change_obj,
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

    def on_change_obj(self,e:ft.ControlEvent):
        e.control.error_text = ""
        e.control.update()

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
            self.lv.controls.append(self.PlayerCard(player_data=player))
            self.lv.update()
    def set_color(self,e:ft.ControlEvent):
        for k, v in self.option_dict.items():
            if k == e.control.data:
                v.border = ft.border.all(3, colors.BLACK26)
                self.color_options.data = v.bgcolor
                self.color_options.update()
            else:
                v.border = None
        self.dlg_add_class.content.update()
    
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
            ...