#!/usr/bin/env python3
"""v25 增量更新：Pushmeet Kohli (Philip Torr学生/DeepMind VP) + AlphaFold"""
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

add_node("Pushmeet_Kohli",
    "Pushmeet Kohli\\nGoogle DeepMind VP of Research",
    "person_overseas", "sim",
    "Oxford Brookes 博士 (2007)，师从 Philip Torr (FRS/FREng)。"
    "Google DeepMind VP of Research。主导或参与：AlphaFold (2024诺贝尔化学奖)、"
    "AlphaCode、AlphaMissense、SynthID。TIME 100 AI 最具影响力人物 (2023)。"
    "作为研究副总裁，直接管辖 DeepMind 的世界模型、具身智能、科学 AI 三大研究方向，"
    "为 Genie/Dreamer/SIMA 等项目提供顶级研究环境与战略支持。",
    bold=True
)

# ═══════════════════════════════════════════════════════════════
# 2. 里程碑节点
# ═══════════════════════════════════════════════════════════════
print("\n=== 里程碑节点 ===")

add_node("AlphaFold",
    "AlphaFold 3 (2024)\\n诺贝尔化学奖\\n蛋白质结构预测",
    "milestone", "sim",
    "Google DeepMind 发布。从氨基酸序列预测蛋白质3D结构，"
    "2024年获诺贝尔化学奖（Demis Hassabis & John Jumper）。"
    "虽非直接世界模型，但其核心思想——从隐空间表征预测3D物理结构——"
    "与 JEPA/空间智能 共享深层方法论基础。"
    "被视为 AI for Science 的里程碑，推动了科学世界模型的发展。"
)

# ═══════════════════════════════════════════════════════════════
# 3. 新增边
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增关系边 ===")

# ── 师承 ──
add_edge("Philip_Torr", "Pushmeet_Kohli", "mentorship",
    "博士导师 (Oxford Brookes, 2007)", "tier1")

# ── 雇佣 ──
add_edge("Pushmeet_Kohli", "Google_DeepMind", "employed",
    "VP of Research / 管辖世界模型+具身智能+科学AI", "tier1")

# ── 同事 ──
add_edge("Pushmeet_Kohli", "Demis_Hassabis", "lab",
    "VP of Research ↔ CEO / 共同推动科学AI战略", "tier1")
add_edge("Pushmeet_Kohli", "Koray_Kavukcuoglu", "lab",
    "同为 DeepMind VP / AlphaFold+AlphaGo 双线", "tier2")

# ── 产品 ──
add_edge("Pushmeet_Kohli", "AlphaFold", "maintainer",
    "研究负责人 / 2024诺贝尔化学奖", "tier1")
add_edge("Google_DeepMind", "AlphaFold", "maintainer",
    "DeepMind 出品 / 2024诺贝尔化学奖", "tier1")
add_edge("Demis_Hassabis", "AlphaFold", "maintainer",
    "DeepMind CEO / 诺贝尔化学奖共同得主", "tier1")

# ── 世界模型连接 ──
add_edge("AlphaFold", "Model_Based_RL", "related",
    "隐空间→3D物理结构预测 / 与JEPA共享方法论基础", "tier2")
add_edge("Pushmeet_Kohli", "Model_Based_RL", "maintainer",
    "DeepMind 研究VP / 管辖Genie+Dreamer+SIMA", "tier2")

# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 29
data["meta"]["updated"] = "2026-05-26"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v29: Pushmeet Kohli(Philip Torr学生/DeepMind VP of Research)+AlphaFold(2024诺贝尔化学奖)，打通Torr→DeepMind管理层师承链")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v25 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
for n in new_nodes_added:
    print(f"    - {n}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
