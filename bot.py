import json
import urllib.request
import re

# Słowa kluczowe, których bot szuka w internecie
SZUKANE_FRAZY = ["orenburg", "lokomotiv"]

# Strona źródłowa, z której bot pobiera aktualny plan transmisji
URL_ZRODLA = "https://meczyki.pl"

print("Bot streamingowy szuka meczu o 16:00...")

try:
    # Pobieranie kodu źródłowego strony źródłowej
    req = urllib.request.Request(URL_ZRODLA, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req) as response:
        kod_strony = response.read().decode('utf-8')

    aktualne_mecze = []

    # Sprawdzamy, czy w kodzie strony są nasze drużyny
    if "orenburg" in kod_strony.lower() or "lokomotiv" in kod_strony.lower():
        print("Znaleziono mecz ligi rosyjskiej w kodzie!")
        
        # Automatyczne przeszukiwanie kodu w poszukiwaniu linków
        linki = re.findall(r'href=[\'"]?([^\'" >]+)', kod_strony)
        prawdziwy_stream = "#"
        
        for l in linki:
            if "live" in l or "stream" in l or "player" in l:
                if l.startswith("http"):
                    prawdziwy_stream = l
                    break
        
        # Jeśli bot nie znalazł bezpośredniego wideo, podaje stronę główną meczu
        if prawdziwy_stream == "#":
            prawdziwy_stream = URL_ZRODLA

        # Dodanie meczu do bazy danych strony
        aktualne_mecze.append({
            "mecz": "Orenburg - Lokomotiv Moskwa",
            "dyscyplina": "⚽ Piłka Nożna",
            "liga": "Rosyjska Priemjer Liga",
            "godzina": "16:00 LIVE",
            "status": "Na żywo",
            "link": prawdziwy_stream
        })

    # Jeśli na stronie źródłowej nie ma jeszcze meczu
    if not aktualne_mecze:
        aktualne_mecze = [{
            "mecz": "Orenburg - Lokomotiv Moskwa",
            "dyscyplina": "⚽ Piłka Nożna",
            "liga": "Rosyjska Priemjer Liga",
            "godzina": "16:00",
            "status": "Oczekuje",
            "link": "#"
        }]

    # Zapis i eksport danych do pliku JSON strony www
    with open("mecze.json", "w", encoding="utf-8") as f:
        json.dump(aktualne_mecze, f, ensure_ascii=False, indent=2)
    print("Plik mecze.json został zaktualizowany!")

except Exception as e:
    print(f"Błąd bota podczas pracy: {e}")
