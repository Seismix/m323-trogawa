---
title: "C1E"
parent: "C - Umsetzung"
nav_order: 3
---

# C1E: Funktionen in Algorithmen implementieren

> *Ich kann Funktionen in zusammenhängende Algorithmen implementieren.*

## Lernziele

| # | Lernziel | Beantwortet in |
| ------ | ------ | ------ |
| 1 | Ich kann eine Verarbeitungspipeline aus verketteten Funktionen implementieren, die Daten schrittweise transformiert. | [1. Pipeline erstellen](#1-pipeline-erstellen) |
| 2 | Ich kann mehrere kleine Funktionen zu einem zusammenhängenden Algorithmus komponieren. | [2. Komposition umsetzen](#2-komposition-umsetzen) |
| 3 | Ich kann mit einem Stream eine zusammenhängende Verarbeitung bauen: zuerst filter auf die Kategorie food, dann map mit Rabatt, dann reduce zur Summe. | [3. Zusammenhängende funktionale Pipeline](#3-zusammenhängende-funktionale-pipeline) |

---

## 1. Pipeline erstellen

Eine **Pipeline** ist eine Kette von Funktionen, bei der die Ausgabe einer Funktion zur Eingabe der nächsten wird. Daten werden schrittweise transformiert, ohne dass Zwischenzustände extern verwaltet werden müssen.

```text
Eingabe ──▶ [ Schritt 1 ] ──▶ [ Schritt 2 ] ──▶ [ Schritt 3 ] ──▶ Ergebnis
              transformiert    transformiert    transformiert
```

Drei wesentliche Eigenschaften einer Pipeline:

| Eigenschaft | Bedeutung |
| ------ | ------ |
| **Unidirektional** | Daten fliessen nur in eine Richtung, kein Rücksprung |
| **Zustandslos** | Jeder Schritt arbeitet nur mit seiner Eingabe, kein gemeinsamer Zustand |
| **Komponierbar** | Schritte können neu zusammengestellt oder ersetzt werden |

### Vorher: imperative Schleifen-Variante

```java
static List<String> processTextImperative(String text) {
    var words = text.split("\\s+");
    var lower = new ArrayList<String>();
    for (var w : words) {
        lower.add(w.toLowerCase());
    }
    var seen = new HashSet<String>();
    var unique = new ArrayList<String>();
    for (var w : lower) {
        if (seen.add(w)) {
            unique.add(w);
        }
    }
    Collections.sort(unique);
    return unique;
}
```

Drei Hilfslisten, zwei Schleifen, ein Set zur Duplikaterkennung: der eigentliche Algorithmus verschwindet hinter Buchhaltung.

### Nachher: Pipeline mit Stream

```java
static List<String> processText(String text) {
    return Arrays.stream(text.split("\\s+"))
        .map(String::toLowerCase)
        .distinct()
        .sorted()
        .toList();
}

public static void main(String[] args) {
    var result = processText("Java ist toll Java ist funktional");
    System.out.println(result);
    // [funktional, ist, java, toll]
}
```

Jeder Schritt in der Kette hat eine klare Aufgabe und arbeitet auf dem Ergebnis des vorherigen Schritts.

| Schritt | Eingabe | Ausgabe |
| ------ | ------ | ------ |
| `split` | `"Java ist toll Java ist funktional"` | `["Java", "ist", "toll", "Java", "ist", "funktional"]` |
| `toLowerCase` | gemischte Schreibweise | nur Kleinbuchstaben |
| `distinct` | mit Duplikaten | ohne Duplikate |
| `sorted` | unsortiert | alphabetisch sortiert |

Gegenüber der imperativen Variante fällt der Ballast weg: keine Hilfslisten, kein manuelles Duplikat-Set, keine separate `sort`-Anweisung. Der Code beschreibt **was** passiert, nicht **wie**.

---

## 2. Komposition umsetzen

**Funktionskomposition** verkettet einzelne Funktionen zu einer neuen Gesamtfunktion. In Java bietet `Function<T, R>` dafür zwei Methoden:

| Methode | Bedeutung | Mathematisch |
| ------ | ------ | ------ |
| `f.andThen(g)` | erst `f`, dann `g` auf das Ergebnis | `g(f(x))` |
| `f.compose(g)` | erst `g`, dann `f` auf das Ergebnis | `f(g(x))` |

```java
public static void main(String[] args) {
    Function<Integer, Integer> doubleIt = x -> x * 2;
    Function<Integer, Integer> addOne   = x -> x + 1;

    System.out.println(doubleIt.andThen(addOne).apply(3));  // (3*2)+1 = 7
    System.out.println(doubleIt.compose(addOne).apply(3));  // (3+1)*2 = 8
}
```

Die Reihenfolge ist relevant: `f(g(x))` ist in der Regel nicht gleich `g(f(x))`.

### Pipeline aus eigenständigen Funktionen zusammensetzen

```java
public static void main(String[] args) {
    Function<String, List<String>> extractWords = s -> List.of(s.split("\\s+"));
    Function<List<String>, List<String>> toLower = words ->
        words.stream().map(String::toLowerCase).toList();
    Function<List<String>, List<String>> unique = words ->
        words.stream().distinct().toList();
    Function<List<String>, List<String>> sort = words ->
        words.stream().sorted().toList();

    var pipeline = extractWords
        .andThen(toLower)
        .andThen(unique)
        .andThen(sort);

    System.out.println(pipeline.apply("Java ist toll Java ist funktional"));
    // [funktional, ist, java, toll]
}
```

Jede Teilfunktion ist isoliert testbar und kann in anderen Pipelines wiederverwendet werden.

### Komposition vs. manuelle Verkettung

Statt jeden Schritt einzeln aufzurufen (`sort(unique(toLower(extractWords(s))))`), wird die Pipeline einmal als Wert komponiert und kann beliebig oft angewendet werden:

| Variante | Code | Eigenschaft |
| ------ | ------ | ------ |
| Manuell verschachtelt | `sort(unique(toLower(extractWords(s))))` | schwer lesbar, Reihenfolge von innen nach aussen |
| Stream-Kette | `stream.map(...).distinct().sorted()` | nur einmal anwendbar, gebunden an Datenquelle |
| Komponierte Function | `extractWords.andThen(toLower).andThen(unique).andThen(sort)` | wiederverwendbarer Wert, mehrfach anwendbar |

### Typische Stolpersteine

| Stolperstein | Folge | Lösung |
| ------ | ------ | ------ |
| `andThen` und `compose` verwechselt | falsches Ergebnis, keine Compilerfehler | merken: `andThen` = von links nach rechts |
| Pipeline mit Seiteneffekten in `map` | Reihenfolge oder parallele Ausführung führen zu Bugs | `map` nur für reine Transformation, `forEach` für Seiteneffekte |
| Zwischenergebnisse in Variablen ablegen | Pipeline-Charakter geht verloren | direkt komponieren, nur am Anfang/Ende benennen |

---

## 3. Zusammenhängende funktionale Pipeline

Streams sind das natürliche Werkzeug für Pipelines: `filter`, `map` und `reduce` bilden zusammen den klassischen Dreischritt der funktionalen Datenverarbeitung.

### Beispiel: Rabatt auf Lebensmittel und Summe

```java
record Item(String name, String category, double price) {}

public static void main(String[] args) {
    var cart = List.of(
        new Item("Brot",     "food",  4.50),
        new Item("Buch",     "media", 19.90),
        new Item("Apfel",    "food",  1.20),
        new Item("Kopfhörer","tech",  89.00),
        new Item("Käse",     "food",  6.80)
    );

    double total = cart.stream()
        .filter(i -> i.category().equals("food"))   // nur Lebensmittel
        .mapToDouble(i -> i.price() * 0.90)         // 10 % Rabatt
        .sum();                                     // reduce zur Summe

    System.out.println(total);  // 11.25
}
```

| Schritt | Rolle | Auswirkung |
| ------ | ------ | ------ |
| `filter(category=="food")` | Auswahl | nur Brot, Apfel, Käse |
| `map(price * 0.90)` | Transformation | Preise mit Rabatt |
| `sum()` / `reduce` | Aggregation | ein einziger Endwert |

Die drei Schritte bilden das **Grundmuster jeder funktionalen Datenverarbeitung**:

```text
Liste<T>  ── filter ──▶  Liste<T>  ── map ──▶  Liste<U>  ── reduce ──▶  Wert
 (Auswahl)              (gefiltert)         (transformiert)           (aggregiert)
```

Die `reduce`-Variante mit explizitem Akkumulator macht die Aggregation noch sichtbarer:

```java
double total = cart.stream()
    .filter(i -> i.category().equals("food"))
    .mapToDouble(i -> i.price() * 0.90)
    .reduce(0.0, Double::sum);   // identisch zu .sum(), nur explizit
```

`Double::sum` ist die Reduktionsfunktion, `0.0` der Startwert. Damit ist klar erkennbar, dass `reduce` zwei Werte zu einem neuen kombiniert, bis nur ein einziger übrig ist.

### Mehrere Methoden in `main` verbinden

Eine Pipeline lässt sich auch aus benannten Methoden bauen, die in `main` zu einem vollständigen Algorithmus verkettet werden:

```java
class Shop {
    static List<Item> onlyFood(List<Item> items) {
        return items.stream()
            .filter(i -> i.category().equals("food"))
            .toList();
    }

    static List<Item> applyDiscount(List<Item> items, double rate) {
        return items.stream()
            .map(i -> new Item(i.name(), i.category(), i.price() * (1 - rate)))
            .toList();
    }

    static double total(List<Item> items) {
        return items.stream().mapToDouble(Item::price).sum();
    }

    public static void main(String[] args) {
        var cart = List.of(
            new Item("Brot",     "food",  4.50),
            new Item("Buch",     "media", 19.90),
            new Item("Apfel",    "food",  1.20),
            new Item("Kopfhörer","tech",  89.00),
            new Item("Käse",     "food",  6.80)
        );

        var food       = onlyFood(cart);
        var discounted = applyDiscount(food, 0.10);
        var sum        = total(discounted);
        System.out.println(sum);  // 11.25
    }
}
```

`main` fungiert als Dirigent: jede Methode erfüllt genau eine Aufgabe, und ihre Verkettung ergibt den vollständigen Algorithmus.

In `applyDiscount` wird absichtlich ein **neues** `Item` erzeugt, statt den Preis im bestehenden Objekt zu überschreiben (Java-Records sind ohnehin unveränderlich). So bleibt die Eingabe der Pipeline unverändert, jede Stufe liefert einen neuen Wert weiter, und Tests können jeden Schritt isoliert prüfen.

### Erweiterung: Bericht statt Zahl

Pipelines lassen sich nahtlos verlängern, sobald sich die Anforderung ändert. Soll statt einer Zahl ein Bericht entstehen, kommt einfach ein weiterer Mapping- und Reduktionsschritt dazu:

```java
class ShopReport {
    record Item(String name, String category, double price) {}

    static List<Item> onlyFood(List<Item> items) {
        return items.stream()
            .filter(i -> i.category().equals("food"))
            .toList();
    }

    static List<Item> applyDiscount(List<Item> items, double rate) {
        return items.stream()
            .map(i -> new Item(i.name(), i.category(), i.price() * (1 - rate)))
            .toList();
    }

    static String formatLine(Item i) {
        return "%-10s CHF %.2f".formatted(i.name(), i.price());
    }

    static String buildReport(List<Item> items) {
        var lines = items.stream().map(ShopReport::formatLine).toList();
        var total = items.stream().mapToDouble(Item::price).sum();
        return String.join("\n", lines) + "\n---\nTotal: CHF %.2f".formatted(total);
    }

    public static void main(String[] args) {
        var cart = List.of(
            new Item("Brot",     "food",  4.50),
            new Item("Buch",     "media", 19.90),
            new Item("Apfel",    "food",  1.20),
            new Item("Kopfhörer","tech",  89.00),
            new Item("Käse",     "food",  6.80)
        );

        var report = buildReport(applyDiscount(onlyFood(cart), 0.10));
        System.out.println(report);
    }
}
```

Erwartete Ausgabe:

```text
Brot       CHF 4.05
Apfel      CHF 1.08
Käse       CHF 6.12
---
Total: CHF 11.25
```

Die ursprüngliche Pipeline `onlyFood → applyDiscount → total` wird zu `onlyFood → applyDiscount → buildReport`. Zwei kleine, neue Funktionen (`formatLine`, `buildReport`), keine Änderung an den bestehenden, ein erweiterter Algorithmus.

### Was C1E zusammenbringt

| Element | Beitrag zum Algorithmus |
| ------ | ------ |
| Kleine Funktionen (`onlyFood`, `applyDiscount`, `total`, `formatLine`) | Bausteine mit je einer Verantwortung |
| Funktionskomposition (`andThen`, verschachtelte Aufrufe) | Bausteine zu einer Pipeline verbinden |
| Stream mit `filter/map/reduce` | Daten als Sequenz transformieren und aggregieren |
| `main` als Dirigent | Pipeline anstossen, Eingabe liefern, Ergebnis ausgeben |

Genau dieses Zusammenspiel meint die Kompetenz C1E: aus vielen kleinen Funktionen einen vollständigen, zusammenhängenden Algorithmus bauen.
