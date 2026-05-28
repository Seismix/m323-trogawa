---
title: "AE1"
parent: "A - Paradigmen"
nav_order: 3
---

# AE1: Problemlösung in verschiedenen Paradigmen vergleichen

> *Ich kann ein Problem mit prozeduraler, objektorientierter und funktionaler Programmierung lösen und die Unterschiede der drei Konzepte, prozedural / objektorientiert / funktional, anhand eines Beispiels vergleichen.*

## Lernziele

| # | Lernziel | Beantwortet in |
| --- | ---------- | ---------------- |
| 1 | Ich kann die drei Paradigmen (prozedural, objektorientiert, funktional) kurz beschreiben und ihren Fokus benennen. | [Die drei Paradigmen](#die-drei-paradigmen) |
| 2 | Ich kann dasselbe Problem prozedural, objektorientiert und funktional lösen. | [Das Vergleichsbeispiel](#das-vergleichsbeispiel) |
| 3 | Ich kann die Unterschiede der drei Ansätze anhand des Beispiels erklären und in einer Tabelle vergleichen. | [Vergleich der Ansätze](#vergleich-der-ansätze) |

---

## Die drei Paradigmen

Ein **Programmierparadigma** ist eine grundlegende Art, wie man ein Problem in Code denkt und strukturiert. Die drei wichtigsten Paradigmen sind:

| Paradigma | Fokus | Kernfrage |
| ----------- | ------- | ----------- |
| **Prozedural** | Schritt-für-Schritt-Anweisungen | *Was soll der Computer als Nächstes tun?* |
| **Objektorientiert (OO)** | Objekte mit Zustand und Verhalten | *Welche Objekte gibt es und wie interagieren sie?* |
| **Funktional** | Transformationen von Daten durch Funktionen | *Welche Funktion liefert das gewünschte Ergebnis?* |

Dieselbe Aufgabe kann mit jedem dieser Paradigmen gelöst werden – aber die Denkweise, die Codestruktur und die Wartbarkeit unterscheiden sich deutlich.

---

## Das Vergleichsbeispiel

Als durchgehendes Beispiel verwenden wir folgende Aufgabe:

> **Berechne den Gesamtpreis aller Produkte, die mehr als 10 CHF kosten, inkl. 7.7% MWST.**

Die Ausgangsdaten sind eine Liste von Produktpreisen in CHF:

```java
double[] preise = {5.90, 12.50, 3.00, 24.80, 8.00, 15.00};
// Erwartet: (12.50 + 24.80 + 15.00) * 1.077 = 56.08 CHF
```

---

## Prozedurale Lösung

Die **prozedurale Programmierung** löst das Problem als eine Folge von Anweisungen. Der Zustand wird in Variablen gespeichert und Schritt für Schritt verändert.

```java
double[] preise = {5.90, 12.50, 3.00, 24.80, 8.00, 15.00};
double summe = 0.0;

for (int i = 0; i < preise.length; i++) {
    if (preise[i] > 10.0) {
        summe += preise[i];
    }
}

double gesamtpreis = summe * 1.077;
System.out.println("Gesamtpreis: " + gesamtpreis + " CHF");
```

**Merkmale des prozeduralen Ansatzes:**

- Der Ablauf ist explizit: Schleife, Bedingung, Akkumulation, Ausgabe – in fester Reihenfolge.
- Der Zustand (`summe`) wird direkt verändert (**mutable state**).
- Der Code beschreibt das **Wie**: "gehe durch den Array, prüfe jedes Element, addiere es zur Summe".
- Gut lesbar für kleine, lineare Probleme; wird bei wachsender Komplexität schnell unübersichtlich.

---

## Objektorientierte Lösung

Die **objektorientierte Programmierung** verteilt die Zuständigkeit auf **Klassen und Objekte**. Daten und das Verhalten, das auf diesen Daten operiert, werden zusammengefasst.

```java
class Produkt {
    private final String name;
    private final double preis;

    Produkt(String name, double preis) {
        this.name = name;
        this.preis = preis;
    }

    double getPreis() { return preis; }

    boolean istTeurer(double grenzwert) {
        return preis > grenzwert;
    }
}
```

```java
class Warenkorb {
    private final List<Produkt> produkte;

    Warenkorb(List<Produkt> produkte) {
        this.produkte = produkte;
    }

    double gesamtpreisAbMinimum(double minimum, double mwst) {
        double summe = 0.0;
        for (Produkt p : produkte) {
            if (p.istTeurer(minimum)) {
                summe += p.getPreis();
            }
        }
        return summe * (1 + mwst);
    }
}
```

```java
var produkte = List.of(
    new Produkt("A", 5.90),
    new Produkt("B", 12.50),
    new Produkt("C", 3.00),
    new Produkt("D", 24.80),
    new Produkt("E", 8.00),
    new Produkt("F", 15.00)
);

var warenkorb = new Warenkorb(produkte);
double gesamtpreis = warenkorb.gesamtpreisAbMinimum(10.0, 0.077);
System.out.println("Gesamtpreis: " + gesamtpreis + " CHF");
```

**Merkmale des OO-Ansatzes:**

- Die Logik ist in **Klassen** gekapselt: `Produkt` kennt seinen Preis, `Warenkorb` kennt die Berechnung.
- **Kapselung** (`private`) schützt die Daten vor ungewolltem Zugriff von aussen.
- Objekte haben **Zustand** (die Liste `produkte`) und **Verhalten** (die Methode `gesamtpreisAbMinimum`).
- Gut geeignet, wenn viele Operationen auf denselben Daten nötig sind oder das System wächst.

---

## Funktionale Lösung

Die **funktionale Programmierung** beschreibt das Problem als eine Kette von **Datentransformationen**. Es gibt keine veränderten Variablen – stattdessen werden neue Werte erzeugt.

```java
double[] preise = {5.90, 12.50, 3.00, 24.80, 8.00, 15.00};

double gesamtpreis = Arrays.stream(preise)
    .filter(p -> p > 10.0)
    .sum() * 1.077;

System.out.println("Gesamtpreis: " + gesamtpreis + " CHF");
```

Oder mit einem Zwischenschritt, um den MWST-Faktor ebenfalls als Transformation auszudrücken:

```java
double gesamtpreis = Arrays.stream(preise)
    .filter(p  -> p > 10.0)
    .map(p    -> p * 1.077)
    .sum();
```

**Merkmale des funktionalen Ansatzes:**

- Der Code beschreibt das **Was**: "filtere, multipliziere, summiere" – nicht den genauen Ablauf.
- **Keine veränderten Variablen**: jede Operation erzeugt einen neuen Stream bzw. Wert.
- **Lambda-Ausdrücke** (`p -> p > 10.0`) sind kompakte, anonyme Funktionen.
- Gut geeignet, wenn Daten transformiert oder gefiltert werden, besonders auf Collections.

---

## Vergleich der Ansätze

| Kriterium | Prozedural | Objektorientiert | Funktional |
| ----------- | ------------ | ------------------ | ------------ |
| **Denkweise** | Abfolge von Schritten | Interaktion von Objekten | Transformation von Daten |
| **Zustand** | Veränderliche Variablen | Zustand in Objekten | Kein veränderlicher Zustand |
| **Struktur** | Funktionen / Prozeduren | Klassen und Objekte | Funktionen als Werte |
| **Lesbarkeit** | Klar bei einfachen Abläufen | Gut bei komplexen Domänen | Kompakt bei Datenverarbeitung |
| **Wiederverwendung** | Gering (prozedural) | Hoch (Vererbung, Interfaces) | Hoch (Funktionen kombinierbar) |
| **Testbarkeit** | Mittel (Zustand schwer isolierbar) | Mittel (abhängig vom Design) | Hoch (pure functions, kein Zustand) |
| **Typisches Einsatzgebiet** | Skripte, einfache Abläufe | Geschäftslogik, grosse Systeme | Datenverarbeitung, Pipelines |

---

## Wann welches Paradigma?

In der Praxis werden die Paradigmen oft **kombiniert**. Java ist zum Beispiel primär objektorientiert, unterstützt aber seit Java 8 auch funktionale Konzepte (Streams, Lambdas).

| Situation | Empfohlenes Paradigma |
| ----------- | ----------------------- |
| Einfaches Skript, linearer Ablauf | Prozedural |
| Komplexe Domäne mit vielen Entitäten und Regeln | Objektorientiert |
| Filtern, Transformieren, Aggregieren von Daten | Funktional |
| Grosse Java-Anwendung mit Datenverarbeitung | OO + Funktional kombiniert |

Das Ziel ist nicht, immer dasselbe Paradigma zu verwenden, sondern das **richtige Werkzeug für das jeweilige Problem** zu wählen.
