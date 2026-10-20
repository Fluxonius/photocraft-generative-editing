# Make a generated edit belong to the photograph

Use this review after every generated insertion, removal or replacement and again after corrections. A geometric fit and a zero-difference audit do not establish visual quality. Compare comparable materials at similar depth and illumination, not the mean brightness of the entire crop. A naturally black object should remain black against bright skin.

| Check | Evidence of mismatch | Local remedy |
|---|---|---|
| Color management | Profile mismatch, unexpected saturation or monochrome tint | Establish actual profiles and transform only the patch into the document working space using supported color management; do not merely relabel unknown RGB samples. Preserve the original profile/depth. |
| White balance and hue | New object looks warmer/cooler or neutral gray has a color cast | Adjust patch temperature/tint or channel balance relative to nearby neutral material. A monochrome frame stays neutral unless the photo itself is toned. |
| Tonal response | Lifted blacks, crushed lens shadows, overly brilliant highlights | Use patch-local curves/levels/exposure; preserve plausible material contrast and source highlight rolloff. |
| Light direction and softness | Bright edge faces away from lamps; contact point floats | Regenerate structural lighting errors. Add small, independently adjustable contact/cast shadows only where physically justified. |
| Reflections and transparency | Lenses behave like opaque stickers or reflect unrelated windows | Preserve believable scene reflections and lens transmission; use separate mask/tone treatment for lens and frame when needed. |
| Focus and edge softness | Insert is razor sharp in a soft plane, or blurrier than adjacent details | Compare same-depth edges at native scale. Resample patch once when possible; apply modest patch-only optical blur or sharpening. Sharpening cannot reconstruct missing detail. |
| Noise/grain and compression | Smooth plastic patch on grainy skin, colored speckles in B&W | Match luminance grain strength, size and character after final scaling. Avoid adding noise to the entire original or matching JPEG artifacts by damaging the baseline. |
| Retouch level | Pores disappear, hair becomes painted, facial features become beautified | Mask out regenerated skin/hair. Prefer the original face beneath an object-only mask; regenerate if geometry cannot align. |
| Occlusion and depth | Temple sits on top of hair, object crosses a foreground hand | Restore original foreground through masks or an original-pixel occlusion layer. Preserve fine strands; do not erase original features. |
| Seam/halo | Bright fringe, cutout edge, doubled hair or texture discontinuity | Refine alignment and mask support first; then edge decontamination or a small interior transition. Broad feathering is not a fix for displacement. |

## Mask construction

The **allowed mask** is a predeclared permission envelope, white wherever a change is authorized, including agreed edge transition and shadows. The **compositing mask** is the actual opacity shape of the insert. Its nonzero support must fit inside the envelope. Do not derive permission by thresholding the final difference or broadening it to include accidental leaks.

Use a selection/path or a dedicated mask per meaningful part. An inserted pair of glasses normally needs frame + lenses + tiny contact shadows, not an entire rectangle of regenerated skin. Retain original hair above the temple and the original face wherever generation adds nothing required. A removal/fill must reveal restored background across the old object and its attributable contact/cast shadows, reflections and residual fringe, including disconnected regions. Follow [object-removal.md](object-removal.md); an object-segmentation mask alone is insufficient. Preserve unrelated shadows and reflections.

A mask can preserve identity better than another generator prompt. Inspect the mask alone and in overlay; look for disconnected holes, residual edges and shadow truncation. Changing mask density lets the original ghost through and is not a substitute for matching appearance.

## Acceptance sequence

1. Geometry and physical fit; correct or regenerate displaced structures.
2. Mask/occlusion and necessary shadow/reflection support. For removals, compare the aligned generated crop with the final composite: verify that no old object-related shadow, reflection or fragment survived because the compositing mask omitted it.
3. Color/profile and local tone, then optics and texture at final placement scale.
4. Whole-frame inspection, layer toggling and 100–200% edge inspection.
5. Pixel audit and native save. If natural blending needs editing protected pixels, revise the allowed area with the user or regenerate; do not silently soften the invariant.

Record observations rather than saying "quality matches" without evidence. A visual match remains a judgment and synthetic detail remains invented. Automated histogram matching may destroy material differences; do not use it as a universal correction.
