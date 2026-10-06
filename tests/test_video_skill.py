"""Static consolidation regression check. Run: python3 tests/test_video_skill.py."""
import json
import os
import re
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
home = Path(os.environ.get('AGENTIC_HOME', Path.home() / '.agentic'))
video = repo / 'skills/writing/video'
entry = (video / 'SKILL.md').read_text()
workflow_names = {
    'production', 'edit-video', 'editor', 'watch', 'youtube', 'brag', 'brag-slim',
    'video-slides', 'meme-edit', 'youtube-shorts', 'hyperframes-core',
    'hyperframes-animation', 'hyperframes-creative', 'hyperframes-keyframes', 'hyperframes-cli',
}
retired = workflow_names - {'production'}
assert list(video.rglob('SKILL.md')) == [video / 'SKILL.md']
assert 'name: video\n' in entry
assert (home / 'skills/video').resolve() == video.resolve()
assert 'Publishing always requires approval of the exact media revision' in entry
assert 'not acoustically or visually reviewed' in entry
assert 'clean edits and assembled intercuts remain export-on-request' in entry
for name in workflow_names:
    path = video / 'workflows' / name / 'GUIDE.md'
    assert path.is_file(), name
    assert f'workflows/{name}/GUIDE.md' in entry, name
    assert not path.read_text().startswith('---\n'), name
    assert path.read_text().count('```') % 2 == 0, name

# Every literal Markdown reference is portable and resolves inside the bundle.
# External URLs, anchors and explicit placeholder templates are not local files.
for path in video.rglob('*.md'):
    for target in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)', path.read_text()):
        if '://' in target or target.startswith(('#', 'mailto:')) or '<' in target:
            continue
        relative = target.split('#')[0]
        if relative:
            resolved = (path.parent / relative).resolve()
            assert resolved.is_relative_to(video.resolve()), (path, target)
            assert resolved.exists(), (path, target)
    assert not re.search(r'skills/(?:' + '|'.join(sorted(retired)) + r')/', path.read_text()), path

engagement = (video / 'references/engagement.md').read_text()
for required in ('maximum viewer engagement', '**Hook:**', '**Progress:**', '**Pacing:**',
                 '**Attention cues:**', '**Payoff:**', 'actual viewer analytics'):
    assert required in engagement, required
intercuts = (video / 'workflows/video-slides/GUIDE.md').read_text()
assert 'Finish and validate the standalone `brag.mp4` before modifying' in intercuts
assert 'Mute all imported brag audio' in intercuts
assert 'review-first mode only' in intercuts
slim = (video / 'workflows/brag-slim/GUIDE.md').read_text()
assert '--no-music' in slim and '--no-sfx' in slim and 'produce a silent asset' in slim
launch = (video / 'workflows/brag/GUIDE.md').read_text()
assert '../brag-slim/GUIDE.md' in launch
assert (video / 'workflows/brag/assets/music').is_dir()
assert (video / 'workflows/hyperframes-creative/frame-presets').is_dir()
assert (video / 'workflows/edit-video/scripts/jev.py').is_file()

index = json.loads((home / 'index.json').read_text())
manifest = json.loads((repo / '.claude-plugin/plugin.json').read_text())
assert index['skills']['video'] == 'skills/video'
assert './skills/writing/video' in manifest['skills']
for name in retired:
    assert not (home / 'skills' / name).exists(), name
    assert name not in index['skills'], name
    assert f'./skills/writing/{name}' not in manifest['skills'], name
    assert not (repo / 'skills/writing' / name).exists(), name
for readme in (repo / 'README.md', repo / 'skills/writing/README.md'):
    text = readme.read_text()
    assert '[video]' in text
    assert all(f'[{name}]' not in text for name in retired)
print('PASS: one video entry point, 15 reachable workflows, portable links, engagement and approval contracts')
