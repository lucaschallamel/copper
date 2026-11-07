---
name: master-asl-rules
description: Advanced Squad Leader rules knowledge , the ASLRB chapter structure, core and advanced mechanics, SSR interpretation, and the errata landscape. Use when resolving a rules question mid-game, interpreting a scenario special rule, or looking up how an interaction actually works.
version: 1.0.0
last_updated: '2026-09-08'
maintained_by: Lucas Challamel
---

# Master ASL Rules (qd-master-asl-rules)

Reusable ASL rules knowledge. This skill is the single source of truth for the capability; the
`qd-masters:master-asl-rules` command invokes it for a rules question.

## Role Overview

ASL's reputation for difficulty is a cataloguing problem more than a complexity problem. The rules
are internally consistent; what defeats people is not knowing WHERE a rule lives or which of several
plausible readings the rulebook actually intends. This skill is the map.

## The Rulebook's Shape

Knowing the chapter a question belongs to is most of the answer:

- **Chapter A , Infantry** , movement, fire, morale, close combat. The spine; most questions start
  here.
- **Chapter B , Terrain** , what each hex type does to movement, LOS and cover. The most consulted
  chapter mid-game.
- **Chapter C , Ordnance** , guns, to-hit and to-kill procedures, ammunition types.
- **Chapter D , Vehicles** , armour, movement, target acquisition.
- **Chapters E onward** , night, weather, fortifications, air support, off-board artillery,
  boats, cave terrain. Consulted only when a scenario invokes them.
- **Module rules** , per-title additions (Beyond Valor, Yanks, Hollow Legions, Rising Sun, West of
  Alamein, and the rest). A module rule beats the base rulebook for its own content.

## Precedence, and why it settles most disputes

Conflicts resolve in a fixed order , this is the single most useful thing to know:

1. **SSR (Scenario Special Rules)** , override everything for that scenario. Written to make one
   historical situation work; they are not general precedent.
2. **Official errata** , correct the printed rulebook. A rule as printed may simply be wrong.
3. **Module rules** , override the base rulebook within their own domain.
4. **The ASLRB** , the default.

Community rulings and tournament practice are **not** in this hierarchy. They are evidence of how a
rule is usually read, useful when the text is genuinely ambiguous, and never authoritative over it.

## Core Mechanics

The interactions that generate most questions:

- **Fire resolution** , the IFT with its DRM stack. Almost every "why did that happen?" is a DRM the
  player did not count. Enumerate the stack explicitly rather than asserting a total.
- **Morale and rout** , the pin/break/rout chain, leadership modifiers, and where a broken unit is
  permitted to go. Rout paths are more constrained than they look.
- **Line of sight** , hindrance versus blockage, and the fact that LOS is reciprocal but cover is
  not.
- **Close combat** , the odds table, ambush, and the sequencing that decides who is even eligible.
- **Sequence of play** , most illegal actions are legal actions attempted in the wrong phase.

## Answering a Rules Question

1. **Locate the chapter** , the answer's address is most of the answer.
2. **Check SSR first**, then errata. Both are cheap to check and both override the text.
3. **Quote the rule**, with its number. A paraphrase is where misreadings enter.
4. **State the mechanism, not just the verdict** , why the rule produces this result, so the next
   similar question does not need asking.
5. **Say when it is genuinely ambiguous.** Some interactions are unsettled; naming that is more
   useful than inventing a confident answer.

## Quality Standards

- Every answer cites a rule number, not a recollection
- SSR and errata are checked before the base rulebook is quoted
- DRM and modifier stacks are enumerated item by item, never given as a total
- Genuine ambiguity is reported as ambiguity
- The mechanism is explained, so the answer teaches rather than only resolves

## Boundaries

This skill knows what the rules SAY. What to DO with them , which tactic suits a situation , is
`qd-masters:master-asl-doctrine`; planning a scenario before play is `qd-masters:master-asl-scenario-analysis`;
teaching a learner and pacing their progress is `qd-coaches:coach-asl`.
