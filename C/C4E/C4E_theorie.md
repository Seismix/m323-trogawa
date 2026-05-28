---
title: "C4E"
parent: "C - Umsetzung"
nav_order: 12
---

# C4E: Komplexe Datenverarbeitung mit Map/Filter/Reduce

> *Ich kann Map, Filter und Reduce verwenden, um komplexe Datenverarbeitungsaufgaben zu lösen, wie z.B. die Aggregation von Daten oder die Transformation von Datenstrukturen.*

## Lernziele

| # | Lernziel | Beantwortet in |
| --- | ---------- | ---------------- |
| 1 | Ich kann mit `filter`, `map` und `reduce` eine anspruchsvollere Aufgabe lösen: die Summe aller rabattierten Food-Artikel berechnen. | [Summe rabattierter Food-Artikel](#summe-rabattierter-food-artikel) |
| 2 | Ich kann mit `reduce` das teuerste Element einer Liste bestimmen, ohne `max()` zu verwenden. | [Teuerstes Element mit reduce](#teuerstes-element-mit-reduce) |
| 3 | Ich kann eine mehrstufige Stream-Pipeline lesen, schrittweise nachvollziehen und die Zwischenergebnisse angeben. | [Pipeline schrittweise nachvollziehen](#pipeline-schrittweise-nachvollziehen) |

---

## Summe rabattierter Food-Artikel

### Die Ausgangsdaten

```java
record Artikel(String name, String kategorie, double preis, double rabatt) {}

var sortiment = List.of(
    new Artikel("Vollmilch",     "Food",     1.80, 0.10),
    new Artikel("Laptop-Tasche", "NonFood",  45.00, 0.05),
    new Artikel("Emmentaler",    "Food",     8.50, 0.20),
    new Artikel("Rotwein",       "Food",    12.00, 0.15),
    new Artikel("Notizbuch",     "NonFood",  4.90, 0.00),
    new Artikel("Birchermüesli", "Food",     3.60, 0.10),
    new Artikel("Olivenöl",      "Food",    11.50, 0.25)
);
```

### Die Aufgabe

> Berechne die **Gesamtsumme der Preise nach Rabatt** aller Artikel der Kategorie "Food", die vor dem Rabatt **mehr als 3 CHF** kosten.

### Lösung als Stream-Pipeline

```java
double summe = sortiment.stream()
    .filter(a  -> a.kategorie().equals("Food"))   // nur Food-Artikel
    .filter(a  -> a.preis() > 3.0)                // nur über 3 CHF
    .map(a     -> a.preis() * (1 - a.rabatt()))   // Rabatt abziehen
    .reduce(0.0, Double::sum);                    // aufsummieren

System.out.println(summe);  // => 31.025
```

### Jeden Schritt nachvollziehen

| Schritt | Operation | Verbleibende Artikel / Werte |
| -------- | ----------- | ------------------------------ |
| Start | Alle Artikel | Vollmilch, Laptop-Tasche, Emmentaler, Rotwein, Notizbuch, Birchermüesli, Olivenöl |
| `filter` (Food) | Nur Kategorie "Food" | Vollmilch, Emmentaler, Rotwein, Birchermüesli, Olivenöl |
| `filter` (> 3 CHF) | Originalpreis > 3 | Emmentaler (8.50), Rotwein (12.00), Birchermüesli (3.60), Olivenöl (11.50) |
| `map` (Rabatt) | Preis × (1 − Rabatt) | 6.80, 10.20, 3.24, 8.625 |
| `reduce` (Summe) | Alle addieren | **28.865** |

### Vergleich mit imperativem Ansatz

```java
// Imperativ: mehrere Zwischenvariablen, explizite Schleife
double summe = 0.0;
for (Artikel a : sortiment) {
    if (a.kategorie().equals("Food") && a.preis() > 3.0) {
        summe += a.preis() * (1 - a.rabatt());
    }
}
```

```java
// Funktional: deklarative Pipeline, kein veränderbarer Zustand
double summe = sortiment.stream()
    .filter(a -> a.kategorie().equals("Food"))
    .filter(a -> a.preis() > 3.0)
    .map(a -> a.preis() * (1 - a.rabatt()))
    .reduce(0.0, Double::sum);
```

| Aspekt | Imperativ | Funktional |
| -------- | ----------- | ------------ |
| Veränderlicher Zustand | `summe` wird laufend überschrieben | Kein veränderbarer Zustand |
| Lesbarkeit | Bedingung und Berechnung vermischt | Klare Trennung: filtern → transformieren → aggregieren |
| Erweiterbarkeit | Neue Bedingung → Codeblock ändern | Neues `.filter()` einfach anhängen |

---

## Teuerstes Element mit reduce

`reduce` ist nicht nur für Summen geeignet. Es kann beliebige Akkumulationslogik ausdrücken – darunter auch das Finden eines Extremwerts.

### Idee

`reduce` vergleicht immer zwei Elemente und behält das "bessere" zurück. Wenn "besser" = "teurer" bedeutet, ergibt sich am Ende das teuerste Element.

```java
// Mit reduce: teuersten Artikel finden
Optional<Artikel> teuerster = sortiment.stream()
    .reduce((a, b) -> a.preis() >= b.preis() ? a : b);

teuerster.ifPresent(a ->
    System.out.println(a.name() + ": " + a.preis() + " CHF")
);
// => Laptop-Tasche: 45.0 CHF
```

### Warum Optional?

`reduce` ohne Startwert gibt ein `Optional` zurück, weil der Stream leer sein könnte – es gäbe dann kein "teuerstes Element". `Optional` zwingt dazu, diesen Fall explizit zu behandeln.

```java
// Nur Food-Artikel: teuerstes
Optional<Artikel> teuersteFood = sortiment.stream()
    .filter(a -> a.kategorie().equals("Food"))
    .reduce((a, b) -> a.preis() >= b.preis() ? a : b);

teuersteFood.ifPresent(a ->
    System.out.println("Teuerstes Food: " + a.name() + " (" + a.preis() + " CHF)")
);
// => Teuerstes Food: Rotwein (12.0 CHF)
```

### reduce vs. max

Java bietet auch `max(Comparator)` für dasselbe Ergebnis:

```java
// Mit max() – kürzer, aber nur für Extremwert-Suche
var teuerster = sortiment.stream()
    .max(Comparator.comparingDouble(Artikel::preis));

// Mit reduce() – flexibler, beliebige Akkumulationslogik möglich
var teuerster = sortiment.stream()
    .reduce((a, b) -> a.preis() >= b.preis() ? a : b);
```

| | `reduce` | `max` / `min` |
| --- | --------- | --------------- |
| **Flexibilität** | Beliebige Akkumulationslogik | Nur Extremwert |
| **Lesbarkeit** | Expliziter Vergleich sichtbar | Klarer Ausdruck der Absicht |
| **Einsatz** | Wenn eigene Akkumulationslogik nötig ist | Wenn nur der grösste/kleinste Wert gesucht wird |

---

## Pipeline schrittweise nachvollziehen

Eine nützliche Technik beim Lesen oder Debuggen von Stream-Pipelines: jeden Schritt einzeln ausführen und das Zwischenergebnis ausgeben.

```java
// Vollständige Pipeline
double summe = sortiment.stream()
    .filter(a -> a.kategorie().equals("Food"))
    .filter(a -> a.preis() > 3.0)
    .map(a -> a.preis() * (1 - a.rabatt()))
    .reduce(0.0, Double::sum);
```

```java
// Schrittweise zum Debuggen
var schritt1 = sortiment.stream()
    .filter(a -> a.kategorie().equals("Food"))
    .toList();
System.out.println("Nach Food-Filter: " + schritt1.size() + " Artikel");

var schritt2 = schritt1.stream()
    .filter(a -> a.preis() > 3.0)
    .toList();
System.out.println("Nach Preisfilter: " + schritt2.size() + " Artikel");

var schritt3 = schritt2.stream()
    .map(a -> a.preis() * (1 - a.rabatt()))
    .toList();
System.out.println("Rabattierte Preise: " + schritt3);

double summe = schritt3.stream().reduce(0.0, Double::sum);
System.out.println("Summe: " + summe);
```

Ausgabe:

```
Nach Food-Filter: 5 Artikel
Nach Preisfilter: 4 Artikel
Rabattierte Preise: [6.8, 10.2, 3.24, 8.625]
Summe: 28.865
```

Dieses Vorgehen hilft, Fehler in der Pipeline zu lokalisieren, indem man Zwischenergebnisse sichtbar macht.
