#!/usr/bin/env python3
"""v11 增量更新：9家世界模型/空间智能创业公司——创始人+公司+关键产品"""
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
# 1. 银河通用 Galaxy Universal — 王鹤 北大教授/Stanford PhD
# ═══════════════════════════════════════════════════════════════
print("\n=== 银河通用 Galaxy Universal ===")

add_node("Wang_He",
    "王鹤 Wang He",
    "person_overseas", "sim",
    "1992年生。清华电子系本科，2021年Stanford博士（师从？）。北大前沿计算研究中心助理教授、博导，北京智源人工智能研究院具身智能研究中心主任。2023年5月创立银河通用。研究方向：具身多模态大模型，合成数据驱动的世界模型仿真。MIT TR35中国入选者(2025)。累计融资超50亿元，估值~30亿美元，为国内估值最高的具身智能初创。"
)

add_node("GalaxyBot",
    "银河通用 GalaxyBot\\n具身大模型通用机器人 (2023)\\n累计融资~$800M / 估值~$3B",
    "company_overseas", "sim",
    "2023年5月由王鹤创立。具身智能赛道国内第一梯队，累计融资约8亿美元。产品Galbot G1（双臂轮式人形机器人）。核心技术路线：合成数据驱动+多模态大模型——用高精物理仿真生成十亿级动作数据预训练，真实数据后训练。发布GraspVLA（全球首个十亿级仿真数据预训练的端到端抓取大模型）、GroceryVLA（零售）、TrackVLA（导航）。已与博世合资、宁德时代/丰田/现代等合作，智慧药店已部署近10家。"
)

add_node("GraspVLA",
    "GraspVLA (2025)\\n十亿级仿真数据端到端抓取大模型",
    "milestone", "sim",
    "银河通用2025年1月发布的全球首个基于十亿级仿真合成动作数据预训练的端到端具身抓取基础大模型。实现零样本泛化能力。核心思路：仿真生成几何信息丰富的3D合成数据（不受光照纹理影响）→大规模预训练→真实数据微调。代表了sim-to-real路线在具身操作领域的SOTA实践。"
)

# ═══════════════════════════════════════════════════════════════
# 2. Genesis AI — 周衔 CMU博士 / 生成式物理引擎
# ═══════════════════════════════════════════════════════════════
print("\n=== Genesis AI ===")

add_node("Zhou_Xian",
    "周衔 Zhou Xian",
    "person_overseas", "sim",
    "1994年生。NTU机械工程本科（最高荣誉），CMU机器人学博士(2024)，师从Katerina Fragkiadaki。博士研究方向：世界模型、模仿学习、强化学习，提出生成式仿真新范式。发起并领导Genesis开源项目（25.4k+ GitHub Stars，最大具身智能开源项目）。2024年12月创立Genesis AI，2025年7月完成$105M种子轮（硅谷具身智能赛道史上最大种子轮），Khosla/Eclipse/红杉中国等投资。"
)

add_node("Genesis_AI",
    "Genesis AI\\n生成式物理AI实验室 (2024)\\n种子轮 $105M",
    "company_overseas", "sim",
    "2024年12月由周衔与Théophile Gervet（前Mistral AI多模态负责人）联合创立。定位全球物理AI实验室+全栈机器人公司。硅谷(Palo Alto)+巴黎双总部。核心产品：生成式物理引擎Genesis——根据自然语言自动生成4D动态物理世界，比现实世界快43万倍，单卡26秒训练可迁移至真机的运动策略。融资$105M种子轮，团队~20人平均年龄不到28岁。"
)

add_node("Genesis_Engine",
    "Genesis 生成式物理引擎 (2024)\\n4D动态世界生成 / 43万倍加速",
    "milestone", "sim",
    "2024年底由CMU/清华/北大/MIT/Stanford等10+机构联合开源。根据自然语言描述自动生成4D动态物理世界（机器人操作、运动策略、交互式3D场景等）。比现实世界快约43万倍，RTX 4090单卡26秒训练可迁移至真机的运动策略。GitHub 25.4k+ Stars，最大具身智能开源项目。代表了生成式仿真替代传统手工建模的范式转变。"
)

