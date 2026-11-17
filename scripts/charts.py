# SPDX-License-Identifier: MIT
"""Create self-contained Japanese charts from public computed CSVs, not third-party images."""
from pathlib import Path
import json
import xml.etree.ElementTree as ET
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
OUT=ROOT/'charts'
PALETTE=['#007B83','#BA3E58','#5C4B99']


def setup_font():
    available={f.name for f in font_manager.fontManager.ttflist}
    family=next((f for f in ['IPAGothic','IPAPGothic','Noto Sans CJK JP','Noto Sans JP'] if f in available),None)
    if family is None:
        raise RuntimeError('Install a Japanese font (IPA Gothic or Noto Sans CJK JP); see reproducibility.md.')
    plt.rcParams.update({'font.family':family,'axes.unicode_minus':False,'svg.fonttype':'path',
                         'font.size':11,'axes.spines.top':False,'axes.spines.right':False,
                         'figure.dpi':120,'axes.prop_cycle':plt.cycler(color=PALETTE)})


def save(fig,name,title,note,description,sources):
    fig.suptitle(title,fontsize=17,y=.97)
    fig.text(.04,.025,note,fontsize=9,va='bottom',linespacing=1.6)
    fig.tight_layout(rect=(.01,.17,.99,.92))
    fig.savefig(OUT/(name+'.png'),dpi=180,metadata={'Description':description,'Source':sources})
    svg=OUT/(name+'.svg')
    fig.savefig(svg,metadata={'Date':None,'Title':title,'Description':description,'Source':sources})
    tree=ET.parse(svg)
    root=tree.getroot()
    ns='http://www.w3.org/2000/svg'
    root.set('role','img')
    root.set('aria-labelledby',name+'-title '+name+'-description')
    for tag,text in [('title',title),('desc',description)]:
        child=ET.Element('{'+ns+'}'+tag,{'id':name+('-title' if tag=='title' else '-description')})
        child.text=text
        root.insert(0,child)
    tree.write(svg,encoding='utf-8',xml_declaration=True)
    plt.close(fig)
    return dict(file=name,title=title,description=description,sources=sources,note=note)


