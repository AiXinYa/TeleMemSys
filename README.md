# 电信运维记忆系统

仿 Claude Code 记忆架构，为电信网络运维构建"懂我·懂角色·懂网"的持久化记忆系统。

## 快速启动

```bash
pip install -r requirements.txt
python run.py                    # http://localhost:8000
python run.py --port 8080        # 指定端口
python run.py --reset            # 重置数据
```

## 功能特性

- **10种记忆类型**: 用户画像/交互偏好/操作习惯/会话上下文/角色权限/外部资源/网络模型/性能基线/故障知识/变更状态
- **智能提取**: 只从用户发言提取，自动过滤通用知识/标准/厂商文档，剥离think过程
- **记忆融合**: 新知识与已有记忆自动匹配→判断关系→按可信度裁决冲突→merge_history审计
- **候选池**: 不确定的知识暂存，多次命中后激活（用户信息2次/网络知识3次）
- **工具路由**: 自动分流到记忆/搜索/安全工具，搜索3GPP标准/厂商文档/通用知识
- **安全防护**: 四级风险评估（绿/黄/橙/红）+ 前置检查 + 回退方案
- **追问选择题**: 信息不够时以按钮形式追问，用户点选后自动提取记忆
- **蒸馏命令**: 对话中输入 `/dream` 直接执行记忆整理

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| LLM_URL | http://71.77.143.9:16313/v1/chat/completions | LLM接口 |
| LLM_MODEL | Qwen3-32B | 模型名 |
| SEARCH_API_KEY | (空=模拟搜索) | Tavily/SerpAPI密钥 |
| PORT | 8000 | 服务端口 |

## 测试

```bash
python tests/test_all.py           # Mock模式 (74项)
REAL_LLM=1 python tests/test_all.py  # 真实LLM模式
```

## 项目结构

```
src/
├── memory/          类型定义 + 存储 + 召回
├── extraction/      提取 + 融合 + 候选池 + 蒸馏 + 技能对接
├── tools/           工具路由 + 搜索
├── safety/          安全防护
└── api/             对话引擎 + FastAPI + 会话持久化
web/index.html       React SPA
tests/test_all.py    自动化测试
```
