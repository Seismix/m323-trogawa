---
title: "BG1_Python"
parent: "B - Anforderungen & Design"
nav_order: 1
---

# BG1: Imperativ vs. Deklarativ unterscheiden

> *Ich kann den Unterschied zwischen Anforderungen der imperativen Programmierung (definierte Folge von Handlungsanweisungen) und der deklarativen Programmierung (Beschreibung des Endzustandes) erklären.*

## Lernziele

| # | Lernziel | Beantwortet in |
|---|----------|----------------|
| 1 | Ich kann anhand eines Beispiels erklären, was imperative Programmierung bedeutet: eine Schritt-für-Schritt-Anweisung, die dem Computer sagt, *wie* etwas zu tun ist. | [Imperativ vs. Deklarativ](#imperativ-vs-deklarativ) |
| 2 | Ich kann anhand eines Beispiels erklären, was deklarative Programmierung bedeutet: eine Beschreibung des gewünschten Endzustands (*was* erreicht werden soll). | [Imperativ vs. Deklarativ](#imperativ-vs-deklarativ) |
| 3 | Ich kann gegebene Codebeispiele korrekt als imperativ oder deklarativ einordnen und meine Zuordnung begründen. | [Imperativ oder deklarativ?](#imperativ-oder-deklarativ) |
| 4 | Ich kann mindestens 2 deklarative Sprachen oder Technologien nennen und erklären, warum sie deklarativ sind. | [Deklarative Sprachen und Technologien](#deklarative-sprachen-und-technologien) |

---

## Imperativ vs. Deklarativ

Der grundlegende Unterschied zwischen den beiden Paradigmen lässt sich einfach auf den Punkt bringen:

| Paradigma | Fokus | Zentrale Frage |
|-----------|-----------|-------|
| **Imperativ** | *Wie* der Lösungsweg aussieht | "Welche exakten Schritte muss das Programm ausführen?" |
| **Deklarativ** | *Was* am Ende herauskommen soll | "Welches Resultat möchte ich erhalten?" |

### Beispiel aus dem Alltag: Ein Gericht bestellen

**Imperativ** (Wie ein Kochrezept, Schritt für Schritt):

> Zwiebeln in feine Stücke schneiden. Etwas Öl in einer kleinen Pfanne erhitzen. Die Zwiebeln darin 5 Minuten glasig dünsten. Anschliessend mit Gemüsebrühe ablöschen und 20 Minuten kochen. Am Ende alles fein pürieren.

**Deklarativ** (Wie eine Bestellung im Restaurant):

> Ich hätte gerne einen Teller Zwiebelsuppe.

Beim imperativen Vorgehen definiert man **jede einzelne Teilaktion**. Beim deklarativen Ansatz hingegen beschreibt man lediglich **das gewünschte Resultat** und überlässt die konkrete Umsetzung dem zuständigen Ausführenden (dem Koch bzw. dem Computer).

---

## Imperativ oder deklarativ?

### Code-Beispiel: Alle Zahlen über 5 herausfiltern

**Imperativ** (Detaillierte Anweisungen, manuelle Schleife):

```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
result = []
for x in numbers:
    if x > 5:
        result.append(x)
```

Hier wird der genaue Ablauf programmiert: eine Iteration durchführen, eine Bedingung evaluieren und das gültige Element explizit zur neuen Liste hinzufügen.

**Deklarativ** (Direkte Formulierung des gewünschten Ergebnisses):

```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Nutzung einer List Comprehension in Python
result = [x for x in numbers if x > 5]

# Alternative mit der filter-Funktion und Lambda:
# result = list(filter(lambda x: x > 5, numbers))
```

Die Comprehension verdeutlicht sofort, *was* wir ermitteln möchten: alle Elemente `x`, für die `x > 5` gilt. Wie die Programmiersprache den Speicher verwaltet und intern durch die Liste geht, ist irrelevant.

### Zusätzliche Beispiele

| Operation | Imperativ | Deklarativ |
|---------|----------|------------|
| Summe kalkulieren | `total = 0; for x in lst: total += x` | `sum(lst)` |
| Liste sortieren | Ein eigener Algorithmus (z.B. Bubble Sort mit Schleifen) | `sorted(lst)` |
| Höchsten Wert finden | Ein iterativer Durchlauf, der eine Extra-Variable speichert | `max(lst)` |

In allen deklarativen Modellen teilt man dem System mit, *welches Ziel* man anstrebt, ohne die interne *Mechanik* auszuschreiben.

---

## Deklarative Sprachen und Technologien

Gewisse Sprachen und Werkzeuge wurden speziell für diesen deklarativen Programmierstil entworfen:

| Technologie | Weshalb deklarativ? | Code-Beispiel |
|---------------------|------------------|----------|
| **SQL** | Man definiert, *welche* Datensätze gefiltert werden sollen, ohne den Suchmechanismus der Datenbank vorzugeben. | `SELECT name FROM users WHERE age > 18` |
| **HTML/CSS** | Man strukturiert, *wie* die Website visuell beschaffen ist, nicht die Pixel-Zeichenanweisungen des Browsers. | `<h1>Titel</h1>` |
| **Reguläre Ausdrücke** | Man legt ein *Textmuster* fest, anstatt manuell jedes einzelne Zeichen in einer Schleife zu untersuchen. | `\d{3}-\d{4}` |

Ein SQL-Statement wie `SELECT name FROM users WHERE age > 18` dient ausschliesslich der Bekanntgabe unseres Zielzustandes. Wir geben keine Befehle der Art weiter: "Öffne die Tabelle, überprüfe nacheinander jede Tabellenzeile ab Index 0 auf das Alter, und speichere den Namen heraus". Das Datenbankmanagementsystem entscheidet und optimiert die Herangehensweise vollkommen eigenständig.

Die funktionale Programmierung stützt sich ebenfalls extrem stark auf das deklarative Prinzip: Anstelle von klassischen Iterator-Schleifen verfasst man Datentransformationen (mit Hilfe von Funktionen wie `map`, `filter`, `reduce` oder eben kompakten List Comprehensions in Python).