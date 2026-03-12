"""
DE1 — Auswirkungen des Refactorings einschätzen

Dieses Beispiel demonstriert:
  1. Mindestens 3 Unit-Tests definieren, die sicherstellen, dass das Verhalten
     einer Funktion nach dem Refactoring unverändert bleibt.
  2. Mindestens 3 potenzielle Nebeneffekte identifizieren und für jede
     eine Gegenmassnahme vorschlagen.
  3. Eine sichere Refactoring-Strategie schrittweise umsetzen.
"""

import unittest


# =============================================================================
# Der ursprüngliche Code (vor Refactoring)
# =============================================================================
# Diese Funktion berechnet Versandkosten. Sie funktioniert, ist aber
# schwer wartbar. Wir wollen sie refactoren — OHNE das Verhalten zu ändern.

def calc_shipping_v1(weight: float, destination: str, express: bool) -> float:
    """Ursprüngliche Version — funktioniert, aber unübersichtlich."""
    if destination == "CH":
        if weight <= 1:
            cost = 7.0
        elif weight <= 5:
            cost = 12.0
        elif weight <= 20:
            cost = 18.0
        else:
            cost = 18.0 + (weight - 20) * 1.5
    elif destination == "EU":
        if weight <= 1:
            cost = 15.0
        elif weight <= 5:
            cost = 25.0
        elif weight <= 20:
            cost = 40.0
        else:
            cost = 40.0 + (weight - 20) * 3.0
    else:
        if weight <= 1:
            cost = 30.0
        elif weight <= 5:
            cost = 50.0
        elif weight <= 20:
            cost = 80.0
        else:
            cost = 80.0 + (weight - 20) * 5.0

    if express:
        cost *= 1.5

    return round(cost, 2)


# =============================================================================
# 3 Unit-Tests, die das Verhalten absichern
# =============================================================================
# Diese Tests werden VOR dem Refactoring geschrieben und definieren das
# erwartete Verhalten. Nach dem Refactoring müssen sie weiterhin bestehen.

class TestShippingBehavior(unittest.TestCase):
    """
    Mindestens 3 Unit-Tests, die sicherstellen, dass das Verhalten
    der Versandkosten-Funktion nach dem Refactoring identisch bleibt.
    """

    def _run_for(self, calc_fn):
        """Hilfsmethode: Erlaubt es, dieselben Tests für v1 und v2 zu nutzen."""
        return calc_fn

    # -- Test 1: Grenzwerte der Gewichtsstufen --
    # Prüft, dass die Schwellenwerte (1kg, 5kg, 20kg) korrekt behandelt werden.
    # Genau auf der Grenze und knapp darüber — hier passieren die meisten Fehler.
    def test_weight_tier_boundaries(self):
        """Gewichtsgrenzen müssen exakt eingehalten werden."""
        for calc_fn in [calc_shipping_v1, calc_shipping_v2]:
            # Genau auf der 1kg-Grenze → günstiger Tarif
            self.assertEqual(calc_fn(1.0, "CH", False), 7.0)
            # Knapp über 1kg → nächster Tarif
            self.assertEqual(calc_fn(1.01, "CH", False), 12.0)
            # Genau auf der 5kg-Grenze
            self.assertEqual(calc_fn(5.0, "CH", False), 12.0)
            # Knapp über 5kg → nächster Tarif
            self.assertEqual(calc_fn(5.01, "CH", False), 18.0)
            # Übergewicht: 25kg CH = 18 + (25-20)*1.5 = 25.5
            self.assertEqual(calc_fn(25.0, "CH", False), 25.5)

    # -- Test 2: Express-Zuschlag korrekt berechnet --
    # Stellt sicher, dass der Express-Multiplikator (1.5x) richtig angewendet wird.
    def test_express_multiplier(self):
        """Express muss den Preis um Faktor 1.5 erhöhen."""
        for calc_fn in [calc_shipping_v1, calc_shipping_v2]:
            normal = calc_fn(3.0, "EU", False)   # 25.0
            express = calc_fn(3.0, "EU", True)    # 37.5
            self.assertEqual(normal, 25.0)
            self.assertEqual(express, 37.5)
            self.assertAlmostEqual(express, normal * 1.5)

    # -- Test 3: Unbekannte Destination fällt auf "Welt"-Tarif --
    # Der else-Branch im Original behandelt alle unbekannten Ziele gleich.
    # Nach dem Refactoring muss das identisch sein.
    def test_unknown_destination_falls_back_to_world(self):
        """Unbekannte Ziele müssen den Welt-Tarif verwenden."""
        for calc_fn in [calc_shipping_v1, calc_shipping_v2]:
            # "US", "JP", "XX" — alles nicht "CH" oder "EU" → Welt-Tarif
            self.assertEqual(calc_fn(0.5, "US", False), 30.0)
            self.assertEqual(calc_fn(0.5, "JP", False), 30.0)
            self.assertEqual(calc_fn(0.5, "XX", False), 30.0)
            # Übergewicht international: 80 + (25-20)*5 = 105, express: 157.5
            self.assertEqual(calc_fn(25.0, "US", True), 157.5)


