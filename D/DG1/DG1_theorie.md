---
title: DG1 — Refactoring-Techniken aufzählen
parent: Home
nav_order: 10
---

# DG1 — Refactoring-Techniken aufzählen

> *Ich kann einige Refactoring-Techniken aufzählen, die einen Code lesbarer und verständlicher machen.*

## Was ist Refactoring?

Refactoring ist die Umstrukturierung von bestehendem Code, **ohne dessen Verhalten zu ändern**. Das Ziel ist es, den Code lesbarer, wartbarer und verständlicher zu machen.

---

## Gängige Refactoring-Techniken

### 1. Extract Function

Ein langer Codeblock wird in eine benannte Funktion ausgelagert.

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

Unklare Namen werden durch aussagekräftige ersetzt.

```python
# Vorher
def calc(x, y, z):
    return x * y - z

# Nachher
def calculate_net_price(unit_price, quantity, discount):
    return unit_price * quantity - discount
```

### 3. Inline Function

Eine Funktion, die nur einmal aufgerufen wird und trivial ist, wird direkt eingesetzt.

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

Nicht erreichbarer oder nicht verwendeter Code wird entfernt.

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

Komplexe Bedingungen werden vereinfacht oder in Funktionen ausgelagert.

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

Unbenannte Zahlenwerte werden durch Konstanten ersetzt.

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

Ein komplexer Ausdruck wird in eine Variable mit erklärendem Namen gespeichert.

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

## Code Smells — Wann braucht es Refactoring?

| Code Smell | Beschreibung | Passende Technik |
|------------|-------------|-----------------|
| **Long Method** | Funktion ist zu lang (>20 Zeilen) | Extract Function |
| **Magic Numbers** | Zahlen ohne Kontext im Code | Named Constant |
| **Duplicated Code** | Gleicher Code an mehreren Stellen | Extract Function |
| **Dead Code** | Unerreichbarer/unbenutzter Code | Remove Dead Code |
| **Poor Naming** | Variablen wie `x`, `tmp`, `data` | Rename Variable |
| **Complex Conditional** | Verschachtelte if/else-Ketten | Simplify Conditional |
| **Long Parameter List** | Funktion mit zu vielen Parametern | Introduce Parameter Object |
