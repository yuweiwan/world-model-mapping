# 世界模型 · 技术全景图谱

这是一个面向世界模型（World Models）、具身智能和 Physical AI 的交互式知识图谱。

它一方面整理领域中的人物、公司、产品、论文和技术路线，另一方面提供一套可以每天运行的论文采集流水线：自动发现新内容、去重和分类，但必须经过人工审核后才会发布到网页。

**在线版本：** https://yuweiwan.github.io/world-model-mapping/

## 这个项目能做什么

- 在一张交互式图谱中查看人物、公司、产品、论文和技术报告之间的关系。
- 按节点类型、技术路线，以及最近 7 天或 30 天筛选内容。
- 从 arXiv、OpenReview 和手动收件箱发现新论文。
- 对候选内容进行相关性评分、技术路线分类和重复检测。
- 通过人工批准或拒绝，避免未经确认的内容直接进入正式图谱。
- 自动生成网页数据和每日论文摘要。
- 使用 GitHub Actions 每天运行采集任务，并在有新候选时创建审核 PR。
- 可选调用 OpenAI-compatible 接口生成中文标题、摘要和贡献点。

## 数据概览

<!-- AUTO-GENERATED:STATS:START -->
| 指标 | 当前值 |
| --- | ---: |
| 实体数 | 695 |
| 关系数 | 1,357 |
| 关系类型 | 9 种 |
| 技术路线 | 9 条 |
| 已审核论文/技术报告 | 36 篇 |

基础图谱包含 661 个节点和 1,335 条关系；论文更新层新增 34 个节点。以上统计由 `python scripts/pipeline.py export` 自动更新。
<!-- AUTO-GENERATED:STATS:END -->

网页顶部的统计会在加载数据后动态计算。README 中的概览会在导出图谱时自动更新，不需要手工修改数字。

## 它是怎样工作的

```text
arXiv / OpenReview / 团队官网 / 手动线索
                    │
                    ▼
             采集与字段标准化
                    │
                    ▼
       相关性评分、路线分类、团队匹配
                    │
                    ▼
          来源 ID 与标准化标题去重
                    │
                    ▼
          data/review_queue.json
                    │
              人工审核闸门
              ┌─────┴─────┐
              ▼           ▼
           批准记录     拒绝记录
              │           │
              ▼           ▼
 data/approved/papers.json data/rejected.json
              │
              ▼
    paper-data.js + 每日摘要 + 网页
```

这里最重要的规则是：**采集不等于发布。**

`collect` 只会把新候选放进待审核队列。只有执行 `review --approve` 后，记录才会进入正式数据，并出现在网页和日报中。微信公众号和媒体文章只作为发现线索；正式记录应尽量使用论文原文、会议页面或团队官网作为一手来源。

## 快速开始

### 1. 环境要求

- Git
- Python 3.12，Python 3.11 通常也可以运行
- 一个现代浏览器

项目没有 npm 依赖，也不需要前端构建。Python 流水线只使用标准库。

### 2. 克隆项目

```powershell
git clone https://github.com/yuweiwan/world-model-mapping.git D:\world-model-mapping
Set-Location D:\world-model-mapping
```

如果已经克隆过，只需要进入项目目录：

```powershell
Set-Location D:\world-model-mapping
```

在 Windows 的传统 CMD 中，切换盘符和目录可以使用：

```bat
cd /d D:\world-model-mapping
```

### 3. 校验项目

```powershell
python scripts/pipeline.py validate
```

正常结果应包含：

```json
{
  "ok": true,
  "errors": [],
  "warnings": []
}
```

### 4. 启动本地网页

```powershell
python -m http.server 8080
```

浏览器打开：

- http://localhost:8080/
- 或 http://localhost:8080/World_Models_TechMap.html

服务器运行时终端会一直停在 `Serving HTTP...`，这是正常现象。按 `Ctrl+C` 可以停止服务器。需要继续运行流水线命令时，可以另开一个 PowerShell 窗口。

## 网页怎么用

