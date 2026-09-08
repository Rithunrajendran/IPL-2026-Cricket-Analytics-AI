# IPL 2026 Data Dictionary

## matches_2026.csv

| Column | Meaning |
|---|---|
| match_id | Unique match identifier from source |
| season | IPL season |
| match_date | Match date |
| venue | Match venue |
| city | Venue city |
| team1 | First listed team |
| team2 | Second listed team |
| toss_winner | Team winning toss |
| toss_decision | Bat or field decision |
| winner | Match winner |
| result_type | Match result classification |
| player_of_match | Player of the match |

## deliveries_2026.csv

| Column | Meaning |
|---|---|
| match_id | Match identifier |
| innings | Innings number |
| over | Over number |
| actual_delivery | Source delivery number |
| batting_team | Team batting |
| batter | Batter facing delivery |
| bowler | Bowler delivering |
| non_striker | Non-striker |
| batter_runs | Runs scored by batter |
| extra_runs | Total extras on delivery |
| total_runs | Total runs from delivery |
| wides | Wide runs |
| noballs | No-ball runs |
| byes | Bye runs |
| legbyes | Leg-bye runs |
| penalty | Penalty runs |
| is_legal_delivery | 1 for legal delivery, 0 otherwise |
| is_wicket | Whether a wicket event occurred |
| dismissal_type | Type of dismissal |
| player_dismissed | Dismissed player |

## Derived metrics

### Strike Rate

Runs scored per 100 balls faced.

### Economy

Runs conceded per six legal balls.

### Bowling Strike Rate

Legal balls required per bowler-credited wicket.

### Boundary Percentage

Percentage of batting runs coming from fours and sixes.

### Dot-ball Percentage

Percentage of legal balls faced that produced zero batter runs.

### Win Percentage

Wins divided by matches played × 100.

### Run Rate

Runs divided by legal balls × 6.

## ML target

`team1_win`

- `1`: Team 1 won
- `0`: Team 1 did not win

Tie and No Result matches are excluded from the binary match-outcome training dataset.
