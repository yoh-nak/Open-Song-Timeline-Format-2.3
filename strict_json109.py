"""Strict OSTF wire JSON ingestion: UTF-8, unique keys, finite JSON numeric constants."""
import json
import math
from decimal import Decimal, InvalidOperation
from pathlib import Path
from standalone_conformance99 import check

class WireJSONError(ValueError):
    pass

def _unique_pairs(pairs):
    obj={}
    for key, value in pairs:
        if key in obj:
            raise WireJSONError('duplicate JSON object key: '+repr(key))
        obj[key]=value
    return obj

def _bad_constant(const):
    raise WireJSONError('nonstandard numeric constant: '+const)

def _finite_float(raw):
    try:
        value=float(raw)
    except (OverflowError, ValueError) as exc:
        raise WireJSONError('invalid JSON floating-point number') from exc
    if not math.isfinite(value):
        raise WireJSONError('non-finite numeric result (overflow): '+raw[:80])
    # Nonzero finite JSON numbers must not silently become zero after binary64 conversion.
    if value == 0.0:
        try:
            if Decimal(raw) != 0:
                raise WireJSONError('nonzero JSON number underflowed to zero: '+raw[:80])
        except InvalidOperation as exc:
            raise WireJSONError('invalid JSON floating-point number') from exc
    return value

def _valid_unicode_tree(value):
    # UTF-8 can encode valid Unicode scalars only. JSON escape sequences
    # that resolve to lone UTF-16 surrogates are forbidden too.
    if isinstance(value, str):
        if any(0xD800 <= ord(ch) <= 0xDFFF for ch in value):
            raise WireJSONError('unpaired Unicode surrogate is not permitted')
    elif isinstance(value, list):
        for item in value: _valid_unicode_tree(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            _valid_unicode_tree(key)
            _valid_unicode_tree(item)

def loads_wire(raw):
    if isinstance(raw,bytes):
        try:
            raw=raw.decode('utf-8',errors='strict')
        except UnicodeDecodeError as exc:
            raise WireJSONError('input is not UTF-8') from exc
    if not isinstance(raw,str):
        raise TypeError('expected str or UTF-8 bytes')
    if raw.startswith('\ufeff'):
        raise WireJSONError('UTF-8 BOM is not permitted in candidate profile')
    try:
        result=json.loads(raw,object_pairs_hook=_unique_pairs,
                          parse_constant=_bad_constant,parse_float=_finite_float)
        _valid_unicode_tree(result)
        return result
    except json.JSONDecodeError as exc:
        raise WireJSONError('invalid JSON: '+exc.msg) from exc

def check_wire(raw):
    try:
        doc=loads_wire(raw)
    except (WireJSONError,TypeError) as exc:
        return [str(exc)]
    return check(doc)

def check_file(path):
    return check_wire(Path(path).read_bytes())
