# 图谱数据格式规范

> 本文档定义 `graph-data.js` 中所有字段的精确格式。每次更新图谱前必须核对。

## 文件结构

```js
window.GRAPH_DATA = {
  "nodes": [ ... ],   // 节点数组
  "links": [ ... ]    // 边数组（注意：键名是 "links" 不是 "edges"）
};
```

文件编码 UTF-8，2 空格缩进，无尾随逗号。

---

## 节点（Node）完整字段

```json
{
  "id": "<string>",
  "name": "<string>",
  "type": "person | company | product_paper",
  "description": "<string>",
  "degree": <integer>,
  "composite_weight": <float>,
  "group_id": "<string>",
  "group_name": "<string>",
  "tags": ["<string>", ...]
}
```

### 各字段说明

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `id` | 是 | string | 唯一标识符，ASCII 字符 + 下划线，格式见 `node-naming.md` |
| `name` | 是 | string | 显示名称。中国人：`"中文名 English Name"`；外国人：`"English Name"`; 公司：`"中文名 English Name"` |
| `type` | 是 | string | `"person"` / `"company"` / `"product_paper"` |
| `description` | 是 | string | 100-200 字简介，包含关键时间节点、机构、成果 |
| `degree` | 是 | integer | **运行时字段**，由实际边数计算。新建时填 0，保存时统一重算 |
| `composite_weight` | 是 | float | **运行时字段**，= degree / maxDegree。新建时填 0，保存时统一重算 |
| `group_id` | 是 | string | 五条路线之一：`"jepa"` / `"spatial"` / `"sim"` / `"active_inf"` / `"causal"` |
| `group_name` | 是 | string | 对应的中文路线全名 |
| `tags` | 是 | array | 字符串数组，第一项必为 `group_name`，可追加额外标签 |

### type 分类

| type | 含义 | 当前数量 | 示例 |
|------|------|---------|------|
| `person` | 研究者 / 企业家 | ~349 | `Yann_LeCun`, `FeiFei_Li` |
| `company` | 公司 / 研究机构 / 实验室 | ~88 | `Meta_FAIR`, `NVIDIA`, `World_Labs` |
| `product_paper` | 论文 / 产品 / 开源项目 / 概念 | ~132 | `V_JEPA2`, `Cosmos`, `Genie1` |

---

## 边（Link）完整字段

```json
{
  "source": "<node_id>",
  "target": "<node_id>",
  "relation_type": "<string>",
  "label": "<string>",
  "weight": <integer>
}
```

### 各字段说明

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `source` | 是 | string | 源节点 ID，必须在 nodes 中存在 |
| `target` | 是 | string | 目标节点 ID，必须在 nodes 中存在 |
| `relation_type` | 是 | string | 7 种关系类型之一（见下表） |
| `label` | 是 | string | 具体关系描述（如 `"PhD advisor"`、`"联合创始人"`） |
| `weight` | 是 | integer | 1-5 整数，表示关系强弱 |

### 7 种 relation_type

| 值 | 中文 | 方向 | label 示例 |
|----|------|------|-----------|
| `mentors` | 指导 | 导师→学生 | `"PhD advisor"`, `"博士后导师"` |
| `collaborates` | 合作 | ↔ | `"共同发表"`, `"联合创办 ICLR"` |
| `founded` | 创办 | 人→公司 | `"founder"`, `"联合创始人"` |
| `works_at` | 任职 | 人→机构 | `"教授"`, `"CEO"`, `"研究科学家"` |
| `develops` | 开发/推动 | 人→产品 | `"第一作者"`, `"核心推动者"` |
| `evolves_to` | 演变 | 产品→产品 | `"架构升级"`, `"技术继承"` |
| `related` | 关联 | ↔ | `"理论延续"`, `"技术同源"` |

**注意**：`related` 应慎用——只用于有明确学术/技术渊源的关联，不用于弱间接关系。

### weight 整数尺度

| 权重 | 含义 | 使用场景 |
|------|------|---------|
| 1 | 一般 | 间接关联、弱合作关系 |
| 2 | 明确 | 同事、一般合作、直接任职 |
| 3 | 重要 | 核心合作者、重要产品推动 |
| 4 | 强 | 直属导师、联合创始人、核心团队成员 |
| 5 | 极强 | 创始人-公司、开创性论文第一作者 |

**统一使用整数权重，禁止使用旧的 0.5/0.7/0.9 等小数尺度。**

---

## 技术路线

| group_id | group_name |
|----------|-----------|
| `jepa` | 路线一：JEPA 联合嵌入预测架构 |
| `spatial` | 路线二：空间智能（3D 世界模型） |
| `sim` | 路线三：学习仿真（生成视频 + RL + 基础设施） |
| `active_inf` | 路线四：主动推理（边缘路线） |
| `causal` | 路线五：因果推断（Pearl 因果推理框架） |

---

## 保存前必做的处理

### 重算 degree

```javascript
// 清空所有 degree
nodes.forEach(function(n) { n.degree = 0; });
// 统计每条边的 source 和 target
links.forEach(function(l) {
  var s = nodes.find(function(n) { return n.id === l.source; });
  var t = nodes.find(function(n) { return n.id === l.target; });
  if (s) s.degree++;
  if (t) t.degree++;
});
```

### 重算 composite_weight

```javascript
var maxDeg = Math.max.apply(null, nodes.map(function(n) { return n.degree; }));
nodes.forEach(function(n) {
  n.composite_weight = maxDeg > 0 ? n.degree / maxDeg : 0;
});
```

### JSON 序列化

```javascript
var json = JSON.stringify({ nodes: nodes, links: links }, null, 2);
var output = 'window.GRAPH_DATA = ' + json + ';';
fs.writeFileSync('graph-data.js', output, 'utf8');
```

---

## 校验清单

- [ ] `JSON.parse` 整个数据部分不报错
- [ ] 所有 `links[].source` 在 `nodes[].id` 中存在
- [ ] 所有 `links[].target` 在 `nodes[].id` 中存在
- [ ] 所有 `links[].relation_type` 是 7 种值之一
- [ ] 无重复的 `(source, target, relation_type)` 三元组
- [ ] 所有节点 `degree` >= 实际连接的边数
- [ ] 所有节点 `composite_weight` = degree / maxDegree
- [ ] `tags` 数组第一项为 `group_name`
- [ ] HTML 中的实体数/关系数统计与数据一致
