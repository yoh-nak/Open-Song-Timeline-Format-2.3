# OSTF 2.3.0 — Complete User and Implementer Manual

## Intended audience

Format authors, tooling developers, arrangers, singers/lyricists and GitHub readers. This is a *data format*, not a MIDI engine or a Max for Live device. Nothing in the specification mandates a UI, playback capability, MIDI export or audio recording.

## Quick start

1. Use an `.ostf` file from `samples/` as a template. They are UTF-8 JSON, using `format: OSTF`, `version: 2.3.0` and 960 PPQ.
2. Edit `song.title`, `timeline.sections`, `tempoChanges` and `meterChanges`.
3. To add custom Section roles, declare each `id`/`name` in `roleDefinitions`, then reference it from `sectionRoleAssignments` with the corresponding Section ID.
4. For colors, set `appearance.roleColors`, `customRoleColors` or add entries to `objectColors` with a valid type, referenced ID and `#RRGGBB` color.
5. For Chord/Melody Clip colors, give the target clip a stable `id`; clips without a color reference may omit IDs.
6. Run `python ostf23_validate.py samples/<filename>.ostf`. Use `--json` for machine-readable results.

## Timing and sections

All positions are absolute ticks with PPQ=960. A quarter note is 960 ticks, and a 4/4 bar is 3840 ticks. A 3/4 bar is 2880 ticks; a 6/8 bar is 2880 ticks (6 eighths). `start` is inclusive and the duration end is exclusive. Section IDs must be unique, timeline sections must be ordered and must not overlap. `tempoChanges` and `meterChanges` are chronological. For examples, use `at:0` to declare opening tempo/meter. Do not assume a 4/4-only bar grid when meters change.

## Sections and roles

The base Section `role` is a broad text label. A custom role has a stable ID (e.g. `riff.main`) and a UI-facing name (e.g. `Main Riff`). Link a Section to a custom role via the mapping `sectionRoleAssignments`, keyed by its Section ID. Editing a display name must not change its stable ID.

## Appearance and colors

`roleColors` is a map keyed by base-role identifier, whereas `customRoleColors` keys must reference defined custom roles. `objectColors` is a list of entries `{targetType, targetId, color}` and supports `section`, `chordClip`, `melodyClip`. Each color uses six-digit RGB hex. Do not introduce a color target that does not exist. The same `(targetType,targetId)` may not be specified more than once. Colors are presentation metadata and must not change musical meaning.

## Harmony and melody data

`harmony.chords` is an array of objects and `melodies` is an array of objects with optional `clips` arrays. Stable clip identity and optional `start`/`duration` (as a pair) are the defined 2.3-level rules. Additional musical descriptors and note events carried within those objects can be preserved but cannot be claimed conformant to a complete pitch/rhythm/notation specification solely on the basis of an OSTF 2.3 PASS.

## Lyrics

`lyrics` is an object. When used, `documents`, `phrases`, `units`, `alignments` are arrays of objects whose optional IDs (when supplied) must be unique within each collection. The core release does not interpret kana/romaji segmentation, phonemes, language, pitch matching or score alignment. Those must be separately specified by producers/consumers.

## Unknown information / forward compatibility

Preserve unknown top-level metadata and music-field values where the schema allows them. Preserve unknown extension namespaces. **Never** drop unfamiliar fields silently in a process claiming lossless conversion. The `.draft23` legacy appearance namespace is prohibited in the 2.3 candidate profile; use the standalone stable `org.ostf.section-role-appearance.v1` namespace. Manual editing is recommended rather than assuming migration is lossless.

## Strict file encoding and validation

Use plain UTF-8 *without BOM*. Disallow duplicate JSON keys at any depth, non-finite JSON numbers, malformed Unicode surrogate sequences and lossy overflow/underflow number tokens. The provided CLI checks more than structural validity: it also checks reference and timeline consistency. Exit code 0 means all supplied files pass, 1 means at least one fails, 2 for command usage errors. Example: `python ostf23_validate.py --json samples/*.ostf`.

## Release guarantee and limitations

The version 2.3.0 release guarantees only explicitly documented fields and the accompanying conformance rules. It does not guarantee harmonic correctness, MIDI event correctness, lyrics pronunciation or complete cross-field lyric alignment for opaque payloads. No interoperability testing with other OSTF devices is required for this standalone release.

## Samples guide

All positive sample files use `.ostf` and are intended to PASS using the included CLI. The manifest `samples/INDEX.md` details each coverage topic and each sample is a complete standalone document. They are illustrative, not an assertion that unspecified musical payload schemas are standard. See `docs/PARAMETER_REFERENCE.md` for every defined schema field and `docs/FORMAT_SPECIFICATION.md` for normative boundaries.

## GitHub distribution

Upload the contents of this folder to the root of an OSTF repository (or as a Release ZIP). Tag the repository `v2.3.0`. Retain `LICENSE` under your project's chosen license (none is invented here). GitHub release notes are in `docs/RELEASE_NOTES.md`. Run `python tools/verify_release.py` before tagging to confirm all examples and ZIP-free file inventory. Install Python dependency `jsonschema` using `pip install -r requirements.txt`.
