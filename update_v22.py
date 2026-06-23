#!/usr/bin/env python3
"""v22 增量更新：三大流派.md 综合补充——JEPA/空间智能/生成仿真派核心人物+里程碑"""
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
# 一、JEPA 流派补充
# ═══════════════════════════════════════════════════════════════
print("\n=== 一、JEPA 流派 ===")

add_node("Jin_Xin",
    "金鑫 Jin Xin",
    "person_overseas", "jepa",
    "华为云盘古多模态大模型首席架构师。负责华为视频生成大模型与世界模型团队。"
    "推动 Drive-OccWorld、WEWA 架构、WordGrow 等多条世界模型路线，"
    "是华为从视频生成向世界模型演进的关键技术推手。"
)

# V-JEPA 2 边（节点 ID 为 V_JEPA2, 已存在）
add_edge("Mahmoud_Assran", "V_JEPA2", "maintainer", "第一作者 (Meta FAIR)", "tier1")
add_edge("V_JEPA2", "JEPA_concept", "evolution", "JEPA 路线在具身智能的工程落地", "tier1")
add_edge("Yann_LeCun", "V_JEPA2", "maintainer", "JEPA 路线的标志性成果", "tier1")

# 金鑫边
add_edge("Jin_Xin", "Model_Based_RL", "maintainer", "华为世界模型多路线布局→视频生成+占用预测", "tier2")

# ═══════════════════════════════════════════════════════════════
# 二、空间智能流派补充
# ═══════════════════════════════════════════════════════════════
print("\n=== 二、空间智能流派 ===")

# ── 人物 ──
add_node("Liu_Yebin",
    "刘烨斌 Liu Yebin",
    "person_overseas", "spatial",
    "清华大学自动化系长聘教授，国家杰青，IEEE Fellow。三维视觉、数字人与空间智能方向。"
    "发表 TPAMI/SIGGRAPH/CVPR/ICCV 论文百篇，引用 13000+。成果许可输出至华为、字节、商汤等 8 家企业。"
    "其三维重建工作与世界模型的 3D 表征技术高度相关。"
)

add_node("Gao_Lin",
    "高林 Gao Lin",
    "person_overseas", "spatial",
    "中国科学院计算技术研究所研究员，国家优青（计算机图形学，2024）。"
    "国内 3D AIGC 方向代表人物。在可微渲染、3D 生成模型方面的工作为世界模型的空间表征提供了重要学术基础。"
)

add_node("Zhang_Zhaoxiang",
    "张兆翔 Zhang Zhaoxiang",
    "person_overseas", "spatial",
    "中国科学院自动化研究所研究员，长江学者特聘教授，IAPR Fellow。"
    "模式识别实验室常务副主任，NeurIPS/ICML/CVPR/ICCV 领域主席。"
    "在 4D 世界模型方向有重要贡献，是国内 3D 视觉向世界模型演进的关键学者。"
)

add_node("Zhao_Hengshuang",
    "赵恒爽 Zhao Hengshuang",
    "person_overseas", "spatial",
    "香港大学助理教授，国家优青。博士师从贾佳亚（CUHK）。MIT 及牛津博士后。"
    "CVPR/NeurIPS/TPAMI 发表论文 100+，引用约 40000。"
    "与白翔合作的 HERMES（ICCV 2025）是首个统一 3D 场景理解与生成的世界模型。"
)

add_node("Jiang_Li",
    "蒋理 Jiang Li",
    "person_overseas", "spatial",
    "香港中文大学（深圳）助理教授。三维场景感知、表征学习与世界模型方向新锐学者。"
    "聚焦赋予机器理解、建模并与真实三维世界互动的能力。与趣丸科技合作 Kiss3DGen 项目。"
)

add_node("Chen_Yingcong",
    "陈颖聪 Chen Yingcong",
    "person_overseas", "spatial",
    "香港科技大学（广州）人工智能学域助理教授。2020 年博士毕业于 CUHK，MIT 博士后。"
    "研究方向：文本生成视频、3D 场景生成与世界模型。在自动驾驶仿真领域通过视频生成解决罕见场景长尾问题。"
    "与趣丸科技合作推出 Kiss3DGen。"
)

