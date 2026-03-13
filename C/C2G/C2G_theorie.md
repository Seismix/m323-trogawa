---
title: "C2G"
parent: "C - Umsetzung"
nav_order: 4
---

# C2G: Funktionen als Objekte behandeln

> *Ich kann Funktionen als First-Class Citizens behandeln: in Variablen speichern, als Rückgabewert verwenden und in Datenstrukturen ablegen.*

## Lernziele

| # | Lernziel | Beantwortet in |
|---|----------|----------------|
| 1 | Ich kann eine Funktion in einer Variable speichern und diese Variable aufrufen, um die Funktion auszuführen. | [1. Funktion einer Variable zuweisen](#1-funktion-einer-variable-zuweisen) |
| 2 | Ich kann eine Funktion schreiben, die eine andere Funktion zurückgibt. | [2. Funktion als Rückgabewert](#2-funktion-als-rückgabewert) |
| 3 | Ich kann Funktionen in Listen oder Dictionaries speichern und gezielt abrufen. | [3. Funktionen in Datenstrukturen speichern](#3-funktionen-in-datenstrukturen-speichern) |

---

## Überblick

In Java sind Funktionen keine eigenständigen Objekte wie in Python, aber mit **funktionalen Interfaces** (z.B. `Function`, `UnaryOperator`, `BiFunction`) können Lambdas und Methodenreferenzen in Variablen gespeichert, zurückgegeben und in Datenstrukturen abgelegt werden.

```java
import java.util.function.*;
```

---

## 1. Funktion einer Variable zuweisen

Ein funktionales Interface mit genau einer abstrakten Methode kann eine Lambda-Expression oder Methodenreferenz aufnehmen.

```java
// Lambda in einer Variable speichern
Function<String, String> greet = name -> "Hallo, " + name + "!";

// Über die Variable aufrufen
System.out.println(greet.apply("Anna"));  // Hallo, Anna!
```

### Methodenreferenz zuweisen

Bestehende Methoden können direkt als Referenz zugewiesen werden:

```java
// Methodenreferenz statt Lambda
Function<String, String> toUpper = String::toUpperCase;

System.out.println(toUpper.apply("hallo"));  // HALLO
```

### Verschiedene funktionale Interfaces

```java
// UnaryOperator: gleicher Typ für Ein- und Ausgabe
UnaryOperator<Integer> doubleIt = x -> x * 2;
System.out.println(doubleIt.apply(5));  // 10

// Predicate: gibt boolean zurück
Predicate<Integer> isEven = x -> x % 2 == 0;
System.out.println(isEven.test(4));  // true
System.out.println(isEven.test(7));  // false

// Consumer: nimmt einen Wert, gibt nichts zurück
Consumer<String> printer = System.out::println;
printer.accept("Hallo Welt");  // Hallo Welt
```

---

## 2. Funktion als Rückgabewert

Eine Methode kann eine Funktion (als funktionales Interface) zurückgeben. Das ermöglicht es, Funktionen dynamisch zu erzeugen.

```java
// Gibt eine Funktion zurück, die mit dem gegebenen Faktor multipliziert
static UnaryOperator<Integer> createMultiplier(int factor) {
    return x -> x * factor;
}

// Neue Funktionen erzeugen
var doubleIt = createMultiplier(2);
var tripleIt = createMultiplier(3);

System.out.println(doubleIt.apply(5));   // 10
System.out.println(tripleIt.apply(5));   // 15
System.out.println(doubleIt.apply(10));  // 20
```

### Weiteres Beispiel: Begrüssung mit Präfix

```java
static UnaryOperator<String> createGreeter(String prefix) {
    return name -> prefix + " " + name + "!";
}

var formal = createGreeter("Guten Tag,");
var casual = createGreeter("Hey");

System.out.println(formal.apply("Herr Müller"));  // Guten Tag, Herr Müller!
System.out.println(casual.apply("Max"));           // Hey Max!
```

---

## 3. Funktionen in Datenstrukturen speichern

Funktionale Interfaces können in Listen oder Maps abgelegt und gezielt aufgerufen werden.

### In einer Liste

```java
// Drei Operationen als BiFunction speichern
record NamedOp(String name, BiFunction<Integer, Integer, Integer> fn) {}

var operations = List.of(
    new NamedOp("add",      (a, b) -> a + b),
    new NamedOp("subtract", (a, b) -> a - b),
    new NamedOp("multiply", (a, b) -> a * b)
);

for (var op : operations) {
    System.out.println(op.name() + "(10, 3) = " + op.fn().apply(10, 3));
}
// add(10, 3) = 13
// subtract(10, 3) = 7
// multiply(10, 3) = 30
```

### In einer Map

```java
// Temperatur-Konverter in einer Map
var converters = Map.<String, UnaryOperator<Double>>of(
    "fahrenheit", c -> c * 9 / 5 + 32,
    "kelvin",     c -> c + 273.15
);

// Gezielt abrufen und aufrufen
var unit = "kelvin";
var convert = converters.get(unit);
System.out.println("25°C in " + unit + ": " + convert.apply(25.0));
// 25°C in kelvin: 298.15

unit = "fahrenheit";
convert = converters.get(unit);
System.out.println("25°C in " + unit + ": " + convert.apply(25.0));
// 25°C in fahrenheit: 77.0
```

Das Map-Pattern ist besonders nützlich, um `if/else`-Ketten zu ersetzen:

```java
// Statt:
double convert(double value, String unit) {
    if (unit.equals("fahrenheit")) return value * 9 / 5 + 32;
    else if (unit.equals("kelvin")) return value + 273.15;
    else throw new IllegalArgumentException("Unknown unit: " + unit);
}

// Einfacher:
double convert(double value, String unit) {
    return converters.get(unit).apply(value);
}
```
