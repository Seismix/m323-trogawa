---
title: "BE1"
parent: "B - Anforderungen & Design"
nav_order: 3
---

# BE1: Anforderungen transferieren

> *Ich kann Anforderungen aus der imperativen Programmierung in Anforderungen der deklarativen Programmierung transferieren. ("klar definierte Abfolge" transformieren zu "Endergebnis beschreiben")*

## Lernziele

| # | Lernziel | Beantwortet in |
|---|----------|----------------|
| 1 | Ich kann eine gegebene imperative Anforderung in eine deklarative Anforderung transformieren, die das Endergebnis statt die Arbeitsschritte beschreibt. | [Transformation: Imperativ zu Deklarativ](#transformation-imperativ-zu-deklarativ) |
| 2 | Ich kann mindestens 2 Informationen benennen, die bei der Transformation verloren gehen, und begründen warum das vorteilhaft ist. | [Was geht bei der Transformation verloren?](#was-geht-bei-der-transformation-verloren) |
| 3 | Ich kann eine mehrstufige imperative Spezifikation in eine deklarative Anforderung umformulieren. | [Mehrstufige Spezifikationen transformieren](#mehrstufige-spezifikationen-transformieren) |

---

## Transformation: Imperativ zu Deklarativ

Die Grundtechnik: Man streicht die **Schritte** und behält nur das **Ergebnis**.

### Beispiel: Rabatt auf teure Produkte

**Imperativ:**

> Gehe die Produktliste durch. Für jedes Produkt, prüfe ob der Preis > 50 ist. Wenn ja, wende 10% Rabatt an. Speichere das Ergebnis.

**Deklarativ:**

> Das Ergebnis ist die Produktliste, wobei alle Produkte mit einem Preis über 50 einen um 10% reduzierten Preis haben.

### Vorgehen

| Schritt | Aktion | Beispiel |
|---------|--------|----------|
| 1 | Imperative Anforderung lesen | "Gehe durch, prüfe, wende an, speichere" |
| 2 | Alle Verben streichen, die *Schritte* beschreiben | ~~Gehe durch~~, ~~prüfe~~, ~~wende an~~, ~~speichere~~ |
| 3 | Das gewünschte **Endergebnis** formulieren | "Produktliste mit reduzierten Preisen" |
| 4 | Bedingungen als **Eigenschaft** des Ergebnisses formulieren | "...wobei Produkte mit Preis > 50 einen Rabatt von 10% haben" |

### Wie sieht das im Code aus?

```java
record Product(String name, double price) {}

// Imperativ (Schritt für Schritt)
var result = new ArrayList<Product>();
for (var p : products) {
    if (p.price() > 50) {
        result.add(new Product(p.name(), p.price() * 0.9));
    } else {
        result.add(p);
    }
}

// Deklarativ (Ergebnis beschreiben)
var result = products.stream()
    .map(p -> p.price() > 50
        ? new Product(p.name(), p.price() * 0.9)
        : p)
    .toList();
```

---

## Was geht bei der Transformation verloren?

Bei der Transformation von imperativ zu deklarativ gehen bestimmte Informationen verloren. Das ist **gewollt und vorteilhaft**:

| Verlorene Information | Warum vorteilhaft |
|----------------------|-------------------|
| **Reihenfolge der Ausführung** | Die Laufzeitumgebung kann die effizienteste Reihenfolge selbst wählen, z.B. Parallelisierung. |
| **Implementierungsdetails** (Schleifen, Zwischenvariablen) | Weniger fehleranfällig, da keine manuelle Schleifenmechanik nötig ist. |
| **Speicherverwaltung** (wann wird was gespeichert) | Das System kann selbst entscheiden, wann und wie Zwischenergebnisse gespeichert werden. |

### Beispiel

**Imperativ:** "Iteriere über die Liste, erstelle eine Zwischenliste, prüfe jedes Element, füge passende ein, sortiere am Ende."

**Deklarativ:** "Das Ergebnis ist eine sortierte Liste aller Elemente, die das Kriterium erfüllen."

Die deklarative Version sagt nichts über Zwischenlisten oder Iterationsreihenfolge. Eine Datenbank könnte die Sortierung schon beim Filtern erledigen, ein Stream könnte parallelisiert werden. Diese Freiheit entsteht genau dadurch, dass die Schritte **nicht** vorgeschrieben sind.

---

## Mehrstufige Spezifikationen transformieren

Komplexere imperative Spezifikationen bestehen aus mehreren aufeinanderfolgenden Schritten. Die Transformation folgt demselben Prinzip, nur dass man die gesamte Pipeline auf ihr Endergebnis reduziert.

### Beispiel: CSV zu JSON

**Imperativ:**

> Lese die CSV-Datei Zeile für Zeile. Parse jede Zeile. Validiere die Felder. Konvertiere gültige Zeilen in JSON. Schreibe die JSON-Objekte in eine Datei.

**Deklarativ:**

> Das Ergebnis ist eine JSON-Datei, die alle gültigen Datensätze der CSV-Eingabedatei enthält, wobei jeder Datensatz als JSON-Objekt repräsentiert ist.

### Weitere Beispiele

| Imperativ (mehrstufig) | Deklarativ (Endergebnis) |
|----------------------|------------------------|
| "Lies alle Log-Dateien. Parse Timestamps. Filtere nach Fehler-Level. Gruppiere nach Stunde. Zähle pro Gruppe." | "Das Ergebnis ist eine Übersicht der Fehleranzahl pro Stunde, basierend auf allen Log-Dateien." |
| "Lade alle Bestellungen. Berechne für jede den Gesamtpreis. Filtere Bestellungen unter 10 CHF. Sortiere absteigend nach Preis." | "Das Ergebnis ist eine nach Preis absteigend sortierte Liste aller Bestellungen mit einem Gesamtpreis von mindestens 10 CHF." |

### Tipp

Je mehr Schritte die imperative Spezifikation hat, desto kürzer wird typischerweise die deklarative Version. Fünf imperative Sätze werden oft zu einem einzigen deklarativen Satz, der nur das Endergebnis beschreibt.
