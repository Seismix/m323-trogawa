---
title: "DG1_Python"
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

## Was bedeutet Refactoring?

Unter Refactoring versteht man das Überarbeiten und Säubern von bestehendem Quellcode, **ohne dass sich dabei das äusserliche Verhalten oder die Funktionalität des Programms verändert**. Der Hauptzweck besteht darin, den Code übersichtlicher, wartungsfreundlicher und intuitiver zu gestalten.

---

## Gängige Refactoring-Techniken

### 1. Funktion auslagern (Extract Function)

**Problem:** Eine Methode ist völlig überladen und übernimmt zu viele Aufgaben auf einmal. Man ist gezwungen, den gesamten Code-Block zu durchlesen, um den Sinn dahinter zu verstehen.

**Wie es die Lesbarkeit verbessert:** Einzelne Logik-Bausteine erhalten eigene, aussagekräftige Namen. Dadurch liest sich die Hauptmethode fast wie ein Inhaltsverzeichnis.

```python
# Vorher
def process_order(order):
    # Summe berechnen
    total_amount = 0
    for item in order["items"]:
        total_amount += item["price"] * item["quantity"]
    if order["has_discount"]:
        total_amount *= 0.9
        
    # Rechnung anzeigen
    print(f"Kundenname: {order['customer']}")
    print(f"Rechnungsbetrag: {total_amount}")

# Nachher
def calculate_order_total(items, discount_applied):
    base_total = sum(item["price"] * item["quantity"] for item in items)
    return base_total * 0.9 if discount_applied else base_total

def print_receipt(customer_name, amount):
    print(f"Kundenname: {customer_name}")
    print(f"Rechnungsbetrag: {amount}")

def process_order(order):
    total_amount = calculate_order_total(order["items"], order["has_discount"])
    print_receipt(order["customer"], total_amount)
```

### 2. Umbenennen (Rename Variable / Rename Function)

**Problem:** Variablen und Funktionen tragen kryptische oder generische Namen wie `a`, `temp_val`, `do_stuff`. Ohne den Kontext mühsam zu analysieren, weiss man nicht, wofür sie existieren.

**Wie es die Lesbarkeit verbessert:** Ein guter Name erklärt bereits die Absicht. Der Code erklärt sich dadurch grösstenteils von selbst.

```python
# Vorher
def compute(x, y, z):
    return x * y - z

# Nachher
def calculate_net_price(unit_price, quantity, discount_amount):
    return unit_price * quantity - discount_amount
```

### 3. Funktion integrieren (Inline Function)

**Problem:** Eine extrem simple Methode, die sowieso nur an einer einzigen Stelle genutzt wird, sorgt für unnötiges Hin- und Herspringen im Code (Indirektion).

**Wie es die Lesbarkeit verbessert:** Der Code steht genau dort, wo er gebraucht wird. Überflüssige Verschachtelungen werden abgebaut.

```python
# Vorher
def is_of_age(age):
    return age >= 18

def can_vote(person):
    return is_of_age(person["age"])

# Nachher
def can_vote(person):
    return person["age"] >= 18
```

### 4. Toten Code entfernen (Remove Dead Code)

**Problem:** Auskommentierte Code-Blöcke oder Passagen, die niemals ausgeführt werden, stiften Verwirrung. Oft getrauen sich Entwickler nicht, diese Zeilen zu löschen, aus Angst, sie könnten noch wichtig sein.

**Wie es die Lesbarkeit verbessert:** Weniger Altlasten im File bedeuten eine aufgeräumtere Arbeitsumgebung. Was da ist, wird auch genutzt.

```python
# Vorher
def get_http_status(code):
    if code == 200:
        return "OK"
    elif code == 404:
        return "Not Found"
        
    # Dieser Codeblock wird nicht mehr gebraucht
    # fallback_status = check_legacy_system(code)
    # return fallback_status
    
    return "Unknown Error"
```

### 5. Bedingungen vereinfachen (Simplify Conditional)

**Problem:** Riesige oder komplex verschachtelte `if`-Konstrukte sind extrem anstrengend zu lesen. Man muss sich viele logische Zwischenschritte gleichzeitig merken.

**Wie es die Lesbarkeit verbessert:** Die komplette Bedingung wird in eine eigene Logik extrahiert und benannt (`is_access_granted`). Das "Warum" einer Abfrage wird sofort klar.

```python
# Vorher
if user.age >= 18 and user.has_active_id and not user.is_banned and user.email_is_verified:
    grant_system_access(user)

# Nachher
def is_eligible_for_access(user):
    return (user.age >= 18
            and user.has_active_id
            and not user.is_banned
            and user.email_is_verified)

if is_eligible_for_access(user):
    grant_system_access(user)
```

### 6. Magische Zahlen ersetzen (Replace Magic Number with Named Constant)

**Problem:** Zahlenwerte wie `3.1415` oder `120` stehen isoliert im Code. Niemand weiss intuitiv, was diese Werte repräsentieren.

**Wie es die Lesbarkeit verbessert:** Durch Konstanten wie `MAX_SPEED_LIMIT` weiss jeder sofort Bescheid. Zudem muss der Wert bei Änderungen nur an einer einzigen Stelle im ganzen File angepasst werden.

```python
# Vorher
if speed > 120:
    issue_speeding_ticket()

# Nachher
MAX_SPEED_LIMIT = 120

if speed > MAX_SPEED_LIMIT:
    issue_speeding_ticket()
```

### 7. Erklärende Variable einführen (Introduce Explaining Variable)

**Problem:** Eine lange mathematische Formel oder eine dicke `if`-Bedingung ist zu verschachtelt. Man muss die Teilstücke erst mental entwirren.

**Wie es die Lesbarkeit verbessert:** Komplizierte Teil-Aussagen werden in sinnvoll benannten Zwischenvariablen gespeichert. Dadurch liest sich die eigentliche Logik danach fast wie ein umgangssprachlicher Satz.

```python
# Vorher
if order.get_total() > 100 and order.customer.loyalty_years > 2:
    apply_special_discount(order)

# Nachher
is_large_order = order.get_total() > 100
is_loyal_customer = order.customer.loyalty_years > 2

if is_large_order and is_loyal_customer:
    apply_special_discount(order)
```

---

## Code Smells: Wann ist Refactoring nötig?

| Code Smell | Beschreibung | Lösungsansatz (Technik) |
|------------|-------------|-----------------|
| **Long Method** | Die Methode umfasst zu viele Zeilen (>20) | Extract Function |
| **Magic Numbers** | Harte Zahlenwerte ohne Kontext | Named Constant |
| **Duplicated Code** | Exakt identische Logik-Schnipsel an mehreren Orten | Extract Function |
| **Dead Code** | Bereiche, die nie erreicht werden | Remove Dead Code |
| **Poor Naming** | Nichtssagende Namen wie `x`, `tmp`, `data` | Rename Variable |
| **Complex Conditional** | Bandwurmartige if/else-Verschachtelungen | Simplify Conditional |
| **Long Parameter List** | Eine Funktion verlangt viel zu viele Argumente | Introduce Parameter Object |