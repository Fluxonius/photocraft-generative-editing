# Generative expand / outpainting

## Fix geometry first

Record source `(W,H)` and integer nonnegative margins `(L,T,R,B)`. Target canvas is `(W+L+R,H+T+B)`; the original moves to `(L,T)` with no resampling. Its protected rectangle is `[L,T,L+W,T+H)` using half-open edges. Preserve all original layers and masks, translating them consistently when the canvas origin moves.

If the user specifies only an aspect ratio, choose the minimal expansion consistent with their requested fixed dimension/direction and disclose the actual integer dimensions. Exact ratio may be impossible: 6000x4000 at fixed height cannot be exactly 16:9; 7111x4000 gives a near ratio and margins 555/556. An exact-ratio larger canvas would also require extra height. Ask only when the choice changes the user's composition materially. Never crop, stretch, or resample the source silently to obtain a ratio.

Discover `image.canvasSize` (or the installed equivalent) and its anchor/offset semantics before mutation; do not infer an argument schema. Verify the source layer bounds moved as planned. A signed preview of target margins can be prepared without changing user work.

## Generate only extensions

Keep the original as a protected native-scale region. Give the generator overlapping edge context plus explicit target layout, perspective, horizon, lighting, grain and content restrictions. Provider context may be resized to fit limits; the final original never is. Record the context scale and mapping for each strip/tile.

For moderate expansion, the provider may return a whole expanded proposal, but only generated border pixels are composited into the final document. The proposal's regenerated central area is discarded. For large additions, work in strips/tiles with contextual overlap and consistent global geometry. Verify corners, long lines, horizon and repeated objects after each stage. Do not resize the original to make a generated tile fit.

Place extension layers below an unchanged original composite, or mask them strictly to new canvas areas. Original document layers can remain above. If using a group for the original, ensure adjustment layers do not inadvertently change new borders or vice versa; compare the final composite. Retain original alpha: for translucent originals, an opaque extension beneath them can change protected output. Mask generated support out of the entire protected rectangle, including transparent pixels.

Inside strict preservation mode, a seam feather into the original is forbidden. You can generate overlap for continuity, then clip at the boundary; if that cannot yield a good seam, retry or ask to allow a narrow, explicit interior blend strip. A protected central rectangle must still pass exact comparison unless the user approved relaxing it.

## Accept

Apply the candidate/composite gates in [quality-and-variants.md](quality-and-variants.md); compare requested alternatives with identical canvas geometry and protected original rectangle.

Run the blending review on borders and corners. Check geometry and seamlessness at viewing size and at native scale. Export a comparable lossless composite and compare the translated original rectangle byte-for-byte at the decoded sample level. Use helper `outpaint` for supported 8-bit data. Check actual target dimensions and masks, save `.pcraft` and the requested export, and report any rounding or newly generated regions.
