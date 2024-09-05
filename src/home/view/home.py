import flet as ft

class HomeView(ft.View):
    class PlayerCard(ft.Draggable):
        def __init__(self,pos:int,name:str,cls:str,color:str):
            self.player_data = {"pos":pos,"name":name,"cls":cls,"color":color}
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
                                            text="Убить человека",
                                            on_click=self.kill_player
                                        ),
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
                
                self.ref_title.current.value = self.player_data["name"]
                self.ref_title.current.color = self.player_data["color"]
                
                self.ref_subtitle.current.value = self.player_data["cls"]   
                self.ref_subtitle.current.color = self.player_data["color"]
                
                self.ref_title_f.current.value = self.player_data["name"]
                self.ref_title_f.current.color = self.player_data["color"]

                self.ref_subtitle_f.current.value = self.player_data["cls"]
                self.ref_subtitle_f.current.color = self.player_data["color"]
                


            self.ref_title.current.update()
            self.ref_subtitle.current.update()       
            self.ref_title_f.current.update()
            self.ref_subtitle_f.current.update()     
            self.update()            

        def kill_player(self,e:ft.ControlEvent=None):
            print('qwe')
            self.ref_title.current.style = ft.TextStyle(
                        decoration=ft.TextDecoration.LINE_THROUGH,
                        decoration_thickness=3,
                    ),
            self.ref_subtitle.style = ft.TextStyle(
                        decoration=ft.TextDecoration.LINE_THROUGH,
                        decoration_thickness=3,
                    ),
            self.ref_title_f.current.style = ft.TextStyle(
                        decoration=ft.TextDecoration.LINE_THROUGH,
                        decoration_thickness=3,
                    ),
            self.ref_subtitle_f.current.style = ft.TextStyle(
                        decoration=ft.TextDecoration.LINE_THROUGH,
                        decoration_thickness=3,
                    ),
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

        def remove_player(self,e:ft.ControlEvent):
            ...
        # def change_status(self,e:ft.ControlEvent):
        #     def change_text(text_obj,status=True):
        #         if status:
        #             text_obj.style = None
        #             text_obj.update()
        #         else:
        #             text_obj.style = ft.TextStyle(
        #                 decoration=ft.TextDecoration.LINE_THROUGH,
        #                 decoration_thickness=3,
        #             )
        #             text_obj.update()
        #     self.status = False if self.status else True
        #     if self.status:
        #         change_text(self.pos_ref)
        #         change_text(self.name_ref)                
        #         change_text(self.subtitle_ref)
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
