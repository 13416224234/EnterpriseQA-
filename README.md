# EnterpriseQA 企业知识库问答系统

基于 LangChain + RAG 架构的企业级智能问答平台。

## 技术栈

`Vue3` `Python Flask` `LangChain` `RAG` `ChromaDB` `Ollama` `SQLite`

## 功能

- 文档上传与自动向量化（PDF/Word/Excel/Markdown）
- Chroma 向量数据库语义检索
- Ollama 本地大模型（Qwen3.5-4b）智能问答
- 对话管理与多轮对话上下文
- 管理员后台（用户管理、文档管理、数据统计）
- JWT 身份认证与权限控制

## 快速启动

### 后端
```bash
cd server
pip install -r requirements.txt
python app.py
```

### 前端
```bash
cd client
npm install
npm run dev
```

### 默认账号
- 管理员：admin / 123456

## 项目结构
```
server/   - Flask 后端 API
client/   - Vue3 前端界面
scripts/  - 系统初始化脚本
```