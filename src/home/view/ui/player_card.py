import flet as ft


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
        self.parent.parent.page.client_storage.set("player_list",player_list)
        self.parent.parent.page.update()
        self.parent.controls.remove(self)
        for i,el in enumerate(self.parent.controls):
            el.player_data["pos"] = i + 1
            el.ref_leading.current.value = i + 1
            el.ref_leading.current.update()
        self.parent.update()