---
title: "AG1"
parent: "A - Paradigmen"
nav_order: 1
---

# AG1: Eigenschaften von Funktionen beschreiben

> *Ich kann die Eigenschaften von Funktionen beschreiben (z.Bsp. pure function) und den Unterschied zu anderen Programmier-Strukturen erläutern (z.Bsp. zu Prozedur).*

## Lernziele

| # | Lernziel | Beantwortet in |
|---|----------|----------------|
| 1 | Ich kann erklären, was eine Pure Function ist und welche zwei Eigenschaften sie erfüllen muss. | Was ist eine Pure Function? |
| 2 | Ich kann den Unterschied zwischen einer Funktion und einer Prozedur anhand von Codebeispielen erläutern. | Funktion vs. Prozedur |
| 3 | Ich kann in gegebenem Code erkennen, ob eine Funktion pure ist, und meine Einschätzung begründen. | Seiteneffekte erkennen |

---

## Was ist eine Pure Function?

Eine Pure Function zeichnet sich durch **zwei Hauptmerkmale** aus, die beide erfüllt sein müssen:

| Merkmal | Erklärung | Beispiel |
|-------------|-------------|----------|
| **Kalkulierbarkeit (Determinismus)** | Ein bestimmter Startwert (Input) liefert stets das identische Resultat (Output). | `double(3)` ist immer `6` |
| **Frei von Seiteneffekten** | Die Ausführung der Funktion hat keinerlei Auswirkungen auf den äusseren Zustand. | Weder `print()`, noch globale Variablen werden genutzt oder Dateien verändert. |

```python
# Pure Function: gleicher Input, identischer Output, keine externen Auswirkungen
def double(x):
    return x * 2

double(3) # => 6 (immer)
double(3) # => 6 (immer)
```

```python
# NICHT pure: modifiziert den externen Zustand, das Resultat ändert sich trotz gleichem Parameter
class Counter:
    def __init__(self):
        self.total = 0

    def add_to_total(self, x):
        self.total += x
        return self.total

counter = Counter()
counter.add_to_total(3) # => 3
counter.add_to_total(3) # => 6 (gleicher Aufruf, aber anderes Resultat!)
```

Die Methode `add_to_total` erfüllt keines der beiden Kriterien: Sie bewirkt einen Seiteneffekt durch die Änderung von `total` und liefert für die wiederholte Eingabe von `3` unterschiedliche Werte.

---

## Funktion vs. Prozedur

Beim Programmieren wird häufig zwischen **Funktionen** und **Prozeduren** unterschieden:

| | Funktion | Prozedur |
|---|---------|----------|
| **Resultat** | Liefert etwas zurück | Kein Rückgabewert (gibt in Python `None` zurück) |
| **Seiteneffekte** | Besitzt im Idealfall keine | Wird oft explizit für Seiteneffekte genutzt |
| **Sinn und Zweck** | Einen Wert berechnen | Einen Vorgang ausführen |
| **Beispiel** | `len("hello")` ergibt `5` | `print("hello")` schreibt etwas auf die Konsole |

```python
# Funktion: nimmt Parameter entgegen, errechnet Resultat
def calculate_area(width, height):
    return width * height

result = calculate_area(5, 3) # => 15

# Prozedur: macht etwas direkt, liefert nichts Nützliches zurück
def display_area(width, height):
    print(f"Die Fläche beträgt {width * height} m²")

display_area(5, 3) # Konsolenausgabe, liefert None
```

In Python lässt sich dieser Unterschied vor allem am Umgang mit dem Resultat feststellen: Echte Funktionen nutzen das Keyword `return`, bei Prozeduren entfällt es (wodurch implizit `None` zurückgegeben wird).

---

## Seiteneffekte erkennen

Als **Seiteneffekt** (Side Effect) bezeichnet man jede Zustandsänderung, die eine Methode ausserhalb ihres lokalen Gültigkeitsbereichs verursacht:

- Modifikation von Feldern oder globalen Werten
- Konsolen-Ausgaben wie `print()`
- Datenbank- oder Dateizugriffe
- Senden von Netzwerk-Requests

### Beispiel: Welche Methode gilt als pure?

```python
class Example:
    x = 0

    @staticmethod
    def a(n):
        return n + 1

    @classmethod
    def b(cls, n):
        cls.x += n
        return cls.x

    @staticmethod
    def c(n):
        print(n)
        return n
```

| Methode | Pure? | Erklärung |
|---------|-------|------------|
| `a(n)` | Ja | Bei gleicher Eingabe kommt das gleiche Resultat heraus, ohne Nebenwirkungen. |
| `b(n)` | Nein | Modifiziert `x` in der Klasse. Bei identischem Input variieren die Ausgaben (`b(1)` ergibt am Anfang `1`, gefolgt von `2`, und darauf `3` etc.). |
| `c(n)` | Nein | Der Aufruf von `print()` löst eine sichtbare Nebenwirkung auf der Konsole aus. |

### Warum versucht funktionale Programmierung Seiteneffekte zu minimieren?

| Argument | Details |
|---------|-----------|
| **Verlässlichkeit** | Das Verhalten von Pure Functions ist unabhängig vom restlichen Programm stets konstant. |
| **Testfreundlichkeit** | Für Unittests müssen keine globalen Zustände bereitgestellt werden. |
| **Nebenläufigkeit** | Ohne das Teilen von Zustand können Funktionen problemlos auf mehreren Cores gleichzeitig (parallel) ausgeführt werden. |
