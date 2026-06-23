#!/usr/bin/env python3
"""v6 增量更新：为10家世界模型公司补充关键人物和产品节点"""
import json, os, subprocess

SRC = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SRC, "World_Models_data.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

existing_ids = {n["id"] for n in data["nodes"]}
existing_names = {n["label"].split("\\n")[0].strip().lower() for n in data["nodes"]}

new_nodes_added = []
new_edges_added = []

def add_node(nid, label, ntype, group, description, bold=False):
    if nid in existing_ids:
        print(f"  ⏭ 跳过重复: {nid}")
        return False
    existing_ids.add(nid)
    data["nodes"].append({
        "id": nid,
        "label": label,
        "type": ntype,
        "group": group,
        "bold": bold,
        "description": description
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
    data["edges"].append({
        "source": source,
        "target": target,
        "type": etype,
        "label": label,
        "strength": strength
    })
    new_edges_added.append(f"{source} → {target}")

# ═══════════════════════════════════════════════════════════════
# 1. Moonlake AI (月湖AI) — 空间智能路线
# ═══════════════════════════════════════════════════════════════
print("\n=== Moonlake AI ===")

add_node("Moonlake_AI",
    "Moonlake AI 月湖AI\\n$28M 种子轮\\n🏷️ Stanford PhD创办",
    "company_overseas", "spatial",
    "Stanford PhD Fan-Yun Sun（CEO）与Sharon Lee联合创办。开发生成式游戏引擎Reverie，将空间智能技术应用于可交互3D世界生成。获$28M种子轮融资。")

add_node("FanYun_Sun",
    "Fan-Yun Sun\\nMoonlake AI CEO / Stanford PhD",
    "person_overseas", "spatial",
    "Stanford大学博士。Moonlake AI联合创始人兼CEO。研究方向为3D生成与空间智能，将学术积累转化为生成式游戏引擎产品。")

add_node("Sharon_Lee",
    "Sharon Lee\\nMoonlake AI联合创始人 / Stanford PhD\\n李飞飞学生",
    "person_overseas", "spatial",
    "Stanford大学博士，师从李飞飞。Moonlake AI联合创始人。研究聚焦3D视觉与空间智能，将李飞飞空间智能理念应用于游戏引擎方向。")

add_node("Reverie",
    "Reverie\\nMoonlake AI 生成式游戏引擎",
    "milestone", "spatial",
    "Moonlake AI的核心产品。生成式游戏引擎，利用空间智能技术从文本/图像生成可交互的3D游戏世界。代表了空间智能在游戏娱乐领域的商业化应用。")

# ═══════════════════════════════════════════════════════════════
# 2. Decart — 学习仿真路线
# ═══════════════════════════════════════════════════════════════
print("\n=== Decart ===")

add_node("Decart",
    "Decart\\n$300M 融资 / ~$4B 估值\\n物理AI世界模型",
    "company_overseas", "sim",
    "由Dean Leitersdorf与Moshe Shalev联合创办。构建物理AI世界模型，产品线覆盖优化(DOS)→沉浸式世界模型(Lucy)→物理世界模型(Oasis)。累计融资约$300M，估值约$4B。")

add_node("Dean_Leitersdorf",
    "Dean Leitersdorf\\nDecart 联合创始人 & CEO",
    "person_overseas", "sim",
    "Decart联合创始人兼CEO。带领公司从AI优化平台(DOS)拓展到物理AI世界模型(Oasis)，完成从基础设施到世界模型的战略升级。")

add_node("Moshe_Shalev",
    "Moshe Shalev\\nDecart 联合创始人",
    "person_overseas", "sim",
    "Decart联合创始人。与Leitersdorf共同推动公司从AI优化到物理世界模型的技术转型。")

add_node("Decart_DOS",
    "DOS (Decart)\\nAI优化平台",
    "milestone", "sim",
    "Decart的AI优化平台产品，为公司早期核心业务。为后续物理AI世界模型提供了工程基础设施和商业化经验。")

add_node("Decart_Lucy",
    "Lucy (Decart)\\n沉浸式世界模型",
    "milestone", "sim",
    "Decart的沉浸式世界模型产品。从优化平台向世界模型的过渡产品，验证了世界模型技术的商业化可行性。")

add_node("Decart_Oasis",
    "Oasis (Decart)\\n物理AI世界模型",
    "milestone", "sim",
    "Decart的旗舰物理AI世界模型产品。代表了公司从AI基础设施向物理世界模型的最终战略转向。")

# ═══════════════════════════════════════════════════════════════
# 3. Physical Intelligence (π) — 学习仿真路线
# ═══════════════════════════════════════════════════════════════
print("\n=== Physical Intelligence ===")

add_node("Physical_Intelligence",
    "Physical Intelligence\\n$1B+ 融资 / ~$11B 估值\\nVLA 机器人世界模型",
    "company_overseas", "sim",
    "由Karol Hausman（CEO）、Sergey Levine、Chelsea Finn、Brian Ichter等联合创办。构建视觉-语言-动作(VLA)机器人基础模型π系列。累计融资超$1B，估值超$11B。核心理念：将世界模型嵌入机器人操作策略，实现通用机器人智能。")

add_node("Karol_Hausman",
    "Karol Hausman\\nPhysical Intelligence CEO\\n前Google DeepMind",
    "person_overseas", "sim",
    "Physical Intelligence联合创始人兼CEO。前Google DeepMind研究科学家。机器人学习与VLA模型方向的领军人物，推动π系列模型从学术走向产业化。")

add_node("Brian_Ichter",
    "Brian Ichter\\nPhysical Intelligence联合创始人\\n前Google DeepMind",
    "person_overseas", "sim",
    "Physical Intelligence联合创始人。前Google DeepMind研究科学家。在机器人基础模型和VLA架构设计上有重要贡献。")

add_node("Pi0",
    "π0 (2024)\\nPhysical Intelligence VLA基础模型",
    "milestone", "sim",
    "Physical Intelligence发布的首个视觉-语言-动作(VLA)基础模型。在多机器人平台和多任务上展现通用操作能力。基于互联网规模视觉数据预训练+机器人数据微调。")

add_node("Pi0_5",
    "π0.5 (2025)\\nVLA模型快速迭代版",
    "milestone", "sim",
    "Physical Intelligence的VLA模型快速迭代版本。在π0基础上提升推理速度和任务泛化能力。")

add_node("Pi_star_06",
    "π*0.6 (2025)\\nVLA模型语义增强版",
    "milestone", "sim",
    "Physical Intelligence VLA模型语义理解增强版。引入更丰富的语言理解和场景推理能力。")

add_node("Pi1_0",
    "π1.0 (2025)\\nVLA模型完整版",
    "milestone", "sim",
    "Physical Intelligence VLA模型首个完整版本。打通视觉感知→语言理解→动作执行的端到端机器人操作闭环，标志着VLA路线从研究原型走向产品化。")

# ═══════════════════════════════════════════════════════════════
# 4. Wayve 补充关键人物
# ═══════════════════════════════════════════════════════════════
print("\n=== Wayve 补充 ===")

add_node("Alex_Kendall",
    "Alex Kendall\\nWayve 联合创始人 & CEO\\n剑桥大学博士",
    "person_overseas", "sim",
    "剑桥大学博士。Wayve联合创始人兼CEO。端到端自动驾驶世界模型先驱，带领团队开发GAIA-1等里程碑产品。主张以世界模型而非高精地图路线实现自动驾驶。")

# ═══════════════════════════════════════════════════════════════
# 5. Odyssey 补充产品节点
# ═══════════════════════════════════════════════════════════════
print("\n=== Odyssey 补充 ===")

add_node("Odyssey_Interactive_WM",
    "Odyssey 交互式世界模型\\n40ms/帧 实时生成",
    "milestone", "sim",
    "Odyssey的核心产品。40ms/帧实时生成可交互视频世界，无需传统游戏引擎。支持用户在AI生成的3D环境中自由导航和交互。代表了生成式世界模型在实时交互方向的前沿探索。")

# ═══════════════════════════════════════════════════════════════
# 6. General Intuition 补充产品节点
# ═══════════════════════════════════════════════════════════════
print("\n=== General Intuition 补充 ===")

add_node("GI_Spatiotemporal_WM",
    "General Intuition 时空推理WM\\n空间-时间世界模型",
    "milestone", "spatial",
    "General Intuition构建的空间-时间推理世界模型。融合扩散世界模型技术(DIAMOND团队)与时空推理能力，面向需要物理常识和因果推理的AI应用场景。")

# ═══════════════════════════════════════════════════════════════
# 7. Runway 补充产品代际节点
# ═══════════════════════════════════════════════════════════════
print("\n=== Runway 补充 ===")

add_node("Gen4_5",
    "Gen-4.5 (2025)\\nRunway 视频生成→世界模型",
    "milestone", "sim",
    "Runway的第四代视频生成模型升级版。是GWM-1通用世界模型的技术基础，标志着Runway从创意视频生成向物理世界模拟的战略转型。")

# ═══════════════════════════════════════════════════════════════
# 新增边
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增关系边 ===")

# ── Moonlake AI ──
add_edge("FanYun_Sun", "Moonlake_AI", "founded", "联合创始人 & CEO", "tier1")
add_edge("Sharon_Lee", "Moonlake_AI", "founded", "联合创始人", "tier1")
add_edge("Moonlake_AI", "Reverie", "maintainer", "核心产品", "tier1")
add_edge("FeiFei_Li", "Sharon_Lee", "mentorship", "博士导师 (Stanford)", "tier1")
add_edge("FanYun_Sun", "FeiFei_Li", "lab", "Stanford空间智能研究网络", "tier2")
add_edge("Moonlake_AI", "Spatial_Intel", "derived", "空间智能在游戏引擎的应用", "tier2")
add_edge("Reverie", "Spatial_Intel", "derived", "生成式3D游戏世界", "tier2")

# ── Decart ──
add_edge("Dean_Leitersdorf", "Decart", "founded", "联合创始人 & CEO", "tier1")
add_edge("Moshe_Shalev", "Decart", "founded", "联合创始人", "tier1")
add_edge("Decart", "Decart_DOS", "maintainer", "早期产品", "tier1")
add_edge("Decart", "Decart_Lucy", "maintainer", "过渡产品", "tier1")
add_edge("Decart", "Decart_Oasis", "maintainer", "旗舰产品", "tier1")
add_edge("Decart_DOS", "Decart_Lucy", "evolution", "平台→世界模型转型", "tier2")
add_edge("Decart_Lucy", "Decart_Oasis", "evolution", "沉浸式→物理AI升级", "tier2")
add_edge("Decart_Oasis", "Model_Based_RL", "evolution", "物理AI世界模型新范式", "tier2")
add_edge("Decart_Oasis", "PhysAI_Infra", "related", "物理世界模型基础设施", "tier2")

# ── Physical Intelligence ──
add_edge("Karol_Hausman", "Physical_Intelligence", "founded", "联合创始人 & CEO", "tier1")
add_edge("Sergey_Levine", "Physical_Intelligence", "founded", "联合创始人", "tier1")
add_edge("Chelsea_Finn", "Physical_Intelligence", "founded", "联合创始人", "tier1")
add_edge("Brian_Ichter", "Physical_Intelligence", "founded", "联合创始人", "tier1")
add_edge("Physical_Intelligence", "Pi0", "maintainer", "旗舰产品 VLA基础模型", "tier1")
add_edge("Physical_Intelligence", "Pi0_5", "maintainer", "快速迭代版", "tier1")
add_edge("Physical_Intelligence", "Pi_star_06", "maintainer", "语义增强版", "tier1")
add_edge("Physical_Intelligence", "Pi1_0", "maintainer", "首个完整版", "tier1")
add_edge("Pi0", "Pi0_5", "evolution", "快速迭代", "tier2")
add_edge("Pi0_5", "Pi_star_06", "evolution", "语义增强", "tier2")
add_edge("Pi_star_06", "Pi1_0", "evolution", "完整产品化", "tier2")
add_edge("Karol_Hausman", "Google_DeepMind", "employed", "前研究科学家", "tier2")
add_edge("Brian_Ichter", "Google_DeepMind", "employed", "前研究科学家", "tier2")
add_edge("Pi0", "Model_Based_RL", "evolution", "VLA机器人世界模型新范式", "tier2")
add_edge("Pi1_0", "Model_Based_RL", "evolution", "端到端VLA操作闭环", "tier2")

# ── Wayve ──
add_edge("Alex_Kendall", "Wayve", "founded", "联合创始人 & CEO", "tier1")
add_edge("Wayve", "GAIA_1", "maintainer", "Alex Kendall推动", "tier1")
add_edge("Alex_Kendall", "GAIA_1", "maintainer", "CEO & 技术推动者", "tier1")

# ── Odyssey ──
add_edge("Odyssey", "Odyssey_Interactive_WM", "maintainer", "核心产品", "tier1")
add_edge("Odyssey_Interactive_WM", "Gen_Video_concept", "evolution", "实时交互生成式世界模型", "tier2")

# ── General Intuition ──
add_edge("General_Intuition", "GI_Spatiotemporal_WM", "maintainer", "核心产品方向", "tier1")
add_edge("GI_Spatiotemporal_WM", "Spatial_Intel", "evolution", "时空推理+空间智能融合", "tier2")

# ── Runway ──
add_edge("Runway", "Gen4_5", "maintainer", "Gen-4.5 视频生成→世界模型", "tier1")
add_edge("Gen4_5", "GWM1", "evolution", "视频生成→通用世界模型升级", "tier1")
add_edge("Cristobal_Valenzuela", "Gen4_5", "maintainer", "CEO & 战略推动者", "tier2")

# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 7
data["meta"]["updated"] = "2026-05-25"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v7: 为10家公司补充关键人物/产品节点——新增Moonlake AI、Decart、Physical Intelligence及其创始人和产品，补充Wayve(Alex Kendall)、Odyssey(交互式WM)、General Intuition(时空推理WM)、Runway(Gen-4.5)")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v6 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

# 运行 rebuild_v4.py
print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
