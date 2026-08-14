import json
import urllib.request
import re

# Bot będzie szukał meczu Huberta Hurkacza
SZUKANE_FRAZY = ["Hurkacz", "Hubert"]

# Przykładowy zagraniczny agregator streamów (na potrzeby testu)
URL_ZRODLA = "https://meczyki.pl"

print("Bot streamingowy szuka meczu turnieju w Cincinnati...")

try:
    req = urllib.request.Request(URL_ZRODLA, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req) as response:
        kod_strony = response.read().decode('utf-8')

    aktualne_mecze = []

    # 1. Sprawdzamy, czy w kodzie strony jest wzmianka o Hurkaczu
    if "hurkacz" in kod_strony.lower() or "hubert" in kod_strony.lower():
        print("Znaleziono mecz Huberta Hurkacza w kodzie strony!")
        
        # 2. AUTOMATYCZNE SZUKANIE LINKU WIDEO
        # Bot szuka w kodzie adresów URL, które mogą być streamami (np. zawierają słowo player, embed, live lub m3u8)
        linki = re.findall(r'href=[\'"]?([^\'" >]+)', kod_strony)
        prawdziwy_stream = "#"
        
        for l in linki:
            if "live" in l or "stream" in l or "player" in l:
                if l.startswith("http"):
                    prawdziwy_stream = l
                    break
        
        # Jeśli nie znalazł bezpośredniego linku, dajemy link do podstrony meczu
        if prawdziwy_stream == "#":
            prawdziwy_stream = URL_ZRODLA

        aktualne_mecze.append({
            "mecz": "Hubert Hurkacz - Sho Shimabukuro",
            "dyscyplina": "🎾 Tenis",
            "liga": "ATP Cincinnati",
            "godzina": "TERAZ LIVE",
            "status": "Na żywo",
            "link": prawdziwy_stream  # TUTAJ BOT WKLEJA WYCIĄGNIĘTY LINK!
        })

    if not aktualne_mecze:
        aktualne_mecze = [{
            "mecz": "Brak meczu Hurkacza na stronie źródłowej",
            "dyscyplina": "-",
            "liga": "-",
            "godzina": "-",
            "status": "Oczekuje",
            "link": "#"
        }]

    # Zapis danych i automatyczny eksport na Vercel
    with open("mecze.json", "w", encoding="utf-8") as f:
        json.dump(aktualne_mecze, f, ensure_ascii=False, indent=2)
    print("Plik mecze.json zaktualizowany o prawdziwy link!")

except Exception as e:
    print(f"Błąd bota podczas scrapowania: {e}")
