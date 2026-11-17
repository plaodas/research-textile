# SPDX-License-Identifier: MIT
from pathlib import Path
import csv
import importlib.util
import json
import re
import struct
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import pytest

ROOT=Path(__file__).resolve().parents[1]


def module(name):
    spec=importlib.util.spec_from_file_location('public_'+name,ROOT/'scripts'/f'{name}.py')
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@pytest.fixture(scope='module')
def e():
    return pd.read_csv(ROOT/'data/employment.csv').set_index('year')


@pytest.fixture(scope='module')
def w():
    return pd.read_csv(ROOT/'data/real_wages.csv').set_index('year')


def test_years_and_scope(e,w):
    assert e.index.tolist()==list(range(1806,1863))
    assert w.index.equals(e.index)
    assert e.source_id.eq('WOOD1910').all()
    assert e.estimate_note.str.contains('not linked').all()


def test_transcription_to_employment_and_nominal_weight(e):
    src=pd.read_csv(ROOT/'data/inputs/wood_table41_transcription.csv').set_index('year')
    assert np.array_equal(e.factory_people,1000*src.factory_employment_thousands)
    assert np.array_equal(e.handloom_people,1000*src.handloom_employment_thousands)
    assert np.array_equal(e.combined_people,e.factory_people+e.handloom_people)


@pytest.mark.parametrize('year,factory,hand,total',[(1831,187000,240000,427000),(1847,277000,53000,330000),(1859,415000,13000,428000)])
def test_article_employment_anchors(e,year,factory,hand,total):
    assert e.loc[year,'factory_people']==factory
    assert e.loc[year,'handloom_people']==hand
    assert e.loc[year,'combined_people']==total


def test_28_is_first_recross_not_worker_absorption(e):
    assert (e.loc[1832:1858,'combined_people']<427000).all()
    assert e.loc[1859,'combined_people']>427000
    assert 1859-1831==28
    assert 1859-1847==12
    assert e.loc[1859,'factory_change_from_1831']==228000
    assert e.loc[1859,'handloom_change_from_1831']==-227000
    assert e.loc[1859,'combined_change_from_1831']==1000


def test_source_errors_not_silently_fixed(e):
    issue=pd.read_csv(ROOT/'data/source_discrepancies.csv')
    assert set(issue[issue.issue=='table41_addition'].year)=={1818,1849,1857}
    assert e.loc[1849,'published_total_people']==350000
    assert e.loc[1849,'combined_people']==360000
    t=pd.read_csv(ROOT/'data/inputs/wood_table40_transcription.csv').set_index('year')
    assert t.loc[1850,'handloom_thousands']==40
    assert e.loc[1850,'handloom_people']==43000


def test_missing_values_not_zero_filled():
    t=pd.read_csv(ROOT/'data/inputs/wood_table40_transcription.csv').set_index('year')
    assert pd.isna(t.loc[1806,'factory_weaving_thousands'])
    assert t.loc[1806,'weaving_missing_reason']=='few_not_numeric'
    assert pd.isna(t.loc[1835,'factory_spinning_thousands'])
    p=pd.read_csv(ROOT/'data/productivity_examples.csv').set_index('date_label')
    assert pd.isna(p.loc['undated_handloom_reference','year'])


@pytest.mark.parametrize('year,cpi,hand_nom,factory_nom',[(1820,115.6,99,124),(1850,84.6,75,110),(1862,99.6,75,137)])
def test_real_wage_formula_independent_published_anchors(w,year,cpi,hand_nom,factory_nom):
    assert w.loc[year,'handloom_real_index']==pytest.approx(100*(hand_nom/cpi)/(240/117.7),rel=1e-10)
    assert w.loc[year,'factory_real_index']==pytest.approx(100*(factory_nom/cpi)/(121/117.7),rel=1e-10)


def test_rebased_means_and_counterevidence(w,e):
    for col in ['handloom_real_index','factory_real_index','weighted_real_index']:
        assert w.loc[1806,col]==100
    assert w.loc[1820,'factory_real_index']>100
    assert w.loc[1850,'factory_real_index']>100
    assert (w.loc[1807:,'handloom_real_index']<100).all()
    # Recombine each group's separately rebased real index, accounting for the
    # different 1806 nominal wages; this is not a simple mean of the index lines.
    mean1806=(90*121+184*240)/274
    expected=(e.factory_people*w.factory_real_index*121+e.handloom_people*w.handloom_real_index*240)/e.combined_people/mean1806
    assert np.allclose(w.weighted_real_index,expected,rtol=1e-10)


