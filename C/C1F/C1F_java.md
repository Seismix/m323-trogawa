---
title: "C1F_Java"
parent: "C - Umsetzung"
nav_order: 2
---

# C1F: Algorithmen in funktionale Teilstücke aufteilen

> *Ich kann Algorithmen in funktionale Teilstücke aufteilen.*

## Lernziele

| # | Lernziel | Beantwortet in |
| --- | ---------- | -------------- |
| 1 | Ich kann in einem gegebenen Algorithmus sinnvolle Teilschritte erkennen, die als eigenständige Funktionen implementiert werden können. | [1. Teilfunktionen identifizieren](#1-teilfunktionen-identifizieren) |
| 2 | Ich kann einen Algorithmus so zerlegen, dass jede Teilfunktion genau eine Aufgabe erfüllt (Single Responsibility). | [2. Funktionale Dekomposition](#2-funktionale-dekomposition) |
| 3 | Ich kann beschreiben, wie die einzelnen Teilfunktionen zusammengesetzt werden, um den Gesamtalgorithmus zu bilden. | [3. Zusammensetzung planen](#3-zusammensetzung-planen) |

---

## 1. Teilfunktionen identifizieren

Ein Algorithmus, der zu viel auf einmal erledigt, wird schnell unübersichtlich und schwer erweiterbar. Der erste Schritt zur Verbesserung ist, logisch zusammengehörende Teilschritte zu erkennen und zu benennen.

### Beispiel: Monolithische Methode

```java
List<String> processLogs(List<String> entries) {
    var errors = new ArrayList<String>();
    for (var entry : entries) {
        if (entry.startsWith("[ERROR]")) {
            var message = entry.substring("[ERROR] ".length()).strip();
            errors.add(message);
        }
    }
    Collections.sort(errors);
    return errors;
}
```

Diese Methode vermischt drei verschiedene Verantwortlichkeiten in einer einzigen Schleife:

| Schritt | Was passiert | Mögliche Funktion |
| ------- | ------------ | ----------------- |
| 1 | Einträge nach Level filtern | `filterByLevel()` |
| 2 | Präfix entfernen, Nachricht extrahieren | `extractMessages()` |
| 3 | Alphabetisch sortieren | `sortEntries()` |

---

## 2. Funktionale Dekomposition

Jede Teilfunktion bekommt genau eine Verantwortung, nimmt Daten entgegen und gibt neue Daten zurück, ohne die Eingabe zu verändern:

```java
// Teilfunktion 1: Nur Einträge eines bestimmten Levels behalten
List<String> filterByLevel(List<String> entries, String level) {
    var prefix = "[" + level + "]";
    return entries.stream()
        .filter(e -> e.startsWith(prefix))
        .toList();
}

// Teilfunktion 2: Präfix entfernen und Nachricht bereinigen
List<String> extractMessages(List<String> entries, String level) {
    var prefix = "[" + level + "] ";
    return entries.stream()
        .map(e -> e.substring(prefix.length()).strip())
        .toList();
}

// Teilfunktion 3: Alphabetisch sortieren
List<String> sortEntries(List<String> messages) {
    return messages.stream().sorted().toList();
}
```

### Vorteile der Zerlegung

| Vorteil | Erklärung |
| ------- | --------- |
| **Testbarkeit** | Jede Funktion lässt sich mit eigenen Eingaben isoliert prüfen |
| **Wiederverwendbarkeit** | `filterByLevel` funktioniert genauso für `"WARN"` oder `"INFO"` |
| **Lesbarkeit** | Aussagekräftige Namen ersetzen inline-Kommentare |
| **Wartbarkeit** | Änderungen an einem Schritt berühren die anderen nicht |

---

## 3. Zusammensetzung planen

Die Teilfunktionen werden in Reihe geschaltet: der Rückgabewert einer Funktion wird direkt als Argument der nächsten übergeben.

```java
List<String> processLogs(List<String> entries) {
    var filtered  = filterByLevel(entries, "ERROR");
    var messages  = extractMessages(filtered, "ERROR");
    return sortEntries(messages);
}
```

### Weiteres Beispiel: Aktive Nutzer mit E-Mail-Adresse sammeln

**Aufgabe:** Aus einer Nutzerliste alle aktiven Accounts herausfiltern, ihre E-Mail-Adressen extrahieren und alphabetisch sortiert zurückgeben.

**Zerlegung:**

```java
record User(String name, String email, boolean active) {}

// Schritt 1: Nur aktive Nutzer behalten
List<User> filterActive(List<User> users) {
    return users.stream().filter(User::active).toList();
}

// Schritt 2: E-Mail-Adressen extrahieren
List<String> extractEmails(List<User> users) {
    return users.stream().map(User::email).toList();
}

// Schritt 3: Sortieren
List<String> sortEmails(List<String> emails) {
    return emails.stream().sorted().toList();
}

// Zusammensetzung
List<String> activeEmails(List<User> users) {
    var active = filterActive(users);
    var emails = extractEmails(active);
    return sortEmails(emails);
}
```

```java
var users = List.of(
    new User("Alice", "alice@example.com", true),
    new User("Bob",   "bob@example.com",   false),
    new User("Clara", "clara@example.com", true)
);
System.out.println(activeEmails(users));
// [alice@example.com, clara@example.com]
```

Die Zerlegung folgt immer demselben Muster: Teilschritte erkennen, als eigenständige Funktionen auslagern, dann in Reihe schalten. Jede Funktion verändert die Eingabe nicht, sondern liefert einen neuen Wert weiter.
