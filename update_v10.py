#!/usr/bin/env python3
"""v10 增量更新：补充NVIDIA Omniverse平台节点和Tesla世界模拟器谱系"""
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
# NVIDIA Omniverse 补充
# ═══════════════════════════════════════════════════════════════
print("\n=== NVIDIA Omniverse ===")

add_node("Omniverse",
    "Omniverse (2021)\\nNVIDIA 数字孪生OS",
    "milestone", "sim",
    "NVIDIA的数字孪生与3D仿真操作系统。基于OpenUSD标准，支持跨3D工具实时协作。核心理念：构建物理世界的高保真数字副本，作为机器人、自动驾驶等AI系统的虚拟训练场。2025年CES发布Mega Blueprint用于工厂级机器人集群仿真。与Cosmos深度整合：Omniverse构建虚拟世界→Cosmos在虚拟世界中训练和推理物理AI。"
)

add_node("Isaac_Sim",
    "Isaac Sim (2025)\\nNVIDIA 机器人仿真平台",
    "milestone", "sim",
    "NVIDIA的机器人仿真平台，基于Omniverse构建。v5.0集成NuRec（3D Gaussian Splatting神经渲染）缩小Sim-to-Real鸿沟。Isaac Lab 2.2提供开源强化学习框架。被Boston Dynamics、Figure AI等头部机器人公司采用。核心理念：机器人在虚拟世界中完成数百万次试错→零样本迁移到现实世界。"
)

# ═══════════════════════════════════════════════════════════════
# Tesla 世界模拟器谱系
# ═══════════════════════════════════════════════════════════════
print("\n=== Tesla ===")

add_node("Tesla",
    "Tesla 特斯拉\\nFSD + 神经世界模拟器",
    "company_overseas", "sim",
    "全球新能源汽车与AI领军企业。在自动驾驶世界模型方向上做了开创性工作：端到端神经网络FSD架构、神经世界模拟器（Neural World Simulator）、3D占用网络（Occupancy Network）。2025年ICCV上AI VP Ashok Elluswamy披露技术细节：模拟器中1天=人类500年驾驶经验，世界模拟器底层引擎同时用于FSD和Optimus机器人。代表了从量产自动驾驶向通用物理世界AI的战略升级。"
)

add_node("Ashok_Elluswamy",
    "Ashok Elluswamy\\nTesla AI 副总裁",
    "person_overseas", "sim",
    "Tesla人工智能副总裁，FSD端到端架构和神经世界模拟器核心推动者。2025年10月在ICCV檀香山首次公开披露FSD技术内幕：端到端架构+3D高斯泼溅场景重建+自然语言推理闭环。将FSD从传统模块化框架推向生成式世界模型范式，是学习仿真路线在量产自动驾驶领域最关键的实践领导者。"
)

add_node("Tesla_World_Sim",
    "Tesla 神经世界模拟器 (2025)\\n闭环视频生成+驾驶推演",
    "milestone", "sim",
    "特斯拉的端到端神经世界模拟器，完全基于神经网络从真实驾驶数据中学习。核心能力：(1)根据当前状态+候选动作→生成未来世界视觉画面；(2)可连续生成6分钟以上、8摄像头24fps逼真视频；(3)支持对抗性长尾场景生成；(4)同底层引擎用于FSD和Optimus机器人训练。2025年ICCV由Ashok Elluswamy首次公开披露。将世界模型从学术概念推向亿级车队验证的量产工程实践。"
)

add_node("Occupancy_Network",
    "Occupancy Network (2022)\\nTesla 3D占用网络",
    "milestone", "sim",
    "特斯拉于CVPR 2022 Workshop首次公开的3D空间感知方案。直接输出3D体素空间的占用概率和语义信息，无需依赖HD地图或LiDAR。仅用视觉输入（多摄像头）即可实现对任意形状物体和不规则空间的鲁棒3D表征。引发自动驾驶行业从2D BEV到全3D占用的范式转变，后被Wayve、华为等广泛跟进。是空间智能在量产自动驾驶中的标志性落地。"
)

# ═══════════════════════════════════════════════════════════════
# 新增边
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增关系边 ===")

# ── NVIDIA Omniverse ──
add_edge("NVIDIA", "Omniverse", "maintainer", "核心平台 (2021)", "tier1")
add_edge("NVIDIA", "Isaac_Sim", "maintainer", "机器人仿真平台", "tier1")
add_edge("Omniverse", "Omniverse_DSX", "evolution", "→DSX数据与物理仿真的工业部署框架", "tier1")
add_edge("Omniverse", "Cosmos", "related", "数字孪生OS + 物理AI模型双向集成", "tier1")
add_edge("Omniverse", "Isaac_Sim", "evolution", "Omniverse→机器人仿真平台", "tier1")
add_edge("Isaac_Sim", "Cosmos", "related", "仿真平台 + Cosmos WFM训练", "tier2")
add_edge("Isaac_Sim", "Model_Based_RL", "related", "机器人世界模型训练场", "tier2")

# ── Tesla ──
add_edge("Ashok_Elluswamy", "Tesla", "employed", "AI 副总裁 / FSD端到端架构推动者", "tier1")
add_edge("Tesla", "Tesla_World_Sim", "maintainer", "核心产品 (2025 ICCV披露)", "tier1")
add_edge("Tesla", "Occupancy_Network", "maintainer", "核心感知方案 (CVPR 2022)", "tier1")
add_edge("Tesla_World_Sim", "Occupancy_Network", "evolution", "占用网络→完整世界模拟器", "tier1")
add_edge("Tesla_World_Sim", "Gen_Video_concept", "evolution", "神经视频生成→闭环驾驶世界推演", "tier2")
add_edge("Tesla_World_Sim", "Model_Based_RL", "evolution", "闭环仿真→规模化强化学习 (1天=500年)", "tier2")
add_edge("Occupancy_Network", "Spatial_Intel", "evolution", "纯视觉3D占用→空间智能量产落地", "tier2")

# ── Tesla与NVIDIA生态连接 ──
add_edge("Tesla", "NVIDIA", "related", "Dojo自研芯片 vs GPU双轨 / 世界模型路线竞争者", "tier2")
add_edge("Ashok_Elluswamy", "Andrej_Karpathy", "lab", "Tesla Autopilot AI 前后任交接", "tier2")


# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 11
data["meta"]["updated"] = "2026-05-25"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v11: NVIDIA Omniverse补充——Omniverse平台/Isaac_Sim，关联已有Cosmos/Omniverse_DSX；Tesla谱系——Tesla公司/Ashok_Elluswamy/神经世界模拟器/Occupancy_Network，连接学习仿真路线与Karpathy")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v10 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

# 运行 rebuild_v4.py
print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
