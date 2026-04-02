---
title: "C4F"
parent: "C - Umsetzung"
nav_order: 11
---

# C4F: Map, Filter und Reduce kombinieren

> *Ich kann Map, Filter und Reduce kombiniert verwenden, um Daten zu verarbeiten und zu manipulieren, die komplexere Transformationen erfordern.*

## Lernziele

| # | Lernziel | Beantwortet in |
| --- | ---------- | -------------- |
| 1 | Ich kann `filter()` und `map()` kombinieren, um Daten zuerst zu filtern und dann zu transformieren. | [1. Filter + Map Kette](#1-filter--map-kette) |
| 2 | Ich kann `map()` und `reduce()` kombinieren, um Daten zu transformieren und anschliessend zu aggregieren. | [2. Map + Reduce Kette](#2-map--reduce-kette) |
| 3 | Ich kann `filter()`, `map()` und `reduce()` in einer Pipeline kombinieren, um eine mehrstufige Datenverarbeitung durchzuführen. | [3. Dreifach-Kombination](#3-dreifach-kombination) |

---

## 1. Filter + Map Kette

Zuerst Elemente auswählen, dann transformieren. Die Reihenfolge ist wichtig: Filtern vor dem Transformieren reduziert die Anzahl der zu verarbeitenden Elemente.

```java
// Nur positive Zahlen quadrieren
var numbers = List.of(1, -2, 3, -4, 5);
var result = numbers.stream()
    .filter(x -> x > 0)       // [1, 3, 5]
    .map(x -> x * x)          // [1, 9, 25]
    .toList();
System.out.println(result);   // [1, 9, 25]
```

### Praxisbeispiel: Produktnamen

```java
record Product(String name, double price) {}

var products = List.of(
    new Product("Laptop", 1200.0),
    new Product("Maus", 25.0),
    new Product("Monitor", 450.0),
    new Product("Kabel", 8.0)
);

// Namen aller Produkte über 100 CHF, in Grossbuchstaben
var expensiveNames = products.stream()
    .filter(p -> p.price() > 100)
    .map(p -> p.name().toUpperCase())
    .toList();
System.out.println(expensiveNames);  // [LAPTOP, MONITOR]
```

---

## 2. Map + Reduce Kette

Zuerst Daten transformieren, dann zu einem einzelnen Wert zusammenfassen.

```java
// Gesamtpreis aller Produkte berechnen
var total = products.stream()
    .map(Product::price)                // [1200.0, 25.0, 450.0, 8.0]
    .reduce(0.0, Double::sum);          // 1683.0
System.out.println(total);
```

### Praxisbeispiel: Zeichenlänge

```java
// Gesamtanzahl Zeichen aller Wörter
var words = List.of("Funktional", "ist", "elegant");
int totalChars = words.stream()
    .map(String::length)           // [10, 3, 7]
    .reduce(0, Integer::sum);      // 20
System.out.println(totalChars);
```

---

## 3. Dreifach-Kombination

Die vollständige Pipeline: filtern, transformieren, aggregieren.

```java
// Summe aller verdoppelten Preise über 10 CHF
var prices = List.of(5.0, 15.0, 8.0, 20.0, 3.0, 12.0);

var sum = prices.stream()
    .filter(p -> p > 10)               // [15.0, 20.0, 12.0]
    .map(p -> p * 2)                   // [30.0, 40.0, 24.0]
    .reduce(0.0, Double::sum);         // 94.0
System.out.println(sum);
```

### Praxisbeispiel: Lohnsumme

```java
record Employee(String name, String dept, double salary) {}

var employees = List.of(
    new Employee("Anna",  "IT",     8500),
    new Employee("Beat",  "IT",     7200),
    new Employee("Clara", "HR",     6800),
    new Employee("David", "IT",     9100),
    new Employee("Eva",   "HR",     7000)
);

// Gesamtlohn aller IT-Mitarbeiter mit Gehalt über 8000
var itHighSalary = employees.stream()
    .filter(e -> e.dept().equals("IT"))     // Anna, Beat, David
    .filter(e -> e.salary() > 8000)         // Anna, David
    .map(Employee::salary)                  // [8500, 9100]
    .reduce(0.0, Double::sum);              // 17600.0
System.out.println(itHighSalary);
```

### Vergleich: Imperativ vs. Pipeline

| Aspekt | Imperativ | Stream-Pipeline |
| -------- | ----------- | ----------------- |
| Zwischenvariablen | Mehrere `ArrayList`-Instanzen | Keine |
| Lesbarkeit | Logik in Schleifen verteilt | Schritte linear von oben nach unten |
| Immutability | Manuell sicherstellen | Automatisch durch Streams |

```java
// Imperativ
var sum = 0.0;
for (var e : employees) {
    if (e.dept().equals("IT") && e.salary() > 8000) {
        sum += e.salary();
    }
}

// Deklarativ (gleiche Logik, klarer strukturiert)
var sum = employees.stream()
    .filter(e -> e.dept().equals("IT"))
    .filter(e -> e.salary() > 8000)
    .map(Employee::salary)
    .reduce(0.0, Double::sum);
```
