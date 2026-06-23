#!/usr/bin/env python3
"""v8 增量更新：从权龙长文中提取节点和关系"""
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
# 1. 权龙 — ICCV 2011 GC / CVPR 2022 GC / 3D视觉奠基人
# ═══════════════════════════════════════════════════════════════
print("\n=== 权龙 Long Quan ===")

add_node("Long_Quan",
    "权龙 Long Quan",
    "person_overseas", "spatial",
    "1989年法国INPL博士（导师Roger Mohr）。香港科技大学计算机科学教授、IEEE Fellow。ICCV 2011大会主席、CVPR 2022大会主席——首位在CVPR和ICCV均担任过GC的华人学者。1988年成为首位在ICCV发表论文的华人。1995年发表'六点算法'解决三视图几何问题，与Faugeras的七点算法并列为三维视觉两大基础算法。创立VisGraph实验室，培养出王井东、谭平、肖健雄等学生。2015年创立Altizure（后被Apple收购）。研究方向：三维重建、SfM、视觉几何。",
    bold=True)

# 2. Roger Mohr — 权龙博士导师
print("\n=== Roger Mohr ===")

add_node("Roger_Mohr",
    "Roger Mohr",
    "person_overseas", "spatial",
    "法国INPL/INRIA教授，射影几何与计算机视觉研究先驱。1987年参加第一届ICCV，将会议论文集带回实验室，直接启发了权龙的ICCV 1988论文。1989年指导权龙完成博士论文。INRIA Grenoble计算机视觉小组创始成员，是权龙从1985-2002年整16年的学术导师与合作者。")

# 3. 谭平 — 权龙学生 / 世界模型+运动模型
print("\n=== 谭平 ===")

add_node("Tan_Ping",
    "谭平 Tan Ping",
    "person_overseas", "spatial",
    "15岁考入上海交大少年班。2003年入权龙组读博（VisGraph第三位博士生），经沈向洋推荐。新加坡国立大学助理教授(2007-2014)，加拿大高校任教(2014-2019)。后回国先后任360AI研究院副院长、阿里达摩院XR实验室负责人。2023年加入港科大任教，研究三维生成模型，创立光影焕像(Light Illusions)。近期将AGI话语体系下的'世界模型'与机器人领域的'运动模型'结合研究。")

# 4. 肖健雄 — 权龙学生 / AutoX创始人
print("\n=== 肖健雄 ===")

add_node("Xiao_Jianxiong",
    "肖健雄 Xiao Jianxiong",
    "person_overseas", "sim",
    "港科大本科(2008)→Mphil(导师权龙)。本科时即发表ICCV 2007 Oral论文。MIT CSAIL博士(2012 Google Research最佳论文奖)。普林斯顿大学助理教授。2016年辞去教职创立AutoX，专注L4级自动驾驶。开拓RGB-D场景分析和三维深度学习研究。")

# 5. 方天 — 权龙学生 / Altizure联合创始人
print("\n=== 方天 ===")

add_node("Fang_Tian",
    "方天 Fang Tian",
    "person_overseas", "spatial",
    "华南理工本科，经沈向洋推荐入权龙组读博(2006)。VisGraph第六位博士生。摄影发烧友。博士及博后期间为IBM(Image-Based Modeling)系列核心贡献者。2015年与权龙共同创立Altizure，将无人机航拍照片转化为三维实景模型。")

# 6. 危夷晨 — 权龙学生 / 旷视→数坤
print("\n=== 危夷晨 ===")

add_node("Wei_Yichen",
    "危夷晨 Wei Yichen",
    "person_overseas", "spatial",
    "北大本科。2001年入权龙组（VisGraph首批两位博士生之一）。博士研究方向：头发建模(SIGGRAPH发表)。MSRA视觉组12年(2006-2018)，贡献Xbox Kinect/Windows Hello等产品。旷视上海研究院负责人(2018-2021)。数坤科技联席CTO(2021-)。")

# 7. 曾钢 — 权龙学生 / 北大
print("\n=== 曾钢 ===")

add_node("Zeng_Gang",
    "曾钢 Zeng Gang",
    "person_overseas", "spatial",
    "北大本科。2001年与危夷晨同批入权龙组（VisGraph首批两位博士生之一）。博士研究方向：植物建模(SIGGRAPH发表)。苏黎世联邦理工学院助理研究员，北京大学人工智能研究院研究员、博导。")

# 8. 袁路 — 权龙学生 / 微软
print("\n=== 袁路 ===")

add_node("Yuan_Lu",
    "袁路 Yuan Lu",
    "person_overseas", "spatial",
    "清华本科。2005年入权龙组读博（VisGraph第五位博士生）。曾在MSRA实习(导师孙剑)。微软云与AI认知服务部门首席研究经理(2009-至今)，参与多模态大模型研究。微软Pix相机、OfficeLens、BLINK等产品核心技术贡献者。")

