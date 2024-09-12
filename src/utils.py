import flet as ft

def on_change_obj(e:ft.ControlEvent):
    e.control.error_text = ""
    e.control.update()

def on_keyboard(e: ft.KeyboardEvent):
    if e.key == "`" and e.shift:
        e.control.client_storage.clear()
        e.control.update()
        print(e.control.client_storage.get_keys("key-prefix."))
