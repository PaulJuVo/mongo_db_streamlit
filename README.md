## DB

TEST

### PYMONGO DOK

[Pymongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/databases-collections/#database)

### SETUP

docker compose up -d
docker compose up --build wenn änderung

streamlit run app/streamlit_app.py

# Projektübersicht

Dieses Projekt stellt eine Daten-Pipeline mit MongoDB, Python und einem Dashboard bereit, um JSON-Daten zu verarbeiten und aufzubereiten.

## Komponenten

- **Docker-Compose**: Startet alle notwendigen Services (App, MongoDB, Dashboard).
- **Dockerfile**: Baut das App-Image mit allen Abhängigkeiten.
- **MongoDB Entry-Point-Skript**:
  - Erstellt zwei Datenbanken: `RAW` und `Processed`.
  - Erstellt zwei Nutzer:
    - **App-User**: Lese- und Schreibrechte auf `RAW` und `Processed`.
    - **Dashboard-User**: Nur Lesezugriff auf `Processed`.

## Dashboard

- Weboberfläche zum Hochladen von JSON-Dateien:
  - Drag & Drop oder klassische Dateiauswahl.
  - Validierung des groben Schemas.
  - Speicherung der Daten in der `RAW`-Datenbank.  
    _(Die Daten werden nicht verändert, nur gespeichert.)_

## Pipeline

1. **Rohdaten → Staging-Area**

   - Nested Objects/Arrays werden entpackt.
   - Einfache Transformationen ohne Business-Logik.
   - Verwendung von MongoDB Aggregation Framework.

2. **Staging-Area → Temporäre Processed-Collection (Python)**

   - Business-Logik wird angewendet.
   - Datenanreicherung, z. B. Berechnung von PE-Ratios.

3. **Temporäre Processed-Collection → Processed-Datenbank**
   - Zusammenführung der verarbeiteten Daten via Aggregation Framework.
   - Endgültige Speicherung in der `Processed`-Datenbank.

## Architektur & Qualität

- **Dependency Injection**: Anwendung des DIP (Dependency Inversion Principle) für flexible Komponenten.
- **Logging**:
  - Zeiterfassung für Funktionen und Datenbankoperationen.
  - Ausführliche Logs für Debugging und Monitoring.
