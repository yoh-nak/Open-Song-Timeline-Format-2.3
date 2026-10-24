"""Standalone v1 candidate validator: structural schema + referential constraints."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator
NEW="org.ostf.section-role-appearance.v1"; OLD="org.ostf.section-role-appearance.draft23"
SCHEMA=json.loads((Path(__file__).parent/'schema/ostf-2.3-standalone-candidate.schema.json').read_text(encoding='utf8'))
Draft202012Validator.check_schema(SCHEMA)
def check(document):
    errors=[str(e.message) for e in Draft202012Validator(SCHEMA).iter_errors(document)]
    if errors:return errors
    ext=document['extensions']
    if OLD in ext:errors.append('legacy draft23 extension forbidden in standalone v1')
    if NEW not in ext:errors.append('stable extension namespace required')
    if errors:return errors
    payload=ext[NEW]['data']
    sections=document['timeline']['sections']
    ids=[s['id'] for s in sections]
    if len(ids)!=len(set(ids)):errors.append('duplicate section ID')
    if any(sections[i]['start']+sections[i]['duration']>sections[i+1]['start'] for i in range(len(sections)-1)):errors.append('unsorted or overlapping sections')
    roles=payload.get('roleDefinitions',[])
    roleids=[r['id'] for r in roles]
    if len(roleids)!=len(set(roleids)):errors.append('duplicate custom role ID')
    assignments=payload.get('sectionRoleAssignments',{})
    for sid,rid in assignments.items():
        if sid not in ids:errors.append('unknown section role assignment '+sid)
        if rid not in roleids:errors.append('unknown assigned custom role '+str(rid))
    appearance=payload.get('appearance',{})
    for rid in appearance.get('customRoleColors',{}):
        if rid not in roleids:errors.append('unknown custom role color reference '+rid)
    # Draft 101 explicit identity paths: harmony.chords[].id and melodies[].clips[].id.
    # IDs become mandatory only for entries that are used as color targets.
    chord_ids=[c['id'] for c in document['harmony'].get('chords',[]) if isinstance(c,dict) and isinstance(c.get('id'),str) and c['id']]
    melody_ids=[c['id'] for track in document['melodies'] if isinstance(track,dict)
                for c in track.get('clips',[]) if isinstance(c,dict) and isinstance(c.get('id'),str) and c['id']]
    for typename,targets in (('chordClip',chord_ids),('melodyClip',melody_ids)):
        if len(targets)!=len(set(targets)):
            errors.append('duplicate '+typename+' ID')
    valid_clip_ids={'chordClip':set(chord_ids),'melodyClip':set(melody_ids)}
    seen=set()
    for item in appearance.get('objectColors',[]):
        target_type=item['targetType']; target_id=item['targetId']
        key=(target_type,target_id)
        if key in seen:errors.append('duplicate object color target '+target_type+':'+target_id)
        seen.add(key)
        if target_type=='section' and target_id not in ids:
            errors.append('unknown section color reference '+target_id)
        elif target_type in valid_clip_ids and target_id not in valid_clip_ids[target_type]:
            errors.append('unknown '+target_type+' color reference '+target_id)
    # Draft 105: lexical identity is scoped to each lyric collection. No
    # unverified alignment or timing semantics are assumed for these records.
    for collection in ('documents','phrases','units','alignments'):
        records=document.get('lyrics',{}).get(collection,[])
        lyric_ids=[item['id'] for item in records if 'id' in item]
        if len(lyric_ids)!=len(set(lyric_ids)):
            errors.append('duplicate lyrics.'+collection+' ID')
    from event_timing103 import temporal_errors
    errors.extend(temporal_errors(document))
    return errors
