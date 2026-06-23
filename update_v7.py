#!/usr/bin/env python3
"""v7 增量更新：添加CV三大顶会华人Chair中与世界模型相关的人物"""
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
# 1. 何恺明 Kaiming He — ICCV 2023 Program Chair
# ═══════════════════════════════════════════════════════════════
print("\n=== 何恺明 Kaiming He ===")

add_node("Kaiming_He",
    "何恺明 Kaiming He\\nMIT 教授 / ResNet作者\\nICCV 2023 程序委员会主席",
    "person_overseas", "spatial",
    "2007年清华本科，2011年CUHK博士。ResNet（CVPR 2016最佳论文）、Mask R-CNN、Faster R-CNN等核心架构作者。FAIR研究科学家(2016-2024)，2024年加入MIT任教。CVPR/ICCV领域最高引学者之一。近年研究方向聚焦3D生成与世界模型，探索从生成式模型到物理世界理解的路径。ICCV 2023程序委员会主席。")

# ═══════════════════════════════════════════════════════════════
# 2. 孙德庆 Deqing Sun — ICCV 2025 Program Chair
# ═══════════════════════════════════════════════════════════════
print("\n=== Deqing Sun ===")

add_node("Deqing_Sun",
    "孙德庆 Deqing Sun\\nGoogle DeepMind 研究科学家\\nICCV 2025 程序委员会主席",
    "person_overseas", "sim",
    "Google DeepMind研究科学家。ICCV 2025程序委员会主席。在物理世界模型方向上有多项开创性工作：δ-Diffusion（视频演示→物理模拟）、Force Prompting（力场提示实现物理交互视频生成）、Fluid/UniFluid（自回归视觉世界模型）。其研究正推动视频生成模型向可交互物理世界模拟演进。")

# ═══════════════════════════════════════════════════════════════
# 3. 虞晶怡 Jingyi Yu — CVPR 2021 PC / ICCV 2025 GC / ICCV 2027 PC
# ═══════════════════════════════════════════════════════════════
print("\n=== 虞晶怡 Jingyi Yu ===")

add_node("Jingyi_Yu",
    "虞晶怡 Jingyi Yu\\n上海科技大学 讲席教授 / IEEE Fellow\\nCVPR 2021 PC / ICCV 2025 GC",
    "person_overseas", "spatial",
    "Caltech本科、MIT博士。上海科技大学副教务长、信息学院院长。IEEE Fellow、OSA Fellow。CVPR 2021程序委员会主席，ICCV 2025大会主席。研究方向：3D重建与生成、神经渲染(NeRF/3DGS)、具身智能。ICIG 2025「空间智能与世界模型」论坛主旨嘉宾。团队CAST获SIGGRAPH 2025最佳论文奖，CLAY获SIGGRAPH 2024荣誉提名。是空间智能路线在中国学术界的重要推动者。")

# ═══════════════════════════════════════════════════════════════
# 4. 刘策 Ce Liu — CVPR 2020 PC / CVPR 2025 Lead GC
# ═══════════════════════════════════════════════════════════════
print("\n=== 刘策 Ce Liu ===")

add_node("Ce_Liu",
    "刘策 Ce Liu\\nMicrosoft Azure AI 首席架构师\\nCVPR 2020 PC / CVPR 2025 Lead GC",
    "person_overseas", "sim",
    "清华本科/硕士，MIT博士(导师Freeman & Adelson)。Microsoft Azure AI计算机视觉首席架构师。CVPR 2020程序委员会主席，CVPR 2025大会主席(IEEE Fellow)。领导开发Florence视觉基础模型，将其定义为'视觉世界模型'(world model for visual understanding)——统一识别、检测、分割、描述等任务的生成式基础模型。研究方向从经典视觉(光流/SIFT Flow)演进到基础模型/世界模型。")

# ═══════════════════════════════════════════════════════════════
# 5. 吕健勤 Chen Change Loy — CVPR 2026 Program Chair
# ═══════════════════════════════════════════════════════════════
print("\n=== 吕健勤 Chen Change Loy ===")

