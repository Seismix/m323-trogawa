---
title: "C1E_Java"
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
| 3 | Ich kann mit einem Stream eine zusammenhängende Verarbeitung bauen: zuerst filter auf die Abteilung, dann map mit Gehaltserhöhung, dann reduce zur Budgetsumme. | [3. Zusammenhängende funktionale Pipeline](#3-zusammenhängende-funktionale-pipeline) |

---

## 1. Pipeline erstellen

Eine **Pipeline** verbindet mehrere Verarbeitungsschritte so, dass das Ergebnis eines Schritts direkt als Eingabe des nächsten dient. Daten durchlaufen die Kette ohne externe Zwischenspeicherung.

```text
Eingabe ──▶ [ Schritt 1 ] ──▶ [ Schritt 2 ] ──▶ [ Schritt 3 ] ──▶ Ergebnis
              bereinigen        normalisieren      deduplizieren
```

| Eigenschaft | Bedeutung |
| ------ | ------ |
| **Unidirektional** | Daten fliessen nur vorwärts, kein Rücksprung |
| **Zustandslos** | Jeder Schritt arbeitet ausschliesslich mit seiner Eingabe |
| **Komponierbar** | Schritte lassen sich austauschen oder ergänzen |

### Vorher: imperative Variante

```java
static List<String> buildTagList(List<String> rawTags) {
    var cleaned = new ArrayList<String>();
    for (var tag : rawTags) {
        var t = tag.strip().toLowerCase();
        if (!t.isEmpty()) {
            cleaned.add(t);
        }
    }
    var seen = new HashSet<String>();
    var unique = new ArrayList<String>();
    for (var t : cleaned) {
        if (seen.add(t)) unique.add(t);
    }
    Collections.sort(unique);
    return unique;
}
```

Vier Hilfsvariablen, zwei Schleifen, ein manuell gepflegtes Set: die eigentliche Absicht des Codes ist hinter Buchführung vergraben.

### Nachher: Pipeline mit Stream

```java
static List<String> buildTagList(List<String> rawTags) {
    return rawTags.stream()
        .map(String::strip)
        .map(String::toLowerCase)
        .filter(t -> !t.isEmpty())
        .distinct()
        .sorted()
        .toList();
}

public static void main(String[] args) {
    var result = buildTagList(List.of("Java ", "  java", "Streams", "", "JAVA"));
    System.out.println(result);
    // [java, streams]
}
```

Jeder Schritt in der Kette hat genau eine Aufgabe:

| Schritt | Eingabe | Ausgabe |
| ------ | ------ | ------ |
| `strip` | Rohtext mit Leerzeichen | bereinigter Text |
| `toLowerCase` | gemischte Schreibweise | nur Kleinbuchstaben |
| `filter` | alle Einträge | nur nicht-leere |
| `distinct` | mit Duplikaten | ohne Duplikate |
| `sorted` | unsortiert | alphabetisch |

Der Code beschreibt **was** passieren soll, nicht **wie** es technisch umgesetzt wird.

---

## 2. Komposition umsetzen

`Function<T, R>` in Java erlaubt es, Funktionen als Werte zu behandeln und mit `andThen` oder `compose` zu neuen Funktionen zu verbinden.

| Methode | Bedeutung | Mathematisch |
| ------ | ------ | ------ |
| `f.andThen(g)` | erst `f`, dann `g` auf das Ergebnis | `g(f(x))` |
| `f.compose(g)` | erst `g`, dann `f` auf das Ergebnis | `f(g(x))` |

```java
public static void main(String[] args) {
    Function<Integer, Integer> triple     = x -> x * 3;
    Function<Integer, Integer> subtractTwo = x -> x - 2;

    System.out.println(triple.andThen(subtractTwo).apply(4));   // (4*3)-2 = 10
    System.out.println(triple.compose(subtractTwo).apply(4));   // (4-2)*3 = 6
}
```

Die Reihenfolge ist entscheidend: `f(g(x))` ist in der Regel nicht gleich `g(f(x))`.

### Eingabe-Normalisierung als komponierte Pipeline

Benutzereingaben kommen oft uneinheitlich formatiert an. Mehrere kleine Funktionen lassen sich zu einer wiederverwendbaren Normalisierungs-Pipeline zusammenstellen:

```java
public static void main(String[] args) {
    Function<String, String> trim        = String::strip;
    Function<String, String> lower       = String::toLowerCase;
    Function<String, String> collapse    = s -> s.replaceAll("\\s+", " ");
    Function<String, String> removePunct = s -> s.replaceAll("[^a-z0-9 ]", "");

    var normalize = trim
        .andThen(lower)
        .andThen(collapse)
        .andThen(removePunct);

    System.out.println(normalize.apply("  Hello,   World!  "));
    // "hello world"
    System.out.println(normalize.apply("  Java  8  Streams!!  "));
    // "java 8 streams"
}
```

Jede Teilfunktion ist isoliert testbar. Die zusammengesetzte `normalize`-Funktion ist ein eigenständiger Wert, der beliebig oft auf unterschiedliche Eingaben angewendet werden kann.

### Kompositionsvergleich

| Variante | Code | Eigenschaft |
| ------ | ------ | ------ |
| Manuell verschachtelt | `removePunct(collapse(lower(trim(s))))` | schwer lesbar, Reihenfolge von innen nach aussen |
| Stream-Kette | `stream.map(trim).map(lower)...` | einmalig, an Datenquelle gebunden |
| Komponierte Function | `trim.andThen(lower).andThen(...)` | wiederverwendbarer Wert, mehrfach anwendbar |

### Typische Stolpersteine

| Stolperstein | Folge | Lösung |
| ------ | ------ | ------ |
| `andThen` und `compose` verwechselt | falsches Ergebnis, kein Compilerfehler | merken: `andThen` = von links nach rechts |
| Seiteneffekte in `map` | unvorhersehbare Reihenfolge bei paralleler Ausführung | `map` nur für reine Transformation, `forEach` für Seiteneffekte |
| Zwischenergebnisse in Variablen benennen | Pipeline-Charakter geht verloren | direkt komponieren, nur Anfang und Ende benennen |

---

## 3. Zusammenhängende funktionale Pipeline

`filter`, `map` und `reduce` bilden zusammen das klassische Grundmuster der funktionalen Datenverarbeitung.

### Beispiel: Gehaltserhöhung für eine Abteilung

```java
record Employee(String name, String department, double salary) {}

public static void main(String[] args) {
    var staff = List.of(
        new Employee("Anna",  "engineering", 80_000),
        new Employee("Ben",   "marketing",   65_000),
        new Employee("Clara", "engineering", 92_000),
        new Employee("David", "support",     58_000),
        new Employee("Eva",   "engineering", 74_000)
    );

    double budget = staff.stream()
        .filter(e -> e.department().equals("engineering"))  // nur Engineering
        .mapToDouble(e -> e.salary() * 1.10)                // 10 % Erhöhung
        .sum();                                             // Gesamtbudget

    System.out.println(budget);  // 270600.0
}
```

| Schritt | Rolle | Auswirkung |
| ------ | ------ | ------ |
| `filter(department == "engineering")` | Auswahl | Anna, Clara, Eva |
| `map(salary * 1.10)` | Transformation | Gehälter mit Erhöhung |
| `sum()` / `reduce` | Aggregation | ein einziger Endwert |

Die drei Schritte bilden das **Grundmuster jeder funktionalen Datenverarbeitung**:

```text
Liste<T>  ── filter ──▶  Liste<T>  ── map ──▶  Liste<U>  ── reduce ──▶  Wert
 (Auswahl)              (gefiltert)         (transformiert)           (aggregiert)
```

Die `reduce`-Variante mit explizitem Startwert macht die Aggregation sichtbarer:

```java
double budget = staff.stream()
    .filter(e -> e.department().equals("engineering"))
    .mapToDouble(e -> e.salary() * 1.10)
    .reduce(0.0, Double::sum);
```

`0.0` ist der Startwert, `Double::sum` kombiniert jeweils zwei Werte zu einem, bis nur noch einer übrig ist.

### Mehrere Methoden in `main` verbinden

```java
class Payroll {
    record Employee(String name, String department, double salary) {}

    static List<Employee> filterDepartment(List<Employee> staff, String dept) {
        return staff.stream()
            .filter(e -> e.department().equals(dept))
            .toList();
    }

    static List<Employee> applyRaise(List<Employee> staff, double rate) {
        return staff.stream()
            .map(e -> new Employee(e.name(), e.department(), e.salary() * (1 + rate)))
            .toList();
    }

    static double totalCost(List<Employee> staff) {
        return staff.stream().mapToDouble(Employee::salary).sum();
    }

    public static void main(String[] args) {
        var staff = List.of(
            new Employee("Anna",  "engineering", 80_000),
            new Employee("Ben",   "marketing",   65_000),
            new Employee("Clara", "engineering", 92_000),
            new Employee("David", "support",     58_000),
            new Employee("Eva",   "engineering", 74_000)
        );

        var engineers = filterDepartment(staff, "engineering");
        var withRaise = applyRaise(engineers, 0.10);
        var budget    = totalCost(withRaise);
        System.out.println(budget);  // 270600.0
    }
}
```

`main` fungiert als Dirigent: jede Methode hat genau eine Aufgabe, ihre Verkettung ergibt den vollständigen Algorithmus.

In `applyRaise` wird bewusst ein **neues** `Employee`-Objekt erzeugt, statt das bestehende zu verändern (Records sind in Java ohnehin unveränderlich). So bleibt die Originalliste unberührt, und jede Stufe der Pipeline liefert einen neuen Wert weiter.

### Erweiterung: Bericht statt Zahl

Sobald sich die Anforderung ändert, lässt sich die Pipeline nahtlos verlängern:

```java
class PayrollReport {
    record Employee(String name, String department, double salary) {}

    static List<Employee> filterDepartment(List<Employee> staff, String dept) {
        return staff.stream().filter(e -> e.department().equals(dept)).toList();
    }

    static List<Employee> applyRaise(List<Employee> staff, double rate) {
        return staff.stream()
            .map(e -> new Employee(e.name(), e.department(), e.salary() * (1 + rate)))
            .toList();
    }

    static String formatLine(Employee e) {
        return "%-10s CHF %.0f".formatted(e.name(), e.salary());
    }

    static String buildReport(List<Employee> staff) {
        var lines = staff.stream().map(PayrollReport::formatLine).toList();
        var total = staff.stream().mapToDouble(Employee::salary).sum();
        return String.join("\n", lines) + "\n---\nBudget: CHF %.0f".formatted(total);
    }

    public static void main(String[] args) {
        var staff = List.of(
            new Employee("Anna",  "engineering", 80_000),
            new Employee("Ben",   "marketing",   65_000),
            new Employee("Clara", "engineering", 92_000),
            new Employee("David", "support",     58_000),
            new Employee("Eva",   "engineering", 74_000)
        );

        var report = buildReport(applyRaise(filterDepartment(staff, "engineering"), 0.10));
        System.out.println(report);
    }
}
```

Erwartete Ausgabe:

```text
Anna       CHF 88000
Clara      CHF 101200
Eva        CHF 81400
---
Budget: CHF 270600
```

Die ursprüngliche Pipeline `filterDepartment → applyRaise → totalCost` wird zu `filterDepartment → applyRaise → buildReport`. Zwei neue Funktionen (`formatLine`, `buildReport`), keine Änderung an den bestehenden — der Algorithmus wird erweitert, nicht umgeschrieben.

### Was C1E zusammenbringt

| Element | Beitrag zum Algorithmus |
| ------ | ------ |
| Kleine Funktionen (`filterDepartment`, `applyRaise`, `totalCost`, `formatLine`) | Bausteine mit je einer Verantwortung |
| Funktionskomposition (`andThen`, verschachtelte Aufrufe) | Bausteine zu einer Pipeline verbinden |
| Stream mit `filter/map/reduce` | Daten als Sequenz transformieren und aggregieren |
| `main` als Dirigent | Pipeline anstossen, Eingabe liefern, Ergebnis ausgeben |

Genau dieses Zusammenspiel meint die Kompetenz C1E: aus vielen kleinen Funktionen einen vollständigen, zusammenhängenden Algorithmus bauen.
