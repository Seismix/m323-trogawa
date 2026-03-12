---
title: DE1 — Auswirkungen des Refactorings einschätzen
parent: Home
nav_order: 12
---

# DE1 — Auswirkungen des Refactorings einschätzen

> *Ich kann die Auswirkungen des Refactorings auf das Verhalten des Codes einschätzen und sicherstellen, dass das Refactoring keine unerwünschten Nebeneffekte hat.*

## Überblick

Refactoring soll das **Verhalten** des Codes nicht verändern — nur seine **Struktur**. Doch wie stellt man das sicher?

1. **Verhaltenserhaltung prüfen** — Für ein gegebenes Refactoring mindestens 3 Unit-Tests definieren, die sicherstellen, dass das Verhalten einer Funktion unverändert bleibt.
2. **Nebeneffekte identifizieren** — Für ein gegebenes Refactoring mindestens 3 potenzielle Nebeneffekte identifizieren und für jede eine Gegenmassnahme vorschlagen.
3. **Refactoring-Strategie wählen** — Schrittweise, testbar, sicher vorgehen.

## Codebeispiel

Siehe [`refactoring_sicherheit.py`](refactoring_sicherheit.py) für ein vollständiges Beispiel, das zeigt:
- Wie man **3 gezielte Unit-Tests** definiert, die das Verhalten vor und nach dem Refactoring absichern
- Wie man **3 potenzielle Nebeneffekte** identifiziert und jeweils eine konkrete **Gegenmassnahme** vorschlägt
- Wie man eine sichere Refactoring-Strategie schrittweise umsetzt

### Nebeneffekte und Gegenmassnahmen (Beispiel)

| # | Nebeneffekt | Gegenmassnahme |
|---|------------|----------------|
| 1 | Unbekannte Destinationen könnten anders behandelt werden als im Original (`else`-Branch) | Expliziter Fallback auf `"WORLD"` via `dict.get()`, der das `else`-Verhalten 1:1 abbildet |
| 2 | Gewichtsstufen-Reihenfolge in der Datenstruktur könnte vertauscht werden → falsche Preise | Tiers aufsteigend sortieren und Unit-Test für Grenzwerte schreiben |
| 3 | Rundungsdifferenzen durch geänderte Berechnungsreihenfolge (z.B. Rabatt vor/nach MwSt) | `round()` am Ende beibehalten + Unit-Tests mit exakten Erwartungswerten auf 2 Dezimalstellen |
