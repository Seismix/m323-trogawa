---
title: "DF2"
parent: "D — Refactoring & Optimierung"
nav_order: 5
---

# DF2 — Massnahmen zur Leistungsverbesserung umsetzen

> *Ich kann vorgegebene Massnahmen zur Verbesserung der Leistung von Code umsetzen.*

## Überblick

Hier geht es darum, Performance-Optimierungen **praktisch umzusetzen**:

1. **Caching / Memoization** — Teure Berechnungen zwischenspeichern
2. **Unnötige Berechnungen eliminieren** — Redundante Arbeit erkennen und entfernen
3. **Lazy Evaluation** — Werte erst bei Bedarf berechnen

---

## 1. Memoization / Caching

Fibonacci ohne Cache hat exponentielle Laufzeit O(2^n), weil dieselben Teilprobleme immer wieder neu berechnet werden.

```python
from functools import lru_cache

# OHNE Caching — O(2^n), extrem langsam ab n > 30
def fibonacci_slow(n: int) -> int:
    if n < 2:
        return n
    return fibonacci_slow(n - 1) + fibonacci_slow(n - 2)

# MIT Caching — O(n)
# @lru_cache speichert die Ergebnisse automatisch.
# Jeder Wert wird nur einmal berechnet und dann aus dem Cache gelesen.
@lru_cache(maxsize=None)
def fibonacci_fast(n: int) -> int:
    if n < 2:
        return n
    return fibonacci_fast(n - 1) + fibonacci_fast(n - 2)
```

**Ergebnis:** `fibonacci(35)` — ohne Cache ~1s, mit Cache ~0.00002s. **~50'000x schneller.**

---

## 2. Unnötige Berechnungen eliminieren

In einer Schleife werden Werte wiederholt berechnet, die sich gar nicht ändern:

```python
# LANGSAM: Durchschnittspreis wird in jeder Iteration neu berechnet — O(n²)
def find_expensive_items_slow(products: list[dict], budget: float) -> list[str]:
    result = []
    for product in products:
        # Diese Berechnung ist in jeder Iteration identisch!
        avg_price = sum(p["price"] for p in products) / len(products)
        if product["price"] > avg_price and product["price"] <= budget:
            result.append(product["name"])
    return result

# SCHNELL: Einmal berechnen, ausserhalb der Schleife — O(n)
def find_expensive_items_fast(products: list[dict], budget: float) -> list[str]:
    avg_price = sum(p["price"] for p in products) / len(products)
    return [
        product["name"]
        for product in products
        if product["price"] > avg_price and product["price"] <= budget
    ]
```

**Ergebnis:** Bei 10'000 Produkten ~**5'000x schneller.**

---

## 3. Lazy Evaluation mit Generatoren

Eine grosse Datenmenge wird komplett in den Speicher geladen, obwohl nur ein Teil davon gebraucht wird:

```python
# EAGER: Sammelt alle Primzahlen in einer Liste
# Braucht Speicher proportional zur Anzahl gefundener Zahlen.
def first_n_primes_eager(n: int) -> list[int]:
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    primes = []
    candidate = 2
    while len(primes) < n:
        if is_prime(candidate):
            primes.append(candidate)
        candidate += 1
    return primes

# LAZY: Gibt Primzahlen eine nach der anderen zurück
# Braucht nur Speicher für die aktuelle Zahl — O(1) Speicher.
def prime_generator():
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    candidate = 2
    while True:
        if is_prime(candidate):
            yield candidate  # Gibt den Wert zurück und pausiert
        candidate += 1
```

**Ergebnis:** Für 1'000 Primzahlen — Liste: ~8'800 Bytes, Generator: ~200 Bytes. Gleiche Ergebnisse, **44x weniger Speicher.**
