---
title: "C3F"
parent: "C - Umsetzung"
nav_order: 8
---

# C3F: Lambda-Ausdrücke mit mehreren Argumenten

> *Ich kann Lambda-Ausdrücke schreiben, die mehrere Argumente verarbeiten können.*

## Lernziele

| # | Lernziel | Beantwortet in |
|---|----------|----------------|
| 1 | Ich kann Lambda-Ausdrücke mit zwei oder mehr Parametern schreiben (z.B. `lambda x, y: x + y`). | [Multi-Parameter Lambdas](#multi-parameter-lambdas) |
| 2 | Ich kann einen Multi-Parameter Lambda-Ausdruck als Sortierkriterium einsetzen, um komplexe Datenstrukturen zu ordnen. | [Lambdas als Sortierkriterium](#lambdas-als-sortierkriterium) |

---

## Multi-Parameter Lambdas

Ein Lambda-Ausdruck kann mehrere Parameter entgegennehmen, getrennt durch Kommas:

```java
// Lambda mit zwei Parametern: Fläche eines Rechtecks
BinaryOperator<Integer> area = (width, height) -> width * height;
area.apply(5, 3); // => 15

// Lambda mit drei Parametern: gewichteter Durchschnitt
TriFunction<Double, Double, Double, Double> weightedAvg =
    (a, b, weight) -> a * weight + b * (1 - weight);
```

### Vergleich: ein Parameter vs. mehrere

```java
// Ein Parameter
Function<Integer, Integer> doubleIt = x -> x * 2;

// Zwei Parameter
BiFunction<Integer, Integer, Integer> add = (x, y) -> x + y;

// Zwei Parameter mit komplexerem Ausdruck
BiFunction<String, String, String> fullName =
    (first, last) -> first + " " + last;
fullName.apply("Max", "Muster"); // => "Max Muster"
```

---

## Lambdas als Sortierkriterium

Multi-Parameter Lambdas werden häufig als Comparator eingesetzt, um Datenstrukturen nach eigenen Kriterien zu sortieren:

```java
// Liste von Tupeln (als String-Arrays) nach dem zweiten Element sortieren
var pairs = List.of(
    new String[]{"1", "b"},
    new String[]{"2", "a"},
    new String[]{"3", "c"}
);

var sorted = pairs.stream()
    .sorted((x, y) -> x[1].compareTo(y[1]))
    .toList();
// => [["2","a"], ["1","b"], ["3","c"]]
```

Der Comparator `(x, y) -> x[1].compareTo(y[1])` ist ein Lambda mit **zwei Parametern**, das die Sortierlogik definiert.

```java
// Records nach Preis sortieren
record Product(String name, double price) {}

var products = List.of(
    new Product("Milch", 1.80),
    new Product("Brot", 3.50),
    new Product("Käse", 5.20)
);

var sorted = products.stream()
    .sorted((a, b) -> Double.compare(a.price(), b.price()))
    .toList();
// => [Milch, Brot, Käse]
```
