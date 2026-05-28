---
title: "BF2"
parent: "B - Anforderungen & Design"
nav_order: 5
---

# BF2: Functional Design entwerfen

> *Ich kann für eine Problemstellung ein Functional-Design entwerfen und dabei die Elemente des Functional Designs anwenden.*

## Lernziele

| # | Lernziel | Beantwortet in |
| --- | -------- | -------------- |
| 1 | Ich kann für eine gegebene Problemstellung ein Functional Design entwerfen, indem ich Domain of Interest, Constructors und Composable Operators definiere. | [Design erstellen](#design-erstellen) |
| 2 | Ich kann das entworfene Design in lauffähigen Code umsetzen und die einzelnen Operatoren zu einer Solution zusammensetzen. | [Design umsetzen](#design-umsetzen) |
| 3 | Ich kann für ein selbst gewähltes einfaches Problem eine vollständige Lösung nach dem Functional-Design-Schema formulieren. | [Functional Design anwenden](#functional-design-anwenden) |

---

## Design erstellen

Bevor Code geschrieben wird, entwirft man das Functional Design auf Papier (oder als Tabelle). Drei Bausteine müssen definiert sein: **Domain of Interest**, **Constructors** und **Composable Operators**.

### Problemstellung: Pizzabestellung

Ein Kunde bestellt mehrere Pizzen mit optionalen Toppings. Die Bestellung hat einen Gesamtpreis, der sich aus Basispreis und Aufpreisen für Toppings zusammensetzt.

### Schritt 1: Domain of Interest identifizieren

| Konzept | Rolle | Begründung |
| ------- | ----- | ---------- |
| Topping | Wert | Hat Name und Aufpreis, kein eigenes Verhalten |
| Pizza | Wert | Hat Name, Basispreis und eine Liste von Toppings |
| Order | Wert | Sammlung von Pizzen, repräsentiert die ganze Bestellung |

### Schritt 2: Constructors definieren

Constructors erzeugen gültige Ausgangswerte. Sie kapseln Defaults und Invarianten.

| Name | Zweck | Signatur |
| ---- | ----- | -------- |
| `margherita()` | Standard-Pizza ohne Toppings | `() -> Pizza` |
| `emptyOrder()` | Leere Bestellung als Startpunkt | `() -> Order` |

### Schritt 3: Composable Operators definieren

Composable Operators haben passende Input/Output-Typen, damit sich ihre Aufrufe verketten lassen.

| Name | Zweck | Signatur |
| ---- | ----- | -------- |
| `addPizza` | Fügt der Bestellung eine Pizza hinzu | `(Order, Pizza) -> Order` |
| `addToppingToLast` | Ergänzt die zuletzt hinzugefügte Pizza um ein Topping | `(Order, Topping) -> Order` |
| `total` | Berechnet den Gesamtpreis | `Order -> double` |

`addPizza` und `addToppingToLast` sind composable (beide `Order -> Order`). `total` ist ein terminaler Operator und schliesst die Pipeline ab.

---

## Design umsetzen

Das Design wird zu Java-Code: Records als Immutable Data Types, static functions als Constructors und Operators, eine Verkettung als Solution.

### Immutable Data Types

```java
record Topping(String name, double extra) {}
record Pizza(String name, double basePrice, List<Topping> toppings) {}
record Order(List<Pizza> pizzas) {}
```

### Constructors

```java
static Pizza margherita() {
    return new Pizza("Margherita", 12.0, List.of());
}

static Order emptyOrder() {
    return new Order(List.of());
}
```

### Composable Operators

```java
static Order addPizza(Order order, Pizza pizza) {
    return new Order(
        Stream.concat(order.pizzas().stream(), Stream.of(pizza)).toList()
    );
}

static Order addToppingToLast(Order order, Topping t) {
    var pizzas = order.pizzas();
    if (pizzas.isEmpty()) return order;
    var last = pizzas.get(pizzas.size() - 1);
    var updated = new Pizza(last.name(), last.basePrice(),
        Stream.concat(last.toppings().stream(), Stream.of(t)).toList());
    var newList = Stream.concat(
        pizzas.stream().limit(pizzas.size() - 1),
        Stream.of(updated)
    ).toList();
    return new Order(newList);
}

static double total(Order order) {
    return order.pizzas().stream()
        .mapToDouble(p -> p.basePrice()
            + p.toppings().stream().mapToDouble(Topping::extra).sum())
        .sum();
}
```

### Solution: Operatoren zur Lösung zusammensetzen

Die einzelnen Operatoren werden zu einer Pipeline verkettet, die das Endergebnis erzeugt.

```java
var order = emptyOrder();
order = addPizza(order, margherita());
order = addToppingToLast(order, new Topping("Salami", 2.5));
order = addPizza(order, new Pizza("Funghi", 13.0, List.of()));

double preis = total(order); // 27.5
```

Jeder Operator gibt eine neue `Order` zurück. Die Variable `order` wird durch Reassignment auf den jeweils nächsten Zustand gesetzt, ohne dass je ein Objekt mutiert wird.

---

## Functional Design anwenden

Das Functional-Design-Schema umfasst fünf Elemente: **Domain of Interest**, **Model**, **Immutable Data Types**, **Constructors** und **Composable Operators**. Eine vollständige Lösung füllt alle fünf aus. Hier ist das selbst gewählte Pizza-Problem nach dem Schema durchformuliert.

### Vollständige Lösung nach Schema

| Element | Im Pizza-Beispiel |
| ------- | ----------------- |
| **Domain of Interest** | Eine Pizzeria nimmt Bestellungen entgegen. Jede Bestellung besteht aus mehreren Pizzen, optional mit Toppings. Aus Basispreis und Aufpreisen entsteht der Gesamtpreis. |
| **Model** | Eine Bestellung wird als Kette von Constructor- und Operator-Aufrufen auf `Order` modelliert. Der Endwert entsteht durch den terminalen Operator `total`. |
| **Immutable Data Types** | `Topping`, `Pizza`, `Order` (alle als Java Records, ohne Setter) |
| **Constructors** | `margherita()` für eine Standard-Pizza, `emptyOrder()` für eine leere Bestellung |
| **Composable Operators** | `addPizza`, `addToppingToLast` (beide `Order -> Order`), `total` (terminaler Operator) |

### Solution als Pseudocode

Die fertige Lösung lässt sich als einzige verschachtelte Komposition lesen:

```text
preis = total(
          addPizza(
            addToppingToLast(
              addPizza(emptyOrder(), margherita()),
              salami
            ),
            funghi
          )
        )
```

Die schrittweise Verkettung im Java-Code (mit Reassignment) und die verschachtelte Komposition im Pseudocode sind äquivalent.

### Was das Schema garantiert

- **Vollständigkeit:** Jede Spalte der Tabelle ist gefüllt, kein Element fehlt.
- **Konsistenz:** Constructors und Operators arbeiten auf denselben Typen, alles passt zusammen.
- **Erweiterbarkeit:** Neue Operatoren (z.B. `removePizza`, `applyDiscount`) können hinzugefügt werden, ohne bestehende zu ändern.

---

## Verwandte Kompetenzen

| Band | Bezug | Link |
| ---- | ----- | ---- |
| **BG2** | Erklärt die Grundelemente des Functional Design (Domain, Model, Solution, Constructors, Operators), die in BF2 angewendet werden | [BG2 Theorie](https://seismix.github.io/m323-trogawa/B/BG2/BG2_theorie/) |
| **BE2** | Setzt auf BF2 auf und transferiert imperatives Design in das hier entworfene funktionale Design | [BE2 Theorie](https://seismix.github.io/m323-trogawa/B/BE2/BE2_theorie/) |
