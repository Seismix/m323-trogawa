---
title: "BF1_Python"
parent: "B - Anforderungen & Design"
nav_order: 2
---

# BF1: Endzustand als Anforderung beschreiben

> *Ich kann den Endzustand als Anforderung im Sinne der deklarativen Programmierung beschreiben. (Das gewünschte Ergebnis wird beschrieben statt die Arbeitsschritte.)*

## Lernziele

| # | Lernziel | Beantwortet in |
|---|----------|----------------|
| 1 | Ich kann eine imperative Anforderung in eine deklarative Anforderung umformulieren, die den Endzustand beschreibt. | [Anforderungen deklarativ formulieren](#anforderungen-deklarativ-formulieren) |
| 2 | Ich kann mindestens 3 Vorteile nennen, warum es vorteilhaft ist, den Endzustand zu beschreiben statt die Arbeitsschritte. | [Warum Endzustand statt Arbeitsschritte?](#warum-endzustand-statt-arbeitsschritte) |
| 3 | Ich kann für ein praxisnahes Szenario eine deklarative Anforderungsbeschreibung verfassen. | [Praxisbeispiele](#praxisbeispiele) |

---

## Warum Endzustand statt Arbeitsschritte?

In der deklarativen Programmierung beschreibt man **was** das Ergebnis sein soll, nicht **wie** man dorthin kommt. Dieselbe Idee lässt sich auf Anforderungen übertragen: statt die Schritte aufzulisten, formuliert man das gewünschte Endergebnis.

| | Imperative Anforderung | Deklarative Anforderung |
|---|----------------------|------------------------|
| **Fokus** | Arbeitsschritte | Endzustand |
| **Beispiel** | "Iteriere über alle Bestellungen, prüfe den Betrag, füge passende in eine neue Liste" | "Das Ergebnis ist eine Liste aller Bestellungen mit Betrag > 100" |

### Vorteile der deklarativen Formulierung

| Vorteil | Erklärung |
|---------|-----------|
| **Optimierung** | Das System kann die effizienteste Ausführungsstrategie selbst wählen (z.B. Parallelisierung). |
| **Lesbarkeit** | Die Anforderung ist kürzer und auf einen Blick verständlich. |
| **Weniger Fehler** | Keine Implementierungsdetails, die falsch umgesetzt werden könnten. |
| **Flexibilität** | Mehrere Implementierungen können dieselbe Anforderung erfüllen. |

---

## Anforderungen deklarativ formulieren

Die Technik: Man nimmt eine Schritt-für-Schritt-Beschreibung, streicht das **Wie** und behält nur das **Was**.

### Transformationsbeispiele

| Imperativ (Schritte) | Deklarativ (Endzustand) |
|---------------------|------------------------|
| "Iteriere über alle Bestellungen, prüfe ob der Betrag > 100 ist, und füge diese in eine neue Liste ein." | "Das Ergebnis ist eine Liste aller Bestellungen mit einem Betrag grösser als 100." |
| "Gehe die Benutzerliste durch, prüfe das letzte Login-Datum, sammle E-Mails der inaktiven Benutzer." | "Das Ergebnis ist eine Liste der E-Mail-Adressen aller Benutzer, deren letzter Login mehr als 90 Tage zurückliegt." |
| "Lies jede Zeile der CSV, parse sie, prüfe die Felder, konvertiere gültige Zeilen zu JSON." | "Das Ergebnis ist eine JSON-Datei mit allen gültigen Datensätzen der CSV-Eingabe." |

### Muster erkennen

Imperative Anforderungen enthalten typischerweise Wörter wie: *iteriere*, *gehe durch*, *prüfe*, *füge ein*, *speichere*, *für jedes Element*. Deklarative Anforderungen beginnen oft mit: *"Das Ergebnis ist..."* oder *"Die Ausgabe enthält..."*.

---

## Praxisbeispiele

### Szenario: Inaktive Benutzer finden

**Imperative Anforderung:**

> Gehe die Liste aller Benutzer durch. Für jeden Benutzer, prüfe ob das letzte Login-Datum mehr als 90 Tage zurückliegt. Wenn ja, lese die E-Mail-Adresse aus und füge sie in eine Ergebnisliste ein. Gib die Liste zurück.

**Deklarative Anforderung:**

> Das Ergebnis ist eine Liste der E-Mail-Adressen aller Benutzer, deren letzter Login mehr als 90 Tage zurückliegt.

### Wie sieht das im Code aus?

Die deklarative Anforderung lässt sich direkt in deklarativen Code übersetzen:

```python
from datetime import datetime, timedelta

class User:
    def __init__(self, email, last_login):
        self.email = email
        self.last_login = last_login

users = [
    User("alice@example.com", datetime(2024, 1, 1)),
    User("bob@example.com", datetime(2024, 12, 1)),
]

cutoff = datetime.now() - timedelta(days=90)

# Imperative Umsetzung (Schritte)
result = []
for user in users:
    if user.last_login < cutoff:
        result.append(user.email)

# Deklarative Umsetzung (Ergebnis beschreiben)
result = [user.email for user in users if user.last_login < cutoff]
```

Beide Varianten liefern dasselbe Ergebnis. Die deklarative Variante spiegelt die Anforderung fast wörtlich wider: "E-Mail-Adressen aller Benutzer, deren letzter Login vor dem Stichtag liegt."

### Anforderung vs. Implementierung

Wichtig: Die deklarative Anforderung ist **nicht** die Implementierung. Sie beschreibt nur das gewünschte Ergebnis. Ob die Implementierung mit einer List Comprehension, einer `for`-Schleife oder einer SQL-Abfrage erfolgt, ist eine separate Entscheidung.
