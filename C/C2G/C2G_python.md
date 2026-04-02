---
title: "C2G_Python"
parent: "C - Umsetzung"
nav_order: 4
---

# C2G: Funktionen als Objekte behandeln

> *Ich kann Funktionen als First-Class Citizens behandeln: in Variablen speichern, als Rückgabewert verwenden und in Datenstrukturen ablegen.*

## Lernziele

| # | Lernziel | Beantwortet in |
|---|----------|----------------|
| 1 | Ich kann eine Funktion in einer Variable speichern und diese Variable aufrufen, um die Funktion auszuführen. | [1. Funktion einer Variable zuweisen](#1-funktion-einer-variable-zuweisen) |
| 2 | Ich kann eine Funktion schreiben, die eine andere Funktion zurückgibt. | [2. Funktion als Rückgabewert](#2-funktion-als-rückgabewert) |
| 3 | Ich kann Funktionen in Listen oder Dictionaries speichern und gezielt abrufen. | [3. Funktionen in Datenstrukturen speichern](#3-funktionen-in-datenstrukturen-speichern) |

---

## Überblick

In Python sind Funktionen vollwertige Objekte, just wie Zahlen oder Strings. Man kann sie in Variablen speichern, zurückgeben und in Datenstrukturen ablegen.

---

## 1. Funktion einer Variable zuweisen

Man kann einfach eine Funktion einer Variablen zuweisen und dann über diese Variable aufrufen.

```python
# Lambda in einer Variable speichern
greet = lambda name: f"Hallo, {name}!"

# Über die Variable aufrufen
print(greet("Anna"))  # Hallo, Anna!
```

### Benannte Funktion zuweisen

Bestehende Funktionen können direkt als Wert zugewiesen werden:

```python
# Methodenreferenz statt Lambda
to_upper = str.upper

print(to_upper("hallo"))  # HALLO
```

### Verschiedene Funktionstypen

```python
# Einfache Berechnung
double_it = lambda x: x * 2
print(double_it(5))  # 10

# Predicate: gibt boolean zurück
is_even = lambda x: x % 2 == 0
print(is_even(4))  # True
print(is_even(7))  # False

# Funktion, die nichts zurückgibt
printer = print
printer("Hallo Welt")  # Hallo Welt
```

---

## 2. Funktion als Rückgabewert

Eine Funktion kann eine andere Funktion zurückgeben. Das ermöglicht es, Funktionen dynamisch zu erzeugen.

```python
# Gibt eine Funktion zurück, die mit dem gegebenen Faktor multipliziert
def create_multiplier(factor: int):
    return lambda x: x * factor

# Neue Funktionen erzeugen
double_it = create_multiplier(2)
triple_it = create_multiplier(3)

print(double_it(5))   # 10
print(triple_it(5))   # 15
print(double_it(10))  # 20
```

### Weiteres Beispiel: Begrüssung mit Präfix

```python
def create_greeter(prefix: str):
    return lambda name: f"{prefix} {name}!"

formal = create_greeter("Guten Tag,")
casual = create_greeter("Hey")

print(formal("Herr Müller"))  # Guten Tag, Herr Müller!
print(casual("Max"))           # Hey Max!
```

---

## 3. Funktionen in Datenstrukturen speichern

Man kann Funktionen in Listen oder Dictionaries ablegen und gezielt abrufen.

### In einer Liste

```python
# Operationen mit Namen als Tuple speichern
operations = [
    ("add",      lambda a, b: a + b),
    ("subtract", lambda a, b: a - b),
    ("multiply", lambda a, b: a * b)
]

for name, fn in operations:
    result = fn(10, 3)
    print(f"{name}(10, 3) = {result}")
# add(10, 3) = 13
# subtract(10, 3) = 7
# multiply(10, 3) = 30
```

### In einem Dictionary

```python
# Temperatur-Konverter in einem Dictionary
converters = {
    "fahrenheit": lambda c: c * 9 / 5 + 32,
    "kelvin":     lambda c: c + 273.15
}

# Gezielt abrufen und aufrufen
unit = "kelvin"
convert = converters[unit]
print(f"25°C in {unit}: {convert(25.0)}")
# 25°C in kelvin: 298.15

unit = "fahrenheit"
convert = converters[unit]
print(f"25°C in {unit}: {convert(25.0)}")
# 25°C in fahrenheit: 77.0
```

Das Dictionary-Pattern ist besonders nützlich, um `if/else`-Ketten zu ersetzen:

```python
# Statt:
def convert(value: float, unit: str) -> float:
    if unit == "fahrenheit":
        return value * 9 / 5 + 32
    elif unit == "kelvin":
        return value + 273.15
    else:
        raise ValueError(f"Unbekannte Einheit: {unit}")

# Einfacher:
def convert(value: float, unit: str) -> float:
    return converters[unit](value)
```
