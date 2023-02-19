# Enemies

Two types:

- Melee
- Ranged

We will first design 3 enemies of each type, with each of those enemies having 3 variants (differentiated by color) that will affect their difficulty.

## Melee

They will follow the player and attack them using weapons or bare hands.

Ideas:

- Normal basic enemy without anything special.
- Slow wide area attack, tanky, high damage.
- Fast attack bursts, small range, little health but fast and not easy to hit, don't deal a lot of damage per attack.

## Ranged

They will keep a distance from the player, this distance will vary depending on the type of enemy.

Ideas:

- Sniper, far away from the player, low attack speed that deal big damage
- Charged shots with slow moving bullets, bullets look bigger and with a brighter color?
- Mid-Range, faster shots than sniper, maybe bursts?

## AI

One for melee and one for ranged.

Melee:

- Health
- Speed
- Aggro range

Ranged:

- Health
- Speed
- Aggro range
- Distance to keep from player
