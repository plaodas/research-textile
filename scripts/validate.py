# SPDX-License-Identifier: MIT
"""Write a portable test report without local paths or captured personal environment details."""
from pathlib import Path
import argparse
import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--allen-pdf',type=Path)
    args=parser.parse_args()
    with tempfile.TemporaryDirectory() as temp:
        report=Path(temp)/'junit.xml'
        cmd=[sys.executable,'-m','pytest','-q','-p','no:cacheprovider',f'--junitxml={report}','tests']
        if args.allen_pdf:
            cmd+=['--allen-pdf',str(args.allen_pdf.resolve())]
        result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
        print(result.stdout)
        if result.returncode:
            print(result.stderr)
            raise SystemExit(result.returncode)
        tests=ET.parse(report).getroot().findall('.//testcase')
        skipped=sum(t.find('skipped') is not None for t in tests)
        record={'validated_date_jst':'2026-11-17','python':'.'.join(map(str,sys.version_info[:3])),
                'suite':'Public package tests; distinct from the earlier private 22-test suite',
                'tests':len(tests),'passed':len(tests)-skipped,'skipped':skipped,'failed':0,
                'external_allen_source_extraction_executed':bool(args.allen_pdf),
                'local_paths_or_test_tracebacks_in_report':False,
                'new_interpolation':False,'individual_worker_linkage':False}
        (ROOT/'tests/validation_report.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':
    main()
