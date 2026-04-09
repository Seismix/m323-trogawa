---
title: "C1G Kotlin"
parent: "C - Umsetzung"
nav_order: 3
---

# C1G: Algorithmus erklären (Kotlin)

> *Ich kann in eigenen Worten erklären, was ein Algorithmus ist, einen gegebenen Algorithmus nachvollziehen und einen einfachen Algorithmus beschreiben.*

## Lernziele

| # | Lernziel | Beantwortet in |
| --- | ---------- | ---------------- |
| 1 | Ich kann in eigenen Worten erklären, was ein Algorithmus ist und welche Eigenschaften er hat (Endlichkeit, Determiniertheit, Ein-/Ausgabe). | [1. Algorithmus-Begriff definieren](#1-algorithmus-begriff-definieren) |
| 2 | Ich kann einen gegebenen Algorithmus Schritt für Schritt durchgehen und das Ergebnis für einen bestimmten Input vorhersagen. | [2. Algorithmus nachvollziehen](#2-algorithmus-nachvollziehen) |
| 3 | Ich kann einen einfachen Algorithmus (z.B. Sortierung, Suche) in Pseudocode oder natürlicher Sprache beschreiben. | [3. Algorithmus beschreiben](#3-algorithmus-beschreiben) |

---

## 1. Algorithmus-Begriff definieren

Ein **Algorithmus** ist eine eindeutige, endliche Abfolge von Schritten, die ein Problem löst.

| Eigenschaft | Bedeutung | Beispiel |
| ------------- | ----------- | ---------- |
| **Endlichkeit** | Terminiert nach endlich vielen Schritten | Das Prüfen aller Zeichen eines Passworts endet beim letzten Zeichen |
| **Determiniertheit** | Gleiche Eingabe ergibt immer gleiches Ergebnis | `"Hallo".count { it == 'l' }` gibt immer `2` zurück |
| **Ein-/Ausgabe** | Nimmt Eingaben entgegen, produziert Ausgabe | Eingabe: Passwort, Ausgabe: gültig/ungültig |

### Alltagsbeispiel: Briefsortierung

Eine Poststelle sortiert Briefe wie ein Algorithmus:

- **Eingabe:** Unsortierter Stapel Briefe
- **Schritte:** PLZ lesen, in das passende Fach legen (endlich viele Briefe)
- **Ausgabe:** Briefe nach Region sortiert
- **Determiniert:** Dieselbe PLZ landet immer im selben Fach

---

## 2. Algorithmus nachvollziehen

Ein Algorithmus, der Vokale in einem Wort zählt:

```kotlin
fun countVowels(text: String): Int {
    val vowels = "aeiouäöü"
    var count = 0
    for (char in text.lowercase()) {
        if (char in vowels) {
            count++
        }
    }
    return count
}
```

### Schritt-für-Schritt-Durchlauf mit `"Zürich"`

| Schritt | `char` | `char in vowels` | `count` |
| ------- | ------ | ----------------- | ------- |
| Start   |        |                   | 0       |
| 1       | z      | Nein              | 0       |
| 2       | ü      | Ja                | 1       |
| 3       | r      | Nein              | 1       |
| 4       | i      | Ja                | 2       |
| 5       | c      | Nein              | 2       |
| 6       | h      | Nein              | 2       |

**Ergebnis:** `2`

### Weiteres Beispiel: Wörter in einem Satz zählen

```kotlin
fun countWords(sentence: String): Int {
    val trimmed = sentence.trim()
    if (trimmed.isEmpty()) return 0
    return trimmed.split(Regex("\\s+")).size
}
```

Durchlauf mit `"  Kotlin ist   kompakt  "`:

| Schritt | Operation | Ergebnis |
| ------- | --------- | -------- |
| 1 | `trim()` | `"Kotlin ist   kompakt"` |
| 2 | `split(Regex("\\s+"))` | `["Kotlin", "ist", "kompakt"]` |
| 3 | `.size` | `3` |

**Ergebnis:** `3`

---

## 3. Algorithmus beschreiben

### Passwort-Validierung in natürlicher Sprache

**Problem:** Prüfe, ob ein Passwort Mindestanforderungen erfüllt.

**Beschreibung:**

1. Prüfe, ob das Passwort mindestens 8 Zeichen lang ist.
2. Gehe jedes Zeichen durch und merke dir, ob mindestens ein Grossbuchstabe, ein Kleinbuchstabe und eine Ziffer vorkommen.
3. Falls alle Bedingungen erfüllt: das Passwort ist gültig.
4. Sonst: gib zurück, welche Bedingung fehlt.

```kotlin
fun validatePassword(password: String): Pair<Boolean, List<String>> {
    val errors = mutableListOf<String>()
    if (password.length < 8)              errors += "mindestens 8 Zeichen"
    if (password.none { it.isUpperCase() }) errors += "mindestens 1 Grossbuchstabe"
    if (password.none { it.isLowerCase() }) errors += "mindestens 1 Kleinbuchstabe"
    if (password.none { it.isDigit() })     errors += "mindestens 1 Ziffer"
    return Pair(errors.isEmpty(), errors)
}

println(validatePassword("Geh3im!!"))  // (true, [])
println(validatePassword("kurz"))
// (false, [mindestens 8 Zeichen, mindestens 1 Grossbuchstabe, mindestens 1 Ziffer])
```

### Caesar-Verschlüsselung in Pseudocode

**Problem:** Verschiebe jeden Buchstaben eines Textes um eine feste Anzahl Positionen im Alphabet.

```text
ALGORITHMUS caesar(text, verschiebung):
    ergebnis = leerer String
    FÜR jedes Zeichen im Text:
        FALLS es ein Buchstabe ist:
            neue Position = (alte Position + verschiebung) MOD 26
            Füge den verschobenen Buchstaben an ergebnis an
        SONST:
            Füge das Zeichen unverändert an ergebnis an
    RÜCKGABE ergebnis
```

```kotlin
fun caesar(text: String, shift: Int): String =
    text.map { char ->
        when {
            char.isLetter() -> {
                val base = if (char.isUpperCase()) 'A' else 'a'
                val shifted = (char - base + shift).mod(26) + base.code
                shifted.toChar()
            }
            else -> char
        }
    }.joinToString("")

println(caesar("Hallo Welt!", 3))   // Kdoor Zhow!
println(caesar("Kdoor Zhow!", -3))  // Hallo Welt!
```
