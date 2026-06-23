#!/usr/bin/env python3
"""v17 增量更新：王建元(VGGT) + Gaoyue Zhou(DINO-WM/NWM) + 导师链"""
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
# 1. 王建元谱系：Andrea Vedaldi → 王建元 → VGGT → VGGT-Ω
# ═══════════════════════════════════════════════════════════════
print("\n=== 王建元 / VGGT 谱系 ===")

add_node("Andrea_Vedaldi",
    "Andrea Vedaldi\\n牛津大学 VGG 组教授",
    "person_overseas", "spatial",
    "牛津大学视觉几何组（Visual Geometry Group, VGG）教授。计算机视觉领域知名学者，"
    "VGG 组在图像识别、3D 重建方向有深厚积累。王建元的博士导师。"
)

add_node("Wang_Jianyuan",
    "王建元 Wang Jianyuan",
    "person_overseas", "spatial",
    "Meta AI 研究员，牛津大学 VGG 组联合培养博士生（博三），师从 Andrea Vedaldi、David Novotny、Christian Rupprecht。"
    "VGGT 第一作者，获 CVPR 2025 最佳论文奖（唯一一篇）。研究方向：前馈 3D 理解与重建。"
    "代表工作：PoseDiffusion、VGGSfM、VGGT、VGGT-Ω。",
    bold=True
)

add_node("VGGT",
    "VGGT (CVPR 2025)\\n最佳论文奖\\n纯前馈 Transformer 3D重建",
    "milestone", "spatial",
    "Visual Geometry Grounded Transformer。Meta AI & 牛津大学联合提出，王建元一作。"
    "首个纯前馈 Transformer，单次前向即可从 1~数百张图像端到端预测完整 3D 场景信息"
    "（相机内外参、深度图、点云图、3D 点轨迹），无需 Bundle Adjustment 等任何后处理。"
    "交替注意力机制（Alternating Attention）：24 层 Transformer 中交替堆叠全局/帧内自注意力，"
    "平衡单帧细节与多视角信息整合。在多个 3D 任务中达到 SOTA，重建速度一秒以内。"
    "代表 3D 重建从'多视图优化'到'前馈端到端理解'的范式转变。"
)

add_node("VGGT_Omega",
    "VGGT-Ω (CVPR 2026)\\n训练数据扩大 100 倍\\n静态+动态场景",
    "milestone", "spatial",
    "VGGT 的大规模扩展版。训练数据：有监督扩大 20 倍，自监督扩大 100 倍。"
    "内存消耗仅为原 VGGT 的 30%，推理速度提升 1.6 倍。"
    "相机估计精度在 Sintel 数据集上提升 77%。同时支持静态和动态场景 3D 重建。"
)

# ── 边 ──
add_edge("Andrea_Vedaldi", "Wang_Jianyuan", "mentorship", "博士导师 (牛津 VGG)", "tier1")
add_edge("Wang_Jianyuan", "VGGT", "maintainer", "第一作者 / CVPR 2025 最佳论文", "tier1")
add_edge("VGGT", "VGGT_Omega", "evolution", "大规模扩展版 (CVPR 2026)", "tier1")
add_edge("VGGT", "Spatial_Intel", "evolution", "前馈端到端 3D 重建→空间智能基础设施", "tier2")
add_edge("VGGT_Omega", "Spatial_Intel", "evolution", "静态+动态场景→通用空间智能", "tier2")

# ═══════════════════════════════════════════════════════════════
# 2. Gaoyue Zhou 谱系：LeCun + Lerrel Pinto → Gaoyue Zhou → DINO-WM + NWM
# ═══════════════════════════════════════════════════════════════
print("\n=== Gaoyue Zhou / DINO-WM / NWM 谱系 ===")

add_node("Lerrel_Pinto",
    "Lerrel Pinto\\nNYU 教授\\n机器人学习",
    "person_overseas", "sim",
    "NYU Courant 计算机科学教授。研究方向：机器人学习、世界模型。"
    "Gaoyue Zhou 的博士 co-advisor（与 Yann LeCun 共同指导）。"
    "在真实世界机器人数据高效学习方面有重要贡献。"
)

add_node("Gaoyue_Zhou",
    "Gaoyue Zhou",
    "person_overseas", "sim",
    "NYU Courant 博二，师从 Yann LeCun & Lerrel Pinto。"
    "UC Berkeley 本科（Sergey Levine 指导 BAIR Lab），CMU 机器人所硕士（Abhinav Gupta 指导）。"
    "DINO-WM 第一作者（ICML 2025），NWM 核心作者（CVPR 2025 最佳论文荣誉提名）。"
    "研究方向：基于预训练视觉特征的世界模型、零样本规划、导航世界模型。"
    "跨越 JEPA（LeCun 学生）和学习仿真（Berkeley/CMU 机器人背景）两条路线。",
    bold=True
)

add_node("NWM",
    "Navigation World Models (CVPR 2025)\\n最佳论文荣誉提名\\n10亿参数导航世界模型",
    "milestone", "sim",
    "Gaoyue Zhou 核心参与（Amir Bar 一作），获 CVPR 2025 最佳论文荣誉提名。"
    "10 亿参数 Conditional Diffusion Transformer（CDiT），"
    "基于人类和机器人自我中心视频的多样化数据集训练。"
    "通过模拟导航轨迹并评估是否达成目标来进行规划，"
    "实现跨环境和跨具身形态的通用导航世界模型。"
    "代表了世界模型从'被动生成'到'主动规划'的关键跨越。"
)

# ── 边 ──
add_edge("Yann_LeCun", "Gaoyue_Zhou", "mentorship", "博士 co-advisor (NYU)", "tier1")
add_edge("Lerrel_Pinto", "Gaoyue_Zhou", "mentorship", "博士 co-advisor (NYU)", "tier1")
add_edge("Sergey_Levine", "Gaoyue_Zhou", "mentorship", "本科导师 (UC Berkeley BAIR)", "tier1")
add_edge("Abhinav_Gupta", "Gaoyue_Zhou", "mentorship", "硕士导师 (CMU RI)", "tier1")
add_edge("Gaoyue_Zhou", "DINO_WM", "maintainer", "第一作者 (ICML 2025)", "tier1")
add_edge("Gaoyue_Zhou", "NWM", "maintainer", "核心作者 (CVPR 2025 荣誉提名)", "tier1")
add_edge("NWM", "Model_Based_RL", "evolution", "导航世界模型→机器人规划", "tier2")
add_edge("DINO_WM", "NWM", "related", "同作者：视觉特征WM→导航WM", "tier2")
add_edge("NWM", "DINO_WM", "related", "共享预训练视觉特征→世界模型核心范式", "tier2")
add_edge("Gaoyue_Zhou", "Yann_LeCun", "lab", "LeCun 学生 / JEPA 路线延展", "tier2")
add_edge("Amir_Bar", "Gaoyue_Zhou", "lab", "NWM 合作者 / Meta FAIR", "tier2")

# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 20
data["meta"]["updated"] = "2026-05-26"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v20: 王建元(VGGT/VGGT-Ω,CVPR 2025最佳论文)+Andrea Vedaldi导师链；Gaoyue Zhou(DINO-WM/NWM,LeCun+Lerrel Pinto学生)+NWM里程碑，打通LeCun→Zhou→DINO-WM/NWM链")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v17 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
for n in new_nodes_added:
    print(f"    - {n}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
