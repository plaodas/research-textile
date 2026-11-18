# SPDX-License-Identifier: MIT
"""Allowlisted publication package. No upload, git operations, or automatic external contact."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import zipfile

ROOT=Path(__file__).resolve().parents[1]
TOP={'PUBLICATION_DECISIONS.md','.gitignore','README.md','findings.md','sources.md','limitations.md',
     'article_factcheck.md','ai_evidence.md','publication_review.md','reproducibility.md',
     'LICENSE.md','LICENSE-CODE','requirements.txt','PUBLIC_FILES.md','publication_manifest.json'}
DATA={'data/README.md','data/data_dictionary.csv','data/employment.csv','data/real_wages.csv',
      'data/productivity_examples.csv','data/source_discrepancies.csv','data/key_numbers.csv',
      'data/calculation_record.json','data/inputs/wood_table41_transcription.csv',
      'data/inputs/wood_table40_transcription.csv','data/inputs/baines_productivity_transcription.csv'}
SCRIPTS={f'scripts/{n}.py' for n in ['process','charts','fetch_source','describe_data','package_public','validate']}
TESTS={'tests/conftest.py','tests/test_public.py','tests/README.md','tests/validation_report.json'}
OTHER={'third_party/README.md','third_party/source_downloads.json','charts/README.md','charts/manifest.json'}
OTHER|={f'charts/{n}.{ext}' for n in ['01_employment','02_real_wages','03_employment_comparison','04_productivity'] for ext in ['svg','png']}
ALLOWED=TOP|DATA|SCRIPTS|TESTS|OTHER
GENERATED={'PUBLIC_FILES.md','publication_manifest.json'}
EXCLUDED_PARTS={'_private','.venv','__pycache__','.pytest_cache','.git','.aws','.codex','.agents'}


def audit_text(text):
    checks={
        'absolute_personal_or_temp_path':r'(?:[/]home[/]|[/]Users[/]|[/]tmp[/]|file:\x2f\x2f|[A-Za-z]:\\Users\\)',
        'private_key':r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',
        'aws_key_pattern':r'\bAKIA[0-9A-Z]{16}\b',
        'token_pattern':r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{30,})\b',
        'credential_assignment':r'(?i)(?:api_key|access_token|client_secret)\s*[:=]\s*[\"\x27][A-Za-z0-9_-]{16,}',
    }
    return [kind for kind,pattern in checks.items() if re.search(pattern,text)]


def public_files(require_generated=True):
    files=[]
    unexpected=[]
    for p in ROOT.rglob('*'):
        if not p.is_file():
            continue
        rel=p.relative_to(ROOT).as_posix()
        if set(p.relative_to(ROOT).parts)&EXCLUDED_PARTS or p.suffix in {'.pyc','.zip'}:
            continue
        if p.is_symlink():
            raise ValueError('Symlinks are not accepted in the public package')
        if rel not in ALLOWED:
            unexpected.append(rel)
        else:
            files.append(p)
    required=ALLOWED if require_generated else ALLOWED-GENERATED
    missing=required-{p.relative_to(ROOT).as_posix() for p in files}
    if unexpected or missing:
        raise ValueError(f'Publication allowlist mismatch. Unexpected={unexpected}; missing={sorted(missing)}')
    return sorted(files)


def audit(files):
    for p in files:
        if p.suffix!='.png':
            issues=audit_text(p.read_text())
            if issues:
                raise ValueError(f'Content audit failed for {p.relative_to(ROOT)}: {issues}')


def license_for(rel):
    if rel.endswith('.py'):
        return 'MIT'
    if rel.startswith('data/') and not rel.endswith('.md'):
        return 'CC0-1.0 on own contributions; source rights not relicensed'
    if rel in {'LICENSE-CODE','requirements.txt','.gitignore'}:
        return 'See LICENSE.md'
    return 'CC-BY-4.0 on own expression; source rights not relicensed'


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    validation=json.loads((ROOT/'tests/validation_report.json').read_text())
    if validation.get('failed') != 0 or validation.get('passed',0) <= 0:
        raise ValueError('A successful public test report is required before packaging')
    files=public_files(require_generated=False)
    names=sorted(ALLOWED)
    lines=['# 公開対象ファイル一覧\n\n',
           'この一覧のファイルだけを公開用ZIPに含めます。原PDF・Excel・OCR・原稿全文は含めません。\n\n',
           'SHA-256とサイズは[publication_manifest.json](publication_manifest.json)を参照してください。\n\n',
           '| ファイル | 適用範囲 |\n|---|---|\n']
    for rel in names:
        lines.append(f'| [{rel}]({rel}) | {license_for(rel)} |\n')
    (ROOT/'PUBLIC_FILES.md').write_text(''.join(lines))
    files=public_files(require_generated=False)
    records=[dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,
                  sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                  license=license_for(p.relative_to(ROOT).as_posix()))
             for p in files if p.name!='publication_manifest.json']
    (ROOT/'publication_manifest.json').write_text(json.dumps({
        'version':'2026-11-17','publication_status':'Research data and documentation package',
        'research_reference_date_jst':'2026-11-17','documentation_revision_date_jst':'2026-11-18',
        'files':records,'manifest_self_hash':'Excluded to avoid recursive hashing',
        'excluded_categories':['third-party PDFs and spreadsheets','OCR and source-page scans',
                               'private manuscript','credentials','personal paths','caches','virtual environments'],
    },ensure_ascii=False,indent=2)+'\n')
    files=public_files()
    audit(files)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(args.output,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in files:
            rel=p.relative_to(ROOT).as_posix()
            # A stable ZIP timestamp makes the archive reproducible from unchanged files.
            info=zipfile.ZipInfo('research_industrial_revolution_public/'+rel,(2026,11,17,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            z.writestr(info,p.read_bytes(),compresslevel=6)
    with zipfile.ZipFile(args.output) as z:
        if z.testzip() is not None:
            raise ValueError('ZIP integrity check failed')
        if len(z.namelist())!=len(files):
            raise ValueError('ZIP member count mismatch')
        for p in files:
            rel=p.relative_to(ROOT).as_posix()
            if z.read('research_industrial_revolution_public/'+rel)!=p.read_bytes():
                raise ValueError('ZIP contents differ from allowlisted file')
    print(f'Packaged {len(files)} allowlisted files. ZIP integrity and content checks passed.')


if __name__=='__main__':
    main()
