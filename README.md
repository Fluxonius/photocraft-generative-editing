# PhotoCraft Generative Editing

An independent Agent Skill for localized AI image edits and canvas expansion in PhotoCraft. Designed for agents using PhotoCraft through MCP, with a provider-neutral workflow and guidance for ChatGPT's built-in ImageGen when available.

[Русская инструкция](README.ru.md) · [Skill entry point](skills/photocraft-generative-editing/SKILL.md) · [Validation report](docs/VALIDATION.md)

## What it covers

- Generative fill: add, replace or remove an object without regenerating the entire original. Removal covers its attributable shadows/reflections and composites the complete repair area.
- Large-crop detail refinement instead of enlarging a low-resolution full-frame generation.
- Generative expand: preserve original pixels at native scale while adding new borders.
- Editable generated layers, selective masks, occlusion, contact shadows and reflections.
- Patch-local matching of color, tone, lighting, focus, grain and retouch level.
- Exact protected-pixel auditing, separate from visual-quality review.
- Live/headless PhotoCraft differences, capability discovery and recovery after uncertain tool outcomes.

This is a workflow skill, not an image model, editor plugin or MCP server. It does not add native generative features to PhotoCraft or provide paid API access.

## Install

Ask your agent's skill installer:

> Install the skill at https://github.com/Fluxonius/photocraft-generative-editing/tree/main/skills/photocraft-generative-editing

Or clone this repository and copy only `skills/photocraft-generative-editing` into your agent's documented skills directory. For Codex and compatible agents, a common location is `~/.agents/skills/`. Check an existing installation before replacing it. Other agents may use different locations or package import flows.

After installation, invoke `$photocraft-generative-editing` in a host supporting that syntax, or ask the agent to use the PhotoCraft generative-editing skill. Refresh the skill list or start a new session if your host requires it.

## Prerequisites

- PhotoCraft and an existing supported MCP connection. **MCP is required for every PhotoCraft operation; direct CLI, raw HTTP/RPC and desktop automation are not fallback routes.** If unavailable, the agent helps connect MCP before editing. To work in the visible app, use a **live bridge**; a headless session has different documents.
- An available image-editing generator. The skill documents built-in ChatGPT ImageGen and a general contract for other providers; it does not install or authenticate them.
- Optional helper: Python 3.10+ and Pillow (`python -m pip install -r requirements.txt` in your chosen environment).

Configure PhotoCraft and its local MCP connection separately on each computer. Installing the skill or signing into the same account does not connect it to that computer's editor.

## Example requests

- "Add sunglasses to the person in the open PhotoCraft document. Preserve their skin and hair and keep the insert on a masked layer."
- "Remove the selected object; match the surrounding lighting, focus and grain."
- "Extend the canvas on both sides while keeping the original photograph at native scale."
- "Regenerate only a close-up of this insert to improve local detail, then composite it back."

## Package layout

```text
skills/photocraft-generative-editing/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/pixel_guard.py
tests/
docs/VALIDATION.md
```

The main skill routes to focused references for local fill, expansion, blending quality, generator adapters, PhotoCraft bridge behavior and pixel auditing. The offline helper extracts context crops, computes coordinate mappings and checks protected pixels. It makes no network or image-generation calls and performs no automatic color matching.

## Test

```sh
python3 -m unittest discover -s tests -v
# Optional genuine headless-engine test, using only temporary synthetic files:
PHOTOCRAFT_CLI="/absolute/path/to/photocraft-cli" python3 -m unittest discover -s tests -v
```

The recorded macOS PhotoCraft 0.10.0 run passed **17 tests**, including masked insertion, native-scale canvas expansion and native project reopen/render checks. Without a CLI, the native test is skipped and 16 helper tests run. The optional native pipe-based test harness is POSIX-specific.

## Limits

The helper audits comparable 8-bit L/LA/RGB/RGBA lossless PNG/TIFF exports up to 64M pixels. It refuses unsupported depths, color modes and transparency/transfer metadata rather than silently converting them. Keep 16/32-bit and CMYK/Lab originals intact and use a verified native-depth path for preservation claims.

Visual blending quality and synthetic detail are not proven by pixel tests. Other providers, operating systems and real-model generative outpainting have not been certified by the synthetic tests. Discover the actual installed PhotoCraft command schemas instead of assuming version-stable tools.

## Sources and license

MIT — see [LICENSE](LICENSE). Original workflow instructions and helper code, informed by public PhotoCraft documentation and community skills. Attribution and tested version boundaries are in [sources.md](skills/photocraft-generative-editing/references/sources.md).

Not affiliated with or endorsed by OpenAI, Adobe or PhotoCraft/ArtCraft.
