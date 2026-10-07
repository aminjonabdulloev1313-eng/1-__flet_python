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
        return []

class OneCApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "1С: Номенклатура"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        self.db = DataManager()
        
        self.title_text = ft.Text("Номенклатура", size=22, weight="bold", color="teal")
        self.search_input = ft.TextField(hint_text="Поиск товара...", width=250, on_change=self.filter_items)
        self.refresh_btn = ft.Button("Получить с 1С", icon="refresh", on_click=self.refresh_data)
        
        self.top_row = ft.Row([self.search_input, self.refresh_btn], alignment=ft.MainAxisAlignment.CENTER)
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
            self.items_list.controls.append(
                ft.Container(
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
                    padding=ft.Padding(left=8, top=4, right=8, bottom=4),
                    border=ft.Border.all(width=1, color="grey300"),
                    border_radius=8,
                    margin=ft.Margin(left=0, top=0, right=0, bottom=8)
                )
            )
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
                self.items_list.controls.append(
                    ft.Container(
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
                        padding=ft.Padding(left=8, top=4, right=8, bottom=4),
                        border=ft.Border.all(width=1, color="grey300"),
                        border_radius=8,
                        margin=ft.Margin(left=0, top=0, right=0, bottom=8)
                    )
                )
        self.page.update()

def main(page: ft.Page):
    app = OneCApp(page)

ft.run(main)