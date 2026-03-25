# Einleitung

## Problemstellung

Die systematische Verarbeitung, Bewertung und der Vergleich anhand von historischen Fundamentaldaten, ist für private wie auch für institutionelle Anwender mit erheblichem Aufwand verbunden. Etablierte Anbieter wie Yahoo Finance, [Finanzen.net](http://Finanzen.net) oder Bloomberg sind entweder sehr teuer oder bieten keine gesonderte zeitliche Darstellung für Price-Ratios an. Viele Anbieter zeigen oft nur Price-Earnings zu den Quartalsenden an. Da Unternehmen ihren Bilanzierungskalender und damit ihre Quartale selbst definieren, gehen zusätzlich zeitliche Informationen verloren. Durch die vielen Ratios entsteht das Problem der Informationsüberflutung und da Price-Ratios vor allem für Value-Investoren interessant sind, bietet es sich an einen kombinierten Value Score aus den Ratios zu generieren und in einem Ranking anzuzeigen und mit einem rein technischen Momentum Score Ranking zu vergleichen.

Darüber hinaus erfordert ein System dieser Art eine sorgfältige Softwarearchitektur: Die Kombination aus heterogenen Datenquellen, komplexer Kennzahlenlogik und dem Anspruch an langfristige Wartbarkeit und Erweiterbarkeit macht den Einsatz etablierter Architekturprinzipien – wie Clean Architecture, Dependency Inversion und systematischem Testing – zu einer zentralen Anforderung an die Umsetzung.

Vor diesem Hintergrund stellt sich die Frage, wie eine Anwendung konzipiert und entwickelt werden kann, die historische Fundamentaldaten des S&P500 strukturiert aufbereitet, relevante Kennzahlen berechnet und einen systematischen Vergleich von Unternehmen innerhalb einer Peer Group über einen Zeitraum von ca. 15 Jahren ermöglicht.

## Zielsetzung

Ziel dieser Arbeit ist die Konzipierung und Umsetzung einer Anwendung, die fundamental sowie historische Daten verarbeitet, in einer Datenbank speichert und diese dann in einem Dashboard zur Ansicht zur Verfügung stellt. Verschiedene Ratios sollen für ein Unternehmen über die Zeit dargestellt und vergleichbar gemacht werden. Außerdem sollen Unternehmen untereinander und mit dem Peer-Group Median verglichen werden können. Um den vollen Funktionsumfang eines Dashboards zu gewährleisten sollen auch die historischen Aktienpreise und zum Vergleich mit ihrem Index angezeigt werden. Basierend auf den Ratios wird ein Combined Score ermittelt, der in einem Ranking angezeigt und mit einem Momentum Ranking verglichen werden kann. Prototypisch wird die Anwendung nur für Unternehmen aus dem S&P500 umgesetzt. Das Projekt fokussiert sich auf historische Fundamentaldaten und beinhaltet keine Echtzeitdaten, keine Prognose -Modelle und keine automatisierte Investment-Empfehlung.

Neben der fachlichen Funktionalität legt die Arbeit einen expliziten Schwerpunkt auf die softwaretechnische Qualität der entwickelten Anwendung. Durch den Einsatz von Clean Architecture und dem Prinzip der Dependency Inversion soll eine modulare, testbare und wartbare Codebasis entstehen. Automatisierte Tests, strukturiertes Logging sowie die konsequente Trennung von Verantwortlichkeiten (Separation of Concerns) gewährleisten dabei sowohl die Korrektheit der Berechnungen als auch die langfristige Erweiterbarkeit des Systems.

## Methodik

### Datengrundlage

Die Anwendung bezieht Daten aus… (Später)

### Architektur

Die Anwendung orientiert sich an der Clean-Architecture von Robert C. Martin und besteht aus Infrastructure, Presentation, Application und Domain Layer. Die Abhängigkeiten sind nach innen gerichtet, sodass die Services und die Datenpipeline von der Datenbank und dem User Interface entkoppelt sind. Dies stellt die Testbarkeit der Business Logik sicher und macht das System flexibel für den Austausch von Infrastruktur.

### Technologie

Als Datenbank hat man eine Mongo Instanz ausgewählt, da sie die Flexibilität einer No-SQL Datenbank mitbringt und spezielle Funktionalitäten für Zeitreihen mitbringt, die für unsere Lösung sehr sinnvoll sind. Als Backend Sprache wird Python verwendet, da es sehr weit verbreitet, gut dokumentiert und die Anforderungen des Anwendungsfall deckt.

# Hauptteil

## Finanzgrundlagen

### Grundlegende Begriffe

**Income Statement (Gewinn- und Verlustrechnung)**

Das Income Statement ist eine periodische Finanzaufstellung, die Umsätze, Kosten und das Nettoergebnis eines Unternehmens über einen definierten Zeitraum ausweist. Es bildet die Grundlage für ertragsbezogene Kennzahlen wie das Kurs-Gewinn-Verhältnis (P/E Ratio) und ist zentraler Bestandteil der fundamentalen Unternehmensanalyse.

**Cash Flow Statement (Kapitalflussrechnung)**

Die Kapitalflussrechnung stellt die tatsächlichen Zahlungsströme eines Unternehmens dar und gliedert sich in operativen, investiven und finanzierenden Cashflow. Im Gegensatz zum Income Statement ist sie nicht durch buchhalterische Abgrenzungen beeinflusst und ermöglicht damit eine realistischere Beurteilung der Liquidität – relevant insbesondere für den Free Cash Flow als Basis des P/FCF-Ratios.

**Symbol / Ticker**

Der Ticker ist ein eindeutiges alphanumerisches Kürzel, das ein börsennotiertes Unternehmen an einer Handelsplattform identifiziert (z.B. `AAPL` für Apple).

**Sector**

Der Sektor klassifiziert Unternehmen nach ihrer wirtschaftlichen Haupttätigkeit gemäß dem Global Industry Classification Standard (GICS), z.B. _Information Technology_, _Health Care_ oder _Financials_.

**Trailing**

Trailing bezeichnet die rückwärtsgerichtete Betrachtung einer Kennzahl auf Basis tatsächlich realisierter Vergangenheitswerte.

**TTM – Trailing Twelve Months**

TTM ist die gebräuchlichste Form der Trailing-Berechnung und aggregiert die Finanzdaten der jeweils letzten zwölf Monate – unabhängig vom Geschäftsjahresende des Unternehmens. Da Unternehmen ihren Bilanzierungskalender selbst definieren, sorgt TTM für eine zeitlich konsistente und unternehmensübergreifend vergleichbare Datenbasis.

**Forward**

Forward-Kennzahlen basieren auf gebräuchlicherweise auf Analystenschätzungen für zukünftige Perioden, z.B. den erwarteten Gewinn der kommenden zwölf Monate. Der Begriff wird zur Abgrenzung gegenüber Trailing-Metriken und bezieht sich in diesem Projektkontext auf tatsächliche Finanzdaten in der vorwärtsgerichteten Betrachtung (kein Forecast!). MEHR

**Index**

Ein Aktienindex aggregiert die Kursentwicklung einer definierten Gruppe von Unternehmen zu einer einzigen Kennzahl und dient als Markt- oder Sektorreferenz. Im Kontext dieser Anwendung bildet der **S&P 500** den Referenzindex, gegen den die historische Kursentwicklung einzelner Unternehmen im Dashboard verglichen wird.

**Weighted Average Shares Outstanding**

Die gewichtete durchschnittliche Anzahl ausstehender Aktien berücksichtigt Veränderungen im Aktienbestand – etwa durch Aktienrückkäufe oder Neuemissionen – anteilig über den Berichtszeitraum. Sie ist die Berechnungsgrundlage für den Earnings per Share (EPS) und beeinflusst damit direkt alle EPS-basierten Kennzahlen wie das P/E-Ratio. Im Kontext dieser Anwendung wird ausschließlich die Diluted-Variante verwendet, da sie das vollständige Verwässerungspotenzial eines Unternehmens abbildet und damit eine konservativere sowie aus Anlegerperspektive realistischere Bewertungsgrundlage darstellt.

### Finanzkennzahlen

**Price - Adjusted Closed**

Der Price bezieht sich im Projektkontext immer auf den adjusted Closed Preis eines Handelstages. Er ist die modifizierte Version des Closed Wertes, der Aktien Spaltung, Dividenden und andere Events berücksichtigt und ermöglicht dadurch eine realistischere Betrachtung.

**Price / Earnings - PE - Ratio**

Diese relative Kennzahl setzt den Tages Price und die Earnings eines Unternehmens in Verhältnis. Dabei wird der Price durch die TTM Earnings per Share (EPS) geteilt.

$\quad P/E = \frac{\text{Price per Share}}{\text{EPS diluted (TTM)}}$

**Price / Sales - PS - Ratio**

Diese relative Kennzahl setzt den Tages Price und die Revenues eines Unternehmens in Verhältnis. Dabei wird der Price durch die TTM Revenues per Share geteilt.

$\quad P/S = \frac{\text{Price per Share}}{\text{Revenue per Share (TTM)}}$

**Price / Operating Cashflow - PC - Ratio**

Diese relative Kennzahl setzt den Tages Price und die Operating Cashflows eines Unternehmens in Verhältnis. Dabei wird der Price durch die TTM Operating Cashflows per Share geteilt.

$\quad P/C = \frac{\text{Price per Share}}{\text{Operating Cashflow per Share (TTM)}}$

**Price / Free Cashflow - PFCF - Ratio**

Diese relative Kennzahl setzt den Tages Price und die Free Cashflows eines Unternehmens in Verhältnis. Dabei wird der Price durch die TTM Free Cashflows per Share geteilt.

$\quad P/FCF = \frac{\text{Price per Share}}{\text{Free Cashflow per Share (TTM)}}$

### **Value Strategy**

> Value investing involves picking stocks that seem to be trading for less than their book value.

QUELLE?

Eine Value Strategie basiert auf der Annahmen, dass der Aktienpreis sich von dem tatsächlichen Wert eines Unternehmens im positiven wie auch im negativen entkoppeln kann, jedoch über einen langen Zeitraum zu ihrem wahren Wert zurückkehrt. Um diese Strategie am Aktienmarkt umzusetzen werden mittels verschiedener Methoden die wahren Unternehmenswerte ermittelt. Eine Methode ist es über die Fundamentaldaten auf den Unternehmenswert Rückschlüsse zu führen. Die Hypothese von Value Investoren ist, dass man in unterbewertete Aktien investiert und sich diese mit der Zeit in Richtung ihres eigentlichen Wertes, und damit positiv entwickeln.

**James O’Shaughnessy und der Value Composite**

James O'Shaughnessy ist ein Amerikanischer Investor, CEO von O'Shaughnessy Ventures und Gründer von O'Shaughnessy Asset Management sowie von LLC. In seinem Buch “What Works on Wall Street” stellt er unter anderem den Value Composite One vor. Dieser besteht aus den einem kombinierten Score aus Price-to-book Ratio, Price / Sales Ratio, EBITDA / Enterprise Value, Price / Cashflow Ratio und Price / Earnings Ratio. In seinem Buch hat er mit einem Backtest von 1963 bis 2009 gezeigt, dass man mittels der Kombination aus mehreren Metriken eine Einzelmetrik in 82% der Fällen am Aktienmarkt schlägt. Sein kombinierter Score hatte eine jährliche Rendite von 17.18%.

**Ratio-Auswahl und Peer-Group-Vergleich**

Man kann aus der uns zur Verfügung stehenden PE - Ratio, der PS - Ratio und der PFCF - Ratio einen Combined Value Score machen. Die PC - Ratio wird für den Score verworfen, da der Cashflow sonst übergwichtet wäre, und der Free Cashflow einen besseren Einblick über die tatsächlich zu Verfügung stehenden liquiden Mittel gibt. Da die einzelnen Sektoren unterschiedlichen Bedingungen und damit auch unterschiedlichen Ratio Niveaus und Abweichungen unterliegen, ist es sinnvoll eine Sektor-relative Bewertung vorzunehmen. WIESO SEKTOR RELATIV ??

**Robust Z-Score**

Da die Ratio im Vergleich mit sich selbst unterschiedliche Skalen aufweisen, aber trotzdem gleich gewichtet werden sollen, werden sie mittels dem Robust Z-Score standardisiert. Der Robust Z-Score ist im Gegensatz zu dem Z-Score weniger sensitiv im Bezug auf Ausreißer, da er den Durchschnitt mit dem Median und die Standardabweichung mit der mittlere absoluten Abweichung (MAD) ersetzt.

$\quad \text{Robust Z-Score }z_i = \frac{x_i - \tilde{x}}{\text{MAD}}$

$\quad \text{MAD} = \text{median}(|x_i - \tilde{x}|)$

**Combined Value Score**

Für die Berechnung der Robust Z-Score standardisierten Ratios werden die Mediane des Sektores und der MAD des Sektores verwendet, da der Vergleich innerhalb der Peer-Group und nicht mit der Historie der Einzelaktie stattfinden soll. Als nächstes wird der Median der drei standardisierten Ratios genommen. Da unterbewertete Aktien negative Z-Scores erhalten wird als letztes der Wert invertiert, um die Verständlichkeit für den Endanwender zu erhöhen.

### Momentum-Analyse

**Momentum Score**

Der Momentum Score basiert rein auf technischen Daten und ist die Rendite aus den letzten 6 Monate. Er dient als Vergleich zum Momentum Score. Je besser die Performance der letzten 6 Monate, desto höher der Score. Momentum Investoren gehen davon aus, dass Aktien, die gut laufen auch weiterhin gut laufen werden.

$\quad \text{Price Index}_{6M} = \frac{Price_{end}}{Price_{start}} - 1$

MEHR?

## Technologie

### Clean Architecture

![Abb. 1: Die saubere Architektur (Martin 2018, S. 193)](attachment:20a16a22-2095-4892-a820-7bd4958f58c0:image.png)

Abb. 1: Die saubere Architektur (Martin 2018, S. 193)

Die Clean Architektur folgt einer Regel: “Quellcode-Abhängigkeiten dürfen nur nach innen in Richtung der übergeordneten Richtlinien weisen.” (Martin 2018, S. 194)

Diese Architektur stellt folgende Eigenschaften sicher:

**Framework-Unabhängigkeit**
Die Kernlogik der Anwendung ist nicht an ein bestimmtes Framework gebunden. Frameworks und Libraries werden als austauschbare Werkzeuge eingesetzt, ohne dass sie die Struktur des Systems diktieren.

**Testbarkeit**
Die Geschäftslogik – also Kennzahlenberechnung und Score-Ermittlung – kann isoliert getestet werden, ohne dass eine Datenbankverbindung, ein laufendes UI oder externe Dienste notwendig sind.

**UI-Unabhängigkeit**
Die Präsentationsschicht ist vollständig von der Businesslogik entkoppelt. Das bestehende Streamlit-Dashboard könnte beispielsweise durch ein anderes Frontend ersetzt werden, ohne dass eine einzige Zeile der Score-Berechnung angepasst werden müsste.

**Datenbank-Unabhängigkeit**
Die Geschäftsregeln haben keine direkte Kenntnis der verwendeten Datenbank. MongoDB könnte theoretisch gegen eine relationale Datenbank oder einen anderen Datenspeicher ausgetauscht werden, da die Kommunikation ausschließlich über Abstraktionen erfolgt.

**Unabhängigkeit von externen Komponenten**
Die Domain- und Applikationsschicht hat keinerlei direkte Abhängigkeit zu externen Datenquellen oder Schnittstellen. Ob Daten über eine Finanz-API, eine CSV-Datei oder einen anderen Kanal bezogen werden, ist für die Kernlogik irrelevant.

**Dependency inversion Principle**

“_HIGH LEVEL MODULES SHOULD NOT DEPEND UPON LOW
LEVEL MODULES. BOTH SHOULD DEPEND UPON ABSTRACTIONS.
ABSTRACTIONS SHOULD NOT DEPEND UPON DETAILS. DETAILS
SHOULD DEPEND UPON ABSTRACTIONS_.” (Martin 1996, S. 6)

Um die Clean Architektur umzusetzen wird das Dependency Inversion Principle (DIP) verwendet. Es ist eines der SOLID - Prinzipien und stellt sicher, dass die Businesslogik nicht von der Infrastruktur abhängig ist. Im konkreten Fall wird das DIP für den Datenbankzugriff verwendet. Der Zugriff auf die Mongo Datenbank erfolgt über ein Repository. Im Application Layer wurde eine abstrakte Klasse Namens BaseRepositoryInterface definiert, welches im Infrastructure Layer implementiert wurde. Die Instanziierung der konkreten Repositories erfolgt im Entry Point der Anwendung (Streamlit) und wird per Dependency Injection in die Services des Application Layers injiziert. Somit sind die Abhängigkeiten alle nach innen gerichtet.

**Dependency Injection**

Dependency Injection ist ein Design Pattern, das die praktische Umsetzung des DIP ermöglicht. Anstatt dass eine Klasse ihre Abhängigkeiten selbst instanziiert, werden diese von außen übergeben. Dadurch bleibt die Klasse unabhängig von konkreten Implementierungen und kennt ausschließlich die Abstraktion.

**Repository**

Das Repository Pattern entstammt dem Domain-Driven Design (DDD) und abstrahiert den Datenzugriff vollständig von der Businesslogik. Die Services arbeiten ausschließlich gegen ein definiertes Interface und haben keine Kenntnis darüber, ob die Daten aus MongoDB, einer relationalen Datenbank oder einer anderen Quelle stammen. Im Kontext dieser Anwendung übernimmt das Repository dabei implizit auch die Rolle eines Adapters, da es die MongoDB-spezifische Abfragesyntax in die interne Domänensprache übersetzt.

**Decorator Pattern**

Das Decorator Pattern ist ein strukturelles Entwurfsmuster, das einer bestehenden Klasse zur Laufzeit zusätzliches Verhalten hinzufügt, ohne ihre Schnittstelle zu verändern. Der Decorator implementiert dasselbe Interface wie die dekorierte Klasse und umhüllt sie – er delegiert den eigentlichen Aufruf weiter und ergänzt ihn um zusätzliche Logik. In dieser Anwendung wird das Decorator Pattern für das **Logging** eingesetzt: Der “perfomance_log” umhüllt die eigentliche Funktion und protokoliert die Dauer des Funktionslaufs, ohne dass die Funktion verändert werden muss.

### Systemarchitektur

![Abb. 2: Systemarchitektur. Quelle: Eigene Darstellung](attachment:d9486466-8e12-46a3-bd48-0db4642a7e98:image.png)

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

MongoDB ist ein dokumentorientiertes NoSQL-Datenbankmanagementsystem und verwaltet Collections in JSON-ähnlichen Dokumenten. Dadurch dass die Rohdaten in JSON Dateien vorliegen ist der die Entscheidung für eine dokumentorientierte Datenbank naheliegend. Des weiteren hat MongoDB spezielle Collections für Zeitreihen, die für den Anwendungsfall von großem Nutzen sind. Durch die spezielle Persistierung ist die Time Series Collection performanter in Abfragen und ermöglicht so eine schnelle Bereitstellung von vielen Datenpunkten. Außerdem bietet MongoDB ein Aggregation Framework welches eine Verarbeitung auf Datenbankebene ermöglicht und in gewissen Fällen deutlich effizienter ist als die Verarbeitung mit Python. Dieses Framework bietet sich vor allem für Verarbeitungsschritte an, die keine Business Logik beinhalten, sondern Daten nur transformiert oder verschiebt. Business Logik soll testbar sein und das ist innerhalb des Aggregation Frameworks schwer.

Docker aktiviert beim ersten Start der Mongo Instanz die Authentifizierung automatisch ein. Per Default ist die Authentifizierung deaktiviert und wird aus Sicherheitsgründen in der Anwendung aktiviert. Außerdem gibt es ein Entrypoint-Skript, welches zwei Datenbank User und zwei Datenbanken einrichtet. Es gibt eine Datenbank “raw” für Rohdaten und Zwischenschritte und eine “processed” Datenbank für die finalen Daten. Der erste User hat Lese und Schreibe Rechte auf beiden Datenbanken und wird genutzt um die Daten zu verarbeiten. Der zweite User hat nur Leserechte auf der “processed” Datenbank. Dies bildet eine weitere Sicherheit vor einem ungewollten Schreib-Zugriff und ist im Sinne des Separation of Concerns.

### Backend

Das Application und das Domain Layer sind in Python geschrieben, da Python eine weitverbreitete und im Finanz und Datenbereich beliebte Sprache ist. Darüber hinaus verfügt Python über ein reiches Ökosystem an Bibliotheken, die den Anwendungsfall direkt abdecken – darunter pymongo für den Datenbankzugriff, pytest für das Testing, jsonschema für die Schema-Validierung und viele weitere.

### Testing

Um die Qualität sicherzustellen wird die Anwendung durch Unittests mit pytest abgesichert. Die Funktionen im Domain Layer - darunter die Berechnungsvorschriften für Robust Z-Score, Ratios und Combined Value Score - werden mittels Unittests auf Korrektheit überprüft. Dank DIP und der Dependency Injection ist das Mocken der Repositories und das erstellen des Services verhältnismäßig einfach. Dies ist der direkte praktische Nachweis der gewählten Architektur.

### Logging

Das Logging ist in zwei separate Logger aufgeteilt. Der Applikations-Logger protokolliert relevante Vorkommnisse während der Datenpipeline – etwa JSON-Dateien, die nicht importiert werden konnten, leer waren oder die Schema-Validierung nicht bestanden haben. Der MongoDB-Logger erfasst datenbankspezifische Ereignisse wie Verbindungsfehler oder fehlgeschlagene Schreiboperationen. Beide Logger verwenden strukturierte Log-Level (INFO, WARNING, ERROR) und schreiben in dedizierte Log-Dateien, um eine gezielte Fehleranalyse zu ermöglichen. Zusätzlich existiert ein Performance-Logger, der als Decorator an beliebige Funktionen angehängt werden kann und deren Ausführungszeit dokumentiert. Dies ermöglicht eine gezielte nachträgliche Optimierung rechenintensiver Schritte.

### Frontend

Die Präsentationsschicht der Anwendung wird mit Streamlit umgesetzt. Streamlit ist ein open-source Python Framework, das die Erstellung von interaktiven Web-Applikationen und Dashboards direkt aus Python-Code ermöglicht, ohne dass separate Frontend-Kenntnisse in HTML, CSS oder JavaScript erforderlich sind. Da die gesamte Anwendung in Python geschrieben ist, fügt sich Streamlit nahtlos in den bestehenden Technologie-Stack ein.

Streamlit organisiert die Anwendung in einzelne Pages, die jeweils eine dedizierte Ansicht des Dashboards repräsentieren. Jede Page instanziiert die benötigten Repository-Implementierungen und injiziert diese in die zuständigen Services – sie übernimmt damit die Rolle des Entry Points und der Composition Root für den jeweiligen Anwendungsfall. Die Pages enthalten dabei selbst keine Geschäftslogik, sondern delegieren ausschließlich an die Services und stellen deren Ergebnisse dar. Dies entspricht der konsequenten Trennung von Präsentation und Businesslogik im Sinne der Clean Architecture.

Da Streamlit eine zustandslose Ausführung pro User-Interaktion hat, wird der st.session_state verwendet, um Nutzereingaben und Zwischenergebnisse innerhalb einer Session zu persistieren und unnötige Datenbankabfragen zu vermeiden.

**Dashboard – Pages**

Das Dashboard gliedert sich in fünf Pages, die den Funktionsumfang der Anwendung strukturiert abbilden.

Die **Sector Page** dient als Einstiegspunkt des Dashboards. Sie bietet eine sektorweite Übersicht, in der der Nutzer einen Sektor auswählen, verschiedene Ratios selektieren und die enthaltenen Unternehmen visuell miteinander vergleichen kann. Eine eingezeichnete Medianlinie ermöglicht dabei eine schnelle Einordnung einzelner Unternehmen relativ zur Peer Group.

Die **Company Page** ermöglicht die gezielte Analyse einzelner Unternehmen über eine Suchfunktion. Nach Auswahl eines Unternehmens werden Stammdaten, historische Aktienkurse sowie die zeitliche Entwicklung der verfügbaren Ratios dargestellt. Der historische Kursverlauf kann dabei dem S&P 500 gegenübergestellt werden. Zusätzlich werden die Renditen der letzten 1, 3, 5 und 10 Jahre ausgewiesen.

Die **Top-10 Ranking Page** zeigt die zehn bestplatzierten Unternehmen eines ausgewählten Sektors zu einem definierten Datum. Das Ranking kann wahlweise nach dem Combined Value Score oder dem Momentum Score dargestellt werden, was einen direkten Vergleich beider Strategien ermöglicht.

Die **Full Ranking Page** stellt das vollständige sektorweite Ranking dar. Der Nutzer kann entweder den gesamten Sektor einsehen oder gezielt nach einzelnen Unternehmen suchen und deren Rankingposition nachvollziehen.

Die **Pipeline Page** dient als administrative Steuerungsseite der Anwendung. Über sie kann der Datenimport gestartet und die Verarbeitungspipeline ausgelöst werden. Sie bildet damit den operativen Einstiegspunkt für die Datenbeschaffung und -verarbeitung.
