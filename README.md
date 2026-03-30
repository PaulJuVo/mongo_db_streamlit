TODO:
Quellen nachrüsten

Mindestens ergänzen bei:

MongoDB / NoSQL Vorteile
Time Series DBs
Z-Score / Robust Statistics
Momentum Strategie

# Einleitung

## Problemstellung

Die systematische Verarbeitung, Bewertung und der Vergleich anhand von historischen Fundamentaldaten, ist für private wie auch für institutionelle Anwender mit erheblichem Aufwand verbunden. Etablierte Anbieter wie Yahoo Finance, [Finanzen.net](http://Finanzen.net) oder Bloomberg sind entweder sehr teuer oder bieten keine gesonderte zeitliche Darstellung für Price-Ratios an. Viele Anbieter zeigen oft nur Price-Earnings zu den Quartalsenden an. Da Unternehmen ihren Bilanzierungskalender und damit ihre Quartale selbst definieren, gehen zusätzlich zeitliche Informationen verloren. Durch die vielen Ratios entsteht das Problem der Informationsüberflutung und da Price-Ratios vor allem für Value-Investoren interessant sind, bietet es sich an einen kombinierten Value Score aus den Ratios zu generieren und in einem Ranking anzuzeigen und mit einem rein technischen Momentum Score Ranking zu vergleichen.

Darüber hinaus erfordert ein System dieser Art eine sorgfältige Softwarearchitektur: Die Kombination aus heterogenen Datenquellen, komplexer Kennzahlenlogik und dem Anspruch an langfristige Wartbarkeit und Erweiterbarkeit macht den Einsatz etablierter Architekturprinzipien – wie Clean Architecture, Dependency Inversion und systematischem Testing – zu einer zentralen Anforderung an die Umsetzung.

Vor diesem Hintergrund stellt sich die Frage, wie eine Anwendung konzipiert und entwickelt werden kann, die historische Fundamentaldaten des S&P500 strukturiert aufbereitet, relevante Kennzahlen berechnet und einen systematischen Vergleich von Unternehmen innerhalb einer Peer Group über einen Zeitraum von ca. 15 Jahren ermöglicht.

## Zielsetzung

Ziel dieser Arbeit ist die Konzipierung und Umsetzung einer Anwendung, die fundamental sowie historische Daten verarbeitet, in einer Datenbank speichert und diese dann in einem Dashboard zur Ansicht zur Verfügung stellt. Verschiedene Ratios sollen für ein Unternehmen über die Zeit dargestellt und vergleichbar gemacht werden. Außerdem sollen Unternehmen untereinander und mit dem Peer-Group Median verglichen werden können. Um den vollen Funktionsumfang eines Dashboards zu gewährleisten sollen auch die historischen Aktienpreise und zum Vergleich mit ihrem Index angezeigt werden. Basierend auf den Ratios wird ein Combined Score ermittelt, der in einem Ranking angezeigt und mit einem Momentum Ranking verglichen werden kann. Prototypisch wird die Anwendung nur für Unternehmen aus dem S&P500 umgesetzt. Das Projekt fokussiert sich auf historische Fundamentaldaten und beinhaltet keine Echtzeitdaten, keine Prognose -Modelle und keine automatisierte Investment-Empfehlung.

Neben der fachlichen Funktionalität legt die Arbeit einen expliziten Schwerpunkt auf die softwaretechnische Qualität der entwickelten Anwendung. Durch den Einsatz von Clean Architecture und dem Prinzip der Dependency Inversion soll eine modulare, testbare und wartbare Codebasis entstehen. Automatisierte Tests, strukturiertes Logging sowie die konsequente Trennung von Verantwortlichkeiten (Separation of Concerns) gewährleisten dabei sowohl die Korrektheit der Berechnungen als auch die langfristige Erweiterbarkeit des Systems.

## Methodik

### Methodisches Vorgehen

Die Entwicklung der Anwendung erfolgte nach einem iterativen und prototypischen Vorgehensmodell. Ziel war es, die komplexe Kombination aus Datenverarbeitung, Kennzahlenberechnung und Visualisierung schrittweise zu entwickeln und frühzeitig zu validieren.

Zu Beginn wurde ein Minimalprototyp umgesetzt, der den grundlegenden Datenfluss vom Import der Rohdaten bis zur Darstellung erster Kennzahlen abbildet. Darauf aufbauend wurde die Anwendung in mehreren Iterationen erweitert, wobei Datenpipeline, Services und Dashboard schrittweise ergänzt und durch Unit-Tests abgesichert wurden.

Das Vorgehen orientiert sich an Prinzipien agiler Softwareentwicklung, ohne ein formales Framework wie Scrum vollständig umzusetzen. Stattdessen lag der Fokus auf kurzen Entwicklungszyklen und kontinuierlicher Validierung der Ergebnisse.

### Datengrundlage

TODO Die Anwendung bezieht Daten aus… (Später)

### Architektur

Die Anwendung orientiert sich an der Clean-Architecture von Robert C. Martin und besteht aus Infrastructure, Presentation, Application und Domain Layer. Die Abhängigkeiten sind nach innen gerichtet, sodass die Services und die Datenpipeline von der Datenbank und dem User Interface entkoppelt sind. Dies stellt die Testbarkeit der Business Logik sicher und macht das System flexibel für den Austausch von Infrastruktur.

### Technologie

Als Datenbank wurde eine Mongo Instanz ausgewählt, da sie die Flexibilität einer No-SQL Datenbank mitbringt und spezielle Funktionalitäten für Zeitreihen mitbringt, die für die Lösung sehr sinnvoll sind. Als Backend Sprache wird Python verwendet, da es sehr weit verbreitet, gut dokumentiert und die Anforderungen des Anwendungsfall deckt.

# Hauptteil

## Finanzgrundlagen

### Grundlegende Begriffe

#### Income Statement (Gewinn- und Verlustrechnung)

Das Income Statement ist eine periodische Finanzaufstellung, die Umsätze, Kosten und das Nettoergebnis eines Unternehmens über einen definierten Zeitraum ausweist. Es bildet die Grundlage für ertragsbezogene Kennzahlen wie das Kurs-Gewinn-Verhältnis (P/E Ratio) und ist zentraler Bestandteil der fundamentalen Unternehmensanalyse.

#### Cash Flow Statement (Kapitalflussrechnung)

Die Kapitalflussrechnung stellt die tatsächlichen Zahlungsströme eines Unternehmens dar und gliedert sich in operativen, investiven und finanzierenden Cashflow. Im Gegensatz zum Income Statement ist sie nicht durch buchhalterische Abgrenzungen beeinflusst und ermöglicht damit eine realistischere Beurteilung der Liquidität – relevant insbesondere für den Free Cash Flow als Basis des P/FCF-Ratios.

#### Symbol / Ticker

Der Ticker ist ein eindeutiges alphanumerisches Kürzel, das ein börsennotiertes Unternehmen an einer Handelsplattform identifiziert (z.B. `AAPL` für Apple).

#### Sector

Der Sektor klassifiziert Unternehmen nach ihrer wirtschaftlichen Haupttätigkeit gemäß dem Global Industry Classification Standard (GICS), z.B. _Information Technology_, _Health Care_ oder _Financials_.

#### Trailing

Trailing bezeichnet die rückwärtsgerichtete Betrachtung einer Kennzahl auf Basis tatsächlich realisierter Vergangenheitswerte.

#### TTM – Trailing Twelve Months

TTM ist die gebräuchlichste Form der Trailing-Berechnung und aggregiert die Finanzdaten der jeweils letzten zwölf Monate – unabhängig vom Geschäftsjahresende des Unternehmens. Da Unternehmen ihren Bilanzierungskalender selbst definieren, sorgt TTM für eine zeitlich konsistente und unternehmensübergreifend vergleichbare Datenbasis.

#### Index

Ein Aktienindex aggregiert die Kursentwicklung einer definierten Gruppe von Unternehmen zu einer einzigen Kennzahl und dient als Markt- oder Sektorreferenz. Im Kontext dieser Anwendung bildet der **S&P 500** den Referenzindex, gegen den die historische Kursentwicklung einzelner Unternehmen im Dashboard verglichen wird.

#### Weighted Average Shares Outstanding

Die gewichtete durchschnittliche Anzahl ausstehender Aktien berücksichtigt Veränderungen im Aktienbestand – etwa durch Aktienrückkäufe oder Neuemissionen – anteilig über den Berichtszeitraum. Sie ist die Berechnungsgrundlage für den Earnings per Share (EPS) und beeinflusst damit direkt alle EPS-basierten Kennzahlen wie das P/E-Ratio. Im Kontext dieser Anwendung wird ausschließlich die Diluted-Variante verwendet, da sie das vollständige Verwässerungspotenzial eines Unternehmens abbildet und damit eine konservativere sowie aus Anlegerperspektive realistischere Bewertungsgrundlage darstellt.

### Finanzkennzahlen

#### Price - Adjusted Closed

Der Price bezieht sich im Projektkontext immer auf den adjusted Closed Preis eines Handelstages. Er ist die modifizierte Version des Closed Wertes, der Aktien Spaltung, Dividenden und andere Events berücksichtigt und ermöglicht dadurch eine realistischere Betrachtung.

#### Price / Earnings - PE - Ratio

Diese relative Kennzahl setzt den Tages Price und die Earnings eines Unternehmens in Verhältnis. Dabei wird der Price durch die TTM Earnings per Share (EPS) geteilt.

$\quad P/E = \frac{\text{Price per Share}}{\text{EPS diluted (TTM)}}$

#### Price / Sales - PS - Ratio

Diese relative Kennzahl setzt den Tages Price und die Revenues eines Unternehmens in Verhältnis. Dabei wird der Price durch die TTM Revenues per Share geteilt.

$\quad P/S = \frac{\text{Price per Share}}{\text{Revenue per Share (TTM)}}$

#### Price / Operating Cashflow - PC - Ratio

Diese relative Kennzahl setzt den Tages Price und die Operating Cashflows eines Unternehmens in Verhältnis. Dabei wird der Price durch die TTM Operating Cashflows per Share geteilt.

$\quad P/C = \frac{\text{Price per Share}}{\text{Operating Cashflow per Share (TTM)}}$

#### Price / Free Cashflow - PFCF - Ratio

Diese relative Kennzahl setzt den Tages Price und die Free Cashflows eines Unternehmens in Verhältnis. Dabei wird der Price durch die TTM Free Cashflows per Share geteilt.

$\quad P/FCF = \frac{\text{Price per Share}}{\text{Free Cashflow per Share (TTM)}}$

### **Value Strategy**

> "Value investing involves picking stocks that seem to be trading for less than their book value." (Investopedia 2025)

Eine Value Strategie basiert auf der Annahmen, dass der Aktienpreis sich von dem tatsächlichen Wert eines Unternehmens im positiven wie auch im negativen entkoppeln kann, jedoch über einen langen Zeitraum zu ihrem wahren Wert zurückkehrt. Um diese Strategie am Aktienmarkt umzusetzen werden mittels verschiedener Methoden die wahren Unternehmenswerte ermittelt. Eine Methode ist es über die Fundamentaldaten auf den Unternehmenswert Rückschlüsse zu führen. Die Hypothese von Value Investoren ist, dass man in unterbewertete Aktien investiert und sich diese mit der Zeit in Richtung ihres eigentlichen Wertes, und damit positiv entwickeln.

#### James O’Shaughnessy und der Value Composite

James O'Shaughnessy ist ein Amerikanischer Investor, CEO von O'Shaughnessy Ventures und Gründer von O'Shaughnessy Asset Management. In seinem Buch “What Works on Wall Street” stellt er unter anderem den Value Composite One vor. Dieser besteht aus den einem kombinierten Score aus Price-to-book Ratio, Price / Sales Ratio, EBITDA / Enterprise Value, Price / Cashflow Ratio und Price / Earnings Ratio. In seinem Buch hat er mit einem Backtest von 1963 bis 2009 gezeigt, dass man mittels der Kombination aus mehreren Metriken eine Einzelmetrik in 82% der Fällen am Aktienmarkt schlägt. Sein kombinierter Score hatte eine jährliche Rendite von 17.18%. vgl. O'Shaughnessy (2011), zitiert nach Estoppey (2024)

#### Ratio-Auswahl und Peer-Group-Vergleich

Zur Aggregation der zur Verfügung stehenden PE - Ratio, der PS - Ratio und der PFCF - Ratio wird ein Combined Value Score definiert. Die PC - Ratio wird für den Score verworfen, da der Cashflow sonst übergwichtet wäre, und der Free Cashflow einen besseren Einblick über die tatsächlich zu Verfügung stehenden liquiden Mittel gibt. Da die einzelnen Sektoren unterschiedlichen Bedingungen und damit auch unterschiedlichen Ratio Niveaus und Abweichungen unterliegen, ist es sinnvoll eine Sektor-relative Bewertung vorzunehmen. Das heißt, dass Aktien werden nur mit Aktien in ihrem Sektor verglichen.

#### Robust Z-Score

Da die Ratios im Vergleich unterschiedliche Skalen aufweisen, aber dennoch gleich gewichtet werden sollen, erfolgt eine Standardisierung mittels eines robusten Z-Scores.

Der klassische Z-Score basiert auf dem arithmetischen Mittel und der Standardabweichung, welche beide stark durch Ausreißer beeinflusst werden und somit keine robusten Schätzer darstellen (vgl. Iglewicz & Hoaglin 1993).

Als robuste Alternative werden der Median als Lageparameter sowie die Median Absolute Deviation (MAD) als Streuungsmaß verwendet. Beide weisen einen hohen Breakdown Point von etwa 50 % auf und sind damit deutlich weniger sensitiv gegenüber Ausreißern (vgl. Iglewicz & Hoaglin 1993).

Die MAD ist definiert als Median der absoluten Abweichungen vom Median (Iglewicz & Hoaglin 1993, S. 11):

$\quad \text{MAD} = \text{median}(|x_i - \tilde{x}|)$

Darauf aufbauend ergibt sich der Modified Z-Score nach Iglewicz & Hoaglin (1993) zu:

$\quad M_i = \frac{0.6745 \cdot (x_i - \tilde{x})}{\text{MAD}}$

Im Rahmen dieser Arbeit wird auf den Skalierungsfaktor verzichtet, da ausschließlich relative Vergleiche innerhalb einer Peer Group durchgeführt werden und keine Schwellenwerte zur Ausreißererkennung verwendet werden.

#### Combined Value Score

Für die Berechnung der Robust Z-Score standardisierten Ratios werden die Mediane des Sektores und der MAD des Sektores verwendet, da der Vergleich innerhalb der Peer-Group und nicht mit der Historie der Einzelaktie stattfinden soll. Als nächstes wird der Median der drei standardisierten Ratios genommen. Eine unterbewertete Aktien hat einen vergleichsweise geringen Price im Verhältnis zu ihren Earnings / Sales / Casflow. Durch die Division haben diese Aktien im Vergleich zu überbewerteten Aktien eine kleinere Price - Ratio. Da diese Aktien unterhalb des Sektor Medians sind führt das dazu, dass der berechnete Z-Score dieser Aktien eine negative Zahl ist. Je kleiner der Combined Value Score, desto unterbewerteter ist die Aktie. Dies ist für Laien nicht intuitiv und deshalb wird der Wert als letzter Schritt invertiert.

### Momentum Strategy

Ein Momentum Indikator ist ein technischer Indikator, der dazu verwendet werden kann kurzfristige Börsentrends zu identifizieren. vgl. (Sue Man Fan 2010, S. 87) Investoren, die der Momentum Strategie folgen, gehen davon aus, dass Aktien, die gut laufen, auch weiterhin gut laufen werden. "[...] strategies which buy stocks that have performed well in the past and sell stocks that have performed poorly in the past generate significant positive returns over 3-to 12-month holding periods." (JEGADEESH & TITMAN 1993, Abstract).

#### Momentum Score

Der Momentum Score basiert rein auf technischen Daten und wird im Projektkontext aus der Rendite der letzten 6 Monate gebildet. Der Betrachtungszeitraum wird auf 6 Monate definiert, da JEGADEESH & TITMAN 3 - 12 Monatszeiträume getestet haben und 6 Monate in dem genannten Zeitraum liegen. Je besser die Performance der letzten 6 Monate, desto höher der Score. Der Momentum Score dient in dieser Arbeit als Vergleichsstrategie und wird darum nicht näher untersucht.

$\quad \text{Price Index}_{6M} = \frac{Price_{end}}{Price_{start}} - 1$

TODO RENDERT NICHT

## Technologie

### Clean Architecture

![Abb. 1: Die saubere Architektur (Martin 2018, S. 193)](attachments/image.png)

Abb. 1: Die saubere Architektur (Martin 2018, S. 193)

Die Clean Architektur folgt einer Regel: “Quellcode-Abhängigkeiten dürfen nur nach innen in Richtung der übergeordneten Richtlinien weisen.” (Martin 2018, S. 194)

Diese Architektur stellt folgende Eigenschaften sicher:

- **Framework-Unabhängigkeit**:
  Die Kernlogik der Anwendung ist nicht an ein bestimmtes Framework gebunden. Frameworks und Libraries werden als austauschbare Werkzeuge eingesetzt, ohne dass sie die Struktur des Systems diktieren.

- **Testbarkeit**:
  Die Geschäftslogik – also Kennzahlenberechnung und Score-Ermittlung – kann isoliert getestet werden, ohne dass eine Datenbankverbindung, ein laufendes UI oder externe Dienste notwendig sind.

- **UI-Unabhängigkeit**:
  Die Präsentationsschicht ist vollständig von der Businesslogik entkoppelt. Das bestehende Streamlit-Dashboard könnte beispielsweise durch ein anderes Frontend ersetzt werden, ohne dass eine einzige Zeile der Score-Berechnung angepasst werden müsste.

- **Datenbank-Unabhängigkeit**:
  Die Geschäftsregeln haben keine direkte Kenntnis der verwendeten Datenbank. MongoDB könnte theoretisch gegen eine relationale Datenbank oder einen anderen Datenspeicher ausgetauscht werden, da die Kommunikation ausschließlich über Abstraktionen erfolgt.

- **Unabhängigkeit von externen Komponenten**:
  Die Domain- und Applikationsschicht hat keinerlei direkte Abhängigkeit zu externen Datenquellen oder Schnittstellen. Ob Daten über eine Finanz-API, eine CSV-Datei oder einen anderen Kanal bezogen werden, ist für die Kernlogik irrelevant.

#### Dependency inversion Principle

“_HIGH LEVEL MODULES SHOULD NOT DEPEND UPON LOW
LEVEL MODULES. BOTH SHOULD DEPEND UPON ABSTRACTIONS.
ABSTRACTIONS SHOULD NOT DEPEND UPON DETAILS. DETAILS
SHOULD DEPEND UPON ABSTRACTIONS_.” (Martin 1996, S. 6)

Um die Clean Architektur umzusetzen wird das Dependency Inversion Principle (DIP) verwendet. Es ist eines der SOLID - Prinzipien und stellt sicher, dass die Businesslogik nicht von der Infrastruktur abhängig ist. Im konkreten Fall wird das DIP für den Datenbankzugriff verwendet. Der Zugriff auf die Mongo Datenbank erfolgt über ein Repository. Im Application Layer wurde eine abstrakte Klasse Namens BaseRepositoryInterface definiert, welches im Infrastructure Layer implementiert wurde. Die Instanziierung der konkreten Repositories erfolgt im Entry Point der Anwendung (Streamlit) und wird per Dependency Injection in die Services des Application Layers injiziert. Somit sind die Abhängigkeiten alle nach innen gerichtet.

#### Dependency Injection

Dependency Injection ist ein Design Pattern, das die praktische Umsetzung des DIP ermöglicht. Anstatt dass eine Klasse ihre Abhängigkeiten selbst instanziiert, werden diese von außen übergeben. Dadurch bleibt die Klasse unabhängig von konkreten Implementierungen und kennt ausschließlich die Abstraktion.

#### Repository

Das Repository Pattern entstammt dem Domain-Driven Design (DDD) und abstrahiert den Datenzugriff vollständig von der Businesslogik. Die Services arbeiten ausschließlich gegen ein definiertes Interface und haben keine Kenntnis darüber, ob die Daten aus MongoDB, einer relationalen Datenbank oder einer anderen Quelle stammen. Im Kontext dieser Anwendung übernimmt das Repository dabei implizit auch die Rolle eines Adapters, da es die MongoDB-spezifische Abfragesyntax in die interne Domänensprache übersetzt.

#### Decorator Pattern

Das Decorator Pattern ist ein strukturelles Entwurfsmuster, das einer bestehenden Klasse zur Laufzeit zusätzliches Verhalten hinzufügt, ohne ihre Schnittstelle zu verändern. Der Decorator implementiert dasselbe Interface wie die dekorierte Klasse und umhüllt sie – er delegiert den eigentlichen Aufruf weiter und ergänzt ihn um zusätzliche Logik. In dieser Anwendung wird das Decorator Pattern für das **Logging** eingesetzt: Der “performance_log” umhüllt die eigentliche Funktion und protokoliert die Dauer des Funktionslaufs, ohne dass die Funktion verändert werden muss.

### Systemarchitektur

![Abb. 2: Systemarchitektur. Quelle: Eigene Darstellung](attachments/systemarchitecture.png)

Abb. 2: Systemarchitektur. Quelle: Eigene Darstellung

Die Anwendung ist nach der traditionellen horizontalen Schichtenarchitektur aufgebaut und besteht im Kern (Core) aus dem Application Layer, der die Services, und dem Domain Layer, der die Business Logik, bzw die Berechnungsvorschriften enthält. Das Infrastructure Layer kapselt die Mongo Verbindung und beinhaltet die Repository - Logik. Die Presentation layer wird durch Streamlit bereitgestellt, und injiziert die Dependencies in die Services. Die Anwendung wird mittels Docker-Compose containerisiert, um das Deployment auf einem anderen Server zu vereinfachen.

```
anwendung
├── app
│   ├── pages
│   ├── shared
│   └── streamlit_app.py # Entry Point
├── core
│   ├── application
│   │   ├── dashboard_service.py
│   │   ├── notification_service.py
│   │   ├── pipeline_service.py
│   │   ├── ranking_service.py
│   │   └── run_import.py
│   ├── domain
│   │   ├── calculation.py
│   │   ├── transform.py
│   │   └── validation.py
│   ├── exceptions
│   └── interfaces
│       └── base_repository_interface.py
├── infrastructure
│   └── mongo
│       ├── mongo_connection.py
│       └── mongo_repository.py
├── Dockerfile
├── docker-compose.yml
├── config
├── logs
├── scripts
└── tests
```

### Datenhaltung mit MongoDB

MongoDB ist ein dokumentorientiertes NoSQL-Datenbankmanagementsystem und verwaltet Collections in JSON-ähnlichen Dokumenten. Dadurch dass die Rohdaten in JSON Dateien vorliegen ist der die Entscheidung für eine dokumentorientierte Datenbank naheliegend. MongoDB stellt spezialisierte Time-Series-Collections bereit, die für zeitreihenbasierte Abfragen optimiert sind. Durch die spezielle Persistierung ist die Time Series Collection performanter in Abfragen und ermöglicht so eine schnelle Bereitstellung von vielen Datenpunkten. vgl. (MongoDB, Inc. 2026) Außerdem bietet MongoDB ein Aggregation Framework welches eine Verarbeitung auf Datenbankebene ermöglicht und in gewissen Fällen deutlich effizienter ist als die Verarbeitung mit Python. Dieses Framework bietet sich vor allem für Verarbeitungsschritte an, die keine Business Logik beinhalten, sondern Daten nur transformiert oder verschiebt. Business Logik soll testbar sein und das ist innerhalb des Aggregation Frameworks schwer.

Docker aktiviert beim ersten Start der Mongo Instanz die Authentifizierung automatisch ein. Per Default ist die Authentifizierung deaktiviert und wird aus Sicherheitsgründen in der Anwendung aktiviert. vgl. (MongoDB, Inc. 2026) Außerdem gibt es ein Entrypoint-Skript, welches zwei Datenbank User und zwei Datenbanken einrichtet. Es gibt eine Datenbank “raw” für Rohdaten und Zwischenschritte und eine Datenbank “processed” für die finalen Daten. Der erste User hat Lese und Schreibe Rechte auf beiden Datenbanken und wird genutzt um die Daten zu verarbeiten. Der zweite User hat nur Leserechte auf der “processed” Datenbank. Dies bildet eine weitere Sicherheit vor einem ungewollten Schreib-Zugriff und ist im Sinne des Separation of Concerns.

### Backend

Das Application und das Domain Layer sind in Python geschrieben, da Python eine weitverbreitete und im Finanz und Datenbereich beliebte Sprache ist.
Python bietet mit pymongo, pytest und jsonschema direkt relevante Bibliotheken für den Anwendungsfall.
Dabei ist pymongo für den Datenbankzugriff, pytest für das Testing und jsonschema für die Schema-Validierung besonders nützlich.

### Testing

Die Anwendung wird durch automatisierte Unit Tests mit pytest abgesichert. Die Tests konzentrieren sich auf den Domain Layer und den Application Layer, da dort die gesamte Business Logik der Anwendung liegt.

#### Teststrategie

Es werden zwei Testebenen unterschieden. Auf der ersten Ebene werden die reinen Berechnungs- und Validierungsfunktionen des Domain Layers isoliert getestet. Da diese Funktionen keine externen Abhängigkeiten besitzen, können sie direkt mit Eingabewerten aufgerufen und deren Rückgabewerte geprüft werden. Auf der zweiten Ebene wird der PipelineService des Application Layers getestet. Hier werden die Repository-Abhängigkeiten mittels unittest.mock durch Mock-Objekte ersetzt, die vordefinierte Testdaten zurückgeben. Dies ermöglicht es, das Verhalten des Services isoliert zu testen, ohne eine Datenbankverbindung zu benötigen – ein direkter praktischer Nachweis der gewählten Clean Architecture und des Dependency Inversion Principle.

#### Abdeckung

Die Tests folgen einer mehrschichtigen Abdeckungsstrategie:

- **Happy Path**: Jede Funktion wird zunächst mit validen Eingaben auf korrekte Ergebnisse geprüft, etwa die Berechnung der PE-Ratio aus realistischen AAPL-Finanzdaten.

- **Edge Cases und Grenzwerte**: Kritische Randfälle werden explizit abgedeckt, darunter eine MAD von 0 bei der Robust-Z-Score-Berechnung, ein Startpreis von 0 beim CAGR oder weniger als vier verfügbare Quartale bei der TTM-Berechnung.

- **None-Propagation**: Da nicht für jeden Handelstag alle Finanzkennzahlen berechnet werden können, wird konsequent getestet, ob None-Werte in Eingabedaten korrekt erkannt und weiterpropagiert werden, statt zu Folgefehlern zu führen. Hierfür existieren dedizierte Fixtures mit teils fehlenden Werten.

- **Validierungslogik**: Die Funktion contains_right_income_statements prüft, ob die vier zugehörigen Quartalsberichte für ein gegebenes Datum korrekt und konsistent vorliegen. Getestet werden dabei Duplikate innerhalb der Perioden, None-Werte in Perioden oder Kalenderjahren, zeitlich inkonsistente Statements mit zu großem Jahresabstand sowie ein Bewertungsdatum, das jünger als der neueste vorliegende Bericht ist.

- **Verhaltensverifikation**: Bei den Service-Tests wird nicht nur geprüft, ob Repository-Methoden aufgerufen wurden, sondern welche Daten dabei übergeben wurden. Über insert_many.call_args wird sichergestellt, dass Symbol, Datum und alle berechneten Ratios im persistierten Dokument korrekt enthalten sind.

#### Testdaten

Die Testdaten sind in einer zentralen conftest.py als wiederverwendbare Fixtures organisiert. Die Finanzdaten orientieren sich an realistischen AAPL-Dimensionen, um praxisnahe Berechnungen verifizieren zu können. Für Grenzfall-Tests existieren dedizierte Fixtures, etwa sample_financedata_only_none oder sample_income_period_w_duplicates, die gezielt fehlerhafte oder unvollständige Datensituationen abbilden.

### Logging

Das Logging ist in zwei separate Logger aufgeteilt. Der Applikations-Logger protokolliert relevante Vorkommnisse während der Datenpipeline – etwa JSON-Dateien, die nicht importiert werden konnten, leer waren oder die Schema-Validierung nicht bestanden haben. Der MongoDB-Logger erfasst datenbankspezifische Ereignisse wie Verbindungsfehler oder fehlgeschlagene Schreiboperationen. Beide Logger verwenden strukturierte Log-Level (INFO, WARNING, ERROR) und schreiben in dedizierte Log-Dateien, um eine gezielte Fehleranalyse zu ermöglichen. Zusätzlich existiert ein Performance-Logger, der als Decorator an beliebige Funktionen angehängt werden kann und deren Ausführungszeit dokumentiert. Dies ermöglicht eine gezielte nachträgliche Optimierung rechenintensiver Schritte.

### Frontend

Die Präsentationsschicht der Anwendung wird mit Streamlit umgesetzt. Streamlit ist ein open-source Python Framework, das die Erstellung von interaktiven Web-Applikationen und Dashboards direkt aus Python-Code ermöglicht, ohne dass separate Frontend-Kenntnisse in HTML, CSS oder JavaScript erforderlich sind. Da die gesamte Anwendung in Python geschrieben ist, fügt sich Streamlit nahtlos in den bestehenden Technologie-Stack ein.

Streamlit organisiert die Anwendung in einzelne Pages, die jeweils eine dedizierte Ansicht des Dashboards repräsentieren. Jede Page instanziiert die benötigten Repository-Implementierungen und injiziert diese in die zuständigen Services – sie übernimmt damit die Rolle des Entry Points und der Composition Root für den jeweiligen Anwendungsfall. Die Pages enthalten dabei selbst keine Geschäftslogik, sondern delegieren ausschließlich an die Services und stellen deren Ergebnisse dar. Dies entspricht der konsequenten Trennung von Präsentation und Businesslogik im Sinne der Clean Architecture.

Da Streamlit eine zustandslose Ausführung pro User-Interaktion hat, wird der st.session_state verwendet, um Nutzereingaben und Zwischenergebnisse innerhalb einer Session zu persistieren und unnötige Datenbankabfragen zu vermeiden.

### Docker

Die Anwendung wird mittels Docker containerisiert und über Docker Compose als Multi-Container-Anwendung betrieben. Docker stellt sicher, dass die Anwendung umgebungsunabhängig und reproduzierbar ausgeführt werden kann, da alle Abhängigkeiten im Container gekapselt sind.
Das Dockerfile basiert auf dem schlanken python:3.11-slim Image, um die Container-Größe minimal zu halten. Die Abhängigkeiten werden über requirements.txt installiert und die Streamlit-Applikation wird auf Port 8501 exponiert.
Die docker-compose.yml definiert zwei Services. Der mongodb Service verwendet das offizielle MongoDB Community Server Image und persistiert die Datenbankdaten in einem externen Docker Volume, sodass die Daten einen Neustart des Containers überleben. Über das docker-entrypoint-initdb.d Verzeichnis wird beim ersten Start ein Initialisierungsskript ausgeführt, das die Datenbankbenutzer und Datenbanken einrichtet. Der streamlit Service wird aus dem lokalen Dockerfile gebaut und ist über depends_on mit dem MongoDB Service verknüpft, sodass die Applikation erst startet, wenn die Datenbank verfügbar ist. Umgebungsvariablen wie Datenbankverbindung und Credentials werden über eine .env.dev Datei injiziert und sind damit nicht im Quellcode hinterlegt.
Log-Dateien und Datendateien werden über Volumes in das Host-Dateisystem gemountet, was eine persistente Fehleranalyse außerhalb des Containers ermöglicht. Das MongoDB Volume ist als external: true konfiguriert, wodurch es unabhängig vom Container-Lifecycle existiert und ein unbeabsichtigtes Löschen der Datenbankdaten beim Neustart verhindert wird.

### Performance

Um geringe Antwortzeiten zu gewährleisten sind alle Ratios in der Finanzzeitreihe persistiert und diese ist als Timeseries Collection in Mongo konfiguriert. Timeseries Collection sind für Zeitreihen optimiert und ermöglichen dadurch geringe Ladezeiten für Abfragen. Die Zeitreihe wurde außerdem auf dem Ticker-Symbol und dem Datum indexiert, sodass Abfragen noch schneller bearbeitet werden.

![Abb. Memory Usage](attachments/memory_usage.png)
Die Erstellung der FinanceData Collection efolgt über Batch Inserts, bei denen Dokumente in definierten Blöcken geschrieben werden. Dies beschleunigt die Verarbeitung großer Datenmengen und begrenzt gleichzeitig den Arbeitsspeicherbedarf, da nie alle Dokumente gleichzeitig im RAM gehalten werden müssen. Die Anwendung kommt dadurch mit 2 GB RAM aus.
Besonders hervorzuheben ist, dass, sofern kein Business-Logik-Anteil vorliegt, das Mongo Aggregation Framework genutzt wird, welches die Datenverarbeitung auf Datenbankebene ermöglicht und damit den Datentransfer zwischen Datenbank und Anwendung minimiert.

Die Laufzeiten der einzelnen Pipeline-Schritte wurden über den Performance-Logger erfasst und sind in der Tabelle dokumentiert. Die Gesamtpipeline verarbeitet die Rohdaten von ca. 370 MB – bestehend aus rund 1.100 EOD-Preisdokumenten sowie 102.000 Income- und 110.000 Cashflow-Quartalsdaten – in einer Gesamtlaufzeit von ca. 5,5 Minuten. Da die Pipeline nur einmalig zur Datenbeschaffung ausgeführt wird und das Dashboard ausschließlich auf vorberechneten Daten operiert, ist diese Laufzeit für den produktiven Betrieb nicht relevant.
| Pipeline-Schritt | gemessene Laufzeit |
|---|---|
| scdConstituents | 0,10 s |
| Company Data | 0,06 s |
| S&P500 Zeitreihe | 0,11 s |
| eod_staged | 144,85 s |
| income_staged | 5,37 s |
| cashflow_staged | 5,47 s |
| FinanceData | 98,80 s |
| SectorData | 78,60 s |
| **Gesamt** | **~333 s** |
Der zeitintensivste Schritt ist die Erstellung von eod_staged mit 145 Sekunden, da das Aggregation Framework hier die verschachtelten Preishistorien aller S&P500-Unternehmen entschachtelt und als Einzeldokumente in die Staged Collection überführt. Für die Erstellung der FinanceData wird anschließend in Python über alle Handelstage iteriert und für jeden Datenpunkt die TTM-Kennzahlen aus den jeweils vier vorangegangenen Quartalsberichten berechnet. Dies dauert 99 Sekunden.

| Query              | gemessene Zeiten |
| ------------------ | ---------------- |
| `get_finance_data` | 3–74 ms          |
| `get_sector_data`  | 2–8 ms           |
| `get_sp500_data`   | 2–12 ms          |
| `get_ranking`      | 414–978 ms       |

Neben den Pipeline-Laufzeiten wurden auch die Antwortzeiten des Dashboards über den
Performance-Logger gemessen. Einfache Datenbankabfragen wie `get_finance_data`,
`get_sector_data` und `get_sp500_data` liefern Ergebnisse konsistent im einstelligen
bis zweistelligen Millisekundenbereich, was auf die Wirksamkeit des zusammengesetzten
Index auf Symbol und Datum zurückzuführen ist. Der rechenintensivste Dashboard-Aufruf
ist `get_ranking` mit 414–978 ms, da das Ranking nicht persistiert ist und bei jedem
Aufruf für alle Unternehmen eines Sektors neu berechnet wird.

## Data

### Data Source

TODO

### Schema Validation

Bevor die Rohdaten in die “raw” Datenbank importiert werden, wird zuerst mit der python Bibliothek jsonschema das Schema der Rohdaten geprüft. Damit wird sichergestellt, dass bestimmte essenzielle Daten vorhanden sind und das die folgenden Verarbeitungsschritte ausgeführt werden können. Ein ValidationError führt dazu, dass der Datensatz geloggt wird und in eine <collection>\_rejected Tabelle eingefügt wird. Somit kann man nochmal nachvollziehen, warum und wie der Datensatz aussieht der nicht importiert wurde.

### Zielschema

![Abb. 2: Zielschema. Quelle: Eigene Darstellung](attachments/processed_schema.png)

Abb. 3: Zielschema. Quelle: Eigene Darstellung

Das Schema für **Company Data** kann folglich wie eine Dimension gesehen werden, die lediglich Kontextdaten beinhaltet, die für Aggregationen oder die Anzeige im Dashboard relevant sind.

Die **Constituents** Collection ist eine Slowly Changing Dimension und wird im Gegensatz zu den anderen Company-Bezogenen Collections nicht über den Ticker/ das Symbol referenziert, sondern über den Company Namen, da der Ticker / das Symbol im Index neu vergeben werden kann.

Die **Finance Data** - Collection ist eine Time Series Collection mit dem "timeField" : "date" und dem "metaField": "symbol". Somit werden Mongo-internen Buckets auf dem Date und dem Symbol erstellt. Die "granularity" ist auf "hours" konfiguriert, da die Datenpunkte aus tägliche Börsenwerte bestehen und "hours" die gröbste Granularität in Mongo ist. Somit werden Daten bis zu einem Monat gruppiert in die Buckets eingefügt. Die Ratio-Felder sind als nullable definiert, da nicht für jeden Datenpunkt alle Kennzahlen berechnet werden können – etwa bei einer negativen Price / Earnings Ratio.

**Sector Data** ist ebenfalls eine Time Series Collection und hat die gleiche Konfiguration wie die Finance Data Collection. Hier ist das "metafield" allerdings "sector" und damit sind die Buckets auch auf Sektor und date erstellt.

Das Schema für **SP500 Data** ist bis auf die fehlenden Ratios das gleiche wie die Finance Data Collection. Es handelt sich ebenfalls um eine Time Series.

Für alle Time Series Collections gilt, dass Dokumente kein eindeutiges \_id-Feld brauchen. MongoDB erstellt keinen Index auf \_id und deshalb spielt \_id für Performance oder Queries meist keine Rolle. Das \_id-Feld könnte also aus der Finance Data Collection auch entfernt werden. Da die \_id für Abfragen und Performance in Time Series Collections keine Rolle spielt, wurde auf eine explizite Entfernung verzichtet.

### Datenfluss

#### FinanceData

![Abb. 2: Datenfluss Finanzdaten Zeitreihe. Quelle: Eigene Darstellung](attachments/datenfluss_ts.jpg)

Abb. 4: Datenfluss Finanzdaten Zeitreihe. Quelle: Eigene Darstellung

Nach dem Import in die "raw" Datenbank werden die Daten mit dem Mongo Aggregation Framework vorverarbeitet. Dabei werden für den Kontext unwichtige Informationen aus den Collections gefiltert und gegebenenfalls Typumwandlungen gemacht. Verschachtelte Objekte werden abgeflacht, sodass die Daten näher an das Zielschema kommen.
Die Finanzdaten Zeitreihe wird dann in Python erstellt. Dazu wird die eodPrice Collection durchlaufen, um für jedes Datum die Ratios berechnet. Die letzten vier Incomestatements und die letzten vier Cashflowstatements werden nach einer Validierung genutzt, um die TTM Average Outstanding Shares, die TTM Earnings per Share, den TTM Revenue per Share und die TTM Cashflows zu berechnen. Dies dient als Grundlage für die Berechnung der Price - Ratios. Falls die Berechnung fehlschlägt oder die Statements nicht Korrekt sind, bzw. nicht die erwarteten letzten vier sind, wird die betroffene Ratio auf NONE gesetzt.

![Abb. 2: Systemarchitektur. Quelle: Eigene Darstellung](attachments/Datenfluss.jpg)

Abb. 4: Datenflussdiagramm. Quelle: Eigene Darstellung

#### Constituents - scdConstituents

Aus der 0_sp_500_constituents_historical_2026.json wird eine Slowly Changing Dimension Type 2 erstellt, um nachvollziehen zu können, wann ein Unternehmen in den Index aufgenommen oder aus dem Index herausgenommen wurde. Diese Collection bleibt bisher ungenutzt, ist aber schon angelegt, da für eine Evaluierung von einer Value Strategie diese Informationen wichtig sind, um einen möglichen Survivorship Bias auszuschließen.

#### S&P500 Data

Für einen Vergleich mit dem Index werden aus den Files SPXEW_autoadjusted.json und ^GSPC_eod_prices.json Zeitreihen für den S&P 500 Index und für den S&P 500 Equal Weights Index extrahiert. Die Extrahierung geschieht durch das Mongo Aggregation Framework.

#### Company Data

Aus der Profil Collection wird durch das Mongo Aggregation Framework die Company Data Collection erstellt. Dabei werden nur ausgewählte Properties übernommen.

#### Sector Data

Diese Collection ist das Ergebnis der Aggregation aus der Financedata Zeitreihe durch das Mongo Aggregation Framework. Nach einem Join mit der CompanyData Collection wird nach Sektoren und Datum gruppiert und der Median der Ratios wird berechnet.

## Dashboard

Das Dashboard gliedert sich in fünf Pages, die den Funktionsumfang der Anwendung strukturiert abbilden.

### Sector Page

Die **Sector Page** dient als Einstiegspunkt des Dashboards. Sie bietet eine sektorweite Übersicht, in der der Nutzer einen Sektor auswählen, verschiedene Ratios selektieren und die enthaltenen Unternehmen visuell miteinander vergleichen kann. Eine eingezeichnete Medianlinie ermöglicht dabei eine schnelle Einordnung einzelner Unternehmen relativ zur Peer Group.

![sector Page](attachments/sector_comparison.png)

### Company Page

Die **Company Page** ermöglicht die gezielte Analyse einzelner Unternehmen über eine Suchfunktion. Nach Auswahl eines Unternehmens werden Stammdaten, historische Aktienkurse sowie die zeitliche Entwicklung der verfügbaren Ratios dargestellt. Der historische Kursverlauf kann dabei dem S&P 500 gegenübergestellt werden. Zusätzlich werden die Renditen der letzten 1, 3, 5 und 10 Jahre ausgewiesen.

![sector Page](attachments/companydata.png)
![Price Ratios vs Sector](attachments/ratio_delta.png)
![Comparison w SP500](attachments/comparison_with_sp500.png)

### Top-10 Ranking Page Page

Die **Top-10 Ranking Page** zeigt die zehn bestplatzierten Unternehmen eines ausgewählten Sektors zu einem definierten Datum. Das Ranking kann wahlweise nach dem Combined Value Score oder dem Momentum Score dargestellt werden, was einen direkten Vergleich beider Strategien ermöglicht.

![Top 10 Value Ranking](attachments/top10_value.png)

### Full Ranking Page

Die **Full Ranking Page** stellt das vollständige sektorweite Ranking dar. Der Nutzer kann entweder den gesamten Sektor einsehen oder gezielt nach einzelnen Unternehmen suchen und deren Rankingposition nachvollziehen.

![Ranking Search](attachments/search_ranking.png)

### Pipeline Page

Die **Pipeline Page** dient als administrative Steuerungsseite der Anwendung. Über sie kann der Datenimport gestartet und die Verarbeitungspipeline ausgelöst werden. Sie bildet damit den operativen Einstiegspunkt für die Datenbeschaffung und -verarbeitung.

![](attachments/pipeline.png)

# Schluss

TODO

# Literaturverzeichnis

Martin, Robert C..

_Clean Architecture : Das Praxis-Handbuch für professionelles SoftwaredesignRegeln und Paradigmen für effiziente Softwarestrukturierung_, mitp, 2018. _ProQuest Ebook Central_, http://ebookcentral.proquest.com/lib/koln/detail.action?docID=5311206. Created from koln on 2026-03-25 10:59:00.

Martin, Robert C.:

_The Dependency Inversion Principle_. Mai 1996 ([PDF](https://web.archive.org/web/20110714224327/http://www.objectmentor.com/resources/articles/dip.pdf) ([Memento](https://de.wikipedia.org/wiki/Webarchivierung#Begrifflichkeiten) vom 14. Juli 2011 im [_Internet Archive_](https://de.wikipedia.org/wiki/Internet_Archive))).

Investopedia. Value Investing Definition, How It Works, Strategies, and Risks. Juli 2025 https://www.investopedia.com/terms/v/valueinvesting.asp

Estoppey Value Investments. (2024). What is a Value Composite?
Abgerufen am 26.03.26 von
https://valueinvestments.ch/en/lexicon/value-composite/

O'Shaughnessy, J. P. (2011). What Works on Wall Street:
The Classic Guide to the Best-Performing Investment
Strategies of All Time (4. Aufl.). McGraw-Hill.

Sue Man Fan, Multiple Tests für die Evaluation von Prognosemodellen, 2010, S. 87, [Google Books](https://www.google.de/books/edition/Multiple_Tests_f%C3%BCr_die_Evaluation_von_P/q7dFUZp9h5kC?hl=de&gbpv=1&dq=momentum+zeitreihe&pg=PA87&printsec=frontcover)

JEGADEESH & TITMAN, Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency, 1993 https://doi.org/10.1111/j.1540-6261.1993.tb04702.x

Jegadeesh, N. and Titman, S. (1993) ‘Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency’, Journal of Finance (Wiley-Blackwell), 48(1), pp. 65–91. doi:10.1111/j.1540-6261.1993.tb04702.x.
https://research.ebsco.com/c/u5zo7q/viewer/pdf/ueaq7mfh2b

Härtung, J.; Elpelt, B.; Klösener, K.-H. (2004):
Lehr- und Handbuch der angewandten Statistik. 9. Auflage, Oldenbourg Verlag, München, S. 42.

Iglewicz, B.; Hoaglin, D. C. (1993): How to detect and handle outliers. Milwaukee: ASQC Quality Press.

MongoDB, Inc., 2026. MongoDB Developer Documentation. [online] Available at: https://www.mongodb.com/docs/development/
[Accessed 30 March 2026].