- 顶部显示当前实体、关系和论文更新数量。
- 左侧搜索框可以搜索人物、公司、产品和论文标题。
- “类型筛选”可以单独显示人物、公司、历史论文、新论文或技术报告。
- “技术路线”可以筛选某一类世界模型方向。
- “最近 7 天”和“最近 30 天”只显示对应时间窗口内的新论文和技术报告。
- 点击节点可以查看简介、作者、团队、venue、发布日期、原文和 PDF 链接。
- 图例中的路线数和关系类型数由当前配置动态计算。

如果审核后网页没有立即变化，请先强制刷新浏览器（Windows 通常为 `Ctrl+F5`），并确认本地 HTTP 服务器启动在项目根目录。

## 每日使用流程

### 第一步：自动采集最近内容

```powershell
python scripts/pipeline.py collect --since-hours 72
```

这条命令会：

1. 读取 `config/sources.json` 中启用的数据源。
2. 获取最近 72 小时的论文。
3. 统一标题、作者、摘要、来源、venue 和发布日期等字段。
4. 计算相关性分数并推荐技术路线。
5. 使用来源 ID 和标准化标题去重。
6. 把满足阈值的新候选写入 `data/review_queue.json`。
7. 把运行结果写入 `data/last_ingest_report.json`。

输出中的常见字段：

| 字段 | 含义 |
| --- | --- |
| `fetched` | 本次从所有来源拿到的记录数 |
| `queued` | 新进入审核队列的数量 |
| `duplicates` | 已存在或本次重复的数量 |
| `ignored_low_score` | 相关性分数不足而未入队的数量 |
| `pending_total` | 当前待审核总数 |
| `errors` | 单个来源的错误；其他来源仍可继续运行 |

联网采集可能需要几十秒。命令暂时没有输出不一定是卡住，请等待它返回 JSON 结果。

### 第二步：查看待审核论文

最直接的方法是打开 `data/review_queue.json`。在 PowerShell 中也可以显示精简表格：

```powershell
$d = Get-Content data\review_queue.json -Raw | ConvertFrom-Json
$d.papers | ForEach-Object {
  [PSCustomObject]@{
    id = $_.id
    score = $_.taxonomy.relevance_score
    route = $_.taxonomy.route_id
    title = $_.title
  }
} | Format-Table -AutoSize
```

审核时建议检查：

- 是否真正与世界模型、具身智能或 Physical AI 相关。
- 标题、作者、摘要、发布日期和原始链接是否可靠。
- 是正式会议论文、arXiv 预印本，还是团队技术报告。
- 推荐技术路线是否正确。
- 是否与图谱中已有记录重复。
- 二手媒体线索是否已经回到一手来源核实。

### 第三步：批准候选

```powershell
python scripts/pipeline.py review `
  --approve arxiv:2608.01234 `
  --reviewer your-name `
  --route action_ground `
  --notes "与 VLA 和机器人动作控制直接相关"
```

批准时可以通过 `--route` 修正自动分类。批准操作会自动：

- 从待审核队列移除记录。
- 写入 `data/approved/papers.json`。
- 记录审核人、审核时间和备注。
- 重新生成 `paper-data.js`。
- 更新 README 数据概览。
- 重新生成当日摘要。

一次批准多篇论文：

```powershell
python scripts/pipeline.py review `
  --approve arxiv:2608.01234 arxiv:2608.05678 `
  --reviewer your-name `
  --route latent_wm
```

同一条命令中的论文会使用同一个路线和审核备注。路线不同的论文应分开审核。

### 第四步：拒绝候选

```powershell
python scripts/pipeline.py review `
  --reject arxiv:2608.01234 `
  --reviewer your-name `
  --notes "核心贡献是通用图像压缩，与图谱主题关联不足"
```

拒绝记录会进入 `data/rejected.json`，以后再次采集到同一来源 ID 或标题时会被识别为重复项，不会反复进入队列。

### 第五步：生成日报

批准论文时日报会自动更新，也可以单独运行：

```powershell
python scripts/pipeline.py digest
```

生成文件：

- `data/daily/latest.json`
- `data/daily/latest.md`
- `data/daily/YYYY-MM-DD.md`

可以使用 PowerShell 检查某篇论文是否进入日报：

```powershell
Select-String -Path data\daily\latest.md -Pattern "论文标题关键词"
```

### 第六步：校验与测试

