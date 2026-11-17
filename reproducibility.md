# 計算・図表・テストの再現

Python 3.12で確認しています。プロジェクトのルートディレクトリで実行します。GitHub上ではREADME・CSV・SVGを読めます。PNGはフォントがなくても閲覧できます。

## 環境

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

作図にはIPA GothicかNoto Sans CJK JPが必要です。Debian/Ubuntuなら`fonts-ipafont-gothic`等のパッケージを利用できます。既存フォントは同梱していません。SVGは文字を輪郭にしているため、配布された図は閲覧者側の日本語フォントに依存しません。タイトルと代替説明をSVGに付けています。

## 公開CSVから図を再作成する

この操作は元のPDF・Excelも通信も必要ありません。

```bash
.venv/bin/python scripts/charts.py
.venv/bin/python -m pytest -q
```

通常のテストは同梱データの算術、既知の原表値、欠損、原表不一致、ライセンス表示、リンク、公開対象への機密・キャッシュ混入等を確認します。第三者の原資料を取らなければ、元PDFの全行を再抽出する確認は実施していません。

## 物価調整も原資料から計算し直す

[利用条件と元URL](sources.md)を確認して、Allen (2007)のPDFを作業用`_private/allen_2007.pdf`へ取得します。取得補助コードは指定PDFだけを取得し、既存ファイルを上書きしません。

```bash
.venv/bin/python scripts/fetch_source.py --allen
.venv/bin/python scripts/process.py --allen-pdf _private/allen_2007.pdf
.venv/bin/python scripts/charts.py
.venv/bin/python -m pytest -q --allen-pdf _private/allen_2007.pdf
```

元のExcelも取得した場合、AllenのCPI全100値と英国銀行A47列BLを同時に照合できます。

```bash
.venv/bin/python scripts/process.py \
  --allen-pdf _private/allen_2007.pdf \
  --boe-xlsx _private/boe_millennium.xlsx
```

物価指数が欠けた年を補間して計算することはありません。入力元を指定しない実質化も拒否します。`data/calculation_record.json`に入力ハッシュと計算式を残し、読者のファイルパスは書き込みません。元PDFの版が変わり抽出できない場合は失敗させ、図から推測した値で自動代替しません。

CSVの丸めによる保存誤差は許容し、同じ値が再計算されることを確認します。図の数値の再現と、PNGの画素単位での一致は異なります。Matplotlibやフォントの版により画像の外観は変わりえます。

## ファイル一覧と公開ZIP

```bash
.venv/bin/python scripts/package_public.py --output research_industrial_revolution_public.zip
```

この処理は公開用ファイルを明示的に選び、一覧とSHA-256を更新します。ZIPに元PDF・Excel・個人データ・秘密設定・原稿全文・仮想環境・キャッシュを含めません。ZIPを作るだけで、Webへのアップロード、GitHubへのpush、外部への連絡は行いません。人間の最終確認事項は[publication_review.md](publication_review.md)にあります。