# ═══════════════════════════════════════════════════════════════
# 里程碑节点
# ═══════════════════════════════════════════════════════════════

add_node("Six_Point_Algorithm",
    "六点算法 (1995)",
    "milestone", "spatial",
    "权龙1995年发表的突破性算法。以封闭形式解决了三视图几何问题：仅需六点三幅图像即可进行三维重建。与Faugeras的七点算法(两视图)并列为三维视觉两大基础算法。几乎所有后续非标定相机三维重建技术均受此启发。论文：Invariants of Six Points and Projective Reconstruction from Three Uncalibrated Images。")

# ═══════════════════════════════════════════════════════════════
# 公司节点
# ═══════════════════════════════════════════════════════════════

add_node("Altizure",
    "Altizure\\n3D重建云平台 (2015)",
    "company_overseas", "spatial",
    "2015年由权龙与方天共同创立。将无人机航拍照片转化为三维实景模型，形成众包Google Earth。产品覆盖无人机爱好者(C端)及智慧城市/测绘(B端/G端)。后被Apple收购，体现空间智能技术在消费电子巨头中的战略价值。")

add_node("Light_Illusions",
    "光影焕像 Light Illusions\\n3D生成AI公司 (2023)",
    "company_overseas", "spatial",
    "2023年由谭平创立。专注三维生成模型技术，将世界模型与运动模型结合的产学研孵化项目。代表了VisGraph学术谱系在3D生成方向上的最新商业化实践。")

# AutoX 检查
add_node("AutoX",
    "AutoX\\nL4自动驾驶 (2016)",
    "company_overseas", "sim",
    "2016年由肖健雄(Professor X)辞去普林斯顿教职后创立。专注L4级全无人驾驶，在中国多个城市落地Robotaxi运营。将三维视觉与深度学习技术大规模应用于自动驾驶场景理解与决策。")

# ═══════════════════════════════════════════════════════════════
# 新增边
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增关系边 ===")

# ── 师承链 ──
add_edge("Roger_Mohr", "Long_Quan", "mentorship", "博士导师 (1989, INPL/INRIA)", "tier1")

# 权龙 → 学生
add_edge("Long_Quan", "Wei_Yichen", "mentorship", "博士导师 (2006, 首批VisGraph学生)", "tier1")
add_edge("Long_Quan", "Zeng_Gang", "mentorship", "博士导师 (2006, 首批VisGraph学生)", "tier1")
add_edge("Long_Quan", "Tan_Ping", "mentorship", "博士导师 (2007, VisGraph第三人)", "tier1")
add_edge("Long_Quan", "Jingdong_Wang", "mentorship", "博士导师 (2007, 经沈向洋推荐)", "tier1")
add_edge("Long_Quan", "Yuan_Lu", "mentorship", "博士导师 (2009, VisGraph第五人)", "tier1")
add_edge("Long_Quan", "Fang_Tian", "mentorship", "博士导师 (VisGraph第六人, 经沈向洋推荐)", "tier1")
add_edge("Long_Quan", "Xiao_Jianxiong", "mentorship", "Mphil导师 (港科大)", "tier1")

# ── 权龙与里程碑 ──
add_edge("Long_Quan", "Six_Point_Algorithm", "maintainer", "提出者 (1995)", "tier1")

# ── 权龙与公司 ──
add_edge("Long_Quan", "Altizure", "founded", "联合创始人 (2015)", "tier1")
add_edge("Fang_Tian", "Altizure", "founded", "联合创始人", "tier1")
add_edge("Tan_Ping", "Light_Illusions", "founded", "创始人 (2023)", "tier1")
add_edge("Xiao_Jianxiong", "AutoX", "founded", "创始人 (2016)", "tier1")

# ── 权龙与世界模型/空间智能 ──
add_edge("Long_Quan", "Spatial_Intel", "maintainer", "三维重建奠基 / 空间智能学术先驱", "tier1")
add_edge("Six_Point_Algorithm", "Spatial_Intel", "evolution", "三视图几何→现代3D重建理论基石", "tier1")
add_edge("Tan_Ping", "Spatial_Intel", "maintainer", "3D生成 + 世界模型×运动模型", "tier2")

# ── 权龙与CV社区(已有节点) ──
add_edge("Long_Quan", "Gang_Hua", "lab", "CVPR 2022共同组织 (Quan GC, 华刚 PC)", "tier1")
add_edge("Long_Quan", "Tieniu_Tan", "lab", "CVPR GC接力 (2021谭→2022权)", "tier2")
add_edge("Long_Quan", "Jingyi_Yu", "lab", "同为3D重建方向 / ICCV GC角色", "tier2")


# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 9
data["meta"]["updated"] = "2026-05-25"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v9: 新增权龙学术谱系——权龙/Roger Mohr/谭平/肖健雄/方天/危夷晨/曾钢/袁路 + 六点算法 + Altizure/Light Illusions/AutoX，打通权龙→王井东师承链")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v8 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

# 运行 rebuild_v4.py
print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
