---
title: "BG2"
parent: "B - Anforderungen & Design"
nav_order: 4
---

# BG2: Elemente des Functional Design erklären

> *Ich kann Elemente des Functional Design erklären. (z.Bsp. Immutable data types, model, solution, domain of interest, constructors, composable operators)*

## Lernziele

| # | Lernziel | Beantwortet in |
| --- | ---------- | -------------- |
| 1 | Ich kann die Kernelemente des Functional Design (Immutable Data Types, Model, Solution, Domain of Interest) benennen und jeweils in einem Satz erklären. | [1. Grundelemente des Functional Design](#1-grundelemente-des-functional-design) |
| 2 | Ich kann erklären, was Constructors und Composable Operators im Kontext des Functional Design sind. | [2. Constructors und Composable Operators](#2-constructors-und-composable-operators) |
| 3 | Ich kann an einem einfachen Beispiel zeigen, wie die Elemente des Functional Design zusammenwirken. | [3. Zusammenspiel der Elemente](#3-zusammenspiel-der-elemente) |

---

## 1. Grundelemente des Functional Design

| Element | Erklärung | Praktisches Beispiel |
| ------- | --------- | -------- |
| **Domain of Interest** | Das Fachgebiet oder die Problemdomäne, die die Anwendung modellieren soll | Kontoführung mit Konzepten wie Konto, Transaktion, Kontostand |
| **Model** | Die abstrakte Repräsentation dieser Domäne mit definierten Datenstrukturen und Funktionen | `@dataclass(frozen=True) class Booking: desc: str, amount: float, date: date` |
| **Solution** | Die praktische Implementierung, welche das Model zur konkreten Problemlösung einsetzt | Eine Verarbeitungs-Pipeline, die Buchungen eines bestimmten Monats aufsummiert |
| **Immutable Data Types** | Strukturen, die nach ihrer Erzeugung nicht mehr geändert werden können | Python Strings, Tuples, `frozenset`, gefrorene Dataclasses |

### Immutable Data Types in Python

```python
from dataclasses import dataclass

# Dataclass mit frozen=True ist unveränderbar (immutable)
@dataclass(frozen=True)
class Product:
    name: str
    price: float

apple = Product("Apfel", 1.50)
# apple.name = "Birne"  # FrozenInstanceError bekommt man hier

# Unveränderbares Tuple (einfache Listenvariante)
items = ("A", "B", "C")
# items.append("D")  # AttributeError: 'tuple' Objekt hat kein append Attribut
```

Anstatt bestehendes zu überschreiben, wird einfach eine geänderte Kopie erstellt:

```python
from dataclasses import replace

expensive_apple = replace(apple, price=apple.price + 0.50)
# Product(name='Apfel', price=2.0)
```

---

## 2. Constructors und Composable Operators

**Constructors** bilden die Schnittstelle zur Erzeugung korrekter, gültiger Datenobjekte. In Python nutzt man hierfür oft Klassenmethoden oder dedizierte Factory-Funktionen:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Temperature:
    celsius: float

    @classmethod
    def from_celsius(cls, c: float):
        return cls(c)

    @classmethod
    def from_fahrenheit(cls, f: float):
        return cls((f - 32) * 5.0 / 9.0)

t1 = Temperature.from_celsius(25.0)
t2 = Temperature.from_fahrenheit(77.0)
```

**Composable Operators** sind spezialisierte Funktionen, die kettenartig zusammengefügt werden (Operator A liefert Daten an Operator B):

```python
from datetime import date

bookings = [
    {"desc": "Miete", "amount": -1200.0, "date": date(2024, 3, 1)},
    {"desc": "Lohn", "amount": 4500.0, "date": date(2024, 3, 5)},
    {"desc": "Essen", "amount": -350.0, "date": date(2024, 3, 10)},
    {"desc": "Lohn", "amount": 4500.0, "date": date(2024, 4, 5)}
]

# Operatorkette durch Comprehensions und built-in Funktionen
march_bookings = [b for b in bookings if b["date"].month == 3]  # Operator 1: Filtern
march_amounts = [b["amount"] for b in march_bookings]             # Operator 2: Extrahieren
march_total = sum(march_amounts)                                  # Operator 3: Summieren
# 2950.0
```

Die Originalstruktur wird in allen Schritten unverändert gelassen. Jeder Operator erzeugt nur neue Daten (keine Seiteneffekte).

---

## 3. Zusammenspiel der Elemente

Ein umfassendes Beispiel mit einer Todo-Verwaltung verdeutlicht, wie alle Komponenten zusammenspielen:

```python
from dataclasses import dataclass, replace

# Immutable Data Type
@dataclass(frozen=True)
class Todo:
    id: int
    title: str
    done: bool

# Constructor
def create_todo(id: int, title: str) -> Todo:
    return Todo(id, title, False)

# Composable Operators (erzeugen immer frische Strukturen)
def add_todo(todos: tuple, todo: Todo) -> tuple:
    return todos + (todo,)

def complete_todo(todos: tuple, target_id: int) -> tuple:
    return tuple(
        replace(t, done=True) if t.id == target_id else t
        for t in todos
    )

def filter_open(todos: tuple) -> tuple:
    return tuple(t for t in todos if not t.done)
```

**Verwendung (Solution):**

```python
todos = ()
todos = add_todo(todos, create_todo(1, "Einkaufen"))
todos = add_todo(todos, create_todo(2, "Lernen"))
todos = complete_todo(todos, 1)

open_todos = filter_open(todos)
# (Todo(id=2, title='Lernen', done=False),)
```

| Element | Umsetzung im Beispiel |
| ------- | ----------- |
| Domain of Interest | Todo-Listen-Management |
| Immutable Data Type | `@dataclass(frozen=True) class Todo(...)` |
| Constructor | `create_todo(id, title)` |
| Composable Operators | `add_todo`, `complete_todo`, `filter_open` |        
| Model | Die Kombination aus Datentyp und Operatoren |     
| Solution | Die Ausführungslogik unten (`todos = () ...`) |
