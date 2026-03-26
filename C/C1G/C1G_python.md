---
title: "C1G_Pyton"
parent: "C - Umsetzung"
nav_order: 1
---

# C1G: Algorithmus erklären

> *Ich kann in eigenen Worten erklären, was ein Algorithmus ist, einen gegebenen Algorithmus nachvollziehen und einen einfachen Algorithmus beschreiben.*

## Lernziele

| # | Lernziel | Beantwortet in |
|---|----------|----------------|
| 1 | Ich kann in eigenen Worten erklären, was ein Algorithmus ist und welche Eigenschaften er hat (Endlichkeit, Determiniertheit, Ein-/Ausgabe). | [1. Algorithmus-Begriff definieren](#1-algorithmus-begriff-definieren) |
| 2 | Ich kann einen gegebenen Algorithmus Schritt für Schritt durchgehen und das Ergebnis für einen bestimmten Input vorhersagen. | [2. Algorithmus nachvollziehen](#2-algorithmus-nachvollziehen) |
| 3 | Ich kann einen einfachen Algorithmus (z.B. Sortierung, Suche) in Pseudocode oder natürlicher Sprache beschreiben. | [3. Algorithmus beschreiben](#3-algorithmus-beschreiben) |

---

## 1. Algorithmus-Begriff definieren

Unter einem **Algorithmus** versteht man eine strikt definierte, endliche Abfolge von Handlungsanweisungen, um ein bestimmtes Problem zu lösen. Dabei bringt er typischerweise drei Kernmerkmale mit:

| Merkmal | Erklärung | Beispiel |
|-------------|-----------|----------|
| **Endlichkeit** | Der Ablauf kommt nach einer begrenzten Anzahl von Aktionen zum Stillstand. | Das Iterieren über eine Liste bricht ab, sobald das letzte Element erreicht ist. |
| **Determiniertheit** | Derselbe Input führt bei jeder Ausführung unweigerlich zum selben Output. | Ein Aufruf von `max([3, 1, 2])` liefert stets `3`. |
| **Ein-/Ausgabe** | Er benötigt Startdaten (Input) und generiert am Ende ein Resultat (Output). | Input: chaotische Liste, Output: geordnete Liste. |

### Vergleich aus dem echten Leben

Ein Rezept zum Backen oder Kochen funktioniert exakt wie ein Algorithmus:
- **Input:** Die rohen Zutaten
- **Verarbeitung:** Schneiden, in der Pfanne braten, abschmecken (eine bestimmte Anzahl an Schritten)
- **Output:** Die fertige Mahlzeit
- **Determiniert:** Werden identische Zutaten auf genau dieselbe Weise verarbeitet, schmeckt das Ergebnis immer gleich.

---

## 2. Algorithmus nachvollziehen

Nehmen wir einen Codeblock, welcher den höchsten Wert in einer Liste ermittelt:

```python
def find_max(numbers):
    current_max = numbers[0]
    for number in numbers:
        if number > current_max:
            current_max = number
    return current_max
```

### Manueller Durchlauf mit `[3, 7, 2, 9, 4]`

| Zeile | `number` | `current_max` | Prüfung: `number > current_max` |
|---------|----------|--------------|----------------------------------|
| Start   |          | 3            |                                  |
| 1       | 3        | 3            | 3 > 3? Falsch                    |
| 2       | 7        | 7            | 7 > 3? Wahr → neuer Maximalwert |
| 3       | 2        | 7            | 2 > 7? Falsch                    |
| 4       | 9        | 9            | 9 > 7? Wahr → neuer Maximalwert |
| 5       | 4        | 9            | 4 > 9? Falsch                    |

**Resultat:** `9`

### Ein zweites Beispiel: Aufsummieren

```python
def total(numbers):
    result = 0
    for number in numbers:
        result += number
    return result
```

Trockenlauf mit `[10, 20, 30]`:

| Schritt | `number` | `result` |
|---------|----------|----------|
| Start   |          | 0        |
| 1       | 10       | 10       |
| 2       | 20       | 30       |
| 3       | 30       | 60       |

**Resultat:** `60`

---

## 3. Algorithmus beschreiben

### Die lineare Suche (in Alltagssprache)

**Ziel:** Prüfen, ob eine gesuchte Variable innerhalb einer Datenstruktur (z. B. einer Liste) existiert.

**Vorgehensweise:**
1. Betrachte die Elemente der Reihe nach von vorne nach hinten.
2. Gleiche das aktuell betrachtete Element mit dem gesuchten Wert ab.
3. Stimmen die Werte überein, brich ab und nenne den aktuellen Index (Position).
4. Hast du alle Elemente durchsucht, ohne einen Treffer zu landen, gib `-1` aus.

```python
def linear_search(items, target):
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1

# Aufruf
items = ["a", "b", "c", "d"]
print(linear_search(items, "c"))  # Output: 2
print(linear_search(items, "x"))  # Output: -1
```

### Der Bubble Sort (als Pseudocode)

**Ziel:** Eine Sammlung von Ziffern chronologisch aufsteigend arrangieren.

```
ALGORITHMUS bubble_sort(daten):
    SOLANGE Vertauschungen getätigt werden:
        GEHE DURCH alle benachbarten Positionen (i, i+1):
            WENN daten[i] grösser ist als daten[i+1]:
                WECHSLE die Plätze von daten[i] und daten[i+1]
    GIB daten zurück
```

```python
def bubble_sort(items):
    # Kopie der Liste erstellen, um das Original nicht zu verändern
    data = items.copy()
    n = len(data)
    
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if data[j] > data[j + 1]:
                # In Python kann man Platzwechsel kompakt so schreiben:
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True
        
        # Wenn im letzten Durchlauf nichts mehr getauscht wurde,
        # ist die Liste bereits komplett sortiert.
        if not swapped:
            break
            
    return data

print(bubble_sort([5, 3, 8, 1, 2]))
# Resultat: [1, 2, 3, 5, 8]
```