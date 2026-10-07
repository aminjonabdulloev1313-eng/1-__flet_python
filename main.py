import json
import os
import flet as ft

class DataManager:
    def __init__(self, filename="data.json"):
        self.filename = filename

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
       
        return [
            {"name": "Товар 1 (Пример)", "price": 150, "stock": 10},
            {"name": "Товар 2 (Пример)", "price": 300, "stock": 5}
        ]


def create_product_tile(item):
    return ft.Container(
        content=ft.ListTile(
            leading=ft.Icon(ft.Icons.INVENTORY, color="teal"),
            title=ft.Text(
                item["name"], 
                weight=ft.FontWeight.BOLD,
                size=16,
                selectable=True
            ),
            subtitle=ft.Text(
                f"Цена: {item['price']} смн  •  Остаток: {item['stock']} шт.",
                color="grey700"
            ),
            is_three_line=True
        ),
        padding=ft.padding.all(8),
        border=ft.border.all(1, "grey300"),
        border_radius=8,
        margin=ft.margin.only(bottom=8)
    )

class OneCApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "1С: Номенклатура"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        self.db = DataManager()
        self.init_ui()

    def init_ui(self):
        self.title_text = ft.Text("Номенклатура", size=22, weight="bold", color="teal")
        
        self.search_input = ft.TextField(
            hint_text="Поиск товара...", 
            width=250, 
            on_change=self.filter_items
        )
        
        self.refresh_btn = ft.ElevatedButton(
            "Получить с 1С", 
            icon=ft.Icons.REFRESH, 
            on_click=self.refresh_data
        )
        
        self.top_row = ft.Row(
            [self.search_input, self.refresh_btn], 
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        self.items_list = ft.ListView(expand=1, spacing=5, padding=10, auto_scroll=True)
        
        self.items_card = ft.Card(
            content=ft.Container(
                content=self.items_list,
                padding=10,
                width=450,
                height=300
            )
        )
        
        self.main_column = ft.Column(
            [
                self.title_text,
                self.top_row,
                self.items_card
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
        
        self.page.add(self.main_column)
        self.load_catalog()

    def load_catalog(self):
        self.items_list.controls.clear()
        data = self.db.load_data()
        
        for item in data:
            # Вызываем наш креатор вместо громоздкого кода
            self.items_list.controls.append(create_product_tile(item))
            
        self.page.update()

    def refresh_data(self, e):
        self.load_catalog()
        print("Синхронизация успешна!")

    def filter_items(self, e):
        query = self.search_input.value.lower() if self.search_input.value else ""
        self.items_list.controls.clear()
        data = self.db.load_data()
        
        for item in data:
            if query in item["name"].lower():
                self.items_list.controls.append(create_product_tile(item))
                
        self.page.update()

def main(page: ft.Page):
    OneCApp(page)

ft.app(target=main)
