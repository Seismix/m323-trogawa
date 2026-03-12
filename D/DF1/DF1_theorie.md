---
title: "DF1"
parent: "D — Refactoring & Optimierung"
nav_order: 2
---

# DF1 — Refactoring-Techniken anwenden

> *Ich kann mit Refactoring-Techniken einen Code lesbarer und verständlicher machen.*

## Überblick

In dieser Kompetenz geht es darum, Refactoring nicht nur zu kennen, sondern **aktiv anzuwenden**. Die drei Kernfähigkeiten sind:

1. **Extract Function** — Lange Codeblöcke in benannte Funktionen auslagern
2. **Rename** — Variablen und Funktionen aussagekräftig benennen
3. **Duplikate entfernen** — Gemeinsamen Code in wiederverwendbare Funktionen extrahieren

## Codebeispiel

Siehe [`refactoring_beispiel.py`](refactoring_beispiel.py) für ein vollständiges, kommentiertes Beispiel, das alle drei Techniken demonstriert.

### Zusammenfassung der Techniken

| Technik | Vorher | Nachher |
|---------|--------|---------|
| Extract Function | Monolithische 50-Zeilen-Funktion | Mehrere kleine, fokussierte Funktionen |
| Rename | `calc(d, r)` | `calculate_discount(days_since_purchase, return_rate)` |
| Duplikate entfernen | Copy-Paste-Code an 3 Stellen | Eine gemeinsame Funktion |
