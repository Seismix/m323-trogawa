---
title: "C4G Kotlin"
parent: "C - Umsetzung"
nav_order: 12
---

# C4G: Map, Filter und Reduce einzeln anwenden (Kotlin)

> *Ich kann `map()`, `filter()` und `reduce()` einzeln verwenden, um Listen zu transformieren, zu filtern und zu aggregieren.*

## Lernziele

| # | Lernziel | Beantwortet in |
| --- | ---------- | ---------------- |
| 1 | Ich kann `map()` verwenden, um eine Transformation auf jedes Element einer Liste anzuwenden. | [1. Map anwenden](#1-map-anwenden) |
| 2 | Ich kann `filter()` verwenden, um Elemente aus einer Liste nach einem Kriterium auszuwählen. | [2. Filter anwenden](#2-filter-anwenden) |
| 3 | Ich kann `reduce()` / `fold()` verwenden, um eine Liste auf einen einzelnen Wert zu reduzieren. | [3. Reduce anwenden](#3-reduce-anwenden) |

---

## Überblick

In Kotlin sind `map`, `filter` und `fold`/`reduce` direkt auf Collections verfügbar (kein Stream nötig).

| Operation | Was sie tut | Eingabe → Ausgabe |
| ----------- | ------------ | ------------------- |
| `map {}` | Transformiert jedes Element | Liste → Liste (gleiche Anzahl) |
| `filter {}` | Wählt Elemente nach Kriterium | Liste → Liste (gleiche oder weniger) |
| `fold()` / `reduce()` | Fasst alle Elemente zusammen | Liste → Einzelwert |

---

## 1. Map anwenden

`map { transformation }` wendet eine Funktion auf jedes Element an und gibt eine neue Liste zurück.

```kotlin
// Rezeptzutaten für 4 statt 2 Personen skalieren
val portions = listOf(100, 250, 50, 200)  // Gramm pro Zutat
val scaled = portions.map { it * 2 }
println(scaled)  // [200, 500, 100, 400]
```

`map` verändert die Originalliste nicht:

```kotlin
println(portions)  // [100, 250, 50, 200] — unverändert
```

### Weitere Beispiele

```kotlin
// Dateinamen normalisieren
val filenames = listOf("Bericht.PDF", "foto.JPG", "notizen.TXT")
val normalized = filenames.map { it.lowercase() }
println(normalized)  // [bericht.pdf, foto.jpg, notizen.txt]

// CHF zu EUR umrechnen (Kurs 0.94)
val chfPrices = listOf(9.90, 24.50, 149.00)
val eurPrices = chfPrices.map { "%.2f".format(it * 0.94) }
println(eurPrices)  // [9.31, 23.03, 140.06]

// Spielernamen mit Rang versehen
val players = listOf("Alice", "Bob", "Charlie")
val ranked = players.mapIndexed { i, name -> "#${i + 1} $name" }
println(ranked)  // [#1 Alice, #2 Bob, #3 Charlie]
```

### Map mit Funktionsreferenz

```kotlin
fun maskEmail(email: String): String {
    val (name, domain) = email.split("@")
    return "${name.first()}***@$domain"
}

val emails = listOf("anna@bbw.ch", "max@gmail.com", "leo@bluewin.ch")
val masked = emails.map(::maskEmail)
println(masked)  // [a***@bbw.ch, m***@gmail.com, l***@bluewin.ch]
```

---

## 2. Filter anwenden

`filter { bedingung }` behält nur Elemente, für die die Bedingung `true` ergibt.

```kotlin
// Nur Fehlermeldungen aus Logeinträgen filtern
val logs = listOf(
    "INFO: Server started",
    "ERROR: Connection refused",
    "INFO: Request processed",
    "ERROR: Timeout after 30s",
    "WARN: Disk usage 85%",
)
val errors = logs.filter { it.startsWith("ERROR") }
println(errors)
// [ERROR: Connection refused, ERROR: Timeout after 30s]
```

### Weitere Beispiele

```kotlin
// Nur volljährige Benutzer
val ages = mapOf("Anna" to 22, "Ben" to 16, "Clara" to 19, "David" to 14, "Eva" to 30)
val adults = ages.filter { (_, age) -> age >= 18 }
println(adults)  // {Anna=22, Clara=19, Eva=30}

// Nur verfügbare Produkte (Bestand > 0)
data class Product(val name: String, val stock: Int)
val inventory = listOf(
    Product("Laptop", 5), Product("Maus", 0),
    Product("Tastatur", 12), Product("Monitor", 0), Product("Kabel", 34),
)
val available = inventory.filter { it.stock > 0 }
println(available.map { it.name })  // [Laptop, Tastatur, Kabel]

// Nur gültige Postleitzahlen (4-stellig, numerisch)
val codes = listOf("8000", "abc", "1234", "99", "3012", "")
val valid = codes.filter { it.length == 4 && it.all { c -> c.isDigit() } }
println(valid)  // [8000, 1234, 3012]
```

### Filter mit benannter Funktion

```kotlin
fun isStrongPassword(pw: String): Boolean =
    pw.length >= 8
        && pw.any { it.isUpperCase() }
        && pw.any { it.isDigit() }

val passwords = listOf("abc", "Passw0rt", "12345678", "Sicher99!", "hi")
val strong = passwords.filter(::isStrongPassword)
println(strong)  // [Passw0rt, Sicher99!]
```

---

## 3. Reduce anwenden

`fold(startwert) { acc, element -> ... }` kombiniert alle Elemente schrittweise zu einem Einzelwert.

```kotlin
// Warenkorb-Gesamtpreis berechnen
val cart = listOf(4.50, 12.90, 3.20, 8.00)
val total = cart.fold(0.0) { acc, price -> acc + price }
println(total)  // 28.6
```

### Wie Fold funktioniert (Schritt für Schritt)

Für `listOf(4.50, 12.90, 3.20, 8.00).fold(0.0) { acc, price -> acc + price }`:

| Schritt | `acc` | `price` | Ergebnis |
| ------- | ----- | ------- | -------- |
| Start   | 0.0   |         | 0.0      |
| 1       | 0.0   | 4.50    | 4.50     |
| 2       | 4.50  | 12.90   | 17.40    |
| 3       | 17.40 | 3.20    | 20.60    |
| 4       | 20.60 | 8.00    | 28.60    |

### Weitere Beispiele

```kotlin
// Längsten String finden
val cities = listOf("Bern", "Zürich", "Winterthur", "Basel")
val longest = cities.reduce { acc, c -> if (c.length > acc.length) c else acc }
println(longest)  // Winterthur

// Verschachtelte Listen flach machen
val nested = listOf(listOf(1, 2), listOf(3), listOf(4, 5, 6))
val flat = nested.fold(emptyList<Int>()) { acc, lst -> acc + lst }
println(flat)  // [1, 2, 3, 4, 5, 6]

// Häufigkeiten zählen
val chars = "abracadabra".toList()
val freq = chars.fold(emptyMap<Char, Int>()) { acc, c ->
    acc + (c to (acc.getOrDefault(c, 0) + 1))
}
println(freq)  // {a=5, b=2, r=2, c=1, d=1}
```

### Fold vs. Reduce

`fold` hat einen expliziten Startwert, `reduce` nimmt das erste Element:

```kotlin
// fold: sicher bei leeren Listen
val safeSum = emptyList<Int>().fold(0) { acc, x -> acc + x }
println(safeSum)  // 0

// reduce: wirft Exception bei leerer Liste
// emptyList<Int>().reduce { acc, x -> acc + x }  // UnsupportedOperationException!

// Lösung: reduceOrNull
val safest = emptyList<Int>().reduceOrNull { acc, x -> acc + x }
println(safest)  // null
```