# ── 里程碑 ──
add_node("InSpatio_World",
    "InSpatio-World (2026)\\n3D空间架构 4D动态世界\\nWorldScore-Dynamic 榜首",
    "milestone", "spatial",
    "浙江大学章国锋团队（影溯智能）2026 年 3 月发布并开源。基于 3D 空间架构从单目视频生成可实时交互的 4D 动态世界。"
    "摒弃纯 2D 视频路径，以更具第一性原理的 3D 空间架构实现实时交互。"
    "力压同类模型登顶李飞飞牵头的 WorldScore-Dynamic 权威榜单。"
)

add_node("HERMES",
    "HERMES (ICCV 2025)\\n首个统一3D理解与生成\\n的世界模型",
    "milestone", "spatial",
    "赵恒爽（港大）与白翔（华中科大）合作提出。首个统一 3D 场景理解与生成的世界模型。"
    "在 3D 空间推理方向有重要贡献，代表了 3D 视觉从分别理解/生成走向统一世界模型的趋势。"
)

add_node("Kairos_3",
    "开悟 3.0 Kairos 3.0\\n商汤绝影世界模型\\n智能驾驶 3.0 阶段",
    "milestone", "spatial",
    "商汤科技王晓刚团队 2025 年 12 月开源。提出世界模型带来智能驾驶从 1.0（规则驱动）→2.0（数据驱动）→3.0（世界模型驱动）的范式跃迁。"
)

# ── 空间智能边 ──
add_edge("Liu_Yebin", "Spatial_Intel", "maintainer", "3D数字人+空间智能→世界模型表征", "tier2")
add_edge("Gao_Lin", "Spatial_Intel", "maintainer", "3D AIGC+可微渲染→世界模型空间表征", "tier2")
add_edge("Zhang_Zhaoxiang", "Spatial_Intel", "maintainer", "4D世界模型+模式识别→空间智能", "tier1")
add_edge("Jiajun_Wu", "Zhang_Zhaoxiang", "lab", "同为3D视觉向世界模型演进学者", "tier2")

# 赵恒爽（Jiaya_Jia 节点在后方统一处理）
add_edge("Zhao_Hengshuang", "HERMES", "maintainer", "第一作者 (ICCV 2025)", "tier1")
add_edge("HERMES", "Spatial_Intel", "evolution", "统一3D理解+生成→空间智能", "tier2")

# 蒋理 & 陈颖聪
add_edge("Jiang_Li", "Spatial_Intel", "maintainer", "3D场景感知+表征学习→空间智能", "tier2")
add_edge("Chen_Yingcong", "Spatial_Intel", "maintainer", "3D世界模型+视频生成→空间智能", "tier2")
add_edge("Jiang_Li", "Chen_Yingcong", "lab", "Kiss3DGen 合作 / 粤港澳3D生成网络", "tier2")

# InSpatio-World
add_edge("Zhang_Guofeng", "InSpatio_World", "maintainer", "第一作者 / 影溯智能开源 (2026.3)", "tier1")
add_edge("InSpatio_World", "InSpatio", "evolution", "影溯智能核心产品", "tier1")
add_edge("InSpatio_World", "Spatial_Intel", "evolution", "3D空间架构4D世界→空间智能", "tier2")

# Kairos 3.0
add_edge("Wang_Xiaogang", "Kairos_3", "maintainer", "商汤绝影世界模型 / 智能驾驶3.0", "tier1")
add_edge("Kairos_3", "Spatial_Intel", "evolution", "世界模型驱动智能驾驶→空间智能", "tier2")

# ═══════════════════════════════════════════════════════════════
# 三、生成仿真流派（学习仿真）补充
# ═══════════════════════════════════════════════════════════════
print("\n=== 三、生成仿真流派 ===")

