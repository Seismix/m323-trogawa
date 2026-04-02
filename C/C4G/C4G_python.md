---
title: "C4G_Python"
parent: "C - Umsetzung"
nav_order: 10
---

# C4G: Map, Filter und Reduce einzeln anwenden

> *Ich kann `map()`, `filter()` und `reduce()` einzeln verwenden, um Listen zu transformieren, zu filtern und zu aggregieren.*

## Lernziele

| # | Lernziel | Beantwortet in |
|---|----------|----------------|
| 1 | Ich kann `map()` verwenden, um eine Transformation auf jedes Element einer Liste anzuwenden. | [1. Map anwenden](#1-map-anwenden) |
| 2 | Ich kann `filter()` verwenden, um Elemente aus einer Liste nach einem Kriterium auszuwählen. | [2. Filter anwenden](#2-filter-anwenden) |
| 3 | Ich kann `reduce()` verwenden, um eine Liste auf einen einzelnen Wert zu reduzieren (z.B. Summe berechnen). | [3. Reduce anwenden](#3-reduce-anwenden) |

---

## Überblick

In Python sind `map`, `filter` und `reduce` eingebaute Funktionen oder Teil der funktionalen Programmierung. Mit diesen kann man Listen elegant transformieren, filtern und aggregieren.

| Operation | Was sie tut | Eingabe → Ausgabe |
|-----------|------------|-------------------|
| `map()` | Transformiert jedes Element | List → List (gleiche Anzahl) |
| `filter()` | Wählt Elemente nach Kriterium | List → List (gleiche oder weniger Elemente) |
| `reduce()` | Fasst alle Elemente zusammen | List → Einzelwert |

---

## 1. Map anwenden

`map(funktion, liste)` wendet eine Funktion auf jedes Element an und gibt einen Iterator zurück.

```python
# Alle Zahlen verdoppeln
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)  # [2, 4, 6, 8, 10]
```

`map()` verändert die Originalliste nicht, sondern erzeugt eine neue:

```python
print(numbers)  # [1, 2, 3, 4, 5] — unverändert
```

### Weitere Beispiele

```python
# Quadratzahlen berechnen
squares = list(map(lambda x: x * x, [1, 2, 3, 4]))
print(squares)  # [1, 4, 9, 16]

# Preise mit Mehrwertsteuer (8.1%)
prices = [10.0, 25.0, 50.0]
with_tax = list(map(lambda p: round(p * 1.081, 2), prices))
print(with_tax)  # [10.81, 27.03, 54.05]

# Strings in Grossbuchstaben
words = ["hallo", "welt", "python"]
upper = list(map(str.upper, words))
print(upper)  # ['HALLO', 'WELT', 'PYTHON']
```

### Map mit benannter Funktion

```python
def format_name(name: str) -> str:
    stripped = name.strip()
    return stripped[0].upper() + stripped[1:].lower()

raw_names = ["  alice", "BOB  ", " charlie "]
clean_names = list(map(format_name, raw_names))
print(clean_names)  # ['Alice', 'Bob', 'Charlie']
```

---

## 2. Filter anwenden

`filter(predicate, liste)` behält nur die Elemente, für die das Predicate `True` zurückgibt.

```python
# Nur gerade Zahlen behalten
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
even = list(filter(lambda x: x % 2 == 0, numbers))
print(even)  # [2, 4, 6, 8]
```

### Weitere Beispiele

```python
# Nur positive Zahlen
values = [-5, 3, -1, 7, 0, -2, 4]
positive = list(filter(lambda x: x > 0, values))
print(positive)  # [3, 7, 4]

# Nur Strings mit mindestens 5 Zeichen
words = ["Hi", "Hallo", "Welt", "Stream", "OK"]
long_words = list(filter(lambda w: len(w) >= 5, words))
print(long_words)  # ['Hallo', 'Stream']

# Nur bestandene Prüfungen (Note >= 4.0)
grades = [5.5, 3.5, 4.0, 2.0, 6.0, 4.5]
passed = list(filter(lambda g: g >= 4.0, grades))
print(passed)  # [5.5, 4.0, 6.0, 4.5]
```

### Filter mit benannter Funktion

```python
def is_valid_email(email: str) -> bool:
    at_index = email.find('@')
    return at_index > 0 and '.' in email[at_index:]

emails = ["alice@example.com", "invalid", "bob@mail.ch", "no-at-sign"]
valid = list(filter(is_valid_email, emails))
print(valid)  # ['alice@example.com', 'bob@mail.ch']
```

---

## 3. Reduce anwenden

`reduce(funktion, liste)` kombiniert alle Elemente schrittweise zu einem einzelnen Wert. Die Funktion nimmt immer zwei Argumente: den bisherigen Wert und das nächste Element.

```python
from functools import reduce

# Summe aller Zahlen
numbers = [1, 2, 3, 4, 5]
total = reduce(lambda acc, x: acc + x, numbers)
print(total)  # 15
```

### Wie Reduce funktioniert (Schritt für Schritt)

Für `reduce(lambda acc, x: acc + x, [1, 2, 3, 4, 5])`:

| Schritt | `acc` | `x` | Ergebnis |
|---------|-------|-----|----------|
| Start   | 1     |     | 1        |
| 1       | 1     | 2   | 3        |
| 2       | 3     | 3   | 6        |
| 3       | 6     | 4   | 10       |
| 4       | 10    | 5   | 15       |

### Weitere Beispiele

```python
# Produkt aller Zahlen
numbers = [2, 3, 4, 5]
product = reduce(lambda acc, x: acc * x, numbers)
print(product)  # 120

# Maximum finden
values = [3, 7, 2, 9, 4]
maximum = reduce(lambda acc, x: x if x > acc else acc, values)
print(maximum)  # 9

# Strings zusammenfügen
words = ["Funktionale", "Programmierung", "ist", "elegant"]
sentence = reduce(
    lambda acc, w: w if acc == "" else acc + " " + w,
    words,
    ""
)
print(sentence)  # Funktionale Programmierung ist elegant
```

### Reduce mit Startwert

Mit einem Startwert beginnt die Reduktion von diesem Wert:

```python
from functools import reduce

numbers = [1, 2, 3]
sum_with_start = reduce(lambda acc, x: acc + x, numbers, 10)
print(sum_with_start)  # 16 (statt 6)

# Leere Liste
empty_sum = reduce(lambda acc, x: acc + x, [], 0)
print(empty_sum)  # 0
```
