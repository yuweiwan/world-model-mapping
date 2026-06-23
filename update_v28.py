#!/usr/bin/env python3
"""v28 增量更新：自然意志(丁宁/具身智能大脑)+丁宁人物节点"""
import json, os, subprocess

SRC = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SRC, "World_Models_data.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

existing_ids = {n["id"] for n in data["nodes"]}

new_nodes_added = []
new_edges_added = []

def add_node(nid, label, ntype, group, description, bold=False):
    if nid in existing_ids:
        print(f"  ⏭ 跳过重复: {nid}")
        return False
    existing_ids.add(nid)
    data["nodes"].append({
        "id": nid, "label": label, "type": ntype,
        "group": group, "bold": bold, "description": description
    })
    new_nodes_added.append(nid)
    print(f"  ✅ 新增: {nid}")
    return True

def add_edge(source, target, etype, label, strength="tier2"):
    if source not in existing_ids:
        print(f"  ⚠ 边源节点不存在: {source}")
        return
    if target not in existing_ids:
        print(f"  ⚠ 边目标节点不存在: {target}")
        return
    for e in data["edges"]:
        if e["source"] == source and e["target"] == target and e["type"] == etype:
            print(f"  ⏭ 跳过重复边: {source} → {target}")
            return
    data["edges"].append({
        "source": source, "target": target, "type": etype,
        "label": label, "strength": strength
    })
    new_edges_added.append(f"{source} → {target}")

# ═══════════════════════════════════════════════════════════════
# 1. 人物节点
# ═══════════════════════════════════════════════════════════════
print("\n=== 人物节点 ===")

add_node("Ding_Ning",
    "丁宁 Ding Ning\\n自然意志创始人\\n清华大学助理教授",
    "person_overseas", "sim",
    "华中科技大学本科，清华大学计算机系博士（2018-2023，导师郑海涛、刘知远），"
    "清华大学电子系博士后（2023-2025，合作导师周伯文）。"
    "2025年5月起任清华大学电子工程系助理教授、博导。"
    "OpenBMB核心贡献者，GitHub累计25000+星标。"
    "谷歌学术引用超1万次，2023年Nature Machine Intelligence封面文章（年度最高引）。"
    "代表工作：Ultra系列对齐、TTRL测试时强化学习、PRIME密集奖励RL。"
    "2026年1月创立自然意志，定位具身智能「大脑」，走「世界模型+强化学习」路线。",
    bold=True
)

# ═══════════════════════════════════════════════════════════════
# 2. 公司节点
# ═══════════════════════════════════════════════════════════════
print("\n=== 公司节点 ===")

add_node("Natural_Will",
    "自然意志 Natural Will\\n具身智能大脑 (2026.1)\\n天使轮估值¥40亿",
    "company_overseas", "sim",
    "2026年1月由清华助理教授丁宁创立于北京。定位具身智能「大脑」——"
    "让AI理解物理世界规律并自主推理决策，区别于传统机器人公司的「身体」路线。"
    "核心技术路径：「世界模型+强化学习」，致力于降低对真实物理数据的依赖，"
    "让AI用更少数据掌握更多物理理解。打造可解释大脑——不仅能决策，还能解释为什么这么做。"
    "天使轮估值40亿元人民币，IDG资本/真格基金/峰瑞资本联合投资。"
    "成立不足4月即获顶级VC押注，被视为国内具身大脑赛道最稀缺的团队。"
)

# ═══════════════════════════════════════════════════════════════
# 3. 新增边
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增关系边 ===")

add_edge("Ding_Ning", "Natural_Will", "founded",
    "创始人兼CEO (2026.1至今)", "tier1")

# ── 技术路线 ──
add_edge("Natural_Will", "Model_Based_RL", "maintainer",
    "「世界模型+强化学习」核心路线 / 具身大脑", "tier1")
add_edge("Ding_Ning", "Model_Based_RL", "maintainer",
    "PRIME/TTRL密集奖励RL→具身世界模型", "tier2")

# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 32
data["meta"]["updated"] = "2026-05-26"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v32: 自然意志Natural Will(丁宁/清华系/具身智能大脑/天使轮¥40亿/IDG+真格+峰瑞)，「世界模型+RL」路线新势力")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v28 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
for n in new_nodes_added:
    print(f"    - {n}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