# ── 人物 ──
add_node("Masayoshi_Tomizuka",
    "Masayoshi Tomizuka\\nUC Berkeley 教授\\n美国国家工程院院士",
    "person_overseas", "sim",
    "UC Berkeley 机械工程系教授，美国国家工程院院士。机电控制与机器人学先驱。"
    "陈建宇的博士导师。在运动控制、人机交互方向有奠基性贡献。"
)

add_node("Chen_Jianyu",
    "陈建宇 Chen Jianyu",
    "person_overseas", "sim",
    "清华大学交叉信息研究院助理教授、博导（28岁），星动纪元创始人。"
    "UC Berkeley 博士（师从 Masayoshi Tomizuka），姚期智邀请回国。"
    "研究方向：具身智能、人形机器人、强化学习。"
    "ERA-42 端到端具身模型作者，Ctrl-World 在 World Arena 榜单登顶（2026.2）。"
    "星动纪元累计融资超 16 亿元（吉利/阿里/联想/海尔/北汽/三星等 16 家产业方）。",
    bold=True
)

add_node("Zhao_Xing",
    "赵行 Zhao Xing",
    "person_overseas", "sim",
    "清华大学交叉信息研究院助理教授，MARS Lab 负责人。MIT 博士，前 Waymo 研究科学家。"
    "星海图联合创始人兼首席科学家。提出「一脑多型」理念——同一 AI 大脑控制轮式、足式等不同形态机器人。"
    "研究方向：多模态学习、自动驾驶、端到端具身大模型。"
)

add_node("Gao_Jiyang",
    "高继扬 Gao Jiyang",
    "person_overseas", "sim",
    "星海图（Galbot）创始人兼 CEO。清华电子系本科，南加大 CV 博士。"
    "前 Waymo 视觉感知研究员，前 Momenta 多模块/产品负责人。"
    "2023 年联合创立星海图，累计融资超 30 亿元，估值突破 200 亿元，国内估值最高具身智能企业。"
    "投资方：高瓴创投、美团龙珠、正心谷、北汽产投、金鼎资本等。",
    bold=True
)

add_node("Lu_Zongqing",
    "卢宗青 Lu Zongqing",
    "person_overseas", "sim",
    "北京大学计算机学院长聘副教授，国家级青年人才，智源学者。"
    "前智源研究院多模态交互研究中心负责人。"
    "提出 Being-0——首个集运动、导航、灵巧操作于一体的人形机器人通用智能体（2025）。"
    "具身智能创业公司 BeingBeyond 创始人。"
)

add_node("Cao_Xudong",
    "曹旭东 Cao Xudong",
    "person_overseas", "sim",
    "Momenta CEO。2026 年 4 月宣布 R7 强化学习世界模型量产首发。"
    "主张世界模型+强化学习是物理 AI 的两大核心支柱。"
    "技术路线与 DeepMind Dreamer 方向一致：世界模型生成仿真数据→RL 训练策略→迁移真实车辆。"
)

add_node("Xiong_Rong",
    "熊蓉 Xiong Rong",
    "person_overseas", "sim",
    "浙江大学求是特聘教授，浙江人形机器人创新中心首席科学家。"
    "2026 年获国际机器人联合会「塑造机器人未来的女性」奖（全球仅 11 位，中国唯一）。"
    "研究智能移动机器人逾二十年，主导制定国家人形机器人通用智能控制系统标准。"
    "联合华为、海康等 41 家单位推进具身智能标准化。"
)

add_node("Wei_Yunchao",
    "魏云超 Wei Yunchao",
    "person_overseas", "sim",
    "北京交通大学计算机学院教授，国家高层次青年人才，IEEE 高级会员。"
    "与豆包大模型团队共同开发 VideoWorld——首个纯视觉、无语言参与的世界模型。"
    "通过观看数万局围棋高手对战视频自主领悟规则，以职业 5 段实力击败人类。"
    "从纯视觉角度提供了不同于 LLM 的推理路径。"
)

