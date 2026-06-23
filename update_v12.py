#!/usr/bin/env python3
"""v12 增量更新：补充10家公司的CTO/技术负责人 + 学术谱系（导师/同门）"""
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
# 学术谱系：导师节点
# ═══════════════════════════════════════════════════════════════

print("\n=== 学术谱系：导师 ===")

add_node("Leonidas_J_Guibas",
    "Leonidas J. Guibas\\nStanford 三院院士",
    "person_overseas", "spatial",
    "Stanford大学计算机科学教授。美国国家科学院、国家工程院及艺术与科学三院院士。计算几何、计算机视觉与机器人学领域泰斗。在3D几何计算、形状分析方面有奠基性贡献，Stanford几何计算实验室（Geometric Computation Lab）主任。培养出王鹤等具身智能领军人物。曾任Stanford AI Lab副主任。",
    bold=True
)

add_node("Wang_Xiaogang",
    "王晓刚 Wang Xiaogang\\nCUHK 教授 / 商汤联合创始人",
    "person_overseas", "sim",
    "香港中文大学（CUHK）电子工程系教授，多媒体实验室（MMLab）创始主任。商汤科技联合创始人兼首席科学家。师承汤晓鸥教授。在计算机视觉、深度学习领域发表论文数百篇。培养出刘宇（Vivix AI）、吕健勤（Chen Change Loy, NTU MMLab主任）等视觉领域领军人物。ImageNet/COCO/MOT等多项国际竞赛冠军团队成员。"
)

# ═══════════════════════════════════════════════════════════════
# 2. 各公司CTO/技术负责人
# ═══════════════════════════════════════════════════════════════

print("\n=== 技术负责人 ===")

# ── 银河通用 ──
add_node("Yao_Tengzhou",
    "姚腾洲 Yao Tengzhou",
    "person_overseas", "sim",
    "北航机器人研究所硕士，师从王田苗教授。前ABB集团上海机器人研发中心工程师。2023年与王鹤共同创立银河通用，负责硬件与系统工程。"
)

# ── HillBot ──
add_node("Han_Zheng",
    "韩铮 Han Zheng",
    "person_overseas", "sim",
    "北航本科，苏昊的昔日同窗。连续创业者：创办ZEPP智能穿戴（2018年被华米收购）、火箭科技智能办公（被优客工场收购）。40余项计算机视觉/IoT/NLP专利。2015年Fast Company中国百大创新者。2024年与苏昊联合创立HillBot，任CEO负责商业化。"
)

# ── 极佳科技 ──
add_node("Zhu_Zheng",
    "朱政 Zhu Zheng",
    "person_overseas", "sim",
    "中科院自动化研究所博士(2019)，清华大学自动化系博士后。极佳科技联合创始人兼首席科学家。发表AI顶会论文50+篇，引用1.7万+。代表作SiamRPN（目标跟踪）、BEVDet系列（自动驾驶感知）。负责GigaWorld/GigaBrain等核心模型技术方向。"
)

# ── 章鱼动力 ──
add_node("Liang_Zhujin",
    "梁柱锦 Liang Zhujin",
    "person_overseas", "sim",
    "清华大学创新领军工程博士。物理AI先行者，业内最早推动「世界模型+端到端RL闭环训练体系」落地真实系统的技术专家之一。前鉴智机器人技术副总裁。2026年与都大龙联合创立章鱼动力，负责SYNWorld世界模型等核心技术。"
)

# ── 影溯 ──
add_node("Liu_Haomin",
    "刘浩敏 Liu Haomin",
    "person_overseas", "spatial",
    "浙江大学CAD&CG国家重点实验室博士。前商汤科技研究总监。主导实现业内首个手机端无标志SLAM商业系统——比苹果ARKit和谷歌ARCore早了整整3年。2025年与章国锋教授联合创立影溯科技，任CTO，负责InSpatio-WorldFM核心架构。"
)

# ── 李飞飞同门：苏昊 → 卢策吾等 ──
add_node("Lu_Cewu",
    "卢策吾 Lu Cewu",
    "person_overseas", "sim",
    "Stanford博士，师从李飞飞。上海交通大学计算机系教授、博导。穹彻智能（Noematrix）创始人，专注机器人操作与技能学习。作为苏昊的同门师弟，代表了李飞飞学术谱系从3D视觉向机器人操作的延伸。ICRA/IROS等机器人顶会最佳论文奖获得者。"
)