# ═══════════════════════════════════════════════════════════════
# 3. HillBot — 苏昊 UCSD教授/李飞飞学生
# ═══════════════════════════════════════════════════════════════
print("\n=== HillBot 山丘机器人 ===")

add_node("Su_Hao",
    "苏昊 Su Hao",
    "person_overseas", "sim",
    "北航本科。UCSD终身教授（2026年将回国任复旦大学电子信息教授）。师从李飞飞，参与缔造ImageNet项目。3D视觉领域里程碑式贡献者：ShapeNet（300万3D模型数据集）、PointNet/PointNet++（3D点云深度学习开创方法），谷歌学术被引超14.5万次。主导开发SAPIEN仿真器与ManiSkill机器人训练平台。CVPR 2024青年学者奖。2024年与北航同窗韩铮联合创立HillBot。"
)

add_node("HillBot",
    "HillBot 山丘机器人\\nAI仿真驱动具身智能 (2024)\\n种子轮 $82.5M",
    "company_overseas", "sim",
    "2024年由韩铮(CEO/北航连续创业者)与苏昊(CTO/UCSD教授)在圣地亚哥联合创立。核心理念：「先去天上修仙，再下凡干活」——在SAPIEN仿真器中进行模块化训练再sim-to-real迁移。核心武器：SAPIEN+ManiSkill（训练速度5倍提升，渲染快10-1000x，GPU内存少2-3倍）+与NVIDIA Cosmos合作生成TB级仿真视频数据。2025年完成$82.5M早期VC轮，高瓴/维塔布里奇等投资，估值百亿级人民币。"
)

# ═══════════════════════════════════════════════════════════════
# 4. Vivix AI — 刘宇 前商汤/CUHK MMLab
# ═══════════════════════════════════════════════════════════════
print("\n=== Vivix AI ===")

add_node("Liu_Yu_Vivix",
    "刘宇 Liu Yu",
    "person_overseas", "sim",
    "CUHK MMLab博士，师从王晓刚教授。前商汤科技执行研究总监，主导AIGC产品「秒画」（上线9天300万用户）。在ImageNet、MOT等国际竞赛中多次夺冠。2025年1月创立Vivix AI，团队不足20人。10个月内估值飙升至超$1.32B，红杉中国/IDG押注。"
)

add_node("Vivix_AI",
    "Vivix AI\\n实时交互式多模态视频生成 (2025)\\n10个月估值 $1.32B",
    "company_overseas", "sim",
    "2025年1月由前商汤核心刘宇创立。专注实时交互式多模态内容生成。核心技术：Vivix Turbo推理引擎——自适应低精度计算+深度学习编译器+混合多维并行，号称「0.6T秒生成T秒画面」，推理速度提升两个数量级。主打产品Tiptap AI通过手势交互实现视频内容实时改造。长远愿景：构建原生多模态系统，视/听/画面作为一等公民在统一标记空间交互。"
)

# ═══════════════════════════════════════════════════════════════
# 5. 爱诗科技 PixelVerse — 王长虎 前字节跳动视觉负责人
# ═══════════════════════════════════════════════════════════════
print("\n=== 爱诗科技 PixelVerse ===")

add_node("Wang_Changhu",
    "王长虎 Wang Changhu",
    "person_overseas", "sim",
    "中科大学士/硕士。前微软亚洲研究院主管研究员，2017年加入字节跳动任AI实验室总监/视觉技术负责人，参与抖音/TikTok从0到1建设。深耕CV领域20年。2023年4月创立爱诗科技，发布PixVerse（全球用户破亿，MAU 1600万+）。"
)

