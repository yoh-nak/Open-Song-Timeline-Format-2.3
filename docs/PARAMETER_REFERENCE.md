# Complete Parameter Reference — OSTF 2.3.0

### Normative scope and semantics

- A **required** field is required in its immediate parent if that parent exists. Parent containers may themselves be optional.
- Paths ending in `[]` denote an array element. `additionalProperties=allowed` means further members are structurally accepted, **not** that their music meaning is standardized.
- Value constraints listed here are generated from the actual bundled JSON Schema; **cross-field rules** also require the standalone validator.
- `roleDefinitions[].id` is a unique custom role ID, independent of `name` (UI text). `sectionRoleAssignments` keys reference Section IDs and values reference custom Role IDs.
- `objectColors` references `(targetType, targetId)` and rejects unresolved and duplicate targets. `targetType` is `section`, `chordClip` or `melodyClip`.
- `harmony.chords[].id` and `melodies[].clips[].id` are optional except when referenced by colors; IDs must be unique within their respective types.
- `start`/`duration` are expressed in 960-PPQ ticks. If present on a clip they must be present together. Timeline ordering and end boundaries are validated semantically.
- `lyrics.documents`, `phrases`, `units`, `alignments` are optional arrays with unique IDs *within each collection*. The internal pronunciation, note alignment and lyric language are **not** normalized by this release.
- Strict UTF-8, duplicate-key rejection, JSON integer/real lexical handling and invalid Unicode rejection are defined by `strict_json109.py`.
- Extra Harmony/Melody/Lyrics members and unknown extensions are opaque pass-through fields. No finite list of named keys is possible for open extension payloads; the inventory below covers **all explicitly named fields in the shipped schema**.


## Every named schema field

| Path | Presence in parent | Type/allowed values | Structural restrictions |
|---|---|---|---|
| `$` | optional | object | additionalProperties=allowed |
| `format` | required | const: OSTF | — |
| `version` | required | const: 2.3.0 | — |
| `ppq` | required | const: 960 | — |
| `song` | required | object | — |
| `timeline` | required | object | — |
| `timeline.sections` | required | array | minItems=1 |
| `timeline.sections[]` | optional | object | — |
| `timeline.sections[].id` | required | string | minLength=1 |
| `timeline.sections[].name` | required | string | minLength=1 |
| `timeline.sections[].start` | required | integer | minimum=0 |
| `timeline.sections[].duration` | required | integer | minimum=1 |
| `timeline.sections[].role` | optional | string | — |
| `timeline.meterChanges` | required | array | minItems=1 |
| `timeline.meterChanges[]` | optional | object | — |
| `timeline.meterChanges[].at` | required | integer | minimum=0 |
| `timeline.meterChanges[].numerator` | required | integer | minimum=1 |
| `timeline.meterChanges[].denominator` | required | enum: 1, 2, 4, 8, 16, 32, 64 | — |
| `timeline.tempoChanges` | required | array | minItems=1 |
| `timeline.tempoChanges[]` | optional | object | — |
| `timeline.tempoChanges[].at` | required | integer | minimum=0 |
| `timeline.tempoChanges[].bpm` | required | number | exclusiveMinimum=0 |
| `harmony` | required | object | additionalProperties=allowed |
| `harmony.chords` | optional | array | — |
| `harmony.chords[]` | optional | object | additionalProperties=allowed |
| `harmony.chords[].id` | optional | string | minLength=1 |
| `harmony.chords[].start` | optional | integer | minimum=0 |
| `harmony.chords[].duration` | optional | integer | minimum=1 |
| `melodies` | required | array | — |
| `melodies[]` | optional | object | additionalProperties=allowed |
| `melodies[].clips` | optional | array | — |
| `melodies[].clips[]` | optional | object | additionalProperties=allowed |
| `melodies[].clips[].id` | optional | string | minLength=1 |
| `melodies[].clips[].start` | optional | integer | minimum=0 |
| `melodies[].clips[].duration` | optional | integer | minimum=1 |
| `lyrics` | required | object | additionalProperties=allowed |
| `lyrics.documents` | optional | array | — |
| `lyrics.documents[]` | optional | object | additionalProperties=allowed |
| `lyrics.documents[].id` | optional | string | minLength=1 |
| `lyrics.phrases` | optional | array | — |
| `lyrics.phrases[]` | optional | object | additionalProperties=allowed |
| `lyrics.phrases[].id` | optional | string | minLength=1 |
| `lyrics.units` | optional | array | — |
| `lyrics.units[]` | optional | object | additionalProperties=allowed |
| `lyrics.units[].id` | optional | string | minLength=1 |
| `lyrics.alignments` | optional | array | — |
| `lyrics.alignments[]` | optional | object | additionalProperties=allowed |
| `lyrics.alignments[].id` | optional | string | minLength=1 |
| `extensions` | required | object | additionalProperties=allowed |
| `extensions.org.ostf.section-role-appearance.v1` | optional | object | additionalProperties=allowed |
| `extensions.org.ostf.section-role-appearance.v1.version` | required | const: 1.0.0 | — |
| `extensions.org.ostf.section-role-appearance.v1.data` | required | object | additionalProperties=allowed |
| `extensions.org.ostf.section-role-appearance.v1.data.roleDefinitions` | optional | array | — |
| `extensions.org.ostf.section-role-appearance.v1.data.roleDefinitions[]` | optional | object | additionalProperties=allowed |
| `extensions.org.ostf.section-role-appearance.v1.data.roleDefinitions[].id` | required | string | minLength=1 |
| `extensions.org.ostf.section-role-appearance.v1.data.roleDefinitions[].name` | required | string | minLength=1 |
| `extensions.org.ostf.section-role-appearance.v1.data.roleDefinitions[].baseRole` | optional | string | — |
| `extensions.org.ostf.section-role-appearance.v1.data.sectionRoleAssignments` | optional | object | additionalProperties=allowed |
| `extensions.org.ostf.section-role-appearance.v1.data.appearance` | optional | object | additionalProperties=allowed |
| `extensions.org.ostf.section-role-appearance.v1.data.appearance.roleColors` | optional | object | additionalProperties=allowed |
| `extensions.org.ostf.section-role-appearance.v1.data.appearance.customRoleColors` | optional | object | additionalProperties=allowed |
| `extensions.org.ostf.section-role-appearance.v1.data.appearance.objectColors` | optional | array | — |
| `extensions.org.ostf.section-role-appearance.v1.data.appearance.objectColors[]` | optional | object | additionalProperties=allowed |
| `extensions.org.ostf.section-role-appearance.v1.data.appearance.objectColors[].targetType` | required | enum: section, chordClip, melodyClip | — |
| `extensions.org.ostf.section-role-appearance.v1.data.appearance.objectColors[].targetId` | required | string | minLength=1 |
| `extensions.org.ostf.section-role-appearance.v1.data.appearance.objectColors[].color` | required | string | pattern=^#[0-9A-Fa-f]{6}$ |

## Additional semantic validation

The schema alone is insufficient: the included CLI runs strict-wire loading, JSON Schema, and semantic reference/time validation. The section `role` value, `roleColors` keys, and opaque music fields do **not** gain new semantics by appearing in an example.

## Definitions not standardized here

Chord names, note pitches, velocities, lyric phonemes, lyric-to-note assignments and any manufacturer/DAW-specific extension fields are not given normative types by the shipped 2.3 profile. Examples may carry opaque illustrative fields, and preservation is required by writers claiming lossless round trips.