def test_productivity_assistant_and_ratios():
    p=pd.read_csv(ROOT/'data/productivity_examples.csv').set_index('date_label')
    assert p.loc['1833','workers_in_description']==2
    assert p.loc['1833','pieces_per_week_low']==18
    assert p.loc['1833','pieces_per_week_high']==20
    assert p.loc['1833','pieces_per_described_person_low']==9
    assert p.loc['1833','pieces_per_described_person_high']==10
    assert p.loc['1833','ratio_to_handloom_per_person_low']==4.5
    assert p.loc['1833','ratio_to_handloom_per_person_high']==5
    assert p.loc['1826','looms_tended']==2


def test_index_rejects_missing_or_invalid_input():
    m=module('process')
    with pytest.raises(ValueError):
        m.index100(pd.Series({1806:np.nan}))
    with pytest.raises(KeyError):
        m.index100(pd.Series({1807:100}))
    src,_=m.employment()
    with pytest.raises(ValueError):
        m.wages(src,pd.Series({1806:117.7}))


def test_key_numbers_match_public_outputs(e,w):
    k=pd.read_csv(ROOT/'data/key_numbers.csv')
    assert len(k)==43
    for r in k.itertuples():
        if r.measure=='years_from_1831_to_first_strict_recross':
            assert r.value==28
        else:
            assert r.value==pytest.approx((e if r.measure in e.columns else w).loc[r.year,r.measure],rel=1e-10)


def test_every_csv_column_has_definition():
    d=pd.read_csv(ROOT/'data/data_dictionary.csv')
    assert not d.duplicated(['file','column']).any()
    for p in (ROOT/'data').rglob('*.csv'):
        with p.open(newline='') as f:
            cols=next(csv.reader(f))
        defined=d[d.file==p.relative_to(ROOT).as_posix()]
        assert set(cols)==set(defined.column)
        assert defined.definition_ja.notna().all()
        assert defined.unit.notna().all()


def test_relative_links_exist():
    for p in ROOT.rglob('*.md'):
        if set(p.relative_to(ROOT).parts)&module('package_public').EXCLUDED_PARTS:
            continue
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if target.startswith(('https://','http://','#')):
                continue
            assert not target.startswith('/')
            assert (p.parent/target.split('#')[0]).exists(),(p.name,target)


def test_charts_have_captions_accessibility_and_valid_outputs():
    c=json.loads((ROOT/'charts/manifest.json').read_text())
    assert len(c)==4
    for item in c:
        assert '出典' in item['note']
        assert item['description'] and item['sources']
        svg=ET.parse(ROOT/'charts'/(item['file']+'.svg')).getroot()
        assert svg.attrib['role']=='img'
        ns='{http://www.w3.org/2000/svg}'
        assert svg.find(ns+'title').text
        assert svg.find(ns+'desc').text
        assert 'aria-labelledby' in svg.attrib
        raw=(ROOT/'charts'/(item['file']+'.png')).read_bytes()
        assert raw[:8]==b'\x89PNG\r\n\x1a\n'
        assert struct.unpack('>II',raw[16:24])[0]>=1200


def test_publication_allowlist_and_content_audit():
    pack=module('package_public')
    files=pack.public_files(require_generated=False)
    pack.audit(files)
    assert not any(p.suffix in {'.pdf','.xlsx','.html'} for p in files)
    assert not any('_private' in p.relative_to(ROOT).parts for p in files)


def test_licenses_and_source_qualification_present():
    for p in list((ROOT/'scripts').glob('*.py'))+list((ROOT/'tests').glob('*.py')):
        assert 'SPDX-License-Identifier: MIT' in p.read_text()
    text=(ROOT/'LICENSE.md').read_text()
    assert all(term in text for term in ['MIT','CC BY 4.0','CC0','第三者'])
    assert 'CC BY-NC-SA' in (ROOT/'sources.md').read_text()
    assert '検証不能' in (ROOT/'limitations.md').read_text()


def test_full_source_replication_if_reader_supplies_pdf(request,w):
    value=request.config.getoption('--allen-pdf')
    if not value:
        pytest.skip('No third-party source supplied; run with --allen-pdf for source extraction verification')
    m=module('process')
    cpi=m.read_allen_pdf(Path(value))
    assert len(cpi)==100
    assert set(cpi.index)==set(range(1770,1870))
    assert cpi.loc[1806]==117.7
    src,_=m.employment()
    reproduced=m.wages(src,cpi)
    for col in ['handloom_real_index','factory_real_index','weighted_real_index']:
        assert np.allclose(reproduced[col],w[col],rtol=1e-10)
