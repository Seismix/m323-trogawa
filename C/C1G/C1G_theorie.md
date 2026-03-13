---
title: "C1G"
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

Ein **Algorithmus** ist eine eindeutige, endliche Abfolge von Schritten, die ein Problem löst. Jeder Algorithmus hat drei zentrale Eigenschaften:

| Eigenschaft | Bedeutung | Beispiel |
|-------------|-----------|----------|
| **Endlichkeit** | Der Algorithmus terminiert nach endlich vielen Schritten | Eine Schleife über eine Liste endet, wenn alle Elemente verarbeitet sind |
| **Determiniertheit** | Bei gleicher Eingabe liefert er immer das gleiche Ergebnis | `Collections.max(List.of(3, 1, 2))` gibt immer `3` zurück |
| **Ein-/Ausgabe** | Er nimmt Eingaben entgegen und produziert eine Ausgabe | Eingabe: unsortierte Liste, Ausgabe: sortierte Liste |

### Alltagsbeispiel

Ein Kochrezept ist ein Algorithmus:
- **Eingabe:** Zutaten
- **Schritte:** Schneiden, Mischen, Kochen (endlich viele)
- **Ausgabe:** Fertiges Gericht
- **Determiniert:** Gleiche Zutaten + gleiche Schritte = gleiches Ergebnis

---

## 2. Algorithmus nachvollziehen

Gegeben ist ein Algorithmus, der das Maximum einer Liste findet:

```java
int findMax(List<Integer> numbers) {
    int currentMax = numbers.getFirst();
    for (int number : numbers) {
        if (number > currentMax) {
            currentMax = number;
        }
    }
    return currentMax;
}
```

### Schritt-für-Schritt-Durchlauf mit `[3, 7, 2, 9, 4]`

| Schritt | `number` | `currentMax` | Bedingung `number > currentMax` |
|---------|----------|--------------|----------------------------------|
| Start   |          | 3            |                                  |
| 1       | 3        | 3            | 3 > 3? Nein                      |
| 2       | 7        | 7            | 7 > 3? Ja → update              |
| 3       | 2        | 7            | 2 > 7? Nein                      |
| 4       | 9        | 9            | 9 > 7? Ja → update              |
| 5       | 4        | 9            | 4 > 9? Nein                      |

**Ergebnis:** `9`

### Weiteres Beispiel: Summe berechnen

```java
int total(List<Integer> numbers) {
    int result = 0;
    for (int number : numbers) {
        result += number;
    }
    return result;
}
```

Durchlauf mit `[10, 20, 30]`:

| Schritt | `number` | `result` |
|---------|----------|----------|
| Start   |          | 0        |
| 1       | 10       | 10       |
| 2       | 20       | 30       |
| 3       | 30       | 60       |

**Ergebnis:** `60`

---

## 3. Algorithmus beschreiben

### Lineare Suche in natürlicher Sprache

**Problem:** Finde heraus, ob ein bestimmter Wert in einer Liste vorkommt.

**Beschreibung:**
1. Gehe die Liste Element für Element durch.
2. Vergleiche jedes Element mit dem gesuchten Wert.
3. Falls ein Element übereinstimmt: gib dessen Position zurück.
4. Falls das Ende der Liste erreicht wird, ohne Treffer: gib `-1` zurück.

```java
int linearSearch(List<String> items, String target) {
    for (int i = 0; i < items.size(); i++) {
        if (items.get(i).equals(target)) {
            return i;
        }
    }
    return -1;
}

// Beispiel
var items = List.of("a", "b", "c", "d");
System.out.println(linearSearch(items, "c"));  // 2
System.out.println(linearSearch(items, "x"));  // -1
```

### Bubble Sort in Pseudocode

**Problem:** Sortiere eine Liste von Zahlen aufsteigend.

```
ALGORITHMUS bubble_sort(liste):
    WIEDERHOLE solange Tausch stattfindet:
        FÜR jedes benachbarte Paar (i, i+1):
            FALLS liste[i] > liste[i+1]:
                TAUSCHE liste[i] und liste[i+1]
    RÜCKGABE liste
```

```java
List<Integer> bubbleSort(List<Integer> items) {
    var data = new ArrayList<>(items);
    int n = data.size();
    for (int i = 0; i < n; i++) {
        boolean swapped = false;
        for (int j = 0; j < n - 1 - i; j++) {
            if (data.get(j) > data.get(j + 1)) {
                var temp = data.get(j);
                data.set(j, data.get(j + 1));
                data.set(j + 1, temp);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
    return data;
}

System.out.println(bubbleSort(List.of(5, 3, 8, 1, 2)));
// [1, 2, 3, 5, 8]
```
