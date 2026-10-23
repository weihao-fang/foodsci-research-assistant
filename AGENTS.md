# Maintainer guidance

- `skills/foodsci-research-assistant/` is the complete, self-contained source.
- The five sibling skills are small task entrypoints; keep shared rules in the main skill.
- Edit relevant references for methods or writing. Do not copy the full resource tree into each entrypoint.
- Keep supported statements tied to actual sources and execution. Preserve uncertainty, negative results and experimental units.
- Update VERSION and skill metadata together; record changed behavior and compatibility in CHANGELOG.md.
- Run `python -B -m unittest discover -s skills/foodsci-research-assistant/tests -v`, `python -B tools/validate.py`, and `python -B tools/build.py` before distributing.
- Downloads are generated. Do not hand-edit a ZIP or claim a client installation that was not tested.
- Keep personal paths, credentials, account receipts and unpublished research out of this repository.
