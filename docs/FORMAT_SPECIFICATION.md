# OSTF 2.3 RC1 — Standalone Conformance Profile

Status: **RC1 PUBLIC TEST SPECIFICATION**, 2026-10-24. This document is the proposed single entry point; older draft documents are historical and **not independently normative**. No external device interoperability is a release gate.

## 1. Document identity and version

A 2.3 standalone document is a JSON object with `format: "OSTF"`, `version: "2.3.0"`, `ppq: 960`, and required top-level `song`, `timeline`, `harmony`, `melodies`, `lyrics`, and `extensions`. File suffix `.ostf`; UTF-8 JSON. Array order is significant; object key order is not.

## 2. Structure and semantic validation

The RC1 structural grammar is `schema/ostf-2.3-standalone-candidate.schema.json` (JSON Schema 2020-12). The RC1 normative acceptance verdict is **schema validation AND** `standalone_conformance99.check()` producing no errors. JSON Schema alone is not sufficient for Section/Clip ID uniqueness, referential integrity, ordering or timing bounds.

### 2.1 Sections

`timeline.sections` contains Sections with stable, unique nonempty IDs, integer `start >= 0`, positive integer `duration`, and typed properties as defined by the schema. Sections are ordered and nonoverlapping. Their bounds are measured in 960 PPQ ticks. Sections may be split/merged/reordered only by implementations that preserve or explicitly update all related music references. The *file format* does not require an editor to implement these operations.

### 2.2 Roles and appearance

The sole RC1 release namespace is `extensions["org.ostf.section-role-appearance.v1"]` with `version: "1.0.0"` and `data`. Custom Role ID is stable and distinct from display name; per-Section assignment references a defined Custom Role. `appearance.roleColors` and `customRoleColors` supply UI colors; `objectColors` targets a Section, chordClip, or melodyClip with a `#RRGGBB` color. Colors **must not** modify musical timing, pitches, or rendering playback semantics. An unresolved or duplicate color target is invalid. No implied color on absence.

### 2.3 Clip identity

`harmony.chords[].id` and `melodies[].clips[].id` are optional for uncolored clips. A clip referenced by a color MUST have a nonempty ID. Within each clip type, present IDs are unique; IDs may coincide between different clip types. This scheme addresses color *references*, not musical phrase identity across different files.

### 2.4 Time and events

Timeline positions and durations use PPQ ticks. Clip `start` and `duration` must either both exist or both be absent. If present: `start` is a nonnegative integer and `duration` a strictly positive integer. The semantic checker further checks bounds and tempo/meter ordering as implemented in `event_timing103.py`.

### 2.5 Music content and opaque fields

**Important scope boundary:** OSTF 2.3 does NOT redefine all inner Harmony/Melody/Lyrics semantics. The schema ensures the candidate envelope and selected collection shapes. Extra fields in music objects and unknown extensions are opaque and preserved by lossless transformations; there is no promise that their unrecognized musical meaning is validated. Therefore a completely arbitrary payload passing the structural profile must not be described as fully music-semantically validated. Implementations must not reinterpret or erase unknown data silently.

### 2.6 Lyrics

`lyrics.documents`, `lyrics.phrases`, `lyrics.units` and `lyrics.alignments` are collection objects (when present), with IDs unique within their own collection. Cross-collection IDs may coincide. No additional phoneme, syllable, lyric-to-note mapping or language semantics are introduced in 2.3.

## 3. Migration and compatibility

`org.ostf.section-role-appearance.draft23` is **not permitted** as the release namespace. The migration tool `namespace_migration98.py` is provisional and refuses conflicting namespace content. Legacy export is potentially lossy; no silent downgrade is permitted. Interoperability with other OSTF devices is explicitly outside the standalone release criteria.

## 4. RC1 conformance and publication scope

The bundled `schema/ostf-2.3-standalone-candidate.schema.json` and `ostf23_validate.py` together define the executable RC1 acceptance profile. The `conformance_113/manifest.json` lists byte-level positive and negative fixtures. A PASS certifies the defined envelope, role/color/ID/timing constraints and strict JSON ingestion, **not** complete correctness of arbitrary harmonic, MIDI-note or lyric contents. Reader/writer implementations preserve unknown fields without silently deleting them. This is a *public test release candidate*, not the final OSTF 2.3.0 standard.

