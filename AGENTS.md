# AGENTS.md｜臺灣道路標線圖鑑

給 AI 協作者（Codex、Claude Code 等）的專案規則。開始任何修改前先讀完本檔。

## 1. 專案目的
- 做一個「一頁一種標線」的教學網站，說明臺灣道路標線叫什麼、依據哪一條、長什麼樣子、可不可以跨越、常被誤會的地方。
- 讀者：考駕照的人、對道路配置有興趣的一般人、修課同學。
- 唯一法規依據：《道路交通標誌標線號誌設置規則》，目前版本為 **民國115年03月11日修正**，原文：https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=K0040014
- 這份資料（`data/markings.json`）也是期末專案「路析平台」RAG 知識庫的來源，所以欄位要完整、說法要可追溯。

## 2. 最重要的規則（違反就不算完成）
1. **每個說法都要有條號。** 條號、尺寸、顏色、意義只能來自條文。查不到或不確定時寫「待查證」，**不可以猜**。條文來源不是現行版原文（例如舊版附件、二手網站）時，必須填 `verify` 欄說明，頁面會自動顯示「待查證」提示，等人工逐字比對後才刪除。
2. **條文以外的補充要標示**：在句尾加「（整理說明）」，例如設置地點的例子、跨越規定的白話解釋。
3. **單一白實線不是禁止變換車道線。** 第167條只規定雙白實線（雙邊）與白實線配白虛線（單邊）。任何頁面都不可寫成單白實線＝禁止變換車道線。
4. **網站與頁面標題不可出現版本或工具字樣**（如「第二版」「整合版」「v2」「Claude」「ChatGPT」）。版本變化只寫在 `CHANGELOG.md`。
5. **不要手改產生出來的檔案**：`index.html`、`changelog.html`、`markings/*.html`、`assets/diagrams/*.svg` 都由 `scripts/build.py` 產生。要改內容就改 `data/markings.json`；要改版型就改 `scripts/build.py`；要改圖就改 `scripts/diagrams.py`。
6. 完成後一定要跑 `python scripts/build.py` 與 `python scripts/check_site.py`，**check 全部通過**才算完成。

## 3. 檔案結構
```
index.html                 首頁（產生）：依類別列出所有標線卡片
changelog.html             更新紀錄頁（產生，來源 CHANGELOG.md）
markings/<slug>.html       每種標線一頁（產生）
assets/style.css           全站唯一樣式檔
assets/diagrams/<slug>.svg 每頁示意圖（產生）
data/markings.json         所有內容的唯一來源
scripts/build.py           產生頁面
scripts/diagrams.py        示意圖繪製函式，DRAW 字典以條號對應函式
scripts/check_site.py      規則檢查
templates/new-marking.json 新增一筆資料的範本
CHANGELOG.md               更新紀錄
AGENTS.md / CLAUDE.md      AI 協作規則（CLAUDE.md 只指向本檔）
```

## 4. 命名規則
- `id`：條號，「之」用連字號，例如 `167`、`189-1`、`183-1`。
- `article`：顯示用條號，`第167條`、`第189條之1`（check 會驗證與 id 一致）。
- `slug`：`<id>-<名稱漢語拼音簡寫>`，全小寫、只用 a–z、0–9、連字號，例如 `167-jinzhi-bianhuan`、`189-1-chuanyue-xu`。頁面與示意圖都用這個檔名。
- `group`：只能是 `禁制標線`、`指示標線`、`警告標線`（依條文所在的節）。

## 5. 資料欄位（`data/markings.json` 的每一筆）
| 欄位 | 內容 | 規則 |
|---|---|---|
| name | 條文名稱 | 用條文用語，不用俗稱 |
| aliases | 俗稱 | 例：「雙白線」「密虛線」，查詢工具會用到 |
| color / pattern | 顏色／線型 | pattern 用「實線、虛線、雙實線、實線配虛線、圖形」等詞組合 |
| dims | 尺寸 | 照條文數字，單位寫公分或公尺，數字與單位間留空格 |
| meaning | 意義 | 一兩句，照條文 |
| where | 設置地點 | 照條文；補充例子加（整理說明） |
| crossing | 跨越或通行 | 條文有寫就照寫；沒有就寫白話解釋並加（整理說明） |
| misread | 常見誤解 | 陣列，每點一句，盡量附條號 |
| related | 相關條號 | 陣列；未收錄的條號頁面會顯示「尚未收錄」 |
| verify | 待查證說明（選填） | 條文未與現行版原文逐字比對時填寫；有此欄頁面顯示黃色提示，check 列為提醒 |

