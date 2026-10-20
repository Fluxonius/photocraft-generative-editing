# Validation report

Date: 2026-10-20. Scope: the shipped skill package and offline helper, with a synthetic native-engine probe. No new image-generation request, external paid API, global skill installation, publication, or mutation of a user's live photograph was performed for this validation.

## Results

- Skill Creator `quick_validate.py`: valid frontmatter/name/description and completed entry point.
- Relative Markdown references and OpenAI UI metadata: checked; all referenced package files exist.
- **16 functional helper tests passed.** Coverage includes offset crop mapping, mismatched aspect ratios, asymmetric expansion, invalid margins, irregular permission-mask leakage inside its bounding box, nonzero feather support, hidden RGB with zero alpha, ICC mismatch, unsupported16-bit/JPEG input, dimension/channel mismatch, source fingerprint mismatch, crop sample/profile preservation and refusal to overwrite or exceed bounds.
- Two independent reviews reproduced false passes for PNG color-key transparency and TIFF transfer-function metadata. Regression tests were run failing first. The shared loader now refuses those unsupported inputs before audit/crop. The reviewers reran the original TIFF and RGB/L transparency reproductions and confirmed explicit rejection (exit2), rather than a false preservation claim.
- **1 optional native-engine integration test passed** against installed PhotoCraft CLI0.10.0 (`8407d9ccb`). It opens a temporary128x96 synthetic RGBA image, places a32x24 patch, creates a selection-based layer mask, saves a lossless composite and `.pcraft`, and reopens the project with two layers and a mask intact. Local audit finds768 permitted changed pixels and zero protected changes. It also extends a fresh original to144x104, saves/reopens the native project, and verifies the original rectangle at offset(8,4) with zero protected changes. Including this test, **17 tests passed, no skips** in the verified run.

The native test uses a genuine partial-alpha source pixel. An initial opaque RGB fixture correctly triggered a mode-mismatch rejection when transparent canvas extension caused an RGBA output. No automatic RGB/RGBA normalization was added: comparison representation must be established explicitly. This is a limitation to handle, not a reason to suppress the audit.

## Independent instruction scenarios

| Scenario | Observed evaluation decision |
|---|---|
| Warm, grainy portrait; smooth cool generated glasses; shifted nose | Use native crop mapping0.8 with origin1900,950; detect landmark drift; preserve original skin/hair; use object-only mask or regenerate; correct patch-local tone, tungsten reflections, optics and grain. |
|6000x4000 to horizontal16:9 at fixed height | Disclose integer rounding;7111x4000 with555/556 margins; original rectangle[555,0,6555,4000); discard regenerated center; no feather into protected pixels without changed authorization. |
| Failed live selection/import, oversized preview, timed-out transform | Stop dependent edits; discover live tab route; use scoped open+copyToDocument; file-backed review; inspect history/bounds/jobs before replay. |
|16-bit original and8-bit generated patch | Preserve native source depth; do not downgrade the original; helper cannot prove native-depth preservation; use a verified native-depth workflow and disclose the limit. |

These scenarios evaluate agent decisions from the packaged instructions. They are not new live GUI runs or real provider generations.

## Reproduce

From the project root, with Python3.10+ and Pillow available:

```sh
python3 -m unittest discover -s tests -v
PHOTOCRAFT_CLI="/absolute/path/to/photocraft-cli" python3 -m unittest discover -s tests -v
```

Without `PHOTOCRAFT_CLI`, the native integration case is skipped and16 helper cases run. On Windows the optional native test's pipe readiness mechanism (`select` on a process pipe) is not portable; run offline helper tests there and use the host's documented process/RPC harness for native acceptance. The runtime skill and helper do not depend on this POSIX test harness.

## Limits

- Visual match of tone, retouch, lighting and grain remains an agent/user judgment. A numerical preservation test cannot establish natural-looking integration.
- No new real-model generative-expand end-to-end run was performed. The native expansion check adds canvas; it does not synthesize border content.
- Other agents, image providers, Windows/Linux GUI behavior, later PhotoCraft versions, color-managed16/32-bit pipelines and native Photoshop PSD fidelity were not validated by these tests.
- The helper is deliberately restricted to comparable8-bit L/LA/RGB/RGBA lossless PNG/TIFF exports up to64M pixels and refuses unsupported metadata/modes. Full scope is stated in the runtime pixel-audit reference.
- Native projects were reopened and structurally inspected. Both reopened projects were exported again and their decoded channel samples matched their corresponding pre-reopen exports exactly in these synthetic cases. This is a tested round trip for these fixtures, not a general file-fidelity certification.

## MCP transport requirement — v0.1.1

A baseline instruction review found that “existing automation connection” did not explicitly exclude standalone CLI or desktop fallback when MCP was unavailable. The entry point and bridge reference now require MCP for PhotoCraft operations and live MCP for visible documents. Independent scenario review confirmed: missing MCP pauses editing; headless MCP cannot replace the intended live document; a CLI serving MCP is allowed through host MCP tools; external generation and offline crop/audit helpers remain allowed. These are instruction evaluations, not new live connection tests.

After this documentation update, skill validation and `git diff --check` passed. The helper suite passed 16 tests; the optional native engine test was skipped in this run. The earlier recorded 17-test engine run remains unchanged.
