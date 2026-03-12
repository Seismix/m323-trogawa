"""
DE2 — Effiziente Algorithmen und Datenstrukturen auswählen

Drei Aspekte der fortgeschrittenen Performance-Optimierung:
  1. Passende Datenstruktur wählen (List vs. Set vs. Dict)
  2. Algorithmus optimieren (Linear Scan vs. Binary Search)
  3. Trade-offs: Speicher vs. Laufzeit
"""

import time
import bisect
import sys


# =============================================================================
# 1. Passende Datenstruktur wählen
# =============================================================================
# Aufgabe: Prüfen, ob Benutzernamen in einer "Erlaubten"-Liste enthalten sind.
# Die Wahl der Datenstruktur bestimmt die Performance dramatisch.

def check_membership_list(allowed: list, usernames: list) -> list[bool]:
    """
    Mitgliedschaftsprüfung mit LISTE — O(n) pro Prüfung.
    Bei m Prüfungen in einer Liste der Länge n: O(m * n).
    """
    return [user in allowed for user in usernames]


def check_membership_set(allowed: set, usernames: list) -> list[bool]:
    """
    Mitgliedschaftsprüfung mit SET — O(1) pro Prüfung (Durchschnitt).
    Bei m Prüfungen: O(m) — unabhängig von der Grösse des Sets.

    Warum? Sets verwenden intern eine Hash-Tabelle. Der Hash-Wert
    eines Elements zeigt direkt auf den Speicherort — kein Durchsuchen nötig.
    """
    return [user in allowed for user in usernames]


def demo_data_structure_choice():
    """Zeigt den Performance-Unterschied zwischen List und Set."""
    n = 50_000
    allowed_list = [f"user_{i}" for i in range(n)]
    allowed_set = set(allowed_list)

    # 1000 Benutzer prüfen (Mix aus vorhandenen und nicht vorhandenen)
    test_users = [f"user_{i * 7}" for i in range(1000)]

    print("1. Datenstruktur wählen: Mitgliedschaftsprüfung")
    print(f"   Erlaubte Benutzer: {n}, Prüfungen: {len(test_users)}")

    start = time.perf_counter()
    result_list = check_membership_list(allowed_list, test_users)
    time_list = time.perf_counter() - start

    start = time.perf_counter()
    result_set = check_membership_set(allowed_set, test_users)
    time_set = time.perf_counter() - start

    print(f"   Liste: {time_list:.4f}s")
    print(f"   Set:   {time_set:.6f}s")
    print(f"   Speedup: {time_list / time_set:.0f}x")
    print(f"   Gleiche Ergebnisse: {result_list == result_set}")


# =============================================================================
# 2. Algorithmus optimieren: Linear Scan vs. Binary Search
# =============================================================================
# Aufgabe: In einer sortierten Liste einen bestimmten Wert finden.

def linear_search(sorted_data: list, target: int) -> int | None:
    """
    Lineare Suche — O(n).
    Geht Element für Element durch, bis der Wert gefunden wird.
    """
    for i, value in enumerate(sorted_data):
        if value == target:
            return i
    return None


def binary_search(sorted_data: list, target: int) -> int | None:
    """
    Binäre Suche — O(log n).
    Halbiert den Suchbereich in jedem Schritt.

    Funktionsweise:
    1. Schaue in die Mitte der Liste
    2. Ist der Wert zu klein? → Suche in der rechten Hälfte
    3. Ist der Wert zu gross? → Suche in der linken Hälfte
    4. Wiederhole, bis gefunden oder Bereich leer

    Bei 1'000'000 Elementen: max. 20 Vergleiche statt 1'000'000.
    """
    index = bisect.bisect_left(sorted_data, target)
    if index < len(sorted_data) and sorted_data[index] == target:
        return index
    return None


def demo_algorithm_optimization():
    """Vergleicht lineare und binäre Suche."""
    n = 1_000_000
    sorted_data = list(range(n))
    target = n - 42  # Element nahe am Ende — worst case für lineare Suche

    print(f"\n2. Algorithmus optimieren: Suche in {n:_} Elementen")

    start = time.perf_counter()
    result_linear = linear_search(sorted_data, target)
    time_linear = time.perf_counter() - start

    start = time.perf_counter()
    result_binary = binary_search(sorted_data, target)
    time_binary = time.perf_counter() - start

    print(f"   Linear Search: Index {result_linear} in {time_linear:.6f}s")
    print(f"   Binary Search: Index {result_binary} in {time_binary:.6f}s")
    if time_binary > 0:
        print(f"   Speedup: {time_linear / time_binary:.0f}x")


# =============================================================================
# 3. Trade-offs: Speicher vs. Laufzeit
# =============================================================================
# Manchmal kann man Laufzeit sparen, indem man mehr Speicher nutzt (und umgekehrt).
# Hier: Duplikate in einer Liste finden.

def find_duplicates_naive(data: list) -> list:
    """
    Naive Methode — O(n²) Zeit, O(1) extra Speicher.
    Vergleicht jedes Element mit jedem anderen.
    """
    duplicates = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i] == data[j] and data[i] not in duplicates:
                duplicates.append(data[i])
    return duplicates


def find_duplicates_with_set(data: list) -> list:
    """
    Set-basierte Methode — O(n) Zeit, O(n) extra Speicher.
    Nutzt ein Set als "Gedächtnis" für bereits gesehene Elemente.

    Trade-off:
    - Braucht mehr Speicher (das Set)
    - Dafür dramatisch schneller
    """
    seen = set()
    duplicates = set()
    for item in data:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)


def demo_tradeoffs():
    """Zeigt den Trade-off zwischen Speicher und Laufzeit."""
    n = 5_000
    # Liste mit einigen Duplikaten
    data = list(range(n)) + list(range(0, n, 7))

    print(f"\n3. Trade-off Speicher vs. Laufzeit: Duplikate in {len(data)} Elementen")

    start = time.perf_counter()
    result_naive = sorted(find_duplicates_naive(data))
    time_naive = time.perf_counter() - start

    start = time.perf_counter()
    result_set = sorted(find_duplicates_with_set(data))
    time_set = time.perf_counter() - start

    print(f"   Naive (O(n²), wenig Speicher): {time_naive:.4f}s, {len(result_naive)} Duplikate")
    print(f"   Set   (O(n),  mehr Speicher):  {time_set:.6f}s, {len(result_set)} Duplikate")

    # Speicherverbrauch des Sets anzeigen
    test_set = set(range(n))
    print(f"   Extra-Speicher für Set mit {n} Elementen: {sys.getsizeof(test_set):_} Bytes")

    if time_set > 0:
        print(f"   Speedup: {time_naive / time_set:.0f}x (Laufzeit für extra Speicher eingetauscht)")

    print(f"   Gleiche Ergebnisse: {result_naive == result_set}")


# =============================================================================
# Alles zusammen ausführen
# =============================================================================

if __name__ == "__main__":
    demo_data_structure_choice()
    demo_algorithm_optimization()
    demo_tradeoffs()