def main():
    setup_font()
    OUT.mkdir(exist_ok=True)
    e=pd.read_csv(DATA/'employment.csv').set_index('year')
    w=pd.read_csv(DATA/'real_wages.csv').set_index('year')
    catalog=[]
    wood='Wood (1910), Table 41, pp.598–599'
    allen='Allen (2007), Appendix I, p.36'
    fig,ax=plt.subplots(figsize=(11,7))
    for col,label in [('handloom_people','手織工'),('factory_people','工場労働者（紡績・織布）')]:
        ax.plot(e.index,e[col]/10000,label=label,linewidth=2.5)
    ax.set(xlabel='年',ylabel='万人',ylim=(0,50),xlim=(1806,1862))
    ax.legend(loc='upper left')
    ax.grid(axis='y',alpha=.2)
    catalog.append(save(fig,'01_employment','手織工は減り、工場労働者が増えた',
                        '対象：英国綿業の手織工と工場労働者。染色・捺染などを含む全産業の人数ではない。\n'
                        '後世の推計で、Wood自身の補間を含む。同一人物の再就職を追った統計ではない。\n出典：'+wood,
                        '1806～1862年。手織工は1831年24万人から1859年1万3千人へ減少。工場は18万7千人から41万5千人へ増加。',wood))
    fig,ax=plt.subplots(figsize=(11,7))
    ax.plot(w.index,w.handloom_real_index,label='手織工',linewidth=2.5)
    ax.plot(w.index,w.factory_real_index,label='工場労働者（紡績・織布）',linewidth=2.5)
    ax.axhline(100,color='#666666',linestyle='--',linewidth=1,label='各群の1806年水準')
    for y in [1820,1850]:
        for col,color,offset in [('handloom_real_index',PALETTE[0],-15),('factory_real_index',PALETTE[1],10)]:
            v=w.loc[y,col]
            ax.scatter([y],[v],color=color)
            ax.annotate(f'{y}年：{v:.1f}',(y,v),xytext=(0,offset),textcoords='offset points',ha='center',fontsize=10)
    ax.set(xlabel='年',ylabel='実質週賃金の指数（各群の1806年＝100）',ylim=(0,165),xlim=(1806,1862))
    ax.legend(loc='upper left',fontsize=10)
    ax.grid(axis='y',alpha=.2)
    catalog.append(save(fig,'02_real_wages','手織工と工場労働者の実質賃金は、異なる動きをした',
                        '対象：各年の就業者の平均週賃金。年齢・性別・職種・労働時間が同じ集団の比較ではない。\n'
                        '推計された名目賃金を全国の生活費指数で調整。指数の差は賃金額の群間差を示さない。\n出典：'+wood+' ／ '+allen,
                        '1806年を各群100とした指数。手織工は1820年42.0、1850年43.5。工場は104.3、126.5。',wood+'; '+allen))
    fig,ax=plt.subplots(figsize=(11,7))
    ee=e.loc[1831:]
    for col,label in [('factory_change_from_1831','工場労働者の増減'),('handloom_change_from_1831','手織工の増減'),('combined_change_from_1831','二群合計の増減')]:
        ax.plot(ee.index,ee[col]/10000,label=label,linewidth=2.5)
    ax.axhline(0,color='#555555',linestyle='--',linewidth=1)
    for y in [1847,1859]:
        v=e.loc[y,'combined_change_from_1831']/10000
        ax.scatter([y],[v],color=PALETTE[2],zorder=5)
        ax.annotate(f'{y}年：計{e.loc[y,"combined_people"]/10000:.1f}万人',
                    (y,v),xytext=(0,-24 if y==1847 else 15),textcoords='offset points',ha='center',fontsize=10)
    ax.set(xlabel='年',ylabel='1831年からの人数差（万人）',xlim=(1831,1862),ylim=(-27,30))
    ax.legend(loc='upper left',fontsize=10)
    ax.grid(axis='y',alpha=.2)
    catalog.append(save(fig,'03_employment_comparison','合計人数の回復は、手織工の人数回復ではない',
                        '対象：Woodが集計した二群。1831年42.7万人、1847年33.0万人、1859年42.8万人。\n'
                        '1859－1831＝28年は推計系列上の再到達までの差。本人の再就職数・失業期間ではない。\n出典：'+wood,
                        '1859年は1831年比で工場22万8千人増、手織工22万7千人減、二群合計千人増。個人の吸収を意味しない。',wood))
    fig,ax=plt.subplots(figsize=(11,7))
    p=pd.read_csv(DATA/'productivity_examples.csv')
    labels=['手織の比較例\n年は明記なし・1人','機械織 1823年\n記述された作業者1人','機械織 1826年\n記述された作業者1人','機械織 1833年\n織工＋助手の2人']
    lo=p.pieces_per_described_person_low
    hi=p.pieces_per_described_person_high
    ax.bar(labels,lo,color=PALETTE[0],width=.62)
    ax.errorbar(range(len(p)),lo,yerr=[lo*0,hi-lo],fmt='none',ecolor='#333333',capsize=5)
    ax.set(ylabel='記述された人数で割った1人当たりの反数／週',ylim=(0,17))
    ax.tick_params(axis='x',labelsize=10)
    catalog.append(save(fig,'04_productivity','1833年の「18～20反」は、織工と助手の2人分',
                        '対象：製造業者による同種シャツ地の比較例（1反＝24ヤード）。産業平均ではない。\n'
                        '年齢・労働時間・関連工程の人数は統一されていない。棒上の線は記述された産出の範囲。\n出典：Baines (1835), p.240（原文を人数で除した独自計算）',
                        '手織は週2反。1833年機械織は2人で18～20反、単純除算で1人9～10反、手織比較例の4.5～5倍。',
                        'Baines (1835), p.240'))
    (OUT/'manifest.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    print('Generated 4 independent charts, each in SVG and PNG.')


if __name__=='__main__':
    main()
