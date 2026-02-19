import os, sys, json, re
import requests

API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()
MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.2").strip()
PROMPT = sys.argv[1] if len(sys.argv) > 1 else ""

if not API_KEY:
    raise SystemExit("Brak OPENAI_API_KEY (sprawdź: Ustawienia → Sekrety i zmienne → Akcje).")

system = """
Jesteś senior frontend developerem. Tworzysz kompletną statyczną aplikację WWW pod GitHub Pages.
Wymagania:
- Tylko statyczne pliki: index.html, style.css, app.js (bez backendu, bez kluczy API w kodzie).
- Brak frameworków i bundlerów. Czysty HTML/CSS/JS.
- Aplikacja ma działać od razu po wejściu w link GitHub Pages.
- Użyj localStorage do zapisu danych (jeśli potrzebne).
Zwróć WYŁĄCZNIE poprawny JSON o strukturze:
{
  "index.html": "...",
  "style.css": "...",
  "app.js": "..."
}
Bez markdown, bez komentarzy, bez dodatkowego tekstu.
"""

def call_openai_chat():
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": PROMPT},
        ],
        "temperature": 0.2,
    }
    r = requests.post(url, headers=headers, json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"]

raw = call_openai_chat().strip()

# Spróbuj wczytać JSON wprost, a jak nie, wytnij największy blok {...}
try:
    obj = json.loads(raw)
except Exception:
    m = re.search(r"\{.*\}", raw, re.S)
    if not m:
        raise SystemExit("Model nie zwrócił JSON. Sprawdź logi workflow w zakładce Akcje.")
    obj = json.loads(m.group(0))

for key in ["index.html", "style.css", "app.js"]:
    if key not in obj or not isinstance(obj[key], str):
        raise SystemExit(f"Brak pola {key} w JSON albo ma zły format.")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(obj["index.html"])
with open("style.css", "w", encoding="utf-8") as f:
    f.write(obj["style.css"])
with open("app.js", "w", encoding="utf-8") as f:
    f.write(obj["app.js"])

print("OK: zapisano index.html, style.css, app.js")
