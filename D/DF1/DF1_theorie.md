---
title: "DF1"
parent: "D - Refactoring & Optimierung"
nav_order: 2
---

# DF1: Refactoring-Techniken anwenden

> *Ich kann mit Refactoring-Techniken einen Code lesbarer und verständlicher machen.*

## Überblick

In dieser Kompetenz geht es darum, Refactoring nicht nur zu kennen, sondern **aktiv anzuwenden**. Die drei Kernfähigkeiten sind:

1. **Extract Function:** Lange Codeblöcke in benannte Funktionen auslagern
2. **Rename:** Variablen und Funktionen aussagekräftig benennen
3. **Duplikate entfernen:** Gemeinsamen Code in wiederverwendbare Funktionen extrahieren

| Technik | Vorher | Nachher |
|---------|--------|---------|
| Extract Function | Monolithische 50-Zeilen-Funktion | Mehrere kleine, fokussierte Funktionen |
| Rename | `calc(d, r)` | `calculate_discount(days_since_purchase, return_rate)` |
| Duplikate entfernen | Copy-Paste-Code an 3 Stellen | Eine gemeinsame Funktion |

---

## Beispiel: Bestellverarbeitung

### Vorher (unrefactored)

Dieser Code funktioniert, ist aber schwer zu lesen und zu warten:

```python
def proc(o):
    """Verarbeitet eine Bestellung - schlecht benannt, zu lang, dupliziert."""
    # Validierung (dupliziert für jeden Bestelltyp)
    if not o.get("customer"):
        print("Fehler: Kein Kunde")
        return None
    if not o.get("items"):
        print("Fehler: Keine Artikel")
        return None

    # Preisberechnung
    t = 0
    for i in o["items"]:
        p = i["price"]
        q = i["qty"]
        t += p * q
    # Rabatt
    if o.get("vip"):
        t = t * 0.85
    # MwSt
    t = t * 1.081

    # Rechnung ausgeben
    print(f"=== RECHNUNG ===")
    print(f"Kunde: {o['customer']}")
    for i in o["items"]:
        p = i["price"]
        q = i["qty"]
        print(f"  {i['name']}: {q}x CHF {p:.2f} = CHF {p * q:.2f}")
    print(f"Total: CHF {t:.2f}")
    return t
```

**Probleme:** Funktion heisst `proc`, Variablen heissen `t`, `p`, `q`, `i`. Validierung, Berechnung und Ausgabe sind in einer Funktion vermischt. Die Artikelausgabe ist dupliziert (einmal für Berechnung, einmal für Anzeige).

---

### Nachher (refactored)

#### Technik 1: Extract Function

Jede logische Einheit wird in eine eigene Funktion extrahiert:

```python
def validate_order(order: dict) -> bool:
    """Prüft, ob eine Bestellung gültig ist."""
    if not order.get("customer"):
        print("Fehler: Kein Kunde angegeben")
        return False
    if not order.get("items"):
        print("Fehler: Keine Artikel in der Bestellung")
        return False
    return True
```

#### Technik 2: Rename Variable / Function

Statt `t`, `p`, `q`, `i` verwenden wir sprechende Namen. Statt `proc` heisst die Funktion `process_order`. Magic Numbers werden zu Konstanten:

```python
VAT_RATE = 1.081         # MwSt-Satz Schweiz (8.1%)
VIP_DISCOUNT = 0.85      # 15% VIP-Rabatt

def calculate_subtotal(items: list[dict]) -> float:
    """Berechnet die Zwischensumme aller Artikel."""
    return sum(item["price"] * item["qty"] for item in items)

def apply_discount(subtotal: float, is_vip: bool) -> float:
    """Wendet den VIP-Rabatt an, falls zutreffend."""
    return subtotal * VIP_DISCOUNT if is_vip else subtotal

def calculate_total(subtotal: float) -> float:
    """Berechnet den Endbetrag inkl. MwSt."""
    return subtotal * VAT_RATE
```

#### Technik 3: Duplikate entfernen

Die Artikelausgabe war vorher dupliziert. Jetzt gibt es eine einzige Funktion dafür:

```python
def format_line_item(item: dict) -> str:
    """Formatiert einen einzelnen Artikel als Rechnungszeile."""
    line_total = item["price"] * item["qty"]
    return f"  {item['name']}: {item['qty']}x CHF {item['price']:.2f} = CHF {line_total:.2f}"

def print_invoice(customer: str, items: list[dict], total: float):
    """Gibt eine formatierte Rechnung aus."""
    print("=== RECHNUNG ===")
    print(f"Kunde: {customer}")
    for item in items:
        print(format_line_item(item))
    print(f"Total (inkl. MwSt): CHF {total:.2f}")
```

#### Zusammengesetzt

```python
def process_order(order: dict) -> float | None:
    """Verarbeitet eine Bestellung: Validierung, Berechnung, Rechnungsausgabe."""
    if not validate_order(order):
        return None

    subtotal = calculate_subtotal(order["items"])
    discounted = apply_discount(subtotal, order.get("vip", False))
    total = calculate_total(discounted)

    print_invoice(order["customer"], order["items"], total)
    return total
```

Jeder Schritt ist in eine eigene Funktion extrahiert, die Hauptfunktion liest sich jetzt wie eine Zusammenfassung.
