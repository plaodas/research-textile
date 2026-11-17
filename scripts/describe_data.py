# SPDX-License-Identifier: MIT
"""Generate column definitions; fail if a public numerical column is undocumented."""
from pathlib import Path
import csv

ROOT=Path(__file__).resolve().parents[1]
FILES={
 'data/inputs/wood_table41_transcription.csv':'Wood1910 Table41; transcribed retrospective estimates',
 'data/inputs/wood_table40_transcription.csv':'Wood1910 Table40; separately transcribed benchmarks',
 'data/inputs/baines_productivity_transcription.csv':'Baines1835 p240; manufacturer examples',
 'data/employment.csv':'Wood1910 Table41; process.employment; original source interpolation retained',
 'data/real_wages.csv':'Wood1910 and Allen2007; process.wages; derived indices, no CPI source table redistributed',
 'data/productivity_examples.csv':'Baines1835 p240; process.productivity; simple division by described people',
 'data/source_discrepancies.csv':'Wood1910 Table40/41; process.discrepancies',
 'data/key_numbers.csv':'process.key_numbers; selection and arithmetic from public outputs',
}
DEFINITIONS={
 'year':('西暦年。年不明の手織比較例では空欄','year'),
 'date_label':('作業例のラベル。undatedは年不明','label'),
 'factory_employment_thousands':('工場で紡績・織布等に従事する人数の原推計','thousand_people'),
 'factory_weekly_pence':('工場就業者の平均名目週賃金の原推計','old_pence_per_week'),
 'handloom_employment_thousands':('手織工人数の原推計','thousand_people'),
 'handloom_weekly_pence':('手織工の平均名目週賃金の原推計','old_pence_per_week'),
 'published_total_thousands':('表41掲載の二群合計。内訳との不一致もそのまま保持','thousand_people'),
 'published_mean_pence':('表41掲載の丸められた平均名目週賃金','old_pence_per_week'),
 'factory_spinning_thousands':('表40掲載の工場紡績人数','thousand_people'),
 'factory_weaving_thousands':('表40掲載の工場織布人数。fewは空欄','thousand_people'),
 'factory_total_thousands':('表40掲載の工場合計人数','thousand_people'),
 'handloom_thousands':('表40掲載の手織工人数。表41と接続しない','thousand_people'),
 'weaving_missing_reason':('few_not_numericまたはnot_reported。空欄は補足理由なし','text'),
 'factory_people':('工場人数の原推計を1000倍','people'),
 'handloom_people':('手織工人数の原推計を1000倍','people'),
 'combined_people':('factory_peopleとhandloom_peopleの和','people'),
 'published_total_people':('表41の掲載合計を1000倍。独自加算列とは区別','people'),
 'factory_change_from_1831':('各年の工場人数から1831年187000人を引く','people'),
 'handloom_change_from_1831':('各年の手織人数から1831年240000人を引く','people'),
 'combined_change_from_1831':('各年の二群人数から1831年427000人を引く','people'),
 'source_id':('原資料コード。BAINESはBAINES1835の取得時表記','source_identifier'),
 'source_table':('使用した原表の番号','table_identifier'),
 'estimate_note':('推計・独自計算・個人追跡の有無に関する注記','text'),
 'handloom_real_index':('手織名目週賃金をAllen CPIで除し1806年100に基準化','index_1806_100'),
 'factory_real_index':('工場名目週賃金をAllen CPIで除し1806年100に基準化','index_1806_100'),
 'weighted_real_index':('二群人数で重み付けした名目平均を実質化し1806年100に基準化','index_1806_100'),
 'wage_source_id':('名目賃金の原資料','source_identifier'),
 'price_source_id':('生活費指数の原資料','source_identifier'),
 'base_year':('指数の基準年1806。群間の絶対賃金額を同一視しない','year'),
 'technology':('handloomは手織、powerloomは機械織','category'),
 'pieces_per_week_low':('記述されたチームの週産出の下限。統計的区間ではない','24yard_pieces_per_team_week'),
 'pieces_per_week_high':('記述されたチームの週産出の上限。統計的区間ではない','24yard_pieces_per_team_week'),
 'looms_tended':('記述された織機の台数','looms'),
 'workers_in_description':('記述された作業者と助手の人数。全工程人数ではない','people'),
 'age_description':('原記述の年齢条件の要約','text'),
 'printed_page':('原著の印刷ページ。PDF通しページとは異なる','page_number'),
 'yards_per_piece':('この比較例での1反24ヤード','yards_per_piece'),
 'pieces_per_described_person_low':('週産出下限を記述人数で割る。労働時間未調整','pieces_per_described_person_week'),
 'pieces_per_described_person_high':('週産出上限を記述人数で割る。労働時間未調整','pieces_per_described_person_week'),
 'ratio_to_handloom_per_person_low':('1人当たり産出下限を手織の2反で割る','ratio'),
 'ratio_to_handloom_per_person_high':('1人当たり産出上限を手織の2反で割る','ratio'),
 'issue':('加算不一致または表40/41の人数相違','category'),
 'value_a':('加算問題では表41掲載値、表間問題では表40の値','people'),
 'value_b':('加算問題では内訳和、表間問題では表41の値','people'),
 'unit':('同じ行のvalue列に使う単位','unit_identifier'),
 'treatment':('不一致を保持する処置の説明','text'),
 'measure':('元の出力列名、または1831年からの再到達年差の識別子','measure_identifier'),
 'value':('measureに対応する値。単位は同じ行のunit列','see_unit_column'),
 'source_ids':('使用した原資料コード。セミコロン区切り','source_identifiers'),
 'calculation':('選択・算術の説明。28年は1859-1831','text'),
}


def main():
    rows=[]
    for filename,provenance in FILES.items():
        with (ROOT/filename).open(newline='') as f:
            columns=next(csv.reader(f))
        for col in columns:
            desc,unit=DEFINITIONS[col]
            rows.append(dict(file=filename,column=col,definition_ja=desc,unit=unit,
                             missing='Empty means missing/not applicable; never zero-filled; see data README',
                             provenance=provenance))
    for col,definition in [('file','定義対象のCSV相対名'),('column','定義対象の列名'),('definition_ja','日本語定義'),
                           ('unit','単位'),('missing','欠損の意味と処置'),('provenance','原資料と計算の経路')]:
        rows.append(dict(file='data/data_dictionary.csv',column=col,definition_ja=definition,unit='text',
                         missing='No missing values expected',provenance='Own metadata; describe_data.py'))
    with (ROOT/'data/data_dictionary.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['file','column','definition_ja','unit','missing','provenance'])
        writer.writeheader()
        writer.writerows(rows)
    print('Documented',len(rows),'CSV columns.')


if __name__=='__main__':
    main()
