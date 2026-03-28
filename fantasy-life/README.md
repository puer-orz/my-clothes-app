# 模拟人生 (Fantasy Life & Romance Simulator)

一个基于 AI 驱动的文字冒险游戏平台。包含两个独特的模式：

- **奇幻人生 (Fantasy Life)**: 硬核穿越模拟。进入随机生成的模拟世界，面临高风险的生存挑战。
- **恋爱模拟 (Romance Simulator)**: 细腻的情感互动。在现实背景下与不同性格的对象展开故事。

## 🚀 快速开始

### 在线游玩
游戏支持通过 GitHub Pages 部署。部署成功后，你可以通过 GitHub 提供的链接直接在浏览器中游玩。

### 本地运行
1. 克隆仓库
2. 安装依赖: `npm install`
3. 启动开发服务器: `npm run dev`

## ⚙️ 配置说明
为了运行游戏，你需要在游戏内的**设置**中配置你的 **DeepSeek API Key**。
- 你的 API Key 仅存储在浏览器的 `localStorage` 中，不会上传到任何服务器。
- 请确保你的 DeepSeek 账户有足够的额度。

## 🛠️ 技术栈
- React + Vite
- Tailwind CSS
- Lucide React (图标)
- DeepSeek API (大模型驱动)

## 📦 部署到 GitHub Pages
如果你想把这个项目部署到你自己的 GitHub 页面：
1. 在 GitHub 上创建一个新的仓库。
2. 将本地代码推送到该仓库：
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <你的仓库链接>
   git push -u origin main
   ```
3. 运行部署命令：
   ```bash
   npm run deploy
   ```
4. 在 GitHub 仓库设置的 **Pages** 选项卡中，确保 Source 设置为 `gh-pages` 分支。
