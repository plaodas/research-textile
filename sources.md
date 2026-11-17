# 出典・来歴・再配布の判断

取得・閲覧・利用条件の確認日：**2026-11-17（JST）**。原資料の掲載数値、後世の推計、今回の独自計算を区別します。取得したPDF・Excel・HTML・OCR・第三者の図そのものは、公開パッケージに含めません。各資料へのリンクを示します。元ファイルを区別するSHA-256は[third_party/source_downloads.json](third_party/source_downloads.json)にあります。

## 直接計算に使用した資料

### WOOD1910

George Henry Wood (1910), “The Statistics of Wages in the Nineteenth Century. Part XIX.—The Cotton Industry. Section V. Changes in the Average Wage of all Employed, with some Account of the Forces Operating to Accelerate or Retard the Progress of the Industry”, *Journal of the Royal Statistical Society*, 73(6), 585–626. [DOI: 10.1111/j.2397-2335.1910.tb00193.x](https://doi.org/10.1111/j.2397-2335.1910.tb00193.x)、[出版社書誌](https://academic.oup.com/jrsssa/article/73/6/585/7092079)、[閲覧したスキャン](https://zenodo.org/records/1941698/files/article.pdf)。

- 使用箇所：表40 p.596（PDF p.13）、表41 pp.598–599（PDF pp.15–16）。仮定と除外範囲の説明pp.593–597。
- 数値の性質：1910年の遡及推計。当時の議会資料、Baines、Ellison、工場監督官Returns等をまとめたもので、各年の直接全数調査ではない。年の間の補間を含む。
- 公開内容：原数値の独自転記CSV、加算等の独自計算、独自の図。原表の掲載合計・平均と不一致を保持。
- 権利の確認：[NZ国立図書館の典拠](https://natlib.govt.nz/records/22398125)は著者を1874–1945とする。[英国政府の通常の期間の説明](https://www.gov.uk/copyright/how-long-copyright-lasts)では文章は著者死後70年。本資料では古い原著の数値の転記を公開対象とし、取得スキャン上のJSTOR等の条件まで消滅したとは扱わない。PDF・ページ画像・組版は再配布しない。公開主体による管轄・利用形態の最終確認は残る。

### BAINES1835

Edward Baines (1835), *History of the Cotton Manufacture in Great Britain*. London: H. Fisher, R. Fisher, and P. Jackson. [閲覧した原本スキャン](https://archive.org/download/cottonmanufact00bain/cottonmanufact00bain.pdf)、[所蔵・公開表示](https://commons.wikimedia.org/wiki/File:Edward_Baines,_History_of_the_cotton_manufacture,_1835.pdf)。DOIは確認できていない。

- 使用箇所：p.240（PDF p.290）の製造業者による作業比較例。関連する機械化の記述pp.235–237。
- 数値の性質：同時代の説明だが、著者に製造業者が提供した例。全産業を調査した生産性統計ではない。手織比較例の年は明記されない。
- 公開内容：記述数値の転記、人数で除した独自計算。原文や画像の長い転載はしない。
- 権利の確認：公開表示は1835年刊の原著について米国のpublic domainとする。スキャン提供者・管轄の違いは別に扱い、原本PDF・画像は同梱しない。

### ALLEN2007

Robert C. Allen (2007), *Pessimism Preserved: Real Wages in the British Industrial Revolution*. University of Oxford, Department of Economics, Economics Series Working Papers 314. [機関公開PDF](https://www.nuffield.ox.ac.uk/media/2166/allen-pessimism-6.pdf)、[Oxford Research Archive書誌](https://ora.ox.ac.uk/objects/uuid:1660bc3a-01c9-4560-9054-f2e57d119e50)。DOIは確認できていない。

- 使用箇所：Appendix I, 印刷p.36／PDF p.37、1770〜1869年の生活費指数。公開版計算は1806〜1862年を使用。
- 数値の性質：後世の学術研究による価格指数。今回の独自調査による当時の価格ではない。
- 公開内容：この指数を入力として独自に計算した実質賃金の結果と独自描画。CPI原表そのもの、原論文、原図、OCRは同梱しない。読者が原資料を別途取得して再現する。
- 権利の確認：PDFにCC等の明示的な再配布許諾を確認できず、Oxfordの書誌はリポジトリ利用条件を示す。**元のCPI表を自由に再配布できるとは判断しない。** 独自指数結果へのライセンスは元表の権利を移転しない。加工結果の公開範囲も公開主体が最終確認する。

### BOE

Ryland Thomas & Nicholas Dimsdale (2017), *A Millennium of Macroeconomic Data for the UK*, Version 3.1, Bank of England. [機関の案内](https://www.bankofengland.co.uk/statistics/research-datasets)、[Excel](https://www.bankofengland.co.uk/-/media/boe/files/statistics/research-datasets/a-millennium-of-macroeconomic-data-for-the-uk.xlsx)。案内のデータ更新終点は2016年で、今回の取得年とは異なる。

- 使用箇所：A47. Wages and prices、列BL（Allen 2007 CPI）。既存調査では1770〜1869年の100値をAllen原論文と照合した。公開版スクリプトには別途取得したExcelとの照合オプションを残す。
- 数値の性質：複数研究を編纂・接続したデータ集。英国銀行自身による1800年代の直接観測ではない。
- 公開内容：ダウンロード先・ハッシュ・抽出コード。Excel、CPI全表、全国23系列の抽出一式は今回の公開版には含めない。
- 権利の確認：[英国銀行の条件](https://www.bankofengland.co.uk/legal)は一般資料とDatabase部分を区別し、第三者著作物の権利を留保する。DatabaseのOGLをこの研究Excelの全系列に一律適用しない。

## 解釈・ファクトチェックに使用した資料

### AJ2024

Daron Acemoglu & Simon Johnson (2024), *Learning from Ricardo and Thompson: Machinery and Labor in the Early Industrial Revolution, and in the Age of AI*, April 26, 2024, MIT Shaping the Future of Work Initiative. [指定版PDF](https://shapingwork.mit.edu/wp-content/uploads/2024/04/Acemoglu_Johnson_April-2024.pdf)。今回確認した版のDOIは特定していない。

使用箇所は図1・3・4、表2、pp.13, 38付近の工場賃金の説明とその出典。数値の元はWoodやAllen等であり独立な観測ではない。再配布ライセンスは未確認。PDF・図は同梱せず、本文との相違の説明とリンクのみ。

### SUGDEN2025

Keith Sugden & Amy Louise Erickson, “Estimating the Number of Cotton Handloom Weavers in England, c.1780–1813: Women and Children Hiding in Plain Sight”, *Textile History*, 54(2), 182–203. 巻年2023、オンライン公表2025-01-30。[DOI: 10.1080/00404969.2024.2437180](https://doi.org/10.1080/00404969.2024.2437180)、[大学公開版](https://api.repository.cam.ac.uk/server/api/core/bitstreams/17c8f1ae-e861-4d57-ab90-ac16f5d4d52d/content)。

表6と周辺本文、原数値の根拠に関する説明を使用。洗礼簿・人口推計等による後世の再構成で、手織工全員が成人男性ではないという留保の根拠。PDFにはCC BY 4.0の明示があるが、このパッケージではPDF・図を再配布せずリンクする。

### LANE2026

Tom Lane, Harry Pickard, Matthew J. Walker & Timo Heinrich (2026), *A Silver Lining? Consumer Preferences Over Human-Made and AI-Generated Production in Two Domains*. Creative PEC Discussion Paper Series, September 2026. [DOI: 10.5281/zenodo.22111802](https://doi.org/10.5281/zenodo.22111802)、[公式紹介](https://pec.ac.uk/discussion_paper_/consumer-preferences-human-made-ai-generated-production/)、[原論文](https://pec.ac.uk/wp-content/uploads/2026/09/AI-Discussion-Paper-09.26.pdf)。

使用箇所：印刷pp.17–24、32–40、44–45、Table 2・3、Figure 4・5、Appendix E/F。研究者による実験の公表結果で、歴史推計ではない。個票の再分析はしていない。

同日の[Creative PEC利用条件](https://pec.ac.uk/terms/)は、別段の表示がない資料にCC BY-NC-SA 4.0を示す。商用利用の自由を含むCC BYやCC0に付け替えない。本資料には書誌・数値事実への独自の説明だけを掲載し、原論文・原図・実験刺激・スクリーンショットは配布しない。商用サイトで原図等を使用したい場合は別途検討が必要。

### 追跡データへの案内

Kevin Schürer, Edward Higgs & FINDMYPAST LIMITED (2026カタログ引用表記；第2版の再寄託は2024), *Integrated Census Microdata (I-CeM), 1851–1911*, UK Data Service SN7481。[公式カタログ](https://datacatalogue.ukdataservice.ac.uk/studies/study/7481)、[DOI](https://doi.org/10.5255/UKDA-SN-7481-3)。2026-11-17閲覧。個票を取得したのではなく、必要資料の案内として使用。通常版はsafeguarded、氏名・住所は別ライセンス。個人データは公開しない。

## 今回の公開版で外したもの

既存の私的レビュー用アーカイブには、原本PDF、Excel、OCR全文、原表ページ画像、全国系列などが含まれていました。**それらのアーカイブは公開用ZIPではありません。** 公開版には、本文の中心的な主張に必要な独自の転記・計算結果・図とコードを選びました。元の調査結論を黙って修正したものではなく、再配布対象を絞った構成変更です。

Allen（2017）・Harleyの価格表・AJの輸入表・Tilly等の補助資料の数値一式は本公開版では再掲しません。これらの原資料を使う場合には独自の出典と条件確認が必要です。
