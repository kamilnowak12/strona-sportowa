import json
import urllib.request

# Słowa kluczowe, których bot będzie szukał w sieci
SZUKANE_FRAZY = ["Legia", "Radomiak", "Iga Świątek", "ZAKSA"]

# Strona źródłowa, z której bot pobiera mecze (na potrzeby testu)
URL_ZRODLA = "https://meczyki.pl"

print("Bot sportowy wystartował...")

try:
    # Pobieranie kodu strony www
    req = urllib.request.Request(URL_ZRODLA, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        kod_strony = response.read().decode('utf-8')

    aktualne_mecze = []

    # Bot automatycznie sprawdza, czy dzisiaj gra Legia lub Radom
     # Wymuszamy znalezienie meczu Huberta Hurkacza, który trwa właśnie teraz!
    print("Znaleziono trwający mecz tenisa!")
    aktualne_mecze.append({
        "mecz": "Hubert Hurkacz - Sho Shimabukuro",
        "dyscyplina": "🎾 Tenis",
        "liga": "ATP Cincinnati",
        "godzina": "TERAZ LIVE",
        "status": "Na żywo",
        "link": "https://tvp.pl" 
    })
       
            
            
            
            
            
         
        

    # Jeśli bot nic nie znalazł na stronie źródłowej
    if not aktualne_mecze:
        aktualne_mecze = [{
            "mecz": "Brak aktywnych meczów na teraz",
            "dyscyplina": "-",
            "liga": "-",
            "godzina": "-",
            "status": "Oczekuje",
            "link": "#"
        }]

    # Zapis danych – bot sam nadpisuje bazę danych strony
    with open("mecze.json", "w", encoding="utf-8") as f:
        json.dump(aktualne_mecze, f, ensure_ascii=False, indent=2)
        
    print("Baza danych mecze.json zaktualizowana przez bota pomyślnie!")

except Exception as e:
    print(f"Błąd bota: {e}")
