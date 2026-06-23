#!/usr/bin/env python3
"""v16 增量更新：五家公司深度信息——极佳视界(GigaWorld-Policy/GigaBrain/Maker)/流形空间(Worldscape)/Sand.AI(ARR更新)/逆矩阵科技/ Liber AI"""
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
# 0. 更新已有节点
# ═══════════════════════════════════════════════════════════════
print("\n=== 更新已有节点 ===")

for node in data["nodes"]:
    # ── 极佳视界 ──
    if node["id"] == "GigaVision":
        node["description"] = (
            "2023年6月由黄冠创立。国内最早系统布局世界模型的公司之一，"
            "'平台+大脑+本体'三条腿走路：世界模型平台GigaWorld、通用具身大脑GigaBrain、自研机器人本体Maker。"
            "GigaWorld-Policy将具身策略与世界模型深度融合设计。Maker H01已在汽车制造、3C电子、仓储物流、家庭服务等场景商业化落地，"
            "2026年冲刺千台交付量。与一汽模具、阿里云完成具身智能在真实工业制造场景的全流程方案落地。"
            "计划年内视觉-动作数据达100万小时以上，世界模型预训练数据超1000万小时。"
            "2026年一个多月内完成25亿元融资，估值突破百亿，是国内首个世界模型百亿独角兽。"
            "华为哈勃首次投资世界模型公司。"
        )
        print("  ✅ 更新 GigaVision description")

    elif node["id"] == "Huang_Guan":
        node["description"] = (
            "清华自动化系博士，微软亚洲研究院深度学习研究（国内最早一批深度学习研究者）。"
            "先后任职地平线、鉴智机器人，三星中国研究院。"
            "同时具备顶尖科研、量产工程、商业落地和连续创业经验。"
            "2023年6月创立极佳科技。90后。"
        )
        print("  ✅ 更新 Huang_Guan description")

    # ── 流形空间 ──
    elif node["id"] == "Manifold_AI":
        node["description"] = (
            "2025年5月由武伟（前商汤绝影）联合清华教授创立。"
            "定位'国内第一家自研世界模型作为具身基础模型落地到机器人的创业公司'。"
            "自研Worldscape世界模型：全球首个同时支持移动和操作交互的实时世界模型，作为机器人预训练基座。"
            "Worldscape Policy实现具身世界-动作模型：时空状态预测+视觉空间内生推理+动作执行，"
            "精度全面超越现有VLA模型，具备少样本和零样本执行能力。"
            "坚持硬件-数据-模型闭环迭代，自研遥操、UMI、ego-centric到采测一体等多种数据采集设备。"
            "成立不到十个月累计完成四轮近5亿元融资，华为哈勃/君联资本/同创伟业等投资。"
        )
        print("  ✅ 更新 Manifold_AI description")

    # ── Sand.AI ──
    elif node["id"] == "Sand_AI":
        node["description"] = (
            "2024年1月由曹越创立。核心技术路线：自回归(Autoregressive)构建视频世界模型，与U-ViT/DiT等Diffusion路线完全不同。"
            "代表产品：MAGI-1（全球首个自回归视频生成大模型，100%开源，Physics-IQ 56%远超Sora/可灵）。"
            "自回归路线更接近语言模型'预测下一个token'逻辑，但用于视觉时空序列预测——本质上即世界模型构建方式。"
            "ARR超千万美元，近期完成约$50M新融资。"
            "被李开复评为「继DeepSeek之后又一家开发出世界一流开源模型的AI公司」。"
        )
        print("  ✅ 更新 Sand_AI description")

    # ── 朱军（新增学生刘松铭） ──
    elif node["id"] == "Zhu_Jun":
        node["description"] = (
            "清华计算机系Bosch AI教授、IEEE Fellow，人工智能研究院副院长。2009年清华博士。"
            "获求是杰出青年奖、科学探索奖。研究方向：正则化贝叶斯理论→扩散模型高效算法→视频世界模型。"
            "DPM-Solver获ICLR 2022杰出论文奖（被DALL·E 2/Stable Diffusion采用），"
            "U-ViT为首个Diffusion+Transformer融合架构（早于Sora的DiT）。"
            "生数科技首席科学家，发布国产视频大模型Vidu。培养出刘松铭（Liber AI创始人）等学生。"
        )
        print("  ✅ 更新 Zhu_Jun description")

# ═══════════════════════════════════════════════════════════════
# 1. 极佳视界新产品节点
# ═══════════════════════════════════════════════════════════════
print("\n=== 极佳视界新产品 ===")

add_node("GigaWorld_Policy",
    "GigaWorld-Policy (2026)\\n具身策略+世界模型深度融合",
    "milestone", "sim",
    "极佳视界的核心产品。将具身策略和世界模型深度融合——不是先建世界模型再往机器人上套，"
    "而是从一开始就绑在一起设计。世界模型负责时空状态预测，策略网络直接利用世界模型的隐空间表征做决策。"
    "代表了世界模型从'感知'到'行动'的范式跨越。"
)

