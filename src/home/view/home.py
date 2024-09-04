import flet as ft

class HomeView(ft.View):
    class PlayerCard(ft.Draggable):
        def __init__(self,pos:int,name:str,cls:str,color:str):
            self.player_data = {"pos":pos,"name":name,"cls":cls,"color":color}
            super().__init__(
                group = "",
                content=ft.DragTarget(
                    on_accept=self.drag_accept,
                    content=ft.Container(
                        data=self.player_data,
                        content=ft.Card(
                            content=ft.ListTile(
                                leading=ft.Text(
                                    value=self.player_data["pos"],
                                    size=15,
                                ),
                                title=ft.Text(
                                    value=self.player_data["name"],
                                    color=self.player_data["color"]
                                ),
                                subtitle=ft.Text(
                                    value=self.player_data["cls"],
                                    color=self.player_data["color"]
                                ),
                                trailing=ft.PopupMenuButton(
                                    items=[
                                        ft.PopupMenuItem(
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
                                value=self.player_data["name"],
                                color=self.player_data["color"],
                            ),
                            subtitle=ft.Text(
                                value=self.player_data["cls"],
                                color=self.player_data["color"],
                            ),
                            trailing=ft.PopupMenuButton()
                        )
                    )
                )
            )


        def drag_accept(self,e: ft.DragTargetAcceptEvent):
            # def change_drag(obj,data):
            #     pos,name,cls,color = data

            #     obj.title.value = name
            #     obj.title.color = color
            #     obj.subtitle.value = cls 
            #     obj.subtitle.color = color 
            #     obj.update()
            src = e.control.page.get_control(e.src_id)
            data_1 = src.player_data
            data_2 = e.control.content.data
            src.player_data = data_2
            print(data_1,data_2)
            # item_1 = src.content.content.content.content
            # item_2 = e.control.content.content.content
            # item_1_f = src.content_feedback.content.content
            # item_2_f = e.concontent_feedback.content.content
            # print(item_2_f)
            # change_drag(src,data_2)
            # change_drag(e,data_1)

            # change_drag(item_1_f,data_2)
            # change_drag(item_2_f,data_1)

        def remove_player(self,e:ft.ControlEvent):
            ...
        def change_status(self,e:ft.ControlEvent):
            def change_text(text_obj,status=True):
                if status:
                    text_obj.style = None
                    text_obj.update()
                else:
                    text_obj.style = ft.TextStyle(
                        decoration=ft.TextDecoration.LINE_THROUGH,
                        decoration_thickness=3,
                    )
                    text_obj.update()
            self.status = False if self.status else True
            if self.status:
                change_text(self.pos_ref)
                change_text(self.name_ref)                
                change_text(self.subtitle_ref)
    def __init__(self,page:ft.Page):
        super().__init__()
        self.route = "/home"

        self.page = page

        self.player_list = []

        self.class_list = [
            ("Мафия","red"),
            ("Мирный житель","white"),
        ]

        self.dd = ft.Dropdown(
            options=[ft.dropdown.Option(cls[0]) for cls in self.class_list],
            on_change=self.on_change_obj,
        )

        self.tf = ft.TextField(
            label="Имя игрока",
            on_change=self.on_change_obj
        )

        self.dlg = ft.AlertDialog(
            title=ft.Text("Добавить человека"),
            content=ft.Column(
                tight=True,
                controls=[
                    self.tf,
                    ft.Divider(),
                    self.dd
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
            leading=ft.IconButton('ADD',scale=0.8,on_click=lambda _: self.page.open(self.dlg)),
            actions = [
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Удалить всех"),
                    ]
                )
            ]
        )    

        self.lv = ft.ListView(
            expand=1,
            spacing=5,
            controls=[
                self.PlayerCard(1,"qwe","Мафия","red"),
                self.PlayerCard(2,"123","Мирный житель","white"),
            ]
        )

        self.controls = [
            self.lv,
        ]

    def on_change_obj(self,e:ft.ControlEvent):
        e.control.error_text = ""
        e.control.update()

    def add_player(self,e:ft.ControlEvent):
        def cheak_obj(obj):
            if not obj.value:
                obj.error_text = 'Обязательно поле'
                obj.update()
                return False
            return True

        if all([cheak_obj(self.dd),cheak_obj(self.tf)]):
            self.player_list.append(
                (self.tf.value,self.dd.value,dict(self.class_list)[self.dd.value])
            )
            self.lv.controls.append(
                self.PlayerCard(len(self.player_list),self.tf.value,self.dd.value,dict(self.class_list)[self.dd.value])
            )
            self.lv.update()

    def remove_player(self,e:ft.ControlEvent):
        print(e.control.parent)
