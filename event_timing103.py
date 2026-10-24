"""Provisional OSTF 2.3 standalone temporal semantic validation.
Does not claim to fully validate lyric/note/music syntax."""

def temporal_errors(document):
    errors=[]
    timeline=document.get('timeline',{})
    sections=timeline.get('sections',[])
    end=max((s['start']+s['duration'] for s in sections), default=0)
    for name in ('meterChanges','tempoChanges'):
        changes=timeline.get(name,[])
        points=[x['at'] for x in changes]
        if not points or points[0]!=0:
            errors.append(name+' must begin at tick zero')
        if any(b<=a for a,b in zip(points,points[1:])):
            errors.append(name+' must have strictly ascending unique at positions')
        if any(at>=end for at in points):
            errors.append(name+' event must fall before section timeline end')
    # Only well-understood clip timing fields are checked. Unknown musical
    # payloads remain outside the claimed semantics.
    clips=[('harmony.chords['+str(i)+']',c) for i,c in enumerate(document.get('harmony',{}).get('chords',[]))]
    for ti,track in enumerate(document.get('melodies',[])):
        for ci,clip in enumerate(track.get('clips',[])):
            clips.append(('melodies['+str(ti)+'].clips['+str(ci)+']',clip))
    for path,clip in clips:
        has_start='start' in clip
        has_duration='duration' in clip
        if has_start!=has_duration:
            errors.append(path+' needs both start and duration when timed')
        elif has_start:
            a,b=clip['start'],clip['duration']
            if type(a) is not int or a<0 or type(b) is not int or b<=0:
                errors.append(path+' requires nonnegative integer start and positive integer duration')
            elif a+b>end:
                errors.append(path+' ends beyond section timeline')
    return errors
