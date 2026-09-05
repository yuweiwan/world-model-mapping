# Physical AI 论文每日更新技术方案

## 目标与边界

首版把“发现论文”和“发布到图谱”分开：采集器只产生候选，候选必须经过审核后才会进入网页。旧的 `graph-data.js` 保持只读，新论文生成到 `paper-data.js`，浏览器加载时合并两层数据。

数据流：官方来源或手动链接 → 统一字段 → 相关性评分与路线分类 → ID/标题去重 → `review_queue.json` → 人工审核 → `approved/papers.json` → `paper-data.js` 与日报 → GitHub Pages。

## 数据来源

- arXiv API：世界模型、Physical AI、具身智能、VLA 和机器人基础模型等预印本。
- OpenReview API v2：ICLR、NeurIPS、CoRL 的公开会议论文；会议 ID 在 `config/sources.json` 中逐年更新。
- 手动收件箱：把 arXiv、团队官网论文页或技术报告链接加入 `data/inbox.json`。
- 团队公众号只作为线索。确认原始论文、团队官网或会议页面后再审核入库，公众号文章本身不作为论文事实的唯一证据。

## 统一记录与关系

论文记录必须包含标题、作者、来源、发表状态与日期、技术路线、相关性评分、审核状态和证据链接。完整约束见 `data/paper.schema.json`。

网页新增 `paper` 和 `tech_report` 两类。首版只自动创建有明确证据的关系：论文到已存在人物的 `authored_by`，论文到已存在关键团队的 `released_by`。技术路线继续使用节点的 `group_id`，避免为同一分类再造一套路线节点。

## 日常 SOP

1. 每天 08:15（Asia/Shanghai）运行 GitHub Actions，抓取最近 72 小时。
2. 规则计算相关性和路线；配置 LLM 密钥时生成中文标题、摘要与贡献点。
3. 新候选进入 `data/review_queue.json`，Action 创建审核 PR，不直接更新线上图谱。
4. 审核人核对标题、作者、日期、venue、原文链接、路线和关系后执行：

```bash
python scripts/pipeline.py review --approve arxiv:2608.01234 --reviewer your-name --route action_ground
python scripts/pipeline.py review --reject arxiv:2608.01234 --reviewer your-name --notes "主题不相关"
```

5. 审核通过会自动重建 `paper-data.js` 与当日日报；合并 PR 后 GitHub Pages 更新。

## 手动新增

在 `data/inbox.json` 的 `items` 中加入 `{ "url": "..." }`。arXiv 链接通过 API 解析；普通论文页读取标准 citation meta 标签。也可以补充 `title`、`authors`、`published_at`、`venue`、`status` 等字段。下一次 `collect` 后系统写回 `processed_at` 与 `record_id`。

## 命令

```bash
python scripts/pipeline.py collect --since-hours 72
python scripts/pipeline.py validate
python scripts/pipeline.py export
python scripts/pipeline.py digest
python scripts/pipeline.py run --since-hours 72
python -m unittest discover -s tests -v
```

LLM 增强是可选项，使用 OpenAI-compatible Chat Completions 接口：`WM_LLM_API_KEY`、`WM_LLM_MODEL`、`WM_LLM_BASE_URL`。没有密钥时，采集、分类、审核和发布仍可完整运行。

## 后续扩展

- 接入 CVF、PMLR、RSS/Atom 等更多官方源，并建立 venue 年度维护表。
- 增加 DOI/作者 ORCID/机构 ROR 实体对齐，处理同名作者和机构别名。
- 做独立审核后台或 GitHub PR 评论指令，降低命令行审核成本。
- 在明确推送渠道后增加企业微信、邮件或 Slack 适配器；日报文件保持渠道无关。