add_node("GigaBrain",
    "GigaBrain (2026)\\n通用具身大脑",
    "milestone", "sim",
    "极佳视界的通用具身大脑模型。利用GigaWorld世界模型生成的合成数据训练，"
    "实现真机泛化。国内首个利用世界模型数据实现真机泛化的VLA模型。"
)

add_node("Maker_H01",
    "Maker H01 (2026)\\n通用机器人本体\\n千台交付目标",
    "milestone", "sim",
    "极佳视界自研通用机器人本体。已在汽车制造、3C电子、仓储物流、家庭服务等场景实现商业化落地。"
    "2026年4月与一汽模具、阿里云完成具身智能机器人在真实工业制造场景的全流程方案落地。"
    "年内冲刺千台交付量。"
)

# ── 边 ──
add_edge("GigaVision", "GigaWorld_Policy", "maintainer", "核心产品 (2026)", "tier1")
add_edge("GigaVision", "GigaBrain", "maintainer", "核心产品 (2026)", "tier1")
add_edge("GigaVision", "Maker_H01", "maintainer", "自研机器人本体", "tier1")
add_edge("GigaWorld", "GigaWorld_Policy", "evolution", "世界模型平台→策略融合", "tier1")
add_edge("GigaWorld", "GigaBrain", "evolution", "世界模型→具身大脑", "tier1")

# ═══════════════════════════════════════════════════════════════
# 2. 流形空间新产品节点
# ═══════════════════════════════════════════════════════════════
print("\n=== 流形空间新产品 ===")

add_node("Worldscape",
    "Worldscape (2025)\\n首个移动+操作交互实时世界模型",
    "milestone", "sim",
    "Manifold AI自研。世界范围内首个同时支持移动和操作交互的实时世界模型。"
    "作为机器人预训练基座，通过世界模型做时空状态预测，结合视觉输入进行空间内生推理并执行动作。"
    "精度全面超越现有VLA模型，具备少样本和零样本执行能力。"
)

add_node("Worldscape_Policy",
    "Worldscape Policy (2026)\\n具身世界-动作模型\\n精度超越VLA",
    "milestone", "sim",
    "基于Worldscape世界模型的具身策略。时空状态预测+视觉空间内生推理+动作执行三位一体。"
    "利用世界模型预训练基座实现少样本/零样本任务执行。"
    "实证精度全面超越现有VLA（视觉-语言-动作）模型。"
)

# ── 边 ──
add_edge("Manifold_AI", "Worldscape", "maintainer", "自研核心基座", "tier1")
add_edge("Manifold_AI", "Worldscape_Policy", "maintainer", "具身策略产品", "tier1")
add_edge("Worldscape", "Worldscape_Policy", "evolution", "世界模型基座→具身策略", "tier1")

# ═══════════════════════════════════════════════════════════════
# 3. 逆矩阵科技 (Inverse Matrix) — 全新公司
# ═══════════════════════════════════════════════════════════════
print("\n=== 逆矩阵科技 Inverse Matrix ===")

add_node("Ji_Jiaming",
    "吉嘉铭 Ji Jiaming",
    "person_overseas", "sim",
    "1998年出生，北大人工智能研究院博士生，2025年北大学生年度人物。"
    "极少数同时获Apple Scholar（当年大陆仅2位）、腾讯、蚂蚁认可的学者，谷歌学术引用5600+。"
    "逆矩阵科技创始人兼CEO。聚焦世界基础模型与强化学习的融合研究。",
    bold=True
)

add_node("Chen_Boyuan",
    "陈博远 Chen Boyuan",
    "person_overseas", "sim",
    "2004年出生，北大元培学院大四本科生，2025年北大学生年度人物。"
    "大一发表顶会论文，大四独立发表NeurIPS 2025亮点论文，代表论文获NeurIPS Oral（接受率仅0.35%）。"
    "谷歌学术引用2000+。逆矩阵科技联合创始人。"
)

add_node("Inverse_Matrix",
    "逆矩阵科技 Inverse Matrix\\nRL+因果推理世界模型 (2026)\\n种子轮 >$10M (高瓴/燕缘)",
    "company_overseas", "sim",
    "定位'通用世界基座模型'，目标是构建能真正'理解'而非'模仿'物理规律的AI系统。"
    "技术路径被业界视为继李飞飞（空间智能）和杨立昆（JEPA）之后的'第三条路'："
    "强化学习+世界模型融合，强调因果推理能力。"
    "核心目标：能响应动作指令并做出物理正确预测，在任意物理场景中进行因果推理与反事实预测。"
    "计划2026年内发布旗舰模型。成立仅40余天获高瓴创投、燕缘创投等超千万美元融资。"
    "团队超30人，来自北大和头部大厂。"
)