# =============================================================================
# 3 potenzielle Nebeneffekte + Gegenmassnahmen
# =============================================================================
#
# NEBENEFFEKT 1: Unbekannte Destinationen
#   Im Original behandelt der else-Branch alle unbekannten Ziele.
#   Beim Refactoring zu einem Dictionary könnte man vergessen, einen
#   Fallback einzubauen → KeyError bei unbekannten Destinationen.
#
#   GEGENMASSNAHME: dict.get() mit explizitem Fallback auf "WORLD" verwenden.
#   Test 3 oben prüft dieses Verhalten mit "US", "JP" und "XX".
#
# NEBENEFFEKT 2: Reihenfolge der Gewichtsstufen
#   Die Tiers im Dictionary müssen aufsteigend sortiert sein.
#   Bei falscher Reihenfolge (z.B. [(20, 18), (5, 12), (1, 7)])
#   würde ein 0.5kg-Paket fälschlicherweise in den 20kg-Tarif fallen.
#
#   GEGENMASSNAHME: Tiers explizit aufsteigend definieren und
#   Test 1 oben prüft die Grenzwerte exakt.
#
# NEBENEFFEKT 3: Rundungsdifferenzen
#   Durch eine geänderte Berechnungsreihenfolge (z.B. erst Multiplikation,
#   dann Addition statt umgekehrt) können minimale Gleitkomma-Abweichungen
#   entstehen. Beispiel: 18.0 + 5 * 1.5 = 25.5 vs. (18.0 + 5) * 1.5 = 34.5
#
#   GEGENMASSNAHME: round(cost, 2) am Ende beibehalten und in Tests mit
#   exakten Werten auf 2 Dezimalstellen vergleichen (assertEqual, nicht
#   assertAlmostEqual mit grosser Toleranz).


# =============================================================================
# Refactoring in kleinen Schritten
# =============================================================================

# Schritt A: Versandtarife als Datenstruktur extrahieren
# → Adressiert Nebeneffekt 1 (Fallback) und 2 (Reihenfolge)

SHIPPING_RATES = {
    "CH":    {"tiers": [(1, 7.0), (5, 12.0), (20, 18.0)], "extra_per_kg": 1.5, "base_at_extra": 18.0},
    "EU":    {"tiers": [(1, 15.0), (5, 25.0), (20, 40.0)], "extra_per_kg": 3.0, "base_at_extra": 40.0},
    "WORLD": {"tiers": [(1, 30.0), (5, 50.0), (20, 80.0)], "extra_per_kg": 5.0, "base_at_extra": 80.0},
}

EXPRESS_MULTIPLIER = 1.5


# Schritt B: Lookup-Funktion für Destinationen
# → Gegenmassnahme für Nebeneffekt 1: dict.get() mit Fallback auf "WORLD"

def get_zone(destination: str) -> dict:
    """Bestimmt die Versandzone. Unbekannte Ziele → WORLD (= else-Branch)."""
    return SHIPPING_RATES.get(destination, SHIPPING_RATES["WORLD"])


# Schritt C: Gewichtsbasierte Kostenberechnung extrahieren
# → Gegenmassnahme für Nebeneffekt 2: Tiers werden aufsteigend durchlaufen

def calculate_weight_cost(weight: float, zone: dict) -> float:
    """Berechnet Versandkosten basierend auf Gewicht und Zone."""
    for max_weight, price in zone["tiers"]:  # Muss aufsteigend sortiert sein!
        if weight <= max_weight:
            return price

    # Übergewicht: Basispreis + Zuschlag pro zusätzliches kg
    extra_weight = weight - zone["tiers"][-1][0]
    return zone["base_at_extra"] + extra_weight * zone["extra_per_kg"]


# Schritt D: Alles zusammensetzen
# → Gegenmassnahme für Nebeneffekt 3: round() am Ende beibehalten

def calc_shipping_v2(weight: float, destination: str, express: bool) -> float:
    """
    Refactored Version — identisches Verhalten, bessere Struktur.

    Vorteile gegenüber v1:
    - Neue Versandzonen erfordern nur einen neuen Dict-Eintrag
    - Jede Teillogik ist einzeln testbar
    - Express-Zuschlag ist konfigurierbar
    """
    zone = get_zone(destination)
    cost = calculate_weight_cost(weight, zone)

    if express:
        cost *= EXPRESS_MULTIPLIER

    return round(cost, 2)  # Gegenmassnahme Nebeneffekt 3: Rundung beibehalten


# =============================================================================
# Ausführen
# =============================================================================

if __name__ == "__main__":
    # Unit-Tests laufen lassen — sowohl für v1 als auch v2
    print("Unit-Tests ausführen...\n")
    unittest.main(verbosity=2)
