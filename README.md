# 下水道實驗室 | Alligator's Lab

一個基於 **Flask + Python + Markdown** 的輕量級 3C 部落格引擎。

> 「在底層邏輯中，挖掘技術的寶藏。」

## ✨ 特色

- **零維護發文流程**：只需將 `.md` 檔案放入 `posts/` 資料夾，刷新瀏覽器即可看到新文章
- **動態 Markdown 解析**：自動掃描並解析 Markdown 檔案，無需重啟服務
- **分類系統**：支援「滲透紀錄 (Tech Logs)」與「樣本拆解 (Device Analysis)」兩大分類
- **工業科技風格**：深色背景 + 霓虹綠/藍色設計，營造實驗室氛圍
- **簡單部署**：支援 Docker + VPS 部署，開箱即用
- **代碼高亮**：內建 Highlight.js 支援 100+ 程式語言
- **響應式設計**：完美適配桌面、平板和手機

## 📋 目錄結構

```
alligators-blog-flask/
├── app.py                    # Flask 主應用程式
├── requirements.txt          # Python 依賴清單
├── Dockerfile               # Docker 容器配置
├── docker-compose.yml       # Docker Compose 配置
├── README.md                # 本檔案
├── .gitignore               # Git 忽略清單
│
├── posts/                   # 【重要】文章資料夾
│   ├── 2026-02-10-hello-world.md
│   └── 2026-02-11-docker-tips.md
│
├── templates/               # Jinja2 模板
│   ├── base.html           # 基礎模板
│   ├── index.html          # 首頁
│   ├── category.html       # 分類頁面
│   ├── post.html           # 文章詳細頁面
│   ├── about.html          # 關於頁面
│   └── 404.html            # 404 頁面
│
└── static/                  # 靜態資源
    ├── css/
    │   └── style.css       # 主樣式表
    └── js/
        └── main.js         # 主 JavaScript 檔案
```

## 🚀 快速開始

### 1. 本地開發

#### 安裝依賴

```bash
pip install -r requirements.txt
```

#### 啟動開發伺服器

```bash
python app.py
```

訪問 `http://localhost:5000` 即可看到網站。

### 2. 使用 Docker

#### 構建並啟動容器

```bash
docker-compose up --build
```

訪問 `http://localhost:5000`。

#### 停止容器

```bash
docker-compose down
```

## ✍️ 發文工作流程

### 第一步：建立文章檔案

在 `posts/` 資料夾中建立一個新的 Markdown 檔案，檔名格式為：

```
YYYY-MM-DD-slug.md
```

例如：`2026-02-26-my-first-post.md`

### 第二步：編寫文章

使用任何文字編輯器編寫 Markdown 內容。檔案頂部可選擇性地包含 YAML frontmatter：

```markdown
---
title: 我的第一篇文章
category: tech-logs
tags: Python, Flask, Markdown
---

# 文章標題

這是文章的內容...

## 小標題

更多內容...
```

#### Frontmatter 欄位說明

| 欄位 | 說明 | 預設值 |
|------|------|--------|
| `title` | 文章標題 | 檔案名稱 |
| `category` | 分類 (`tech-logs` 或 `device-analysis`) | `tech-logs` |
| `tags` | 標籤，逗號分隔 | 無 |

### 第三步：發布

**本地開發**：
- 將檔案保存到 `posts/` 資料夾
- 刷新瀏覽器，新文章自動出現

**VPS 部署**：
- 方式 1：透過 Git 推送
  ```bash
  git add posts/2026-02-26-my-post.md
  git commit -m "Add new post"
  git push origin main
  ```
  
- 方式 2：直接 SFTP 上傳
  ```bash
  sftp user@your-vps.com
  put posts/2026-02-26-my-post.md /path/to/posts/
  ```

**完成！** 無需修改 HTML、無需操作資料庫、無需重啟服務。

## 📝 Markdown 語法支援

本部落格支援完整的 Markdown 語法，包括：

### 基礎格式

```markdown
# 標題 1
## 標題 2
### 標題 3

**粗體** 和 *斜體*

- 列表項目 1
- 列表項目 2
  - 子項目

1. 有序項目 1
2. 有序項目 2
```

### 代碼塊

````markdown
```python
def hello_world():
    print("Hello, Alligator's Lab!")
```

```javascript
console.log("Hello, Alligator's Lab!");
```
````

### 引用

```markdown
> 這是一個引用
> 可以多行
```

### 表格

```markdown
| 列 1 | 列 2 | 列 3 |
|------|------|------|
| 內容 | 內容 | 內容 |
| 內容 | 內容 | 內容 |
```

### 連結和圖片

```markdown
[連結文字](https://example.com)
![圖片描述](https://example.com/image.png)
```

## 🎨 自訂設計

### 修改色彩

編輯 `static/css/style.css` 中的 CSS 變數：

```css
:root {
    --color-primary: #00ff41;        /* 霓虹綠 */
    --color-secondary: #00d4ff;      /* 霓虹藍 */
    --color-accent: #ff006e;         /* 霓虹粉 */
    --color-bg-dark: #0a0e27;        /* 深色背景 */
    /* ... 其他變數 ... */
}
```

### 修改字體

在 `templates/base.html` 中修改 Google Fonts 連結：

```html
<link href="https://fonts.googleapis.com/css2?family=YOUR_FONT&display=swap" rel="stylesheet">
```

然後在 `style.css` 中更新字體變數：

```css
--font-mono: 'YOUR_FONT', monospace;
--font-sans: 'YOUR_FONT', sans-serif;
```

## 🔧 進階配置

### 生產環境優化

編輯 `app.py` 中的最後一行：

```python
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,  # 關閉調試模式
        use_reloader=False,
    )
```

### 使用 Gunicorn 部署

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 使用 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 📦 VPS 部署指南

### 前置要求

- Ubuntu 20.04+ 或其他 Linux 發行版
- Docker 和 Docker Compose
- Git

### 部署步驟

1. **克隆倉庫**

```bash
git clone https://github.com/your-username/alligators-blog-flask.git
cd alligators-blog-flask
```

2. **構建並啟動容器**

```bash
docker-compose up -d --build
```

3. **配置 Nginx**

```bash
sudo nano /etc/nginx/sites-available/default
```

添加反向代理配置（見上方 Nginx 配置示例）。

4. **配置 SSL（推薦）**

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

5. **自動更新文章**

設定 Git Webhook 或 Cron 任務自動拉取最新文章：

```bash
# 編輯 crontab
crontab -e

# 添加每 5 分鐘拉取一次的任務
*/5 * * * * cd /path/to/alligators-blog-flask && git pull origin main
```

## 🐛 故障排除

### 文章不顯示

- 檢查檔案名稱格式是否為 `YYYY-MM-DD-slug.md`
- 確認檔案在 `posts/` 資料夾中
- 刷新瀏覽器快取

### 代碼高亮不工作

- 確認 Highlight.js CDN 連結正常
- 檢查代碼塊的語言標籤是否正確

### Docker 容器無法啟動

```bash
# 查看日誌
docker-compose logs web

# 重新構建
docker-compose down
docker-compose up --build
```

## 📄 許可證

MIT License

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

