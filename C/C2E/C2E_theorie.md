---
title: "C2E"
parent: "C - Umsetzung"
nav_order: 6
---

# C2E: Komplexe Aufgaben mit Funktionen lösen

> *Ich kann Funktionen als Objekte und Argumente verwenden, um komplexe Aufgaben zu lösen und den Code sauberer und effizienter zu gestalten.*

## Lernziele

| # | Lernziel | Beantwortet in |
| ------ | ------ | ------ |
| 1 | Ich kann Closures verwenden, um Zustand in funktionalem Code zu kapseln. | [1. Closures nutzen](#1-closures-nutzen) |
| 2 | Ich kann Currying einsetzen, um Funktionen mit mehreren Parametern in eine Kette von Funktionen mit je einem Parameter umzuwandeln. | [2. Currying anwenden](#2-currying-anwenden) |
| 3 | Ich kann eine Funktion implementieren, die eine andere Funktion zurückgibt, und damit z.B. einen festen Steuersatz auf einen Nettopreis anwenden. | [3. Currying mit Funktionen höherer Ordnung](#3-currying-mit-funktionen-höherer-ordnung) |

---

## 1. Closures nutzen

Ein **Closure** ist eine Funktion, die Variablen aus ihrem umgebenden Scope «einfängt» und darauf zugreift, auch nachdem dieser Scope nicht mehr aktiv ist. In Java müssen die eingefangenen Variablen **effektiv final** sein.

### Beispiel: Logger mit eigenem Prefix

```java
static Function<String, String> createLogger(String prefix) {
    return message -> "[" + prefix + "] " + message;
}

public static void main(String[] args) {
    var errorLog = createLogger("ERROR");
    var infoLog  = createLogger("INFO");

    System.out.println(errorLog.apply("Disk full"));      // [ERROR] Disk full
    System.out.println(infoLog.apply("Server started"));  // [INFO] Server started
}
```

Jeder Logger «erinnert sich» an sein eigenes `prefix`, obwohl der ursprüngliche Methodenaufruf längst zurückgekehrt ist. So lässt sich Zustand kapseln, **ohne** eine eigene Klasse mit Feldern zu schreiben.

### Closures vs. Klasse mit Feld

| Aspekt | Closure | Klasse |
| ------ | ------ | ------ |
| Zustand | im umgebenden Scope eingefangen | als Feld gespeichert |
| Schreibaufwand | eine Methode, ein Lambda | Klasse, Konstruktor, Feld, Methode |
| Veränderbarkeit | nur effektiv finale Werte | beliebig mutierbar |
| Eignung | kleine, einmalige Kapselung | komplexer, langlebiger Zustand |

---

## 2. Currying anwenden

**Currying** wandelt eine Funktion mit mehreren Parametern in eine Kette von Funktionen mit je einem Parameter um. Statt `add(1, 2, 3)` schreibt man `add(1)(2)(3)`.

```java
public static void main(String[] args) {
    // Reguläre BiFunction (nicht gecurryt)
    BiFunction<Integer, Integer, Integer> addBi = (a, b) -> a + b;
    System.out.println(addBi.apply(1, 2));  // 3

    // Gecurryte Variante
    Function<Integer, Function<Integer, Integer>> addCurried = a -> b -> a + b;
    System.out.println(addCurried.apply(1).apply(2));  // 3
}
```

### Drei Parameter currying und teilweise Anwendung

Der grosse Vorteil von Currying: man kann eine Funktion schrittweise mit Argumenten «füllen» und wiederverwendbare Zwischenfunktionen erzeugen (**Partial Application**).

```java
public static void main(String[] args) {
    Function<Integer, Function<Integer, Function<Integer, Integer>>> add =
        a -> b -> c -> a + b + c;

    // Vollständiger Aufruf
    int result = add.apply(1).apply(2).apply(3);  // 6

    // Teilweise Anwendung
    var addFive      = add.apply(5);          // b -> c -> 5 + b + c
    var addFiveThree = addFive.apply(3);      // c -> 5 + 3 + c
    int sum          = addFiveThree.apply(2); // 10

    System.out.println(result + " / " + sum);
}
```

| Aufruf | Was bleibt offen | Typ |
| ------ | ------ | ------ |
| `add.apply(5)` | `b` und `c` | `Function<Integer, Function<Integer, Integer>>` |
| `add.apply(5).apply(3)` | nur `c` | `Function<Integer, Integer>` |
| `add.apply(5).apply(3).apply(2)` | nichts | `Integer` |

---

## 3. Currying mit Funktionen höherer Ordnung

Currying entsteht in Java fast immer dadurch, dass eine **Higher-Order Function** ein Lambda zurückgibt, das die übrigen Parameter aus dem umgebenden Scope per Closure mitnimmt.

### Beispiel: Steuersatz auf Nettopreis anwenden

```java
static Function<Double, Double> steuerFaktor(double satz) {
    return netto -> netto * (1 + satz);
}

public static void main(String[] args) {
    var mwst77 = steuerFaktor(0.077);   // CH Standardsatz
    var mwst26 = steuerFaktor(0.026);   // CH reduzierter Satz

    double brutto1 = mwst77.apply(8.20);   // 8.83
    double brutto2 = mwst26.apply(8.20);   // 8.41

    System.out.println(brutto1 + " / " + brutto2);
}
```

`steuerFaktor` vereint **drei Konzepte** in wenigen Zeilen:

1. **Higher-Order Function**: die Methode gibt eine Funktion zurück.
2. **Currying**: aus der zweistelligen Operation `brutto(satz, netto)` wird die einstellige Kette `steuerFaktor(satz).apply(netto)`.
3. **Closure**: das zurückgegebene Lambda hält `satz` aus dem umgebenden Scope fest und merkt sich diesen Wert für jeden späteren Aufruf.

Jeder erzeugte Faktor (`mwst77`, `mwst26`) merkt sich also dauerhaft seinen eigenen Steuersatz.

### Vorteile dieses Musters

| Vorteil | Erklärung |
| ------ | ------ |
| **Konfiguration trennen** | Steuersatz wird einmal gesetzt, danach nur noch Preise eingegeben |
| **Wiederverwendbar** | `mwst77` kann beliebig oft auf neue Nettopreise angewendet werden |
| **Komponierbar** | Lässt sich mit `andThen` in eine Pipeline einbauen, z.B. nach Rabatt |
| **Testbar** | Der zurückgegebene Funktionswert ist eine eigenständige, isoliert prüfbare Einheit |

### Kombination: Rabatt und Steuer

```java
static Function<Double, Double> rabatt(double rate) {
    return netto -> netto * (1 - rate);
}

public static void main(String[] args) {
    var endpreis = rabatt(0.10).andThen(steuerFaktor(0.077));
    System.out.println(endpreis.apply(100.0));   // 100 * 0.9 * 1.077 = 96.93
}
```

Zwei kleine Funktionen, beide per Currying konfiguriert, ergeben durch Komposition einen kompletten Preisrechner, ohne eine einzige zusätzliche Klasse.
