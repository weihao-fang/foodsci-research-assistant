"""Create a new public repository after explicit execution and GitHub CLI login."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def run(args, capture=False):
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=capture, encoding='utf-8')
    if result.returncode:
        raise RuntimeError(f'Command failed: {args[0]} {args[1]}. Inspect its result before retrying; repository creation may already have occurred.')
    return result.stdout if capture else ''

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true', help='Actually create and push a PUBLIC repository')
    parser.add_argument('--name', default='foodsci-research-assistant')
    args = parser.parse_args()
    if not args.execute:
        print('Dry run: validate local source; check GitHub CLI login; create local initial commit if needed; create a new PUBLIC repository and push. No external action performed.')
        return
    if not shutil.which('gh') or not shutil.which('git'):
        raise RuntimeError('Install Git and official GitHub CLI, then run gh auth login --web --scopes workflow first.')
    run([sys.executable, '-B', 'tools/validate.py'])
    user = json.loads(run(['gh', 'api', 'user'], capture=True))
    login = user['login']
    remote = subprocess.run(['git', 'remote', 'get-url', 'origin'], cwd=ROOT, capture_output=True)
    if remote.returncode == 0:
        raise RuntimeError('This directory already has an origin remote. Inspect it and use the normal Git update flow; no new repository created.')
    if not (ROOT / '.git').exists():
        run(['git', 'init', '--initial-branch=main'])
    head = subprocess.run(['git', 'rev-parse', '--verify', 'HEAD'], cwd=ROOT, capture_output=True)
    if head.returncode:
        run(['git', 'add', '.'])
        email = str(user['id']) + '+' + login + '@users.noreply.github.com'
        run(['git', '-c', 'user.name=' + login, '-c', 'user.email=' + email,
             'commit', '-m', 'Prepare FoodSci Research Assistant 0.7.0'])
    else:
        dirty = run(['git', 'status', '--porcelain'], capture=True)
        if dirty.strip():
            raise RuntimeError('Existing local history has uncommitted changes. Review and commit them before publishing.')
    run(['gh', 'repo', 'create', login + '/' + args.name, '--public', '--source', str(ROOT),
         '--remote', 'origin', '--push', '--description',
         'FoodSci: biology and food research skills for literature, experimental design, analysis, writing and review. Noncommercial learning and research.'])
    print('Created and pushed: https://github.com/' + login + '/' + args.name)

if __name__ == '__main__':
    try:
        main()
    except (OSError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
