#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给 deploy/ 下所有 HTML 批量注入 mobile-fix.css 的引用。
幂等：已经引用过就跳过。
"""
import re
from pathlib import Path

DEPLOY_DIR = Path(__file__).resolve().parent
LINK_TAG = '<link rel="stylesheet" href="mobile-fix.css">'

# 匹配 <meta name="viewport" ...>（不管有没有 user-scalable）
viewport_re = re.compile(r'(<meta\s+name="viewport"[^>]*>)', re.IGNORECASE)

def process(fp: Path) -> str:
    text = fp.read_text(encoding='utf-8')

    if 'mobile-fix.css' in text:
        return 'skip (already has mobile-fix.css)'

    m = viewport_re.search(text)
    if not m:
        # 兜底：插到 </head> 之前
        if '</head>' in text:
            text = text.replace('</head>', f'  {LINK_TAG}\n</head>', 1)
            fp.write_text(text, encoding='utf-8')
            return 'inserted before </head>'
        return 'WARN: no viewport and no </head>'

    # 插到 viewport 后面一行
    replacement = m.group(1) + '\n' + LINK_TAG
    text = text[:m.start()] + replacement + text[m.end():]
    fp.write_text(text, encoding='utf-8')
    return 'inserted after viewport'

def main():
    htmls = sorted(DEPLOY_DIR.glob('*.html'))
    for fp in htmls:
        status = process(fp)
        print(f'{fp.name:30s} -> {status}')

if __name__ == '__main__':
    main()
