---
title: "C1F"
parent: "C - Umsetzung"
nav_order: 2
---

# C1F: Algorithmen in funktionale Teilstücke aufteilen

> *Ich kann Algorithmen in funktionale Teilstücke aufteilen.*

## Lernziele

| # | Lernziel | Beantwortet in |
| --- | ---------- | -------------- |
| 1 | Ich kann in einem gegebenen Algorithmus sinnvolle Teilschritte erkennen, die als eigenständige Funktionen implementiert werden können. | [1. Teilfunktionen identifizieren](#1-teilfunktionen-identifizieren) |
| 2 | Ich kann einen Algorithmus so zerlegen, dass jede Teilfunktion genau eine Aufgabe erfüllt (Single Responsibility). | [2. Funktionale Dekomposition](#2-funktionale-dekomposition) |
| 3 | Ich kann beschreiben, wie die einzelnen Teilfunktionen zusammengesetzt werden, um den Gesamtalgorithmus zu bilden. | [3. Zusammensetzung planen](#3-zusammensetzung-planen) |

---

## 1. Teilfunktionen identifizieren

Ein Algorithmus, der zu viel auf einmal macht, ist schwer zu testen und zu warten. Der erste Schritt ist, logische Teilschritte zu erkennen.

### Beispiel: Monolithische Methode

```java
List<String> process(List<String> data) {
    var result = new ArrayList<String>();
    for (var s : data) {
        var trimmed = s.strip();
        if (!trimmed.isEmpty()) {
            result.add(trimmed.toLowerCase());
        }
    }
    var unique = new ArrayList<>(new HashSet<>(result));
    Collections.sort(unique);
    return unique;
}
```

Dieser Code enthält vier logische Schritte:

| Schritt | Was passiert | Mögliche Funktion |
| ------- | ------------ | ----------------- |
| 1 | Whitespace entfernen und leere Strings filtern | `cleanEntries()` |
| 2 | In Kleinbuchstaben umwandeln | (Teil von `cleanEntries()`) |
| 3 | Duplikate entfernen | `removeDuplicates()` |
| 4 | Alphabetisch sortieren | `sortList()` |

---

## 2. Funktionale Dekomposition

Jede Teilfunktion bekommt genau eine Aufgabe (Single Responsibility), nimmt eine Liste entgegen und gibt eine neue Liste zurück:

```java
// Teilfunktion 1: Bereinigen und leere Einträge entfernen
List<String> cleanEntries(List<String> data) {
    return data.stream()
        .map(String::strip)
        .filter(s -> !s.isEmpty())
        .map(String::toLowerCase)
        .toList();
}

// Teilfunktion 2: Duplikate entfernen
List<String> removeDuplicates(List<String> data) {
    return data.stream().distinct().toList();
}

// Teilfunktion 3: Sortieren
List<String> sortList(List<String> data) {
    return data.stream().sorted().toList();
}
```

### Vorteile der Zerlegung

| Vorteil | Erklärung |
| ------- | --------- |
| **Testbarkeit** | Jede Funktion kann isoliert mit eigenen Testfällen geprüft werden |
| **Wiederverwendbarkeit** | `removeDuplicates` kann überall eingesetzt werden, nicht nur hier |
| **Lesbarkeit** | Funktionsnamen dokumentieren die Logik |
| **Wartbarkeit** | Änderungen betreffen nur die betroffene Teilfunktion |

---

## 3. Zusammensetzung planen

Die Teilfunktionen werden so zusammengesetzt, dass der Output der einen zum Input der nächsten wird:

```java
List<String> process(List<String> data) {
    var cleaned = cleanEntries(data);
    var unique = removeDuplicates(cleaned);
    return sortList(unique);
}
```

### Weiteres Beispiel: Durchschnitt positiver Zahlen

**Aufgabe:** Berechne den Durchschnitt aller positiven Zahlen in einer Liste.

**Zerlegung:**

```java
// Schritt 1: Nur positive Zahlen behalten
List<Integer> filterPositive(List<Integer> numbers) {
    return numbers.stream().filter(n -> n > 0).toList();
}

// Schritt 2: Summe berechnen
int sum(List<Integer> numbers) {
    return numbers.stream().reduce(0, Integer::sum);
}

// Schritt 3: Durchschnitt berechnen
double average(List<Integer> numbers) {
    return numbers.isEmpty() ? 0.0 : (double) sum(numbers) / numbers.size();
}

// Zusammensetzung
double averageOfPositive(List<Integer> numbers) {
    var positive = filterPositive(numbers);
    return average(positive);
}
```

```java
var data = List.of(-3, 5, -1, 8, 2, -7, 4);
System.out.println(averageOfPositive(data));  // 4.75
```

Die Zerlegung folgt immer dem gleichen Muster: Teilschritte identifizieren, als eigenständige Funktionen implementieren, dann verketten. Jede Funktion verändert dabei die Eingabe nicht, sondern erzeugt einen neuen Wert.
