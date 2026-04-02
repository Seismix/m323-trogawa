---
title: "C3G_Python"
parent: "C - Umsetzung"
nav_order: 7
---

# C3G: Einfache Lambda-Ausdrücke schreiben

> *Ich kann einfache Lambda-Ausdrücke für Berechnungen und String-Operationen schreiben, mit bedingten Ausdrücken kombinieren und erklären, wann Lambdas sinnvoll sind.*

## Lernziele

| # | Lernziel | Beantwortet in |
|---|----------|----------------|
| 1 | Ich kann eine Lambda-Funktion schreiben, die eine einfache Berechnung durchführt (z.B. `lambda x: x ** 2`). | [1. Einzeilige Lambda-Funktion](#1-einzeilige-lambda-funktion) |
| 2 | Ich kann eine Lambda-Funktion schreiben, die eine String-Transformation durchführt (z.B. Grossbuchstaben-Konvertierung). | [2. Lambda mit String-Operation](#2-lambda-mit-string-operation) |
| 3 | Ich kann erklären, wann ein Lambda-Ausdruck sinnvoller ist als eine benannte Funktion und umgekehrt. | [3. Lambda vs. benannte Funktion](#3-lambda-vs-benannte-funktion) |
| 4 | Ich kann einen Lambda-Ausdruck mit einem ternären Operator schreiben. | [4. Lambda mit bedingtem Ausdruck](#4-lambda-mit-bedingtem-ausdruck) |

---

## Überblick

Ein **Lambda-Ausdruck** in Python ist eine kompakte Schreibweise für eine anonyme Funktion. Lambdas sind bestens für kurze, einmalige Operationen.

```python
# Syntax
lambda parameter: ausdruck
```

Lambdas eignen sich für kurze, einmalige Operationen. Für alles Komplexere sollte man eine benannte Funktion verwenden.

---

## 1. Einzeilige Lambda-Funktion

```python
# Lambda für einfache Berechnungen
square = lambda x: x * x
print(square(5))  # 25

double_it = lambda x: x * 2
print(double_it(7))  # 14

add_ten = lambda x: x + 10
print(add_ten(5))  # 15
```

Lambdas sind besonders praktisch, wenn sie direkt als Argument übergeben werden:

```python
numbers = [1, 2, 3, 4, 5]

# Lambda direkt in sorted() verwenden
descending = sorted(numbers, key=lambda x: -x)
print(descending)  # [5, 4, 3, 2, 1]
```

---

## 2. Lambda mit String-Operation

```python
# Grossbuchstaben
to_upper = lambda s: s.upper()
print(to_upper("hallo"))  # HALLO

# Oder direkt mit der Methode
to_upper2 = str.upper

# String umkehren
reverse = lambda s: s[::-1]
print(reverse("Hallo"))  # ollaH
```

### Anwendung: Liste von Namen normalisieren

```python
names = ["  alice ", "BOB", " Charlie"]

cleaned = [
    name.strip()[0].upper() + name.strip()[1:].lower()
    for name in names
]
print(cleaned)  # ['Alice', 'Bob', 'Charlie']
```

---

## 3. Lambda vs. benannte Funktion

| Kriterium | Lambda | Benannte Methode |
|-----------|--------|------------------|
| **Umfang** | Ein Ausdruck | Beliebig viele Zeilen |
| **Name** | Anonym | Sprechender Funktionsname |
| **Wiederverwendung** | Für einmaligen Gebrauch | Für mehrfachen Aufruf |
| **Lesbarkeit** | Kurze, offensichtliche Logik | Komplexe oder benannte Logik |
| **Debugging** | Stacktrace zeigt `<lambda>` | Stacktrace zeigt Funktionsnamen |

### Wann Lambda sinnvoll ist

```python
# Gut: kurze, einmalige Sortierlogik
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

students = [
    Student("Anna", 2.1),
    Student("Ben", 1.5),
    Student("Clara", 1.8)
]
sorted_students = sorted(students, key=lambda s: s.grade)
```

### Wann eine benannte Methode besser ist

```python
# Schlecht: Lambda zu komplex, schwer zu lesen
process = lambda x: (
    x.strip().lower().replace(" ", "_")
    if isinstance(x, str)
    else str(x)
)

# Besser: benannte Funktion
def normalize_value(x):
    if isinstance(x, str):
        return x.strip().lower().replace(" ", "_")
    return str(x)
```

**Faustregel:** Wenn die Lambda-Logik nicht auf einen Blick verständlich ist, sollte man eine benannte Funktion verwenden.

---

## 4. Lambda mit bedingtem Ausdruck

Der ternäre Operator (`bedingung if wahrbedingung else wertfallsfaelsch`) kann direkt in einem Lambda verwendet werden.

```python
# Gerade oder ungerade?
parity = lambda x: "gerade" if x % 2 == 0 else "ungerade"
print(parity(4))  # gerade
print(parity(7))  # ungerade

# Positiv, negativ oder null?
sign = lambda x: "positiv" if x > 0 else ("null" if x == 0 else "negativ")
print(sign(5))   # positiv
print(sign(0))   # null
print(sign(-3))  # negativ

# Praktisches Beispiel: Rabatt berechnen
discount = lambda price: price * 0.9 if price > 100 else price
print(discount(150.0))  # 135.0
print(discount(80.0))   # 80.0
```

### Anwendung in map()

```python
temperatures = [35, 28, 42, 15, 38]

warnings = list(map(
    lambda t: f"{t}°C: {'WARNUNG' if t > 35 else 'OK'}",
    temperatures
))
print(warnings)
# ['35°C: OK', '28°C: OK', '42°C: WARNUNG', '15°C: OK', '38°C: WARNUNG']
```