add_node("Aisphere",
    "爱诗科技 AIsphere\\nPixVerse 视频生成→世界模型 (2023)\\n累计融资 $300M+",
    "company_overseas", "sim",
    "2023年4月由王长虎创立。PixVerse（海外）/ 拍我AI（国内）——从AI视频生成工具升级为实时世界模型。代表产品PixVerse V5.6在全球榜单长期位列前2。2026年初发布PixVerse R1——号称全球首个通用实时世界模型，实现无限流/多模态/实时响应。ARR超$40M。累计融资超$300M（含阿里巴巴B轮$60M、鼎晖C轮$300M创亚洲纪录）。全球用户破亿。"
)

add_node("PixVerse_R1",
    "PixVerse R1 (2026)\\n全球首个通用实时世界模型",
    "milestone", "sim",
    "爱诗科技2026年初发布的全球首个通用实时世界模型。从视频生成工具进化为实时交互世界模拟器：「无限流、多模态、实时响应」——用户指令可实时改变视频世界走向。标志着国产视频生成赛道从内容工具向世界模型路线的战略升级。"
)

# ═══════════════════════════════════════════════════════════════
# 6. 影溯科技 InSpatio — 章国锋 浙大教授
# ═══════════════════════════════════════════════════════════════
print("\n=== 影溯科技 InSpatio ===")

add_node("Zhang_Guofeng",
    "章国锋 Zhang Guofeng",
    "person_overseas", "spatial",
    "浙江大学CAD&CG国家重点实验室教授、博导，国家杰出青年科学基金获得者。前商汤数字空间事业群首席科学家。在SLAM和3D重建领域深耕超20年。2025年7月创立影溯科技。联合创始人/CTO刘浩敏（浙大博士，前商汤研究总监，主导业内首个手机端无标志SLAM商业系统）。"
)

add_node("InSpatio",
    "影溯 InSpatio\\n原生3D世界模型 / 空间智能 (2025)\\n天使轮",
    "company_overseas", "spatial",
    "2025年7月由章国锋（浙大教授）与刘浩敏（前商汤研究总监）联合创立。核心产品InSpatio-WorldFM——开源实时交互3D世界模型。技术特色：从海量2D视频「数据升维」提取3D几何与物理规律；「显式锚点+隐式记忆」混合架构支持无限时长生成；单张RTX 4090即可实时推理，训练仅用100张卡。投资方：藕舫天使/正轩投资/招商创投等。"
)

add_node("InSpatio_WorldFM",
    "InSpatio-WorldFM (2025)\\n开源实时交互3D世界模型",
    "milestone", "spatial",
    "影溯科技开源的原生3D世界模型。从海量2D视频中做「数据升维」提取3D几何与物理规律。混合架构「显式锚点+隐式记忆」支持无限时长3D世界生成，单张4090实时推理。代表中国学术界（浙江大学）与世界模型开源的紧密结合。"
)

# ═══════════════════════════════════════════════════════════════
# 7. 极佳科技 GigaVision — 黄冠 清华博士/华为哈勃投资
# ═══════════════════════════════════════════════════════════════
print("\n=== 极佳科技 GigaVision ===")

add_node("Huang_Guan",
    "黄冠 Huang Guan",
    "person_overseas", "sim",
    "清华自动化系AI方向博士。连续创业者：微软亚研→三星→地平线（视觉感知负责人）→鉴智机器人（合伙人/自动驾驶负责人），COCO挑战赛冠军/NIST-FRVT人脸识别世界第一/BEVDet霸榜NuScenes。2023年6月创立极佳科技（国内首家纯血物理AI公司）。90后。"
)

