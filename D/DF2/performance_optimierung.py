"""
DF2 — Massnahmen zur Leistungsverbesserung umsetzen

Drei praktische Optimierungstechniken mit Zeitmessungen:
  1. Memoization / Caching
  2. Unnötige Berechnungen eliminieren
  3. Lazy Evaluation mit Generatoren
"""

import time
from functools import lru_cache


# =============================================================================
# Technik 1: Memoization / Caching
# =============================================================================
# Problem: Fibonacci ohne Cache hat exponentielle Laufzeit O(2^n),
# weil dieselben Teilprobleme immer wieder neu berechnet werden.

def fibonacci_slow(n: int) -> int:
    """Fibonacci OHNE Caching — O(2^n), extrem langsam ab n > 30."""
    if n < 2:
        return n
    return fibonacci_slow(n - 1) + fibonacci_slow(n - 2)


@lru_cache(maxsize=None)
def fibonacci_fast(n: int) -> int:
    """
    Fibonacci MIT Caching (Memoization) — O(n).

    @lru_cache speichert die Ergebnisse automatisch.
    Jeder Wert wird nur einmal berechnet und dann aus dem Cache gelesen.
    """
    if n < 2:
        return n
    return fibonacci_fast(n - 1) + fibonacci_fast(n - 2)


def demo_memoization():
    """Vergleicht Fibonacci mit und ohne Caching."""
    n = 35

    print(f"Fibonacci({n}):")

    start = time.perf_counter()
    result_slow = fibonacci_slow(n)
    time_slow = time.perf_counter() - start
    print(f"  Ohne Cache: {result_slow} in {time_slow:.4f}s")

    start = time.perf_counter()
    result_fast = fibonacci_fast(n)
    time_fast = time.perf_counter() - start
    print(f"  Mit Cache:  {result_fast} in {time_fast:.6f}s")

    speedup = time_slow / time_fast if time_fast > 0 else float("inf")
    print(f"  Speedup:    {speedup:.0f}x schneller")


# =============================================================================
# Technik 2: Unnötige Berechnungen eliminieren
# =============================================================================
# Problem: In einer Schleife werden Werte wiederholt berechnet,
# die sich gar nicht ändern.

def find_expensive_items_slow(products: list[dict], budget: float) -> list[str]:
    """
    LANGSAM: Berechnet den Durchschnittspreis in jeder Iteration neu.
    Bei n Produkten: n * n = O(n²) Operationen für die Durchschnitts-Berechnung.
    """
    result = []
    for product in products:
        # Diese Berechnung ist in jeder Iteration identisch!
        avg_price = sum(p["price"] for p in products) / len(products)
        if product["price"] > avg_price and product["price"] <= budget:
            result.append(product["name"])
    return result


def find_expensive_items_fast(products: list[dict], budget: float) -> list[str]:
    """
    SCHNELL: Berechnet den Durchschnittspreis nur einmal — O(n).
    """
    # Einmal berechnen, ausserhalb der Schleife
    avg_price = sum(p["price"] for p in products) / len(products)

    return [
        product["name"]
        for product in products
        if product["price"] > avg_price and product["price"] <= budget
    ]


def demo_eliminate_redundancy():
    """Vergleicht die Versionen mit/ohne redundante Berechnung."""
    # 10'000 Produkte generieren
    products = [{"name": f"Produkt_{i}", "price": float(i % 500)} for i in range(10_000)]
    budget = 300.0

    print("\nUnnötige Berechnungen eliminieren:")

    start = time.perf_counter()
    result_slow = find_expensive_items_slow(products, budget)
    time_slow = time.perf_counter() - start
    print(f"  Redundant:   {len(result_slow)} Treffer in {time_slow:.4f}s")

    start = time.perf_counter()
    result_fast = find_expensive_items_fast(products, budget)
    time_fast = time.perf_counter() - start
    print(f"  Optimiert:   {len(result_fast)} Treffer in {time_fast:.4f}s")

    speedup = time_slow / time_fast if time_fast > 0 else float("inf")
    print(f"  Speedup:     {speedup:.0f}x schneller")


# =============================================================================
# Technik 3: Lazy Evaluation mit Generatoren
# =============================================================================
# Problem: Eine grosse Datenmenge wird komplett in den Speicher geladen,
# obwohl nur ein kleiner Teil davon gebraucht wird.

def first_n_primes_eager(n: int) -> list[int]:
    """
    EAGER: Sammelt alle Primzahlen in einer Liste.
    Braucht Speicher proportional zur Anzahl gefundener Zahlen.
    """
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


def prime_generator():
    """
    LAZY: Gibt Primzahlen eine nach der anderen zurück.
    Braucht nur Speicher für die aktuelle Zahl — O(1) Speicher.
    """
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


def demo_lazy_evaluation():
    """Zeigt den Unterschied zwischen Eager und Lazy Evaluation."""
    import sys

    n = 1000
    print(f"\nErste {n} Primzahlen finden:")

    # Eager: Alles in eine Liste
    primes_list = first_n_primes_eager(n)
    print(f"  Eager (Liste): Speicher = {sys.getsizeof(primes_list)} Bytes")

    # Lazy: Generator, der Werte on-demand liefert
    gen = prime_generator()
    # Nur die ersten n Werte nehmen
    primes_lazy = []
    for _ in range(n):
        primes_lazy.append(next(gen))

    print(f"  Lazy (Generator): Speicher des Generator-Objekts = {sys.getsizeof(gen)} Bytes")
    print(f"  Gleiche Ergebnisse: {primes_list == primes_lazy}")

    # Der Generator braucht praktisch keinen Speicher, egal wie viele
    # Primzahlen man berechnet — er speichert immer nur den aktuellen Zustand.


# =============================================================================
# Alles zusammen ausführen
# =============================================================================

if __name__ == "__main__":
    demo_memoization()
    demo_eliminate_redundancy()
    demo_lazy_evaluation()
