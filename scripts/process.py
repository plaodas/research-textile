# SPDX-License-Identifier: MIT
"""Reproduce public results from historical transcriptions and a separately obtained CPI.

No interpolation. The Allen source PDF or BoE workbook is supplied by the reader and
is never copied into the public data directory. Paths are relative to this project.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
INPUTS = DATA / 'inputs'


def index100(values, base_year=1806):
    base = values.loc[base_year]
    if pd.isna(base) or base <= 0:
        raise ValueError('Base year must be present and positive')
    return 100 * values / base


def read_allen_pdf(path):
    from pypdf import PdfReader
    pages = PdfReader(path).pages
    matches = [p.extract_text(extraction_mode='layout') for p in pages
               if 'Appendix I: The New Consumer Price Index' in p.extract_text()]
    # Whitespace differs between PDF extraction versions; the title and the numbers
    # are checked without relying only on a page position.
    if not matches:
        matches = [p.extract_text(extraction_mode='layout') for p in pages
                   if '117.7' in p.extract_text() and '115.6' in p.extract_text()]
    if len(matches) != 1:
        raise ValueError('Cannot unambiguously locate Allen Appendix I')
    pairs = re.findall(r'\b(1[78]\d{2})\s+(\d+\.\d+)\b', matches[0])
    if len(pairs) != 100 or len({y for y, _ in pairs}) != 100:
        raise ValueError('Expected exactly 100 distinct published CPI values')
    return pd.Series({int(y): float(v) for y, v in pairs}).sort_index()


def read_boe(path):
    import openpyxl
    book = openpyxl.load_workbook(path, read_only=True, data_only=True)
    return pd.Series({int(row[0]): row[63] for row in book['A47. Wages and prices'].values
                      if isinstance(row[0], (int, float)) and 1770 <= row[0] <= 1869}).sort_index()


def employment():
    w = pd.read_csv(INPUTS/'wood_table41_transcription.csv').set_index('year')
    if w.index.tolist() != list(range(1806, 1863)):
        raise ValueError('Wood transcription must have 57 consecutive source rows')
    e = pd.DataFrame(index=w.index)
    e['factory_people'] = w.factory_employment_thousands * 1000
    e['handloom_people'] = w.handloom_employment_thousands * 1000
    e['combined_people'] = e.factory_people + e.handloom_people
    e['published_total_people'] = w.published_total_thousands * 1000
    e['factory_change_from_1831'] = e.factory_people - e.loc[1831, 'factory_people']
    e['handloom_change_from_1831'] = e.handloom_people - e.loc[1831, 'handloom_people']
    e['combined_change_from_1831'] = e.combined_people - e.loc[1831, 'combined_people']
    e['source_id'] = 'WOOD1910'
    e['source_table'] = '41'
    e['estimate_note'] = 'Retrospective estimates; includes source interpolation; not linked workers'
    return w, e


def wages(w, cpi):
    cpi = cpi.reindex(w.index)
    if cpi.isna().any() or (cpi <= 0).any():
        raise ValueError('Missing/nonpositive CPI: refuse to interpolate')
    r = pd.DataFrame(index=w.index)
    r['handloom_real_index'] = index100(w.handloom_weekly_pence / cpi)
    r['factory_real_index'] = index100(w.factory_weekly_pence / cpi)
    mean = ((w.factory_employment_thousands*w.factory_weekly_pence
             + w.handloom_employment_thousands*w.handloom_weekly_pence)
            / (w.factory_employment_thousands+w.handloom_employment_thousands))
    r['weighted_real_index'] = index100(mean / cpi)
    r['wage_source_id'] = 'WOOD1910'
    r['price_source_id'] = 'ALLEN2007'
    r['base_year'] = 1806
    r['estimate_note'] = 'Own computed index; changing worker composition; national CPI approximation'
    return r


def productivity():
    p = pd.read_csv(INPUTS/'baines_productivity_transcription.csv')
    p['yards_per_piece'] = 24
    p['pieces_per_described_person_low'] = p.pieces_per_week_low / p.workers_in_description
    p['pieces_per_described_person_high'] = p.pieces_per_week_high / p.workers_in_description
    p['ratio_to_handloom_per_person_low'] = p.pieces_per_described_person_low / 2
    p['ratio_to_handloom_per_person_high'] = p.pieces_per_described_person_high / 2
    return p


def discrepancies(w, e):
    rows = []
    for y in e.index:
        if e.loc[y, 'combined_people'] != e.loc[y, 'published_total_people']:
            rows.append(dict(year=y,issue='table41_addition',
                             value_a=e.loc[y, 'published_total_people'],
                             value_b=e.loc[y, 'combined_people'],unit='people',
                             treatment='Preserve published value; explicitly sum components'))
    t = pd.read_csv(INPUTS/'wood_table40_transcription.csv').set_index('year')
    for y in t.index.intersection(w.index):
        if t.loc[y, 'handloom_thousands'] != w.loc[y, 'handloom_employment_thousands']:
            rows.append(dict(year=y,issue='table40_vs_table41_handloom',
                             value_a=t.loc[y,'handloom_thousands']*1000,
                             value_b=w.loc[y,'handloom_employment_thousands']*1000,unit='people',
                             treatment='Do not splice; annual analysis uses table41'))
    return pd.DataFrame(rows)


def key_numbers(e, r):
    rows=[]
    for y in [1806, 1820, 1831, 1847, 1850, 1859, 1862]:
        for measure in ['factory_people','handloom_people','combined_people']:
            rows.append(dict(year=y,measure=measure,value=e.loc[y,measure],unit='people',
                             source_ids='WOOD1910',calculation='Wood Table41 component sum for combined'))
        for measure in ['handloom_real_index','factory_real_index','weighted_real_index']:
            rows.append(dict(year=y,measure=measure,value=r.loc[y,measure],unit='index_1806_100',
                             source_ids='WOOD1910;ALLEN2007',calculation='100*(nominal/CPI)/(nominal1806/CPI1806)'))
    base=e.loc[1831,'combined_people']
    below=e.loc[1832:1858,'combined_people']
    crossed=e.loc[1832:,'combined_people']
    first=int(crossed[crossed>base].index[0])
    assert (below<base).all()
    rows.append(dict(year=first,measure='years_from_1831_to_first_strict_recross',value=first-1831,
                     unit='years_in_reconstruction',source_ids='WOOD1910',calculation='1859-1831; not an unemployment duration'))
    return pd.DataFrame(rows)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--allen-pdf', type=Path)
    parser.add_argument('--boe-xlsx', type=Path)
    args=parser.parse_args()
    if not args.allen_pdf and not args.boe_xlsx:
        parser.error('Supply --allen-pdf or --boe-xlsx. See reproducibility.md; no source PDF is redistributed.')
    source=args.allen_pdf or args.boe_xlsx
    cpi=read_allen_pdf(args.allen_pdf) if args.allen_pdf else read_boe(args.boe_xlsx)
    if args.allen_pdf and args.boe_xlsx:
        other=read_boe(args.boe_xlsx)
        pd.testing.assert_series_equal(cpi.astype(float),other.astype(float),check_names=False)
    w,e=employment()
    r=wages(w,cpi)
    e.to_csv(DATA/'employment.csv')
    r.to_csv(DATA/'real_wages.csv',float_format='%.12g')
    productivity().to_csv(DATA/'productivity_examples.csv',index=False,float_format='%.12g')
    discrepancies(w,e).to_csv(DATA/'source_discrepancies.csv',index=False)
    key_numbers(e,r).to_csv(DATA/'key_numbers.csv',index=False,float_format='%.12g')
    # Store source hash and type only; omit reader-specific filesystem paths.
    record={'input_source':'ALLEN2007' if args.allen_pdf else 'BOE',
            'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'price_series':'Allen2007 Appendix I; BoE A47 BL equivalent',
            'new_interpolation':False,'individual_worker_linkage':False,
            'years': [1806,1862],'wage_formula':'100*(nominal_t/CPI_t)/(nominal_1806/CPI_1806)'}
    (DATA/'calculation_record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    print('Reproduced employment, real wages, productivity examples and key numbers; no new interpolation.')


if __name__=='__main__':
    main()
