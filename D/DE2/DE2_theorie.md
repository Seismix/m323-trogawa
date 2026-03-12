---
title: "DE2"
parent: "D - Refactoring & Optimierung"
nav_order: 6
---

# DE2: Effiziente Algorithmen und Datenstrukturen auswählen

> *Ich kann effiziente Algorithmen, Techniken oder Datenstrukturen auswählen und einsetzen, um die Leistung von Code zu verbessern.*

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

**Ergebnis:** Bei 50'000 erlaubten Benutzern und 1'000 Prüfungen, Set ist **~90x schneller.**

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

**Ergebnis:** Bei 1'000'000 Elementen, Binary Search ist **~1'800x schneller.**

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

**Ergebnis:** Bei 5'000 Elementen, Set-Methode ist **~600x schneller**, braucht dafür ~500 KB extra Speicher.

| Methode | Zeit | Speicher | Wann verwenden? |
|---------|------|----------|----------------|
| Naive (O(n²)) | Langsam | Minimal | Nur bei sehr kleinen Datenmengen |
| Set (O(n)) | Schnell | Mehr | Fast immer, der Speicher-Overhead ist minimal |
