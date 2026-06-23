#!/usr/bin/env python3
"""v15 增量更新：更新 Danijar Hafner（Embo）+ 新增原始 Dreamer 里程碑 + Embo 公司"""
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
    # 去重
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
# 1. 更新 Danijar Hafner 节点
# ═══════════════════════════════════════════════════════════════
print("\n=== 更新 Danijar Hafner ===")
for node in data["nodes"]:
    if node["id"] == "Danijar_Hafner":
        node["label"] = "Danijar Hafner\\nEmbo 创始人\\nDreamer系列作者"
        node["description"] = (
            "多伦多大学博士（导师Jimmy Ba），UC Berkeley访问（Pieter Abbeel），"
            "UCL MRes（导师Karl Friston & Tim Lillicrap）。Dreamer系列算法（v1→v2→v3→v4）的唯一主导作者。"
            "DreamerV3首次在Minecraft中无人类数据取得钻石，登《Nature》。Dreamer 4实现纯离线学习+实时推理。"
            "2025年离开Google DeepMind，创立Embo，获a16z领投超$1亿种子轮，聚焦机器人世界模型。"
        )
        print("  ✅ 更新 Danijar_Hafner label + description")
        break

# ═══════════════════════════════════════════════════════════════
# 2. 新增：原始 Dreamer (2019/2020)
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增原始 Dreamer 里程碑 ===")
add_node("Dreamer",
    "Dreamer (2020)\\n隐空间想象训练\\nICLR 2020",
    "milestone", "sim",
    "Danijar Hafner等人提出。Dreamer系列的开山之作。《Dream to Control: Learning Behaviors by Latent Imagination》。"
    "核心洞察：如果有一个足够好的隐空间世界模型，训练期间根本不需要碰真实环境。"
    "智能体在隐空间（latent space）中想象动作序列和后果，接收奖励信号，更新策略——所有这一切都在想象中完成，没有一次真实交互。"
    "当它最终进入真实环境时，已经知道该做什么。奠定了Dreamer系列「Learn by Imagination」的核心范式。"
)

# ═══════════════════════════════════════════════════════════════
# 3. 新增：Embo 公司
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增 Embo 公司 ===")
add_node("Embo",
    "Embo (2025)\\nDreamer商业化\\n种子轮 >$100M (a16z领投)",
    "company_overseas", "sim",
    "2025年由Danijar Hafner创立，a16z领投超$1亿种子轮。核心技术路线：基于Dreamer系列隐空间世界模型，"
    "构建机器人通用智能。核心理念延续Dreamer范式——让机器人在隐空间想象中学习和规划，"
    "最小化真实环境交互成本。代表了从Google DeepMind学术研究向商业化的关键一跃。"
)

# ═══════════════════════════════════════════════════════════════
# 4. 新增边
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增关系边 ===")

# ── Dreamer 演化链 ──
add_edge("Danijar_Hafner", "Dreamer", "maintainer", "Dreamer系列开山之作 (ICLR 2020)", "tier1")
add_edge("Dreamer", "DreamerV3", "evolution", "隐空间想象→Nature验证 (2023)", "tier1")
add_edge("Dreamer", "Dreamer4", "evolution", "隐空间想象→纯离线+实时推理 (2025)", "tier2")
add_edge("Dreamer", "Model_Based_RL", "evolution", "隐空间世界模型→基于模型的RL核心范式", "tier1")

# ── Hafner → Embo ──
add_edge("Danijar_Hafner", "Embo", "founded", "创始人 & CEO (2025)", "tier1")
add_edge("Embo", "Dreamer4", "maintainer", "核心技术内核", "tier1")
add_edge("Embo", "DreamerV3", "related", "技术前身", "tier2")

# ── Embo 与路线的关联 ──
add_edge("Embo", "Model_Based_RL", "maintainer", "Dreamer商业化→机器人世界模型", "tier2")

# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 17
data["meta"]["updated"] = "2026-05-26"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v17: 更新Danijar_Hafner(Embo创始人)+新增原始Dreamer里程碑(ICLR 2020)+Embo公司(a16z>$100M)，补全Dreamer→DreamerV3→Dreamer4完整演化链")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v15 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
