/**
 * 下水道實驗室 | Alligator's Lab
 * 主 JavaScript 檔案
 */

// ============================================================================
// 初始化
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    initializeCodeHighlight();
    initializeScrollEffects();
    initializeInteractiveElements();
});

// ============================================================================
// 代碼高亮初始化
// ============================================================================

function initializeCodeHighlight() {
    // 為代碼塊添加複製按鈕
    const codeBlocks = document.querySelectorAll('pre');
    
    codeBlocks.forEach((block, index) => {
        // 創建複製按鈕
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.textContent = '複製';
        copyButton.setAttribute('data-index', index);
        copyButton.type = 'button';
        
        // 添加複製功能
        copyButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const code = block.querySelector('code');
            if (!code) return;
            
            const text = code.innerText || code.textContent;
            
            // 使用 Clipboard API
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(text).then(() => {
                    copyButton.textContent = '✓ 已複製！';
                    copyButton.style.background = 'rgba(0, 255, 65, 0.3)';
                    setTimeout(() => {
                        copyButton.textContent = '複製';
                        copyButton.style.background = '';
                    }, 2000);
                }).catch(() => {
                    copyButton.textContent = '✗ 複製失敗';
                    setTimeout(() => {
                        copyButton.textContent = '複製';
                    }, 2000);
                });
            } else {
                // 備用方案：使用 execCommand
                const textArea = document.createElement('textarea');
                textArea.value = text;
                textArea.style.position = 'fixed';
                textArea.style.left = '-999999px';
                document.body.appendChild(textArea);
                textArea.select();
                try {
                    document.execCommand('copy');
                    copyButton.textContent = '✓ 已複製！';
                    copyButton.style.background = 'rgba(0, 255, 65, 0.3)';
                    setTimeout(() => {
                        copyButton.textContent = '複製';
                        copyButton.style.background = '';
                    }, 2000);
                } catch (err) {
                    copyButton.textContent = '✗ 複製失敗';
                    setTimeout(() => {
                        copyButton.textContent = '複製';
                    }, 2000);
                }
                document.body.removeChild(textArea);
            }
        });
        
        // 將按鈕插入到代碼塊
        block.style.position = 'relative';
        block.appendChild(copyButton);
    });
}

// ============================================================================
// 滾動效果
// ============================================================================

function initializeScrollEffects() {
    // 添加滾動時的視差效果或其他動畫
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // 觀察所有文章卡片
    document.querySelectorAll('.post-item, .timeline-item, .related-post-card').forEach(el => {
        observer.observe(el);
    });
}

// ============================================================================
// 互動元素
// ============================================================================

function initializeInteractiveElements() {
    // 為所有外部連結添加 target="_blank"
    const externalLinks = document.querySelectorAll('a[href^="http"]');
    externalLinks.forEach(link => {
        if (!link.hostname || link.hostname !== window.location.hostname) {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
        }
    });
    
    // 平滑滾動
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });
}

// ============================================================================
// 工具函數
// ============================================================================

/**
 * 添加淡入效果的 CSS
 */
function addFadeInStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .fade-in {
            animation: fadeIn 0.6s ease-in-out forwards;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .copy-button {
            position: absolute;
            top: 8px;
            right: 8px;
            background: rgba(0, 255, 65, 0.1);
            color: #00ff41;
            border: 1px solid rgba(0, 255, 65, 0.3);
            padding: 4px 12px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 0.8rem;
            font-family: 'JetBrains Mono', monospace;
            transition: all 0.3s ease;
            z-index: 10;
        }
        
        .copy-button:hover {
            background: rgba(0, 255, 65, 0.2);
            border-color: rgba(0, 255, 65, 0.5);
            box-shadow: 0 0 8px rgba(0, 255, 65, 0.3);
        }
    `;
    document.head.appendChild(style);
}

// 添加淡入樣式
addFadeInStyles();

// ============================================================================
// 控制台歡迎訊息
// ============================================================================

console.log(
    '%c下水道實驗室 | Alligator\'s Lab',
    'font-size: 20px; font-weight: bold; color: #00ff41; text-shadow: 0 0 10px #00ff41;'
);
console.log(
    '%c「在底層邏輯中，挖掘技術的寶藏。」',
    'font-size: 12px; color: #00d4ff; font-family: "JetBrains Mono", monospace;'
);
