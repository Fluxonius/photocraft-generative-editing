# Sources, provenance and compatibility

This skill's prose and helper code were written for this project, informed by public protocols, existing community workflows and observed integration failures. No upstream skill body or manual is bundled verbatim. This is an independent community project, not an official OpenAI, Adobe or PhotoCraft product.

- [mroxso/artcraft-skills — PhotoCraft](https://github.com/mroxso/artcraft-skills/blob/main/artcraft/photocraft/SKILL.md): live-session preservation, capability discovery, scoped file operations, editable results, uncertain mutation reconciliation.
- [midasmatterhorn/artcraft-skills — PhotoCraft](https://github.com/midasmatterhorn/artcraft-skills/blob/main/photocraft/SKILL.md): versioned capabilities, source-based limitations, reversible workflows and export verification.
- [hermes-pro/storytold-skills — PhotoCraft](https://github.com/hermes-pro/storytold-skills/blob/main/photocraft/SKILL.md): practical layer, selection, adjustment and compositing recipes; its Hermes-specific setup is not a prerequisite here.
- [PhotoCraft 0.10.0 control protocol](https://github.com/storytold/photocraft/blob/v0.10.0/docs/control-protocol.md) and [MCP](https://github.com/storytold/photocraft/blob/v0.10.0/docs/mcp.md): authoritative transport/version reference. Discover installed schemas rather than trusting a frozen list.
- [Agent Skills format](https://agentskills.io/specification): portable SKILL.md package conventions.

The macOS 0.10.0 live routes for tab selection, opening/exporting files, copying a layer between documents, affine transforms and selection-based masks were exercised in the originating workflow. That evidence does not verify every PhotoCraft command, other OSes or later releases. Native generative fill/expand inside PhotoCraft is not assumed: generation is supplied externally.

The project includes functional helper tests and independent instruction scenarios. Those do not establish successful generative outpainting by every image provider, color fidelity at unsupported bit depths, or end-to-end integration on other agents. See the project validation report for the tested scope. If redistributing copied upstream materials later, include their applicable license/copyright notices; links here do not relicense upstream content.
