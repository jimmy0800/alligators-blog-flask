#!/usr/bin/env python3
"""
下水道實驗室 | Alligator's Lab
Flask + Markdown 動態部落格引擎

工作流程：
1. 將 .md 檔案放入 posts/ 資料夾
2. 刷新瀏覽器，自動偵測並渲染
3. 無需修改 HTML、無需操作資料庫
"""

import os
import re
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, abort
import markdown
from markdown.extensions import fenced_code, tables, toc

# ============================================================================
# 應用初始化
# ============================================================================

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
POSTS_DIR = Path(__file__).parent / 'posts'
POSTS_DIR.mkdir(exist_ok=True)

# ============================================================================
# Markdown 解析器設定
# ============================================================================

md = markdown.Markdown(
    extensions=[
        fenced_code.FencedCodeExtension(),
        tables.TableExtension(),
        toc.TocExtension(),
        'markdown.extensions.codehilite',
        'markdown.extensions.extra',
        'markdown.extensions.nl2br',
    ],
    extension_configs={
        'markdown.extensions.codehilite': {
            'use_pygments': True,
            'css_class': 'highlight',
        }
    }
)

# ============================================================================
# 文章解析工具函數
# ============================================================================

def parse_post_filename(filename):
    """
    解析檔案名稱格式：YYYY-MM-DD-slug.md
    
    返回：
        {
            'date': datetime 物件,
            'slug': 文章 URL slug,
            'filename': 原始檔案名稱
        }
    或 None 如果格式不符
    """
    match = re.match(r'^(\d{4})-(\d{2})-(\d{2})-(.+)\.md$', filename)
    if not match:
        return None
    
    year, month, day, slug = match.groups()
    try:
        date = datetime(int(year), int(month), int(day))
        return {
            'date': date,
            'slug': slug,
            'filename': filename
        }
    except ValueError:
        return None


def extract_frontmatter(content):
    """
    從 Markdown 內容中提取 YAML frontmatter
    
    格式：
    ---
    title: 文章標題
    category: tech-logs  # 或 device-analysis
    tags: tag1, tag2
    ---
    
    返回：(frontmatter_dict, content_without_frontmatter)
    """
    frontmatter = {}
    
    if content.startswith('---'):
        try:
            _, fm_text, rest = content.split('---', 2)
            for line in fm_text.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip()
            return frontmatter, rest.strip()
        except ValueError:
            pass
    
    return frontmatter, content


def load_post(slug):
    """
    根據 slug 載入文章
    
    返回：
        {
            'slug': 文章 slug,
            'title': 文章標題,
            'date': 發布日期 (datetime),
            'date_str': 格式化日期字串,
            'category': 分類 (tech-logs 或 device-analysis),
            'tags': 標籤列表,
            'content': HTML 內容,
            'toc': 目錄 (如果有的話)
        }
    """
    # 掃描 posts 資料夾找到對應的檔案
    for filename in os.listdir(POSTS_DIR):
        if not filename.endswith('.md'):
            continue
        
        parsed = parse_post_filename(filename)
        if not parsed or parsed['slug'] != slug:
            continue
        
        filepath = POSTS_DIR / filename
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                raw_content = f.read()
        except Exception as e:
            print(f"讀取檔案失敗: {filepath} - {e}")
            return None
        
        # 提取 frontmatter
        frontmatter, markdown_content = extract_frontmatter(raw_content)
        
        # 重置 Markdown 解析器（清除上次的 TOC）
        md.reset()
        html_content = md.convert(markdown_content)
        
        # 構建文章物件
        post = {
            'slug': slug,
            'title': frontmatter.get('title', filename),
            'date': parsed['date'],
            'date_str': parsed['date'].strftime('%Y-%m-%d'),
            'category': frontmatter.get('category', 'tech-logs'),
            'tags': [t.strip() for t in frontmatter.get('tags', '').split(',') if t.strip()],
            'content': html_content,
            'toc': md.toc if hasattr(md, 'toc') else '',
        }
        
        return post
    
    return None


