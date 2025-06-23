import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Lista do przechowywania danych
data_list = []

# Podstawowy URL
base_url = "https://www.autosphere.be"

# Iteracja po stronach wyników
for i in range(0, 1081, 30):
    print(f"Pobieranie strony {i}")
    url = f"{base_url}/nl/wagen?size=30&from={i}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Błąd pobierania strony {i}")
        continue
    
    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.find_all("a", class_="ss_link")
    
    for listing in listings:
        link = base_url + listing["href"]
        print(f"Przetwarzanie oferty: {link}")
        
        offer_response = requests.get(link)
        if offer_response.status_code != 200:
            print(f"Błąd pobierania oferty {link}")
            continue
        
        offer_soup = BeautifulSoup(offer_response.text, 'html.parser')
        
        # Pobieranie danych z oferty
        details_section = offer_soup.find("section", class_="single-vehicle-description__tab-pane__block")
        details = details_section.find_all("li") if details_section else []
        
        data = {"ID": "", "Marka": "", "Model": "", "Wersja": "", "Paliwo": "", "Przebieg": "",
                "Rok": "", "Skrzynia": "", "Cena": "", "Nadwozie": "", "CO2": "", "Kolor": "", 
                "Norma Euro": "", "Drzwi": "", "Moc": "", "Opis oferty": "", "Link": link}
        
        for detail in details:
            label = detail.find("span", class_="single-vehicle-description__tab-pane__prop")
            value = detail.find("span", class_="single-vehicle-description__tab-pane__value")
            if not label or not value:
                continue
            
            label_text = label.text.strip()
            value_text = value.text.strip()
            
            if "Referentievoertuig" in label_text:
                data["ID"] = value_text
            elif "Merk" in label_text:
                data["Marka"] = value_text
            elif "Model" in label_text:
                data["Model"] = value_text
            elif "Versie" in label_text:
                data["Wersja"] = value_text
            elif "Brandstof" in label_text:
                data["Paliwo"] = value_text
            elif "Km" in label_text:
                data["Przebieg"] = value_text
            elif "Jaar" in label_text:
                data["Rok"] = value_text
            elif "Versnellingsbak" in label_text:
                data["Skrzynia"] = value_text
            elif "Prijs BTW inclusief" in label_text:
                data["Cena"] = value_text
            elif "Koetswerk" in label_text:
                data["Nadwozie"] = value_text
            elif "CO2" in label_text:
                data["CO2"] = value_text
            elif "Kleur" in label_text:
                data["Kolor"] = value_text
            elif "Euro Norm" in label_text:
                data["Norma Euro"] = value_text
            elif "Deuren" in label_text:
                data["Drzwi"] = value_text
            elif "Vermogen" in label_text:
                data["Moc"] = value_text
        
        # Pobieranie opisu
        description_section = offer_soup.find_all("div", class_="single-vehicle-description__tab-pane__description-content wysiwyg-content")

        if description_section and len(description_section) > 1:  # Sprawdzenie czy lista ma wystarczającą liczbę elementów
            data["Opis oferty"] = description_section[1].get_text(strip=True)    
            print(data["Opis oferty"])  # Dodano nową linię po print

        data_list.append(data)  # To było wcześniej błędnie umieszczone w tej samej linii co print
        time.sleep(1)

# Tworzenie DataFrame i zapis do CSV
df = pd.DataFrame(data_list)
df.to_csv("Oferty_aut.csv", index=False, encoding="utf-8", sep=";")
print("Zapisano dane do pliku Oferty_aut.csv!")
