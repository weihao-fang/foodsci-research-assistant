"""Local structure and public-export checks; this is not a client or scientific certification."""
import json
from pathlib import Path
import re
from zipfile import ZipFile

import yaml

from build import ENTRIES

def validate(root):
    root = Path(root).resolve()
    version = (root / 'VERSION').read_text(encoding='utf-8').strip()
    skills = list((root / 'skills').glob('*/SKILL.md'))
    assert {p.parent.name for p in skills} == set(ENTRIES)
    for path in skills:
        text = path.read_text(encoding='utf-8')
        match = re.match(r'\A---\r?\n(.*?)\r?\n---', text, re.S)
        assert match, path
        meta = yaml.safe_load(match.group(1))
        assert meta['name'] == path.parent.name and isinstance(meta['description'], str)
        assert 0 < len(meta['description']) <= 1024 and meta['metadata']['version'] == version
        if path.parent.name != ENTRIES[0]:
            assert meta['metadata']['requires-foodsci-research-assistant'] == version
        ui = yaml.safe_load((path.parent / 'agents/openai.yaml').read_text(encoding='utf-8'))
        assert ui['interface']['display_name'] and ui['interface']['short_description']
    manifest = json.loads((root / 'plugin.json').read_text(encoding='utf-8'))
    assert manifest['version'] == version
    assert manifest['$schema'] == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
    assert manifest['extensions']['com.openai']['onboardingSkill'] == './skills/foodsci-research-assistant/SKILL.md'
    assert manifest['license'] == 'LicenseRef-FoodSci-Research-Noncommercial-1.0'
    assert (root / 'LICENSE').read_bytes() == (root / 'skills/foodsci-research-assistant/LICENSE').read_bytes()
    links = 0
    for path in root.rglob('*'):
        if '.git' in path.parts or '__pycache__' in path.parts or not path.is_file():
            continue
        assert not path.is_symlink(), path
        if path.suffix in ('.md', '.py', '.yml', '.yaml', '.json', '.txt') or path.name in ('LICENSE', 'AGENTS.md'):
            text = path.read_text(encoding='utf-8')
            for pattern in (r'[A-Za-z]:[/\\]foodsci', r'[A-Za-z]:[/\\]Users[/\\][^/\\\s]+',
                            r'plugins_[0-9a-f]{32}', r'pluginrel_[0-9a-f]{32}',
                            r'\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b'):
                assert not re.search(pattern, text), f'Personal origin or account receipt in {path.relative_to(root)}'
            if path.suffix == '.md':
                targets = re.findall(r'\[[^\]]*\]\(([^)]+)\)', text)
                targets += re.findall(r'<img[^>]+src="([^"]+)"', text)
                for target in targets:
                    target = target.split('#', 1)[0].split('?', 1)[0].strip('<>')
                    if not target or re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                        continue
                    resolved = (path.parent / target).resolve()
                    assert resolved.is_relative_to(root) and resolved.is_file(), (path, target)
                    if path.is_relative_to(root / 'skills/foodsci-research-assistant'):
                        assert resolved.is_relative_to(root / 'skills/foodsci-research-assistant'), (path, target)
                    links += 1
    for path in (root / 'downloads').glob('*.zip'):
        with ZipFile(path) as archive:
            assert archive.testzip() is None
            assert all(not n.startswith('/') and '..' not in Path(n).parts for n in archive.namelist())
    return {'status': 'passed', 'version': version, 'skills': len(skills), 'local_links': links,
            'public_export_scan': 'passed', 'client_installation_test': False}

if __name__ == '__main__':
    print(json.dumps(validate(Path(__file__).resolve().parents[1]), ensure_ascii=False, indent=2))
