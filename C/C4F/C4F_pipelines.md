---
title: "C4F_Pipelines"
parent: "C - Umsetzung"
nav_order: 11
---

# C4F: Kombinierte Pipelines für Statistiken und Auswertungen

> *Ich kann Map, Filter und Reduce kombiniert verwenden, um Daten zu verarbeiten und zu manipulieren, die komplexere Transformationen erfordern.*

## Lernziele

| # | Lernziel | Beantwortet in |
| --- | ---------- | -------------- |
| 1 | Ich kann mit `Collectors.groupingBy` und `Collectors.summingDouble` aus einer Liste von Bestellungen den Umsatz pro Kategorie berechnen, beschränkt auf bezahlte Bestellungen. | [Umsatz pro Kategorie](#umsatz-pro-kategorie) |
| 2 | Ich kann mehrere funktionale Operationen zu einer Pipeline verketten und erklären, warum das lesbarer ist als temporäre Zwischenvariablen. | [Chaining statt Zwischenvariablen](#chaining-statt-zwischenvariablen) |
| 3 | Ich kann mindestens drei kombinierte Stream-Pipelines mit Filter, Map und Reduce erstellen und den Code mit Kommentaren dokumentieren. | [Drei kombinierte Pipelines](#drei-kombinierte-pipelines) |

---

## Umsatz pro Kategorie

`groupingBy` bildet die Gruppen, `summingDouble` aggregiert pro Gruppe. Ein vorgeschalteter `filter` schränkt die Datenbasis ein, hier auf bezahlte Bestellungen.

```java
record Bestellung(String kategorie, double betrag, boolean bezahlt) {}

var bestellungen = List.of(
    new Bestellung("Getränke", 12.50, true),
    new Bestellung("Essen",    28.00, true),
    new Bestellung("Getränke",  9.00, false),  // nicht bezahlt
    new Bestellung("Essen",    15.50, true),
    new Bestellung("Dessert",   7.20, true),
    new Bestellung("Essen",    22.00, false)   // nicht bezahlt
);

Map<String, Double> umsatzProKategorie = bestellungen.stream()
    .filter(Bestellung::bezahlt)                              // nur bezahlte
    .collect(Collectors.groupingBy(
        Bestellung::kategorie,                               // Schlüssel: Kategorie
        Collectors.summingDouble(Bestellung::betrag)));      // Betrag pro Gruppe summieren
// HashMap, Schlüsselreihenfolge nicht garantiert:
// {Getränke=12.5, Essen=43.5, Dessert=7.2}
```

Der `filter` vor dem `collect` sorgt dafür, dass nicht bezahlte Bestellungen gar nicht erst in die Gruppierung gelangen.

---

## Chaining statt Zwischenvariablen

Dieselbe Logik einmal mit Zwischenvariablen und einmal als Pipeline:

```java
record Person(String name, int alter) {}

// Mit Zwischenvariablen: jeder Schritt braucht einen Namen
var erwachsene = personen.stream().filter(p -> p.alter() >= 18).toList();
var namen      = erwachsene.stream().map(Person::name).toList();
var gross      = namen.stream().map(String::toUpperCase).toList();
```

```java
// Als Pipeline: klarer Datenfluss von oben nach unten
var gross = personen.stream()
    .filter(p -> p.alter() >= 18)   // 1. Erwachsene auswählen
    .map(Person::name)              // 2. Namen extrahieren
    .map(String::toUpperCase)       // 3. gross schreiben
    .toList();
```

### Warum die Pipeline lesbarer ist

| Aspekt | Zwischenvariablen | Pipeline |
| -------- | ------------------- | ---------- |
| Benennung | Jeder Schritt braucht einen Variablennamen | Keine Hilfsnamen nötig |
| Lesefluss | Sprünge zwischen den Variablen | Linear von oben nach unten |
| Verarbeitung | Mehrere Listen werden materialisiert | Ein Durchgang, lazy ausgewertet |
| Fehlerquellen | Falsche Variable leicht verwechselt | Jeder Schritt baut auf dem vorherigen auf |

---

## Drei kombinierte Pipelines

Drei Pipelines auf demselben Datensatz, jede mit Filter, Map und einer Aggregation.

```java
record Person(String name, int alter, double groesse, String stadt) {}

var leute = List.of(
    new Person("Anna",  25, 1.72, "Bern"),
    new Person("Beat",  17, 1.81, "Bern"),
    new Person("Clara", 31, 1.65, "Zürich"),
    new Person("David", 22, 1.90, "Bern"),
    new Person("Eva",   45, 1.68, "Zürich")
);

// Pipeline 1: Durchschnittsgrösse der Erwachsenen aus Bern
double avgGroesse = leute.stream()
    .filter(p -> p.alter() >= 18)             // nur erwachsen
    .filter(p -> p.stadt().equals("Bern"))    // nur Bern
    .mapToDouble(Person::groesse)             // Grösse extrahieren
    .average().orElse(0.0);                    // Durchschnitt, Fallback 0
// (1.72 + 1.90) / 2 = 1.81

// Pipeline 2: Gesamtalter aller Personen über 1.70 m
int summeAlter = leute.stream()
    .filter(p -> p.groesse() > 1.70)          // nur grosse
    .map(Person::alter)                       // Alter extrahieren
    .reduce(0, Integer::sum);                 // aufsummieren
// 25 + 17 + 22 = 64

// Pipeline 3: Namen der Zürcherinnen und Zürcher, alphabetisch verbunden
String zuercher = leute.stream()
    .filter(p -> p.stadt().equals("Zürich"))  // nur Zürich
    .map(Person::name)                        // Namen extrahieren
    .sorted()                                 // alphabetisch sortieren
    .collect(Collectors.joining(", "));       // zu einem String verbinden
// "Clara, Eva"
```

Jede Pipeline filtert zuerst die relevante Teilmenge, transformiert dann auf das benötigte Feld und fasst am Ende zu einem einzelnen Ergebnis zusammen.

> Pipeline 2 nutzt das generische `reduce(0, Integer::sum)`. `average()` (Pipeline 1) und `Collectors.joining()` (Pipeline 3) sind spezialisierte Reduktionen: sie fassen den Stream ebenfalls auf einen einzelnen Wert zusammen, nur mit fester Akkumulationslogik.
