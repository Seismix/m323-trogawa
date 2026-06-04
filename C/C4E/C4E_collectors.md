---
title: "C4E_Collectors"
parent: "C - Umsetzung"
nav_order: 12
---

# C4E: Gruppierte Ansichten und Statistiken mit Collectors

> *Ich kann Map, Filter und Reduce verwenden, um komplexe Datenverarbeitungsaufgaben zu lösen, wie z.B. die Aggregation von Daten oder die Transformation von Datenstrukturen.*

## Lernziele

| # | Lernziel | Beantwortet in |
| --- | ---------- | ---------------- |
| 1 | Ich kann mit verschachtelten Collectors (`groupingBy`, `mapping`, `collectingAndThen`) aus einer flachen `List<LogEintrag>` eine `Map<Level, List<String>>` erzeugen, die nach Datum gefiltert und alphabetisch sortiert ist. | [Verschachtelte Collectors](#verschachtelte-collectors) |
| 2 | Ich kann eine `DoubleSummaryStatistics` Analyse durchführen (Min, Max, Durchschnitt, Summe) und eine Map-Transformation von "Nachname" zu "Liste von Vornamen" umsetzen. | [Statistiken und Transformationen](#statistiken-und-transformationen) |
| 3 | Ich kann mit `Collectors.groupingBy()` mindestens zwei verschiedene Gruppierungen erstellen und mit `counting()` oder `mapping()` weiterverarbeiten. | [Mehrfache Gruppierungen](#mehrfache-gruppierungen) |

---

## Verschachtelte Collectors

Collectors lassen sich ineinander schachteln, um in einem einzigen Durchgang zu gruppieren, zu transformieren und nachzubearbeiten.

### Aufgabe

> Aus einer flachen Liste von Log-Einträgen soll eine `Map<Level, List<Nachricht>>` entstehen: nur Einträge ab einem Stichdatum, je Level alphabetisch sortiert.

```java
record LogEintrag(LocalDate datum, String level, String nachricht) {}

var logs = List.of(
    new LogEintrag(LocalDate.of(2024, 1, 5),  "ERROR", "Verbindung fehlgeschlagen"),
    new LogEintrag(LocalDate.of(2024, 1, 5),  "INFO",  "Start ok"),
    new LogEintrag(LocalDate.of(2024, 1, 6),  "ERROR", "Abbruch"),
    new LogEintrag(LocalDate.of(2024, 1, 7),  "WARN",  "Speicher knapp"),
    new LogEintrag(LocalDate.of(2023, 12, 31),"ERROR", "Alt, wird gefiltert")
);

LocalDate ab = LocalDate.of(2024, 1, 1);

Map<String, List<String>> nachLevel = logs.stream()
    .filter(l -> !l.datum().isBefore(ab))                  // nur ab Stichdatum
    .collect(Collectors.groupingBy(
        LogEintrag::level,                                 // Schlüssel: Level
        TreeMap::new,                                      // stabile, sortierte Schlüssel
        Collectors.mapping(
            LogEintrag::nachricht,                         // nur die Nachricht behalten
            Collectors.collectingAndThen(
                Collectors.toList(),
                list -> list.stream().sorted().toList()))  // alphabetisch sortieren
    ));
// {ERROR=[Abbruch, Verbindung fehlgeschlagen], INFO=[Start ok], WARN=[Speicher knapp]}
```

### Die drei Bausteine

| Collector | Aufgabe |
| ----------- | --------- |
| `groupingBy` | Bildet die Map, ein Eintrag pro Level |
| `mapping` | Wandelt jedes Element in der Gruppe um (hier: nur die Nachricht) |
| `collectingAndThen` | Wendet eine Nachbearbeitung auf das fertige Ergebnis an (hier: sortieren) |

### Warum verschachteln statt nachbearbeiten?

Man könnte die Map auch nachträglich sortieren, also erst `groupingBy(level, mapping(..., toList()))` und danach jede Liste in einer zweiten Schleife sortieren. Die verschachtelte Variante hat zwei Vorteile:

- **Ein Durchgang, ein Ausdruck:** Gruppieren, Umwandeln und Sortieren passieren in einer einzigen `collect`-Operation, ohne veränderbare Zwischenstruktur.
- **Keine nachträgliche Mutation:** `collectingAndThen` ersetzt die fertige Liste durch eine sortierte Kopie, statt eine bestehende Liste in-place zu verändern.

Die `mapFactory` `TreeMap::new` macht zusätzlich die Schlüsselreihenfolge deterministisch (alphabetisch nach Level). Ohne sie liefert `groupingBy` eine `HashMap`, deren Schlüsselreihenfolge nicht garantiert ist.

---

## Statistiken und Transformationen

### DoubleSummaryStatistics

Statt vier Aggregate einzeln zu berechnen, liefert `summaryStatistics()` Min, Max, Durchschnitt und Summe in einem Durchgang.

```java
record Person(String vorname, String nachname, double groesse) {}

var personen = List.of(
    new Person("Anna",  "Meier", 1.72),
    new Person("Beat",  "Meier", 1.81),
    new Person("Clara", "Huber", 1.65),
    new Person("David", "Huber", 1.90),
    new Person("Eva",   "Meier", 1.68)
);

DoubleSummaryStatistics stats = personen.stream()
    .mapToDouble(Person::groesse)
    .summaryStatistics();

System.out.println("Min:   " + stats.getMin());      // 1.65
System.out.println("Max:   " + stats.getMax());      // 1.9
System.out.println("Avg:   " + stats.getAverage());  // 1.752
System.out.println("Summe: " + stats.getSum());      // 8.76
```

### Map-Transformation: Nachname zu Vornamen

```java
// Datenstruktur umwandeln: pro Nachname die Liste der Vornamen
Map<String, List<String>> vornamenProNachname = personen.stream()
    .collect(Collectors.groupingBy(
        Person::nachname,
        Collectors.mapping(Person::vorname, Collectors.toList())));
// HashMap, Schlüsselreihenfolge nicht garantiert:
// {Meier=[Anna, Beat, Eva], Huber=[Clara, David]}
```

---

## Mehrfache Gruppierungen

Mit `groupingBy()` lassen sich dieselben Daten nach unterschiedlichen Kriterien strukturieren. Ein nachgelagerter Collector bestimmt, was pro Gruppe entsteht.

```java
record Film(String titel, String genre, int jahr) {}

var filme = List.of(
    new Film("Matrix",    "SciFi", 1999),
    new Film("Inception", "SciFi", 2010),
    new Film("Heat",      "Krimi", 1995),
    new Film("Sicario",   "Krimi", 2015),
    new Film("Arrival",   "SciFi", 2016)
);

// Gruppierung 1: nach Jahrzehnt, Anzahl Filme zählen
Map<Integer, Long> proJahrzehnt = filme.stream()
    .collect(Collectors.groupingBy(
        f -> (f.jahr() / 10) * 10,
        Collectors.counting()));
// HashMap, Schlüsselreihenfolge nicht garantiert: {1990=2, 2010=3}

// Gruppierung 2: nach Genre, Titel sammeln
Map<String, List<String>> titelProGenre = filme.stream()
    .collect(Collectors.groupingBy(
        Film::genre,
        Collectors.mapping(Film::titel, Collectors.toList())));
// HashMap, Schlüsselreihenfolge nicht garantiert:
// {SciFi=[Matrix, Inception, Arrival], Krimi=[Heat, Sicario]}
```

| Nachgelagerter Collector | Ergebnis pro Gruppe |
| -------------------------- | --------------------- |
| `counting()` | Anzahl Elemente (`Long`) |
| `mapping(..., toList())` | Liste umgewandelter Werte |
| `summingDouble(...)` | Summe eines Zahlenfeldes |
| `averagingInt(...)` | Durchschnitt eines Zahlenfeldes |
