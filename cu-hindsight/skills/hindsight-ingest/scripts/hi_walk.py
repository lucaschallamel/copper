"""Which notes a vault offers, and their ids (US-380 AC2, AC8, AC12a).

Forbidden and excluded folders are pruned BEFORE descending: their contents are never
listed, read, scanned or sent. A rule without '/' names a folder at any depth; a rule
with '/' (a leading one included, as in `/_ARCHIVES`) is a path from the vault root.
Rules match case-insensitively (macOS volumes usually are), and ids are Unicode NFC
(macOS stores names decomposed).

Symbolic links are never followed: a link could point into a forbidden folder or out of
the vault. They are reported, never read. A folder that cannot be read stops the walk
(WalkError), so its notes can never be mistaken for deleted ones.
"""

from __future__ import annotations

import os
import unicodedata
from pathlib import Path, PurePosixPath

ALWAYS_EXCLUDED = frozenset({"node_modules"})
ROOT_CHUNK = "_root"
PILOT_CHUNK = "pilot"
RESERVED = (ROOT_CHUNK, PILOT_CHUNK)
PLACEHOLDER_SUFFIX = ".icloud"
DRAWING_SUFFIX = ".excalidraw.md"  # drawing JSON, little prose: opt in (Q29)
NOTE, PLACEHOLDER, LINK = "note", "placeholder", "link"


class ChunkRefused(Exception):
    """A chunk names a forbidden, excluded or missing folder."""


class WalkError(Exception):
    """A folder could not be read; nothing may be concluded about its notes."""


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def key(text: str) -> str:
    """The comparison form of a name or rule: NFC, case-folded."""
    return nfc(text).casefold()


def doc_id(vault: Path, path: Path) -> str:
    """The note's document id: its vault-relative POSIX path, NFC-normalised."""
    return nfc(PurePosixPath(path.relative_to(vault).as_posix()).as_posix())


def _rule_hits(parts: tuple[str, ...], rules: tuple[str, ...]) -> bool:
    folded = tuple(key(p) for p in parts)
    joined = "/".join(folded)
    for raw in rules:
        rule = key(raw.strip("/"))
        anchored = raw.startswith("/") or "/" in rule  # a path from the vault root
        if anchored and (joined == rule or joined.startswith(rule + "/")):
            return True
        if not anchored and rule in folded:
            return True
    return False


def folder_blocked(parts: tuple[str, ...], cfg) -> str | None:
    """Why a vault-relative folder (as parts) is never entered, or None."""
    if any(p.startswith(".") or key(p) in ALWAYS_EXCLUDED for p in parts):
        return "excluded"
    if _rule_hits(parts, cfg.forbidden):
        return "forbidden"
    if _rule_hits(parts, cfg.exclude_dirs):
        return "excluded"
    return None


def _file_excluded(name: str, cfg) -> bool:
    if not cfg.include_drawings and key(name).endswith(DRAWING_SUFFIX):
        return True
    return key(name) in {key(f) for f in cfg.exclude_files}


def id_blocked(note_id: str, cfg) -> str | None:
    """Why an existing document id now falls outside the scope (AC13), or None."""
    parts = tuple(PurePosixPath(nfc(note_id)).parts)
    reason = folder_blocked(parts[:-1], cfg)
    if reason:
        return reason
    return "excluded" if _file_excluded(parts[-1], cfg) else None


def _is_note(name: str, cfg) -> bool:
    return name.lower().endswith(".md") and not _file_excluded(name, cfg)


def _placeholder_note(name: str) -> str | None:
    """`.<note>.md.icloud` is an evicted iCloud note: present, just not downloaded."""
    if name.startswith(".") and name.endswith(PLACEHOLDER_SUFFIX):
        inner = name[1 : -len(PLACEHOLDER_SUFFIX)]
        return inner if inner.lower().endswith(".md") else None
    return None


def _classify(folder: Path, name: str, cfg) -> tuple[Path, str] | None:
    inner = _placeholder_note(name)
    if inner and _is_note(inner, cfg):
        return folder / inner, PLACEHOLDER
    if not _is_note(name, cfg):
        return None
    path = folder / name
    return (path, LINK) if path.is_symlink() else (path, NOTE)


def _raise(err: OSError) -> None:
    raise WalkError(f"cannot read folder '{err.filename}' ({type(err).__name__})")


def walk(vault: Path, root: Path, cfg):
    """Yield (path, kind) per note under root, pruning before descending."""
    for dirpath, dirnames, filenames in os.walk(root, onerror=_raise):
        here = Path(dirpath)
        base = here.relative_to(vault).parts
        dirnames[:] = sorted(
            d
            for d in dirnames
            if not (here / d).is_symlink() and not folder_blocked((*base, d), cfg)
        )
        for name in sorted(filenames):
            found = _classify(here, name, cfg)
            if found:
                yield found


def _entries(folder: Path) -> list[Path]:
    try:
        return sorted(folder.iterdir())
    except OSError as err:
        raise WalkError(
            f"cannot read folder '{folder}' ({type(err).__name__})"
        ) from None


def top_level_dirs(vault: Path, cfg) -> list[Path]:
    return [
        p
        for p in _entries(vault)
        if p.is_dir() and not p.is_symlink() and not folder_blocked((p.name,), cfg)
    ]


def _root_entries(vault: Path, cfg):
    for path in _entries(vault):
        if path.is_file() or path.is_symlink():
            found = _classify(vault, path.name, cfg)
            if found:
                yield found


def _resolve_top(vault: Path, name: str, cfg) -> Path:
    want = name.strip("/")
    reason = folder_blocked(tuple(PurePosixPath(want).parts), cfg)
    if reason:
        raise ChunkRefused(f"refused: '{name}' is {reason}")
    for path in top_level_dirs(vault, cfg):
        if key(path.name) == key(want):
            return path
    raise ChunkRefused(f"no such top-level folder: {name}")


def scan(vault: Path, cfg, chunk: str) -> tuple[list[Path], list[Path]]:
    """A chunk's (readable notes, skipped links): `_root`, `pilot` or a top folder."""
    if chunk == ROOT_CHUNK:
        found = list(_root_entries(vault, cfg))
    else:
        names = cfg.pilot if chunk == PILOT_CHUNK else (chunk,)
        if chunk == PILOT_CHUNK and not names:
            raise ChunkRefused("refused: the config declares no 'pilot' folders")
        roots = [_resolve_top(vault, name, cfg) for name in names]
        found = [item for root in roots for item in walk(vault, root, cfg)]
    notes = sorted(p for p, kind in found if kind == NOTE)
    return notes, sorted(p for p, kind in found if kind == LINK)


def scan_all(vault: Path, cfg) -> tuple[list[Path], list[Path], set[str]]:
    """Every (readable note, skipped link) in scope, and every id present (AC12a)."""
    found = list(_root_entries(vault, cfg))
    for top in top_level_dirs(vault, cfg):
        found += list(walk(vault, top, cfg))
    notes = sorted(p for p, kind in found if kind == NOTE)
    links = sorted(p for p, kind in found if kind == LINK)
    present = {doc_id(vault, p) for p, kind in found if kind != LINK}
    return notes, links, present


def chunk_files(vault: Path, cfg, chunk: str) -> list[Path]:
    return scan(vault, cfg, chunk)[0]


def chunk_names(vault: Path, cfg) -> list[str]:
    return [ROOT_CHUNK, *(p.name for p in top_level_dirs(vault, cfg))]


def present_ids(vault: Path, cfg) -> set[str]:
    return scan_all(vault, cfg)[2]
