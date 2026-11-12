# 上架前检查清单

## 必须准备

- Chrome Web Store 开发者账号
- 扩展 zip：在仓库根目录打包，只包含插件运行需要的文件（见下方命令）
- 隐私政策 URL：把 `privacy-policy.md` 发布到可公开访问的网址
- 商店图标：`icons/icon128.png`
- 截图：`screenshot-1` ~ `screenshot-4`（1280x800，无透明通道）
- 小宣传图：`small-promo-tile-440x280.png`
- 大宣传图（可选）：`marquee-promo-tile-1400x560.png`
- 详细说明、权限说明、审核测试说明：见 `listing.md`

打包命令（在仓库根目录运行）：

```bash
zip -r inkbox.zip manifest.json content.js page-hook.js deepseek-content.js deepseek-page-hook.js popup.html popup.js popup.css icons
```

## 素材说明

- 图标和截图都由 `design/` 里的 HTML 设计稿用 Chrome 无头模式渲染，运行 `python store-assets/design/render.py` 可重新生成。
- 截图里的聊天页面是中性风格的示意界面，没有使用豆包或 DeepSeek 的标志和界面；弹窗部分直接渲染插件真实的 `popup.html`，悬浮按钮和导出文件内容与插件实际输出一致。
- 如果想换成真实截图：在真实页面上截 1280x800 的图，替换同名文件即可。

## 本版注意事项

- 全新品牌与界面：墨匣，黑白灰视觉；功能与内部消息协议保持不变。
- 悬浮按钮文案为「墨匣 · 导出对话」，导出文件前缀为 `inkbox-`。
- 弹窗改为格式单选（Markdown / JSON）+ 独立导出按钮；读取方式和滚动兜底不再显示，弹窗固定使用接口读取。
- 「只导出我的提问」默认关闭，可在弹窗中开启。
- 界面和导出文件都不显示版本号；Markdown 仅保留「导出工具：墨匣」。
- 审核测试时勾选「只导出我的提问」导出一次，确认文件里没有 AI 回复。

## 隐私字段建议

是否收集用户数据：
建议按实际情况选择“是”，因为扩展会读取当前页面对话内容用于本地导出。

数据类型：
选择“网页内容”或平台表单中最接近“网站内容/用户内容”的选项；如果表单有“身份验证信息”，说明扩展会在页面内使用登录 token 向 `chat.deepseek.com` 请求会话历史，但不保存、不传出。

用途：
单一用途：导出用户当前对话为本地文件。

是否传输到第三方：
不传输给开发者服务器；接口模式只请求当前网站（`doubao.com`、`chat.deepseek.com`），用于获取用户有权访问的对话数据。

是否用于广告：
否。

是否出售数据：
否。
