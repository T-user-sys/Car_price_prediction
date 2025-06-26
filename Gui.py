import flet as ft
import csv
import os
from datetime import datetime

# Deklaracja obiektów: Ich nazwy, wartości tekstowe, filtry wprowadzanych wartości, typy obiektów
def main(page: ft.Page):  
    page.title = "Car price prediction"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    haptic = ft.HapticFeedback()
    page.overlay.append(haptic)

    # Pole na liczbę koni mechanicznych
    tb_HP = ft.TextField(
        label="Horse Power",
        hint_text="Horse Power",
        input_filter=ft.NumbersOnlyInputFilter(),
        width=200
    )

    # Pole na przebieg pojazdu
    tb_mileage = ft.TextField(
        label="Mileage",
        hint_text="Mileage",
        input_filter=ft.NumbersOnlyInputFilter(),
        width=200
    )

    # Pole na rok produkcji
    tb_year = ft.TextField(
        label="Production Year",
        hint_text="Year of production",
        input_filter=ft.NumbersOnlyInputFilter(),
        width=200
    )

    # Dropdown: skrzynia biegów
    transmission_dropdown = ft.Dropdown(
        label="Transmission",
        width=300,
        options=[
            ft.dropdown.Option("Manual"),
            ft.dropdown.Option("Automatic"),
        ]
    )

    # Dropdown: rodzaj paliwa
    fuel_dropdown = ft.Dropdown(
        label="Fuel",
        width=300,
        options=[
            ft.dropdown.Option("Gas"),
            ft.dropdown.Option("Diesel"),
            ft.dropdown.Option("Hybrid"),
            ft.dropdown.Option("LPG"),
            ft.dropdown.Option("Electric"),
        ]
    )

    # Wynik
    text = ft.Text(
        opacity=0,
        animate_opacity=400,
    )

    # Funkcja zapisująca historię do CSV
    def save_to_history(data):
        file_exists = os.path.isfile('history.csv')
        with open('History.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Timestamp', 'Horse Power', 'Mileage', 'Year', 
                                'Transmission', 'Fuel', 'Estimated Value'])
            writer.writerow(data)

    # Warstwa logiczna obiektów. Wartości konkretnych opcji 
    def button_clicked(e):
        haptic.vibrate()
        try:
            HP = int(tb_HP.value)
        except (ValueError, TypeError):
            text.value = "Error: Input correct number of horse power"
            text.opacity = 1 
            page.update()
            return
        
        try:
            Mileage = int(tb_mileage.value)
        except (ValueError, TypeError):
            text.value = "Error: Input correct mileage"
            text.opacity = 1 
            page.update()
            return
        
        try:
            Year = int(tb_year.value)
        except (ValueError, TypeError):
            text.value = "Error: Input correct year of production"
            text.opacity = 1 
            page.update()
            return

        if transmission_dropdown.value == "Manual":
            Transmission_Manual = 1
        elif transmission_dropdown.value == "Automatic":
            Transmission_Manual = 0
        else:
            text.value = "Chose transmission (Manual/Automatic)"
            text.opacity = 1 
            page.update()
            return

        if fuel_dropdown.value == "Diesel":
            Fuel_Gas = 0
            Fuel_Electric = 0
            Fuel_Hybrid = 0
            Fuel_LPG = 0
        elif fuel_dropdown.value == "Gas":
            Fuel_Gas = 1
            Fuel_Electric = 0
            Fuel_Hybrid = 0
            Fuel_LPG = 0
        elif fuel_dropdown.value == "Electric":
            Fuel_Gas = 0
            Fuel_Electric = 1
            Fuel_Hybrid = 0
            Fuel_LPG = 0
        elif fuel_dropdown.value == "Hybrid":
            Fuel_Gas = 0
            Fuel_Electric = 0
            Fuel_Hybrid = 1
            Fuel_LPG = 0
        elif fuel_dropdown.value == "LPG":
            Fuel_Gas = 0
            Fuel_Electric = 0
            Fuel_Hybrid = 0
            Fuel_LPG = 1
        else:
            text.value = "Input fuel type"
            text.opacity = 1 
            page.update()
            return

        # Obliczenia
        CAR_VALUE = -3629424.4660 - 0.0760 * Mileage + 1796.8177 * Year + 233.1252 * HP - 11198.4543 * Fuel_Electric - 3389.1961 * Fuel_Gas - 1171.1920 * Fuel_Hybrid - 4388.0221 * Fuel_LPG - 1776.4866 * Transmission_Manual  
        # Zapis do historii
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_to_history([
            timestamp,
            HP,
            Mileage,
            Year,
            transmission_dropdown.value,
            fuel_dropdown.value,
            f"{CAR_VALUE:.2f} €"
        ])         
        text.value = f"Estimated car value is: {CAR_VALUE:.2f} €"
        text.opacity = 1
        page.update()

    # Funkcja czyszczenia historii
    def clear_history(e):
        haptic.vibrate()
        if os.path.exists("history.csv"):
            os.remove("history.csv")
            text.value = "History cleared successfully! History.csv file has been deleted!"
        else:
            text.value = "No history file found"
        text.opacity = 1
        page.update()

    calculate_button = ft.ElevatedButton(
        text="Calculate",
        width=250,
        on_click=button_clicked
    )
    
    clear_button = ft.ElevatedButton(
        text="Clear History",
        width=250,
        color="white",
        bgcolor="red",
        on_click=clear_history
    )

 # Ustawienia responsywności
    tb_HP.col = {"sm": 12, "md": 4}
    tb_mileage.col = {"sm": 12, "md": 4}
    tb_year.col = {"sm": 12, "md": 4}
    transmission_dropdown.col = {"sm": 12, "md": 6}
    fuel_dropdown.col = {"sm": 12, "md": 6}
    calculate_button.col = {"sm": 12, "md": 12}
    text.col = {"sm": 12, "md": 12}

    # Kontener z przyciskami w kolumnie
    buttons_column = ft.Column([
        ft.ResponsiveRow([calculate_button]),
        ft.ResponsiveRow([clear_button])
    ], spacing=10)

    # Główny kontener
    container = ft.Container(
        content=ft.ResponsiveRow(
            controls=[
                tb_HP,
                tb_mileage,
                tb_year,
                transmission_dropdown,
                fuel_dropdown,
                buttons_column,
                text
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        ),
        width=600,
        alignment=ft.alignment.center
    )

    page.add(container)

ft.app(target=main)