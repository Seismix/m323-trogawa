---
title: "C4G"
parent: "C - Umsetzung"
nav_order: 10
---

# C4G: Map, Filter und Reduce einzeln anwenden

> *Ich kann `map()`, `filter()` und `reduce()` einzeln verwenden, um Listen zu transformieren, zu filtern und zu aggregieren.*

## Lernziele

| # | Lernziel | Beantwortet in |
|---|----------|----------------|
| 1 | Ich kann `map()` verwenden, um eine Transformation auf jedes Element einer Liste anzuwenden. | [1. Map anwenden](#1-map-anwenden) |
| 2 | Ich kann `filter()` verwenden, um Elemente aus einer Liste nach einem Kriterium auszuwählen. | [2. Filter anwenden](#2-filter-anwenden) |
| 3 | Ich kann `reduce()` verwenden, um eine Liste auf einen einzelnen Wert zu reduzieren (z.B. Summe berechnen). | [3. Reduce anwenden](#3-reduce-anwenden) |

---

## Überblick

In Java werden `map`, `filter` und `reduce` über die **Stream API** verwendet. Ein Stream wird aus einer Collection erzeugt, verarbeitet die Elemente und sammelt das Ergebnis ein.

| Operation | Was sie tut | Eingabe → Ausgabe |
|-----------|------------|-------------------|
| `map()` | Transformiert jedes Element | Stream → Stream (gleiche Anzahl) |
| `filter()` | Wählt Elemente nach Kriterium | Stream → Stream (gleiche oder weniger Elemente) |
| `reduce()` | Fasst alle Elemente zusammen | Stream → Einzelwert |

```java
import java.util.stream.*;
```

---

## 1. Map anwenden

`map(funktion)` wendet eine Funktion auf jedes Element an und gibt einen neuen Stream zurück.

```java
// Alle Zahlen verdoppeln
var numbers = List.of(1, 2, 3, 4, 5);
var doubled = numbers.stream()
    .map(x -> x * 2)
    .toList();
System.out.println(doubled);  // [2, 4, 6, 8, 10]
```

`map()` verändert die Originalliste nicht, sondern erzeugt eine neue:

```java
System.out.println(numbers);  // [1, 2, 3, 4, 5] — unverändert
```

### Weitere Beispiele

```java
// Quadratzahlen berechnen
var squares = List.of(1, 2, 3, 4).stream()
    .map(x -> x * x)
    .toList();
System.out.println(squares);  // [1, 4, 9, 16]

// Preise mit Mehrwertsteuer (8.1%)
var prices = List.of(10.0, 25.0, 50.0);
var withTax = prices.stream()
    .map(p -> Math.round(p * 1.081 * 100.0) / 100.0)
    .toList();
System.out.println(withTax);  // [10.81, 27.03, 54.05]

// Strings in Grossbuchstaben
var words = List.of("hallo", "welt", "java");
var upper = words.stream()
    .map(String::toUpperCase)
    .toList();
System.out.println(upper);  // [HALLO, WELT, JAVA]
```

### Map mit Methodenreferenz

```java
static String formatName(String name) {
    var stripped = name.strip();
    return stripped.substring(0, 1).toUpperCase()
         + stripped.substring(1).toLowerCase();
}

var rawNames = List.of("  alice", "BOB  ", " charlie ");
var cleanNames = rawNames.stream()
    .map(Main::formatName)
    .toList();
System.out.println(cleanNames);  // [Alice, Bob, Charlie]
```

---

## 2. Filter anwenden

`filter(predicate)` behält nur die Elemente, für die das Predicate `true` zurückgibt.

```java
// Nur gerade Zahlen behalten
var numbers = List.of(1, 2, 3, 4, 5, 6, 7, 8);
var even = numbers.stream()
    .filter(x -> x % 2 == 0)
    .toList();
System.out.println(even);  // [2, 4, 6, 8]
```

### Weitere Beispiele

```java
// Nur positive Zahlen
var values = List.of(-5, 3, -1, 7, 0, -2, 4);
var positive = values.stream()
    .filter(x -> x > 0)
    .toList();
System.out.println(positive);  // [3, 7, 4]

// Nur Strings mit mindestens 5 Zeichen
var words = List.of("Hi", "Hallo", "Welt", "Stream", "OK");
var longWords = words.stream()
    .filter(w -> w.length() >= 5)
    .toList();
System.out.println(longWords);  // [Hallo, Stream]

// Nur bestandene Prüfungen (Note >= 4.0)
var grades = List.of(5.5, 3.5, 4.0, 2.0, 6.0, 4.5);
var passed = grades.stream()
    .filter(g -> g >= 4.0)
    .toList();
System.out.println(passed);  // [5.5, 4.0, 6.0, 4.5]
```

### Filter mit Methodenreferenz

```java
static boolean isValidEmail(String email) {
    int atIndex = email.indexOf('@');
    return atIndex > 0 && email.substring(atIndex).contains(".");
}

var emails = List.of("alice@example.com", "invalid", "bob@mail.ch", "no-at-sign");
var valid = emails.stream()
    .filter(Main::isValidEmail)
    .toList();
System.out.println(valid);  // [alice@example.com, bob@mail.ch]
```

---

## 3. Reduce anwenden

`reduce(identity, accumulator)` kombiniert alle Elemente schrittweise zu einem einzelnen Wert. Der Accumulator nimmt immer zwei Argumente: den bisherigen Wert und das nächste Element.

```java
// Summe aller Zahlen
var numbers = List.of(1, 2, 3, 4, 5);
int total = numbers.stream()
    .reduce(0, (acc, x) -> acc + x);
System.out.println(total);  // 15
```

### Wie Reduce funktioniert (Schritt für Schritt)

Für `reduce(0, (acc, x) -> acc + x)` mit `[1, 2, 3, 4, 5]`:

| Schritt | `acc` | `x` | Ergebnis |
|---------|-------|-----|----------|
| Start   | 0     |     | 0        |
| 1       | 0     | 1   | 1        |
| 2       | 1     | 2   | 3        |
| 3       | 3     | 3   | 6        |
| 4       | 6     | 4   | 10       |
| 5       | 10    | 5   | 15       |

### Weitere Beispiele

```java
// Produkt aller Zahlen
var numbers = List.of(2, 3, 4, 5);
int product = numbers.stream()
    .reduce(1, (acc, x) -> acc * x);
System.out.println(product);  // 120

// Maximum finden
var values = List.of(3, 7, 2, 9, 4);
int maximum = values.stream()
    .reduce(Integer.MIN_VALUE, (acc, x) -> x > acc ? x : acc);
System.out.println(maximum);  // 9

// Strings zusammenfügen
var words = List.of("Funktionale", "Programmierung", "ist", "elegant");
String sentence = words.stream()
    .reduce("", (acc, w) -> acc.isEmpty() ? w : acc + " " + w);
System.out.println(sentence);  // Funktionale Programmierung ist elegant
```

### Reduce ohne Startwert

Ohne Startwert gibt `reduce` ein `Optional` zurück, da die Liste leer sein könnte:

```java
var numbers = List.of(1, 2, 3);
Optional<Integer> sum = numbers.stream()
    .reduce((acc, x) -> acc + x);
System.out.println(sum.orElse(0));  // 6

// Leere Liste
Optional<Integer> empty = List.<Integer>of().stream()
    .reduce((acc, x) -> acc + x);
System.out.println(empty.orElse(0));  // 0
```

### Spezialisierte Reduce-Methoden

Für primitive Typen bietet Java optimierte Varianten:

```java
var numbers = List.of(1, 2, 3, 4, 5);

// mapToInt erzeugt einen IntStream mit spezialisierten Methoden
int sum = numbers.stream().mapToInt(Integer::intValue).sum();
OptionalInt max = numbers.stream().mapToInt(Integer::intValue).max();
double avg = numbers.stream().mapToInt(Integer::intValue).average().orElse(0);

System.out.println(sum);                // 15
System.out.println(max.orElse(0));      // 5
System.out.println(avg);                // 3.0
```
