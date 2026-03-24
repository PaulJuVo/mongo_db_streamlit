# Einleitung

## Problemstellung

Die systematische Verarbeitung, Bewertung und der Vergleich anhand von historischen Fundamentaldaten, ist für private wie auch für institutionelle Anwender mit erheblichem Aufwand verbunden. Etablierte Anbieter wie Yahoo Finance, [Finanzen.net](http://Finanzen.net) oder Bloomberg sind entweder sehr teuer oder bieten keine gesonderte zeitliche Darstellung für Price-Ratios an. Viele Anbieter zeigen oft nur Price-Earnings zu den Quartalsenden an. Da Unternehmen ihren Bilanzierungskalender und damit ihre Quartale selbst definieren, gehen zusätzlich zeitliche Informationen verloren. Durch die vielen Ratios entsteht das Problem der Informationsüberflutung und da Price-Ratios vor allem für Value-Investoren interessant sind, bietet es sich an einen kombinierten Value Score aus den Ratios zu generieren und in einem Ranking anzuzeigen und mit einem rein technischen Momentum Score Ranking zu vergleichen.

Darüber hinaus erfordert ein System dieser Art eine sorgfältige Softwarearchitektur: Die Kombination aus heterogenen Datenquellen, komplexer Kennzahlenlogik und dem Anspruch an langfristige Wartbarkeit und Erweiterbarkeit macht den Einsatz etablierter Architekturprinzipien – wie Clean Architecture, Dependency Inversion und systematischem Testing – zu einer zentralen Anforderung an die Umsetzung.

Vor diesem Hintergrund stellt sich die Frage, wie eine Anwendung konzipiert und entwickelt werden kann, die historische Fundamentaldaten des S&P500 strukturiert aufbereitet, relevante Kennzahlen berechnet und einen systematischen Vergleich von Unternehmen innerhalb einer Peer Group über einen Zeitraum von ca. 15 Jahren ermöglicht.

## Zielsetzung

Konzipierung und Umsetzung einer Anwendung, die fundamental sowie historische Daten verarbeitet, in einer Datenbank speichert und diese dann in einem Dashboard zur Ansicht zur Verfügung stellt. Verschiedene Ratios sollen für ein Unternehmen über die Zeit dargestellt und vergleichbar gemacht werden. Außerdem sollen Unternehmen untereinander und mit dem Peer-Group Median verglichen werden können. Um den vollen Funktionsumfang eines Dashboards zu gewährleisten sollen auch die historischen Aktienpreise und zum Vergleich mit ihrem Index angezeigt werden. Basierend auf den Ratios wird ein Combined Score ermittelt, der in einem Ranking angezeigt und mit einem Momentum Ranking verglichen werden kann. Prototypisch wird die Anwendung nur für Unternehmen aus dem S&P500 umgesetzt. Das Projekt fokussiert sich auf historische Fundamentaldaten und beinhaltet keine Echtzeitdaten, keine Prognose -Modelle und keine automatisierte Investment-Empfehlung.

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

Forward-Kennzahlen basieren auf gebräuchlicherweise auf Analystenschätzungen für zukünftige Perioden, z.B. den erwarteten Gewinn der kommenden zwölf Monate. Der Begriff wird zur Abgrenzung gegenüber Trailing-Metriken und bezieht sich in diesem Projektkontext auf tatsächliche Finanzdaten in der vorwärtsgerichteten Betrachtung (kein Forecast!).

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

### Value-Analyse

**Value Strategy**

> Value investing involves picking stocks that seem to be trading for less than their book value.

Eine Value Strategie basiert auf der Annahmen, dass der Aktienpreis sich von dem tatsächlichen Wert eines Unternehmens im positiven wie auch im negativen entkoppeln kann, jedoch über einen langen Zeitraum zu ihrem wahren Wert zurückkehrt. Um diese Strategie am Aktienmarkt umzusetzen werden mittels verschiedener Methoden die wahren Unternehmenswerte ermittelt. Eine Methode ist es über die Fundamentaldaten auf den Unternehmenswert Rückschlüsse zu führen. Die Hypothese von Value Investoren ist, dass man in unterbewertete Aktien investiert und sich diese mit der Zeit in Richtung ihres eigentlichen Wertes, und damit positiv entwickeln.

**James O’Shaughnessy und der Value Composite**

James O'Shaughnessy ist ein Amerikanischer Investor, CEO von O'Shaughnessy Ventures und Gründer von O'Shaughnessy Asset Management sowie von LLC. In seinem Buch “What Works on Wall Street” stellt er unter anderem den Value Composite One vor. Dieser besteht aus den einem kombinierten Score aus Price-to-book Ratio, Price / Sales Ratio, EBITDA / Enterprise Value, Price / Cashflow Ratio und Price / Earnings Ratio. In seinem Buch hat er mit einem Backtest von 1963 bis 2009 gezeigt, dass man mittels der Kombination aus mehreren Metriken eine Einzelmetrik in 82% der Fällen am Aktienmarkt schlägt. Sein kombinierter Score hatte eine jährliche Rendite von 17.18%.

**Ratio-Auswahl und Peer-Group-Vergleich**

Man kann aus der uns zur Verfügung stehenden PE - Ratio, der PS - Ratio und der PFCF - Ratio einen Combined Value Score machen. Die PC - Ratio wird für den Score verworfen, da der Cashflow sonst übergwichtet wäre, und der Free Cashflow einen besseren Einblick über die tatsächlich zu Verfügung stehenden liquiden Mittel gibt. Da die einzelnen Sektoren unterschiedlichen Bedingungen und damit auch unterschiedlichen Ratio Niveaus und Abweichungen unterliegen, ist es sinnvoll eine Sektor-relative Bewertung vorzunehmen.

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