# ── 里程碑 ──
add_node("Genie_3",
    "Genie 3 (2025.8)\\n720p 24fps 实时交互\\n通用世界模型",
    "milestone", "sim",
    "Google DeepMind 发布。目前最接近实时交互通用世界模型的成果：720p、24fps 生成可持续导航的 3D 环境。"
    "无硬编码物理引擎——所有行为从训练数据中学习。正在被用于训练 SIMA 智能体。"
    "代表了从视频生成模型向可交互世界模拟器的关键跨越。"
)

add_node("Dreamer_V4",
    "Dreamer V4 (2025)\\n纯离线数据挖钻石\\n世界模型+RL融合",
    "milestone", "sim",
    "Danijar Hafner 系列最新版。标志性成就：仅凭离线数据在 Minecraft 中挖到钻石——"
    "此前 OpenAI VPT 需要 27 万小时标注视频 + 19.4 万小时在线 RL，Dreamer V4 数据量仅为前者 1%。"
    "人类已可交互式在其世界模型中游玩。模糊了生成环境与 RL 训练的边界。"
)

add_node("Being_0",
    "Being-0 (2025)\\n首个集运动+导航+操作\\n的人形机器人通用智能体",
    "milestone", "sim",
    "北京大学卢宗青团队提出。首个集运动、导航、灵巧操作于一体的人形机器人通用智能体。"
    "代表了从单任务 RL 到通用具身智能体的重要探索。"
)

add_node("Ctrl_World",
    "Ctrl-World (2026.2)\\nWorld Arena 榜单登顶\\n端到端具身世界模型",
    "milestone", "sim",
    "陈建宇（清华/星动纪元）与 Chelsea Finn（Stanford）合作。"
    "2026 年 2 月在李飞飞牵头的全球具身智能评测 World Arena 榜单登顶。"
    "端到端具身世界模型，代表了中国 90 后学者在国际具身智能竞赛中的最高水平。"
)

add_node("VideoWorld",
    "VideoWorld (2025)\\n首个纯视觉无语言世界模型\\n围棋职业5段",
    "milestone", "sim",
    "魏云超（北京交大）与豆包大模型团队共同开发。首个纯视觉、无语言模型参与的世界模型。"
    "仅通过观看数万局围棋高手对战视频自主领悟规则，以职业 5 段实力击败人类对手。"
    "证明了纯视觉推理可以独立于语言模型实现对复杂系统的深刻理解。"
)

add_node("HappyOyster",
    "HappyOyster (2026.4)\\n阿里ATH 可交互AI数字世界\\n对标 Genie 3",
    "milestone", "sim",
    "阿里 ATH 创新事业部 2026 年 4 月发布。对标 Google Genie 3，"
    "支持用户实时构建可互动、可演绎、可探索的 AI 数字世界。"
    "阿里在视频生成领域多年积累向世界模型方向延伸的重要节点。"
)

add_node("X_World",
    "X-World (2026.4)\\n小鹏汽车世界模型\\n两阶段可控多视角生成",
    "milestone", "sim",
    "小鹏汽车 2026 年 4 月发布。基于视频扩散生成技术构建可控多视角生成式世界模型。"
    "两阶段训练：①将大型预训练视频生成模型改造为可控多摄像头世界模型；"
    "②通过分块因果架构+少步自强制学习实现实时推理。已在闭环仿真测试与在线闭环中应用。"
    "正在研发 720 亿参数超大规模自研模型。"
)

add_node("Drive_OccWorld",
    "Drive-OccWorld (2024)\\n以视觉为中心的占用预测\\n世界模型",
    "milestone", "sim",
    "华为联合浙江大学 2024 年发布。以视觉为中心的占用预测世界模型，"
    "用于自动驾驶场景的端到端世界理解与预测。华为 Drive 系列世界模型的开端。"
)

