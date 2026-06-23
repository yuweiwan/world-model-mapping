# 世界模型 · 技术全景图谱

交互式 Cytoscape 知识图谱，展示世界模型（World Models）领域的人物、公司、产品与学术脉络。

## 在线访问

**https://yuweiwan.github.io/world-model-mapping/**

部署于 GitHub Pages（纯静态站点）。搜索、筛选、缩放、节点详情等交互均在浏览器内完成，无需后端。

## 本地预览

```bash
# 任意静态服务器，例如 Python
python -m http.server 8080
# 浏览器打开 http://localhost:8080
```

## 更新数据

1. 编辑 `World_Models_data.json` 或运行 `update_v*.py` 增量脚本
2. 运行 `python rebuild_v4.py` 重新生成 `graph-data.js`
3. 提交并 push，Pages 会自动更新
