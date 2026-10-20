---
name: photocraft-generative-editing
description: Use when adding, replacing or removing image content with AI in PhotoCraft, refining a generated local patch, or extending a canvas with generative fill, inpainting or outpainting while preserving original detail and editable layers.
---
# PhotoCraft generative editing

Combine an available image generator with PhotoCraft through MCP. Preserve the user's target document, requested live workflow and protected original pixels. This skill supplies a workflow, not a generator, MCP server or Photoshop feature implementation.

## Require PhotoCraft MCP

Use a connected PhotoCraft MCP server for all PhotoCraft inspection, document edits, layer/mask operations, and saves/exports. First discover its tools and verify the intended session/document with a read-only inspection. Server names vary; use the actual inventory. For a document open in the visible app, require the live MCP bridge; headless MCP documents are separate sessions.

If MCP is absent, disconnected, or lacks a required capability, pause the affected PhotoCraft operation, explain the missing prerequisite and help configure or reconnect MCP within the user's authorization. Verify the connection before resuming. Do not substitute direct CLI, raw HTTP/RPC, desktop clicks or file rewriting to control PhotoCraft outside MCP, even if faster or already authorized. A CLI launched as an MCP server is a valid transport when invoked through the host's MCP tools. External image generation and offline crop/pixel-audit helpers remain separate tools; they do not replace MCP for PhotoCraft operations.

## Establish the edit contract

Inspect the document, dimensions, mode/depth/profile, layer and mask targets, selection, history and jobs. Identify the subject and requested change. Record the baseline and distinguish **allowed edit region**, **generator context crop**, and **actual compositing mask**. Include agreed feather/shadow support in the allowed region before generating. Resolve consequential ambiguity; otherwise state sensible choices and proceed under existing authorization.

Work from a checkpoint or duplicate, keeping original layers. Export a native-resolution lossless baseline. Never substitute a lower-resolution full-frame generation for the original. Treat missing provider access or a missing supported bridge capability as a concrete prerequisite; do not install, expose credentials, change providers or spend on an external API silently.

## Choose the route

- Live PhotoCraft or transport errors: read [photocraft-bridge.md](references/photocraft-bridge.md).
- Fill, remove, insert, or refine local details: read [local-fill.md](references/local-fill.md). For removal/replacement, also read [object-removal.md](references/object-removal.md): remove the object and its attributable shadows/reflections, and composite the complete restored area rather than only its silhouette.
- Expand a canvas: read [expand.md](references/expand.md).
- Before generation: read the relevant provider section in [generators.md](references/generators.md) and [quality-and-variants.md](references/quality-and-variants.md) for candidate screening, optional alternatives and bounded iteration.
- Before accepting any generated edit: read [blend-quality.md](references/blend-quality.md).

## Preserve geometry and editability

Use document pixels. For crop `(x0,y0,Wc,Hc)` and generated `(Wg,Hg)`, map `x=x0+xg*Wc/Wg`, `y=y0+yg*Hc/Hg` only after verifying unchanged framing and alignment. Transform only the patch. Different aspect ratios require resolving reframing/padding, not blind stretching. A small object's detail budget is its pixels in the generated crop; whole-frame output dimensions are misleading.

Keep generated content on named layers with reversible masks; separate cast shadows or transparent effects when needed. Preserve original hair, skin, texture and foreground occluders outside the intended insert. Match color, lighting, sharpness, grain and retouch locally rather than altering the entire photograph to fit the patch.

## Accept and save

1. Apply the candidate and final-composite gates in [quality-and-variants.md](references/quality-and-variants.md). Inspect a full view and native-scale close-up; resolve failures before calling a result accepted. Preserve requested alternatives for selection.
2. Audit the **visible composite**, not only the untouched original layer: local edits preserve decoded samples outside the allowed mask; expansion preserves the original rectangle at its translated offset. See [pixel-audit.md](references/pixel-audit.md) for an optional offline helper and its limits.
3. Save a new `.pcraft`, read warnings and confirm layers/masks. When user selection is pending, save a working project with alternatives; export the requested final format only from the selected/delegated variant. Reopen a saved copy when claiming round-trip verification.
4. Report actual dimensions, localized scope, visual/pixel checks, saved files and material limitations. Do not claim optical equivalence, restored real detail, supported bit depth or tested provider compatibility without evidence.

Source attribution and version boundaries: [sources.md](references/sources.md).
