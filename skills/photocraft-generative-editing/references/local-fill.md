# Local fill, removal, insertion and detail refinement

## Prepare

Capture baseline revision, active document identity, original dimensions, mode/depth/profile, and a source fingerprint. A filename alone is not a revision identity. Keep a checkpoint. Decide whether to preserve the last accepted grade or the undeveloped original; use the user's established baseline.

Define the allowed area before editing. The generator crop contains enough context for perspective, lighting, occlusion and material; it may be much larger than the allowed area. For insertion, the final mask reveals the new object and its necessary shadows/reflections. For removal/replacement, follow [object-removal.md](object-removal.md): reveal restored surfaces over the old object and all attributable visible effects, including disconnected shadows/reflections. For a new shape, an old object's silhouette may be too narrow. Do not expand permission after seeing a pixel difference just to make verification pass.

Export the full composite losslessly, then extract its native-pixel crop. Use a PhotoCraft duplicate with merged layers and `image.crop`, or the optional helper's `crop` command. Never use an app-window screenshot as the image source: it includes viewport scale and UI. Scratch crops must not replace the live target.

Small edits deserve large generator coverage: crop around the face for glasses rather than sending a full street photograph. Request high local detail at the intended physical scale; inspect actual returned dimensions. More generated pixels are not evidence of more real detail. Detail refinement is a synthetic reconstruction, not recovered camera information.

## Generate and align

Use the provider guidance. Ask to change only the identified element, preserve pose/identity/crop, and match existing optics, tones and texture. Reference-only generation may still move anatomy or structures.

Record crop origin/size, returned size and placement matrix. Compare at least two stable landmarks near the edit, preferably on opposite sides; check a third to reveal scale/rotation errors. Exact dimensions do not guarantee exact framing. Resolve translation/scale/rotation before masking. If the model changed facial geometry, choose a smaller object-only mask or regenerate. Never warp protected original pixels to follow it.

For an identical-framing crop, `edit.transform`'s affine matrix is `[Wc/Wg,0,0,Hc/Hg,x0,y0]`, subject to discovered schema. The optional `map` helper rejects mismatched aspect ratios. It cannot prove landmark alignment.

## Composite in PhotoCraft

Open the generated file in an authorized read root. In live 0.10.0, transfer its layer to the intended document through the discovered `layer.copyToDocument` engine command. Inspect the resulting layer ID and selected target; transform only that layer. In headless, capability-scoped `doc_place` can be used if supported. See the bridge reference for the distinction.

Construct an object/surface mask in document coordinates. Retain editable source pixels and masks. Choose feather based on the native edge's optical softness; a fixed large blur gives halos and erases fine detail. Keep transitions inside the allowed envelope. Hair can sit above an eyeglass temple; an object can cast a separate masked shadow; see-through lenses may need different alpha/tone from an opaque frame. Selective masking is more faithful than replacing the entire face crop.

Run the blending review. Apply color, luminance or texture corrections only to the patch, via clipping or equivalent layer targeting. Confirm channel/mask target before filters; a command may otherwise affect the mask. Changes to any previously accepted correction layer invalidate the corresponding preservation baseline.

## Verify

Toggle the new layer/group against the baseline. Examine edges at 100–200% and the whole image at viewing size. Export the composite, audit outside the allowed region, save the editable project and keep the accepted patch. Leave the final document active. Remove only scratch documents that the agent created and whose state is known; never close unrelated user work.
