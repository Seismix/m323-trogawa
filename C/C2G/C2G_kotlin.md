---
title: "C2G Kotlin"
parent: "C - Umsetzung"
nav_order: 6
---

# C2G: Funktionen als Objekte behandeln (Kotlin)

> *Ich kann Funktionen als First-Class Citizens behandeln: in Variablen speichern, als Rückgabewert verwenden und in Datenstrukturen ablegen.*

## Lernziele

| # | Lernziel | Beantwortet in |
| --- | ---------- | ---------------- |
| 1 | Ich kann eine Funktion in einer Variable speichern und diese Variable aufrufen, um die Funktion auszuführen. | [1. Funktion einer Variable zuweisen](#1-funktion-einer-variable-zuweisen) |
| 2 | Ich kann eine Funktion schreiben, die eine andere Funktion zurückgibt. | [2. Funktion als Rückgabewert](#2-funktion-als-rückgabewert) |
| 3 | Ich kann Funktionen in Listen oder Maps speichern und gezielt abrufen. | [3. Funktionen in Datenstrukturen speichern](#3-funktionen-in-datenstrukturen-speichern) |

---

## Überblick

In Kotlin sind Funktionen First-Class Citizens. Mit Funktionstypen wie `(String) -> String` können Lambdas und Funktionsreferenzen direkt in Variablen gespeichert, zurückgegeben und in Datenstrukturen abgelegt werden.

---

## 1. Funktion einer Variable zuweisen

```kotlin
// Markdown-Formatierung als Funktionsvariablen
val makeBold: (String) -> String = { text -> "**$text**" }
val makeItalic: (String) -> String = { text -> "*$text*" }
val makeHeading: (String) -> String = { text -> "# $text" }

println(makeBold("Wichtig"))    // **Wichtig**
println(makeItalic("Hinweis"))  // *Hinweis*
println(makeHeading("Titel"))   // # Titel
```

### Funktionsreferenz zuweisen

Bestehende Funktionen können mit `::` referenziert werden:

```kotlin
fun censored(text: String): String =
    text.first() + "*".repeat(text.length - 1)

val hide = ::censored
println(hide("Passwort"))  // P*******
println(hide("Geheim"))    // G*****
```

### Verschiedene Funktionstypen

```kotlin
// Textverarbeitung
val shout: (String) -> String = { it.uppercase() + "!" }
println(shout("stopp"))  // STOPP!

// Prüfung (gibt Boolean zurück)
val isPalindrome: (String) -> Boolean = { s ->
    s.lowercase() == s.lowercase().reversed()
}
println(isPalindrome("Anna"))   // true
println(isPalindrome("Hallo"))  // false

// Eingebaute Funktionen referenzieren
val count: (Collection<*>) -> Int = Collection<*>::size
println(count(listOf(1, 2, 3)))  // 3
```

---

## 2. Funktion als Rückgabewert

Eine Funktion kann eine andere Funktion zurückgeben. Das ermöglicht es, spezialisierte Funktionen dynamisch zu erzeugen.

```kotlin
// Gibt eine Funktion zurück, die Schadenspunkte berechnet
fun createAttack(baseDamage: Int): (Int) -> Int =
    { multiplier -> baseDamage * multiplier }

val swordHit = createAttack(25)
val magicBolt = createAttack(40)

println(swordHit(1))    // 25  (normaler Treffer)
println(swordHit(2))    // 50  (kritischer Treffer)
println(magicBolt(1))   // 40
println(magicBolt(3))   // 120 (dreifach verstärkt)
```

### Weiteres Beispiel: Textrahmen

```kotlin
fun createWrapper(left: String, right: String): (String) -> String =
    { text -> "$left$text$right" }

val parentheses = createWrapper("(", ")")
val brackets = createWrapper("[", "]")
val htmlBold = createWrapper("<b>", "</b>")

println(parentheses("optional"))  // (optional)
println(brackets("index"))        // [index]
println(htmlBold("wichtig"))      // <b>wichtig</b>
```

---

## 3. Funktionen in Datenstrukturen speichern

### In einer Liste: Textverarbeitungspipeline

```kotlin
val pipeline: List<(String) -> String> = listOf(
    String::trim,
    String::lowercase,
    { s -> s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue") },
    { s -> s.replace(" ", "_") },
)

var filename = "  Über Uns Seite "
for (step in pipeline) {
    filename = step(filename)
}
println(filename)  // ueber_uns_seite
```

### In einer Map: Spielaktionen

```kotlin
data class Player(val hp: Int, val gold: Int, val xp: Int)

val actions: Map<String, (Player) -> Player> = mapOf(
    "heal"    to { p -> p.copy(hp = minOf(100, p.hp + 30), gold = p.gold - 10) },
    "train"   to { p -> p.copy(xp = p.xp + 25) },
    "buy_gem" to { p -> p.copy(gold = p.gold - 20) },
)

var player = Player(hp = 100, gold = 50, xp = 0)

player = actions["heal"]!!(player)
println(player)  // Player(hp=100, gold=40, xp=0)

player = actions["train"]!!(player)
println(player)  // Player(hp=100, gold=40, xp=25)

player = actions["buy_gem"]!!(player)
println(player)  // Player(hp=100, gold=20, xp=25)
```

Das Map-Pattern ersetzt lange `when`-Ketten:

```kotlin
// Statt:
fun execute(action: String, player: Player): Player = when (action) {
    "heal"  -> player.copy(hp = minOf(100, player.hp + 30), gold = player.gold - 10)
    "train" -> player.copy(xp = player.xp + 25)
    else    -> throw IllegalArgumentException("Unknown: $action")
}

// Einfacher:
fun execute(action: String, player: Player): Player =
    actions[action]!!(player)
```
