export {};
// C2F: Funktionen als Argumente und Higher-Order Functions
// Thema: Badminton-Turnier-Verwaltung

interface Player {
  name: string;
  country: string;
  ranking: number;
  points: number;
}

interface Match {
  player1: string;
  player2: string;
  sets: readonly [number, number][];
  round: string;
}

const TOP_SEED_CUTOFF = 4 as const;
const SEEDING_CUTOFF = 8 as const;
const SUPER_SERIES_BONUS_PERCENT = 15 as const;
const WORLD_TOUR_BONUS_PERCENT = 25 as const;
const BASE_POINTS = 10_000 as const;

const players = [
  { name: "Viktor Axelsen", country: "DEN", ranking: 1, points: 118_472 },
  { name: "Kunlavut Vitidsarn", country: "THA", ranking: 2, points: 102_890 },
  { name: "Shi Yu Qi", country: "CHN", ranking: 3, points: 98_120 },
  { name: "Anders Antonsen", country: "DEN", ranking: 4, points: 91_750 },
  { name: "Kodai Naraoka", country: "JPN", ranking: 5, points: 85_330 },
  { name: "Jonatan Christie", country: "INA", ranking: 8, points: 72_455 },
  { name: "Loh Kean Yew", country: "SGP", ranking: 12, points: 61_200 },
  { name: "Chou Tien Chen", country: "TPE", ranking: 15, points: 52_800 },
] as const satisfies readonly Player[];

const matches = [
  { player1: "Viktor Axelsen", player2: "Kodai Naraoka", sets: [[21, 18], [21, 15]], round: "Final" },
  { player1: "Kunlavut Vitidsarn", player2: "Shi Yu Qi", sets: [[21, 19], [18, 21], [21, 17]], round: "Semi-Final" },
  { player1: "Anders Antonsen", player2: "Loh Kean Yew", sets: [[21, 12], [21, 16]], round: "Quarter-Final" },
] as const satisfies readonly Match[];

// --- Higher-Order Function: Ranking-Filter erstellen ---
// Gibt eine Filter-Funktion zurück (Closure über maxRank)
const createRankingFilter = (maxRank: number) =>
  (player: Player): boolean => player.ranking <= maxRank;

// --- Higher-Order Function: Sortier-Funktion erstellen ---
// Nimmt einen Key-Extraktor als Argument und gibt einen Comparator zurück
const createSortBy = <T>(extractKey: (item: T) => number, descending = false) => {
  const sortDirection = descending ? -1 : 1;
  return (first: T, second: T): number =>
    (extractKey(first) - extractKey(second)) * sortDirection;
};

// --- Higher-Order Function: Transformation auf alle Elemente anwenden ---
// Eigene Implementierung mit reduce statt Mutation
const applyToAll = <T, R>(items: readonly T[], transform: (item: T) => R): R[] =>
  items.reduce<R[]>(
    (accumulated, item) => [...accumulated, transform(item)],
    [],
  );

// --- Higher-Order Function: Match-Gewinner bestimmen ---
const determineMatchWinner = (match: Match): { winner: string; loser: string } => {
  const setsWonByPlayer1 = match.sets.filter(
    ([scorePlayer1, scorePlayer2]) => scorePlayer1 > scorePlayer2,
  ).length;
  const player1Won = setsWonByPlayer1 > match.sets.length / 2;
  return player1Won
    ? { winner: match.player1, loser: match.player2 }
    : { winner: match.player2, loser: match.player1 };
};

// --- Higher-Order Function: Match-Ergebnis mit Callback formatieren ---
const formatMatchResult = (
  match: Match,
  formatter: (winner: string, loser: string, round: string) => string,
): string => {
  const { winner, loser } = determineMatchWinner(match);
  return formatter(winner, loser, match.round);
};

// --- Higher-Order Function: Punkte-Bonus anwenden ---
// Gibt eine neue Funktion zurück (Closure über bonusPercent)
const createBonusCalculator = (bonusPercent: number) =>
  (basePoints: number): number =>
    Math.round(basePoints * (1 + bonusPercent / 100));

// --- Higher-Order Function: Pipe (Komposition von Transformationen) ---
const pipe = <T>(...functions: ((value: T) => T)[]): ((value: T) => T) =>
  functions.reduce(
    (composedSoFar, nextFunction) =>
      (value) => nextFunction(composedSoFar(value)),
  );

// --- Anwendung ---

console.log("=== Badminton Tournament System ===\n");

// createRankingFilter: Funktion als Rückgabewert
const isTopSeed = createRankingFilter(TOP_SEED_CUTOFF);
const isSeeded = createRankingFilter(SEEDING_CUTOFF);
console.log("Top Seeds:", players.filter(isTopSeed).map((player) => player.name));
console.log("All Seeds:", players.filter(isSeeded).map((player) => player.name));

// createSortBy: Funktion als Argument (extractKey), Funktion als Rückgabewert (comparator)
const byPointsDescending = createSortBy<Player>((player) => player.points, true);
const byRankingAscending = createSortBy<Player>((player) => player.ranking);
console.log(
  "\nNach Punkten:",
  [...players].sort(byPointsDescending).map((player) => `${player.name} (${player.points})`),
);
console.log(
  "Nach Ranking:",
  [...players].sort(byRankingAscending).map((player) => `#${player.ranking} ${player.name}`),
);

// applyToAll: Funktion als Argument (transform)
const playerSummaries = applyToAll(
  players,
  (player) => `${player.name} [${player.country}] #${player.ranking}`,
);
console.log("\nSpieler-Übersicht:", playerSummaries);

// formatMatchResult: Funktion als Argument (formatter)
const formatSetScores = (match: Match): string =>
  match.sets.map(([scorePlayer1, scorePlayer2]) => `${scorePlayer1}-${scorePlayer2}`).join(", ");

const resultLines = matches.map((match) =>
  formatMatchResult(match, (winner, loser, round) =>
    `  ${round}: ${winner} besiegt ${loser} (${formatSetScores(match)})`,
  ),
);
console.log("\nMatch-Ergebnisse:");
resultLines.forEach((line) => console.log(line));

// createBonusCalculator: Funktion als Rückgabewert (Closure)
const superSeriesBonus = createBonusCalculator(SUPER_SERIES_BONUS_PERCENT);
const worldTourBonus = createBonusCalculator(WORLD_TOUR_BONUS_PERCENT);
console.log(`\nBonus-Berechnung für ${BASE_POINTS.toLocaleString()} Basis-Punkte:`);
console.log(`  Super Series (+${SUPER_SERIES_BONUS_PERCENT}%): ${superSeriesBonus(BASE_POINTS)} Punkte`);
console.log(`  World Tour Finals (+${WORLD_TOUR_BONUS_PERCENT}%): ${worldTourBonus(BASE_POINTS)} Punkte`);

// pipe: Komposition mehrerer Bonus-Funktionen
const combinedBonus = pipe(superSeriesBonus, worldTourBonus);
console.log(`  Beide Boni kombiniert: ${combinedBonus(BASE_POINTS)} Punkte`);