add_node("Chen_Change_Loy",
    "吕健勤 Chen Change Loy\\nNTU 讲席教授 / MMLab主任\\nCVPR 2026 程序委员会主席",
    "person_overseas", "sim",
    "NTU计算机与数据科学学院讲席教授，MMLab@NTU主任。CVPR 2026程序委员会主席。共同组织CVPR 2025 Tutorial'从视频生成到世界模型'(From Video Generation to World Models)。领导开发LaVie、SeedVR、Seaweed-7B等视频生成基础模型。核心命题：视频生成能否作为通向世界模型的桥梁——连接具身智能、物理推理与决策。")

# ═══════════════════════════════════════════════════════════════
# 6. Olga Russakovsky — ECCV 2024 Program Chair
# ═══════════════════════════════════════════════════════════════
print("\n=== Olga Russakovsky ===")

add_node("Olga_Russakovsky",
    "Olga Russakovsky\\nPrinceton 副教授\\nECCV 2024 程序委员会主席",
    "person_overseas", "spatial",
    "Stanford博士(2015)，师从李飞飞。Princeton大学计算机科学副教授。ECCV 2024程序委员会主席。与李飞飞共同领导ImageNet大规模视觉识别挑战赛(ILSVRC)，该数据集成为深度学习革命的关键催化剂。研究方向：计算机视觉、算法公平性、人机协作AI。其工作为空间智能路线提供了基础数据和方法论支撑。")

# ═══════════════════════════════════════════════════════════════
# 7. 谭铁牛 Tieniu Tan — CVPR 2021 General Chair
# ═══════════════════════════════════════════════════════════════
print("\n=== 谭铁牛 Tieniu Tan ===")

add_node("Tieniu_Tan",
    "谭铁牛 Tieniu Tan\\n中国科学院院士\\nCVPR 2021 大会主席",
    "person_overseas", "spatial",
    "中国科学院院士、自动化研究所研究员。CVPR 2021大会主席——首位担任CVPR大会主席的中国学者。前中国科学院自动化研究所所长。研究方向：生物特征识别、计算机视觉、模式识别。作为中国CV领域学术领袖，其担任CVPR GC标志着中国学者在全球CV学术治理中的里程碑式突破。")

# ═══════════════════════════════════════════════════════════════
# 8. 王井东 Jingdong Wang — ICCV 2025 Program Chair
# ═══════════════════════════════════════════════════════════════
print("\n=== 王井东 Jingdong Wang ===")

add_node("Jingdong_Wang",
    "王井东 Jingdong Wang\\n百度 计算机视觉负责人\\nICCV 2025 程序委员会主席",
    "person_overseas", "spatial",
    "百度计算机视觉负责人。ICCV 2025程序委员会主席。IEEE Fellow。在高分辨率表征学习(HRNet系列)、视觉注意力机制、图像检索等方向有重要贡献。推动CV基础研究向自动驾驶和世界模型应用场景的转化。")

# ═══════════════════════════════════════════════════════════════
# 9. 张少霆 Shaoting Zhang — CVPR 2026 Program Chair
# ═══════════════════════════════════════════════════════════════
print("\n=== 张少霆 Shaoting Zhang ===")

add_node("Shaoting_Zhang",
    "张少霆 Shaoting Zhang\\n上海交通大学 教授\\nCVPR 2026 程序委员会主席",
    "person_overseas", "spatial",
    "上海交通大学教授。CVPR 2026程序委员会主席（首位以SJTU身份担任CVPR PC的学者）。研究方向：医学影像分析、多模态AI。虽然在医疗AI而非世界模型方向，但其担任CVPR PC角色标志着中国学者在CV学术治理中日益重要的地位。")

# ═══════════════════════════════════════════════════════════════
# 10. 华刚 Gang Hua — ICCV 2027 Lead General Chair
# ═══════════════════════════════════════════════════════════════
print("\n=== 华刚 Gang Hua ===")

