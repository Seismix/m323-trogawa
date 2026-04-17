export {};
// C3G: Einfache Lambda-Ausdrücke schreiben
// Thema: Badminton-Ranking und Disziplinen

interface Player {
  name: string;
  country: string;
  ranking: number;
  points: number;
}

const TOP_SEED_CUTOFF = 4 as const;
const SEEDING_CUTOFF = 8 as const;

const DISCIPLINE_CODES = ["MS", "WS", "MD", "WD", "XD"] as const;
type DisciplineCode = (typeof DISCIPLINE_CODES)[number];

const DISCIPLINE_NAMES = {
  MS: "Men's Singles",
  WS: "Women's Singles",
  MD: "Men's Doubles",
  WD: "Women's Doubles",
  XD: "Mixed Doubles",
} as const satisfies Record<DisciplineCode, string>;

const players = [
  { name: "Viktor Axelsen", country: "DEN", ranking: 1, points: 118_472 },
  { name: "Kunlavut Vitidsarn", country: "THA", ranking: 2, points: 102_890 },
  { name: "Shi Yu Qi", country: "CHN", ranking: 3, points: 98_120 },
  { name: "Kodai Naraoka", country: "JPN", ranking: 5, points: 85_330 },
  { name: "Jonatan Christie", country: "INA", ranking: 8, points: 72_455 },
  { name: "Loh Kean Yew", country: "SGP", ranking: 12, points: 61_200 },
  { name: "Chou Tien Chen", country: "TPE", ranking: 15, points: 52_800 },
] as const satisfies readonly Player[];

// Lambda: Spieler-Name mit Land formatieren
const formatPlayer = (player: Player): string =>
  `${player.name} (${player.country})`;

// Lambda: Prüfen ob Spieler gesetzt ist (Top 8)
const isSeeded = (player: Player): boolean =>
  player.ranking <= SEEDING_CUTOFF;

// Lambda: Ranking-Punkte als Tausender-String formatieren
const formatPoints = (rankingPoints: number): string =>
  `${(rankingPoints / 1000).toFixed(1)}k`;

// Lambda mit bedingtem Ausdruck: Seeding-Kategorie bestimmen
const seedingCategory = (player: Player): string =>
  player.ranking <= TOP_SEED_CUTOFF
    ? "Top-Seed"
    : player.ranking <= SEEDING_CUTOFF
      ? "Seeded"
      : "Unseeded";

// Lambda: Disziplin-Kürzel in lesbaren Namen umwandeln (typsicher via DisciplineCode)
const disciplineDisplayName = (code: DisciplineCode): string =>
  DISCIPLINE_NAMES[code];

// Lambda: Zusammengesetztes Label durch Komposition mehrerer Lambdas
const playerSeedingLabel = (player: Player): string =>
  `[${seedingCategory(player)}] ${formatPlayer(player)} — ${formatPoints(player.points)}`;

// --- Lambda vs. benannte Funktion ---
// Die Lambdas oben (formatPlayer, isSeeded, seedingCategory) sind kurz und
// haben je eine einzige Aufgabe: ideal als Lambda.
// Für komplexere Logik (z.B. vollständige Ranking-Berechnung über mehrere
// Turniere mit Gewichtung und Tie-Breaking) wäre eine benannte Funktion besser,
// weil sie im Stacktrace erkennbar ist und durch ihren Namen dokumentiert.
//
// Faustregel: Lambda wenn die Logik auf einen Blick verständlich ist,
// benannte Funktion wenn man einen sprechenden Namen braucht um den Zweck
// zu kommunizieren.

// --- Anwendung (pure Transformationen, dann Ausgabe) ---

const allPlayersFormatted = players.map(formatPlayer);
const seededPlayerLabels = players.filter(isSeeded).map(playerSeedingLabel);
const pointsOverview = players.map(
  (player) => `${player.name}: ${formatPoints(player.points)} Punkte`,
);
const disciplineNames = DISCIPLINE_CODES.map(disciplineDisplayName);

console.log("=== Badminton World Ranking ===\n");
console.log("Alle Spieler:");
allPlayersFormatted.forEach((formatted) => console.log(` - ${formatted}`));
console.log("\nGesetzte Spieler (Top 8):");
seededPlayerLabels.forEach((label) => console.log(` ${label}`));
console.log("\nPunkte-Übersicht:");
pointsOverview.forEach((line) => console.log(` ${line}`));
console.log("\nDisziplinen:");
disciplineNames.forEach((discipline) => console.log(` - ${discipline}`));
