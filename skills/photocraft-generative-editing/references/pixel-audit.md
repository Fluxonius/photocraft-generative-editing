# Geometry and protected-pixel auditing

The optional helper `scripts/pixel_guard.py` is offline and uses Python 3.10+ with Pillow. It performs no AI generation, compositing, color matching or sharpening. Use PhotoCraft or other explicitly authorized tools for those tasks. Existing PhotoCraft capabilities remain preferred when they suffice; the helper does not bypass bridge filesystem restrictions.

Invoke it by interpreter with the actual skill directory as `SKILL_DIR`. All paths below are examples relative to an authorized task directory, not magic output locations. The output parent must exist. Never overwrite the frozen baseline.

```sh
python "$SKILL_DIR/scripts/pixel_guard.py" crop --source baseline.png --box 1900 950 1000 1000 --output context.png
python "$SKILL_DIR/scripts/pixel_guard.py" map --crop 1900 950 1000 1000 --generated 1250 1250
python "$SKILL_DIR/scripts/pixel_guard.py" local --before baseline.png --after composite.png --allow-mask allowed.png --expected-source-sha256 SOURCE_SHA256
python "$SKILL_DIR/scripts/pixel_guard.py" expand --source-size 6000 4000 --margins 555 0 556 0
python "$SKILL_DIR/scripts/pixel_guard.py" outpaint --before baseline.png --after expanded.png --margins 555 0 556 0 --expected-source-sha256 SOURCE_SHA256
```

`crop` extracts samples without resampling, records source SHA256, and refuses an existing output. `map` returns `[a,b,c,d,e,f]` for the unchanged-framing affine case; mismatched aspect ratios are rejected, not stretched. Record the full native baseline fingerprint even when using the generator crop. An unchanged fingerprint is required to prove the baseline file used for the audit is the captured one. In-memory document changes still require revision/layer inspection.

`local` needs a full-canvas **8-bit grayscale L permission mask**: zero = protected, any nonzero sample = permitted change. This is an audit envelope, not alpha strength. Include the agreed feather/shadow extent. Construct it from the predeclared selection/path or task geometry, never from differences found after editing. An arbitrary bounding rectangle can be valid permission when explicitly chosen, but does not establish an object-tight mask. Mask creation/export is an editor or authorized raster-tool step.

`outpaint` compares every original channel sample inside its translated rectangle at the specified margins. It does not validate new-border aesthetics or require those borders to differ from background. `local` likewise can pass an unchanged output: verify the requested new content exists visually.

Both return JSON counts/bounds and source/output fingerprints. Exit **0** means comparable/pass, **1** means protected samples changed, **2** means invalid/unsupported input. A successful process invocation is not sufficient: read `passed`, counts and any error. Rectangles returned as `bbox` use `[left,top,right,bottom)`.

## Supported data and honest claims

The helper supports single-frame lossless PNG/TIFF, **8-bit L/LA/RGB/RGBA**, same channel mode and identical embedded ICC/transfer metadata. It compares all decoded channels, including alpha and hidden RGB under zero alpha. It rejects JPEG, unsupported modes/depths, nontrivial EXIF orientation, mismatched sizes/profiles, PNG color-key transparency (tRNS), TIFF TransferFunction/WhitePoint/PrimaryChromaticities/ReferenceBlackWhite tags, JPEG-compressed TIFF and images over 64M pixels. Color-key transparency must be explicitly represented as alpha in a verified comparison export before this helper is used; it is never silently ignored. TIFFs with those additional color-interpretation tags need a verified color-managed export or another auditor. No automatic conversion, profile assignment, normalization, or resampling is performed during auditing.

For 16/32-bit, CMYK/Lab or larger images, keep the native original intact and use a verified native-depth export/comparison path. A temporary 8-bit proxy can guide a visual preview but cannot prove preservation of higher-depth samples. Report the limitation; never downconvert the document to make this helper pass. Identical absent profiles prove only equal untagged samples, not a verified color space. File bytes and metadata beyond the stated signature may differ even when sample preservation passes.

## Visual acceptance remains separate

The audit detects unintended changes, not a bad generated face, incorrect lighting or synthetic detail. Use [blend-quality.md](blend-quality.md) before acceptance. The correct claim is "protected decoded pixels unchanged in comparable exports", accompanied by dimensions and visual observations, not "the whole image is lossless in every format".
