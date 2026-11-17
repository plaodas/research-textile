# Web掲載用の図

図はすべて独自描画、SVGとPNGです。元論文の図やページ画像を転載・加工していません。図中に対象・推計であること・出典を記載しています。SVGは日本語文字の輪郭を含み、タイトル・説明の代替テキストも持ちます。フォントファイル自体は同梱していません。

| 図 | 元データ | Web掲載時の代替テキスト |
|---|---|---|
| [01 雇用人数 SVG](01_employment.svg) ／ [PNG](01_employment.png) | [employment.csv](../data/employment.csv) | Woodの推計では、1831年から1859年に手織工は24万人から1万3千人、工場は18万7千人から41万5千人に変化。本人の転職を追ったものではない |
| [02 実質賃金 SVG](02_real_wages.svg) ／ [PNG](02_real_wages.png) | [real_wages.csv](../data/real_wages.csv) | 各群1806年100。手織工は1820年42.0、1850年43.5、工場は104.3、126.5。異なる就業者群の平均である |
| [03 雇用の回復と手織工 SVG](03_employment_comparison.svg) ／ [PNG](03_employment_comparison.png) | [employment.csv](../data/employment.csv) | 1859年は1831年比で工場22万8千人増、手織工22万7千人減、合計千人増。個人の再就職は分からない |
| [04 生産性の例 SVG](04_productivity.svg) ／ [PNG](04_productivity.png) | [productivity_examples.csv](../data/productivity_examples.csv) | Bainesの例は手織1人週2反、1833年機械織2人で週18〜20反。人数で割ると1人9〜10反。産業平均ではない |

「産業全体の雇用規模と手織工の比較」という依頼に対し、統計の対象範囲を正確にするため図3は「二群合計」と表示しました。全産業の人数に改称していません。各群の指数の差を、2群の賃金額の比と読むこともできません。

図4の棒上の線は原文に記された産出の範囲で、統計的な信頼区間ではありません。手織比較例の年が不明であること、年齢や労働時間をそろえた比較ではないことを併記しています。

ライセンスは独自描画部分に[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。元のデータ出典も保持してください。掲載画面では画像の下に本文や注記を添え、注記を落とした切り抜きを避けてください。作図コードは[scripts/charts.py](../scripts/charts.py)、図の機械可読メタデータは[manifest.json](manifest.json)。
