# データの読み方

公開CSVはUTF-8、先頭行が列名、年は西暦です。Excelや表計算ソフトでも開けます。数値の単位は以下と[data_dictionary.csv](data_dictionary.csv)を参照してください。空欄は欠損で、0ではありません。後世の推計の転記と、今回の独自計算を区別します。

## ファイル

| CSV | 内容 | 行数 | 由来 |
|---|---|---:|---|
| [inputs/wood_table41_transcription.csv](inputs/wood_table41_transcription.csv) | 工場・手織の人数、週賃金、掲載合計と平均 | 57 | Wood表41 pp.598–599を転記。人数は千人、賃金はd/週 |
| [inputs/wood_table40_transcription.csv](inputs/wood_table40_transcription.csv) | 紡績・織布内訳と合計、手織工 | 18 | Wood表40 p.596。掲載年のみ |
| [inputs/baines_productivity_transcription.csv](inputs/baines_productivity_transcription.csv) | 4つの作業比較例 | 4 | Baines p.240。1反24ヤード |
| [employment.csv](employment.csv) | 人数を人単位に換算、二群を加算、1831年からの差を計算 | 57 | Wood表41を独自加工 |
| [real_wages.csv](real_wages.csv) | 手織、工場、雇用加重平均の実質指数 | 57 | Wood名目週賃金÷Allen CPI、各群1806＝100 |
| [productivity_examples.csv](productivity_examples.csv) | 記述された人数で割った生産量と比率 | 4 | Bainesの作業例を独自加工 |
| [source_discrepancies.csv](source_discrepancies.csv) | 表41の加算不一致3件と、表40/41の1850年相違 | 4 | 原表の相違を保持 |
| [key_numbers.csv](key_numbers.csv) | 指定7年の人数・実質指数と28年の算式 | 43 | 上記の出力から選択 |
| [data_dictionary.csv](data_dictionary.csv) | 公開CSVごとの全列の定義・単位・欠損・由来 | 列数による | 本資料の独自メタデータ |

`calculation_record.json`は計算式と入力ハッシュの記録。物価指数の原表・Excel本体は公開せず、別途取得した入力で再計算できます。すべての数値転記・独自結果に関する本資料作成者の権利はCC0。元の選択・編集等に第三者の権利が残る場合は別です。[ライセンス範囲](../LICENSE.md)

## 重要な列

- `factory_people`は紡績・織布等の工場労働者、`handloom_people`は手織工、`combined_people`は両者の和。単位は人。
- `published_total_people`はWood表41の掲載合計を1,000倍したもの。不一致を消すための修正はしない。
- `*_change_from_1831`は同じ人数列から1831年値を引く。元手織工の転職数ではない。
- `*_real_index`は各群の1806年を100とする実質指数。群間の絶対賃金比較には使わない。
- 生産性の`pieces_per_week_low/high`は記述されたチームの週産出、`workers_in_description`はそのチームの人数。`pieces_per_described_person_*`は単純除算であり、時間調整はしない。
- 不一致の`value_a/b`は、加算問題では掲載合計／内訳和、表間問題では表40／表41。単位は人。
- `source_id`の取得時の旧表記`BAINES`は本文の`BAINES1835`、取得台帳の`WOOD`は`WOOD1910`と同じ資料。

## 算式

```text
人数（人） = 元の人数（千人） × 1,000
二群人数 = 工場人数 ＋ 手織工人数
二群平均名目賃金 = (工場人数×工場賃金 ＋ 手織人数×手織賃金) / 二群人数
実質指数(t) = 100 × [名目賃金(t)/CPI(t)] / [名目賃金(1806)/CPI(1806)]
1人当たり週産出 = 記述された週産出 / 記述された人数
手織例との比 = 1人当たり週産出 / 2反
回復までの年差 = 最初に1831年合計を厳密に上回る年 − 1831
```

## 欠損・丸め・補間

表40の`Few`、内訳がない年は数値欄を空欄にし、`weaving_missing_reason`に理由を残します。Bainesの手織比較例は年が不明なので`year`は空欄です。補助列の空欄は「特に欠損理由なし」を意味する場合があります。

新しい補間、前方補完、0埋め、別系列による自動代替はしません。ただしWood自身の原系列が補間・推計を含みます。CSVには浮動小数の保存精度があり、文書では小数2桁、図では一部小数1桁を使用します。生データの整数を丸めたわけではありません。

## 公開対象を絞った理由

私的調査で取得した全国23系列や原本PDF等の全再配布はしていません。コラムの中心的な計算を追える入力・出力だけを収録し、第三者のCPI原表は別取得としています。加工したことだけを理由に第三者の権利が消えるとは扱っていません。
