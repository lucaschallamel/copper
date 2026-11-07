---
name: hindsight-ingest
description: Ingest an Obsidian vault's Markdown notes into the vault's own Hindsight memory bank and keep it in sync, behind a local secret gate. Use when setting up shared agent memory for a vault, sending a folder, previewing what would be redacted, forgetting notes, or scheduling nightly sync.
version: 1.1.0
last_updated: '2026-10-25'
maintained_by: Lucas Challamel
---

# Hindsight vault ingestion (hindsight-ingest)

One vault, one Hindsight bank. The tool reads the vault's `.hindsight-ingest.json`, redacts and
gates every note locally, and sends only what passes, in small throttled batches that can be
resumed. Vault content leaves the machine, so **the user runs every command that talks to the
server**; the agent prepares, explains and reads the reports.

## Before anything

- `HINDSIGHT_URL` and `HINDSIGHT_API_KEY` are set in the user's shell. Never ask for, print or write
  the key. The tool reads both from the environment only.
- `gitleaks` is on the PATH; the tool refuses to run without it.
- **Where the content goes**: to the Hindsight server, AND to the LLM provider the server extracts
  memories with (a hosted model API, a subscription CLI, or a local model). Find out which before
  the first send.
- The script: `scripts/hindsight_ingest.py` in this skill's own folder, run with
  `python3 -I <script> --vault <vault> <command>` (Python 3.11+, standard library only). When
  handing a command to the user, resolve the script's absolute path first: a variable set inside the
  agent session does not exist in the user's shell.

## Setup questions

Ask these one at a time, each with clickable options and a recommendation, then write the config:

1. **Provider**: which LLM provider does the server use, and may this vault's content go to it? If
   not, stop: no config is written.
2. **Transport**: `https://` (recommended), loopback, or a tailnet host over plain `http://` (needs
   `"allow_insecure_transport": true`; the tool checks the resolved address, never the name).
3. **Scope**: which folders are `forbidden` (never listed, read, scanned or sent), which go in
   `exclude_dirs` (transit or archive folders) and which files in `exclude_files` (agent files such
   as `AGENTS.md`, notes holding a third party's identity data).
4. **Detectors**: password lines are always redacted; add `"fr-nir"` (French social-security
   numbers) and `"iban"` where the vault holds them.
5. **Pilot**: one or two small folders to try first.
6. **Sync host**: the one machine allowed to run `sync` (`sync_host`).

See `resources/config-example.md` for every key. An unknown key is an error, on purpose.

## Workflow

```bash
S=/absolute/path/to/this/skill/scripts/hindsight_ingest.py
python3 -I $S --vault ~/vault check                  # server version, required paths, gitleaks
python3 -I $S --vault ~/vault init-bank              # only if the bank is new; type its name to confirm
python3 -I $S --vault ~/vault chunks                 # folders and note counts (local)
python3 -I $S --vault ~/vault dry-run pilot          # what would be sent, redacted, skipped (local)
python3 -I $S --vault ~/vault preview Folder/note.md # redacted lines only, safe to paste
python3 -I $S --vault ~/vault send pilot
```

Then verify recall from an agent session on the vault bank, and send the rest **folder by folder**
(`send <folder>`, `send _root`), reading each report. A `SECRET?` line means the note was skipped:
fix or exclude it. `send` never deletes: a note sent before keeps its old copy until `sync` purges
it, and the report says so. On any error the run stops and says so; re-run the same command to
resume.

## Keeping the bank in step

```bash
python3 -I $S --vault ~/vault sync --dry-run # adds, updates, deletes and purges, nothing sent
python3 -I $S --vault ~/vault sync
python3 -I $S --vault ~/vault schedule --at 02:30
```

- `sync` sends new or changed notes, deletes documents whose note is gone, and purges notes under a
  folder that became forbidden or excluded, and sent notes the gate now calls secret (an edit, new
  rules or a new gitleaks binary; a clean edit sends them again). Secret purges are never `HELD`:
  holding them would keep a secret on the server, so `sync --dry-run` first after a gitleaks
  upgrade. A purge cleans the live bank (the document and the memories built from it); the server's
  LLM provider and backups saw the note already, so `sync` tells the user to rotate the secret and
  exits 1, so a scheduled run shows as failed (`systemctl --user --failed`). A new gitleaks binary
  makes the first `sync` re-scan every sent note once; nothing unchanged is re-sent. Two files that
  normalise to one note id (the same accented name stored two ways) are never sent and are listed as
  `duplicate-id`: rename one. It deletes **only documents this tool sent**: memories agents wrote
  into the same bank are never touched.
- Evicted iCloud notes (`.<name>.md.icloud`) count as present. If more than `max_delete_ratio`
  (default 10%) of the sent notes look missing, `sync` deletes nothing and lists them as `HELD`.
- `sync` runs only on `sync_host`. Notes sent by hand from another machine are re-sent once by the
  sync host (state is per machine).
- `schedule` writes a systemd timer (Linux) or a launchd plist (macOS) to a staging folder and
  prints the install commands for the user to run; it never enables anything. Credentials go in an
  env file the user creates with mode 600. Re-run `schedule` after the kit is updated, since the
  script path may change.

## Forgetting

`forget <note|folder>...` deletes those documents; `forget --all` deletes everything this tool sent
to the bank after the user types the bank name. Use it when a secret slipped through or a vault is
retired. `forget` removes documents from the live bank only: backups or exports of the server keep
them until those are purged or rotated, which is the server operator's job.

## Moving from a hand-run pilot script

`import-state <pilot>/hindsight_state.json` records the pilot's sent notes without sending them
again. Every pilot note becomes this tool's own: one changed since, gone, or now out of scope
(forbidden, excluded, a drawing) is re-sent, deleted or purged by the next `sync`, which also runs
gitleaks over every imported note once (the pilot never did) and purges any it flags. Run
`sync --dry-run` next: notes the pilot sent under a non-NFC name (accented paths stored decomposed)
are listed as `RENAME`: deleted and re-sent once under the NFC id, without tripping the mass-delete
guard.

## Guarantees worth knowing

- **Symbolic links are never followed** (a link could lead into a forbidden folder or out of the
  vault); they are listed as `SKIP ... (symlink, never followed)`.
- Folder rules: a bare name matches at **any depth**, a rule with `/` (a leading `/` included, as
  `/_ARCHIVES`) matches **from the vault root** only. Folder and file rules match
  **case-insensitively**; a malformed rule (`./x`, `a/../b`, stray spaces) is refused rather than
  silently matching nothing.
- A folder that cannot be read **stops** the run: `sync` never treats unreadable notes as deleted.
- **One vault per bank**: the state records its vault and refuses another; one run at a time per
  bank (a second run waits for the first to finish).
- Enabling a detector later re-checks every note, so already-sent notes are re-sent masked.
- Excalidraw drawings (`*.excalidraw.md`) are skipped unless `"include_drawings": true`: they are
  mostly drawing data, which sets off the masks and costs extraction for little memory.
- `pilot` and `_root` are reserved chunk names: a top folder with either name is sent by `sync`.

## Limits

Markdown only; notes above `max_chars` are skipped (PDF, Office and splitting are follow-ups). The
server builds memories asynchronously: a successful send means queued, and each batch's
`operation_id` is in the log beside the state (`status` shows where).
