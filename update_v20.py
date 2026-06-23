#!/usr/bin/env python3
"""v20 增量更新：陈宝权深挖(Arie Kaufman导师/SLAM3R/刘利斌) + 齐国君(Thomas Huang导师/王井东合作/西湖大学MAPLE)"""
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
# 1. 陈宝权深挖——导师 Arie Kaufman + SLAM3R + 刘利斌
# ═══════════════════════════════════════════════════════════════
print("\n=== 陈宝权深挖节点 ===")

add_node("Arie_Kaufman",
    "Arie Kaufman\\nStony Brook 教授\\n体积渲染之父",
    "person_overseas", "spatial",
    "纽约州立大学石溪分校计算机系杰出教授、前系主任。体积渲染（Volume Rendering）领域的开创者，"
    "IEEE Fellow、ACM Fellow。陈宝权的博士导师（1999）。"
    "其体积渲染技术是现代医学可视化、科学可视化和3D图形管线的基础。"
)

add_node("SLAM3R",
    "SLAM3R (CVPR 2025)\\nHighlight + China3DV 最佳论文\\n实时稠密3D重建",
    "milestone", "spatial",
    "北京大学陈宝权团队等提出。首个基于单目RGB视频的实时稠密3D场景重建方法，"
    "在消费级显卡上达 20+ FPS。纯前馈架构：I2P (Image-to-Points) + L2W (Local-to-World)，"
    "无需相机参数、无需迭代优化。一作刘宇政（北大本科生）、董思言（HKU），共同通讯陈宝权、杨言超。"
    "与VGGT并列为「「前馈3D重建」」双星：VGGT重全局相机+几何，SLAM3R重实时局部稠密重建。"
)

add_node("Liu_Libin",
    "刘利斌 Liu Libin",
    "person_overseas", "sim",
    "北京大学智能学院助理教授、博雅青年学者，VCL Lab 核心成员。"
    "前硅谷 DeepMotion Inc. 首席科学家，UBC 及 Disney Research 博士后。"
    "研究方向：数字人建模与运动控制、具身智能。与陈宝权团队在数字人仿真、"
    "可微物理代理、RL运动策略方向深度合作。"
)

# ═══════════════════════════════════════════════════════════════
# 2. 齐国君深挖——Thomas Huang + 齐国君本人
# ═══════════════════════════════════════════════════════════════
print("\n=== 齐国君/Thomas Huang 深挖节点 ===")

add_node("Thomas_Huang",
    "黄煦涛 Thomas S. Huang\\n1936-2020\\n华人计算机视觉鼻祖",
    "person_overseas", "spatial",
    "美籍华裔计算机科学家，被誉为「华人计算机视觉鼻祖」。MIT 博士（1963），UIUC Beckman 研究所图像实验室主任，"
    "Swanlund 主席教授（UIUC最高头衔）。中国科学院外籍院士、中国工程院外籍院士、美国国家工程院院士。"
    "H-index 155。培养100+博士，弟子包括：周曦(云从科技)、颜水成(依图CTO)、韩旭(文远知行CEO)、"
    "田奇(华为CV首席)、齐国君等。曾直接推荐李飞飞获得第一份教职。"
    "奠定了从2D图像序列估计3D运动的理论框架，是Google街景等技术的重要源头。",
    bold=True
)

add_node("Qi_Guojun",
    "齐国君 Guo-Jun Qi",
    "person_overseas", "sim",
    "西湖大学工学院教授，MAPLE Lab（机器感知与学习实验室）负责人（~20人）。"
    "IEEE Fellow、IAPR Fellow、ACM 杰出科学家。中科大自动化博士（2009）+ UIUC 电子与计算机工程博士（2013，师从 Thomas Huang），"
    "7.5年获双博士学位。前华为美国研究中心技术副总裁兼首席AI科学家（2018-2021，获华为总裁奖），"
    "前 OPPO 西雅图研究中心创始院长（2021-2023）。"
    "研究方向：多模态感知+生成+交互、AIGC、跨模态语义转移（文生图/文生视频的数学基础）、"
    "3D智慧创作、具身智能交互。MAPLE Lab 横跨视觉生成大模型与机器人世界模型两大前沿。",
    bold=True
)

# ═══════════════════════════════════════════════════════════════
# 3. 新增边
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增关系边 ===")

# ── 陈宝权谱系 ──
add_edge("Arie_Kaufman", "Chen_Baoquan", "mentorship", "博士导师 (SUNY Stony Brook, 1999)", "tier1")

# ── SLAM3R 连接 ──
add_edge("Chen_Baoquan", "SLAM3R", "maintainer", "共同通讯作者 / CVPR 2025 Highlight", "tier1")
add_edge("SLAM3R", "Spatial_Intel", "evolution", "实时3D重建→空间智能基础设施", "tier2")
add_edge("SLAM3R", "VGGT", "related", "同为「前馈3D重建」 / 互补：VGGT重全局+SLAM3R重实时局部", "tier2")

# ── 刘利斌 ──
add_edge("Chen_Baoquan", "Liu_Libin", "lab", "PKU VCL Lab 合作者 / 数字人+具身智能", "tier2")
add_edge("Liu_Libin", "Model_Based_RL", "maintainer", "数字人运动控制→可微物理仿真→具身世界模型", "tier2")

# ── Thomas Huang 谱系 ──
add_edge("Thomas_Huang", "Qi_Guojun", "mentorship", "博士导师 (UIUC Beckman Institute, 2013)", "tier1")
add_edge("Thomas_Huang", "FeiFei_Li", "lab", "推荐第一份教职 / 学术引路人", "tier2")

# ── 齐国君 连接 ──
add_edge("Qi_Guojun", "Jingdong_Wang", "lab", "KDD 2017 合作 / 同年 IEEE Fellow (2022)", "tier2")
add_edge("Qi_Guojun", "Model_Based_RL", "maintainer", "MAPLE Lab: 多模态感知+生成→具身世界模型", "tier2")

# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 24
data["meta"]["updated"] = "2026-05-26"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v24: 陈宝权深挖(Arie Kaufman导师链/SLAM3R CVPR2025 Highlight/刘利斌)+齐国君(Thomas Huang华人CV鼻祖导师链/王井东合作/西湖大学MAPLE Lab/华为OPPO履历)，打通图形学→实时3D重建→多模态世界模型两条新链")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v20 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
for n in new_nodes_added:
    print(f"    - {n}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