## 5. Draft 109 wire-level JSON conformance (proposed normative addition)

A conforming `.ostf` release-candidate file MUST decode as strict UTF-8 and MUST be a single JSON document (RFC 8259 compatible). Duplicate keys at *any depth* are invalid, rather than allowing silently implementation-dependent last-key-wins parsing. `NaN`, `Infinity` and `-Infinity` are invalid JSON. A UTF-8 BOM is not accepted by the candidate strict profile. No reordering of object keys is required for acceptance; arbitrary unknown extension JSON object content is preserved.

The complete acceptance path is **`strict_json109.loads_wire` → `standalone_conformance99.check`**. Validating a Python object alone does not validate the bytes on disk and cannot detect duplicate keys already discarded by a permissive parser. `strict_json109.check_file` and `check_wire` are the reference ingress checks. These rules govern the standalone `.ostf` file format, not device APIs.

These rules are adopted for the RC1 public test profile.

## 6. Draft 110 additional wire safety rules (candidate)

OSTF 2.3 strict JSON readers reject unpaired surrogate code points in decoded JSON values or property names, including escaped lone UTF-16 surrogates; valid escaped pairs are allowed. The reference validator additionally rejects JSON real-number tokens that overflow to non-finite binary floats. The strict JSON reader implementation included here defines the executable rule.

## 7. Draft 111 finite-number ingress rule (candidate normative)

For the current reference wire reader, each JSON floating-point token MUST decode to a finite binary64 value. A mathematically nonzero token which converts to positive or negative zero is rejected rather than silently losing magnitude. Exact zero tokens (`0.0`, `-0e-999`) are allowed, as are nonzero representable subnormals. No limit is imposed on JSON integer tokens at the lexical layer; typed timing values remain subject to their schema constraints. This is the **RC1 transport profile**; cross-language implementation portability is not yet certified. Strict ingress is not interchangeable with parsing through permissive JSON libraries.

The `strict_json109.py` module keeps its name for import stability but includes the Draft 110 and 111 rules. The rules do not imply complete fidelity for all finite decimal fractional tokens; ordinary IEEE-754 rounding can still occur.

RC1 is released only for public testing and feedback; the final 2.3.0 specification is not yet approved. Other OSTF device compatibility is not a release gate.


---

# OSTF 2.3.0 — Final Release Scope / Specification Freeze Proposal

Status: **technically releasable under this bounded conformance profile; official publication and maintainer approval not represented as completed.**

## Fixed wire profile

- `.ostf` is a UTF-8 JSON document; strict decoding rejects BOM, duplicate keys, invalid Unicode and non-finite/overflow/underflow floating-point tokens per bundled strict reader.
- Root `format` = `OSTF`; `version` = `2.3.0`; `ppq` = `960`.
- Required containers and structural constraints are defined by `schema/ostf-2.3-standalone-candidate.schema.json`.
- Extension namespace `org.ostf.section-role-appearance.v1` (`version: 1.0.0`) is the release profile.
- Section IDs, roles, appearance, color target references, optional clip identities, tempo/meter ordering and clip timing are checked by the bundled semantic validator.
- The conformance verdict is successful strict ingress **and** JSON Schema **and** semantic validation; the CLI `ostf23_validate.py` is the release reference entrypoint.

## Deliberate limitations

Harmony, Melody and Lyrics nested payloads beyond explicit schema/validator rules are **opaque**: the standard does **not** certify their harmonic correctness, full MIDI note semantics, vocal pronunciation, or lyric alignment. A PASS therefore does not assert fully valid music semantics. Unknown music/extension data must be preserved by transformations that claim round-trip fidelity.

Other OSTF device compatibility is **not** a release criterion and was not evaluated. The underlying RC1 schema filename remains unchanged to avoid a last-minute untested renaming.

## Publication decision

Technical recommendation: **GO to publish OSTF 2.3.0 with the above explicit limitations.** The maintainer must decide whether to adopt this limited scope and publish/tag it. This archive is a final release candidate, not evidence of external publication, independent certification, or the maintainer's approval.
