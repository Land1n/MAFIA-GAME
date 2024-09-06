import flet as ft

from src.router import Router
from src.database import DataBase

def main(page:ft.Page):
    page.title = 'ZAL'
    router = Router(page)
    page.fonts = {
        "Dimkin Regular": "fonts/Dimkin Regular.ttf",
    }
    page.on_route_change = router.route_change
    page.views.clear()
    page.go("/home") 
    

if __name__ == '__main__':
    ft.app(main)