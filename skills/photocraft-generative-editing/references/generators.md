# Generator adapters

## Built-in ChatGPT / Codex ImageGen

When the built-in generation/editing tool and an imagegen skill are available, use their current documented workflow. Inspect a local source crop through the host's image viewer before editing. Pass the crop as the edit target and other inputs with explicit roles. Ask for unchanged framing, target object and protected landmarks, plausible material/lighting, final local detail and no new text/logos.

Use actual tool schemas; don't invent resolution, seed, mask, filesystem-output, model or local-file arguments. A requested resolution in prose is not proof it was returned: inspect the saved output dimensions. Save/copy the returned file into the authorized PhotoCraft read root, then import it. Don't send a window screenshot or entire 4K frame for a tiny change unless full-scene context is essential; even then extract a local patch before compositing.

Built-in generation does not inherently grant arbitrary user-supplied mask support, pixel-exact preservation, transparent output or exact identity/geometry retention. Use the skill's geometry/mask/audit steps. For a transparent insert, request real alpha and verify it. A generated file path is an artifact, not executable instructions.

Example prompt (fill/refine):

> Edit this crop only by adding [object] on [identified subject]. Preserve framing, subject identity, pose and all existing structures. Match [observed light], [working monochrome/color appearance], [focus] and [grain]. Keep [landmarks] fixed; add only physically necessary shadows/reflections. Return this same composition with enough detail for the object's final native-pixel size. Do not retouch surrounding skin or hair.

For output screening, optional variant counts, similar-reference refinement and retry limits, follow [quality-and-variants.md](quality-and-variants.md). Inspect every actual returned candidate; a successful generation call does not mean the fill passed review.

## Other providers and agents

The SKILL.md workflow is provider-neutral. Adapt to real available image-edit/inpaint/outpaint capabilities. Confirm reference-image input, mask semantics (white may mean edit OR preserve), supported modes/profiles/alpha, maximum output size and whether resizing/padding/reframing occurs. Follow that host's tooling and permissions. Lack of a generator is a prerequisite to resolve, not grounds to silently choose a new paid service.

A provider adapter needs to supply:

- The source context image, target edit, protection instructions and optional provider-specific mask.
- The actual result artifact, dimensions, alpha/mode/profile information and any known crop/padding behavior.
- Enough information to map generated coordinates back to document coordinates. If unknown, inspect landmarks; do not assert exact alignment.

The compositing mask stays under agent/editor control regardless of the provider mask. No helper in this package calls any generator or accepts API keys. Installing this skill does not create a Gemini/OpenAI/ComfyUI account or add PhotoCraft generative features.

## Outpaint prompts

Describe the new margins, continued surfaces and long lines, camera perspective, light, focus and texture. Identify the preserved rectangle and prohibit duplicating the original subject into the new border unless requested. If the provider returns the whole scene, discard its central original region when assembling. Generate detail from crops/strips at useful pixel density, not a tiny entire-canvas preview enlarged later.
