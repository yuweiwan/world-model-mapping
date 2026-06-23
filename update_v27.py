#!/usr/bin/env python3
"""v27 增量更新：张直政(银河通用联合创始人/大模型负责人) + LDA里程碑"""
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

add_node("Zhang_Zhizheng",
    "张直政 Zhang Zhizheng\\n银河通用联合创始人",
    "person_overseas", "sim",
    "中科大本科/博士（2021，导师陈志波、李卫平），哥伦比亚大学CSC联合培养。"
    "前微软亚洲研究院（MSRA）高级研究员，参与Copilot、Dynamics 365等大模型产品。"
    "2023年与王鹤联合创立银河通用，任大模型负责人。"
    "主导LDA（Latent Dynamics Action Model），入选RSS 2026并开源，"
    "在隐空间中统一世界模型与VLA的跨本体动作基础模型。"
    "主张「虚实共融、人机结合」具身数据观，提出具身智能三阶段："
    "仿真冷启动→真实数据对接→业务回流闭环。"
    "2025年北京市劳动模范。",
    bold=True
)

# ═══════════════════════════════════════════════════════════════
# 2. 里程碑节点
# ═══════════════════════════════════════════════════════════════
print("\n=== 里程碑节点 ===")

add_node("LDA_Model",
    "LDA (RSS 2026)\\n隐空间世界模型+VLA融合\\n跨本体动作基础模型",
    "milestone", "sim",
    "银河通用张直政主导。LDA（Latent Dynamics Action Model）在隐空间中"
    "统一世界模型与VLA，实现跨本体（不同机器人形态）的动作生成。"
    "入选机器人顶会RSS 2026（仅210篇录用），已全面开源。"
    "代表具身智能从「单一本体专用模型」向「跨本体通用基础模型」的关键跨越。"
)

# ═══════════════════════════════════════════════════════════════
# 3. 新增边
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增关系边 ===")

# ── 创业 ──
add_edge("Zhang_Zhizheng", "GalaxyBot", "founded",
    "联合创始人兼大模型负责人 (2023至今)", "tier1")
add_edge("Zhang_Zhizheng", "Wang_He", "lab",
    "联合创始人/同事 (2023至今)", "tier1")

# ── 产品 ──
add_edge("Zhang_Zhizheng", "GraspVLA", "maintainer",
    "大模型负责人 / 仿真数据+端到端抓取", "tier1")
add_edge("Zhang_Zhizheng", "LDA_Model", "maintainer",
    "主导研发 / RSS 2026 / 开源", "tier1")
add_edge("GalaxyBot", "LDA_Model", "maintainer",
    "银河通用出品 / RSS 2026", "tier1")

# ── 世界模型关联 ──
add_edge("LDA_Model", "Model_Based_RL", "evolution",
    "隐空间世界模型+动作生成 / Dreamer路线具身延伸", "tier2")
add_edge("Zhang_Zhizheng", "Model_Based_RL", "maintainer",
    "世界模型→VLA融合 / 具身智能世界模型", "tier2")

# ── 具身智能关联 ──
add_edge("LDA_Model", "GraspVLA", "evolution",
    "跨本体通用→端到端抓取 / 同一团队技术栈", "tier1")

# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 31
data["meta"]["updated"] = "2026-05-26"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v31: 张直政(银河通用联合创始人/大模型负责人/中科大博士/MSRA前高级研究员)+LDA(隐空间世界模型+VLA融合/RSS 2026)，补全银河通用创始团队")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v27 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
for n in new_nodes_added:
    print(f"    - {n}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