## 6. 頁面版型（由 build.py 產生，固定順序）
標題＋條號徽章 → 一句話意義 → 示意圖（#diagram）→ 規格表（#spec）→ 意義（#meaning）→ 設置地點（#where）→ 跨越或通行（#crossing）→ 常見誤解（#misread）→ 相關標線（#related）→ 出處與更新日期（#source）。
新增區塊時要同步修改 `check_site.py` 的 SECTIONS。

## 7. 示意圖繪製慣例（`scripts/diagrams.py`）
- 俯視圖，行車方向由左往右（雙向道路上方車道往左）。
- **長度依比例：1 公尺＝12 px**；車道寬 3.5 公尺＝42 px；畫面寬 760 px（約 60 公尺）。
- **線寬放大示意：px＝公分 × 0.3，最小 3 px**；斜紋等過密的圖案可放大間距，但要在圖說寫「圖中間距放大」。
- 顏色只用：瀝青 `#3b403e`、白線 `#f4f4ee`、黃線 `#e2b40c`、背景草地 `#b7c6ae`（與 road-sim 模擬器一致）。
- 每張圖左上角一句說明（重點規格），左下角 10 m 比例尺，加上方向箭頭。
- 兩車道以上匝道的分流或匯流處只畫一組槽化線；配置依實景時要照衛星圖或街景，不可想像。
- 新函式加到 `DRAW` 字典，鍵為 id。

## 8. 新增一種標線的步驟
1. 到全國法規資料庫讀該條原文，確認條號、尺寸、意義。
2. 複製 `templates/new-marking.json`，填好後加到 `data/markings.json` 的 `markings` 陣列（依條號排序）。
3. 在 `scripts/diagrams.py` 寫 `svg_<id>()` 並加入 `DRAW`。
4. 若其他標線與它相關，更新那些標線的 `related`。
5. 執行 `python scripts/build.py`，再執行 `python scripts/check_site.py`，直到全部通過。
6. 在 `CHANGELOG.md` 最上方新增日期與一行說明，再跑一次 build。

### check_site.py 會檢查的項目
欄位齊全、id／slug／article 格式一致、group 合法、每頁 8 個區塊、條號與法規連結出現在頁面、首頁連到每一頁、沒有多餘頁面、標題沒有版本或工具字樣、單白實線未被寫成禁止變換車道線、crossing 非條文用語時有（整理說明）。`verify` 欄列為提醒。

### 完成後回報格式（給使用者看）
1. 新增或修改了哪幾筆（條號＋名稱）。
2. 條文來源（網址或文件）與版本；沒能讀到現行版原文就明說。
3. `check_site.py` 的輸出（含提醒）。
4. 需要使用者確認的地方（例如待查證條文、實景配置）。

### 範例：第183條之1 是怎麼加進來的
1. 第167條與第183條的 related 已列「183-1」，頁面顯示「尚未收錄」，表示這是下一個該補的。
2. 複製範本填入 slug `183-1-kuaiman-fenge`、group `指示標線`；因只讀到 102 年附件，填了 `verify`。
3. 在 `diagrams.py` 加 `svg_183_1()`，`DRAW` 加 `"183-1"`。
4. build → check 全部通過（1 則待查證提醒），CHANGELOG 加一行。
5. 使用者提供現行版原文後逐字比對：刪除「距人行道 2 公尺」（舊版內容）、補上慢車道機車與自行車圖案的規定，移除 `verify`，再 build → check。

## 9. 其他修改
- 改樣式：只改 `assets/style.css`，用 `:root` 的顏色變數；手機寬度不得出現水平捲動。
- 法規修正時：更新 `data/markings.json` 的 `source.version`，逐條比對受影響的條文，並記錄在 CHANGELOG。
- 不加入外部 JavaScript 或追蹤碼；網站必須是純靜態檔案，可直接放 GitHub Pages。

## 10. 延伸方向（沿用同一套規則）
- 標線第四節「警告標線」：group 已支援，首頁有資料就會出現該類別。
- 第二章「標誌」或第四章「號誌」：新增 group 值與對應繪圖函式，並在 check 的 group 清單加入；其餘欄位、版型、檢查不變。
- 期末專案「路析平台」直接讀 `data/markings.json` 當 RAG 知識庫，所以欄位名稱不要改。

## 11. 語言
臺灣慣用繁體中文與全形標點；道路用語用「匝道、交流道、路肩、壅塞、大客車、大貨車」，不用「閘道、應急車道、擁堵」。
