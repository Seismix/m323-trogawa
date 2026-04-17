export {};
// C1F: Algorithmen in funktionale Teilstücke aufteilen
// Thema: Badminton-Turnier-Rangliste berechnen
//
// Algorithmus: "Berechne die Turnier-Rangliste aus Spielergebnissen"
// Zerlegung in 5 Teilfunktionen, zusammengesetzt als Pipeline:
//   parseResults → determineWinners → tallyPoints → rankPlayers → formatStandings

interface MatchResult {
  player1: string;
  player2: string;
  sets: [number, number][];
}

interface MatchOutcome {
  winner: string;
  loser: string;
}

interface StandingsEntry {
  rank: number;
  player: string;
  wins: number;
  losses: number;
  points: number;
}

const POINTS_PER_WIN = 3 as const;
const POINTS_PER_LOSS = 1 as const;
const PLAYER_COLUMN_WIDTH = 24 as const;

const rawResults = [
  "Viktor Axelsen vs Kodai Naraoka: 21-18, 21-15",
  "Kunlavut Vitidsarn vs Shi Yu Qi: 21-19, 18-21, 21-17",
  "Anders Antonsen vs Loh Kean Yew: 21-12, 21-16",
  "Viktor Axelsen vs Kunlavut Vitidsarn: 21-16, 19-21, 21-18",
  "Kodai Naraoka vs Loh Kean Yew: 21-14, 21-19",
  "Shi Yu Qi vs Anders Antonsen: 18-21, 21-15, 21-19",
  "Viktor Axelsen vs Shi Yu Qi: 21-17, 21-13",
  "Kodai Naraoka vs Anders Antonsen: 19-21, 21-18, 21-16",
] as const;

// --- Teilfunktion 1: Rohdaten parsen ---
const parseResults = (rawLines: readonly string[]): MatchResult[] =>
  rawLines.map((line) => {
    const [playerNames, setScores] = line.split(": ");
    const [player1, player2] = playerNames.split(" vs ");
    const sets = setScores
      .split(", ")
      .map((score) => score.split("-").map(Number) as [number, number]);
    return { player1, player2, sets };
  });

// --- Teilfunktion 2: Gewinner jedes Matches bestimmen ---
const determineWinner = (match: MatchResult): MatchOutcome => {
  const setsWonByPlayer1 = match.sets.filter(
    ([scorePlayer1, scorePlayer2]) => scorePlayer1 > scorePlayer2,
  ).length;
  const player1Won = setsWonByPlayer1 > match.sets.length / 2;
  return player1Won
    ? { winner: match.player1, loser: match.player2 }
    : { winner: match.player2, loser: match.player1 };
};

// --- Teilfunktion 3: Ergebnisse zu Punktestand pro Spieler zusammenzählen ---
// Map.groupBy (ES2024) gruppiert die Einzelergebnisse nach Spielername
const tallyPoints = (outcomes: readonly MatchOutcome[]): Map<string, StandingsEntry> => {
  const allPlayerResults = outcomes.flatMap((outcome) => [
    { player: outcome.winner, won: true },
    { player: outcome.loser, won: false },
  ]);

  const groupedByPlayer = Map.groupBy(allPlayerResults, (result) => result.player);

  return new Map(
    [...groupedByPlayer.entries()].map(([player, results]) => {
      const wins = results.filter((result) => result.won).length;
      const losses = results.length - wins;
      return [player, {
        rank: 0,
        player,
        wins,
        losses,
        points: wins * POINTS_PER_WIN + losses * POINTS_PER_LOSS,
      }] as const;
    }),
  );
};

// --- Teilfunktion 4: Nach Punkten sortieren und Rang zuweisen ---
const rankPlayers = (standings: ReadonlyMap<string, StandingsEntry>): StandingsEntry[] =>
  [...standings.values()]
    .sort((entryA, entryB) => entryB.points - entryA.points || entryB.wins - entryA.wins)
    .map((entry, index) => ({ ...entry, rank: index + 1 }));

// --- Teilfunktion 5: Rangliste formatieren ---
const formatStandings = (standings: readonly StandingsEntry[]): string => {
  const header = `${"#".padStart(2)} | ${"Spieler".padEnd(PLAYER_COLUMN_WIDTH)} | W | L | Pts`;
  const separator = "-".repeat(header.length);
  const rows = standings.map(
    (entry) =>
      `${String(entry.rank).padStart(2)} | ${entry.player.padEnd(PLAYER_COLUMN_WIDTH)} | ${entry.wins} | ${entry.losses} | ${entry.points}`,
  );
  return [header, separator, ...rows].join("\n");
};

// --- Pipeline: alle Teilfunktionen zusammensetzen ---
const parsedMatches = parseResults(rawResults);
const matchOutcomes = parsedMatches.map(determineWinner);
const pointsTally = tallyPoints(matchOutcomes);
const rankedStandings = rankPlayers(pointsTally);
const formattedOutput = formatStandings(rankedStandings);

console.log("=== Badminton Turnier-Rangliste ===\n");
console.log(formattedOutput);
console.log(`\n${parsedMatches.length} Spiele ausgewertet, ${rankedStandings.length} Spieler`);
