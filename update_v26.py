#!/usr/bin/env python3
"""v26 增量更新：沈向洋学术谱系——孙剑/刘利刚/吕乐 + 补汤晓鸥→何恺明导师边"""
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

add_node("Sun_Jian",
    "孙剑 Sun Jian\\n1976-2022\\n旷视科技首席科学家",
    "person_overseas", "spatial",
    "西安交大本硕博（1997-2006）。MSRA首席研究员，长期受沈向洋指导。"
    "ResNet共同作者之一（CVPR 2016最佳论文），MobileNet系列核心贡献者。"
    "旷视科技（Megvii）首席科学家、研究院院长。西安交大人工智能学院首任院长。"
    "在轻量化视觉模型、图像识别领域做出重大贡献。"
    "2022年因病去世，被视为中国CV从学术到产业化的关键桥梁人物。",
    bold=True
)

add_node("Liu_Ligang",
    "刘利刚 Liu Ligang\\n浙江大学 教授",
    "person_overseas", "spatial",
    "浙江大学计算机辅助设计与图形学国家重点实验室教授、求是特聘教授。"
    "博士毕业后在MSRA从事博士后研究三年（导师沈向洋），在沈向洋指导下"
    "确立SIGGRAPH发表目标，后成为SIGGRAPH常客。"
    "研究方向：计算机图形学、几何处理、3D视觉。"
    "几何处理与3D重建技术是空间智能和3D世界模型的基础设施。"
)

add_node("Lyu_Le",
    "吕乐 Le Lu\\nIEEE/AAIA Fellow\\n医学影像AI",
    "person_overseas", "spatial",
    "1999-2001年沈向洋学生（MSR）。IEEE Fellow、AAIA Fellow。"
    "约翰霍普金斯大学博士（2007）。先后在西门子、NVIDIA、PAII等机构"
    "从事医学影像AI研究。医学计算机视觉领域的代表性学者。"
    "虽非直接从事世界模型研究，但其在3D医学影像分析中的空间表征学习"
    "与空间智能共享方法论基础。"
)

# ═══════════════════════════════════════════════════════════════
# 2. 新增边
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增关系边 ===")

# ── 沈向洋 → 学生/门生 ──
add_edge("Harry_Shum", "Sun_Jian", "mentorship",
    "MSRA院长→首席研究员 / 长期学术指导 (2006-2016)", "tier1")
add_edge("Harry_Shum", "Liu_Ligang", "mentorship",
    "MSRA博士后导师 / 指导SIGGRAPH研究", "tier1")
add_edge("Harry_Shum", "Lyu_Le", "mentorship",
    "MSR学生导师 (1999-2001)", "tier1")
add_edge("Harry_Shum", "Gang_Hua", "mentorship",
    "MSRA多年合作与师承 / 微软CV科学主任", "tier1")

# ── 沈向洋 → 汤晓鸥 (MSRA CV组传承) ──
add_edge("Harry_Shum", "Tang_Xiaoou", "lab",
    "邀请汤晓鸥接管MSRA计算机视觉组 / 共同培育华人CV人才", "tier1")

# ── 汤晓鸥 → 何恺明 (补漏——CUHK博士导师) ──
add_edge("Tang_Xiaoou", "Kaiming_He", "mentorship",
    "博士导师 (CUHK MMLab, 2011-2016) / ResNet共同作者", "tier1")

# ── 孙剑 → MSRA/旷视 关联 ──
add_edge("Sun_Jian", "Kaiming_He", "lab",
    "MSRA同事+ResNet共同作者 / 同为沈向洋门生", "tier1")
add_edge("Sun_Jian", "Tang_Xiaoou", "lab",
    "MSRA CV组核心成员 / 沈向洋+汤晓鸥双重学术网络", "tier2")

# ── 世界模型关联 ──
add_edge("Liu_Ligang", "Spatial_Intel", "maintainer",
    "几何处理+3D重建→空间智能基础设施", "tier2")
add_edge("Lyu_Le", "Model_Based_RL", "related",
    "3D医学影像空间表征→隐空间建模", "tier2")

# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 30
data["meta"]["updated"] = "2026-05-26"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v30: 沈向洋学术谱系——孙剑(旷视首席科学家/ResNet共同作者)+刘利刚(浙大/MSRA→SIGGRAPH几何处理)+吕乐(医学CV/IEEE Fellow)+补汤晓鸥→何恺明博士导师边，完善MSRA→CUHK人才网络")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v26 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
for n in new_nodes_added:
    print(f"    - {n}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