add_node("WordGrow",
    "WordGrow (2025)\\n单卡30分钟生成272m²\\n超大室内场景",
    "milestone", "sim",
    "华为联合上海交大/华中科技大学 2025 年发布。单张 GPU 30 分钟生成 272 m² 超大规模室内场景。"
    "结合 LLM 布局推理与程序化 3D 生成，代表了世界模型在室内空间生成方向的突破。"
)

# ── 生成仿真边 ──
# 星海图三角
add_edge("Masayoshi_Tomizuka", "Chen_Jianyu", "mentorship", "博士导师 (UC Berkeley)", "tier1")
add_edge("Chen_Jianyu", "Zhao_Xing", "lab", "清华交叉信息院同事 / 具身智能", "tier2")

# 陈建宇
add_edge("Chen_Jianyu", "Star_Era", "founded", "创始人 & CEO (2023)", "tier1")
add_edge("Chen_Jianyu", "Ctrl_World", "maintainer", "与 Chelsea Finn 合作 / World Arena 登顶", "tier1")
add_edge("Chelsea_Finn", "Ctrl_World", "maintainer", "Stanford 合作者 (2026.2)", "tier1")
add_edge("Ctrl_World", "Model_Based_RL", "evolution", "端到端具身世界模型→RL落地", "tier2")
add_edge("Chen_Jianyu", "Model_Based_RL", "maintainer", "星动纪元 ERA-42→具身世界模型+RL", "tier2")

# 星海图
add_edge("Gao_Jiyang", "Galbot", "founded", "创始人 & CEO (2023)", "tier1")
add_edge("Zhao_Xing", "Galbot", "founded", "联合创始人 & 首席科学家", "tier1")
add_edge("Gao_Jiyang", "Zhao_Xing", "lab", "清华电子系校友 / 星海图共同创始人", "tier2")
add_edge("Gao_Jiyang", "Xu_Huazhe", "lab", "星海图共同创始人", "tier2")

# 卢宗青
add_edge("Lu_Zongqing", "Being_0", "maintainer", "第一作者 (2025)", "tier1")
add_edge("Lu_Zongqing", "BeingBeyond", "founded", "创始人 (BeingBeyond)", "tier1")
add_edge("Being_0", "Model_Based_RL", "evolution", "人形机器人通用智能体→具身世界模型", "tier2")

# 熊蓉
add_edge("Xiong_Rong", "Model_Based_RL", "maintainer", "人形机器人标准化→具身世界模型落地", "tier2")

# 魏云超 & VideoWorld
add_edge("Wei_Yunchao", "VideoWorld", "maintainer", "与豆包大模型团队共同开发", "tier1")
add_edge("VideoWorld", "Model_Based_RL", "evolution", "纯视觉世界模型→无语言推理", "tier2")

# Genie 3
add_edge("Tim_Brooks", "Genie_3", "maintainer", "核心贡献者 (Google DeepMind)", "tier1")
add_edge("Google_DeepMind", "Genie_3", "maintainer", "2025.8 发布 / 720p 24fps", "tier1")
add_edge("Genie_3", "SIMA2", "evolution", "Genie 3 环境→SIMA 智能体训练", "tier2")
add_edge("Genie_3", "Genie2", "evolution", "Genie 系列最新版", "tier1")
add_edge("Genie_3", "Model_Based_RL", "evolution", "可交互环境生成→RL训练基础设施", "tier2")

# Dreamer V4
add_edge("Danijar_Hafner", "Dreamer_V4", "maintainer", "Dreamer 系列最新版 (2025)", "tier1")
add_edge("Dreamer_V4", "Dreamer4", "evolution", "Dreamer 系列最新版 / 离线RL突破", "tier1")
add_edge("Dreamer_V4", "DreamerV3", "evolution", "Dreamer 系列演进", "tier1")
add_edge("Dreamer_V4", "Model_Based_RL", "evolution", "世界模型+RL融合 / 纯想象训练", "tier2")
add_edge("Dreamer_V4", "Genie_3", "related", "生成环境+RL训练的两条融合路线", "tier2")