add_node("Gang_Hua",
    "华刚 Gang Hua\\nAmazon AWS AI Lab\\nICCV 2027 Lead 大会主席",
    "person_overseas", "spatial",
    "Amazon AWS AI Lab研究科学家。ICCV 2027 Lead大会主席（首位担任ICCV Lead GC的华人学者）。IEEE Fellow。研究方向：计算机视觉、多模态学习、以人为中心的视觉理解。其担任ICCV最高领导角色是中国学者在全球CV学术体系中的重要里程碑。")

# ═══════════════════════════════════════════════════════════════
# 11. 吴建鑫 Jianxin Wu — CVPR 2024 Program Chair
# ═══════════════════════════════════════════════════════════════
print("\n=== 吴建鑫 Jianxin Wu ===")

add_node("Jianxin_Wu",
    "吴建鑫 Jianxin Wu\\n南京大学 教授\\nCVPR 2024 程序委员会主席",
    "person_overseas", "spatial",
    "南京大学计算机科学与技术系教授。CVPR 2024程序委员会主席。研究方向：计算机视觉、深度学习、高效模型设计。在轻量化视觉模型、细粒度识别等方向有系列工作。")

# ═══════════════════════════════════════════════════════════════
# 新增边
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增关系边 ===")

# ── 何恺明 ──
add_edge("Kaiming_He", "FeiFei_Li", "lab", "CV社区核心人物 / ICCV 2023 PC", "tier2")
add_edge("Kaiming_He", "Spatial_Intel", "related", "3D生成与世界模型研究", "tier2")

# ── 孙德庆 ──
add_edge("Deqing_Sun", "Google_DeepMind", "employed", "研究科学家 / 物理世界模型", "tier1")
add_edge("Deqing_Sun", "Gen_Video_concept", "maintainer", "δ-Diffusion / Force Prompting", "tier1")
add_edge("Deqing_Sun", "Model_Based_RL", "related", "物理交互视频生成→世界模拟", "tier2")

# ── 虞晶怡 ──
add_edge("Jingyi_Yu", "Spatial_Intel", "maintainer", "3D重建/NeRF/3DGS / 空间智能论坛嘉宾", "tier1")
add_edge("Jingyi_Yu", "Gaussian_Splat", "related", "3D Gaussian Splatting研究方向", "tier2")
add_edge("Jingyi_Yu", "NeRF", "related", "神经渲染研究方向", "tier2")

# ── 刘策 ──
add_edge("Ce_Liu", "Gen_Video_concept", "related", "Florence视觉基础模型→世界模型观", "tier2")
add_edge("Ce_Liu", "Model_Based_RL", "related", "基础模型作为视觉世界模型", "tier2")

# ── 吕健勤 ──
add_edge("Chen_Change_Loy", "Gen_Video_concept", "maintainer", "CVPR 2025 Tutorial'从视频生成到世界模型'", "tier1")
add_edge("Chen_Change_Loy", "Model_Based_RL", "related", "视频生成→世界模型桥接", "tier2")

# ── Olga Russakovsky ──
add_edge("FeiFei_Li", "Olga_Russakovsky", "mentorship", "博士导师 (Stanford 2015)", "tier1")
add_edge("Olga_Russakovsky", "ImageNet", "maintainer", "ILSVRC联合负责人", "tier1")

# ── General Chairs 互相连接 ──
add_edge("Tieniu_Tan", "FeiFei_Li", "lab", "CV社区学术领袖 / CVPR GC", "tier2")
add_edge("Jingyi_Yu", "Tieniu_Tan", "lab", "CVPR 2021共同组织 / 中国CV学术领袖", "tier2")

# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 8
data["meta"]["updated"] = "2026-05-25"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v8: 新增CV三大顶会华人Chair(11人)——何恺明/孙德庆/虞晶怡/刘策/吕健勤/Olga Russakovsky/谭铁牛/王井东/张少霆/华刚/吴建鑫，关联世界模型及学术治理视角")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v7 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

# 运行 rebuild_v4.py
print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
