---
title: Markdown 檔案轉換指南：讓舊文章適配部落格系統
category: tech-logs
tags: Markdown, 部落格, 教學, 文檔管理
image: /static/images/tech-life-illustration.png
---



# Markdown 檔案轉換指南：讓舊文章適配部落格系統

![Markdown 轉換](/static/images/tech-life-illustration.png)

如果您已經有一些用 Markdown 撰寫的文章，想要將它們遷移到下水道實驗室部落格，本文將為您詳細介紹轉換過程。好消息是：**轉換非常簡單！** 只需要在檔案開頭添加一些元數據即可。

## 🎯 為什麼需要轉換？

部落格系統使用 **YAML frontmatter** 來管理文章的元數據，包括：

- 📝 **標題**：文章的名稱
- 🏷️ **分類**：幫助讀者快速找到相關內容
- 🔖 **標籤**：補充分類，提高內容的可發現性
- 🖼️ **圖片**：首頁卡片上顯示的縮圖

這些元數據讓部落格系統能夠自動組織和展示您的文章。

## 📋 轉換步驟

### 第一步：準備舊的 Markdown 檔案

假設您有一篇舊的 Markdown 檔案，內容如下：

```markdown
# 我的第一篇技術文章

這是一篇關於 Python 的文章...

## 基礎概念

Python 是一種...
```

### 第二步：添加 Frontmatter

在檔案的最開頭（在任何內容之前）添加以下格式的 YAML 元數據：

```markdown
---
title: 我的第一篇技術文章
category: tech-logs
tags: Python, 編程, 教學
image: /static/images/my-image.png
---

# 我的第一篇技術文章

這是一篇關於 Python 的文章...

## 基礎概念

Python 是一種...
```

**注意**：
- 元數據必須被 `---` 包圍
- 冒號後面必須有空格（例如 `title: 標題`）
- 不要使用 Tab 鍵，只用空格縮進

### 第三步：設定正確的欄位

#### `title`（必需）
文章的標題，將顯示在首頁卡片和文章頁面上。

```yaml
title: 我的第一篇技術文章
```

#### `category`（必需）
文章的分類，決定它會出現在哪個分類頁面。

選擇以下其中一個：

- **`tech-logs`** - 滲透紀錄（技術文章、系統架構、程式設計）
- **`device-analysis`** - 樣本拆解（硬體評測、產品分析、拆解指南）
- **`life-thoughts`** - 生活碎念（個人思考、生活分享、隨筆）

```yaml
category: tech-logs
```

#### `tags`（可選）
用逗號分隔的標籤列表，幫助讀者更快地找到相關內容。

```yaml
tags: Python, 編程, 教學, 初學者
```

#### `image`（可選）
首頁卡片上顯示的圖片路徑。如果不指定，系統會：
1. 自動提取文章中的第一張圖片
2. 如果沒有圖片，使用預設圖片 `/static/images/404.jpg`

```yaml
image: /static/images/my-image.png
```

## 🖼️ 圖片管理

### 添加圖片到部落格

1. **準備圖片檔案**
   - 支援格式：PNG、JPG、GIF、WebP 等
   - 建議大小：不超過 2-3 MB

2. **上傳到 `/static/images/` 資料夾**
   ```bash
   # 在本地
   cp /path/to/my-image.png posts/static/images/
   ```

3. **在 frontmatter 中指定**
   ```yaml
   image: /static/images/my-image.png
   ```

4. **提交到 GitHub**
   ```bash
   git add static/images/my-image.png
   git add posts/my-article.md
   git commit -m "Add new article with image"
   git push origin master
   ```

### 在文章內容中使用圖片

您也可以在文章內容中添加多張圖片：

```markdown
# 我的文章

## 第一部分

這是第一部分的內容。

![圖片描述](/static/images/image1.png)

## 第二部分

這是第二部分的內容。

![另一張圖片](/static/images/image2.png)
```

## 📝 完整轉換例子

### 原始檔案（舊格式）

```markdown
# Flask 部落格架構完全指南

Flask 是一個輕量級的 Python Web 框架...

## 為什麼選擇 Flask？

1. **簡單易學**：語法直觀，新手友好
2. **靈活性強**：可以自由組合各種擴展
3. **社群活躍**：有大量的教程和資源

## 基本架構

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'
```
## 🎓 總結

轉換舊 Markdown 檔案到部落格系統只需要三個簡單的步驟：

1. **添加 frontmatter**：在檔案開頭添加 YAML 元數據
2. **準備圖片**：上傳代表性圖片到 `/static/images/`
3. **提交上傳**：使用 Git 推送到 GitHub，然後在 VPS 上拉取

完成後，您的文章會自動出現在首頁和對應的分類頁面上。


## ⚠️ 常見錯誤

### 錯誤 1：YAML 格式不正確

❌ **錯誤**：
```markdown
---
title:我的文章
category:tech-logs
---
```

✅ **正確**：
```markdown
---
title: 我的文章
category: tech-logs
---
```

**問題**：冒號後面必須有空格。

### 錯誤 2：使用 Tab 縮進

❌ **錯誤**：
```markdown
---
title:	我的文章  ← 使用了 Tab
category:	tech-logs
---
```

✅ **正確**：
```markdown
---
title: 我的文章  ← 使用空格
category: tech-logs
---
```

### 錯誤 3：圖片路徑錯誤

❌ **錯誤**：
```yaml
image: static/images/my-image.png  ← 缺少開頭的 /
image: /images/my-image.png  ← 路徑不完整
```

✅ **正確**：
```yaml
image: /static/images/my-image.png
```

### 錯誤 4：分類名稱錯誤

❌ **錯誤**：
```yaml
category: 技術文章  ← 使用中文
category: tech  ← 不完整
```

✅ **正確**：
```yaml
category: tech-logs
category: device-analysis
category: life-thoughts
```

## 💡 最佳實踐

### 1. 使用一致的檔案名稱格式

```
2026-02-27-flask-guide.md
2026-02-27-python-tips.md
2026-02-27-hardware-review.md
```

### 2. 為每篇文章添加一張代表性圖片

首頁卡片上的圖片是讀者第一眼看到的內容，選擇一張清晰、相關的圖片可以提高點擊率。

### 3. 使用有意義的標籤

```yaml
# ✅ 好的標籤
tags: Python, Flask, Web 開發, 後端

# ❌ 不好的標籤
tags: 文章, 東西, 內容
```

### 4. 保持標題簡潔但有描述性

```yaml
# ✅ 好的標題
title: Flask 部落格架構完全指南

# ❌ 不好的標題
title: 我的文章
title: Flask
```