# HappyOyster & X-World
add_edge("HappyOyster", "Model_Based_RL", "evolution", "阿里可交互AI世界→世界模型平台", "tier2")
add_edge("X_World", "Model_Based_RL", "evolution", "小鹏自动驾驶世界模型→闭环仿真", "tier2")

# 华为世界模型
add_edge("Jin_Xin", "Drive_OccWorld", "maintainer", "华为 Drive 系列世界模型", "tier1")
add_edge("Jin_Xin", "WordGrow", "maintainer", "华为世界模型室内场景生成", "tier1")
add_edge("Drive_OccWorld", "Model_Based_RL", "evolution", "占用预测世界模型→自动驾驶", "tier2")
add_edge("WordGrow", "Spatial_Intel", "evolution", "程序化3D生成→空间智能", "tier2")

# 曹旭东
add_edge("Cao_Xudong", "Momenta", "founded", "Momenta CEO / RL世界模型量产", "tier1")
add_edge("Cao_Xudong", "Model_Based_RL", "maintainer", "世界模型+RL=物理AI两大支柱", "tier2")

# ── 补充公司节点 ──
add_node("Star_Era",
    "星动纪元 Star Era\\n具身智能 (2023)\\n融资超16亿",
    "company_overseas", "sim",
    "2023 年由陈建宇（清华助理教授）创立。核心产品 ERA-42 端到端具身模型。"
    "2026 年 Ctrl-World 在 World Arena 榜单登顶。"
    "累计融资超 16 亿元，投资方包括吉利资本、阿里巴巴、联想、海尔、北汽、三星等 16 家产业方。"
)

add_node("BeingBeyond",
    "BeingBeyond\\n人形机器人通用智能体\\n卢宗青创立 (2025)",
    "company_overseas", "sim",
    "北京大学卢宗青团队孵化。方向：人形机器人通用智能体，"
    "基于 Being-0 的多模态感知-规划-执行一体化框架。"
)

add_node("Momenta",
    "Momenta\\n自动驾驶 (2016)\\nRL世界模型量产首发",
    "company_overseas", "sim",
    "2016 年由曹旭东创立。2026 年 4 月宣布 R7 强化学习世界模型量产首发。"
    "技术路线：世界模型生成仿真数据→RL 训练策略→迁移真实车辆。"
    "中国自动驾驶领域世界模型+RL 路线的最激进实践者之一。"
)

# 补全 Jiaya_Jia 节点（贾佳亚，赵恒爽导师）
if "Jiaya_Jia" not in existing_ids:
    add_node("Jiaya_Jia",
        "贾佳亚 Jiaya Jia\\nCUHK 教授\\n思谋科技创始人",
        "person_overseas", "spatial",
        "香港中文大学计算机科学与工程系教授，思谋科技（SmartMore）创始人。"
        "赵恒爽的博士导师。在计算机视觉、图像处理方向有重要贡献。"
        "培养多位CV领军人物，CUHK MMLab/VisGraph 生态的重要人物。"
    )
add_edge("Jiaya_Jia", "Zhao_Hengshuang", "mentorship", "博士导师 (CUHK)", "tier1")
add_edge("Jiaya_Jia", "Tang_Xiaoou", "lab", "CUHK 同事 / MMLab 生态", "tier2")

# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 26
data["meta"]["updated"] = "2026-05-26"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v26: 三大流派综合补充——JEPA(V-JEPA2/金鑫)+空间智能(刘烨斌/高林/张兆翔/赵恒爽/蒋理/陈颖聪/Jiaya_Jia+HERMES/InSpatio-World/Kairos3)+生成仿真(陈建宇/赵行/高继扬/卢宗青/曹旭东/熊蓉/魏云超+星动纪元/BeingBeyond/Momenta+Genie3/DreamerV4/Being-0/Ctrl-World/VideoWorld/HappyOyster/X-World/Drive-OccWorld/WordGrow)")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v22 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
for n in new_nodes_added:
    print(f"    - {n}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
