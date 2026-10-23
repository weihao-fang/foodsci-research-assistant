import importlib.util
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('foodsci_build', ROOT / 'tools/build.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

class PackageTests(unittest.TestCase):
    def test_rebuild_is_identical_and_packages_share_one_runtime(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            first = builder.build(ROOT, a)
            second = builder.build(ROOT, b)
            self.assertEqual(first, second)
            version = first['version']
            with ZipFile(Path(a) / f'foodsci-suite-{version}.zip') as z:
                entries = [n for n in z.namelist() if n.endswith('/SKILL.md')]
                self.assertEqual(len(entries), 6)
                self.assertEqual(sum(n.endswith('/scripts/analyze.py') for n in z.namelist()), 1)
            with ZipFile(Path(a) / f'foodsci-codex-{version}.zip') as z:
                self.assertEqual(sum(n.endswith('/SKILL.md') for n in z.namelist()), 1)
                self.assertIn('foodsci-research-assistant/LICENSE', z.namelist())
            with ZipFile(Path(a) / f'foodsci-plugin-{version}.zip') as z:
                self.assertFalse(any('/downloads/' in n or '/.git/' in n for n in z.namelist()))
            chat = (Path(a) / 'FoodSci-豆包聊天版.md').read_bytes()
            self.assertEqual(chat, (Path(a) / 'FoodSci-豆包聊天版.txt').read_bytes())
            for notice in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                self.assertIn((ROOT / notice).read_text(encoding='utf-8').strip(), chat.decode('utf-8').replace('\r\n', '\n'))
            with ZipFile(Path(a) / f'foodsci-doubao-chat-{version}.zip') as z:
                self.assertEqual(z.read('FoodSci-豆包聊天版.md'), chat)

if __name__ == '__main__':
    unittest.main()
