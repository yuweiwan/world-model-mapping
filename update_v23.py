#!/usr/bin/env python3
"""v23 增量更新：郭春超/王腾飞(腾讯混元3D世界模型) + 关联节点"""
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

add_node("Guo_Chunchao",
    "郭春超 Guo Chunchao",
    "person_overseas", "spatial",
    "腾讯混元3D项目研发负责人、专家研究员。领导混元3D从1.0到2.1的完整迭代，"
    "团队集结AI Lab、游戏光子工作室群、自动驾驶实验室等27位跨领域专家。"
    "主导HunyuanWorld开源世界模型系列。判断3D生成目前处于GPT2-GPT3之间阶段，"
    "视觉合格率一年从20%提升至60%。推动开源生态，商业许可申请超50家。",
    bold=True
)

add_node("Wang_Tengfei",
    "王腾飞 Wang Tengfei",
    "person_overseas", "spatial",
    "腾讯混元3D世界模型负责人，主导HY-World系列（1.0/1.1/1.5/2.0/Voyager）"
    "研发与落地。HKUST博士（2023，导师陈启峰Qifeng Chen），北航本科。"
    "前MSRA研究员（2021-2023）。CVPR/ICCV/SIGGRAPH/ICLR等顶会论文40+篇，"
    "引用3500+。ICCV/ECCV最有影响力论文奖。"
    "核心观点：3D表示是构建可交互、物理一致世界模型的关键基础。"
    "FlashWorld项目：9秒从单图生成3D场景（比CAT3D快500倍）。",
    bold=True
)

add_node("Qifeng_Chen",
    "陈启峰 Qifeng Chen\\nHKUST 助理教授",
    "person_overseas", "spatial",
    "香港科技大学计算机科学与工程系助理教授。Stanford博士（2017，师从Vladlen Koltun）。"
    "王腾飞的博士导师（2023）。研究方向：计算机视觉、计算摄影、3D生成。"
    "曾获Google PhD Fellowship、Adobe Fellowship。HKUST CSE最佳博士论文奖指导教师。"
)

# ═══════════════════════════════════════════════════════════════
# 2. 产品/里程碑节点
# ═══════════════════════════════════════════════════════════════
print("\n=== 产品/里程碑节点 ===")

add_node("Hunyuan3D",
    "混元3D 2.1 (CVPR 2025)\\n全链路开源工业级3D生成\\n首个PBR材质生成",
    "milestone", "spatial",
    "腾讯混元团队，郭春超领导。业界首个全链路开源工业级3D生成大模型。"
    "支持文/图生成3D资产，引入PBR材质生成（CVPR 2025）。"
    "从Hunyuan3D-1.0（2024.11）→2.0（2025.01）→2.1（2025.06）→2.5（2025.12），"
    "有效面片数增加超10倍。开源24小时获3.2万GitHub Stars。"
)

add_node("HY_World",
    "HY-World (2025.7-2026.4)\\n首个开源多模态世界模型\\n兼容物理引擎·3D可交互",
    "milestone", "spatial",
    "腾讯混元团队，王腾飞主导研发。从HunyuanWorld 1.0（2025.7首次开源）"
    "→1.5 WorldPlay（2025.12，实时交互24FPS/720P）→2.0（2026.4）。"
    "四阶段架构：HY-Pano全景生成→WorldNav轨迹规划→WorldStereo世界扩展→WorldMirror重建构成。"
    "兼容Unity/Unreal Engine，支持导出Mesh/3DGS/点云。"
    "定位为engine-ready世界模型：输入一张图输出可编辑3D场景。"
)

add_node("Hunyuan_Voyager",
    "混元Voyager (2026)\\nWorldScore 平均分第一\\nRGB-D联合建模+空间缓存",
    "milestone", "spatial",
    "腾讯混元团队，HY-World 扩展版。引入RGB-D联合建模与空间缓存机制，"
    "在斯坦福WorldScore排行榜三项能力登顶，平均分第一。"
    "代表了腾讯3D世界模型在国际评测中的最高水平。"
)

# ═══════════════════════════════════════════════════════════════
# 3. 新增边
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增关系边 ===")

# ── 师承关系 ──
add_edge("Qifeng_Chen", "Wang_Tengfei", "mentorship", "博士导师 (HKUST, 2023)", "tier1")

# ── 腾讯混元内部 ──
add_edge("Wang_Tengfei", "Guo_Chunchao", "lab", "腾讯混元3D团队同事 / 3D资产+世界模型协同", "tier1")

# ── 产品归属 ──
add_edge("Guo_Chunchao", "Hunyuan3D", "maintainer", "混元3D项目研发负责人", "tier1")
add_edge("Wang_Tengfei", "HY_World", "maintainer", "HY-World 系列主导研发", "tier1")
add_edge("Wang_Tengfei", "Hunyuan_Voyager", "maintainer", "Voyager 扩展版 / WorldScore 榜首", "tier1")

# ── 产品演进链 ──
add_edge("Hunyuan3D", "HY_World", "evolution", "3D资产生成→可交互3D世界生成", "tier1")
add_edge("HY_World", "Hunyuan_Voyager", "evolution", "扩展版 / RGB-D+空间缓存", "tier1")

# ── 空间智能连接 ──
add_edge("Hunyuan3D", "Spatial_Intel", "evolution", "工业级3D生成→空间智能基础设施", "tier2")
add_edge("HY_World", "Spatial_Intel", "evolution", "多模态世界模型→通用空间智能", "tier1")
add_edge("Hunyuan_Voyager", "InSpatio_World", "related", "WorldScore 榜首竞逐 / 3D世界模型双雄", "tier2")

# ── MSRA 网络 ──
add_edge("Wang_Tengfei", "Harry_Shum", "lab", "前MSRA研究员 (2021-2023) / MSRA学术网络", "tier2")

# ── 世界模型路线连接 ──
add_edge("Guo_Chunchao", "Model_Based_RL", "maintainer", "混元3D→世界模型+游戏/具身仿真", "tier2")
add_edge("Wang_Tengfei", "Model_Based_RL", "maintainer", "3D世界模型→可交互物理仿真环境", "tier2")

# ── 与已有空间智能人物连接 ──
add_edge("Guo_Chunchao", "Chen_Baoquan", "lab", "同为3D生成+空间智能 / 开源生态", "tier2")
add_edge("Wang_Tengfei", "Zhang_Guofeng", "lab", "3D世界模型路线：HY-World vs InSpatio-World", "tier2")
add_edge("HY_World", "Marble", "related", "World Labs Marble vs 腾讯HY-World / 可交互3D世界赛道", "tier2")

# ── 与生成仿真连接 ──
add_edge("HY_World", "Genie_3", "related", "可交互世界模型：HY-World vs Genie 3", "tier2")

# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 27
data["meta"]["updated"] = "2026-05-26"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v27: 郭春超(腾讯混元3D/Hunyuan3D)+王腾飞(HY-World/Voyager/HKUST PhD Qifeng Chen)+陈启峰导师链，打通腾讯混元3D世界模型全链路(资产生成→世界生成→WorldScore登顶)")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v23 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
for n in new_nodes_added:
    print(f"    - {n}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