add_node("GigaVision",
    "极佳科技 GigaVision\\n物理AI世界模型 (2023)\\n估值破百亿 / 华为哈勃投资",
    "company_overseas", "sim",
    "2023年6月由黄冠创立。国内首家纯血物理AI公司，定位世界模型驱动的物理世界通用智能。旗舰产品：GigaWorld系列世界模型（WorldArena评测全球第一）、DriveDreamer（全球首个真实世界驱动的自动驾驶世界模型）、GigaBrain系列VLA模型（国内首个利用世界模型数据实现真机泛化）。已服务30+海内外头部车企。2026年1个月内融资25亿元，估值破百亿，华为哈勃首次投资世界模型公司。"
)

add_node("GigaWorld",
    "GigaWorld 系列 (2025)\\n自动驾驶+具身世界模型平台",
    "milestone", "sim",
    "极佳科技的世界模型平台。GigaWorld-1在WorldArena评测中击败Google/英伟达等登顶全球第一。覆盖驾驶世界模型（DriveDreamer）和具身世界模型两大方向，WorldArena评测全球第一。代表国产世界模型在国际评测体系中的里程碑。"
)

# ═══════════════════════════════════════════════════════════════
# 8. 流形空间 Manifold AI — 武伟 前商汤绝影
# ═══════════════════════════════════════════════════════════════
print("\n=== 流形空间 Manifold AI ===")

add_node("Wu_Wei",
    "武伟 Wu Wei",
    "person_overseas", "sim",
    "前商汤科技高管（2015年加入商汤初创），曾任商汤绝影智能云研发总经理，主导商汤「开悟」世界模型研发与落地。联合发起人包括清华教授（长江学者）及清华助理教授。2025年5月创立流形空间，坚持WMA路线。"
)

add_node("Manifold_AI",
    "流形空间 Manifold AI\\n具身智能世界模型 (2025)\\n累计融资约5亿元",
    "company_overseas", "sim",
    "2025年5月由武伟（前商汤绝影）联合清华教授创立。坚持WMA（World Model Action）路线：Reasoning→Dreaming→Acting三位一体。核心方案WorldScape具身基座世界模型：通过海量第一人称视角视频预训练让模型理解物理世界因果。率先全域布局DriveScape(CVPR)/RoboScape(NeurIPS)/AirScape(ACM MM)。累计四轮约5亿元融资，华为哈勃/华控基金/锡创投等投资。"
)

# ═══════════════════════════════════════════════════════════════
# 9. 章鱼动力 SynapX — 都大龙 前地平线/鉴智
# ═══════════════════════════════════════════════════════════════
print("\n=== 章鱼动力 SynapX ===")

add_node("Du_Dalong",
    "都大龙 Du Dalong",
    "person_overseas", "sim",
    "中科院计算所硕士，清华创新领军工程博士。百度IDL创始成员；地平线6号创始员工（深度参与国内首款AI芯片BPU设计）；2021年联合创办鉴智机器人任CTO（2025年底被四维图新并购，A股最大智能驾驶并购案）。2026年1月创立章鱼动力。"
)

add_node("SynapX",
    "章鱼动力 SynapX\\n物理AGI具身智能 (2026)\\n种子轮 ~$50M",
    "company_overseas", "sim",
    "2026年1月由都大龙联合创立。定位物理AGI，提出SYNTH深思架构三大模块：SYNAction（REMA分频多尺度端到端操作架构，System 2→1→0三层闭环）、SYNWorld（VFT-WFM视-力-触统一世界模型）、SYNData（OPDS全模态物理数据系统）。首轮近$50M，地平线/高瓴/小米/顺为/线性投资，后续获新加坡K3（郭鹤年家族）追加。成立不到60天即完成首轮。"
)

# ═══════════════════════════════════════════════════════════════
# 新增边
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增关系边 ===")

# ── 1. 银河通用 ──
add_edge("Wang_He", "GalaxyBot", "founded", "创始人 & CEO (2023)", "tier1")
add_edge("GalaxyBot", "GraspVLA", "maintainer", "核心产品 (2025)", "tier1")
add_edge("GraspVLA", "Model_Based_RL", "evolution", "十亿级仿真合成数据→端到端抓取", "tier2")
add_edge("Wang_He", "FeiFei_Li", "lab", "Stanford空间智能网络 (Stanford PhD)", "tier2")

