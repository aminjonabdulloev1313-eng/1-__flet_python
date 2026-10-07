import json
import os
import flet as ft

# ООП: Класс для работы с внешними данными (симуляция обмена с 1С)
class DataManager:
    def __init__(self, filename="data.json"):
        self.filename = filename

    def load_data(self):
        """Метод чтения JSON-файла с номенклатурой"""
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
        return []

# ООП: Главный класс приложения на Flet
class OneCApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "АРМ 1С: Каталог номенклатуры"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        self.db = DataManager()
        
        # Компонент 1: Заголовок приложения (ft.Text)
        self.title_text = ft.Text("Каталог номенклатуры (Интеграция 1С)", size=22, weight="bold", color="teal")
        
        # Компонент 2: Поле поиска по товарам (ft.TextField)
        self.search_input = ft.TextField(hint_text="Поиск товара...", width=250, on_change=self.filter_items)
        
        # Компонент 3: Кнопка обновления (ft.Button для Flet 1.0+)
        self.refresh_btn = ft.Button("Обновить из 1С", icon="refresh", on_click=self.refresh_data)
        
        # Компонент 4: Строка для размещения поиска и кнопки рядом (ft.Row)
        self.top_row = ft.Row([self.search_input, self.refresh_btn], alignment=ft.MainAxisAlignment.CENTER)
        
        # Компонент 5: Прокручиваемый список элементов (ft.ListView)
        self.items_list = ft.ListView(expand=1, spacing=5, padding=10, auto_scroll=True)
        
        # Компонент 6: Карточка-контейнер для оформления списка (ft.Card)
        self.items_card = ft.Card(
            content=ft.Container(
                content=self.items_list,
                padding=10,
                width=450,
                height=300
            )
        )
        
        # Компонент 7: Общая колонка для компоновки всех элементов на экране (ft.Column)
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
        """Метод для загрузки элементов каталога в список"""
        self.items_list.controls.clear()
        data = self.db.load_data()
        for item in data:
            self.items_list.controls.append(
                ft.ListTile(
                    leading=ft.Icon("inventory", color="teal"),
                    title=ft.Text(item["name"], weight="bold"),
                    subtitle=ft.Text(f"Цена: {item['price']} тенге | Остаток: {item['stock']} шт.")
                )
            )
        self.page.update()

    def refresh_data(self, e):
        """Метод обработки нажатия кнопки обновления"""
        self.load_catalog()
        print("Данные успешно синхронизированы!")

    def filter_items(self, e):
        """Метод динамической фильтрации товаров при вводе текста"""
        query = self.search_input.value.lower()
        self.items_list.controls.clear()
        data = self.db.load_data()
        for item in data:
            if query in item["name"].lower():
                self.items_list.controls.append(
                    ft.ListTile(
                        leading=ft.Icon("inventory", color="teal"),
                        title=ft.Text(item["name"], weight="bold"),
                        subtitle=ft.Text(f"Цена: {item['price']} тенге | Остаток: {item['stock']} шт.")
                    )
                )
        self.page.update()

def main(page: ft.Page):
    app = OneCApp(page)

ft.run(main)