---
title: "AF1"
parent: "A - Paradigmen"
nav_order: 2
---

# AF1: Immutable Values erläutern

> *Ich kann das Konzept von immutable values erläutern und dazu Beispiele anwenden. Somit kann ich dieses Konzept funktionaler Programmierung im Unterschied zu anderen Programmiersprachen erklären (z.Bsp. im Vergleich zu referenzierten Objekten).*

## Lernziele

| # | Lernziel | Beantwortet in |
|---|----------|----------------|
| 1 | Ich kann erklären, was Immutability bedeutet, und an einem Java-Beispiel zeigen, wie immutable Werte funktionieren. | [Was ist Immutability?](#was-ist-immutability) |
| 2 | Ich kann erklären, warum referenzierte Objekte in OO-Sprachen problematisch sein können und wie Immutability dieses Problem löst. | [Das Aliasing-Problem](#das-aliasing-problem) |
| 3 | Ich kann in gegebenem Code erkennen, ob eine Mutation vorliegt, und die funktionale Alternative zeigen. | [Das Aliasing-Problem](#das-aliasing-problem) |

---

## Was ist Immutability?

**Immutability** bedeutet, dass ein Wert nach seiner Erstellung **nicht mehr verändert** werden kann. Statt einen bestehenden Wert zu ändern, erstellt man einen neuen.

### Immutability in Java

Java bietet mehrere Mechanismen, um Immutability durchzusetzen:

| Mechanismus | Beschreibung | Beispiel |
|-------------|-------------|----------|
| **`final`** | Verhindert die Neuzuweisung einer Variable. | `final int x = 5;` |
| **`record`** | Erzeugt eine Klasse mit unveränderlichen Feldern. | `record Point(int x, int y) {}` |
| **`List.of()`** | Erstellt eine unveränderbare Liste. | `List.of(1, 2, 3)` |
| **`String`** | Strings sind in Java immer immutable. | `"hello".toUpperCase()` erzeugt einen neuen String |

### Beispiel: `record` vs. Klasse mit Settern

```java
// Immutable: record hat keine Setter, Felder sind final
record Product(String name, double price) {}

var apple = new Product("Apfel", 1.50);
// apple.name = "Birne";  // Kompilierfehler! Felder sind final.
```

```java
// Mutable: klassische Klasse mit Settern
class MutableProduct {
    String name;
    double price;

    MutableProduct(String name, double price) {
        this.name = name;
        this.price = price;
    }
}

var apple = new MutableProduct("Apfel", 1.50);
apple.name = "Birne"; // Erlaubt, aber gefährlich: das Original wird verändert.
```

Bei einem `record` erzwingt der Compiler Immutability. Man kann das Objekt nach der Erstellung nicht mehr verändern.

### Unveränderbare Collections

```java
// Immutable: List.of() erlaubt keine Änderungen
var numbers = List.of(1, 2, 3);
numbers.add(4); // UnsupportedOperationException zur Laufzeit!

// Neues Ergebnis erzeugen statt mutieren
var moreNumbers = Stream.concat(numbers.stream(), Stream.of(4)).toList();
// => [1, 2, 3, 4], numbers bleibt [1, 2, 3]
```

---

## Mutable vs. Immutable in Java

| Mutable (veränderbar) | Immutable (unveränderbar) |
|----------------------|--------------------------|
| `ArrayList` | `List.of()`, `Collections.unmodifiableList()` |
| `HashMap` | `Map.of()`, `Collections.unmodifiableMap()` |
| Klasse mit Settern | `record` |
| `StringBuilder` | `String` |

### Vergleich im Code

```java
// Mutable: ArrayList wird direkt verändert
var numbers = new ArrayList<>(List.of(1, 2, 3));
numbers.add(4);       // numbers ist jetzt [1, 2, 3, 4]
System.out.println(numbers); // => [1, 2, 3, 4]

// Immutable: String kann nicht verändert werden
var text = "hello";
var textNeu = text.toUpperCase(); // Erstellt einen neuen String
System.out.println(text);         // => "hello" (Original unverändert)
System.out.println(textNeu);      // => "HELLO"
```

### Vorteile von Immutability

| Vorteil | Erklärung |
|---------|-----------|
| **Vorhersagbarkeit** | Wenn sich Werte nie ändern, gibt es keine Überraschungen. |
| **Thread-Sicherheit** | Unveränderbare Daten können ohne Locks parallel gelesen werden. |
| **Einfacheres Debugging** | Man muss nicht suchen, wo ein Wert ungewollt geändert wurde. |
| **Compiler-Garantien** | `record` und `final` werden vom Compiler überprüft, nicht nur per Konvention. |

---

## Das Aliasing-Problem

In Java zeigen Variablen auf **dasselbe Objekt im Speicher** (Referenzsemantik). Wenn mehrere Variablen auf dasselbe Objekt zeigen, kann eine Änderung über eine Variable alle anderen unbeabsichtigt beeinflussen.

### Das Problem in Aktion

```java
var original = new ArrayList<>(List.of(1, 2, 3));
var kopie = original; // Keine echte Kopie, nur eine zweite Referenz!

kopie.add(4);

System.out.println(original); // => [1, 2, 3, 4]  (unbeabsichtigt verändert!)
System.out.println(kopie);    // => [1, 2, 3, 4]
```

Beide Variablen zeigen auf **dieselbe** Liste. Eine Änderung über `kopie` betrifft auch `original`.

### Konkretes Beispiel: Warenkorb

```java
// Problematisch: verändert die originale Liste
List<String> addItem(List<String> cart, String item) {
    cart.add(item);
    return cart;
}

var warenkorb = new ArrayList<>(List.of("Brot", "Milch"));
var neuerWarenkorb = addItem(warenkorb, "Käse");

System.out.println(warenkorb);       // => [Brot, Milch, Käse]  (ungewollt verändert!)
System.out.println(neuerWarenkorb);  // => [Brot, Milch, Käse]
```

### Funktionale Lösung mit Immutability

```java
// Funktional: erstellt eine neue Liste, Original bleibt unverändert
List<String> addItem(List<String> cart, String item) {
    return Stream.concat(cart.stream(), Stream.of(item)).toList();
}

var warenkorb = List.of("Brot", "Milch");
var neuerWarenkorb = addItem(warenkorb, "Käse");

System.out.println(warenkorb);       // => [Brot, Milch]  (unverändert!)
System.out.println(neuerWarenkorb);  // => [Brot, Milch, Käse]
```

`Stream.concat(...).toList()` erzeugt eine **neue**, unveränderbare Liste. Das Original bleibt unangetastet. Genau das ist das Prinzip der funktionalen Programmierung: statt Daten zu verändern, neue Werte erzeugen. In Java wird dieses Prinzip durch `record`, `List.of()` und die Stream API vom Compiler und der Laufzeit durchgesetzt.
