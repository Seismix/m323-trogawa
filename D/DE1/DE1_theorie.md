---
title: "DE1"
parent: "D - Refactoring & Optimierung"
nav_order: 3
---

# DE1: Auswirkungen des Refactorings einschätzen

> *Ich kann die Auswirkungen des Refactorings auf das Verhalten des Codes einschätzen und sicherstellen, dass das Refactoring keine unerwünschten Nebeneffekte hat.*

## Überblick

Refactoring soll das **Verhalten** des Codes nicht verändern, nur seine **Struktur**. Doch wie stellt man das sicher?

1. **Verhaltenserhaltung prüfen:** Für ein gegebenes Refactoring mindestens 3 Unit-Tests definieren, die sicherstellen, dass das Verhalten einer Funktion unverändert bleibt.
2. **Nebeneffekte identifizieren:** Für ein gegebenes Refactoring mindestens 3 potenzielle Nebeneffekte identifizieren und für jede eine Gegenmassnahme vorschlagen.
3. **Refactoring-Strategie wählen:** Schrittweise, testbar, sicher vorgehen.

---

## Ausgangslage: Versandkosten-Funktion

Diese Funktion funktioniert, ist aber schwer wartbar. Wir wollen sie refactoren, OHNE das Verhalten zu ändern.

```python
def calc_shipping_v1(weight: float, destination: str, express: bool) -> float:
    if destination == "CH":
        if weight <= 1:    cost = 7.0
        elif weight <= 5:  cost = 12.0
        elif weight <= 20: cost = 18.0
        else:              cost = 18.0 + (weight - 20) * 1.5
    elif destination == "EU":
        if weight <= 1:    cost = 15.0
        elif weight <= 5:  cost = 25.0
        elif weight <= 20: cost = 40.0
        else:              cost = 40.0 + (weight - 20) * 3.0
    else:  # Welt-Tarif
        if weight <= 1:    cost = 30.0
        elif weight <= 5:  cost = 50.0
        elif weight <= 20: cost = 80.0
        else:              cost = 80.0 + (weight - 20) * 5.0

    if express:
        cost *= 1.5
    return round(cost, 2)
```

---

## 3 Unit-Tests zur Verhaltensabsicherung

Diese Tests werden **vor** dem Refactoring geschrieben. Wenn nach dem Refactoring ein Test fehlschlägt, wissen wir sofort, dass etwas kaputt ist.

```python
import unittest

class TestShippingBehavior(unittest.TestCase):

    # Test 1: Grenzwerte der Gewichtsstufen
    # Genau auf der Grenze und knapp darüber - hier passieren die meisten Fehler.
    def test_weight_tier_boundaries(self):
        for calc_fn in [calc_shipping_v1, calc_shipping_v2]:
            self.assertEqual(calc_fn(1.0, "CH", False), 7.0)    # Genau auf 1kg
            self.assertEqual(calc_fn(1.01, "CH", False), 12.0)   # Knapp darüber
            self.assertEqual(calc_fn(5.0, "CH", False), 12.0)    # Genau auf 5kg
            self.assertEqual(calc_fn(5.01, "CH", False), 18.0)   # Knapp darüber
            self.assertEqual(calc_fn(25.0, "CH", False), 25.5)   # Übergewicht

    # Test 2: Express-Zuschlag korrekt berechnet
    def test_express_multiplier(self):
        for calc_fn in [calc_shipping_v1, calc_shipping_v2]:
            normal = calc_fn(3.0, "EU", False)   # 25.0
            express = calc_fn(3.0, "EU", True)    # 37.5
            self.assertEqual(normal, 25.0)
            self.assertEqual(express, 37.5)
            self.assertAlmostEqual(express, normal * 1.5)

    # Test 3: Unbekannte Destination → Welt-Tarif
    # Der else-Branch behandelt alle unbekannten Ziele gleich.
    def test_unknown_destination_falls_back_to_world(self):
        for calc_fn in [calc_shipping_v1, calc_shipping_v2]:
            self.assertEqual(calc_fn(0.5, "US", False), 30.0)
            self.assertEqual(calc_fn(0.5, "JP", False), 30.0)   # Auch JP → Welt
            self.assertEqual(calc_fn(0.5, "XX", False), 30.0)   # Auch XX → Welt
            self.assertEqual(calc_fn(25.0, "US", True), 157.5)  # Übergewicht + Express
```

---

## 3 potenzielle Nebeneffekte + Gegenmassnahmen

