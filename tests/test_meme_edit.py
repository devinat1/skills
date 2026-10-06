"""Static skill/install checks, not proof of editing or acoustic quality.

Run: python3 tests/test_meme_edit.py
"""
import importlib.util
import json
import os
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
home = Path(os.environ.get('AGENTIC_HOME', Path.home() / '.agentic'))
path = repo / 'skills/writing/video/workflows/meme-edit/GUIDE.md'
text = path.read_text()
spec = importlib.util.spec_from_file_location(
    'metadata', repo / 'scripts/generate-skill-metadata.py')
metadata = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metadata)
fields = metadata.read_frontmatter(repo / 'skills/writing/video/SKILL.md')
assert fields['name'] == 'video'
assert not (path.parent / 'SKILL.md').exists()
assert text.count('```') % 2 == 0
for dependency in ('../watch/GUIDE.md', '../editor/GUIDE.md'):
    assert dependency in text, dependency
    assert (path.parent / dependency).is_file(), dependency
assert (home / 'skills/video/workflows/edit-video/references/media-workflow.md').is_file()
for requirement in (
    'finished MP4 or an editable Diffusion Studio project',
    'one best humorous edit', 'without per-placement approval',
    'dense opening, then mostly clean explanation',
    'Abrupt audio and distorted meaning are rejection criteria',
    'Never fabricate quotations or replacement speech',
    'no safe-duration exemption', 'Do not upload or publish',
    'not acoustically or visually reviewed', 'Verify protected inputs are unchanged',
    'Verify the actual MP4', 'ASSETS.md', 'EDIT-LEDGER.md', 'REVIEW.md',
):
    assert requirement in text, requirement
assert not (home / 'skills/meme-edit').exists()
index = json.loads((home / 'index.json').read_text())
assert index['skills']['video'] == 'skills/video'
assert 'meme-edit' not in index['skills']
manifest = json.loads((repo / '.claude-plugin/plugin.json').read_text())
assert './skills/writing/video' in manifest['skills']
assert './skills/writing/meme-edit' not in manifest['skills']
for readme in (repo / 'README.md', repo / 'skills/writing/README.md'):
    assert '[video]' in readme.read_text(), readme
    assert '[meme-edit]' not in readme.read_text(), readme
print('PASS: merged meme workflow dependencies, catalog and static contract checks')
