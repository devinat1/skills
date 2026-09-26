"""Static policy regression checks; not proof of agent behavior.

Run: python3 tests/test_media_workflow_policy.py
Installed standalone editor/watch/postiz skills are checked through AGENTIC_HOME.
"""
import os
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
home = Path(os.environ.get('AGENTIC_HOME', Path.home() / '.agentic'))
owned = repo / 'skills/writing'
texts = {name: (owned / name / 'SKILL.md').read_text()
         for name in ('edit-video', 'youtube-shorts', 'meme-edit', 'video-slides', 'post')}
texts.update({name: (home / 'skills' / name / 'SKILL.md').read_text()
              for name in ('editor', 'watch', 'postiz')})
policy = (owned / 'edit-video/references/media-workflow.md').read_text()
for name, text in texts.items():
    assert text.startswith('---\n'), name
    assert 'media-workflow.md' in text, name
    assert text.count('```') % 2 == 0, name
assert (home / 'skills/edit-video/references/media-workflow.md').is_file()
for required in ('do not install or download inference models', '10 minutes',
                 '15 minutes', 'jev-video-policy.md',
                 'not acoustically or visually reviewed',
                 'source checksum', 'GUI changes', 'publication permission',
                 'https://whisper.taila3f981.ts.net'):
    assert required in policy, required
for forbidden in ('free local Whisper', 'transcribe the actual input locally',
                  'Use free local transcription', 'MAX_RETRIES=3'):
    assert all(forbidden not in text for text in texts.values()), forbidden
assert 'not uploads or publication' in texts['youtube-shorts']
assert 'Which clips do you approve for upload and posting' in texts['youtube-shorts']
assert 'Export a finished video only when requested' in texts['edit-video']
assert 'before another `posts:create`' in texts['postiz']
jev = (owned / 'edit-video/references/jev-video-policy.md').read_text()
for required in ('jev.py', 'post-edit', 'agent', 'stops the workflow',
                 'structural', 'not acoustically or visually reviewed'):
    assert required.lower() in jev.lower(), required
for name in ('edit-video', 'youtube-shorts', 'meme-edit', 'video-slides', 'editor', 'watch'):
    assert 'Jev-first' in texts[name] or 'Jev decisions' in texts[name] or 'Jev text-evidence judgments' in texts[name], name
    assert 'stop' in texts[name].lower() and 'unavailab' in texts[name].lower(), name
    assert 'listening review pending' not in texts[name].lower(), name
assert 'artifacts/jev/PROTOCOL.md' not in texts['watch']
assert 'not uploads or publication' in texts['youtube-shorts']
assert 'Hard approval gate — review-first mode only' in texts['video-slides']
assert 'rather than asking a layout question' in texts['video-slides']
assert 'questions` is an object keyed by question ID' in jev
assert 'local `Invalid batch` result' in jev
assert 'A completed stage, self-correctable command error' in policy
assert 'Export remains request-only' in policy
print('PASS: video skills preserve safety boundaries and continue through routine edit decisions')
