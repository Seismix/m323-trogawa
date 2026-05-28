---
title: "BE2"
parent: "B - Anforderungen & Design"
nav_order: 6
---

# BE2: Design transferieren

> *Ich kann ein Design einer imperativen Programmierung in ein Design der deklarativen Programmierung transferieren.*

## Lernziele

| # | Lernziel | Beantwortet in |
| --- | -------- | -------------- |
| 1 | In dieser Aufgabe überführe ich ein imperatives Design in ein deklaratives Design und zeige anhand eines Beispiels, wie das gewünschte Ergebnis statt der einzelnen Arbeitsschritte in den Mittelpunkt gestellt wird. | [Transfer von imperativem zu deklarativem Design](#transfer-von-imperativem-zu-deklarativem-design) |
| 2 | Ich kann in gegebenem imperativem Code die Schleifen und Zustandsvariablen identifizieren und erklären, was sie bewirken. | [Code analysieren](#code-analysieren) |
| 3 | Ich kann den imperativen Code in eine deklarative Variante umschreiben, indem ich filter(), map() und reduce() einsetze und den Unterschied begründen. | [Transfer durchführen](#transfer-durchführen) |
| 4 | Ich kann dieselbe Aufgabe (Summe der Quadrate) einmal imperativ mit Index-Schleife und einmal deklarativ mit Stream lösen und zeigen, dass das Ergebnis gleich ist. | [Imperatives vs. deklaratives Design](#imperatives-vs-deklaratives-design) |

---

## Transfer von imperativem zu deklarativem Design

Beim Transfer rückt der **gewünschte Endzustand** in den Vordergrund. Statt eine Abfolge von Anweisungen zu geben, beschreibt das deklarative Design das Ergebnis.

### Fokuswechsel

| Aspekt | Imperativ | Deklarativ |
| ------ | --------- | ---------- |
| Fokus | Wie wird es berechnet? | Was ist das Ergebnis? |
| Steuerung | Reihenfolge der Schritte ist im Code | Reihenfolge ist Sache der Laufzeitumgebung |
| Zustand | Akkumulator-Variablen, Schleifenindex | keine sichtbaren Zustandsvariablen |
| Composability | Methodenaufrufe auf demselben Objekt | Operatoren mit passenden Typen verkettbar |

### Beispiel im Mini-Format

**Aufgabe:** Aus einer Liste von Zahlen die geraden Quadrate aufsummieren.

**Imperatives Design:**

> Initialisiere `sum = 0`. Gehe über jedes Element der Liste. Wenn das Element gerade ist, quadriere es und addiere es zu `sum`. Gib `sum` zurück.

**Deklaratives Design:**

> Das Ergebnis ist die Summe aller Quadrate der geraden Zahlen aus der Liste.

Die deklarative Variante beschreibt nur das Endergebnis, nicht die Schritte. Schleife, Akkumulator und Indexvariable verschwinden.

---

## Code analysieren

Bevor ein imperatives Stück Code transferiert wird, muss klar sein, **welche Elemente** überhaupt vorhanden sind. Schleifen, Zustandsvariablen und Bedingungen sind die typischen Verdächtigen.

### Gegebener imperativer Code

```java
static int sumOfEvenSquares(int[] numbers) {
    int sum = 0;
    for (int i = 0; i < numbers.length; i++) {
        int n = numbers[i];
        if (n % 2 == 0) {
            int square = n * n;
            sum = sum + square;
        }
    }
    return sum;
}
```

### Identifizierte Elemente

| Code | Typ | Wirkung |
| ---- | --- | ------- |
| `int sum = 0;` | Zustandsvariable (Akkumulator) | Hält die laufende Summe über alle Iterationen hinweg |
| `int i = 0; i < numbers.length; i++` | Schleifenvariable (Index) | Steuert die Iteration und wählt jedes Element nacheinander aus |
| `numbers[i]` | Index-Zugriff | Liest das Element an Position `i` aus dem Array |
| `if (n % 2 == 0)` | Bedingung | Filtert: nur gerade Zahlen sollen weiter verarbeitet werden |
| `int square = n * n;` | Transformation | Berechnet das Quadrat eines Elements |
| `sum = sum + square;` | Mutation der Zustandsvariable | Aggregiert das aktuelle Quadrat in den Akkumulator |

### Was die Analyse zeigt

- Zwei Zustandsvariablen wandern durch die Schleife: `sum` (Akkumulator) und `i` (Index). Beide sind technisch notwendig, weil die imperative Schleife sonst keine Möglichkeit hätte, mehrere Elemente nacheinander zu verarbeiten.
- Die eigentliche Logik besteht aus drei Schritten: **filtern** (gerade Zahlen), **transformieren** (quadrieren) und **aggregieren** (summieren). Diese drei Schritte sind im imperativen Code nicht direkt sichtbar, sondern in die Schleife eingewoben.
- Diese drei Schritte sind genau das, was beim Transfer als filter(), map() und reduce() wieder auftaucht.

---

## Transfer durchführen

Sobald die Elemente erkannt sind, lässt sich der imperative Code direkt in eine Stream-Pipeline aus `filter()`, `map()` und `reduce()` umschreiben.

### Deklarative Variante

```java
static int sumOfEvenSquares(int[] numbers) {
    return Arrays.stream(numbers)
        .filter(n -> n % 2 == 0)      // filter
        .map(n -> n * n)              // map
        .reduce(0, Integer::sum);     // reduce
}
```

### Eins-zu-eins Zuordnung

| Imperatives Konstrukt | Deklaratives Äquivalent | Aufgabe |
| --------------------- | ----------------------- | ------- |
| `for (int i = 0; ...)` mit `numbers[i]` | `Arrays.stream(numbers)` | Sequenz erzeugen |
| `if (n % 2 == 0) { ... }` | `.filter(n -> n % 2 == 0)` | Elemente auswählen |
| `int square = n * n;` | `.map(n -> n * n)` | Element transformieren |
| `int sum = 0;` plus `sum = sum + square;` | `.reduce(0, Integer::sum)` | Werte zu einem Ergebnis aggregieren |

### Unterschied begründen

| Kriterium | Imperativ | Deklarativ |
| --------- | --------- | ---------- |
| **Sichtbare Zustandsvariablen** | `sum`, `i` | keine |
| **Lesbarkeit** | Was passiert in der Schleife? Mehrere Konzepte gemischt | Drei Operatoren, jeder mit einer einzigen Aufgabe |
| **Composability** | Schleife ist abgeschlossen, nicht wiederverwendbar | Jede Stufe ist ein eigener Operator, austauschbar |
| **Parallelisierung** | Schleife ist sequentiell vorgegeben | `.parallelStream()` macht die Pipeline parallel ohne Codeänderung |
| **Erweiterbarkeit** | weitere Bedingungen erfordern Schachtelung | weitere Bedingungen werden als zusätzliche `filter()`/`map()` angehängt |

Der Hauptgewinn ist, dass die drei Konzepte (filtern, transformieren, aggregieren) jetzt **getrennt benannt** im Code stehen. Das macht die Absicht sofort lesbar und erlaubt, einzelne Stufen zu ändern, ohne die anderen anzufassen.

---

## Imperatives vs. deklaratives Design

Als Capstone-Beispiel folgt die **Summe der Quadrate**, ein Klassiker, der den Transfer in seiner reinsten Form zeigt.

### Aufgabe

Aus einer Liste von Zahlen die Summe der Quadrate berechnen.

> Für `[1, 2, 3, 4, 5]` ist das Ergebnis 1 + 4 + 9 + 16 + 25 = **55**.

### Imperative Lösung (Index-Schleife)

```java
static int sumOfSquaresImperative(int[] numbers) {
    int sum = 0;
    for (int i = 0; i < numbers.length; i++) {
        sum = sum + numbers[i] * numbers[i];
    }
    return sum;
}
```

Zwei Zustandsvariablen: `sum` (Akkumulator) und `i` (Schleifenindex). Die Schleife steuert die Iteration explizit.

### Deklarative Lösung (Stream)

```java
static int sumOfSquaresDeclarative(int[] numbers) {
    return Arrays.stream(numbers)
        .map(n -> n * n)
        .sum();
}
```

Keine Zustandsvariable im Code, keine Schleife. Das Ergebnis wird direkt als Pipeline beschrieben: erzeuge einen Stream, quadriere jedes Element, summiere alles. Die Stream-Variante hat keinen sichtbaren Zwischenakkumulator: `IntStream.sum()` arbeitet intern wie `reduce(0, Integer::sum)` aus dem vorigen Abschnitt und aggregiert die Werte erst am Ende.

### Beide Varianten liefern dasselbe Ergebnis

```java
int[] input = {1, 2, 3, 4, 5};

int imperativ = sumOfSquaresImperative(input);    // 55
int deklarativ = sumOfSquaresDeclarative(input);  // 55

assert imperativ == deklarativ;
```

### Schritt-für-Schritt-Tabelle

| n | n² | Imperativ: `sum` nach Schritt | Deklarativ: map liefert |
| - | -- | ----------------------------- | ----------------------- |
| 1 | 1 | 0 + 1 = 1 | 1 |
| 2 | 4 | 1 + 4 = 5 | 4 |
| 3 | 9 | 5 + 9 = 14 | 9 |
| 4 | 16 | 14 + 16 = 30 | 16 |
| 5 | 25 | 30 + 25 = 55 | 25 |
| | | **Resultat: 55** | **sum() = 55** |

Beide Wege erreichen dasselbe Ziel. Die imperative Variante zeigt jeden Zwischenzustand des Akkumulators, die deklarative Variante zeigt jeden Zwischenwert nach der Transformation. Das Endergebnis ist in beiden Fällen 55, und das beweist die Korrektheit des Transfers.

### Warum der Transfer trotzdem etwas verändert

Auch wenn das **Ergebnis** identisch ist, ist das **Design** ein anderes:

- Die imperative Variante schreibt die **Reihenfolge** der Operationen fest (erst i=0, dann i=1, ...).
- Die deklarative Variante überlässt die Reihenfolge dem Stream. Mit `.parallelStream()` lässt sich die Berechnung über mehrere Threads verteilen, ohne den Code zu ändern.
- Aussagen wie "die Schleife darf nicht abbrechen, bevor `i == numbers.length`" sind im imperativen Design eine Invariante, die der Entwickler sicherstellen muss. Im deklarativen Design ist sie durch die Stream-API garantiert.

---

## Verwandte Kompetenzen

| Band | Bezug | Link |
| ---- | ----- | ---- |
| **BF2** | Definiert das Zielbild: wie ein Functional Design (Domain, Immutable Data Types, Constructors, Composable Operators) entworfen wird | [BF2 Theorie](https://seismix.github.io/m323-trogawa/B/BF2/BF2_theorie/) |
| **BG2** | Erklärt die Grundelemente des Functional Design, die das Ergebnis dieser Transformation bilden | [BG2 Theorie](https://seismix.github.io/m323-trogawa/B/BG2/BG2_theorie/) |
| **BE1** | Pendant auf Anforderungsebene: transferiert imperative Anforderungen statt imperatives Design | [BE1 Theorie](https://seismix.github.io/m323-trogawa/B/BE1/BE1_theorie/) |
| **C4F** | Kombiniert `filter()`, `map()` und `reduce()` zu Pipelines, das technische Werkzeug für den Transfer | [C4F Theorie](https://seismix.github.io/m323-trogawa/C/C4F/C4F_theorie/) |
