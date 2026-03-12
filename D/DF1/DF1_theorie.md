---
title: "DF1"
parent: "D - Refactoring & Optimierung"
nav_order: 2
---

# DF1: Refactoring-Techniken anwenden

> *Ich kann mit Refactoring-Techniken einen Code lesbarer und verständlicher machen.*

## Lernziele

| # | Lernziel | Beantwortet in |
|---|----------|----------------|
| 1 | Ich kann einen zu langen Codeabschnitt in eine benannte Funktion extrahieren, um die Lesbarkeit zu verbessern. | [Technik 1: Extract Function](#technik-1-extract-function) |
| 2 | Ich kann Variablen und Funktionen so umbenennen, dass ihr Zweck klar ersichtlich ist. | [Technik 2: Rename Variable / Function](#technik-2-rename-variable--function) |
| 3 | Ich kann duplizierten Code erkennen und durch eine gemeinsame Funktion ersetzen. | [Technik 3: Duplikate entfernen](#technik-3-duplikate-entfernen) |

---

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

Der Validierungsblock war Teil der 30-Zeilen-Funktion `proc`. Jetzt ist er eine eigene Funktion mit klarem Namen. Wer `process_order` liest, sieht sofort: zuerst wird validiert, ohne den Validierungscode selbst lesen zu müssen.

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

Im Original hiessen die Variablen `t`, `p`, `q`, `i` und die Funktion `proc`. Ohne den umliegenden Code zu lesen, ist unklar, was sie bedeuten. Nach dem Umbenennen verrät jeder Name seinen Zweck:

- `t` → `subtotal`, `discounted`, `total` (drei verschiedene Werte, die vorher alle `t` hiessen)
- `p` → `item["price"]` (direkt über das Dictionary)
- `proc` → `process_order`
- `0.85` → `VIP_DISCOUNT`, `1.081` → `VAT_RATE`

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

Im Original wurde `item["price"] * item["qty"]` zweimal berechnet: einmal für die Summe, einmal für die Ausgabe. Die Formatierung eines Artikels als Rechnungszeile war ebenfalls dupliziert. Jetzt gibt es dafür eine einzige Funktion:

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
