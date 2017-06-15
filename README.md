# Adresse

Dette prosjektet benytter data fra Kartverket, som kan hentes inn fra
[data.kartverket.no](http://data.kartverket.no/download/content/geodataprodukter?korttype=3637&aktualitet=All&datastruktur=All&dataskema=All).

Ettersom det er veldig mye data i `.csv`-filene deres, er dette naturlig nok mye man kanskje ikke trenger.

Dette prosjektet henter ut kun den informasjonen man trenger, og passer på at hver data-objekt er unikt, slik at man ikke får flere oppføringer på samme adressen.

# Mål

Målet er å sette dette inn i en database. Men dette krever et database-system som håndterer datamengden, selv om vi bare sitter igjen med ca 5% av dataen fra kartverket.

Foreløbig blir dataen hentet ut og lagret i en JSON-fil, men det kan enkelt endres til å benytte en database.

# Bruk

kjør filen `python3 adresse.py` for å hente ut dataen og lage JSON-filen. Merk at dette tar noe tid, men minnehåndteringen er optimalisert, og programmet kan dermed bare stå i bakgrunnen for å jobbe seg ferdig.

## Tidsbruk

For øyeblikket tar dette ca 25 sekunder å bygge opp dataen.
