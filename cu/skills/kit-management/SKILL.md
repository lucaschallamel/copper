---
name: kit-management
description: Runtime kit package-manager skill , install and surgically uninstall capability kits onto a host harness. Use when installing a kit, uninstalling a kit, or reasoning about the install-record, dependency-closure resolution, or checksum-gated removal. Tier-2 white-label core (no organisation identity).
version: 1.0.0
last_updated: '2026-06-07'
maintained_by: Lucas Challamel
---

# Kit Management

The runtime package-manager capability for kits: install a kit (and its dependency closure) onto a
host, and uninstall it surgically using a per-install record. Implements the ADR-019 "package
manager, not build-time compile" model against the frozen install-record + adapter seam (kit SPEC
section 5).

This is Tier-2 white-label core: it carries no organisation identity and depends on no kit. The
per-target asset prefix is applied by the adapter at install time, not embedded here.

## Goal

Let a host install and remove optional capability kits at runtime, on top of a running core, the way
`apt`/`brew`/`npm` add and remove packages , reversibly and auditably.

## When to Use

When a user runs `/cu:kit install <kit>` or `/cu:kit uninstall <kit>`, or when reasoning about kit
resolution, the install-record, or safe removal.

## Setup

The install/uninstall algorithms live in the `deploy.kit` Python package; the `/cu:kit` command is the
harness-facing surface. No host configuration is required beyond a kit source (a local `kits/` tree
for the MVP).

## Steps

1. **Install**: resolve the kit + its dependency closure (pinned-only, prerequisites first); plan
   all placements and refuse on any conflict BEFORE touching the host (no silent clobber); place
   additively; write one install-record per kit (paths + SHA-256 checksums + provenance).
2. **Uninstall**: read the kit's install-record; for each placed file, checksum-gate before deleting
   , a file whose checksum still matches is removed; a user-modified file is preserved and flagged,
   never blind-deleted; reverse recorded config deltas; refuse if another installed kit still
   depends on this one.

## Constraints

Pinned-only resolution for the MVP (no version ranges). Additive-only placement, refuse-on-conflict.
One host (the current harness) per the MVP. Authoring exemplars under a reserved reference area are
excluded from installation.

## Safety Notes

Surgical uninstall is checksum-gated: a user-modified file is never blind-deleted. Installs refuse
rather than partially applying on conflict (no half-modified host). The install-record is plaintext
local state and MUST NOT contain secrets , config that needs a credential references it indirectly
(an env-var name or secret-manager path), never the literal value.
