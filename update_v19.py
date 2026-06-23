#!/usr/bin/env python3
"""v19 增量更新：李飞飞学术谱系——许华哲/夏斐/黄文龙/向宇/Yunzhu Li/Kuan Fang + 导师 Trevor Darrell/Savarese/Torralba/Tedrake + 星海图"""
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
# 1. 导师节点
# ═══════════════════════════════════════════════════════════════
print("\n=== 导师节点 ===")

add_node("Trevor_Darrell",
    "Trevor Darrell\\nUC Berkeley 教授",
    "person_overseas", "sim",
    "UC Berkeley 计算机科学教授，BAIR Lab 核心成员。计算机视觉与机器人学习先驱。"
    "许华哲的博士导师。在跨模态学习、领域自适应、具身AI方向有深厚积累。",
    bold=True
)

add_node("Silvio_Savarese",
    "Silvio Savarese\\nStanford 教授\\nSVL 联合主任",
    "person_overseas", "sim",
    "Stanford 计算机科学教授，与李飞飞共同领导 Stanford Vision and Learning Lab (SVL)。"
    "研究方向：计算机视觉、机器人学、3D场景理解。"
    "指导了 Yuke Zhu、徐丹飞、Kuan Fang、Fei Xia 等多名世界模型/具身智能方向的学者。"
    "前 Salesforce 首席科学家。",
    bold=True
)

add_node("Antonio_Torralba",
    "Antonio Torralba\\nMIT 教授\\nMIT CSAIL",
    "person_overseas", "sim",
    "MIT EECS 教授，MIT CSAIL 核心成员。计算机视觉与场景理解泰斗。"
    "Yunzhu Li 的博士主导师。在视觉场景理解、数据集构建方向有奠基性贡献。"
    "Places 数据集、MIT Indoor 场景数据集创建者。"
)

add_node("Russ_Tedrake",
    "Russ Tedrake\\nMIT 教授\\nToyota Research Institute VP",
    "person_overseas", "sim",
    "MIT EECS 教授，机器人学权威。Toyota Research Institute VP of Robotics Research。"
    "Yunzhu Li 的博士 co-advisor。研究方向：非线性控制、欠驱动机器人、操作规划。"
)

# ═══════════════════════════════════════════════════════════════
# 2. 李飞飞学生节点
# ═══════════════════════════════════════════════════════════════
print("\n=== 李飞飞学生节点 ===")

add_node("Xu_Huazhe",
    "许华哲 Xu Huazhe",
    "person_overseas", "sim",
    "清华电子系本科，UC Berkeley 博士（师从 Trevor Darrell），Stanford 博士后（李飞飞组）。"
    "清华大学交叉信息研究院助理教授、博导，清华具身智能实验室（TEA Lab）负责人。"
    "提出 3D Diffusion Policy (DP3)，已被业内广泛采用。"
    "2023年联合创立星海图（Galbot，融资近30亿/估值200亿），2026年2月离开创办破壳机器人，"
    "押注家庭通用机器人+世界模型+强化学习路线，天使轮数千万美元（云启/顺为/小米战投等）。",
    bold=True
)

add_node("Fei_Xia",
    "夏斐 Fei Xia",
    "person_overseas", "sim",
    "Stanford 博士（师从 Silvio Savarese & Leonidas Guibas），SVL 实验室。"
    "Google DeepMind 机器人团队 Senior Research Scientist。"
    "代表性工作：RT-1/RT-2 (Robotics Transformer)、PaLM-E（562B具身多模态语言模型）、"
    "SayCan、Inner Monologue、AutoRT、Open X-Embodiment。"
    "CoRL 特别创新奖、ICRA 杰出机器人学习论文奖。",
    bold=True
)

add_node("Wenlong_Huang",
    "黄文龙 Wenlong Huang",
    "person_overseas", "sim",
    "UC Berkeley 本科（Deepak Pathak/Pieter Abbeel），Stanford 博士在读（师从李飞飞）。"
    "代表性工作：VoxPoser（LLM驱动的零样本机器人操作）、PaLM-E（562B参数）、"
    "Inner Monologue、Code as Policies。实习于 MIT CSAIL/NVIDIA Robotics/Google Robotics。"
    "ICRA 2023 杰出机器人学习论文奖、CoRL 2024 LEAP 最佳论文奖。"
)

add_node("Yu_Xiang",
    "向宇 Yu Xiang",
    "person_overseas", "sim",
    "Michigan 博士，Stanford SVL 访问学者（Savarese 组）。"
    "前 NVIDIA Research 高级研究科学家（2018-2021）。"
    "UT Dallas 计算机系助理教授，IRVL 实验室主任。"
    "研究方向：机器人视觉感知、3D物体识别与位姿估计。"
)

add_node("Yunzhu_Li",
    "Yunzhu Li",
    "person_overseas", "sim",
    "北大本科，MIT CSAIL 博士（师从 Antonio Torralba & Russ Tedrake），"
    "Stanford 博士后（李飞飞组）。哥伦比亚大学计算机系助理教授，RoboPIL 实验室主任。"
    "研究方向：结构化世界模型用于机器人操作、多模态感知（视觉+触觉+听觉+语言）。"
    "ICRA 最佳论文奖、CoRL 最佳系统论文奖。成果发表于 Nature/Science/RSS/NeurIPS/CVPR。",
    bold=True
)

add_node("Kuan_Fang",
    "Kuan Fang",
    "person_overseas", "sim",
    "清华本科，Stanford 博士（师从李飞飞 & Silvio Savarese）。"
    "UC Berkeley 博士后（Sergey Levine），Boston Dynamics AI Institute 研究员。"
    "康奈尔大学计算机系助理教授。"
    "研究方向：从大规模多模态数据学习通用视运动技能，自主数据生成与持续学习。",
    bold=True
)