def load_all_posts(category=None):
    """
    載入所有文章，按日期倒序排列
    
    參數：
        category: 可選，篩選特定分類 ('tech-logs' 或 'device-analysis')
    
    返回：
        文章列表，每篇包含 slug, title, date, date_str, category, tags
    """
    posts = []
    
    for filename in os.listdir(POSTS_DIR):
        if not filename.endswith('.md'):
            continue
        
        parsed = parse_post_filename(filename)
        if not parsed:
            continue
        
        filepath = POSTS_DIR / filename
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                raw_content = f.read()
        except Exception:
            continue
        
        # 提取 frontmatter
        frontmatter, _ = extract_frontmatter(raw_content)
        
        post_category = frontmatter.get('category', 'tech-logs')
        
        # 篩選分類
        if category and post_category != category:
            continue
        
        posts.append({
            'slug': parsed['slug'],
            'title': frontmatter.get('title', filename),
            'date': parsed['date'],
            'date_str': parsed['date'].strftime('%Y-%m-%d'),
            'category': post_category,
            'tags': [t.strip() for t in frontmatter.get('tags', '').split(',') if t.strip()],
        })
    
    # 按日期倒序排列
    posts.sort(key=lambda x: x['date'], reverse=True)
    return posts


# ============================================================================
# 路由定義
# ============================================================================

@app.route('/')
def index():
    """首頁 - 實驗室入口"""
    tech_posts = load_all_posts('tech-logs')
    device_posts = load_all_posts('device-analysis')
    life_posts = load_all_posts('life-thoughts')
    
    return render_template(
        'index.html',
        tech_posts=tech_posts,
        device_posts=device_posts,
        life_posts=life_posts,
    )


@app.route('/tech-logs')
def tech_logs():
    """技術文章列表 - 滲透紀錄"""
    posts = load_all_posts('tech-logs')
    return render_template(
        'category.html',
        category='tech-logs',
        category_title='滲透紀錄',
        category_description='深入技術細節，探索系統底層邏輯',
        posts=posts,
    )


@app.route('/device-analysis')
def device_analysis():
    """3C 評測列表 - 樣本拆解"""
    posts = load_all_posts('device-analysis')
    return render_template(
        'category.html',
        category='device-analysis',
        category_title='樣本拆解',
        category_description='拆解各類電子設備，發掘硬體秘密',
        posts=posts,
    )


@app.route('/life-thoughts')
def life_thoughts():
    """生活碎念列表"""
    posts = load_all_posts('life-thoughts')
    return render_template(
        'category.html',
        category='life-thoughts',
        category_title='生活碎念',
        category_description='分享日常的技術感悟和生活思考',
        posts=posts,
    )


@app.route('/about')
def about():
    """關於我 - 首席研究員"""
    return render_template('about.html')


@app.route('/post/<slug>')
def post(slug):
    """文章詳細頁面"""
    post_data = load_post(slug)
    
    if not post_data:
        abort(404)
    
    # 載入同分類的其他文章，用於「相關文章」推薦
    related_posts = [
        p for p in load_all_posts(post_data['category'])
        if p['slug'] != slug
    ][:3]
    
    return render_template(
        'post.html',
        post=post_data,
        related_posts=related_posts,
    )


@app.errorhandler(404)
def not_found(error):
    """404 頁面"""
    return render_template('404.html'), 404


# ============================================================================
# 開發工具
# ============================================================================

@app.context_processor
def inject_config():
    """注入全域變數到模板"""
    return {
        'site_title': '下水道實驗室 | Alligator\'s Lab',
        'site_tagline': '「在底層邏輯中，挖掘技術的寶藏。」',
    }


if __name__ == '__main__':
    # 開發模式：自動重載，支援 Markdown 熱更新
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True,
    )
