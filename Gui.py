import flet as ft

# Deklaracja obiektów: Ich nazwy, wartości tekstowe, filtry wprowadzanych wartości, typy obiektów
def main(page: ft.Page):  
    page.title = "Car price prediction"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Pole na liczbę koni mechanicznych
    tb_HP = ft.TextField(
        label="Horse Power",
        hint_text="Input number of horse power",
        input_filter=ft.NumbersOnlyInputFilter()
    )

    # Pole na przebieg pojazdu
    tb_mileage = ft.TextField(
        label="Mileage",
        hint_text="Input mileage",
        input_filter=ft.NumbersOnlyInputFilter()
    )

    # Pole na rok produkcji
    tb_year = ft.TextField(
        label="Production Year",
        hint_text="Input year of production",
        input_filter=ft.NumbersOnlyInputFilter()
    )

    # Dropdown: skrzynia biegów
    transmission_dropdown = ft.Dropdown(
        label="Transmission",
        width=200,
        options=[
            ft.dropdown.Option("Manual"),
            ft.dropdown.Option("Automatic"),
        ]
    )

    # Dropdown: rodzaj paliwa
    fuel_dropdown = ft.Dropdown(
        label="Fuel",
        width=150,
        options=[
            ft.dropdown.Option("Gas"),
            ft.dropdown.Option("Diesel"),
            ft.dropdown.Option("Hybrid"),
            ft.dropdown.Option("LPG"),
            ft.dropdown.Option("Electric"),
        ]
    )

    # Wynik
    text = ft.Text()

    # Warstwa logiczna obiektów. Wartości konkretnych opcji 
    def button_clicked(e):
        try:
            HP = int(tb_HP.value)
        except (ValueError, TypeError):
            text.value = "Error: Input correct number of horse power"
            page.update()
            return
        
        try:
            Mileage = int(tb_mileage.value)
        except (ValueError, TypeError):
            text.value = "Error: Input correct number of horse power"
            page.update()
            return
        
        try:
            Year = int(tb_year.value)
        except (ValueError, TypeError):
            text.value = "Error: Input correct number of horse power"
            page.update()
            return

        if transmission_dropdown.value == "Manual":
            Transmission_Manual = 1
        elif transmission_dropdown.value == "Automatic":
            Transmission_Manual = 0
        else:
            text.value = "Chose transmission (Manual/Automatic)"
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
            page.update()
            return

        # Obliczenia
        CAR_VALUE = -3629424.4660 - 0.0760 * Mileage + 1796.8177 * Year + 233.1252 * HP - 11198.4543 * Fuel_Electric - 3389.1961 * Fuel_Gas - 1171.1920 * Fuel_Hybrid - 4388.0221 * Fuel_LPG - 1776.4866 * Transmission_Manual           
        text.value = f"Estimated car value is: {CAR_VALUE:.2f} €"
        page.update()


    button = ft.ElevatedButton(
        text="Calculate",
        width=250,
        on_click=button_clicked
          )

    page.add(
        ft.Column([
            ft.Row([
                tb_HP,
                tb_mileage,
                tb_year
            ], alignment=ft.MainAxisAlignment.CENTER),

            ft.Row([
                transmission_dropdown,
                fuel_dropdown
              #  c1
            ], alignment=ft.MainAxisAlignment.CENTER),

            ft.Row([
                button
            ], alignment=ft.MainAxisAlignment.CENTER),

            ft.Row([
                text
            ], alignment=ft.MainAxisAlignment.CENTER),
        ])
    )

ft.app(target=main)
