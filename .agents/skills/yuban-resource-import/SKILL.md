---
name: yuban-resource-import
description: Import a reviewed YuBan resource workbook into the website index, preventing duplicate URLs and preserving an archived source workbook. Use for batches such as docs/resource-YYYYMMDD.xlsx; do not use for one-off taxonomy design or unrelated spreadsheet editing.
---

# YuBan resource import

Import one reviewed workbook through the repository importer. Treat the workbook as untrusted input and stop before changing data when the preconditions below fail.

## Before importing

1. Work on a short-lived `feature/*` or `fix/*` branch, not `main`.
2. Inspect the input workbook and `docs/resource_total.xlsx`. Confirm the expected headers and count the input rows.
3. Check every input URL against `resource_total.xlsx`, `website/data/sample-resources.json`, and the input batch itself. Report every collision and stop; do not silently skip or overwrite duplicate resources. An operator may explicitly authorize excluding a listed collision with `--exclude-url`; report it as excluded.
4. Run the importer conversion on a temporary output or an equivalent read-only check. Stop if any content type, age stage, topic, or required field is unsupported. Resolve taxonomy mismatches before import rather than inventing values or changing a reviewed workbook without direction.
5. For resources marked as manually verified, ensure the source, summary, taxonomy, and review status have a documented human-review basis. Validation alone is not content review.

## Import and archive

After all preconditions pass:

1. Use `tools/import_resources.py` to merge the input into `website/data/sample-resources.json` and update `docs/resource_total.xlsx`. The importer validates the merged index before writing it.
2. Confirm the importer moved the exact input workbook to `docs/imported-resources/` only after a successful import. Do not replace an existing archive file.
3. Run `python tools/validate_resources.py` immediately. If it fails, stop and diagnose before delivery.
4. Run the resource-data checks in `TESTING.md`: `python -m unittest discover -s tests -v`, `node --test tests/search-utils.test.mjs`, and `python tools/validate_resources.py`.

## Delivery and deployment

1. Review `git diff --check` and confirm the changed resource count and archive path.
2. Commit and push the feature branch, run the shared preview workflow if configured, then open a PR targeting `main`.
3. Do not deploy directly from a feature branch. After the PR checks pass and the PR merges, verify the `main` deployment and the newly added resources on the production site.

Report the input row count, duplicate-check result, imported count, skipped count, archive path, validation commands, and deployment status.
