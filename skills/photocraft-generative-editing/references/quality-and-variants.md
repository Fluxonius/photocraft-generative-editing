# Quality gates and optional variants

This is an agent workflow using external generation and ordinary editable PhotoCraft layers through MCP. Do not claim a native Photoshop-style variations panel, automatic quality certification, or guaranteed photorealism. More samples do not ensure a better fill.

## Choose the batch and keep a common baseline

For a normal edit, start with one candidate and inspect all outputs the provider actually returns. When the user requests options or exploration, target three candidates unless they specify another count. State this default and honor available generation access, time/cost limits and existing authorization. Do not make paid calls or switch providers without the required authorization. If the provider returns one image per call, count each call toward the batch; do not invent a batch/seed parameter or claim three variants from one image. With insufficient access/budget, deliver the available count and explain the limit.

Track the batch's generator calls used, remaining retry allowance, and any authorized cost/time limit in the review notes. Give variants stable IDs (A, B, C). Keep the same frozen source revision, requested edit, repair envelope, crop and intended output geometry, so variation concerns the generated solution rather than an altered original. Store the actual prompt/reference roles, artifact path, returned dimensions, mapping and review notes per candidate. New scope or geometry starts a clearly identified batch. A preferred candidate can guide “more like B” only if the actual provider supports reference editing; retain the original crop as the preservation/landmark reference. This does not imply an available Generate Similar command.

## Gate 1 — inspect each generated candidate

Inspect the saved output, not just a thumbnail or tool success message. Record short observations; use pass / needs repair / reject rather than invented confidence percentages.

| Check | Required evidence |
|---|---|
| Artifact and mapping | Readable actual file, dimensions/mode/profile known, enough local pixels, framing and stable landmarks checked; no unresolved crop/scale drift. |
| Task completeness | Requested content exists; removal eliminates attributable shadows/reflections/fringes; outpaint fills all intended margins without duplicated subjects. |
| Geometry and structure | Perspective, floor joints, horizon, object anatomy and text where relevant remain plausible; protected structures can be retained with the intended mask. |
| Appearance | Lighting, tone, material, focus, grain and retouch fit nearby comparable surfaces; no repeated texture, halos, accidental new objects or broken lines. |

Reject a candidate whose required repair region contains unresolved structural errors, missing task content or unusable resolution. Drift entirely outside the intended support may be masked out; do not warp the original to fit it. Treat an otherwise sound patch with correctable local tone/grain as needing repair, not already accepted. A good-looking crop cannot establish final preservation.

## Gate 2 — test actual PhotoCraft composites

For each shortlisted option, align it and create its own editable masked layer/group using MCP. Use the same baseline and repair scope, with candidate-specific masks and local corrections where needed. Display only one alternative at a time over the baseline; stacking alternatives creates an invalid comparison. Restore the previous accepted state between trials and inspect actual visibility/bounds/mask targets.

Compare original, aligned generation and final composite at full-frame viewing size and native-scale 100–200% close-ups. Apply [blend-quality.md](blend-quality.md) and task-specific removal/expand checks. Check mask support/opacity, occlusion, shadow/reflection completeness, border/corner continuity, local color/focus/grain and protected identity. If generation is correct but the composite is wrong, fix placement, masks, visibility or local adjustment targets first. Regenerate for defects that remain in the required generated content.

Export the shortlisted composite and audit protected pixels using a supported comparable path. A hard failure (wrong subject/geometry, incomplete removal, seam, leaked protected pixels) cannot be offset by a nicer style or a numerical average. An unsupported audit is “not verified”, never “passed”; disclose the limit. Keep a provisional preview separate from an accepted result when a required check is unresolved. Re-run affected checks after any correction; after a user switches variants, verify that exact visible state before final export/save.

## Present and preserve a choice

For requested alternatives, show labeled A/B/C previews of actual composites with identical framing, display scale and color treatment, plus matching close-ups where useful. Full-frame previews may be downscaled for display; preserve native source/patches and label preview dimensions. Do not present an attractive raw generation as proof its final composite works. If a preview sheet cannot be made with available authorized tools, show separate labeled previews.

Provide a small comparison with ID, observed geometry/coverage/blending issues, preservation check status, and recommendation/reason. Only technically acceptable options form the selection set; label failed or provisional options explicitly. Recommend the strongest passing option on task fidelity and integration, then subjective appearance. If the user asked to choose, leave that choice pending; do not call the recommendation user-approved. If they delegated selection, choose and report the reason. If none pass, say so rather than choosing the least bad as final; restore the baseline/last accepted visible state and hide failed candidates.

Retain requested usable alternatives as named editable layers/groups (for example `Removal A`, `Removal B`) with their own masks/corrections; hide all unselected alternatives, leave only the chosen/recommended candidate visible when one exists, and identify whether selection is pending. Keep original and candidate artifacts without destructive merging. Where grouping is unsupported, use separate editable project copies and explain how to switch. Save a working project for pending selection, and make the final export only from the confirmed/delegated visible variant. Combining useful parts is allowed only when geometry/lighting agree; keep masks editable and run the gates on the combined result as a new candidate.

## Bound the repair loop

Diagnose and state a concrete failure before retrying: context/coverage, prompt/structure, placement/mask, or local appearance. Fix a compositing error without another generation. For a generation defect, change the relevant prompt/context/reference rather than repeat blindly. Preserve the best accepted result and return to the frozen baseline to avoid cumulative drift.

If the user supplied no iteration limit, allow at most two additional generator calls after the initial batch within already authorized access/budget, and stop earlier if the same defect recurs without improvement. A user-specified tighter limit wins. At the limit, stop generation, retain the checkpoint and report the unresolved defect plus a targeted next step; obtain a new budget before more calls. More variants requested later form a new authorized batch. Do not spend the retry allowance merely to fill a cosmetic three-option quota, or keep generating after a satisfactory single-result task has passed.
