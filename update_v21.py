#!/usr/bin/env python3
"""v21 增量更新：王井东学术谱系深挖——沈向洋(MSRA→VisGraph)/张长水(清华硕士导师)/汤晓鸥(CUHK MMLab)/马毅(UC Berkeley)"""
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
# 1. 王井东深挖——清华/张长水 + MSRA/沈向洋 + HKUST/权龙
# ═══════════════════════════════════════════════════════════════
print("\n=== 王井东谱系深挖 ===")

add_node("Zhang_Changshui",
    "张长水 Zhang Changshui",
    "person_overseas", "sim",
    "清华大学自动化系教授。国内最早从事人工智能研究的学者之一。"
    "研究方向：机器学习、模式识别、数据挖掘。"
    "王井东的硕士导师（2001-2004）。其学生还包括贾扬清（Caffe 作者、前阿里技术副总裁）。"
    "清华自动化系是中国AI研究的重要源头院系之一。"
)

add_node("Harry_Shum",
    "沈向洋 Harry Shum",
    "person_overseas", "spatial",
    "微软亚洲研究院（MSRA）创始成员及第三任院长（2004-2013），前微软全球执行副总裁。"
    "中国计算机视觉领域的奠基性组织者之一。MSRA 培养/吸引了一代华人CV学者："
    "汤晓鸥、孙剑、马毅、屠卓文、何恺明、华刚等。"
    "2003-2006年间多次将MSRA实习生推荐至权龙（HKUST VisGraph）读博，"
    "包括王井东（2004）、谭平（2003）、肖健雄（2006）等，"
    "打通了MSRA→VisGraph这一重要人才通道。"
    "现为清华大学高等研究院双聘教授、香港大学计算机系教授。",
    bold=True
)

add_node("Tang_Xiaoou",
    "汤晓鸥 Tang Xiaoou\\n1968-2023\\n商汤科技联合创始人",
    "person_overseas", "spatial",
    "香港中文大学（CUHK）信息工程系教授，多媒体实验室（MMLab）创始人。"
    "商汤科技（SenseTime）联合创始人兼首席科学家。"
    "王晓刚的导师，培养了吕健勤（Chen Change Loy）等大批CV领军人物。"
    "MMLab 与权龙的 VisGraph 是早期中国CV学者参与国际顶会的两大中坚力量。"
    "在深度学习人脸识别方向有奠基性贡献（DeepID系列）。",
    bold=True
)

add_node("Ma_Yi",
    "马毅 Ma Yi\\nUC Berkeley 教授",
    "person_overseas", "spatial",
    "UC Berkeley EECS 教授。清华大学本科，UC Berkeley 博士（2000）。"
    "曾在 UIUC 与 Thomas Huang 共事十年（2000-2010），后任 MSRA 视觉计算组首席研究员。"
    "研究方向：3D 视觉、高维数据分析、压缩感知。"
    "近期提出「白盒 Transformer」（CRATE），推动深度网络的可解释性。"
    "与 Thomas Huang（UIUC同事）、沈向洋（MSRA）均有深厚学术联系。"
)

# ═══════════════════════════════════════════════════════════════
# 2. 新增边
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增关系边 ===")

# ── 张长水 → 王井东：硕士导师 ──
add_edge("Zhang_Changshui", "Jingdong_Wang", "mentorship", "硕士导师 (清华大学, 2001-2004)", "tier1")

# ── 沈向洋 → 王井东/谭平/权龙：MSRA→VisGraph 通道 ──
add_edge("Harry_Shum", "Jingdong_Wang", "mentorship", "MSRA实习导师 / 推荐至权龙组读博 (2004)", "tier1")
add_edge("Harry_Shum", "Tan_Ping", "mentorship", "推荐至权龙组读博 (2003)", "tier2")
add_edge("Harry_Shum", "Long_Quan", "lab", "MSRA→VisGraph 人才推荐通道", "tier1")

# ── 沈向洋 → MSRA 网络 ──
add_edge("Harry_Shum", "Kaiming_He", "lab", "MSRA 同门 / 学术网络", "tier2")

# ── 汤晓鸥 → 王晓刚/权龙 ──
add_edge("Tang_Xiaoou", "Wang_Xiaogang", "mentorship", "博士导师 (CUHK MMLab)", "tier1")
add_edge("Tang_Xiaoou", "Long_Quan", "lab", "MMLab ↔ VisGraph / 中国CV两大先驱", "tier2")

# ── 马毅 → Thomas Huang（已在UIUC共事） ──
add_edge("Ma_Yi", "Thomas_Huang", "lab", "UIUC 同事十年 (2000-2010)", "tier2")

# ── 王井东 → 权龙 ──（补全王井东侧边）

# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 25
data["meta"]["updated"] = "2026-05-26"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v25: 王井东谱系深挖——张长水(清华硕士导师)+沈向洋(MSRA→VisGraph人才通道)+汤晓鸥(CUHK MMLab/商汤)+马毅(UC Berkeley/UIUC同事)，打通清华→MSRA→HKUST→CUHK中国CV学术网")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v21 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
for n in new_nodes_added:
    print(f"    - {n}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