```powershell
python scripts/pipeline.py validate
python -m unittest discover -s tests -v
```

`validate` 会检查记录字段、审核状态、路线 ID 和图关系引用。单元测试会检查 arXiv/OpenReview 解析、分类、图谱导出、团队关系和 README 自动统计。

### 一条命令运行完整流程

```powershell
python scripts/pipeline.py run --since-hours 72
```

`run` 会依次执行采集、图谱导出、日报生成和数据校验。它不会自动批准候选，新的记录仍然只会进入待审核队列。

## 手动添加论文或技术报告

自动检索不可能覆盖所有团队官网、公众号线索和技术博客。遇到这类内容时，将一手来源链接加入 `data/inbox.json`。

### arXiv 链接

```json
{
  "url": "https://arxiv.org/abs/2608.01234",
  "note": "来自团队公众号的论文线索"
}
```

下一次执行 `collect` 时，系统会通过 arXiv API 补齐元数据。

### 团队官网或技术博客

普通网页会优先读取 `citation_*`、Open Graph 和 description 元标签。如果网页没有完整元数据，可以手动补充：

```json
{
  "url": "https://example.com/blog/new-model",
  "note": "来自行业媒体的线索，已改用团队官网作为一手来源",
  "title": "Example Model: An Embodied Foundation Model",
  "authors": ["Example Team"],
  "abstract": "A concise factual summary containing the method, task and main result.",
  "published_at": "2026-08-19T00:00:00Z",
  "venue": "Example Team Technical Blog",
  "status": "technical_report"
}
```

处理成功后，系统会自动向该条目写入：

```json
{
  "processed_at": "2026-08-20T01:20:10Z",
  "record_id": "manual:examplemodelanembodiedfoundationmodel"
}
```

存在 `processed_at` 的条目不会重复处理。如果需要重新测试该条目，应先确认它没有进入 approved、rejected 或 review queue，再移除 `processed_at` 和 `record_id`。

## 技术路线

当前使用 9 个 `group_id`：

| 路线 ID | 含义 |
| --- | --- |
| `jepa` | JEPA 联合嵌入预测架构 |
| `spatial` | 空间智能与 3D 表征 |
| `latent_wm` | 隐空间动力学与规划 |
| `interactive_wm` | 可交互世界模型 |
| `action_ground` | 动作对齐、VLA 与具身控制 |
| `gen_simulator` | 生成式世界模拟 |
| `phys_engine` | 物理仿真引擎 |
| `active_inf` | 主动推理 |
| `causal` | 因果推断 |

路线配置、关键词权重和关键团队名单位于 `config/sources.json`。自动分类只是审核建议，最终路线由审核人确认。

## 数据与文件结构

| 路径 | 用途 |
| --- | --- |
| `World_Models_TechMap.html` | Cytoscape 图谱页面、筛选和详情面板 |
| `graph-data.js` | 原有人工维护的基础人物、公司和产品图谱 |
| `paper-data.js` | 从已批准论文生成的增量图谱数据 |
| `config/sources.json` | 数据源、关键词、阈值、路线和关键团队配置 |
| `data/inbox.json` | 手动提交的论文或技术报告线索 |
| `data/review_queue.json` | 等待人工审核的候选记录 |
| `data/approved/papers.json` | 已批准并允许发布的正式记录 |
| `data/rejected.json` | 已拒绝记录及原因 |
| `data/last_ingest_report.json` | 最近一次采集报告 |
| `data/daily/` | 每日摘要 JSON 和 Markdown |
| `data/paper.schema.json` | 统一论文字段规范 |
| `scripts/pipeline.py` | 采集、审核、导出、日报和校验 CLI |
| `scripts/wm_pipeline.py` | 流水线核心实现 |
| `tests/` | 解析、分类、导出和数据一致性测试 |
| `.github/workflows/` | CI 和每日自动采集任务 |

基础节点类型为 `person`、`company`、`product_paper`；论文更新层新增 `paper` 和 `tech_report`。

基础关系包括：

- `develops`：开发或推动
- `collaborates`：合作
- `mentors`：指导
- `founded`：创办
- `works_at`：任职
- `related`：关联
- `evolves_to`：技术演变

论文更新层新增：

