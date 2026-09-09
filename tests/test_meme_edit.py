"""Static skill/install checks, not proof of editing or acoustic quality.

Run: python3 tests/test_meme_edit.py
"""
import importlib.util
import json
import os
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
home = Path(os.environ.get('AGENTIC_HOME', Path.home() / '.agentic'))
path = repo / 'skills/writing/meme-edit/SKILL.md'
text = path.read_text()
spec = importlib.util.spec_from_file_location(
    'metadata', repo / 'scripts/generate-skill-metadata.py')
metadata = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metadata)
fields = metadata.read_frontmatter(path)
assert fields['name'] == 'meme-edit'
assert fields['disable-model-invocation'] == 'true'
assert text.count('```') % 2 == 0
for dependency in ('watch/SKILL.md', 'editor/SKILL.md',
                   'edit-video/references/media-workflow.md'):
    assert dependency in text, dependency
    assert (home / 'skills' / dependency).is_file(), dependency
for requirement in (
    'finished MP4 or an editable Diffusion Studio project',
    'one best humorous edit', 'without per-placement approval',
    'dense opening, then mostly clean explanation',
    'Abrupt audio and distorted meaning are rejection criteria',
    'Never fabricate quotations or replacement speech',
    'no safe-duration exemption', 'Do not upload or publish',
    'edited; listening review pending', 'Verify protected inputs are unchanged',
    'Verify the actual MP4', 'ASSETS.md', 'EDIT-LEDGER.md', 'REVIEW.md',
):
    assert requirement in text, requirement
assert (home / 'skills/meme-edit').resolve() == path.parent.resolve()
index = json.loads((home / 'index.json').read_text())
assert index['skills']['meme-edit'] == 'skills/meme-edit'
manifest = json.loads((repo / '.claude-plugin/plugin.json').read_text())
assert './skills/writing/meme-edit' in manifest['skills']
for readme in (repo / 'README.md', repo / 'skills/writing/README.md'):
    assert '[meme-edit]' in readme.read_text(), readme
print('PASS: meme-edit metadata, dependencies, catalog and static contract checks')
