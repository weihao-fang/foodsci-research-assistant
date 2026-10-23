"""Build deterministic, self-contained download packages from the maintained source."""
import hashlib
import io
import json
from pathlib import Path
import re
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ENTRIES = ('foodsci-research-assistant', 'foodsci-literature', 'foodsci-experimental-design',
           'foodsci-data-analysis', 'foodsci-writing', 'foodsci-peer-review')

def file_members(root, folder, prefix):
    result = {}
    for path in sorted(folder.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'Symlinks are not packaged: {path.relative_to(root)}')
        if not path.is_file() or any(x in path.parts for x in ('__pycache__', '.pytest_cache', '.git')) or path.suffix in ('.pyc', '.pyo'):
            continue
        result[prefix + '/' + path.relative_to(folder).as_posix()] = path.read_bytes()
    return result

def archive_bytes(members):
    output = io.BytesIO()
    with ZipFile(output, 'w', compression=ZIP_DEFLATED) as archive:
        for name, content in sorted(members.items()):
            info = ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
    data = output.getvalue()
    with ZipFile(io.BytesIO(data)) as archive:
        assert archive.testzip() is None and set(archive.namelist()) == set(members)
        assert all(archive.read(name) == value for name, value in members.items())
    return data

def build(root, destination=None):
    root = Path(root).resolve()
    destination = Path(destination).resolve() if destination else root / 'downloads'
    version = (root / 'VERSION').read_text(encoding='utf-8').strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('VERSION must be a release SemVer')
    found = {p.parent.name for p in (root / 'skills').glob('*/SKILL.md')}
    if found != set(ENTRIES):
        raise ValueError(f'Expected six skills, found {sorted(found)}')
    main = root / 'skills' / ENTRIES[0]
    if (main / 'LICENSE').read_bytes() != (root / 'LICENSE').read_bytes():
        raise ValueError('The self-contained skill LICENSE must match the root LICENSE')
    single = file_members(root, main, main.name)
    suite = {}
    for entry in ENTRIES:
        suite.update(file_members(root, root / 'skills' / entry, 'foodsci-suite/' + entry))
    plugin = {'foodsci-research-assistant/' + name: (root / name).read_bytes()
              for name in ('plugin.json', 'LICENSE', 'THIRD_PARTY_NOTICES.md', 'assets/icon.svg')}
    for entry in ENTRIES:
        plugin.update(file_members(root, root / 'skills' / entry, 'foodsci-research-assistant/skills/' + entry))
    chat = (root / 'adapters/doubao/FoodSci-豆包聊天版.md').read_bytes()
    usage = '解压后打开FoodSci-豆包聊天版.md；界面允许并可读取时上传，否则粘贴全文，并明确要求将规则用于本次任务。普通聊天附件不等于持久安装；没有工具时不声称运行脚本。完整安装教程在原仓库docs/INSTALL_DOUBAO.md。\n'
    payloads = {
        f'foodsci-codex-{version}.zip': archive_bytes(single),
        f'foodsci-suite-{version}.zip': archive_bytes(suite),
        f'foodsci-plugin-{version}.zip': archive_bytes(plugin),
        f'foodsci-doubao-chat-{version}.zip': archive_bytes({'FoodSci-豆包聊天版.md': chat,
            '使用说明.txt': usage.encode('utf-8'), 'LICENSE': (root / 'LICENSE').read_bytes(),
            'THIRD_PARTY_NOTICES.md': (root / 'THIRD_PARTY_NOTICES.md').read_bytes()}),
        'FoodSci-豆包聊天版.md': chat,
        'FoodSci-豆包聊天版.txt': chat,
    }
    destination.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name, data in payloads.items():
        (destination / name).write_bytes(data)
        manifest.append({'file': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    (destination / 'SHA256SUMS').write_text(''.join(f"{item['sha256']}  {item['file']}\n" for item in manifest), encoding='utf-8')
    return {'version': version, 'packages': manifest}

if __name__ == '__main__':
    print(json.dumps(build(Path(__file__).resolve().parents[1]), ensure_ascii=False, indent=2))