# ── 爱诗科技 ──
add_node("Xie_Xuzhang",
    "谢旭璋 Xie Xuzhang",
    "person_overseas", "sim",
    "北京大学光华管理学院毕业。曾任光源资本董事，专注科技领域融资与IPO。2023年与王长虎联合创立爱诗科技，负责商业运营与海外市场拓展。"
)

# ═══════════════════════════════════════════════════════════════
# 新增边
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增关系边 ===")

# ── 学术谱系 ──
add_edge("Leonidas_J_Guibas", "Wang_He", "mentorship", "博士导师 (Stanford 2021)", "tier1")
add_edge("Wang_Xiaogang", "Liu_Yu_Vivix", "mentorship", "博士导师 (CUHK MMLab)", "tier1")

# ── 李飞飞门下师兄弟链 ──
add_edge("FeiFei_Li", "Lu_Cewu", "mentorship", "博士导师 (Stanford)", "tier1")
add_edge("Su_Hao", "Lu_Cewu", "lab", "同门师兄弟 (Stanford 李飞飞组)", "tier2")
add_edge("Lu_Cewu", "Andrej_Karpathy", "lab", "同门 (Stanford 李飞飞组)", "tier2")

# ── 银河通用：王鹤 + 姚腾洲 ──
add_edge("Wang_He", "Yao_Tengzhou", "lab", "联合创始人 (2023, GalaxyBot)", "tier1")
add_edge("Yao_Tengzhou", "GalaxyBot", "founded", "联合创始人 / 硬件负责人", "tier1")

# ── HillBot：苏昊 + 韩铮 ──
add_edge("Su_Hao", "Han_Zheng", "lab", "联合创始人 / 北航同窗 (2024, HillBot)", "tier1")
add_edge("Han_Zheng", "HillBot", "founded", "联合创始人 & CEO", "tier1")

# ── 极佳科技：黄冠 + 朱政 ──
add_edge("Huang_Guan", "Zhu_Zheng", "lab", "联合创始人 (2023, GigaVision)", "tier1")
add_edge("Zhu_Zheng", "GigaVision", "founded", "联合创始人 & 首席科学家", "tier1")

# ── 章鱼动力：都大龙 + 梁柱锦 ──
add_edge("Du_Dalong", "Liang_Zhujin", "lab", "联合创始人 (2026, SynapX)", "tier1")
add_edge("Liang_Zhujin", "SynapX", "founded", "联合创始人 / 技术负责人", "tier1")

# ── 影溯：章国锋 + 刘浩敏 ──
add_edge("Zhang_Guofeng", "Liu_Haomin", "lab", "联合创始人 (2025, InSpatio)", "tier1")
add_edge("Liu_Haomin", "InSpatio", "founded", "联合创始人 & CTO", "tier1")

# ── 爱诗科技：王长虎 + 谢旭璋 ──
add_edge("Wang_Changhu", "Xie_Xuzhang", "lab", "联合创始人 (2023, AIsphere)", "tier1")
add_edge("Xie_Xuzhang", "Aisphere", "founded", "联合创始人 / 商业运营负责人", "tier1")

# ── 吕健勤(Chen Change Loy)也是王晓刚学生 ──
add_edge("Wang_Xiaogang", "Chen_Change_Loy", "mentorship", "博士导师 (CUHK MMLab)", "tier1")

# ── 刘宇 & 吕健勤同门 ──
add_edge("Liu_Yu_Vivix", "Chen_Change_Loy", "lab", "同门师兄弟 (CUHK MMLab 王晓刚组)", "tier2")

# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 14
data["meta"]["updated"] = "2026-05-25"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v14: 补充学术谱系与CTO/技术负责人——Leonidas J. Guibas(王鹤导师)/王晓刚(刘宇导师)/姚腾洲/韩铮/朱政/梁柱锦/刘浩敏/卢策吾/谢旭璋，打通Stanford几何计算→具身智能、CUHK MMLab→商汤/Vivix学术链")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v12 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

# 运行 rebuild_v4.py
print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
