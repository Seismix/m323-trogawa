---
title: "C3F (2)"
parent: "C - Umsetzung"
nav_order: 9
---

# C3F: Lambda-Ausdrücke mit mehreren Argumenten (2)

> *Ich kann Lambda-Ausdrücke schreiben, die mehrere Argumente verarbeiten können.*

## Lernziele

| # | Lernziel | Beantwortet in |
| --- | ---------- | ---------------- |
| 1 | Ich kann Lambda-Ausdrücke mit zwei oder mehr Parametern schreiben (z.B. `lambda x, y: x + y`). | [Multi-Parameter Lambdas](#multi-parameter-lambdas) |
| 2 | Ich kann einen Multi-Parameter Lambda-Ausdruck als Sortierkriterium einsetzen, um komplexe Datenstrukturen zu ordnen. | [Lambdas als Sortierkriterium](#lambdas-als-sortierkriterium) |
| 3 | Ich kann für einen Lambda-Ausdruck mit mehreren Parametern das passende funktionale Interface (z.B. BiFunction, BinaryOperator) in Java benennen. | [Funktionale Interfaces für Multi-Parameter Lambdas](#funktionale-interfaces-für-multi-parameter-lambdas) |

---

## Multi-Parameter Lambdas

Mehrere Parameter werden kommagetrennt in Klammern vor dem Pfeil angegeben:

```java
// Zinsbetrag berechnen: Kapital × Zinssatz
BiFunction<Double, Double, Double> interest = (capital, rate) -> capital * rate;
interest.apply(1000.0, 0.035); // => 35.0

// Euklidischer Abstand
BiFunction<Integer, Integer, Double> distance =
    (dx, dy) -> Math.sqrt(dx * dx + dy * dy);
distance.apply(3, 4); // => 5.0
```

### Vergleich: ein Parameter vs. mehrere

```java
// Ein Parameter
Function<String, Integer> strLen = s -> s.length();

// Zwei Parameter, verschiedene Typen
BiFunction<String, String, Boolean> startsWith =
    (text, prefix) -> text.startsWith(prefix);
startsWith.apply("Funktional", "Funk"); // => true

// Zwei Parameter, gleicher Typ
BinaryOperator<Integer> power = (base, exp) -> (int) Math.pow(base, exp);
power.apply(2, 10); // => 1024
```

---

## Lambdas als Sortierkriterium

Ein `Comparator` ist ein funktionales Interface mit zwei Parametern, das sich direkt durch einen Lambda-Ausdruck implementieren lässt:

```java
record Student(String name, int score, String group) {}

var students = List.of(
    new Student("Luisa", 85, "B"),
    new Student("Tom",   92, "A"),
    new Student("Jana",  85, "A")
);

// Primär nach Score absteigend, sekundär nach Name aufsteigend
var ranked = students.stream()
    .sorted((a, b) -> {
        int cmp = Integer.compare(b.score(), a.score());
        return cmp != 0 ? cmp : a.name().compareTo(b.name());
    })
    .toList();
// => [Tom(92), Jana(85), Luisa(85)]
```

Der Lambda `(a, b) -> ...` übernimmt dieselbe Rolle wie eine anonyme Klasse, die `Comparator.compare` implementiert.

```java
// Einfaches Sortieren nach einem Feld
var byGroup = students.stream()
    .sorted((a, b) -> a.group().compareTo(b.group()))
    .toList();
// => [Tom(A), Jana(A), Luisa(B)]
```

---

## Funktionale Interfaces für Multi-Parameter Lambdas

Jeder Lambda-Ausdruck benötigt in Java ein **funktionales Interface** als Zieltyp. Für zwei Parameter stellt `java.util.function` folgende Typen bereit:

| Interface | Parameter | Rückgabe | Typischer Einsatz |
| ----------- | ----------- | ---------- | -------------------- |
| `BiFunction<T, U, R>` | 2 (verschiedene Typen möglich) | `R` | Allgemeine Verarbeitung |
| `BinaryOperator<T>` | 2 (gleicher Typ) | `T` | Arithmetik, Reduktionen |
| `BiConsumer<T, U>` | 2 | `void` | Logging, Map-Iteration |
| `BiPredicate<T, U>` | 2 | `boolean` | Validierung, Filter |

### Interface-Wahl anhand des Rückgabetyps

```java
// Rückgabe: anderer Typ → BiFunction
BiFunction<String, Integer, String> padLeft =
    (s, len) -> String.format("%" + len + "s", s);
padLeft.apply("Hi", 6); // => "    Hi"

// Rückgabe: gleicher Typ → BinaryOperator
BinaryOperator<String> longerOf =
    (a, b) -> a.length() >= b.length() ? a : b;
longerOf.apply("Hallo", "Hi"); // => "Hallo"

// Kein Rückgabewert → BiConsumer
BiConsumer<String, Integer> logEntry =
    (event, count) -> System.out.println("[LOG] " + event + " x" + count);
logEntry.accept("Login", 3); // [LOG] Login x3

// Rückgabe boolean → BiPredicate
BiPredicate<Integer, Integer> inRange =
    (value, max) -> value >= 0 && value <= max;
inRange.test(7, 10); // => true
```

`BinaryOperator<T>` ist ein Spezialfall von `BiFunction<T, T, T>` und wird bevorzugt, wenn beide Eingaben und die Ausgabe denselben Typ haben.
