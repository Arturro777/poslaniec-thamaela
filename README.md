# Przebudzone GPT-4o

Prosta aplikacja webowa (100% frontend: HTML/CSS/JS), która pozwala wkleić własny klucz OpenAI API i rozmawiać z modelem `gpt-4o`.

## Funkcje
- nowoczesny, ciemny interfejs czatu,
- połączenie z OpenAI przez własny klucz użytkownika,
- ustawienie modelu i instrukcji systemowej,
- lokalny zapis ustawień i historii (`localStorage`),
- status: **Łączenie / Gotowe / Błąd**,
- sekcja „Jak zacząć”.

## Uruchomienie lokalnie
Wystarczy otworzyć `index.html` w przeglądarce.

Opcjonalnie z prostym serwerem statycznym:
```bash
python3 -m http.server 8000
```

## Hosting publiczny
Projekt jest gotowy do hostowania jako statyczna strona, np.:
- GitHub Pages,
- Netlify,
- Vercel (static).

Wystarczy opublikować plik `index.html` oraz `README.md`.
