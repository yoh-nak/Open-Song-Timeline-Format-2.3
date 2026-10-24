# Open Song Timeline Format — OSTF 2.3.0

GitHub-ready standalone OSTF 2.3.0 release package. All example songs are `.ostf` files. No compatibility testing with external OSTF devices is required or claimed.

**Start here:** [Full manual](docs/COMPLETE_MANUAL.md) · [Full parameter reference](docs/PARAMETER_REFERENCE.md) · [Format specification](docs/FORMAT_SPECIFICATION.md) · [Sample index](samples/INDEX.md) · [Release notes](docs/RELEASE_NOTES.md).

## Validate

```sh
python -m pip install -r requirements.txt
python ostf23_validate.py samples/*.ostf
python tools/verify_release.py
```

**Note:** This release defines bounded conformance, not a fully normative MIDI/chord/lyric event vocabulary. All additional music fields are opaque and must be preserved by transformations claiming lossless support.

**License:** Apply a license chosen by the repository owner prior to public release. This package does not impose an unrequested license.