- `authored_by`：论文指向图谱中已存在的作者
- `released_by`：论文指向图谱中已存在的团队或机构

自动关系只连接能够明确匹配的已有节点，不会仅凭相似名称创建关系。

## 命令速查

| 命令 | 作用 | 主要写入文件 |
| --- | --- | --- |
| `collect --since-hours 72` | 采集、分类和去重 | queue、inbox、ingest report |
| `review --approve ...` | 批准并发布 | approved、queue、paper-data、README、daily |
| `review --reject ...` | 拒绝并留档 | rejected、queue |
| `export` | 重建论文图谱和统计 | paper-data、README |
| `digest` | 生成当日摘要 | data/daily |
| `validate` | 校验数据和关系 | 不写文件 |
| `run --since-hours 72` | collect + export + digest + validate | 上述对应生成文件 |

## GitHub Actions 自动化

项目包含两个工作流：

- `ci.yml`：在 push 和 Pull Request 时运行导出、单元测试，并检查 `paper-data.js` 与 README 统计是否最新。
- `daily-papers.yml`：每天 08:15（Asia/Shanghai）采集最近 72 小时的内容，也支持手动触发。

每日任务的行为：

1. 运行完整流水线。
2. 如果没有新候选，任务正常结束，不创建 PR。
3. 如果发现新候选，创建 `automation/papers-...` 分支。
4. 将待审核队列和采集报告提交到一个审核 PR。
5. 审核人检查候选后再批准或拒绝。

定时任务不会自动批准论文，也不会直接发布未经审核的内容。GitHub 的 schedule 只在默认分支上运行，因此工作流需要先合并到默认分支。

## 可选中文摘要

不配置模型接口时，采集、分类、审核、导出和日报仍可完整运行。需要自动生成中文标题、摘要和贡献点时，配置以下环境变量：

```powershell
$env:WM_LLM_API_KEY = "your-api-key"
$env:WM_LLM_MODEL = "your-model"
$env:WM_LLM_BASE_URL = "https://api.example.com/v1"
```

GitHub Actions 使用：

- Secret：`WM_LLM_API_KEY`
- Variable：`WM_LLM_MODEL`
- Variable：`WM_LLM_BASE_URL`

接口不可用时会在采集报告的 `errors` 中记录 `llm` 错误，不影响原始元数据进入审核流程。

## 常见问题

### `fatal: not a git repository`

说明当前终端不在项目目录。PowerShell 中运行：

```powershell
Set-Location D:\world-model-mapping
git status
```

### `can't open file ... scripts/pipeline.py`

同样是目录不正确。先进入项目根目录，再运行 Python 命令。

### `collect` 很久没有输出

采集需要依次等待 arXiv、OpenReview 和手动网页请求，通常需要几十秒。单个来源超时会被记录到 `errors`，不会阻断其他来源。

### `queued` 为 0

常见原因包括：最近没有新内容、候选已经存在、分数低于阈值，或手动 inbox 条目已经有 `processed_at`。结合 `duplicates`、`ignored_low_score` 和 `errors` 判断即可。

### 端口 8080 被占用

换一个端口：

```powershell
python -m http.server 8081
```

然后打开 http://localhost:8081/ 。

### 批准后网页找不到论文

依次检查：

```powershell
python scripts/pipeline.py validate
Select-String -Path paper-data.js -Pattern "论文标题关键词"
```

确认服务器在项目根目录启动，再使用 `Ctrl+F5` 强制刷新网页。

## 提交与发布

完成审核和校验后：

```powershell
git status
git add .github README.md World_Models_TechMap.html config data paper-data.js scripts tests
git commit -m "feat: update Physical AI paper map"
git push
```

通过 Pull Request 合并到默认分支后，GitHub Pages 会使用仓库中的静态文件发布更新。

## 进一步说明

更详细的来源策略、审核规范和维护 SOP 见 [`docs/DAILY_PAPER_PIPELINE.md`](docs/DAILY_PAPER_PIPELINE.md)。字段约束见 [`data/paper.schema.json`](data/paper.schema.json)。

## 技术栈

- Cytoscape.js
- fCoSE 布局
- Python 3.12 标准库
- GitHub Actions
- GitHub Pages

## License

MIT
