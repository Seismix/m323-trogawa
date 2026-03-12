---
title: "DG2"
parent: "D - Refactoring & Optimierung"
nav_order: 4
---

# DG2: Massnahmen zur Leistungsverbesserung aufzählen

> *Ich kann mindestens 3 allgemeine Techniken zur Leistungsverbesserung von Code benennen und deren Einsatzgebiet erklären.*

## Allgemeine Optimierungstechniken

### Übersicht: 3 Kerntechniken und ihre Einsatzgebiete

| # | Technik | Einsatzgebiet |
|---|---------|--------------|
| 1 | **Caching / Memoization** | Wiederholte teure Berechnungen mit gleichen Inputs (z.B. rekursive Algorithmen, API-Abfragen, Datenbankresultate) |
| 2 | **Lazy Evaluation** | Grosse Datenmengen, bei denen nur ein Teil tatsächlich gebraucht wird (z.B. Streams, Paginierung, Log-Verarbeitung) |
| 3 | **Vermeidung unnötiger Berechnungen** | Schleifen und Hot-Paths, in denen sich wiederholende Ausdrücke aus der Schleife herausgezogen werden können |

---

### 1. Caching / Memoization

Ergebnisse teurer Berechnungen werden zwischengespeichert, sodass sie bei wiederholtem Aufruf nicht neu berechnet werden müssen.

**Einsatzgebiet:** Funktionen, die häufig mit denselben Argumenten aufgerufen werden, typisch bei rekursiven Algorithmen, Datenbankabfragen oder API-Calls.

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Ohne Cache: O(2^n) - extrem langsam
# Mit Cache:  O(n) - jedes Teilergebnis wird nur einmal berechnet
```

### 2. Lazy Evaluation

Werte werden erst berechnet, wenn sie tatsächlich gebraucht werden. Spart Speicher und vermeidet unnötige Arbeit.

**Einsatzgebiet:** Verarbeitung grosser Datenmengen, bei denen man nicht alles gleichzeitig im Speicher braucht, z.B. Datei-Streaming, Paginierung, oder wenn nur die ersten N Ergebnisse benötigt werden.

```python
# Eager: Erstellt die gesamte Liste im Speicher
squares_list = [x ** 2 for x in range(1_000_000)]

# Lazy: Berechnet Werte erst bei Bedarf
squares_gen = (x ** 2 for x in range(1_000_000))
```

### 3. Vermeidung unnötiger Berechnungen

Berechnungen, die wiederholt identisch ausgeführt werden, sollten nur einmal gemacht werden.

**Einsatzgebiet:** Schleifen und häufig durchlaufene Codepfade, in denen derselbe Ausdruck mehrfach ausgewertet wird, z.B. `len()` in jeder Iteration, wiederholte String-Formatierung, oder mehrfache Attribut-Lookups.

```python
# Schlecht: len() wird in jeder Iteration aufgerufen
for i in range(len(items)):
    process(items[i], len(items))

# Besser: Einmal berechnen, wiederverwenden
n = len(items)
for i in range(n):
    process(items[i], n)
```

---

### Weitere Techniken

### 4. Richtige Datenstruktur wählen

Die Wahl der Datenstruktur hat grossen Einfluss auf die Performance.

```python
# Schlecht: Suche in Liste ist O(n)
allowed_users = ["alice", "bob", "charlie", ...]
if username in allowed_users:  # Langsam bei grossen Listen
    grant_access()

# Besser: Suche in Set ist O(1)
allowed_users = {"alice", "bob", "charlie", ...}
if username in allowed_users:  # Konstante Zeit
    grant_access()
```

### 5. Algorithmus-Optimierung

Ein besserer Algorithmus kann den Unterschied zwischen Sekunden und Stunden ausmachen.

```python
# O(n²) - Bubble Sort
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

# O(n log n) - Built-in Sort (Timsort)
arr.sort()
```

---

## Performance-Bottleneck-Typen

| Typ | Beschreibung | Beispiel |
|-----|-------------|---------|
| **CPU-bound** | Prozessor ist der Engpass (viel Rechenarbeit) | Verschlüsselung, Bildverarbeitung, Sortierung grosser Datenmengen |
| **Memory-bound** | Speicher ist der Engpass (zu viel RAM-Verbrauch) | Laden einer riesigen Datei komplett in den Speicher |
| **I/O-bound** | Ein-/Ausgabe ist der Engpass (Warten auf Daten) | Datenbankabfragen, Netzwerk-Requests, Dateizugriffe |

---

## Big-O Notation: Grundlagen

Die Big-O-Notation beschreibt, wie die Laufzeit eines Algorithmus mit der Eingabegrösse wächst.

| Notation | Name | Beispiel | 1'000 Elemente |
|----------|------|---------|----------------|
| **O(1)** | Konstant | Dictionary-Lookup | 1 Operation |
| **O(log n)** | Logarithmisch | Binäre Suche | ~10 Operationen |
| **O(n)** | Linear | Liste durchsuchen | 1'000 Operationen |
| **O(n log n)** | Linearithmisch | Effizientes Sortieren | ~10'000 Operationen |
| **O(n²)** | Quadratisch | Verschachtelte Schleifen | 1'000'000 Operationen |
| **O(2ⁿ)** | Exponentiell | Brute-Force-Suche | Praktisch unmöglich |

### Warum ist O(n) besser als O(n²)?

```
Eingabe:  n = 1'000
O(n):     1'000 Operationen        → Millisekunden
O(n²):    1'000'000 Operationen    → Merklich langsamer

Eingabe:  n = 1'000'000
O(n):     1'000'000 Operationen    → Noch machbar
O(n²):    1'000'000'000'000 Op.    → Stunden bis Tage
```

Je grösser die Eingabe, desto dramatischer wird der Unterschied.
