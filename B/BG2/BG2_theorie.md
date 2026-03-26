---
title: "BG2"
parent: "B - Anforderungen & Design"
nav_order: 4
---

# BG2: Elemente des Functional Design erklären

> *Ich kann Elemente des Functional Design erklären. (z.Bsp. Immutable data types, model, solution, domain of interest, constructors, composable operators)*

## Lernziele

| # | Lernziel | Beantwortet in |
| --- | ---------- | -------------- |
| 1 | Ich kann die Kernelemente des Functional Design (Immutable Data Types, Model, Solution, Domain of Interest) benennen und jeweils in einem Satz erklären. | [1. Grundelemente des Functional Design](#1-grundelemente-des-functional-design) |
| 2 | Ich kann erklären, was Constructors und Composable Operators im Kontext des Functional Design sind. | [2. Constructors und Composable Operators](#2-constructors-und-composable-operators) |
| 3 | Ich kann an einem einfachen Beispiel zeigen, wie die Elemente des Functional Design zusammenwirken. | [3. Zusammenspiel der Elemente](#3-zusammenspiel-der-elemente) |

---

## 1. Grundelemente des Functional Design

| Element | Bedeutung | Beispiel |
| ------- | --------- | -------- |
| **Domain of Interest** | Der Problembereich, den die Software abbilden soll | Finanzverwaltung mit Konzepten wie Konto, Buchung, Bilanz |
| **Model** | Die abstrakte Darstellung der Domain mit Datentypen und Operationen | `record Booking(String desc, double amount, LocalDate date)` |
| **Solution** | Die konkrete Lösung, die das Model auf die Domain anwendet | Eine Pipeline, die alle Buchungen eines Monats summiert |
| **Immutable Data Types** | Datentypen, deren Werte nach der Erstellung nicht verändert werden können | Java Records, `String`, `List.of()` |

### Immutable Data Types in Java

```java
// Record: automatisch immutable
record Product(String name, double price) {}

var apple = new Product("Apfel", 1.50);
// apple.name = "Birne";  // Kompilierungsfehler: kein Setter

// Unveränderbare Liste
var items = List.of("A", "B", "C");
// items.add("D");  // UnsupportedOperationException
```

Statt Werte zu ändern, erzeugt man neue Instanzen:

```java
var expensiveApple = new Product(apple.name(), apple.price() + 0.50);
// Product[name=Apfel, price=2.0]
```

---

## 2. Constructors und Composable Operators

**Constructors** erzeugen neue Instanzen der Datentypen. Im Functional Design sind das Factory-Methoden, die gültige Werte garantieren:

```java
record Temperature(double celsius) {
    static Temperature ofCelsius(double c) {
        return new Temperature(c);
    }
    static Temperature ofFahrenheit(double f) {
        return new Temperature((f - 32) * 5.0 / 9.0);
    }
}

var t1 = Temperature.ofCelsius(25.0);
var t2 = Temperature.ofFahrenheit(77.0);
```

**Composable Operators** sind Funktionen, die sich verketten lassen: der Output von Operator A ist der Input von Operator B.

```java
var bookings = List.of(
    new Booking("Miete", -1200.0, LocalDate.of(2024, 3, 1)),
    new Booking("Lohn",   4500.0, LocalDate.of(2024, 3, 5)),
    new Booking("Essen",  -350.0, LocalDate.of(2024, 3, 10)),
    new Booking("Lohn",   4500.0, LocalDate.of(2024, 4, 5))
);

var marchTotal = bookings.stream()
    .filter(b -> b.date().getMonthValue() == 3)  // Operator 1: Monat filtern
    .map(Booking::amount)                          // Operator 2: Betrag extrahieren
    .reduce(0.0, Double::sum);                     // Operator 3: Summieren
// 2950.0
```

Jeder Operator nimmt das Ergebnis des vorherigen und erzeugt ein neues Ergebnis. Keiner verändert die Originaldaten.

---

## 3. Zusammenspiel der Elemente

Ein vollständiges Beispiel mit einer Todo-Liste zeigt, wie alle Elemente zusammenspielen:

```java
// Immutable Data Type
record Todo(int id, String title, boolean done) {}

// Constructor
static Todo createTodo(int id, String title) {
    return new Todo(id, title, false);
}

// Composable Operators (erzeugen jeweils neue Listen)
static List<Todo> addTodo(List<Todo> todos, Todo todo) {
    return Stream.concat(todos.stream(), Stream.of(todo)).toList();
}

static List<Todo> completeTodo(List<Todo> todos, int id) {
    return todos.stream()
        .map(t -> t.id() == id ? new Todo(t.id(), t.title(), true) : t)
        .toList();
}

static List<Todo> filterOpen(List<Todo> todos) {
    return todos.stream().filter(t -> !t.done()).toList();
}
```

**Verwendung (Solution):**

```java
var todos = List.<Todo>of();
todos = addTodo(todos, createTodo(1, "Einkaufen"));
todos = addTodo(todos, createTodo(2, "Lernen"));
todos = completeTodo(todos, 1);

var open = filterOpen(todos);
// [Todo[id=2, title=Lernen, done=false]]
```

| Element | Im Beispiel |
| ------- | ----------- |
| Domain of Interest | Aufgabenverwaltung |
| Immutable Data Type | `record Todo(...)` |
| Constructor | `createTodo(id, title)` |
| Composable Operators | `addTodo`, `completeTodo`, `filterOpen` |
| Model | Alle Datentypen und Operatoren zusammen |
| Solution | Die konkrete Verkettung der Operatoren |
