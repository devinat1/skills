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
         for name in ('edit-video', 'youtube-shorts', 'post')}
texts.update({name: (home / 'skills' / name / 'SKILL.md').read_text()
              for name in ('editor', 'watch', 'postiz')})
policy = (owned / 'edit-video/references/media-workflow.md').read_text()
for name, text in texts.items():
    assert text.startswith('---\n'), name
    assert 'media-workflow.md' in text, name
    assert text.count('```') % 2 == 0, name
assert (home / 'skills/edit-video/references/media-workflow.md').is_file()
for required in ('do not install or download inference models', '10 minutes',
                 '15 minutes', 'digital silence', 'known tone', 'clean known speech',
                 'deliberately cut words', 'known interruptions',
                 'listening review pending', 'same model and processing configuration',
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
print('PASS: six skills reference shared policy; provider, handoff, reuse and approval guards present')
