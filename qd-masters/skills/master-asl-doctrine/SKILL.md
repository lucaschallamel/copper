---
name: master-asl-doctrine
description: Tactical doctrine for Advanced Squad Leader , fire and movement, per-nation national characteristics, terrain employment, and combined arms. Use when deciding HOW to fight a situation rather than what a rule permits, or when a nationality's units should be handled differently.
version: 1.0.0
last_updated: '2026-09-08'
maintained_by: Lucas Challamel
---

# Master ASL Doctrine (qd-master-asl-doctrine)

Reusable ASL tactical knowledge. This skill is the single source of truth for the capability; the
`qd-masters:master-asl-doctrine` command invokes it for a tactical question.

# Role Overview

Rules say what is permitted; doctrine says what works. The gap between a player who knows the rules
and one who wins is almost entirely here , and most of it reduces to a handful of ideas applied
consistently rather than a large body of tricks.

## The Load-Bearing Principles

- **Fire and movement, never movement alone.** A unit moving in the open without covering fire is
  giving the defender a free shot. The covering fire does not need to kill; it needs to make the
  defender choose.
- **Concentration beats distribution.** Three squads firing at one target usually beats three squads
  firing at three. The IFT rewards mass.
- **Terrain is the cheapest force multiplier.** A squad in a building or woods is worth several in
  the open. Buying position costs movement, not casualties.
- **The defender's problem is frontage, the attacker's is time.** A defence cannot cover everything;
  an attack cannot take forever. Each side attacks the other's constraint.
- **Leaders are the scarcest resource.** Their modifiers apply to rally, fire and morale
  simultaneously. Losing one is worse than losing the squad beside it.

## National Characteristics

Nationality is not flavour , it changes correct play:

- **German** , strong leadership and squad quality; the doctrine assumes initiative at low level and
  rewards aggressive fire-and-movement.
- **Soviet** , mass and cheap infantry, weaker leadership. Correct play accepts losses to achieve
  concentration; hesitancy is the expensive mistake.
- **American** , firepower and support weapons, strong ordnance. Fight by attrition from cover
  rather than by manoeuvre where possible.
- **British** , solid infantry with distinctive support-weapon handling. Positional and methodical.
- **Japanese** , unique close-combat and morale rules that make ordinary defensive assumptions
  unsafe. Read the specific rules before applying general doctrine.
- **Finnish, Italian, French, and the rest** , each has at least one rule that inverts a general
  assumption. Check before assuming a nationality plays like its neighbour.

## Combined Arms

- **Armour without infantry is a target.** Unescorted tanks in close terrain are killed by things
  they cannot see.
- **Infantry without armour is slow.** Armour buys tempo, which is the attacker's scarce resource.
- **Ordnance shapes the fight before it starts.** Guns and off-board artillery deny ground rather
  than take it; site them for what they prevent.
- **Smoke is the most undervalued asset.** It converts an impossible approach into a merely costly
  one, and it costs nothing but a placement.

## Answering a Tactical Question

State the SITUATION's constraint first , what does each side lack? Then propose an approach and name
what it trades away. A tactical answer with no cost stated is incomplete: every option spends
something (time, casualties, position, initiative), and naming the spend is what makes the advice
usable.

## Quality Standards

- Every recommendation names what it trades away
- Nationality is checked before general doctrine is applied
- Advice cites the situation's actual constraint, not a general maxim
- Where a rule makes the general principle wrong, the rule wins , say so and point at
  `qd-masters:master-asl-rules`

## Boundaries

This skill decides HOW to fight. What the rules permit is `qd-masters:master-asl-rules`; planning a specific
scenario before play is `qd-masters:master-asl-scenario-analysis`; teaching and pacing a learner is
`qd-coaches:coach-asl`. General strategic method beyond this game is `qd-masters:master-strategist` , this skill is
the named game's craft, as `qd-masters:master-chess` is for chess.
