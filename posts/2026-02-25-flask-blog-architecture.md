---
title: Flask 部落格架構：從零到一
category: tech-logs
tags: Flask, Python, 架構設計
image: /static/images/flask-markdown-blog-hero.png
---



# Flask 部落格架構：從零到一

在本文中，我們將深入探討如何使用 Flask 和 Markdown 構建一個輕量級、易於維護的部落格系統。

![Flask 架構](/static/images/flask-markdown-blog-hero.png)
## 🎯 設計目標

我們的部落格系統需要滿足以下要求：

1. **零維護**：無需資料庫，只需丟 Markdown 檔案
2. **熱更新**：修改文章後無需重啟服務
3. **高性能**：支援快取機制，應對高流量
4. **易於部署**：支援 Docker 和傳統 VPS 部署

## 🏗️ 系統架構

### 核心流程

```
用戶請求
    ↓
Flask 路由
    ↓
掃描 posts/ 資料夾
    ↓
解析 Markdown 檔案
    ↓
提取 Frontmatter
    ↓
轉換為 HTML
    ↓
渲染 Jinja2 模板
    ↓
返回 HTML 響應
```

### 目錄結構

```
alligators-blog-flask/
├── app.py                    # 主應用程式
├── posts/                    # 文章資料夾
├── templates/                # Jinja2 模板
└── static/                   # 靜態資源
```

## 📝 Frontmatter 設計

我們使用 YAML frontmatter 來儲存文章元資料：

```yaml
---
title: 文章標題
category: tech-logs
tags: tag1, tag2, tag3
---
```

### 解析邏輯

```python
def extract_frontmatter(content):
    """提取 YAML frontmatter"""
    if content.startswith('---'):
        try:
            _, fm_text, rest = content.split('---', 2)
            frontmatter = {}
            for line in fm_text.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip()
            return frontmatter, rest.strip()
        except ValueError:
            pass
    return {}, content
```

## 🔄 Markdown 解析

我們使用 `python-markdown` 庫進行解析：

```python
import markdown
from markdown.extensions import fenced_code, tables, toc

md = markdown.Markdown(
    extensions=[
        fenced_code.FencedCodeExtension(),
        tables.TableExtension(),
        toc.TocExtension(),
        'markdown.extensions.extra',
    ]
)

html_content = md.convert(markdown_content)
```

### 支援的擴展

| 擴展 | 功能 |
|------|------|
| `fenced_code` | 程式碼塊 |
| `tables` | Markdown 表格 |
| `toc` | 目錄生成 |
| `extra` | 其他高級功能 |

## 🗂️ 檔案名稱約定

檔案名稱格式：`YYYY-MM-DD-slug.md`

```python
def parse_post_filename(filename):
    """解析檔案名稱"""
    match = re.match(r'^(\d{4})-(\d{2})-(\d{2})-(.+)\.md$', filename)
    if not match:
        return None
    
    year, month, day, slug = match.groups()
    date = datetime(int(year), int(month), int(day))
    return {
        'date': date,
        'slug': slug,
        'filename': filename
    }
```

## 🚀 路由設計

### 主要路由

```python
@app.route('/')
def index():
    """首頁"""
    tech_posts = load_all_posts('tech-logs')
    device_posts = load_all_posts('device-analysis')
    return render_template('index.html', ...)

@app.route('/tech-logs')
def tech_logs():
    """技術文章列表"""
    posts = load_all_posts('tech-logs')
    return render_template('category.html', ...)

@app.route('/post/<slug>')
def post(slug):
    """文章詳細頁面"""
    post_data = load_post(slug)
    return render_template('post.html', post=post_data)
```

## 💾 快取策略

### 簡單快取

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def load_post(slug):
    """載入文章（帶快取）"""
    # 實現邏輯
    pass
```

### 監聽檔案變化

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PostChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.md'):
            load_post.cache_clear()
```

## 🎨 模板設計

### 基礎模板 (base.html)

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    <nav><!-- 導航 --></nav>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer><!-- 頁腳 --></footer>
</body>
</html>
```

### 文章模板 (post.html)

```html
{% extends "base.html" %}

{% block content %}
<article>
    <h1>{{ post.title }}</h1>
    <div class="meta">
        <time>{{ post.date_str }}</time>
        <span>{{ post.category }}</span>
    </div>
    <div class="content">
        {{ post.content | safe }}
    </div>
</article>
{% endblock %}
```

## 📊 性能優化

### 1. 靜態檔案快取

```python
@app.after_request
def add_cache_headers(response):
    if response.content_type.startswith('image/') or \
       response.content_type in ['text/css', 'application/javascript']:
        response.cache_control.max_age = 86400  # 1 天
    return response
```

### 2. Gzip 壓縮

```python
from flask_compress import Compress
Compress(app)
```

### 3. CDN 部署

將靜態資源上傳到 CDN，在模板中使用 CDN URL：

```html
<link rel="stylesheet" href="https://cdn.example.com/style.css">
```

## 🔐 安全考慮

### 1. 模板自動轉義

```html
<!-- 安全：自動轉義 HTML -->
<p>{{ user_input }}</p>

<!-- 不安全：禁用轉義 -->
<p>{{ user_input | safe }}</p>
```

### 2. 路徑遍歷防護

```python
def load_post(slug):
    # 防止 ../../../etc/passwd 攻擊
    if '..' in slug or '/' in slug:
        abort(400)
    # ...
```

## 📦 部署選項

### Docker 部署

```bash
docker-compose up -d
```

### Gunicorn + Nginx

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 雲平台部署

- Heroku
- Railway
- Render
- DigitalOcean App Platform

## 🎓 學習資源

- [Flask 官方文件](https://flask.palletsprojects.com/)
- [Python-Markdown 文件](https://python-markdown.github.io/)
- [Jinja2 模板文件](https://jinja.palletsprojects.com/)

## 📝 總結

使用 Flask + Markdown 構建部落格的優勢：

✅ 簡單易懂，適合個人部落格
✅ 無需資料庫，維護成本低
✅ 支援版本控制，方便備份
✅ 部署靈活，支援多種環境

---

**下水道實驗室 | Alligator's Lab**

「在底層邏輯中，挖掘技術的寶藏。」
