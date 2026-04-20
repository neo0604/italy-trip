# 移动端适配规范（Mobile Adaptation Spec）

> 所有 `deploy/` 下的 HTML 页面必须遵循本规范。  
> 适用设备：iPhone SE (375×667) → iPhone 17 Pro Max / 安卓旗舰 (430×932)。  
> 规范建立日期：**2026-04-20**。

---

## 🎯 核心原则

1. **原样式不改，只做兜底修复** — 所有修复统一走 `mobile-fix.css`
2. **每个 HTML 必须引用** `<link rel="stylesheet" href="mobile-fix.css">`
3. **viewport 必须允许缩放**（意大利旅行中需要放大看地址/电话）：
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
   ```

---

## 📋 新页面 checklist

创建或更新任何 HTML 时，必须逐项确认：

### HTML 头部
- [ ] `<meta charset="UTF-8">`
- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">`
- [ ] `<link rel="stylesheet" href="mobile-fix.css">`（放在 viewport 下一行）
- [ ] **不要**写 `user-scalable=no`（禁用缩放会让地图和电话号码很难看）

### 布局元素
| 元素 | 规范 |
|------|------|
| **SVG 路线图** | `style="width:100%; max-width:960px; height:auto; display:block;"` |
| **图片** | 默认被 `mobile-fix.css` 自动限宽，无需额外处理 |
| **表格 `<table>`** | 列数 ≥ 4 时，必须能横向滚动（`mobile-fix.css` 已兜底） |
| **Grid 布局** | 类名用 `.tip-grid / .info-grid / .rest-grid / .card-grid`，手机上会自动单列 |
| **Flex 行布局** | 长内容必须加 `flex-wrap: wrap` |
| **长英文地址/URL/电话** | 无需处理，`mobile-fix.css` 已加 `overflow-wrap: anywhere` |

### Day Tab 切换栏（所有 day*.html 必备）
必须使用这套模板（复制粘贴即可）：

```html
<div class="day-tabs" id="dayTabs">
  <a class="day-tab day-tab-home" href="index.html" title="首页">🏠</a>
  <a class="day-tab" href="day1.html"><span class="tab-day">D1</span><span class="tab-city">罗马</span></a>
  <!-- ... 按日循环 ... -->
  <a class="day-tab active" href="dayN.html">...</a>  <!-- 当前日加 active -->
</div>

<!-- 页面末尾必须加自动滚动到 active 的脚本 -->
<script>document.addEventListener("DOMContentLoaded",function(){var t=document.querySelector(".day-tab.active");if(t){t.scrollIntoView({inline:"center",block:"nearest"})}});</script>
```

对应 CSS（放在页面 `<style>` 里）：
```css
.day-tabs {
  display: flex; gap: 6px; overflow-x: auto; padding: 10px 14px;
  background: #fff; border-bottom: 1px solid #eee;
  -webkit-overflow-scrolling: touch;
}
.day-tabs::-webkit-scrollbar { display: none; }
.day-tab {
  flex-shrink: 0; display: flex; flex-direction: column; align-items: center;
  padding: 6px 12px; border-radius: 8px; color: #888;
  text-decoration: none; min-width: 56px;
}
.day-tab.active { background: /* 本日主题色 */; color: white; }
```

---

## 🧪 测试方法

### 快速本地测试（推荐在每次更新后跑一次）

```bash
# 1. 用 agent-browser 模拟 iPhone 15 视口
AB=/Users/neo/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser-darwin-arm64
$AB set device "iPhone 15"
$AB open "https://neo0604.github.io/italy-trip/dayN.html"
$AB screenshot /tmp/check.png
$AB close
```

支持的设备：iPhone 15 / 16 / 16 Pro / 17 / iPad / iPad Pro / Pixel 9 / Galaxy S25

### 真机测试
部署后用 Neo 手机实际打开一次，重点看：
1. Hero 标题不换行成太多
2. Stats bar 数字排列整齐
3. SVG 路线图不溢出
4. 表格可横向滚动
5. 底部 Day Tab 滚动到当前日居中

---

## 🔧 mobile-fix.css 覆盖范围

**全局**：防 overflow-x、图片自适应、长文本换行  
**表格**：手机端自动横向滚动 + 最小列宽 70px  
**≤640px 手机**：所有 Grid 单列化、标题缩小、padding 收紧、Tab 栏字号调整  
**≤380px 超小屏**：进一步收紧  
**打印**：隐藏工具栏、导出 PDF 友好

---

## ✅ 后续所有更新默认遵循

今后我（老六）给你做的任何新的 HTML 行程/攻略页面，都会：
1. 自动引入 `mobile-fix.css`
2. 设置正确的 viewport（允许缩放）
3. 用规范的 Day Tab 模板
4. 复杂表格自带横向滚动
5. SVG 用百分比宽度

**你不需要每次提醒我。**

---

_维护：老六 · 2026-04-20_
