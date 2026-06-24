# Preliminary static proxy (computed from existing artifacts, no repo run)

A cheap static check while the dynamic coverage run (above) is pending. Using
each repo's `repo_index.json` (per-file import lists) and the dataset's
`common_files_changed`, we asked: **does any test file even _import_ a module the
LLM modified?** If not, the existing suite cannot exercise (let alone validate)
the edit.

## Result

Scope: the **8** repositories where the LLM edited a *pre-existing* file (and a
`repo_index.json` exists). New-file-only extractions are excluded because
pre-existing tests cannot cover code that did not yet exist.

| Outcome | repos |
|---|---|
| With ≥1 test file in the index | 7 / 8 |
| …where a test imports a modified module | **1** (whoogle-search) |
| …with tests but **no test reaches the edited module** | **6** |
| No test file at all | 1 |

So in 6 of the 7 repos that had tests *and* edited an existing file, the suite
does not even reference the edited module — consistent with the test-adequacy
gap argued in §5.2.

## Caveats (why this is a proxy, not the result to cite)

- **Static, not dynamic:** import-level reachability misses integration tests
  that exercise code indirectly (via the app/CLI), conftest fixtures, and
  dynamic imports; it can therefore *under*-count true coverage.
- **Approximate matching:** modules are matched by file stem against import
  strings — possible false negatives on aliased/renamed imports.
- **Small N (8):** only counts edits to pre-existing files; most improvements
  came from *new* files, which pre-existing tests inherently cannot cover.

Treat as directional support. Cite `measure_edit_coverage.py` output, not this.
