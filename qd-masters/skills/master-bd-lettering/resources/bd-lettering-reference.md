---
title: 'BD balloon taxonomy, text budgets and EN/FR onomatopoeia banks'
version: '1.0.0'
last_updated: '2026-09-10'
maintained_by: 'Lucas Challamel'
---

# BD lettering

Enumerated reference for `qd-masters:master-bd-lettering`. Consulted during a scripting pass , balloon
types, the word budgets, condensation technique and the sound-effect banks, kept verbatim.

## Balloon taxonomy

- **Speech balloon**: standard rounded outline, for spoken words
- **Thought bubble**: cloud-shaped, for internal monologue
- **Whisper balloon**: dashed outline, for quiet speech
- **Shout balloon**: spiky or jagged outline, for yelling
- **Radio / phone**: zigzag or electrical outline, for transmitted speech
- **Narrative caption**: rectangular box, for narration

## Text volume , the operational limits

- **Maximum per balloon**: ~25-30 words (readability limit)
- **Balloons per panel**: typically 1-3; more overcrowds
- **Caption density**: 1-2 captions per panel maximum
- **Silent panels**: embrace wordless storytelling when the visuals suffice

## Lettering style

- **Case**: ALL CAPS (traditional BD standard) or sentence case (modern preference)
- **Bold / italic**: emphasis sparingly , bold for loudness, italic for emphasis or thought
- **Size variation**: larger letters read as louder
- **Sound effects**: creative typography, size reflecting intensity

## Condensation technique

Prose:

> "I've been thinking about what you said last week, and I have to admit that you might have been
> right about the whole situation with the committee."

Balloon-ready:

> "You were right about the committee."

**Principles** , cut verbal padding ("I think", "you know", "kind of"); remove what the image
already shows; imply context readers infer from previous panels; preserve subtext, which is what
makes the line interesting; maintain the character's distinct speech pattern.

**Keep**: emotional content, character-specific vocabulary, story-advancing information,
relationship dynamics, humour and wit.

**Cut**: stage direction, obvious reactions the art shows, excessive politeness, thinking aloud that
adds no information.

## Multi-balloon splitting

Split at complete thoughts, never mid-thought.

- **Bad** , Balloon 1: "I went to the store and bought" / Balloon 2: "milk and bread."
- **Good** , Balloon 1: "I went to the store." / Balloon 2: "Got milk and bread."

Split at sentence breaks and between ideas; maximum 2-3 balloons per character per panel; balloon
tails indicate reading order.

## Captions , add value, never redundancy

**Types**: time/location establishing ("Paris. 1944.", "Three days later..."); narrative voice when
the POV character has a distinctive internal register; exposition only when the visuals cannot carry
it; internal thought as a more literary alternative to a thought bubble, preferred for serious BD.

**Use for**: time jumps, scene establishment, literary internal monologue, information impossible to
show (smells, abstract concepts), dramatic irony.

**Do not use for**: describing what is clearly visible; stating emotions the art already shows;
redundant action description.

**Placement**: top of panel sets context before the reader takes in the image; bottom comments on or
responds to it. Never block important visual elements.

## Sound effects , English bank

- **Impact** (hits, crashes): BOOM, BANG, CRASH, THUD, WHAM, SLAM, CRACK, SMASH , intensity through
  larger, bolder letters and more exclamation marks
- **Movement** (motion, vehicles): WHOOSH, ZOOM, VROOM, SWOOSH, ZIP, SCREECH , can arc along the
  motion path
- **Mechanical** (doors, machines): CLICK, CLACK, WHIRR, BEEP, BUZZ, HUM, CREAK, GROAN
- **Environmental** (nature, weather): SPLASH, DRIP, RUSTLE, HOWL, CRACK (thunder)

**Intensity ladder**: quiet `_tap_` -> moderate KNOCK KNOCK -> loud **BOOM** -> extreme
**BOOOOOM!!**

**Placement equals source**: position the effect near its source; it may overlap panel borders for
extreme sounds; integrate it into the artwork rather than floating it.

## Sound effects , French bank

Categorised to match the English bank above, since the form is Franco-Belgian. Category parity, not
token parity: the same four categories, 25 tokens to the English bank's 26.

- **Impact** (chocs, coups): BOUM, VLAN, PAF, BANG, CRAC, SBAM, TCHAC, POUM
- **Movement** (mouvement, véhicules): VROUM, ZIOU, FROU, SCHTONK, VLOUF
- **Mechanical** (portes, machines): CLIC, CLAC, DZING, DRING, TIC-TAC, GRRR, COUIC
- **Environmental** (nature, météo): PLOUF, SPLATCH, FLOC, OUUUH, CRAAAC (tonnerre)

**Language selection** is an output parameter, not a fixed choice: `[English | French | Mixed]`.
Match the sound-effect language to the dialogue language, or keep the iconic English forms where the
album convention calls for it , both are current Franco-Belgian practice.

**Invention is legitimate**: "FZZZZT" for electricity, playful forms such as "bloop", "squelch",
"kathunk". Match the register to the story's tone.

## Balloon placement

**Reading order** , Western flow: the top-left balloon is read first, then left-to-right and
top-to-bottom; the balloon tail direction reinforces that order.

**Guidelines**: balloons must not obscure faces or key action; leave spacing from panel edges; tails
point clearly at the speaker; overlapping balloons indicate reading sequence.

**Formats**

- Speech , `[CHARACTER]: "Dialogue text."`
- Thought , `[CHARACTER] (thinks): "Thought text."`
- Caption , `[CAPTION]: "Narrative text."`
- Sound effect , `[SFX]: SOUND` (integrated into the art, no balloon)

## Comic-script output contract

```markdown
## BD Page [#] , Comic Script

### Panel [#]: [brief panel description]

**CAPTION** (top): "..."

**[CHARACTER NAME]** (speech balloon): "..."

**SFX**: _CREAK_ [door opening]

**Placement Notes**:

- [caption position]
- [balloon position and tail direction]
- [SFX position relative to source]

### Script Summary / Character Voice Verification / Text Density Check

**Language**: [English | French | Other] **Sound Effect Language**: [English | French | Mixed]
```

## Quality bar

Non-negotiable , balloons never exceed ~30 words; each character sounds distinctly themselves; text
does not obscure critical artwork; reading order is always clear.

Excellence , concision mastery, subtext preserved through condensation, silent panels embraced when
the art carries the beat, inventive onomatopoeia, and captions that add value rather than repeat.
