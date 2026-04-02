---
title: "AG1"
parent: "A - Paradigmen"
nav_order: 1
---

# AG1: Eigenschaften von Funktionen beschreiben

> *Ich kann die Eigenschaften von Funktionen beschreiben (z.Bsp. pure function) und den Unterschied zu anderen Programmier-Strukturen erläutern (z.Bsp. zu Prozedur).*

## Lernziele

| # | Lernziel | Beantwortet in |
| --- | ---------- | ---------------- |
| 1 | Ich kann erklären, was eine Pure Function ist und welche zwei Eigenschaften sie erfüllen muss. | [Was ist eine Pure Function?](#was-ist-eine-pure-function) |
| 2 | Ich kann den Unterschied zwischen einer Funktion und einer Prozedur anhand von Codebeispielen erläutern. | [Funktion vs. Prozedur](#funktion-vs-prozedur) |
| 3 | Ich kann in gegebenem Code erkennen, ob eine Funktion pure ist, und meine Einschätzung begründen. | [Seiteneffekte erkennen](#seiteneffekte-erkennen) |

---

## Was ist eine Pure Function?

Eine Pure Function ist eine Funktion, die **zwei Eigenschaften** gleichzeitig erfüllt:

| Eigenschaft | Beschreibung | Beispiel |
| ------------- | ------------- | ---------- |
| **Determinismus** | Bei gleichem Input kommt immer der gleiche Output zurück. | `double(3)` ergibt immer `6` |
| **Keine Seiteneffekte** | Die Funktion verändert keinen Zustand ausserhalb ihrer selbst. | Kein `System.out.println()`, keine Feldänderungen, keine Dateizugriffe |

```java
// Pure Function: gleicher Input, gleicher Output, keine Seiteneffekte
int double(int x) {
    return x * 2;
}

double(3); // => 6 (immer)
double(3); // => 6 (immer)
```

```java
// NICHT pure: verändert externen Zustand und gibt bei gleichem Input unterschiedliche Ergebnisse
class Counter {
    int total = 0;

    int addToTotal(int x) {
        total += x;
        return total;
    }
}

var counter = new Counter();
counter.addToTotal(3); // => 3
counter.addToTotal(3); // => 6 (gleicher Input, anderer Output!)
```

`addToTotal` verletzt beide Eigenschaften: Sie verändert das Feld `total` (Seiteneffekt) und gibt bei gleichem Input (`3`) jedes Mal ein anderes Ergebnis zurück.

---

## Funktion vs. Prozedur

In der Programmierung unterscheidet man zwischen **Funktionen** und **Prozeduren**:

| | Funktion | Prozedur |
| --- | --------- | ---------- |
| **Rückgabewert** | Gibt einen Wert zurück | Gibt keinen Wert zurück (`void`) |
| **Seiteneffekte** | Idealerweise keine | Hat typischerweise Seiteneffekte |
| **Zweck** | Berechnung eines Ergebnisses | Ausführung einer Aktion |
| **Beispiel** | `"hello".length()` ergibt `5` | `System.out.println("hello")` gibt Text aus |

```java
// Funktion: nimmt Input, gibt Output zurück
int calculateArea(int width, int height) {
    return width * height;
}

var result = calculateArea(5, 3); // => 15

// Prozedur: führt eine Aktion aus, kein Rückgabewert (void)
void displayArea(int width, int height) {
    System.out.println("Die Fläche beträgt " + (width * height) + " m²");
}

displayArea(5, 3); // Gibt Text aus, kein Rückgabewert
```

In Java ist der Unterschied syntaktisch sichtbar: Funktionen haben einen Rückgabetyp (`int`, `String`, ...), Prozeduren sind `void`. In der funktionalen Programmierung arbeitet man bevorzugt mit Funktionen (mit Rückgabewert, ohne Seiteneffekte).

---

## Seiteneffekte erkennen

Ein **Seiteneffekt** (Side Effect) ist jede Veränderung, die eine Methode ausserhalb ihres eigenen Scopes bewirkt:

- Felder oder statische Variablen verändern
- Ausgabe auf dem Bildschirm (`System.out.println`)
- In eine Datei oder Datenbank schreiben
- Eine Netzwerkanfrage senden

### Beispiel: Welche Methode ist pure?

```java
class Example {
    static int x = 0;

    static int a(int n) {
        return n + 1;
    }

    static int b(int n) {
        x += n;
        return x;
    }

    static int c(int n) {
        System.out.println(n);
        return n;
    }
}
```

| Methode | Pure? | Begründung |
| --------- | ------- | ------------ |
| `a(n)` | Ja | Gleicher Input ergibt immer gleichen Output, keine Seiteneffekte. |
| `b(n)` | Nein | Verändert das statische Feld `x`. Bei gleichem Input kommen unterschiedliche Ergebnisse zurück (`b(1)` ergibt erst `1`, dann `2`, dann `3`...). |
| `c(n)` | Nein | `System.out.println()` ist ein Seiteneffekt (Konsolenausgabe). |

### Warum vermeidet funktionale Programmierung Seiteneffekte?

| Vorteil | Erklärung |
| --------- | ----------- |
| **Vorhersagbarkeit** | Pure Functions verhalten sich immer gleich, unabhängig vom restlichen Programmzustand. |
| **Testbarkeit** | Man muss keinen globalen Zustand aufsetzen, um eine Funktion zu testen. |
| **Parallelisierung** | Ohne gemeinsamen Zustand können Funktionen parallel ausgeführt werden, ohne Konflikte. |