# ── 边 ──
add_edge("Ji_Jiaming", "Inverse_Matrix", "founded", "创始人 & CEO (2026)", "tier1")
add_edge("Chen_Boyuan", "Inverse_Matrix", "founded", "联合创始人 (2026)", "tier1")
add_edge("Ji_Jiaming", "Chen_Boyuan", "lab", "联合创始人 / 北大同门", "tier1")
add_edge("Inverse_Matrix", "Model_Based_RL", "maintainer", "RL+世界模型融合→因果推理", "tier2")
add_edge("Inverse_Matrix", "Active_Inference", "related", "因果推理→主动推理理论关联", "tier2")

# ═══════════════════════════════════════════════════════════════
# 4. Liber AI — 全新公司
# ═══════════════════════════════════════════════════════════════
print("\n=== Liber AI ===")

add_node("Liu_Songming",
    "刘松铭 Liu Songming",
    "person_overseas", "sim",
    "清华大学00后本科生特等奖学金得主（每年仅10人），师从朱军教授。"
    "RDT系列一作，多篇ICML、NeurIPS顶会论文。"
    "2024年由AI for Physics转向具身智能，主导RDT系列研发。"
    "2025年12月创立Liber AI，任CEO。"
    "愿景：'像苹果一样，去定义世界模型的数采范式、本体及系统'。",
    bold=True
)

add_node("Lin_Fanqi",
    "林凡淇 Lin Fanqi",
    "person_overseas", "sim",
    "清华大学，师从高阳老师。一作论文《Data Scaling Laws》提出模型泛化性随数据多样性增加而显著提升的规律，"
    "获ICLR Oral、CoRL X-Embodiment Workshop Best Paper。Liber AI联合创始人。"
)

add_node("Gao_Yang",
    "高阳 Gao Yang",
    "person_overseas", "sim",
    "清华大学教师。研究方向：具身智能、机器人学习。林凡淇的导师。"
    "Data Scaling Laws在具身智能领域有重要影响。"
)

add_node("Liber_AI",
    "Liber AI (2025)\\nUMI数据+世界模型融合\\n累计融资数亿元",
    "company_overseas", "sim",
    "2025年12月由刘松铭（清华特奖/朱军学生）创立。"
    "聚焦具身智能模型研发，瞄准人类UMI数据与世界模型融合的下一代技术范式。"
    "已跑通UMI硬件→数据采集→大模型训练全流程闭环。"
    "核心产品：具身智能大模型及配套UMI硬件、数据采集与训练体系。"
    "两大创新：模态对齐（让海量视频数据反哺稀缺物理数据）+ 归纳偏置（把物理规律注入模型加速收敛）。"
    "成立4个月发布首个Demo：五指灵巧手实现双手剥香蕉、拧瓶盖、持锅颠勺等精细操作长程任务。"
    "三个月内连续完成种子轮/天使轮/天使+轮，累计数亿元，真格/红杉中国/美团龙珠/顺为等投资，估值翻5倍。"
)

add_node("RDT_1B",
    "RDT-1B (2024)\\n全球首个大规模预训练+扩散Transformer\\n具身基座模型",
    "milestone", "sim",
    "刘松铭主导研发。全球首个使用大规模预训练+扩散Transformer范式的具身基座模型，"
    "领先硅谷竞品PI-0模型一个月发布。奠定了大规模预训练在具身智能中的技术路线。"
)

add_node("RDT_2",
    "RDT-2 (2025)\\n首个大规模UMI无本体人类数据\\n预训练具身模型",
    "milestone", "sim",
    "刘松铭团队发布。首个使用大规模UMI无本体人类数据预训练范式的具身模型，"
    "领先Generalist的GEN-0模型一个月。无需本体数据即可从人类操作视频中学习操作技能，"
    "代表了世界模型+人类数据融合的技术方向。"
)

# ── 边 ──
add_edge("Liu_Songming", "Liber_AI", "founded", "创始人 & CEO (2025)", "tier1")
add_edge("Lin_Fanqi", "Liber_AI", "founded", "联合创始人 (2025)", "tier1")
add_edge("Liu_Songming", "Lin_Fanqi", "lab", "联合创始人 / 清华同门", "tier1")
add_edge("Zhu_Jun", "Liu_Songming", "mentorship", "本科导师 (清华)", "tier1")
add_edge("Gao_Yang", "Lin_Fanqi", "mentorship", "导师 (清华)", "tier1")
add_edge("Liber_AI", "RDT_1B", "maintainer", "核心产品 (2024)", "tier1")
add_edge("Liber_AI", "RDT_2", "maintainer", "核心产品 (2025)", "tier1")
add_edge("RDT_1B", "RDT_2", "evolution", "大规模预训练→UMI人类数据范式", "tier1")

# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 18
data["meta"]["updated"] = "2026-05-26"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v18: 五家公司深度更新——极佳视界(+GigaWorld-Policy/GigaBrain/Maker H01)/流形空间(+Worldscape/Worldscape Policy)/Sand.AI(ARR+融资更新)/逆矩阵科技(吉嘉铭+陈博远,RL+因果推理)/Liber AI(刘松铭+林凡淇+RDT-1B/RDT-2,朱军/高阳师承)")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v16 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
for n in new_nodes_added:
    print(f"    - {n}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
