---
title: "C3E"
parent: "C - Umsetzung"
nav_order: 9
---

# C3E: Lambda für Programmflusssteuerung

> *Ich kann Lambda-Ausdrücke verwenden, um den Programmfluss zu steuern, z.B. durch Sortieren von Listen basierend auf benutzerdefinierten Kriterien. Ich kann erklären, was eine Closure ist, und anhand eines Beispiels zeigen, wie eine Funktion sich Variablen aus ihrem Erstellungskontext merkt.*

## Lernziele

| # | Lernziel | Beantwortet in |
| --- | ---------- | ---------------- |
| 1 | Ich kann erklären, was eine Closure ist und welche Variablen ein Lambda aus seinem Erstellungskontext "einfangen" kann. | [Was ist eine Closure?](#was-ist-eine-closure) |
| 2 | Ich kann die "effectively final"-Regel in Java erklären und zeigen, warum sie für Closures gilt. | [Effectively Final](#effectively-final) |
| 3 | Ich kann Lambda-Ausdrücke als Comparator einsetzen, um den Sortierablauf einer Liste nach eigenen Kriterien zu steuern. | [Sortieren mit Lambda-Comparatoren](#sortieren-mit-lambda-comparatoren) |

---

## Was ist eine Closure?

Eine **Closure** (deutsch: Abschluss) ist eine Funktion, die sich Variablen aus ihrem **Erstellungskontext** merkt – auch dann noch, wenn dieser Kontext eigentlich nicht mehr existieren würde.

In Java ist jeder Lambda-Ausdruck automatisch eine Closure, sobald er auf eine Variable aus dem umgebenden Code zugreift:

```java
int schwellenwert = 10;

// Dieser Lambda "schliesst über" schwellenwert ab
Predicate<Integer> grossGenug = zahl -> zahl > schwellenwert;

grossGenug.test(15);  // => true
grossGenug.test(7);   // => false
```

Der Lambda-Ausdruck `zahl -> zahl > schwellenwert` enthält keine eigene Definition von `schwellenwert`. Er "erinnert sich" an den Wert aus dem umgebenden Scope, wo er erstellt wurde.

### Closure vs. normale Funktion

| | Normale Methode | Closure (Lambda) |
| --- | ----------------- | ------------------ |
| **Zugriff auf äussere Variablen** | Nur auf Felder der Klasse | Auf lokale Variablen des Erstellungskontexts |
| **Trägt Kontext mit sich** | Nein | Ja |
| **Typisches Einsatzgebiet** | Immer verfügbare Logik | Kontextabhängige, konfigurierbare Logik |

### Praxisbeispiel: Konfigurierbarer Filter

Closures ermöglichen es, eine allgemeine Funktion mit einem konkreten Wert zu "befüllen":

```java
Predicate<Integer> filterAb(int minimum) {
    return zahl -> zahl >= minimum;  // Lambda merkt sich minimum
}

var filterAb18 = filterAb(18);
var filterAb21 = filterAb(21);

filterAb18.test(20);  // => true
filterAb21.test(20);  // => false
```

`filterAb(18)` und `filterAb(21)` sind zwei unabhängige Closures, jede mit ihrem eigenen `minimum`-Wert.

---

## Effectively Final

In Java dürfen Lambdas nur auf Variablen zugreifen, die **effectively final** sind – das heisst, ihr Wert wird nach der ersten Zuweisung **nicht mehr verändert**. Das `final`-Schlüsselwort ist optional; der Compiler prüft es automatisch.

```java
int grenze = 100;           // effectively final: wird nie neu zugewiesen
Predicate<Integer> check = x -> x > grenze;   // erlaubt
```

```java
int grenze = 100;
grenze = 200;               // Neuzuweisung → NICHT mehr effectively final
Predicate<Integer> check = x -> x > grenze;   // Kompilierfehler!
```

### Warum diese Regel?

Wenn ein Lambda in einem anderen Thread oder zu einem späteren Zeitpunkt ausgeführt wird, ist der ursprüngliche Stack-Frame längst weg. Java kopiert den Wert der Variable in den Lambda – aber nur dann, wenn sichergestellt ist, dass er sich nie geändert hat. Sonst wäre unklar, welcher Wert kopiert wurde.

| Situation | Erlaubt? | Grund |
| ----------- | --------- | ------- |
| `final int x = 5;` | Ja | Explizit final |
| `int x = 5;` (nie geändert) | Ja | Effectively final |
| `int x = 5; x = 10;` | Nein | Nicht mehr effectively final |
| Instanzfeld `this.x` | Ja | Felder sind über `this` immer erreichbar |

---

## Sortieren mit Lambda-Comparatoren

Lambdas steuern direkt den Programmfluss, wenn sie als **Comparator** an `sort` oder `sorted` übergeben werden. Der Sortieralgorithmus entscheidet dann anhand dieser Funktion, wie Elemente angeordnet werden.

### Einfaches Sortieren nach einem Feld

```java
record Produkt(String name, double preis) {}

var produkte = List.of(
    new Produkt("Käse",   5.20),
    new Produkt("Milch",  1.80),
    new Produkt("Brot",   3.50)
);

// Aufsteigend nach Preis
var nachPreis = produkte.stream()
    .sorted((a, b) -> Double.compare(a.preis(), b.preis()))
    .toList();
// => [Milch 1.80, Brot 3.50, Käse 5.20]

// Absteigend nach Name
var nachName = produkte.stream()
    .sorted((a, b) -> b.name().compareTo(a.name()))
    .toList();
// => [Milch, Käse, Brot]
```

### Sortieren mit Closure: dynamisches Kriterium

Eine Closure ermöglicht es, das Sortierkriterium zur Laufzeit zu bestimmen:

```java
Comparator<Produkt> sortiererFuer(String feld) {
    return switch (feld) {
        case "preis" -> (a, b) -> Double.compare(a.preis(), b.preis());
        case "name"  -> (a, b) -> a.name().compareTo(b.name());
        default      -> (a, b) -> 0;
    };
}

var kriteriuam = "preis";  // könnte aus Benutzereingabe kommen
var sortiert = produkte.stream()
    .sorted(sortiererFuer(kriteriuam))
    .toList();
```

Der zurückgegebene Lambda ist eine Closure: Er "erinnert sich" an das gewählte Feld, ohne dass `sorted()` wissen muss, nach welchem Kriterium sortiert wird.

### Sortieren nach mehreren Kriterien

```java
record Mitarbeiter(String name, String abteilung, double gehalt) {}

var mitarbeiter = List.of(
    new Mitarbeiter("Anna",  "IT", 8500),
    new Mitarbeiter("Beat",  "HR", 7200),
    new Mitarbeiter("Clara", "IT", 7200),
    new Mitarbeiter("David", "HR", 9100)
);

// Zuerst nach Abteilung, dann nach Gehalt absteigend
var sortiert = mitarbeiter.stream()
    .sorted((a, b) -> {
        int abt = a.abteilung().compareTo(b.abteilung());
        if (abt != 0) return abt;
        return Double.compare(b.gehalt(), a.gehalt());  // absteigend
    })
    .toList();
// => [Clara IT 7200, Anna IT 8500, David HR 9100, Beat HR 7200]
// (IT vor HR alphabetisch; innerhalb IT: zuerst höheres Gehalt)
```

Der mehrzeilige Lambda-Block steuert den Programmfluss mit einer Bedingung: nur wenn die Abteilungen gleich sind, wird das Gehalt als Tiebreaker verwendet.

### Comparator.comparing als Alternative

Für einfache Fälle bietet Java `Comparator.comparing()` als lesbarere Alternative:

```java
// Gleichwertig zu (a, b) -> Double.compare(a.preis(), b.preis())
var sortiert = produkte.stream()
    .sorted(Comparator.comparing(Produkt::preis))
    .toList();

// Mehrstufig mit thenComparing
var sortiert2 = mitarbeiter.stream()
    .sorted(Comparator.comparing(Mitarbeiter::abteilung)
        .thenComparing(Comparator.comparingDouble(Mitarbeiter::gehalt).reversed()))
    .toList();
```

| Ansatz | Wann verwenden |
| -------- | ---------------- |
| `(a, b) -> ...` Lambda | Komplexe oder bedingte Vergleichslogik |
| `Comparator.comparing(...)` | Einfaches Sortieren nach einem Feld |
| `.thenComparing(...)` | Mehrstufige Sortierung nach festen Feldern |
