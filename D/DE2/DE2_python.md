---
title: "DE2_Python"
parent: "D - Refactoring & Optimierung"
nav_order: 6
---

# DE2: Effiziente Algorithmen und Datenstrukturen auswählen

> *Ich kann effiziente Algorithmen, Techniken oder Datenstrukturen auswählen und einsetzen, um die Leistung von Code zu verbessern.*

## Lernziele

| # | Lernziel | Beantwortet in |
|---|----------|----------------|
| 1 | Ich kann für ein gegebenes Problem die effizienteste Datenstruktur auswählen und die Wahl begründen. | [1. Passende Datenstruktur wählen](#1-passende-datenstruktur-wählen) |
| 2 | Ich kann einen ineffizienten Algorithmus durch einen effizienteren ersetzen. | [2. Algorithmus optimieren: Linear vs. Binary Search](#2-algorithmus-optimieren-linear-vs-binary-search) |
| 3 | Ich kann anhand eines Beispiels mindestens 2 Trade-offs zwischen Speicherverbrauch und Laufzeit erklären. | [3. Trade-offs: Speicher vs. Laufzeit](#3-trade-offs-speicher-vs-laufzeit) |

---

## Überblick

Die fortgeschrittenste Kompetenz im Performance-Bereich:

1. **Passende Datenstruktur wählen:** Das richtige Werkzeug für das Problem
2. **Algorithmus optimieren:** Von brute-force zu effizient
3. **Trade-offs abwägen:** Speicher vs. Laufzeit

---

## 1. Passende Datenstruktur wählen

Aufgabe: Prüfen, ob Benutzernamen in einer "Erlaubten"-Sammlung enthalten sind.

```python
# Mit LISTE - O(n) pro Prüfung
# Die Liste wird linear durchsucht, Element für Element.
def check_membership_list(allowed: list, usernames: list) -> list[bool]:
    return [user in allowed for user in usernames]

# Mit SET - O(1) pro Prüfung (Durchschnitt)
# Sets verwenden intern eine Hash-Tabelle. Der Hash-Wert eines Elements
# zeigt direkt auf den Speicherort - kein Durchsuchen nötig.
def check_membership_set(allowed: set, usernames: list) -> list[bool]:
    return [user in allowed for user in usernames]
```

**Ergebnis:** Liste prüft O(n) pro Lookup, Set prüft O(1). Bei grossen Datenmengen ist der Unterschied massiv.

---

## 2. Algorithmus optimieren: Linear vs. Binary Search

Aufgabe: In einer sortierten Liste einen bestimmten Wert finden.

```python
import bisect

# Lineare Suche - O(n)
# Geht Element für Element durch, bis der Wert gefunden wird.
def linear_search(sorted_data: list, target: int) -> int | None:
    for i, value in enumerate(sorted_data):
        if value == target:
            return i
    return None

# Binäre Suche - O(log n)
# Halbiert den Suchbereich in jedem Schritt:
#   1. Schaue in die Mitte der Liste
#   2. Wert zu klein? → Rechte Hälfte
#   3. Wert zu gross? → Linke Hälfte
#   4. Wiederhole, bis gefunden oder Bereich leer
#
# Bei 1'000'000 Elementen: max. 20 Vergleiche statt 1'000'000.
def binary_search(sorted_data: list, target: int) -> int | None:
    index = bisect.bisect_left(sorted_data, target)
    if index < len(sorted_data) and sorted_data[index] == target:
        return index
    return None
```

**Ergebnis:** Linear Search ist O(n), Binary Search ist O(log n). Bei 1'000'000 Elementen braucht die binäre Suche maximal ~20 Vergleiche statt bis zu 1'000'000.

---

## 3. Trade-offs: Speicher vs. Laufzeit

Manchmal kann man Laufzeit sparen, indem man mehr Speicher nutzt. Hier: Duplikate in einer Liste finden.

```python
# Naive Methode - O(n²) Zeit, O(1) extra Speicher
# Vergleicht jedes Element mit jedem anderen.
def find_duplicates_naive(data: list) -> list:
    duplicates = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i] == data[j] and data[i] not in duplicates:
                duplicates.append(data[i])
    return duplicates

# Set-basierte Methode - O(n) Zeit, O(n) extra Speicher
# Nutzt ein Set als "Gedächtnis" für bereits gesehene Elemente.
def find_duplicates_with_set(data: list) -> list:
    seen = set()
    duplicates = set()
    for item in data:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)
```

**Ergebnis:** Die naive Methode ist O(n²), die Set-Methode O(n), braucht dafür O(n) zusätzlichen Speicher für das Set.

| Methode | Zeit | Speicher | Wann verwenden? |
|---------|------|----------|----------------|
| Naive (O(n²)) | Langsam | Minimal | Nur bei sehr kleinen Datenmengen |
| Set (O(n)) | Schnell | Mehr | Fast immer, der Speicher-Overhead ist minimal |

### Trade-off 2: Memoization (Caching vs. Speicher)

```python
# Ohne Cache: berechnet fibonacci(n) jedes Mal neu - O(2^n) Zeit, O(n) Speicher (Rekursionsstack)
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Mit Cache: speichert bereits berechnete Werte - O(n) Zeit, O(n) Speicher (Cache + Stack)
from functools import lru_cache

@lru_cache
def fibonacci_cached(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)
```

**Ergebnis:** Der Cache reduziert die Laufzeit von O(2^n) auf O(n), braucht dafür aber O(n) zusätzlichen Speicher für die gespeicherten Ergebnisse.

### Trade-off 3: Vorberechnung (Precomputation)

```python
# Ohne Vorberechnung: berechnet die Summe jedes Mal neu - O(n) pro Abfrage
def range_sum(data: list[int], start: int, end: int) -> int:
    return sum(data[start:end + 1])

# Mit Prefix-Sum-Array: O(n) Vorberechnung, danach O(1) pro Abfrage
def build_prefix_sums(data: list[int]) -> list[int]:
    prefix = [0]
    for x in data:
        prefix.append(prefix[-1] + x)
    return prefix

def range_sum_fast(prefix: list[int], start: int, end: int) -> int:
    return prefix[end + 1] - prefix[start]
```

**Ergebnis:** Das Prefix-Sum-Array braucht O(n) zusätzlichen Speicher, macht aber jede Bereichssumme in O(1) statt O(n). Lohnt sich, wenn viele Abfragen auf dieselben Daten gemacht werden.

### Trade-off 4: Lazy vs. Eager Evaluation

```python
# Eager: erzeugt die gesamte Liste im Speicher - O(n) Speicher
squares_list = [x ** 2 for x in range(1_000_000)]

# Lazy: erzeugt Werte erst bei Bedarf - O(1) Speicher
squares_gen = (x ** 2 for x in range(1_000_000))
```

**Ergebnis:** Die Eager-Variante ist schneller beim wiederholten Zugriff (Daten liegen bereit), die Lazy-Variante spart Speicher, muss aber bei jedem Durchlauf neu berechnen. Lazy lohnt sich bei grossen Datenmengen oder wenn nur ein Teil der Daten gebraucht wird.

### Zusammenfassung: 4 Trade-off-Muster

| Trade-off | Mehr Speicher für... | Beispiel |
|-----------|---------------------|----------|
| **Lookup-Struktur** | Schnelleren Zugriff (O(1) statt O(n)) | Set statt Liste für Duplikatsuche |
| **Caching** | Vermeidung redundanter Berechnungen | Memoization bei rekursiven Funktionen |
| **Vorberechnung** | Schnellere Abfragen (O(1) statt O(n)) | Prefix-Sum-Array für Bereichssummen |
| **Lazy Evaluation** | Weniger Speicher, dafür langsamerer Zugriff | Generator statt Liste bei grossen Datenmengen |
