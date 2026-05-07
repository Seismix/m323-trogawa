---
title: "C1F_Python"
parent: "C - Umsetzung"
nav_order: 2
---

# C1F: Algorithmen in funktionale Teilstücke aufteilen

> *Ich kann Algorithmen in funktionale Teilstücke aufteilen.*

## Lernziele

| # | Lernziel | Beantwortet in |
| --- | ---------- | -------------- |
| 1 | Ich kann in einem gegebenen Algorithmus sinnvolle Teilschritte erkennen, die als eigenständige Funktionen implementiert werden können. | [1. Teilfunktionen identifizieren](#1-teilfunktionen-identifizieren) |
| 2 | Ich kann einen Algorithmus so zerlegen, dass jede Teilfunktion genau eine Aufgabe erfüllt (Single Responsibility). | [2. Funktionale Dekomposition](#2-funktionale-dekomposition) |
| 3 | Ich kann beschreiben, wie die einzelnen Teilfunktionen zusammengesetzt werden, um den Gesamtalgorithmus zu bilden. | [3. Zusammensetzung planen](#3-zusammensetzung-planen) |

---

## 1. Teilfunktionen identifizieren

Ein Algorithmus, der zu viel auf einmal macht, ist schwer zu testen und zu warten. Der erste Schritt ist, logische Teilschritte zu erkennen.

### Beispiel: Monolithische Funktion

```python
def process(data):
    result = []
    for s in data:
        trimmed = s.strip()
        if trimmed:
            result.append(trimmed.lower())
    unique = list(dict.fromkeys(result))
    unique.sort()
    return unique
```

Dieser Code enthält vier logische Schritte:

| Schritt | Was passiert | Mögliche Funktion |
| ------- | ------------ | ----------------- |
| 1 | Whitespace entfernen und leere Strings filtern | `clean_entries()` |
| 2 | In Kleinbuchstaben umwandeln | (Teil von `clean_entries()`) |
| 3 | Duplikate entfernen | `remove_duplicates()` |
| 4 | Alphabetisch sortieren | `sort_list()` |

---

## 2. Funktionale Dekomposition

Jede Teilfunktion bekommt genau eine Aufgabe (Single Responsibility), nimmt eine Liste entgegen und gibt eine neue Liste zurück:

```python
# Teilfunktion 1: Bereinigen und leere Einträge entfernen
def clean_entries(data):
    return [s.strip().lower() for s in data if s.strip()]

# Teilfunktion 2: Duplikate entfernen
def remove_duplicates(data):
    return list(dict.fromkeys(data))

# Teilfunktion 3: Sortieren
def sort_list(data):
    return sorted(data)
```

### Vorteile der Zerlegung

| Vorteil | Erklärung |
| ------- | --------- |
| **Testbarkeit** | Jede Funktion kann isoliert mit eigenen Testfällen geprüft werden |
| **Wiederverwendbarkeit** | `remove_duplicates` kann überall eingesetzt werden, nicht nur hier |
| **Lesbarkeit** | Funktionsnamen dokumentieren die Logik |
| **Wartbarkeit** | Änderungen betreffen nur die betroffene Teilfunktion |

---

## 3. Zusammensetzung planen

Die Teilfunktionen werden so zusammengesetzt, dass der Output der einen zum Input der nächsten wird:

```python
def process(data):
    cleaned = clean_entries(data)
    unique = remove_duplicates(cleaned)
    return sort_list(unique)
```

### Weiteres Beispiel: Durchschnitt positiver Zahlen

**Aufgabe:** Berechne den Durchschnitt aller positiven Zahlen in einer Liste.

**Zerlegung:**

```python
# Schritt 1: Nur positive Zahlen behalten
def filter_positive(numbers):
    return [n for n in numbers if n > 0]

# Schritt 2: Summe berechnen
def sum_numbers(numbers):
    return sum(numbers)

# Schritt 3: Durchschnitt berechnen
def average(numbers):
    return 0.0 if not numbers else sum_numbers(numbers) / len(numbers)

# Zusammensetzung
def average_of_positive(numbers):
    positive = filter_positive(numbers)
    return average(positive)
```

```python
data = [-3, 5, -1, 8, 2, -7, 4]
print(average_of_positive(data))  # Output: 4.75
```

Die Zerlegung folgt immer dem gleichen Muster: Teilschritte identifizieren, als eigenständige Funktionen implementieren, dann verketten. Jede Funktion verändert dabei die Eingabe nicht, sondern erzeugt einen neuen Wert.
