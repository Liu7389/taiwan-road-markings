"""依 data/markings.json 產生全部標線頁與首頁。用法：python scripts/build.py"""
import json, os, html, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import diagrams as svg
OUT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=json.load(open(os.path.join(OUT,"data","markings.json"),encoding="utf-8"))
SRC=D["source"]; MS=D["markings"]; BY={m["id"]:m for m in MS}
UPDATED=D.get("updated") or datetime.date.today().isoformat()
for d in ["markings", "assets/diagrams"]:
    os.makedirs(os.path.join(OUT,d), exist_ok=True)
e=html.escape
def page(m, body_rel="../"):
    rel="".join(f'<li><a href="{BY[r]["slug"]}.html">{e(BY[r]["article"])} {e(BY[r]["name"])}</a></li>' if r in BY else f'<li>第{e(r.replace("-","條之"))}{"" if "-" in r else "條"}（尚未收錄）</li>' for r in m["related"])
    verify=f'<p class="verify">待查證：{e(m["verify"])}</p>' if m.get("verify") else ""
    mis="".join(f"<li>{e(x)}</li>" for x in m["misread"])
    return f'''<!doctype html>
<html lang="zh-Hant-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(m["name"])}｜臺灣道路標線圖鑑</title>
<meta name="description" content="{e(m["article"])} {e(m["name"])}：{e(m["meaning"])}">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<header class="site"><a class="brand" href="../index.html">臺灣道路標線圖鑑</a></header>
<main class="page" data-id="{e(m["id"])}">
<nav class="crumb"><a href="../index.html">首頁</a> › {e(m["group"])} › {e(m["name"])}</nav>
<h1>{e(m["name"])} <span class="badge">{e(m["article"])}</span></h1>
<p class="lead">{e(m["meaning"])}</p>
{verify}
<figure id="diagram"><img src="../assets/diagrams/{m["slug"]}.svg" alt="{e(m["name"])}示意圖" width="760">
<figcaption>示意圖：長度依比例（1 公尺＝12 px），線寬放大示意，非施工圖。</figcaption></figure>
<section id="spec"><h2>規格</h2>
<table><tr><th>類別</th><td>{e(m["group"])}</td></tr><tr><th>顏色</th><td>{e(m["color"])}</td></tr>
<tr><th>線型</th><td>{e(m["pattern"])}</td></tr><tr><th>尺寸</th><td>{e(m["dims"])}</td></tr></table></section>
<section id="meaning"><h2>意義</h2><p>{e(m["meaning"])}</p></section>
<section id="where"><h2>設置地點</h2><p>{e(m["where"])}</p></section>
<section id="crossing"><h2>跨越或通行</h2><p>{e(m["crossing"])}</p></section>
<section id="misread"><h2>常見誤解</h2><ul>{mis}</ul></section>
<section id="related"><h2>相關標線</h2><ul>{rel}</ul></section>
<section id="source"><h2>出處</h2><p>{e(SRC["law"])}（{e(SRC["version"])}）{e(m["article"])}。<a href="{e(SRC["url"])}">全國法規資料庫原文</a></p>
<p class="note">本頁為條文整理，用字以原文為準；標「整理說明」者為本站補充。最後更新：{UPDATED}</p></section>
</main>
<footer class="site"><a href="../index.html">回目錄</a>・<a href="../changelog.html">更新紀錄</a></footer>
</body>
</html>
'''
for m in MS:
    if m["id"] not in svg.DRAW:
        sys.exit(f"缺少示意圖函式：請在 scripts/diagrams.py 的 DRAW 加入 '{m['id']}'")
    open(f'{OUT}/assets/diagrams/{m["slug"]}.svg','w',encoding='utf-8').write(svg.DRAW[m["id"]]())
    open(f'{OUT}/markings/{m["slug"]}.html','w',encoding='utf-8').write(page(m))
def card(m): return f'''<a class="card" href="markings/{m["slug"]}.html" data-group="{e(m["group"])}"><img src="assets/diagrams/{m["slug"]}.svg" alt=""><span class="badge">{e(m["article"])}</span><strong>{e(m["name"])}</strong><span class="sum">{e(m["meaning"])}</span></a>'''
groups=[g for g in ["禁制標線","指示標線","警告標線"] if any(m["group"]==g for m in MS)]
secs="".join(f'<section class="group" id="{g}"><h2>{g}</h2><div class="grid">'+"".join(card(m) for m in MS if m["group"]==g)+'</div></section>' for g in groups)
idx=f'''<!doctype html>
<html lang="zh-Hant-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>臺灣道路標線圖鑑</title>
<meta name="description" content="依《道路交通標誌標線號誌設置規則》整理的道路標線圖鑑，每頁一種標線，附條號、示意圖與常見誤解。">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="site"><a class="brand" href="index.html">臺灣道路標線圖鑑</a></header>
<main>
<section class="hero"><h1>臺灣道路標線圖鑑</h1>
<p>一頁一種標線：叫什麼、第幾條、長什麼樣子、可不可以跨越，以及最常被誤會的地方。內容依《{e(SRC["law"])}》（{e(SRC["version"])}）整理，每個說法都附條號。</p>
<p class="quick">快速對照：<a href="markings/167-jinzhi-bianhuan.html">單一白實線是禁止變換車道線嗎？</a>・<a href="markings/189-1-chuanyue-xu.html">匝道旁很密的虛線是什麼？</a></p></section>
{secs}
</main>
<footer class="site">條文以<a href="{e(SRC["url"])}">全國法規資料庫</a>為準・<a href="changelog.html">更新紀錄</a>・收錄 {len(MS)} 種標線</footer>
</body>
</html>
'''
open(f'{OUT}/index.html','w',encoding='utf-8').write(idx)
# 更新紀錄頁：由 CHANGELOG.md 轉成 changelog.html（只處理 ## 標題與 - 清單）
items=[]
for line in open(os.path.join(OUT,"CHANGELOG.md"),encoding="utf-8"):
    line=line.rstrip()
    if line.startswith("## "): items.append(f"</ul><h2>{e(line[3:])}</h2><ul>")
    elif line.startswith("- "): items.append(f"<li>{e(line[2:])}</li>")
log="<ul>"+"".join(items)+"</ul>"
open(f'{OUT}/changelog.html','w',encoding='utf-8').write(idx.split('<main>')[0].replace('<title>臺灣道路標線圖鑑</title>','<title>更新紀錄｜臺灣道路標線圖鑑</title>')+f'<main class="page"><h1>更新紀錄</h1>{log}</main></body></html>')
print("已產生", len(MS), "個標線頁與 index.html")
