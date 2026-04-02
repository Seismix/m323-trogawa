---
title: "AF1_Python"
parent: "A - Paradigmen"
nav_order: 2
---

# AF1: Immutable Values erläutern

> *Ich kann das Konzept von immutable values erläutern und dazu Beispiele anwenden. Somit kann ich dieses Konzept funktionaler Programmierung im Unterschied zu anderen Programmiersprachen erklären (z.Bsp. im Vergleich zu referenzierten Objekten).*

## Lernziele

| # | Lernziel | Beantwortet in |
|---|----------|----------------|
| 1 | Ich kann erklären, was Immutability bedeutet, und an einem Python-Beispiel zeigen, wie immutable Werte funktionieren. | [Was ist Immutability?](#was-ist-immutability) |
| 2 | Ich kann anhand eines Codebeispiels erklären, warum referenzierte Objekte in Python problematisch sein können und wie Immutability dieses Problem löst. | [Das Aliasing-Problem](#das-aliasing-problem) |
| 3 | Ich kann in gegebenem Code erkennen, ob eine Mutation vorliegt, und die funktionale Alternative zeigen. | [Das Aliasing-Problem](#das-aliasing-problem) |

---

## Was ist Immutability?

**Immutability** bedeutet, dass ein Wert nach seiner Erstellung **nicht mehr verändert** werden kann. Statt einen bestehenden Wert zu ändern, erstellt man einen neuen.

### Immutability in Python

Python bietet mehrere immutable Typen:

| Typ | Beschreibung | Beispiel |
|-----|------------|----------|
| **tuple** | Unveränderbare Liste | `(1, 2, 3)` |
| **frozenset** | Unveränderbare Menge | `frozenset([1, 2, 3])` |
| **str** | Strings sind immer immutable | `"hello".upper()` erzeugt einen neuen String |
| **Zahltypen** | int, float sind immutable | `x = 5` kann nicht verändert werden |

### Beispiel: tuple vs. list

```python
# Immutable: tuple hat keine Änderungsmethoden
items = (1, 2, 3)
# items[0] = 99  # TypeError! Kann nicht verändert werden.

# Mutable: list kann verändert werden
items = [1, 2, 3]
items[0] = 99  # Erlaubt, aber potentiell gefährlich: das Original wird verändert.
```

Bei einem `tuple` erzwingt Python die Unveränderlichkeit. Man kann das Objekt nach der Erstellung nicht mehr verändern.

### Unveränderbare Collections

```python
# Immutable: tuple("...") erzeugt einen neuen String
text = "hello"
text_neu = text.upper()
print(text)      # "hello" - Original unverändert
print(text_neu)  # "HELLO"

# List mit Kopie arbeiten statt zu mutieren
numbers = [1, 2, 3]
more_numbers = numbers + [4]  # Neue Liste statt Mutation
print(numbers)      # [1, 2, 3]
print(more_numbers) # [1, 2, 3, 4]
```

---

## Mutable vs. Immutable in Python

| Mutable (veränderbar) | Immutable (unveränderbar) |
|----------------------|--------------------------|
| `list` | `tuple` |
| `dict` | `frozenset` |
| `set` | `str` |

### Vergleich im Code

```python
# Mutable: Liste wird direkt verändert
numbers = [1, 2, 3]
numbers.append(4)       # numbers ist jetzt [1, 2, 3, 4]
print(numbers) # => [1, 2, 3, 4]

# Immutable: String kann nicht verändert werden
text = "hello"
text_upper = text.upper() # Erstellt einen neuen String
print(text)         # => "hello" (Original unverändert)
print(text_upper)   # => "HELLO"
```

### Vorteile von Immutability

| Vorteil | Erklärung |
|---------|-----------|
| **Vorhersagbarkeit** | Wenn sich Werte nie ändern, gibt es keine Überraschungen. |
| **Thread-Sicherheit** | Unveränderbare Daten können ohne Locks parallel gelesen werden. |
| **Einfacheres Debugging** | Man muss nicht suchen, wo ein Wert ungewollt geändert wurde. |
| **Performance** | Unveränderbare Objekte können einfacher optimiert werden. |

---

## Das Aliasing-Problem

In Python zeigen Variablen auf **dasselbe Objekt im Speicher** (Referenzsemantik). Wenn mehrere Variablen auf dasselbe Objekt zeigen, kann eine Änderung über eine Variable alle anderen unbeabsichtigt beeinflussen.

### Das Problem in Aktion

```python
original = [1, 2, 3]
copy = original  # Keine echte Kopie, nur eine zweite Referenz!

copy.append(4)

print(original) # => [1, 2, 3, 4]  (unbeabsichtigt verändert!)
print(copy)     # => [1, 2, 3, 4]
```

Beide Variablen zeigen auf **dieselbe** Liste. Eine Änderung über `copy` betrifft auch `original`.

### Konkretes Beispiel: Warenkorb

```python
# Problematisch: verändert die originale Liste
def add_item(cart: list, item: str) -> list:
    cart.append(item)
    return cart

warenkorb = ["Brot", "Milch"]
neuer_warenkorb = add_item(warenkorb, "Käse")

print(warenkorb)       # => ["Brot", "Milch", "Käse"]  (ungewollt verändert!)
print(neuer_warenkorb) # => ["Brot", "Milch", "Käse"]
```

### Funktionale Lösung mit Immutability

```python
# Funktional: erstellt eine neue Liste, Original bleibt unverändert
def add_item(cart: list, item: str) -> list:
    return cart + [item]

warenkorb = ["Brot", "Milch"]
neuer_warenkorb = add_item(warenkorb, "Käse")

print(warenkorb)       # => ["Brot", "Milch"]  (unverändert!)
print(neuer_warenkorb) # => ["Brot", "Milch", "Käse"]
```

`cart + [item]` erzeugt eine **neue**, unveränderbare Liste. Das Original bleibt unangetastet. Genau das ist das Prinzip der funktionalen Programmierung: statt Daten zu verändern, neue Werte erzeugen. In Python wird dieses Prinzip durch `tuple`, `frozenset` und unveränderbare String-Operationen unterstützt.
