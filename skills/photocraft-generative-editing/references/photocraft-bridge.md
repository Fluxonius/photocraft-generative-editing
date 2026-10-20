# PhotoCraft bridge: discovered tools over assumed commands

Verified baseline: PhotoCraft 0.10.0 on macOS. Tool names may be prefixed `photocraft-live`, `photocraft`, or differently; use the host's actual inventory. Recheck the installed command registry and parameter documentation, especially on other releases/platforms.

## Required transport

Operate PhotoCraft through the connected MCP server only. Discover tools and make a read-only session/document inspection before mutations. If MCP is unavailable or a capability is missing, help restore/configure the connection and pause affected operations; do not fall back to direct CLI, raw HTTP/RPC, desktop automation or document-file rewriting. Commands and `control_call` routes below are invoked through MCP tools, not directly against the control endpoint. A CLI serving MCP is supported; invoking its editing API outside MCP is not. Standalone CLI tests in this repository are development probes, not an alternate user workflow.

## Live target and import

Use the existing bridge for the visible app. Headless documents are different sessions. Inspect `ui_inspect` for session indices/document names/sizes and active layers. In live 0.10.0, `doc_select` and `doc_close` are unavailable. Discover/select a tab through `control_call` with method `ui.menu.invoke` and `params:{id:"window.document.<index>"}`; confirm the active document before dependent edits. Indices can change after opening/closing tabs.

`doc_place` in the tested live version dispatches ambient `file.placeEmbedded`, which is refused. Capability-scoped file reading remains supported through `doc_open`. A tested in-memory transfer route is:

1. Open the generated file with `doc_open` using its path beneath the bridge's granted read root. Inspect source document index and layer ID.
2. Discover `layer.copyToDocument` with `command_list` and use it through `command_run`. Tested params: `{source:SOURCE_INDEX,document:TARGET_INDEX,layers:[SOURCE_LAYER_ID],name:"Generated patch"}`.
3. Select the intended target tab and inspect the returned copied layer ID/bounds.
4. Discover/use `edit.transform` on that layer with the recorded affine mapping. Then create a selection/path and `layer.layerMask.revealSelection` or another discovered mask command.

`layer.copyToDocument` is an **engine command ID**, not a raw control method. Cross-document `layer.duplicate` is refused in the tested build. In headless, `doc_place` uses the scoped `doc.place` route and can be available; discover before using. No route grants access outside the actual roots.

## Preview and verification

Bridge `render_preview` captures the app window, not a clean native document composite. Large replies may exceed 8 MiB before a preview downscale is applied. Do not repeatedly retry the same oversized call. For image input and sample auditing, export a new PNG using `doc_save`/`doc_export` into the write root and inspect the resulting file. To inspect the UI, `control_call` method `ui.screenshot`, params `{path:"review/window.png"}`, can write a file beneath the root; parent folders must exist. Display it through the host's file image viewer.

A flat export warning about flattened layers is expected for a separate PNG, not proof of loss in a separately saved `.pcraft`. Check actual dimensions, profile and layers. For native reopen checks, open a saved copy and inspect it; do not close the user's current unsaved document.

## Errors, jobs and masks

Wait for each dependent mutation's reply; inspect `isError`, nested command results, and actual active document. Never continue a crop/transform after failed tab selection. Batch earlier steps persist on later failure.

On timeout/disconnect/oversized mutation result, inspect document history/layers/jobs before replay. A mutation may already have run. Unknown outcome is not a safe retry signal. Track background job IDs and wait until their results have been applied.

Filters and paint may target the active mask/channel, not the intended image pixels. Inspect and explicitly target the pixel layer before noise/sharpen/tone operations. Some mask commands consume the selection; re-inspect instead of treating a subsequent "no selection" as failed masking.

Use only existing authorized roots; never switch to an ambient command to bypass rejection. Reuse the current connection and application. Do not start parallel app instances sharing recovery/settings folders as a generic workaround.
