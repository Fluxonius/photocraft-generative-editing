# Remove the object and its visible effects

Use for object removal and replacement. A successful removal shows the scene as if the target were absent. The object silhouette is only part of the repair area. A correct generated crop can still produce an incomplete final edit if compositing reveals only that silhouette.

## Define the repair area before generation

Inspect the source at viewing size and native scale. Identify the target's silhouette, thin parts and gaps, contact/occlusion darkening, cast shadow through its soft penumbra, reflections, colored light spill and edge fringes where attributable to the target. Effects may extend far beyond the object or form disconnected regions. A fixed expansion of a segmentation mask does not establish their coverage.

A normal request to remove an object includes removing its clearly attributable visible effects. State that scope and proceed without asking for each shadow. Preserve unrelated subjects, their shadows/reflections and scene lighting. If attribution is consequentially ambiguous, or the user supplied a strict selection that excludes needed repair, resolve that boundary before changing it; do not silently broaden a protected area.

Declare an allowed repair envelope covering these regions and the needed transition support. It can contain disconnected components. Choose a larger context crop showing the effects and enough clean surface to infer perspective, texture, lighting and structural lines. If more repair is discovered later, revise the scope explicitly before further edits, not retrospectively to pass the pixel audit.

## Generate the restored scene

Request removal of both the target and its attributable effects, reconstructing the underlying surfaces and continuing texture, joints, lines and lighting. Keep unrelated subjects and effects. For replacement, first remove obsolete effects of the old object, then integrate physically plausible effects of the new one; the old shadow is not automatically valid for a new shape.

Example:

> Remove this chair, including its legs, contact darkening, long shadow on the right and separate reflection in the polished floor. Reconstruct the floor's perspective, seams, texture, light and grain. Preserve the person's overlapping shadow and all other subjects. Keep framing and fixed landmarks unchanged.

Where shadows overlap, recover the surface with the retained subject's shadow still present. Masking alone cannot separate two effects occupying the same pixels. Regenerate or reconstruct that overlap if the result erased the retained effect; do not reveal an unchanged source region that brings the chair's shadow back.

## Composite the complete repair

Align the generated crop first. Build the editable compositing mask from the repair area, not solely the removed object's segmentation or alpha. Reveal restored surface over every target-related region, with sufficient opacity to replace the old object/effect. Separate masks/layers are useful for disconnected repairs. Keep context-only pixels hidden.

Place transitions in compatible clean background outside the old fringe/penumbra and inside the allowed envelope. Low mask density or feathering across a remaining shadow core can ghost it back. Use optical softness appropriate to the surrounding surface; a broad blur cannot fix incomplete coverage.

## Verify semantic completeness

Compare three views: the original, the aligned generated crop, and the final visible composite. Toggle the repair group and inspect all identified regions, including distant reflections and overlapping shadows. Check for residual legs, dark silhouettes, floating shadows, reflection fragments, halos, repeated texture and broken floor lines. If an artifact is absent in generation but present in the composite, inspect mask support/opacity, placement and layer order before generating again. If it exists in generation, repair or regenerate that area.

Check the whole image and 100–200% details, then audit protected pixels and save through MCP. A pixel audit proves preservation outside the allowed area; it cannot prove that removal is complete. An unchanged old shadow may pass that audit and still fail this task.