| # | Nebeneffekt | Gegenmassnahme |
|---|------------|----------------|
| 1 | **Unbekannte Destinationen:** Beim Refactoring zu einem Dictionary könnte man vergessen, einen Fallback einzubauen → `KeyError` statt Welt-Tarif | `dict.get()` mit explizitem Fallback auf `"WORLD"`. Test 3 prüft das Verhalten. |
| 2 | **Reihenfolge der Gewichtsstufen:** Tiers im Dictionary könnten vertauscht sein → ein 0.5kg-Paket fällt in den 20kg-Tarif | Tiers explizit aufsteigend definieren. Test 1 prüft die Grenzwerte exakt. |
| 3 | **Rundungsdifferenzen:** Geänderte Berechnungsreihenfolge kann Gleitkomma-Abweichungen erzeugen | `round(cost, 2)` am Ende beibehalten + Tests mit exakten Erwartungswerten. |

---

## Refactoring-Strategie wählen

> *Ich kann für eine gegebene Codebasis eine sichere Refactoring-Strategie vorschlagen, die schrittweise vorgeht und testbar bleibt.*

Eine sichere Strategie folgt immer demselben Muster:

1. **Tests schreiben** bevor man den Code anfasst. Ohne Tests weiss man nicht, ob das Verhalten noch stimmt.
2. **Einen Schritt auf einmal.** Nie mehrere Änderungen gleichzeitig. Nach jedem Schritt Tests laufen lassen.
3. **Riskante Stellen zuerst identifizieren.** Wo könnte sich das Verhalten ändern? (→ Nebeneffekte oben)
4. **Rückwärtskompatibilität sicherstellen.** Bestehende Aufrufer dürfen nicht brechen.

### Beispiel: Strategie für die Versandkosten-Funktion

| Schritt | Änderung | Risiko | Test danach |
|---------|----------|--------|-------------|
| A | Tarife in Datenstruktur extrahieren | Werte könnten falsch übertragen werden | Alle 3 Tests laufen lassen |
| B | `get_zone()` mit Fallback einführen | Unbekannte Destinationen | Test 3 (unknown destination) |
| C | `calculate_weight_cost()` extrahieren | Reihenfolge der Tiers | Test 1 (Grenzwerte) |
| D | Alles zusammensetzen, `round()` beibehalten | Rundungsdifferenzen | Alle 3 Tests laufen lassen |

Jeder Schritt ist einzeln testbar. Wenn ein Test nach Schritt C fehlschlägt, weiss man genau, dass die Gewichtsberechnung das Problem ist.

---

## Refactored Version

```python
# Schritt A: Versandtarife als Datenstruktur extrahieren
# → Adressiert Nebeneffekt 1 (Fallback) und 2 (Reihenfolge)
SHIPPING_RATES = {
    "CH":    {"tiers": [(1, 7.0), (5, 12.0), (20, 18.0)], "extra_per_kg": 1.5, "base_at_extra": 18.0},
    "EU":    {"tiers": [(1, 15.0), (5, 25.0), (20, 40.0)], "extra_per_kg": 3.0, "base_at_extra": 40.0},
    "WORLD": {"tiers": [(1, 30.0), (5, 50.0), (20, 80.0)], "extra_per_kg": 5.0, "base_at_extra": 80.0},
}
EXPRESS_MULTIPLIER = 1.5

# Schritt B: Lookup-Funktion
# → Gegenmassnahme Nebeneffekt 1: dict.get() mit Fallback
def get_zone(destination: str) -> dict:
    return SHIPPING_RATES.get(destination, SHIPPING_RATES["WORLD"])

# Schritt C: Gewichtsbasierte Kostenberechnung
# → Gegenmassnahme Nebeneffekt 2: Tiers werden aufsteigend durchlaufen
def calculate_weight_cost(weight: float, zone: dict) -> float:
    for max_weight, price in zone["tiers"]:  # Muss aufsteigend sortiert sein!
        if weight <= max_weight:
            return price
    extra_weight = weight - zone["tiers"][-1][0]
    return zone["base_at_extra"] + extra_weight * zone["extra_per_kg"]

# Schritt D: Alles zusammensetzen
# → Gegenmassnahme Nebeneffekt 3: round() beibehalten
def calc_shipping_v2(weight: float, destination: str, express: bool) -> float:
    zone = get_zone(destination)
    cost = calculate_weight_cost(weight, zone)
    if express:
        cost *= EXPRESS_MULTIPLIER
    return round(cost, 2)
```

Die Unit-Tests oben laufen für **beide** Versionen, so ist sichergestellt, dass das Verhalten identisch bleibt.
