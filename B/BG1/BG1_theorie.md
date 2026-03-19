---
title: "BG1"
parent: "B - Anforderungen & Design"
nav_order: 1
---

# BG1: Imperativ vs. Deklarativ unterscheiden

> *Ich kann den Unterschied zwischen Anforderungen der imperativen Programmierung (definierte Folge von Handlungsanweisungen) und der deklarativen Programmierung (Beschreibung des Endzustandes) erklären.*

## Lernziele

| # | Lernziel | Beantwortet in |
|---|----------|----------------|
| 1 | Ich kann den Unterschied zwischen imperativ ("wie") und deklarativ ("was") an einem Alltagsbeispiel erklären. | [Imperativ vs. Deklarativ](#imperativ-vs-deklarativ) |
| 2 | Ich kann gegebene Codebeispiele korrekt als imperativ oder deklarativ einordnen und meine Zuordnung begründen. | [Imperativ oder deklarativ?](#imperativ-oder-deklarativ) |
| 3 | Ich kann Beispiele für deklarative Sprachen und Technologien nennen und erklären, warum sie deklarativ sind. | [Deklarative Sprachen und Technologien](#deklarative-sprachen-und-technologien) |

---

## Imperativ vs. Deklarativ

Der Kernunterschied lässt sich in einem Satz zusammenfassen:

| Paradigma | Beschreibt | Frage |
|-----------|-----------|-------|
| **Imperativ** | *Wie* etwas gemacht wird | "Welche Schritte muss ich ausführen?" |
| **Deklarativ** | *Was* das Ergebnis sein soll | "Wie soll das Endergebnis aussehen?" |

### Alltagsbeispiel: Essen bestellen

**Imperativ** (Rezept, Schritt für Schritt):

> Schneide die Zwiebeln. Erhitze das Öl in einem Topf. Brate die Zwiebeln 5 Minuten an. Giesse Brühe dazu. Lass alles 20 Minuten köcheln. Püriere die Suppe.

**Deklarativ** (Bestellung im Restaurant):

> Ich hätte gerne eine Zwiebelsuppe.

Beim imperativen Ansatz beschreibt man **jeden einzelnen Schritt**. Beim deklarativen Ansatz beschreibt man **das gewünschte Ergebnis** und überlässt die Ausführung dem Koch (oder dem Computer).

---

## Imperativ oder deklarativ?

### Codebeispiel: Zahlen grösser als 5 filtern

**Imperativ** (Schritt für Schritt, explizite Schleifenmechanik):

```java
var numbers = List.of(0, 1, 2, 3, 4, 5, 6, 7, 8, 9);
var result = new ArrayList<Integer>();
for (var x : numbers) {
    if (x > 5) {
        result.add(x);
    }
}
```

Hier wird exakt gesteuert: iterieren, prüfen, anfügen.

**Deklarativ** (Beschreibung des Ergebnisses):

```java
var result = IntStream.range(0, 10)
    .filter(x -> x > 5)
    .boxed()
    .toList();
```

Die Stream-Pipeline beschreibt *was* gewünscht ist: alle `x` grösser als `5`. Die Schleifenmechanik wird nicht explizit gesteuert.

### Weitere Beispiele

| Aufgabe | Imperativ | Deklarativ |
|---------|----------|------------|
| Summe berechnen | `int total = 0; for (var x : list) total += x;` | `list.stream().mapToInt(Integer::intValue).sum()` |
| Sortieren | Manueller Bubble Sort mit verschachtelten Schleifen | `list.stream().sorted().toList()` |
| Maximum finden | Schleife mit Vergleich und Zwischenvariable | `list.stream().max(Integer::compareTo)` |

Bei allen deklarativen Varianten sagt man dem Computer *was* man will, nicht *wie* er es tun soll.

---

## Deklarative Sprachen und Technologien

Einige Sprachen und Technologien sind von Grund auf deklarativ:

| Sprache/Technologie | Warum deklarativ? | Beispiel |
|---------------------|------------------|----------|
| **SQL** | Man beschreibt, *welche* Daten man will, nicht *wie* die Datenbank sie sucht. | `SELECT name FROM users WHERE age > 18` |
| **HTML/CSS** | Man beschreibt, *wie* die Seite aussehen soll, nicht *wie* der Browser sie rendert. | `<h1>Titel</h1>` |
| **Regular Expressions** | Man beschreibt das *Muster*, nicht den Suchalgorithmus. | `\d{3}-\d{4}` |

Bei SQL zum Beispiel schreibt man `SELECT name FROM users WHERE age > 18`. Man sagt nicht: "Öffne die Tabelle, gehe Zeile für Zeile durch, prüfe das Alter, sammle die Namen." Die Datenbank entscheidet selbst, wie sie die Abfrage am effizientesten ausführt.

Funktionale Programmierung ist eine Form der deklarativen Programmierung: Man beschreibt Transformationen auf Daten (mit `map`, `filter`, `reduce`), statt Schritt-für-Schritt-Anweisungen zu geben.
