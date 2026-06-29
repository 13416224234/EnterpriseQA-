<p align="center">
  <h1 align="center">🏢 EnterpriseQA</h1>
  <p align="center">基于 LangChain + RAG 架构的企业智能知识库问答系统</p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Vue-3.0-4FC08D?logo=vue.js" alt="Vue">
  <img src="https://img.shields.io/badge/Python-Flask-000000?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/LangChain-RAG-121212?logo=langchain" alt="LangChain">
  <img src="https://img.shields.io/badge/Ollama-Qwen3.5-000000?logo=ollama" alt="Ollama">
  <img src="https://img.shields.io/badge/ChromaDB-Vector-4B8BBE?logo=python" alt="ChromaDB">
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite" alt="SQLite">
</p>

---

## ✨ 功能特性

| 模块 | 功能 |
|------|------|
| 📄 文档管理 | 支持 PDF / Word / Excel / Markdown 多格式上传与自动向量化 |
| 🔍 语义检索 | Chroma 向量数据库实现文档语义相似度搜索 |
| 🤖 智能问答 | 集成 Ollama 本地大模型（Qwen3.5-4b），基于知识库内容生成精准答案 |
| 💬 对话管理 | 多轮对话上下文、历史记录、来源引用展示 |
| 👥 权限控制 | JWT 身份认证，管理员 / 普通用户双角色 |
| 📊 管理后台 | 用户管理、文档管理、数据统计面板 |

---

## 🛠 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue3 + Element Plus + Pinia + Axios |
| 后端 | Python Flask + SQLAlchemy + JWT |
| AI | LangChain + Ollama (Qwen3.5-4b) + nomic-embed-text |
| 数据库 | SQLite + ChromaDB |
| 部署 | Docker + docker-compose |

---

## 🚀 快速启动

### 环境要求

- Python 3.10+
- Node.js 18+
- Ollama（运行中）
- Qwen3.5-4b 和 nomic-embed-text 模型已下载

### 一键启动

```bash
# Windows 双击运行
start.bat
```

### 手动启动

**后端**
```bash
cd server
pip install -r requirements.txt
python app.py
# 运行在 http://localhost:5000
```

**前端**
```bash
cd client
npm install
npm run dev
# 运行在 http://localhost:5173
```

### 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | 123456 |

---

## 📂 项目结构

```
EnterpriseQA/
├── server/               # Flask 后端
│   ├── routes/           # API 路由
│   ├── models/           # 数据模型
│   ├── services/         # RAG 服务 + 向量化服务
│   ├── scripts/          # 初始化脚本
│   └── app.py            # 入口文件
├── client/               # Vue3 前端
│   └── src/
│       ├── views/        # 页面组件
│       ├── components/   # 公共组件
│       └── api/          # Axios 封装
├── docker-compose.yml    # Docker 编排
├── start.bat             # 一键启动脚本
└── README.md
```

---

## 📸 界面预览

- **智能问答**：对话列表 + 实时对话，AI 回答可展开思考过程，引用来源自动标注
- **文档管理**：拖拽上传 + 多文件批量上传，自动向量化
- **管理后台**：用户管理 + 数据统计图表

---

## 📝 许可证

MIT License