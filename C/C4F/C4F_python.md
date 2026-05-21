---
title: "C4F_Python"
parent: "C - Umsetzung"
nav_order: 11
---

# C4F: Map, Filter und Reduce kombinieren

> *Ich kann Map, Filter und Reduce kombiniert verwenden, um Daten zu verarbeiten und zu manipulieren, die komplexere Transformationen erfordern.*

## Lernziele

| # | Lernziel | Beantwortet in |
|---|----------|----------------|
| 1 | Ich kann `filter()` und `map()` kombinieren, um Daten zuerst zu filtern und dann zu transformieren. | [1. Filter + Map Kette](#1-filter--map-kette) |
| 2 | Ich kann `map()` und `reduce()` kombinieren, um Daten zu transformieren und anschliessend zu aggregieren. | [2. Map + Reduce Kette](#2-map--reduce-kette) |
| 3 | Ich kann `filter()`, `map()` und `reduce()` in einer Pipeline kombinieren, um eine mehrstufige Datenverarbeitung durchzuführen. | [3. Dreifach-Kombination](#3-dreifach-kombination) |

---

## 1. Filter + Map Kette

Zuerst Elemente auswählen, dann transformieren. Die Reihenfolge ist wichtig: Filtern vor dem Transformieren reduziert die Anzahl der zu verarbeitenden Elemente.

```python
# Nur positive Zahlen quadrieren
numbers = [1, -2, 3, -4, 5]
result = list(map(lambda x: x * x, filter(lambda x: x > 0, numbers)))
print(result)  # [1, 9, 25]
```

### Praxisbeispiel: Produktnamen

```python
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float

products = [
    Product("Laptop", 1200.0),
    Product("Maus", 25.0),
    Product("Monitor", 450.0),
    Product("Kabel", 8.0),
]

# Namen aller Produkte über 100 CHF, in Grossbuchstaben
expensive = filter(lambda p: p.price > 100, products)
expensive_names = list(map(lambda p: p.name.upper(), expensive))
print(expensive_names)  # ['LAPTOP', 'MONITOR']
```

---

## 2. Map + Reduce Kette

Zuerst Daten transformieren, dann zu einem einzelnen Wert zusammenfassen.

```python
from functools import reduce

# Gesamtpreis aller Produkte berechnen
total = reduce(lambda acc, x: acc + x, map(lambda p: p.price, products), 0.0)
print(total)  # 1683.0
```

### Praxisbeispiel: Zeichenlänge

```python
from functools import reduce

# Gesamtanzahl Zeichen aller Wörter
words = ["Funktional", "ist", "elegant"]
total_chars = reduce(lambda acc, n: acc + n, map(len, words), 0)
print(total_chars)  # 20
```

---

## 3. Dreifach-Kombination

Die vollständige Pipeline: filtern, transformieren, aggregieren.

```python
from functools import reduce

# Summe aller verdoppelten Preise über 10 CHF
prices = [5.0, 15.0, 8.0, 20.0, 3.0, 12.0]

filtered = filter(lambda p: p > 10, prices)       # [15.0, 20.0, 12.0]
doubled  = map(lambda p: p * 2, filtered)          # [30.0, 40.0, 24.0]
total    = reduce(lambda acc, x: acc + x, doubled, 0.0)  # 94.0
print(total)
```

### Praxisbeispiel: Lohnsumme

```python
from dataclasses import dataclass
from functools import reduce

@dataclass
class Employee:
    name: str
    dept: str
    salary: float

employees = [
    Employee("Anna",  "IT", 8500),
    Employee("Beat",  "IT", 7200),
    Employee("Clara", "HR", 6800),
    Employee("David", "IT", 9100),
    Employee("Eva",   "HR", 7000),
]

# Gesamtlohn aller IT-Mitarbeitenden mit Gehalt über 8000
it_staff      = filter(lambda e: e.dept == "IT", employees)     # Anna, Beat, David
high_earners  = filter(lambda e: e.salary > 8000, it_staff)     # Anna, David
salaries      = map(lambda e: e.salary, high_earners)           # [8500, 9100]
total         = reduce(lambda acc, s: acc + s, salaries, 0.0)   # 17600.0
print(total)
```

### Vergleich: Imperativ vs. Pipeline

| Aspekt | Imperativ | Pipeline |
|--------|-----------|----------|
| Zwischenvariablen | Mehrere Listen | Keine (lazy evaluation) |
| Lesbarkeit | Logik in Schleifen verteilt | Schritte linear von oben nach unten |
| Immutability | Manuell sicherstellen | Automatisch durch `filter`/`map` |

```python
# Imperativ
total = 0.0
for e in employees:
    if e.dept == "IT" and e.salary > 8000:
        total += e.salary

# Deklarativ (gleiche Logik, klarer strukturiert)
total = reduce(
    lambda acc, s: acc + s,
    map(lambda e: e.salary,
        filter(lambda e: e.dept == "IT" and e.salary > 8000, employees)),
    0.0
)
```
