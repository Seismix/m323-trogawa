---
title: "DG1"
parent: "D - Refactoring & Optimierung"
nav_order: 1
---

# DG1: Refactoring-Techniken aufzählen

> *Ich kann einige Refactoring-Techniken aufzählen, die einen Code lesbarer und verständlicher machen.*

## Lernziele

| # | Lernziel | Beantwortet in |
|---|----------|----------------|
| 1 | Ich kann mindestens 3 Refactoring-Techniken benennen. | [Gängige Refactoring-Techniken](#gängige-refactoring-techniken) (7 Techniken) |
| 2 | Ich kann für jede Technik erklären, welches Problem sie löst und wie sie die Lesbarkeit verbessert. | **Problem** und **Wie es die Lesbarkeit verbessert** bei jeder Technik |
| 3 | Ich kann in gegebenem Code typische Code Smells identifizieren, die auf Refactoring-Bedarf hinweisen. | [Code Smells](#code-smells-wann-braucht-es-refactoring) |

---

## Was ist Refactoring?

Refactoring ist die Umstrukturierung von bestehendem Code, **ohne dessen Verhalten zu ändern**. Das Ziel ist es, den Code lesbarer, wartbarer und verständlicher zu machen.

---

## Gängige Refactoring-Techniken

### 1. Extract Function

**Problem:** Eine Funktion ist zu lang und macht mehrere Dinge gleichzeitig. Man muss den gesamten Code lesen, um zu verstehen, was passiert.

**Wie es die Lesbarkeit verbessert:** Jeder Codeblock bekommt einen sprechenden Funktionsnamen. Die Hauptfunktion liest sich danach wie eine Zusammenfassung.

```python
# Vorher
def process_order(order):
    # Preis berechnen
    total = 0
    for item in order["items"]:
        total += item["price"] * item["quantity"]
    if order["discount"]:
        total *= 0.9
    # Rechnung drucken
    print(f"Kunde: {order['customer']}")
    print(f"Total: {total}")

# Nachher
def calculate_total(items, has_discount):
    total = sum(item["price"] * item["quantity"] for item in items)
    return total * 0.9 if has_discount else total

def print_invoice(customer, total):
    print(f"Kunde: {customer}")
    print(f"Total: {total}")

def process_order(order):
    total = calculate_total(order["items"], order["discount"])
    print_invoice(order["customer"], total)
```

### 2. Rename Variable / Rename Function

**Problem:** Variablen und Funktionen haben nichtssagende Namen wie `x`, `tmp`, `calc`. Man muss den umliegenden Code lesen, um zu verstehen, was sie bedeuten.

**Wie es die Lesbarkeit verbessert:** Der Name allein verrät den Zweck. Code wird selbstdokumentierend.

```python
# Vorher
def calc(x, y, z):
    return x * y - z

# Nachher
def calculate_net_price(unit_price, quantity, discount):
    return unit_price * quantity - discount
```

### 3. Inline Function

**Problem:** Eine triviale Funktion, die nur einmal aufgerufen wird, erzeugt unnötige Indirektion. Man muss zur Funktionsdefinition springen, nur um eine Zeile zu lesen.

**Wie es die Lesbarkeit verbessert:** Der Code ist direkt sichtbar, ohne Sprünge. Weniger Abstraktionsebenen.

```python
# Vorher
def is_adult(age):
    return age >= 18

def can_vote(person):
    return is_adult(person["age"])

# Nachher
def can_vote(person):
    return person["age"] >= 18
```

### 4. Remove Dead Code

**Problem:** Auskommentierter oder unerreichbarer Code lenkt ab und suggeriert, dass er noch relevant ist. Entwickler trauen sich nicht, ihn zu löschen, weil unklar ist, ob er gebraucht wird.

**Wie es die Lesbarkeit verbessert:** Weniger Code bedeutet weniger zu lesen. Alles, was im File steht, ist auch tatsächlich relevant.

```python
# Vorher
def get_status(code):
    if code == 200:
        return "OK"
    elif code == 404:
        return "Not Found"
    # Diese Zeile wird nie erreicht, wenn alle Codes abgedeckt sind
    # old_status = legacy_lookup(code)
    return "Unknown"
```

### 5. Simplify Conditional

**Problem:** Verschachtelte oder lange `if`-Bedingungen sind schwer zu lesen. Man muss mehrere Teilbedingungen im Kopf behalten, um den Gesamtausdruck zu verstehen.

**Wie es die Lesbarkeit verbessert:** Die Bedingung bekommt einen sprechenden Namen (`is_eligible`). Die Geschäftslogik wird auf einen Blick klar.

```python
# Vorher
if user.age >= 18 and user.has_id and not user.is_banned and user.email_verified:
    grant_access(user)

# Nachher
def is_eligible(user):
    return (user.age >= 18
            and user.has_id
            and not user.is_banned
            and user.email_verified)

if is_eligible(user):
    grant_access(user)
```

### 6. Replace Magic Number with Named Constant

**Problem:** Zahlen wie `120` oder `0.85` im Code haben keine erkennbare Bedeutung. Man muss raten oder den Kontext studieren, um zu verstehen, wofür sie stehen.

**Wie es die Lesbarkeit verbessert:** `MAX_SPEED_LIMIT` ist sofort verständlich. Ausserdem muss der Wert nur an einer Stelle geändert werden.

```python
# Vorher
if speed > 120:
    issue_ticket()

# Nachher
MAX_SPEED_LIMIT = 120

if speed > MAX_SPEED_LIMIT:
    issue_ticket()
```

### 7. Introduce Explaining Variable

**Problem:** Ein komplexer Ausdruck in einer `if`-Bedingung oder Berechnung ist schwer zu parsen. Man muss ihn mental zerlegen, um zu verstehen, was geprüft wird.

**Wie es die Lesbarkeit verbessert:** Jeder Teilausdruck bekommt einen Namen, der seine Bedeutung erklärt. Die Bedingung liest sich danach wie natürliche Sprache.

```python
# Vorher
if order.total() > 100 and order.customer.loyalty_years > 2:
    apply_discount(order)

# Nachher
is_large_order = order.total() > 100
is_loyal_customer = order.customer.loyalty_years > 2

if is_large_order and is_loyal_customer:
    apply_discount(order)
```

---

## Code Smells: Wann braucht es Refactoring?

| Code Smell | Beschreibung | Passende Technik |
|------------|-------------|-----------------|
| **Long Method** | Funktion ist zu lang (>20 Zeilen) | Extract Function |
| **Magic Numbers** | Zahlen ohne Kontext im Code | Named Constant |
| **Duplicated Code** | Gleicher Code an mehreren Stellen | Extract Function |
| **Dead Code** | Unerreichbarer/unbenutzter Code | Remove Dead Code |
| **Poor Naming** | Variablen wie `x`, `tmp`, `data` | Rename Variable |
| **Complex Conditional** | Verschachtelte if/else-Ketten | Simplify Conditional |
| **Long Parameter List** | Funktion mit zu vielen Parametern | Introduce Parameter Object |
