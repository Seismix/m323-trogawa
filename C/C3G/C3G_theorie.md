---
title: "C3G"
parent: "C - Umsetzung"
nav_order: 7
---

# C3G: Einfache Lambda-Ausdrücke schreiben

> *Ich kann einfache Lambda-Ausdrücke für Berechnungen und String-Operationen schreiben, mit bedingten Ausdrücken kombinieren und erklären, wann Lambdas sinnvoll sind.*

## Lernziele

| # | Lernziel | Beantwortet in |
|---|----------|----------------|
| 1 | Ich kann eine Lambda-Funktion schreiben, die eine einfache Berechnung durchführt (z.B. `lambda x: x ** 2`). | [1. Einzeilige Lambda-Funktion](#1-einzeilige-lambda-funktion) |
| 2 | Ich kann eine Lambda-Funktion schreiben, die eine String-Transformation durchführt (z.B. Grossbuchstaben-Konvertierung). | [2. Lambda mit String-Operation](#2-lambda-mit-string-operation) |
| 3 | Ich kann erklären, wann ein Lambda-Ausdruck sinnvoller ist als eine benannte Funktion und umgekehrt. | [3. Lambda vs. benannte Funktion](#3-lambda-vs-benannte-funktion) |
| 4 | Ich kann einen Lambda-Ausdruck mit einem ternären Operator schreiben. | [4. Lambda mit bedingtem Ausdruck](#4-lambda-mit-bedingtem-ausdruck) |

---

## Überblick

Ein **Lambda-Ausdruck** in Java ist eine kompakte Schreibweise für eine anonyme Funktion. Lambdas implementieren ein funktionales Interface (ein Interface mit genau einer abstrakten Methode).

```java
// Syntax
(parameter) -> ausdruck
(parameter) -> { anweisungen; }
```

Lambdas eignen sich für kurze, einmalige Operationen. Für alles Komplexere sollte man eine benannte Methode verwenden.

---

## 1. Einzeilige Lambda-Funktion

```java
// Lambda für einfache Berechnungen
UnaryOperator<Integer> square = x -> x * x;
System.out.println(square.apply(5));  // 25

UnaryOperator<Integer> doubleIt = x -> x * 2;
System.out.println(doubleIt.apply(7));  // 14

UnaryOperator<Integer> addTen = x -> x + 10;
System.out.println(addTen.apply(5));  // 15
```

Lambdas sind besonders praktisch, wenn sie direkt als Argument übergeben werden:

```java
var numbers = List.of(1, 2, 3, 4, 5);

// Lambda direkt in sorted() verwenden
var descending = numbers.stream()
    .sorted((a, b) -> b - a)
    .toList();
System.out.println(descending);  // [5, 4, 3, 2, 1]
```

---

## 2. Lambda mit String-Operation

```java
// Grossbuchstaben
UnaryOperator<String> toUpper = s -> s.toUpperCase();
System.out.println(toUpper.apply("hallo"));  // HALLO

// Oder als Methodenreferenz
UnaryOperator<String> toUpper2 = String::toUpperCase;

// String umkehren
UnaryOperator<String> reverse = s -> new StringBuilder(s).reverse().toString();
System.out.println(reverse.apply("Hallo"));  // ollaH
```

### Anwendung: Liste von Namen normalisieren

```java
var names = List.of("  alice ", "BOB", " Charlie");

var cleaned = names.stream()
    .map(name -> name.strip().substring(0, 1).toUpperCase()
              + name.strip().substring(1).toLowerCase())
    .toList();
System.out.println(cleaned);  // [Alice, Bob, Charlie]
```

---

## 3. Lambda vs. benannte Funktion

| Kriterium | Lambda | Benannte Methode |
|-----------|--------|------------------|
| **Umfang** | Ein Ausdruck oder kurzer Block | Beliebig viele Zeilen |
| **Name** | Anonym | Sprechender Methodenname |
| **Wiederverwendung** | Für einmaligen Gebrauch | Für mehrfachen Aufruf |
| **Lesbarkeit** | Kurze, offensichtliche Logik | Komplexe oder benannte Logik |
| **Debugging** | Stacktrace zeigt `lambda$...` | Stacktrace zeigt Methodennamen |

### Wann Lambda sinnvoll ist

```java
// Gut: kurze, einmalige Sortierlogik
record Student(String name, double grade) {}

var students = List.of(
    new Student("Anna", 2.1),
    new Student("Ben", 1.5),
    new Student("Clara", 1.8)
);
var sorted = students.stream()
    .sorted((a, b) -> Double.compare(a.grade(), b.grade()))
    .toList();
```

### Wann eine benannte Methode besser ist

```java
// Schlecht: Lambda zu komplex, schwer zu lesen
Function<Object, String> process = x ->
    x instanceof String s
        ? s.strip().toLowerCase().replace(" ", "_")
        : x.toString();

// Besser: benannte Methode
static String normalizeValue(Object x) {
    if (x instanceof String s) {
        return s.strip().toLowerCase().replace(" ", "_");
    }
    return x.toString();
}
```

**Faustregel:** Wenn die Lambda-Logik nicht auf einen Blick verständlich ist, sollte man eine benannte Methode verwenden.

---

## 4. Lambda mit bedingtem Ausdruck

Der ternäre Operator (`bedingung ? wertWennWahr : wertWennFalsch`) kann direkt in einem Lambda verwendet werden.

```java
// Gerade oder ungerade?
Function<Integer, String> parity = x -> x % 2 == 0 ? "gerade" : "ungerade";
System.out.println(parity.apply(4));  // gerade
System.out.println(parity.apply(7));  // ungerade

// Positiv, negativ oder null?
Function<Integer, String> sign = x -> x > 0 ? "positiv" : (x == 0 ? "null" : "negativ");
System.out.println(sign.apply(5));   // positiv
System.out.println(sign.apply(0));   // null
System.out.println(sign.apply(-3));  // negativ

// Praktisches Beispiel: Rabatt berechnen
UnaryOperator<Double> discount = price -> price > 100 ? price * 0.9 : price;
System.out.println(discount.apply(150.0));  // 135.0
System.out.println(discount.apply(80.0));   // 80.0
```

### Anwendung in `map()`

```java
var temperatures = List.of(35, 28, 42, 15, 38);

var warnings = temperatures.stream()
    .map(t -> t + "°C: " + (t > 35 ? "WARNUNG" : "OK"))
    .toList();
System.out.println(warnings);
// [35°C: OK, 28°C: OK, 42°C: WARNUNG, 15°C: OK, 38°C: WARNUNG]
```
