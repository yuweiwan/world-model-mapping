# 世界模型 · 技术全景图谱

交互式知识图谱，展示世界模型（World Models）领域的人物、公司、产品与学术脉络。

**在线访问：https://yuweiwan.github.io/world-model-mapping/**

## 数据概览

| 指标 | 当前值 |
|------|--------|
| 实体数 | 566 |
| 关系数 | 1,191 |
| 关系类型 | 7 种 |
| 技术路线 | 5 条 |

### 7 种关系类型

| 类型 | 中文 | 示例 |
|------|------|------|
| `develops` | 开发/推动 | 人物 → 产品/概念 |
| `collaborates` | 合作 | 人物 ↔ 人物/机构 |
| `mentors` | 指导 | 导师 → 学生 |
| `founded` | 创办 | 人物 → 公司 |
| `works_at` | 任职 | 人物 → 公司/机构 |
| `related` | 关联 | 概念 ↔ 概念 |
| `evolves_to` | 演变 | 技术 → 后继技术 |

### 5 条技术路线

1. **JEPA** — 联合嵌入预测架构（LeCun）
2. **空间智能** — 3D 世界模型（李飞飞）
3. **学习仿真** — 生成视频 + RL + 基础设施
4. **主动推理** — 自由能原理（Friston）
5. **因果推断** — Pearl 因果推理框架

## 本地预览

```bash
# 任意静态服务器
python -m http.server 8080
# 浏览器打开 http://localhost:8080
```

## 数据结构

数据存储在 `graph-data.js` 中，格式：

```js
window.GRAPH_DATA = {
  "nodes": [
    { "id": "...", "name": "显示名称", "type": "person|company|product_paper",
      "description": "...", "degree": N, "composite_weight": 0.X,
      "group_id": "路线ID", "group_name": "路线名称", "tags": [...] }
  ],
  "links": [
    { "source": "node_id", "target": "node_id",
      "relation_type": "develops|collaborates|mentors|founded|works_at|related|evolves_to",
      "label": "关系说明", "weight": 0.X }
  ]
};
```

## 更新数据

1. 直接编辑 `graph-data.js`（或用 Node.js 脚本批量操作）
2. 确保 `relation_type` 使用上述 7 种值之一
3. 确保所有 `source`/`target` 对应的节点 ID 存在
4. 更新 `World_Models_TechMap.html` 中的统计数字
5. `git push` 到 `main` 分支，GitHub Pages 自动部署

## 技术栈

- [Cytoscape.js](https://js.cytoscape.org/) — 图可视化引擎
- [fcose](https://github.com/iVis-at-Bilkent/cytoscape.js-fcose) — 力导向布局
- GitHub Pages — 静态托管

## License

MIT
