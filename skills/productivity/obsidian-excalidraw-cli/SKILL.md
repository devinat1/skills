---
name: obsidian-excalidraw-cli
description: Create, inspect, edit, export, or test Obsidian Excalidraw drawings through the local Obsidian CLI, including timeout and BUSY recovery.
---

# Obsidian Excalidraw CLI

Use the running desktop app's native `obsidian-excalidraw-plugin:*` commands. No separate CLI, Node helpers, or downloaded repository is required.

## Discover

Establish the task and exact registered vault name/ID. Drawing and output paths are visible, vault-relative paths including extensions. Use `obsidian vaults verbose` to find vault names; never infer the focused vault.

```sh
obsidian vault="State" obsidian-excalidraw-plugin:help
obsidian vault="State" obsidian-excalidraw-plugin:status
obsidian vault="State" obsidian-excalidraw-plugin:schema action=create
```

Replace `State` with the established vault on every command; put `vault=` before the plugin command. Run locally on the computer running Obsidian; Windows uses `Obsidian.com` for captured output.

Require `ok: true`, `status: completed`, the expected returned vault, `nativeCLI: true`, and `ready: true`; creation also needs converter readiness. Related discovery responses must share one plugin session. Exit code zero alone is not success.

Query `schema action=<command>` before using a command. The running `help`, `schema`, and `api` responses define the contract, not a guessed version. For authoring details, use focused lookups such as `api surface=ea name=addText` or `api surface=lib`.

If discovery fails, report the exact error and stop. Do not install another CLI, change settings, enable plugins, restart the app, or bypass the protocol with arbitrary `obsidian eval` without permission.

## Operate

Inspection is read-only. Establish exact drawing/output paths before writes; only perform the requested changes. Opening can run configured drawing scripts. Trusted `script` execution needs separate code review and explicit authorization.

| Task | Native workflow |
|---|---|
| Inspect | `list` or `read path="<drawing>" source=disk detail=elements`; no opening or saving. |
| Create | `create` at an unused exact `.excalidraw.md` path; never overwrite or delete/recreate. Read disk afterward. |
| Edit | `open path="<drawing>"` once; retain `data.viewId`. Read the complete live scene using that ID as `view=`, then `apply` a bounded change with actual element IDs and the fresh `expectedRevision`. |
| Export | `export path="<drawing>" source=disk out="<preview.png>" requestId=<unique-id>`; use a new output path unless overwriting is explicitly authorized. |

Requests use `json=<small JSON>` as one process argument, or `input=<visible vault-relative JSON file>`. Prefer argument-array execution; never interpolate untrusted text into shell code. An external private state file is not a valid `input=` path. Authorize any additional request file created inside the vault.

Before a write, retain the exact request and unique `requestId` privately outside Git, under `${AGENTIC_HOME:-$HOME/.agentic}/state/runs/obsidian-excalidraw-cli/<unique-run>/<vault-key>/`. Use owner-only permissions where supported; retain the response there too. These files can contain private drawing text.

Serialize writes to each drawing. Require `ok: true`, `status: completed`, `mutation: applied`, and `persistence: saved`; then verify the saved result. Use creation's `data.idMap` or IDs from read-back for edits, not skeleton-local IDs. Bound labels have their own text-element IDs.

Exhaust `nextOffset` for reads/lists at the same returned `revision`. Restart the read if that revision changes; a first page is not a complete scene.

## Recover

- **Timeout/lost output:** query `result requestId=<original-id>`, then inspect the exact disk target and relevant live state. The receipt can name the original command rather than `result`. Do not repeat an uncertain write with a new ID or rerun the whole recipe.
- **`BUSY`:** inspect disk and live state without another write. If the view remains loading, closing, or migrating, stop and ask the user to inspect it before an authorized retry.
- **`STALE_REVISION`:** read the complete live scene again and reconsider the edit before applying against its fresh revision.
- **Pending, unsaved, unknown, or expired receipt:** stop writes until state inspection resolves the outcome. `ok: null` is not success. Receipts are session-scoped; disk state alone cannot rule out unsaved live state or a pending operation.

## Verify

After creation/editing, read the complete disk scene and confirm intended elements, labels, bindings, and changes. Export does not save live state: confirm a nonempty output and that its exported revision matches the saved revision being verified.

Inspect the image for clipping, labels, connectors, layering, and framing using an available image viewer. If unavailable, report visual inspection as unverified.

Finish with exact artifact paths, checks passed, and anything unverified. Distinguish working discovery, saved creation/editing, export, and visual inspection. Keep partial artifacts and receipts unless cleanup is explicitly authorized.
