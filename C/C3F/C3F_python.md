---
title: "C3F_Python"
parent: "C - Umsetzung"
nav_order: 8
---

# C3F: Lambda-Ausdrücke mit mehreren Argumenten

> *Ich kann Lambda-Ausdrücke schreiben, die mehrere Argumente verarbeiten können.*

## Lernziele

| # | Lernziel | Beantwortet in |
|---|----------|----------------|
| 1 | Ich kann Lambda-Ausdrücke mit zwei oder mehr Parametern schreiben (z.B. `lambda x, y: x + y`). | [Multi-Parameter Lambdas](#multi-parameter-lambdas) |
| 2 | Ich kann einen Multi-Parameter Lambda-Ausdruck als Sortierkriterium einsetzen, um komplexe Datenstrukturen zu ordnen. | [Lambdas als Sortierkriterium](#lambdas-als-sortierkriterium) |
| 3 | Ich kann Lambda-Ausdrücke mit Typ-Annotationen (`Callable`) versehen und in Variablen speichern. | [Lambdas in Variablen speichern](#lambdas-in-variablen-speichern) |

---

## Multi-Parameter Lambdas

Ein Lambda-Ausdruck in Python kann beliebig viele Parameter entgegennehmen, getrennt durch Kommas:

```python
# Lambda mit zwei Parametern: Fläche eines Rechtecks
area = lambda width, height: width * height
area(5, 3)  # => 15

# Lambda mit drei Parametern: gewichteter Durchschnitt
weighted_avg = lambda a, b, weight: a * weight + b * (1 - weight)
weighted_avg(80, 60, 0.7)  # => 74.0
```

### Vergleich: ein Parameter vs. mehrere

```python
# Ein Parameter
double_it = lambda x: x * 2

# Zwei Parameter
add = lambda x, y: x + y

# Zwei Parameter mit komplexerem Ausdruck
full_name = lambda first, last: first + " " + last
full_name("Max", "Muster")  # => "Max Muster"
```

---

## Lambdas als Sortierkriterium

In Python nimmt `sorted()` einen `key=`-Parameter entgegen – eine Funktion, die aus jedem Element einen Vergleichswert erzeugt:

```python
# Liste von Tupeln nach dem zweiten Element sortieren
pairs = [("1", "b"), ("2", "a"), ("3", "c")]

sorted_pairs = sorted(pairs, key=lambda pair: pair[1])
# => [("2", "a"), ("1", "b"), ("3", "c")]
```

Der `key`-Lambda erhält ein einzelnes Element und gibt den Vergleichswert zurück.

```python
# Dataclass nach Preis sortieren
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float

products = [
    Product("Milch", 1.80),
    Product("Brot", 3.50),
    Product("Käse", 5.20),
]

sorted_products = sorted(products, key=lambda p: p.price)
# => [Milch, Brot, Käse]
```

### Sortieren nach mehreren Kriterien

Mit einem Tupel im `key`-Lambda kann nach mehreren Feldern gleichzeitig sortiert werden:

```python
students = [("Anna", 5.5), ("Ben", 4.0), ("Clara", 5.5), ("David", 4.0)]

# Zuerst nach Note (absteigend), dann alphabetisch nach Name
sorted_students = sorted(students, key=lambda s: (-s[1], s[0]))
# => [("Anna", 5.5), ("Clara", 5.5), ("Ben", 4.0), ("David", 4.0)]
```

---

## Lambdas in Variablen speichern

In Python können Lambda-Ausdrücke direkt in Variablen gespeichert werden. Mit `Callable` aus dem `typing`-Modul lassen sich Typ-Annotationen hinzufügen:

```python
from typing import Callable

# Zwei verschiedene Typen → Callable[[str, int], str]
repeat: Callable[[str, int], str] = lambda s, n: s * n
repeat("Ha", 3)  # => "HaHaHa"

# Zwei gleiche Typen, gleicher Rückgabetyp
maximum: Callable[[int, int], int] = lambda a, b: a if a > b else b
maximum(7, 3)  # => 7

# Zwei Parameter, kein Rückgabewert → Callable[[str, int], None]
print_entry: Callable[[str, int], None] = lambda key, val: print(f"{key}: {val}")
print_entry("Score", 42)  # Score: 42

# Zwei Parameter, boolescher Rückgabewert
has_length: Callable[[str, int], bool] = lambda s, length: len(s) == length
has_length("Hallo", 5)  # => True
```

Im Gegensatz zu Java gibt es in Python keine eigenen Interfaces wie `BiFunction` oder `BinaryOperator`. Stattdessen beschreibt `Callable[[Arg1, Arg2], Rückgabe]` den Typ eines Multi-Parameter Lambdas vollständig.
