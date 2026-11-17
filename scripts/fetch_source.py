# SPDX-License-Identifier: MIT
"""Reader-side retrieval into an excluded private directory; no publishing actions."""
from pathlib import Path
import argparse
import hashlib
import json
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
URL='https://www.nuffield.ox.ac.uk/media/2166/allen-pessimism-6.pdf'


def main():
    parser=argparse.ArgumentParser(description='Read third_party/README.md before retrieving third-party sources.')
    parser.add_argument('--allen', action='store_true',required=True)
    args=parser.parse_args()
    private=ROOT/'_private'
    private.mkdir(exist_ok=True)
    path=private/'allen_2007.pdf'
    if path.exists():
        raise SystemExit('Source already exists; refusing to overwrite it.')
    with urllib.request.urlopen(urllib.request.Request(URL,headers={'User-Agent':'Mozilla/5.0 (research reproduction)'}),timeout=60) as response:
        content=response.read()
    if not content.startswith(b'%PDF'):
        raise ValueError('URL did not return a PDF; do not substitute another source silently')
    path.write_bytes(content)
    expected=[r['sha256'] for r in json.loads((ROOT/'third_party/source_downloads.json').read_text()) if r['source_id']=='ALLEN2007'][0]
    matched=hashlib.sha256(content).hexdigest()==expected
    print('Source stored in excluded _private directory. Matches research snapshot:',matched)
    if not matched:
        print('Source version differs; inspect the document and the appendix before treating results as a replication.')


if __name__=='__main__':
    main()
