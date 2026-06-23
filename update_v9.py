#!/usr/bin/env python3
"""v9 增量更新：添加姚遥（权龙学生/MVSNet）和张飞虎（DreamTech/Direct3D）"""
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
# 1. 姚遥 — 权龙学生 / MVSNet / 南大副教授
# ═══════════════════════════════════════════════════════════════
print("\n=== 姚遥 Yao Yao ===")

add_node("Yao_Yao",
    "姚遥 Yao Yao",
    "person_overseas", "spatial",
    "2019年港科大博士，导师权龙。VisGraph实验室后期核心博士生。MVSNet系列开创者（深度学习多视图立体视觉基准，引用6000+），Altizure创始团队核心成员。Altizure被Apple收购后任Apple高级研究员。后回国任南京大学智能科学与技术学院副教授、博导，国家级青年人才（海外优青）。代表工作：MVSNet、Matrix3D（CVPR 2025 Highlight）、Direct2.5（text-to-3D，10秒生成）、Gaussian-Flow（CVPR 2024 Highlight）、NeILF系列。"
)

add_node("MVSNet",
    "MVSNet (2018)\\n深度学习多视图立体视觉基准",
    "milestone", "spatial",
    "2018年由姚遥等在港科大VisGraph实验室提出。首个将深度学习应用于多视图立体匹配（MVS）的端到端框架，通过可微分单应性变换将2D特征映射到3D空间，实现高精度深度估计。引用超6000次，成为MVS领域的基准方法，被Google、Meta等广泛采用。后续衍生MVSNet-v2、PointMVSNet、FastMVSNet等系列工作。"
)

add_node("Matrix3D",
    "Matrix3D (CVPR 2025)\\n多视角单图端到端3D生成",
    "milestone", "spatial",
    "姚遥团队发表于CVPR 2025的Highlight论文。仅需单张图片，通过多视角扩散+端到端3D重建实现高质量3D生成，无需额外的多视图扩散模型预训练。代表空间智能向低成本、快速3D生成方向的突破。"
)

# ═══════════════════════════════════════════════════════════════
# 2. 张飞虎 — Oxford PhD / DreamTech / Direct3D
# ═══════════════════════════════════════════════════════════════
print("\n=== 张飞虎 Zhang Feihu ===")

add_node("Zhang_Feihu",
    "张飞虎 Zhang Feihu",
    "person_overseas", "spatial",
    "牛津大学博士，导师Philip Torr（FRS/FREng，Torr Vision Group负责人）。DreamTech创始人兼CEO。发现3D生成领域的Scaling Law——模型参数、数据量和3D生成质量之间的幂律关系。GA-Net（CVPR 2019）获最佳论文提名。研究方向：3D生成大模型、立体匹配、神经渲染。"
)

add_node("Philip_Torr",
    "Philip Torr\\n牛津大学教授 / FRS, FREng",
    "person_overseas", "spatial",
    "牛津大学工程科学系教授，Torr Vision Group（TVG）负责人。英国皇家学会院士（FRS）、英国皇家工程院院士（FREng）。牛津VGG实验室的继承者（延续Andrew Zisserman传统）。研究方向：计算机视觉、机器学习、具身智能。微软Research Cambridge和Oxford的联合实验室主任。培养大量3D视觉方向创业者。"
)

add_node("DreamTech",
    "DreamTech\\n3D生成大模型 (2023)",
    "company_overseas", "spatial",
    "2023年由张飞虎创立。专注原生3D生成大模型，发布全球首个5B参数级原生3D生成模型Direct3D。首次在3D领域验证Scaling Law的适用性——即模型参数和数据量的增加能够持续提升3D生成质量。产品面向游戏、影视、AR/VR等行业的3D资产生成需求。"
)

add_node("Direct3D",
    "Direct3D (2024)\\n全球首个5B参数原生3D生成大模型",
    "milestone", "spatial",
    "DreamTech发布的全球首个5B参数级原生3D生成大模型。采用原生3D DiT（Diffusion Transformer）架构直接从3D数据学习分布（区别于从2D图像间接生成3D），验证了3D生成领域的Scaling Law。支持文/text/图到3D的高质量生成，输出几何-纹理解耦的高精度3D资产。"
)

# ═══════════════════════════════════════════════════════════════
# 新增边
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增关系边 ===")

# ── 姚遥师承链 ──
add_edge("Long_Quan", "Yao_Yao", "mentorship", "博士导师 (2019, VisGraph后期核心)", "tier1")

# ── 姚遥与Altizure ──
add_edge("Yao_Yao", "Altizure", "founded", "创始团队核心成员", "tier1")

# ── 姚遥与里程碑 ──
add_edge("Yao_Yao", "MVSNet", "maintainer", "提出者 (2018, ECCV)", "tier1")
add_edge("Yao_Yao", "Matrix3D", "maintainer", "提出者 (CVPR 2025 Highlight)", "tier1")

# ── 姚遥与空间智能 ──
add_edge("Yao_Yao", "Spatial_Intel", "maintainer", "3D重建与生成 / NeILF系列", "tier2")
add_edge("MVSNet", "Spatial_Intel", "evolution", "深度学习MVS基准→空间智能基础方法", "tier2")
add_edge("Matrix3D", "Spatial_Intel", "evolution", "单图端到端3D生成", "tier2")

# ── 姚遥与南大同事 ──
add_edge("Yao_Yao", "Jianxin_Wu", "lab", "同在南京大学任教", "tier2")

# ── 张飞虎师承 ──
add_edge("Philip_Torr", "Zhang_Feihu", "mentorship", "博士导师 (Oxford)", "tier1")

# ── 张飞虎与DreamTech ──
add_edge("Zhang_Feihu", "DreamTech", "founded", "创始人 & CEO (2023)", "tier1")

# ── DreamTech与Direct3D ──
add_edge("DreamTech", "Direct3D", "maintainer", "核心产品 (2024)", "tier1")

# ── 张飞虎与空间智能 ──
add_edge("Zhang_Feihu", "Spatial_Intel", "maintainer", "3D生成大模型 / 3D Scaling Law", "tier2")
add_edge("Direct3D", "Spatial_Intel", "evolution", "5B原生3D大模型→3D生成Scaling Law", "tier2")


# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 10
data["meta"]["updated"] = "2026-05-25"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v10: 新增姚遥(Yao Yao)学术谱系——姚遥/MVSNet/Matrix3D，打通权龙→姚遥→Altizure链条；新增张飞虎(Zhang Feihu)创业谱系——张飞虎/Philip Torr/DreamTech/Direct3D，加入3D生成Scaling Law里程碑")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v9 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

# 运行 rebuild_v4.py
print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
