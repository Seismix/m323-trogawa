---
title: "C2F"
parent: "C - Umsetzung"
nav_order: 5
---

# C2F: Higher-Order Functions erstellen

> *Ich kann Funktionen als Argumente für andere Funktionen verwenden und dadurch höherwertige Funktionen erstellen.*

## Lernziele

| # | Lernziel | Beantwortet in |
| --- | ---------- | -------------- |
| 1 | Ich kann eine Funktion schreiben, die eine andere Funktion als Parameter entgegennimmt und aufruft. | [1. Funktion als Argument übergeben](#1-funktion-als-argument-übergeben) |
| 2 | Ich kann eine eigene Higher-Order Function implementieren (z.B. eine eigene `apply`-Funktion). | [2. Eigene Higher-Order Function schreiben](#2-eigene-higher-order-function-schreiben) |
| 3 | Ich kann das Callback-Muster mit Higher-Order Functions umsetzen, um flexiblen, wiederverwendbaren Code zu schreiben. | [3. Callback-Muster anwenden](#3-callback-muster-anwenden) |

---

## 1. Funktion als Argument übergeben

Eine **Higher-Order Function** ist eine Funktion, die mindestens eine Funktion als Argument entgegennimmt oder eine Funktion als Rückgabewert liefert.

```java
static int applyTwice(Function<Integer, Integer> func, int value) {
    return func.apply(func.apply(value));
}

System.out.println(applyTwice(x -> x + 3, 7));   // 13  (7→10→13)
System.out.println(applyTwice(x -> x * 2, 5));    // 20  (5→10→20)
```

`applyTwice` ist eine Higher-Order Function, weil sie eine `Function<Integer, Integer>` als Parameter entgegennimmt. Die konkrete Logik wird erst beim Aufruf festgelegt.

### Bekannte Higher-Order Functions in Java

Die Stream API besteht fast nur aus Higher-Order Functions:

| Methode | Funktionsargument | Zweck |
| ------- | ----------------- | ----- |
| `map()` | `Function<T, R>` | Jedes Element transformieren |
| `filter()` | `Predicate<T>` | Elemente nach Kriterium auswählen |
| `sorted()` | `Comparator<T>` | Sortierreihenfolge festlegen |
| `forEach()` | `Consumer<T>` | Aktion pro Element ausführen |
| `reduce()` | `BinaryOperator<T>` | Alle Elemente zusammenfassen |

---

## 2. Eigene Higher-Order Function schreiben

### Eigenes `applyToAll` (wie `map`, aber ohne Streams)

```java
static List<Integer> applyToAll(List<Integer> list, Function<Integer, Integer> func) {
    var result = new ArrayList<Integer>();
    for (var item : list) {
        result.add(func.apply(item));
    }
    return result;
}

var numbers = List.of(1, 2, 3, 4);
var doubled = applyToAll(numbers, x -> x * 2);      // [2, 4, 6, 8]
var squared = applyToAll(numbers, x -> x * x);       // [1, 4, 9, 16]
var negated = applyToAll(numbers, x -> -x);           // [-1, -2, -3, -4]
```

Die gleiche Funktion `applyToAll` kann drei völlig verschiedene Operationen ausführen, weil die Logik von aussen übergeben wird.

### Funktion zurückgeben: `createMultiplier`

```java
static Function<Integer, Integer> createMultiplier(int factor) {
    return x -> x * factor;
}

var doubler = createMultiplier(2);
var tripler = createMultiplier(3);

System.out.println(doubler.apply(5));  // 10
System.out.println(tripler.apply(5));  // 15
```

`createMultiplier` ist eine Higher-Order Function, weil sie eine Funktion zurückgibt. Das Lambda `x -> x * factor` bildet einen Closure über den Parameter `factor`.

---

## 3. Callback-Muster anwenden

Beim Callback-Muster übergibt man eine Funktion, die zu einem bestimmten Zeitpunkt aufgerufen wird. Das ermöglicht flexiblen, wiederverwendbaren Code.

### Beispiel: Listenverarbeitung mit Logging

```java
static <T> List<T> processWithCallback(
        List<T> items,
        Predicate<T> filter,
        Consumer<T> onMatch) {
    var result = new ArrayList<T>();
    for (var item : items) {
        if (filter.test(item)) {
            onMatch.accept(item);
            result.add(item);
        }
    }
    return result;
}

var numbers = List.of(1, 2, 3, 4, 5, 6, 7, 8);

// Callback: Treffer auf der Konsole ausgeben
var even = processWithCallback(
    numbers,
    x -> x % 2 == 0,
    x -> System.out.println("Gefunden: " + x)
);
// Gefunden: 2
// Gefunden: 4
// Gefunden: 6
// Gefunden: 8
```

### Beispiel: Flexible Validierung

```java
static boolean validateAll(List<String> inputs, Predicate<String> rule) {
    return inputs.stream().allMatch(rule);
}

var emails = List.of("a@b.ch", "c@d.com", "e@f.org");

var allContainAt = validateAll(emails, s -> s.contains("@"));     // true
var allDotCh     = validateAll(emails, s -> s.endsWith(".ch"));   // false
```

Die Validierungslogik wird per Callback übergeben. `validateAll` selbst muss nicht wissen, welche Regel geprüft wird.
