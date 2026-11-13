"""檢查網站是否符合 AGENTS.md 的規則。用法：python scripts/check_site.py（全部通過才算完成）"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "markings.json"), encoding="utf-8"))
REQUIRED_FIELDS = ["id", "article", "slug", "name", "aliases", "group", "color", "pattern", "dims", "meaning", "where", "crossing", "misread", "related"]
SECTIONS = ["diagram", "spec", "meaning", "where", "crossing", "misread", "related", "source"]
BANNED_IN_TITLE = ["版", "v1", "v2", "Claude", "ChatGPT", "Codex", "整合"]
errors = []
warnings = []
index = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
ids, slugs = set(), set()
for m in D["markings"]:
    tag = m.get("id", "?")
    for f in REQUIRED_FIELDS:
        if f not in m or m[f] in ("", None):
            errors.append(f"{tag}: data 缺欄位 {f}")
    if m["id"] in ids: errors.append(f"{tag}: id 重複")
    ids.add(m["id"])
    if not re.fullmatch(r"\d+(-\d+)?-[a-z0-9-]+", m["slug"]): errors.append(f"{tag}: slug 格式應為「條號-拼音」小寫，例如 167-jinzhi-bianhuan")
    elif not m["slug"].startswith(m["id"] + "-"): errors.append(f"{tag}: slug 必須以條號開頭")
    if m["slug"] in slugs: errors.append(f"{tag}: slug 重複")
    slugs.add(m["slug"])
    if group := m.get("group"):
        if group not in ("禁制標線", "指示標線", "警告標線"): errors.append(f"{tag}: group 只能是禁制／指示／警告標線")
    want = "第" + m["id"].replace("-", "條之") + ("" if "-" in m["id"] else "條")
    if m["article"] != want: errors.append(f"{tag}: article 應寫成「{want}」")
    page = os.path.join(ROOT, "markings", m["slug"] + ".html")
    svgf = os.path.join(ROOT, "assets", "diagrams", m["slug"] + ".svg")
    if not os.path.exists(svgf): errors.append(f"{tag}: 缺示意圖 {svgf}")
    if not os.path.exists(page):
        errors.append(f"{tag}: 缺頁面，請執行 python scripts/build.py"); continue
    h = open(page, encoding="utf-8").read()
    for s in SECTIONS:
        if f'id="{s}"' not in h: errors.append(f"{tag}: 頁面缺少區塊 #{s}")
    if m["article"] not in h: errors.append(f"{tag}: 頁面沒有出現條號")
    if "law.moj.gov.tw" not in h: errors.append(f"{tag}: 頁面沒有全國法規資料庫連結")
    if f'markings/{m["slug"]}.html' not in index: errors.append(f"{tag}: index.html 沒有連到此頁")
    # 規則 3：單一白實線不可寫成禁止變換車道線
    text = "".join(str(m.get(k, "")) for k in ("meaning", "where", "crossing")) + "".join(m.get("misread", []))
    for sent in re.split(r"[。；]", text):
        if re.search(r"單[一條]?白實線", sent) and "禁止變換車道線" in sent and not re.search(r"不是|不屬|並非|不可", sent):
            errors.append(f"{tag}: 疑似把單一白實線寫成禁止變換車道線：{sent}")
    # 規則 2：沒有條文依據的補充要標（整理說明）；crossing 若沒有「不得／禁止／應」等條文用語就必須加註
    if not re.search(r"不得|禁止|應|允許|整理說明", m.get("crossing", "")): errors.append(f"{tag}: crossing 非條文用語時要加「（整理說明）」")
    if m.get("verify"): warnings.append(f"{tag}: 待查證 — {m['verify']}")
    for r in m["related"]:
        if r == m["id"]: errors.append(f"{tag}: related 不可包含自己")
for f in sorted(os.listdir(os.path.join(ROOT, "markings"))):
    if f.endswith(".html") and f[:-5] not in slugs: errors.append(f"多餘頁面 markings/{f}（data 沒有對應資料）")
for f in ["index.html"] + [os.path.join("markings", s + ".html") for s in slugs]:
    p = os.path.join(ROOT, f)
    if os.path.exists(p):
        t = re.search(r"<title>(.*?)</title>", open(p, encoding="utf-8").read())
        if t and any(b in t.group(1) for b in BANNED_IN_TITLE): errors.append(f"{f}: 標題不可含版本或工具字樣：{t.group(1)}")
if warnings:
    print("提醒（不擋完成，但要在回報中列出）：\n- " + "\n- ".join(warnings))
if errors:
    print("未通過：\n- " + "\n- ".join(errors)); sys.exit(1)
print(f"全部通過：{len(D['markings'])} 種標線，頁面、示意圖、首頁連結與標題規則皆符合。")
