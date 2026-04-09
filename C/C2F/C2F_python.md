---
title: "C2F"
parent: "C - Umsetzung"
nav_order: 5
---

# C2F: Higher-Order Functions erstellen

> *Ich kann Funktionen als Argumente für andere Funktionen verwenden und dadurch höherwertige Funktionen erstellen.*

## Lernziele

| # | Lernziel | Beantwortet in |
| --- | ---------- | -------------- |
| 1 | Ich kann eine Funktion schreiben, die eine andere Funktion als Parameter entgegennimmt und aufruft. | [1. Funktion als Argument übergeben](#1-funktion-als-argument-übergeben) |
| 2 | Ich kann eine eigene Higher-Order Function implementieren (z.B. eine eigene `apply`-Funktion). | [2. Eigene Higher-Order Function schreiben](#2-eigene-higher-order-function-schreiben) |
| 3 | Ich kann das Callback-Muster mit Higher-Order Functions umsetzen, um flexiblen, wiederverwendbaren Code zu schreiben. | [3. Callback-Muster anwenden](#3-callback-muster-anwenden) |

---

## 1. Funktion als Argument übergeben

Eine **Higher-Order Function** ist eine Funktion, die als Parameter selbst eine andere Funktion entgegennimmt und diese aufruft, oder eine Funktion als Ergebnis liefert.

```python
def apply_twice(func, value):
    # Erwartet eine Funktion als Argument und wendet diese zweimal an
    return func(func(value))

print(apply_twice(lambda x: x + 3, 7))   # 13  (7→10→13)
print(apply_twice(lambda x: x * 2, 5))   # 20  (5→10→20)
```

`apply_twice` ist eine Higher-Order Function, weil ihr Parameter `func` keine statische Variable ist, sondern selbst ein Verhalten darstellt. Welche exakte Logik ausgeführt wird, entscheidet sich erst beim Methodenaufruf.

### Eingebaute Higher-Order Functions in Python

Python besitzt zahlreiche vordefinierte Higher-Order Functions für elegante Datentransformationen:

| Funktion | Callback-Art | Anwendungsfall |
| ------- | ----------------- | ----- |
| `map()` | Transformations-Funktion | Jedes Element umwandeln |     
| `filter()`| Prüf-Funktion (Predicate) | Elemente nach Kriterium filtern | 
| `sorted()`| Sortierschlüssel (`key=`) | Sortierreihenfolge definieren |
| `reduce()`| Aggregations-Funktion | Alle Elemente cumulativ zusammenfassen |

---

## 2. Eigene Higher-Order Function schreiben

### Eigenes `apply_to_all` (wie `map`, aber selbst verfasst)

```python
def apply_to_all(lst, func):
    result = []
    for item in lst:
        result.append(func(item))
    return result

numbers = [1, 2, 3, 4]

doubled = apply_to_all(numbers, lambda x: x * 2)  # [2, 4, 6, 8]
squared = apply_to_all(numbers, lambda x: x * x)  # [1, 4, 9, 16]
negated = apply_to_all(numbers, lambda x: -x)     # [-1, -2, -3, -4]
```

Dieselbe `apply_to_all`-Routine kann völlig unterschiedliche Transformationen durchführen, weil die konkrete Programm-Logik von aussen eingefügt wird (Dependency Injection).

### Funktion zurückgeben: `create_multiplier`

```python
def create_multiplier(factor):
    return lambda x: x * factor

doubler = create_multiplier(2)
tripler = create_multiplier(3)

print(doubler(5))  # 10
print(tripler(5))  # 15
```

Auch `create_multiplier` ist eine Higher-Order Function, weil sie eine Funktion-Referenz zurückgibt. Das zurückgegebene Lambda speichert den übergebenen `factor` (sog. Closure) dauerhaft.

---

## 3. Callback-Muster anwenden

Das **Callback**-Prinzip sieht vor, dass man eine Funktion übergibt, die zu einem bestimmten Zeitpunkt oder unter bestimmten Bedingungen ausgeführt wird. Das erhöht die Wiederverwendbarkeit und reduziert Code-Duplikation.

### Beispiel: Listenverarbeitung mit Logging-Callback

```python
def process_with_callback(items, filter_rule, on_match):
    result = []
    for item in items:
        # Erste Funktion wird als Filter-Test genutzt
        if filter_rule(item):
            # Zweite Funktion wird aufgerufen, wenn das Item den Filter erfüllt
            on_match(item)
            result.append(item)
    return result

numbers = [1, 2, 3, 4, 5, 6, 7, 8]

# Callback: Gefundene Elemente im Terminal melden
even_numbers = process_with_callback(
    numbers,
    lambda x: x % 2 == 0,
    lambda x: print(f"Gefunden: {x}")
)
# Konsolenausgabe:
# Gefunden: 2
# Gefunden: 4
# Gefunden: 6
# Gefunden: 8
```

### Beispiel: Austauschbare Validierungs-Logik

```python
def validate_all(inputs, rule):
    # Diese Funktion definiert nur das "wie", nicht das "was"
    return all(rule(item) for item in inputs)

emails = ["a@b.ch", "c@d.com", "e@f.org"]

all_have_at = validate_all(emails, lambda s: "@" in s)           # True     
all_are_swiss = validate_all(emails, lambda s: s.endswith(".ch"))  # False
```

Die eigentliche Validierungs-Logik (`rule`) wird komplett ausgelagert. Die Funktion `validate_all` bleibt völlig neutral und weiss nicht, welche spezifischen Anforderungen geprüft werden – sie fungiert nur als Wrapper für die Callback-Ausführung.