# ── 2. Genesis AI ──
add_edge("Zhou_Xian", "Genesis_AI", "founded", "创始人 & CEO (2024)", "tier1")
add_edge("Genesis_AI", "Genesis_Engine", "maintainer", "核心产品 (2024)", "tier1")
add_edge("Genesis_Engine", "Model_Based_RL", "evolution", "4D生成式物理世界→通用物理仿真", "tier2")

# ── 3. HillBot ──
add_edge("Su_Hao", "HillBot", "founded", "联合创始人 & CTO (2024)", "tier1")
add_edge("FeiFei_Li", "Su_Hao", "mentorship", "博士导师 (Stanford) / ImageNet", "tier1")
add_edge("HillBot", "Model_Based_RL", "related", "仿真驱动 sim-to-real + NVIDIA Cosmos生态", "tier2")

# ── 4. Vivix AI ──
add_edge("Liu_Yu_Vivix", "Vivix_AI", "founded", "创始人 & CEO (2025)", "tier1")
add_edge("Vivix_AI", "Gen_Video_concept", "evolution", "实时交互式多模态→视频世界模型", "tier2")

# ── 5. 爱诗科技 ──
add_edge("Wang_Changhu", "Aisphere", "founded", "创始人 & CEO (2023)", "tier1")
add_edge("Aisphere", "PixVerse_R1", "maintainer", "核心产品 (2026)", "tier1")
add_edge("PixVerse_R1", "Gen_Video_concept", "evolution", "视频生成→通用实时世界模型", "tier2")

# ── 6. 影溯 ──
add_edge("Zhang_Guofeng", "InSpatio", "founded", "创始人 (2025, 浙大教授)", "tier1")
add_edge("InSpatio", "InSpatio_WorldFM", "maintainer", "开源核心产品 (2025)", "tier1")
add_edge("InSpatio_WorldFM", "Spatial_Intel", "evolution", "原生3D世界模型→空间智能开源路线", "tier2")
add_edge("Zhang_Guofeng", "Spatial_Intel", "maintainer", "SLAM/3D重建→3D世界模型", "tier2")

# ── 7. 极佳科技 ──
add_edge("Huang_Guan", "GigaVision", "founded", "创始人 & CEO (2023)", "tier1")
add_edge("GigaVision", "GigaWorld", "maintainer", "核心产品 (2025)", "tier1")
add_edge("GigaWorld", "Model_Based_RL", "evolution", "WorldArena全球第一→驾驶+具身世界模型", "tier2")

# ── 8. 流形空间 ──
add_edge("Wu_Wei", "Manifold_AI", "founded", "创始人 & CEO (2025)", "tier1")
add_edge("Manifold_AI", "Model_Based_RL", "related", "WMA路线：Reasoning→Dreaming→Acting", "tier2")

# ── 9. 章鱼动力 ──
add_edge("Du_Dalong", "SynapX", "founded", "创始人 & CEO (2026)", "tier1")
add_edge("SynapX", "Model_Based_RL", "related", "SYNTH深思架构：操作+世界+数据全栈", "tier2")


# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 12
data["meta"]["updated"] = "2026-05-25"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v12: 新增9家世界模型/空间智能公司——银河通用(王鹤+GraspVLA)/Genesis AI(周衔+Genesis引擎)/HillBot(苏昊+ShapeNet/PointNet)/Vivix AI(刘宇)/爱诗科技(王长虎+PixVerse R1)/影溯(章国锋+WorldFM)/极佳科技(黄冠+GigaWorld)/流形空间(武伟)/章鱼动力(都大龙+SYNTH)")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v11 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

# 运行 rebuild_v4.py
print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