# ═══════════════════════════════════════════════════════════════
# 3. 公司节点
# ═══════════════════════════════════════════════════════════════
print("\n=== 公司节点 ===")

add_node("Galbot",
    "星海图 Galbot\\n具身智能机器人 (2023)\\n累计融资近30亿",
    "company_overseas", "sim",
    "2023年由高继扬(CEO/清华→Waymo)、许华哲(首席科学家/清华教授)、赵行(清华)、李天威(UCL)联合创立。"
    "核心产品：R1系列轮式仿人形通用机器人。估值一度突破200亿。"
    "李飞飞团队曾使用 R1 平台训练机器人系统。"
    "2026年2月许华哲离开独立创办破壳机器人。"
)

# ═══════════════════════════════════════════════════════════════
# 4. 新增边
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增关系边 ===")

# ── 许华哲 ──
add_edge("Trevor_Darrell", "Xu_Huazhe", "mentorship", "博士导师 (UC Berkeley)", "tier1")
add_edge("FeiFei_Li", "Xu_Huazhe", "lab", "博士后导师 (Stanford SVL)", "tier1")
add_edge("Xu_Huazhe", "Galbot", "founded", "联合创始人 & 首席科学家 (2023-2026)", "tier1")
add_edge("Xu_Huazhe", "Model_Based_RL", "maintainer", "DP3→世界模型+RL家庭机器人", "tier2")

# ── 夏斐 (Fei Xia) ──
add_edge("Silvio_Savarese", "Fei_Xia", "mentorship", "博士 co-advisor (Stanford SVL)", "tier1")
add_edge("Leonidas_J_Guibas", "Fei_Xia", "mentorship", "博士 co-advisor (Stanford)", "tier1")
add_edge("Fei_Xia", "Google_DeepMind", "employed", "Senior RS / RT-1/RT-2 机器人团队", "tier1")
add_edge("Fei_Xia", "Model_Based_RL", "maintainer", "RT-2/PaLM-E→具身世界模型", "tier2")

# ── 黄文龙 ──
add_edge("FeiFei_Li", "Wenlong_Huang", "mentorship", "博士导师 (Stanford SVL)", "tier1")
add_edge("Wenlong_Huang", "Model_Based_RL", "maintainer", "VoxPoser/PaLM-E→LLM+机器人世界模型", "tier2")

# ── 向宇 (Yu Xiang) ──
add_edge("Silvio_Savarese", "Yu_Xiang", "lab", "Stanford SVL 访问学者", "tier2")
add_edge("Yu_Xiang", "NVIDIA", "employed", "前 Senior RS (2018-2021)", "tier1")
add_edge("Yu_Xiang", "Model_Based_RL", "maintainer", "机器人3D视觉→世界模型感知", "tier2")

# ── Yunzhu Li ──
add_edge("Antonio_Torralba", "Yunzhu_Li", "mentorship", "博士主导师 (MIT CSAIL)", "tier1")
add_edge("Russ_Tedrake", "Yunzhu_Li", "mentorship", "博士 co-advisor (MIT)", "tier1")
add_edge("FeiFei_Li", "Yunzhu_Li", "lab", "博士后导师 (Stanford SVL)", "tier1")
add_edge("Yunzhu_Li", "Model_Based_RL", "maintainer", "结构化世界模型→机器人操作", "tier1")

# ── Kuan Fang ──
add_edge("FeiFei_Li", "Kuan_Fang", "mentorship", "博士 co-advisor (Stanford SVL)", "tier1")
add_edge("Silvio_Savarese", "Kuan_Fang", "mentorship", "博士 co-advisor (Stanford SVL)", "tier1")
add_edge("Kuan_Fang", "Sergey_Levine", "lab", "博士后导师 (UC Berkeley)", "tier1")
add_edge("Kuan_Fang", "Model_Based_RL", "maintainer", "通用视运动技能→世界模型规划", "tier2")

# ── Savarese → 已有学生 / 李飞飞 ──
add_edge("Silvio_Savarese", "Yuke_Zhu", "mentorship", "博士 co-advisor (Stanford SVL)", "tier1")
add_edge("Silvio_Savarese", "Xu_Danfei", "mentorship", "博士 co-advisor (Stanford SVL)", "tier1")
add_edge("Silvio_Savarese", "FeiFei_Li", "lab", "Stanford SVL 联合主任", "tier1")
add_edge("Silvio_Savarese", "Leonidas_J_Guibas", "lab", "Stanford 同事 / 共同指导学生", "tier1")

# ── 交叉互联 ──
add_edge("Wenlong_Huang", "Fei_Xia", "lab", "PaLM-E 合作 / SVL 同门", "tier2")
add_edge("Wenlong_Huang", "Jim_Fan", "lab", "同为李飞飞学生", "tier2")
add_edge("Kuan_Fang", "Xu_Danfei", "lab", "同为 Li+Savarese 学生", "tier2")
add_edge("Kuan_Fang", "Yuke_Zhu", "lab", "同为 Li+Savarese 学生", "tier2")
add_edge("Yunzhu_Li", "Jiajun_Wu", "lab", "Stanford 博后同事 / 3D理解", "tier2")

# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 23
data["meta"]["updated"] = "2026-05-26"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v23: 李飞飞学术谱系扩展——许华哲(+Trevor Darrell/星海图Galbot)/夏斐(+Savarese+Guibas→DeepMind)/黄文龙(李飞飞直博)/向宇(Savarese访问→NVIDIA→UTD)/Yunzhu Li(+Torralba+Tedrake/Columbia)/Kuan Fang(+Savarese→Cornell), 新增Savarese导师节点, 打通SVL核心师承链")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v19 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
for n in new_nodes_added:
    print(f"    - {n}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
