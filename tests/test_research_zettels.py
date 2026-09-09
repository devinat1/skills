"""Static contract checks; behavioral acceptance cases below require an agent dry-run.

Dry-run with no vault writes:
- One note with one question: retain one question and stop at gate 1.
- Two overlapping notes: propose two questions; after approval show shared and
  unique zettels, then stop at gate 2. Preserve conflicting evidence and caveats.
- Conversation only: resolve authorship scope; create proposed Agentic outlines.
- Existing matching zettel: reuse it; disclose any update before approval.
- Source edited after approval: stop before overwrite and retain the backup.
- Create times out after succeeding: reconcile readback before retrying.
- Repeated run: reuse matching notes and umbrella rather than duplicate them.
- Literature source: read it but propose a new outline instead of replacing it.

These checks test the written contract, not model compliance or a live vault.
"""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/productivity/research-zettels/SKILL.md"


class ResearchZettelsContract(unittest.TestCase):
    def test_discovery_and_references(self):
        text = SKILL.read_text()
        self.assertTrue(text.startswith("---\nname: research-zettels\ndescription:"))
        self.assertTrue((SKILL.parent / "../../../docs/skill-connections.md").resolve().is_file())
        for dependency in ("unscramble", "obsidian", "obsidian-markdown"):
            self.assertIn(f"`{dependency}`", text)

    def test_ordered_approval_gates(self):
        text = SKILL.read_text()
        markers = ["**Approval gate 1:**", "**Approval gate 2:**", "## 3. Draft", "## 4. Apply"]
        positions = [text.index(marker) for marker in markers]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("Wait for explicit approval before any vault mutation", text)

    def test_safe_dry_canonicalization_contract(self):
        text = SKILL.read_text()
        for required in (
            "obsidian vault=State vault", "selector **before the command**",
            "snapshots immutable", "local citation routing", "Unicode collisions",
            "Create canonical notes first", "a timeout may\nhave succeeded",
            "Leave other existing\nMOC bodies unchanged", "Literature and periodic notes remain read-only",
            "**never invoke follow-up skills automatically**", "No new research belongs",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
