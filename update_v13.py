#!/usr/bin/env python3
"""v13 增量更新：10位世界模型相关学者——陈宝权/李弘扬/徐丹飞/朱森华/俞扬/汪军/张伟楠/杨耀东/朱军/曹越"""
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
    data["edges"].append({
        "source": source, "target": target, "type": etype,
        "label": label, "strength": strength
    })
    new_edges_added.append(f"{source} → {target}")

# ═══════════════════════════════════════════════════════════════
print("\n=== 1. 陈宝权 — 北大 ACM/IEEE Fellow / 图形学→空间智能 ===")
add_node("Chen_Baoquan",
    "陈宝权 Chen Baoquan",
    "person_overseas", "spatial",
    "北大博雅特聘教授、智能学院副院长，ACM/IEEE Fellow。首位入选ACM SIGGRAPH Academy（图形学名人堂）的华人学者。研究方向：计算机图形学→3D视觉→空间智能。提出通过图形学构建数字孪生世界作为世界模型核心，让机器智能体在虚拟环境中训练试错。China3DV（中国三维视觉大会）发起人，SLAM3R等工作推动实时3D重建。",
    bold=True
)

# ═══════════════════════════════════════════════════════════════
print("\n=== 2. 李弘扬 — HKU / 上海AI Lab OpenDriveLab / 驾驶世界模型 ===")
add_node("Li_Hongyang",
    "李弘扬 Li Hongyang",
    "person_overseas", "sim",
    "HKU助理教授，上海AI Lab OpenDriveLab负责人。2019年CUHK博士（导师？）。IEEE Senior Member。研究方向：端到端自动驾驶→驾驶世界模型。代表工作：BEVFormer（鸟瞰图感知框架，2022年Top 100 AI Papers）、UniAD（CVPR 2023最佳论文，首个规划导向端到端自动驾驶框架）、Vista（NeurIPS 2024，高质量可控驾驶世界模型）、GenAD/ReSim。"
)

add_node("BEVFormer_UniAD",
    "BEVFormer + UniAD (2022-23)\\n端到端自动驾驶感知-规划框架",
    "milestone", "sim",
    "李弘扬团队的代表性工作组合。BEVFormer：利用时空Transformer从多摄像头输入学习鸟瞰图表示，2022年Top 100 AI Papers（NVIDIA CEO黄仁勋公开认可）。UniAD：首个规划导向的端到端自动驾驶统一框架，获CVPR 2023最佳论文奖，对特斯拉FSD V12产生重大影响。两者共同奠定了从感知到规划的端到端自动驾驶范式。"
)

# ═══════════════════════════════════════════════════════════════
print("\n=== 3. 徐丹飞 — Georgia Tech / 李飞飞学生 / 机器人世界模型 ===")
add_node("Xu_Danfei",
    "徐丹飞 Danfei Xu",
    "person_overseas", "sim",
    "2021年Stanford博士，师从李飞飞与Silvio Savarese。Georgia Tech助理教授，NVIDIA AI Research研究科学家。NSF CAREER Award获得者。研究方向：结构化世界模型用于长程规划、机器人操作技能学习。「人类数据是伪装成另一种形式的机器人数据」理念推动者，EgoMimic/EgoScale等从人类视频学习机器人先验。"
)

# ═══════════════════════════════════════════════════════════════
print("\n=== 4. 朱森华 — 具脑磐石 / 前华为具身大脑一号位 / 类脑世界模型 ===")
add_node("Zhu_Senhua",
    "朱森华 Zhu Senhua",
    "person_overseas", "active_inf",
    "宾夕法尼亚大学认知神经科学博士，中科院脑与认知科学国家重点实验室博后。前华为云AI算法创新Lab主任（华为具身大脑一号位）。2025年创立具脑磐石，对标Yann LeCun的JEPA路线，提出「认知世界模型五层级」体系：视觉真实→物理真实→交互真实→抽象学习(JEPA)→主动推理。核心理念：回归智能本源，向人类大脑学习。"
)

add_node("BrainStone",
    "具脑磐石 BrainStone\\n类脑认知世界模型 (2025)\\n亿元级融资",
    "company_overseas", "active_inf",
    "2025年由朱森华创立。对标Yann LeCun的JEPA联合嵌入预测架构路线。主张在抽象表征空间中学习世界演化规律（非逐像素预测），提出认知世界模型五层级体系。强调低数据、高泛化、终身学习、低功耗的类脑认知路径，反对堆数据/算力的纯经验主义路线。获四川科创投、乐聚机器人等亿元级投资。"
)

# ═══════════════════════════════════════════════════════════════
print("\n=== 5. 俞扬 — 南大 / 因果世界模型 / LAMDA ===")
add_node("Yu_Yang",
    "俞扬 Yu Yang",
    "person_overseas", "sim",
    "南大人工智能学院教授、博导，LAMDA课题组核心成员。2011年南大博士。入选IEEE Intelligent Systems「AI's 10 to Watch」(2018)，获CCF-IEEE青年科学家奖。研究方向：强化学习→因果世界模型。核心观点：世界模型的核心价值是反事实推理——对未见过的决策推断其结果；纯视频生成不准确学到物理规律，难以作为真正世界模型。"
)

# ═══════════════════════════════════════════════════════════════
print("\n=== 6. 汪军 — UCL / 多智能体RL / OpenR ===")
add_node("Wang_Jun",
    "汪军 Wang Jun",
    "person_overseas", "sim",
    "UCL计算机系正教授、阿兰·图灵研究所Turing Fellow。上海数字大脑研究院联合创始人/院长，前华为诺亚实验室决策推理首席科学家。研究方向：多智能体深度强化学习、生成模型、决策大模型。代表作：BiCNet（多智能体协调网络）、PR2（概率递归推理）、OpenR（首个类o1开源RL全链条训练框架）。培养出张伟楠/杨耀东等学生。",
    bold=True
)

# ═══════════════════════════════════════════════════════════════
print("\n=== 7. 张伟楠 — 上海交大 / 强化学习→决策大模型 ===")
add_node("Zhang_Weinan",
    "张伟楠 Zhang Weinan",
    "person_overseas", "sim",
    "上海交大计算机系教授、博导、副系主任。2011年上海交大ACM班学士，2016年UCL博士（师从汪军）。2018年阿里达摩院青橙奖，2021年吴文俊AI优秀青年奖。谷歌学术引用3万+。研究方向：强化学习(模型驱动/数据驱动)→决策大模型。著有《动手学强化学习》《动手学机器学习》。"
)

# ═══════════════════════════════════════════════════════════════
print("\n=== 8. 杨耀东 — 北大 / 多智能体RL / AI安全对齐 ===")
add_node("Yang_Yaodong",
    "杨耀东 Yang Yaodong",
    "person_overseas", "sim",
    "北大人工智能研究院助理教授（博雅青年学者），AI安全与治理中心执行主任。中科大本科，UCL博士（师从汪军，提名ACM SIGAI优秀博士论文）。MIT TR「AI 100青年先锋」。研究方向：多智能体强化学习、大模型安全对齐、具身世界模型。团队开源MARLlib/HARL/Omnisafe等RL框架。发表200+论文，引用1.6万+。"
)

# ═══════════════════════════════════════════════════════════════
print("\n=== 9. 朱军 — 清华 / IEEE Fellow / 贝叶斯ML→视频世界模型 ===")
add_node("Zhu_Jun",
    "朱军 Zhu Jun",
    "person_overseas", "sim",
    "清华计算机系Bosch AI教授、IEEE Fellow，人工智能研究院副院长。2009年清华博士。获求是杰出青年奖、科学探索奖。研究方向：正则化贝叶斯理论→扩散模型高效算法→视频世界模型。DPM-Solver获ICLR 2022杰出论文奖（被DALL·E 2/Stable Diffusion采用），U-ViT为首个Diffusion+Transformer融合架构（早于Sora的DiT）。生数科技首席科学家，发布国产视频大模型Vidu（16s/1080P，对标Sora）。",
    bold=True
)

add_node("Shengshu",
    "生数科技 Shengshu\\n国产视频大模型Vidu (2023)\\n朱军担任首席科学家",
    "company_overseas", "sim",
    "朱军作为首席科学家参与孵化的AI创业公司。2024年4月发布中国首个长时长（16s）、高一致性（1080P）视频大模型Vidu，采用自研U-ViT架构（全球首个Diffusion+Transformer融合架构，早于Sora的DiT），能模拟真实物理世界。代表清华体系在视频世界模型方向的突破。"
)

add_node("Vidu",
    "Vidu (2024)\\n国产16s/1080P视频大模型",
    "milestone", "sim",
    "生数科技2024年4月发布的国产视频大模型，对标OpenAI Sora。采用朱军团队自研U-ViT架构端到端生成，支持一键生成16秒1080P高清视频，具备多镜头生成、时空一致性高等特点。基于DPM-Solver高效扩散模型采样技术（ICLR 2022杰出论文）。代表国产视频世界模型的自研突破。"
)

# ═══════════════════════════════════════════════════════════════
print("\n=== 10. 曹越 — Sand.AI / Swin Transformer / 自回归视频世界模型 ===")
add_node("Cao_Yue",
    "曹越 Cao Yue",
    "person_overseas", "sim",
    "清华软件学院博士，2018年清华特等奖学金获得者。Swin Transformer第一作者（ICCV 2021最佳论文马尔奖，引用近6万次）。前北京智源研究院视觉模型研究中心负责人、光年之外联合创始人。2024年1月创立Sand.AI，押注自回归路线构建视频世界模型——认为自回归是更接近终局的方案，时序因果建模+可扩展。"
)

add_node("Sand_AI",
    "Sand.AI (2024)\\n自回归视频生成→世界模型\\n累计融资~$60M",
    "company_overseas", "sim",
    "2024年1月由曹越创立。核心技术路线：自回归(Autoregressive)+扩散模型结合构建视频世界模型。代表产品：MAGI-1（全球首个自回归视频生成大模型，100%开源，Physics-IQ 56%远超Sora/可灵）、Gaga-1（人物表演视频生成）。24B+4.5B双版本，Apache 2.0开源。被李开复评为「继DeepSeek之后又一家开发出世界一流开源模型的AI公司」。"
)

add_node("MAGI_1",
    "MAGI-1 (2025)\\n全球首个自回归视频生成大模型",
    "milestone", "sim",
    "Sand.AI于2025年4月发布。全球首个自回归视频生成大模型，Diffusion Transformer + Flow-Matching，24帧/块分块自回归支持无限长度扩展。Physics-IQ基准56.02%（远超Sora/可灵等扩散方案），VBench-I2V总分89.28排名第一。100% Apache 2.0开源。核心思路：视频存在天然时间因果性，自回归能更好建模物理一致性（Sora等纯扩散方案容易左腿右腿同出）。"
)

# ═══════════════════════════════════════════════════════════════
# 新增边
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增关系边 ===")

# ── 学术谱系：导师→学生 ──
add_edge("Wang_Jun", "Zhang_Weinan", "mentorship", "博士导师 (UCL 2016)", "tier1")
add_edge("Wang_Jun", "Yang_Yaodong", "mentorship", "博士导师 (UCL, ACM SIGAI优博提名)", "tier1")
add_edge("Zhang_Weinan", "Yang_Yaodong", "lab", "同门师兄弟 (UCL 汪军组)", "tier2")
add_edge("FeiFei_Li", "Xu_Danfei", "mentorship", "博士导师 (Stanford 2021)", "tier1")
add_edge("Xu_Danfei", "Su_Hao", "lab", "同门 (Stanford 李飞飞组)", "tier2")
add_edge("Xu_Danfei", "Andrej_Karpathy", "lab", "同门 (Stanford 李飞飞组)", "tier2")

# ── 公司创建 ──
add_edge("Zhu_Senhua", "BrainStone", "founded", "创始人 & CEO (2025)", "tier1")
add_edge("Zhu_Jun", "Shengshu", "founded", "首席科学家 (2023)", "tier1")
add_edge("Shengshu", "Vidu", "maintainer", "核心产品 (2024)", "tier1")
add_edge("Cao_Yue", "Sand_AI", "founded", "创始人 & CEO (2024)", "tier1")
add_edge("Sand_AI", "MAGI_1", "maintainer", "核心产品 (2025)", "tier1")

# ── 陈宝权 ──
add_edge("Chen_Baoquan", "Spatial_Intel", "maintainer", "图形学→数字孪生→世界模型 / China3DV发起人", "tier1")
add_edge("Chen_Baoquan", "Jingyi_Yu", "lab", "同为3D视觉/空间智能学术领袖", "tier2")

# ── 李弘扬 ──
add_edge("Li_Hongyang", "BEVFormer_UniAD", "maintainer", "核心作者 (2022-23)", "tier1")
add_edge("BEVFormer_UniAD", "Model_Based_RL", "evolution", "端到端驾驶→世界模型Vista/ReSim", "tier2")

# ── 俞扬 ──
add_edge("Yu_Yang", "Model_Based_RL", "maintainer", "因果世界模型 / 反事实推理", "tier2")

# ── 朱森华 ──
add_edge("BrainStone", "Yann_LeCun", "related", "对标JEPA路线 / 抽象表征空间预测", "tier2")
add_edge("Zhu_Senhua", "Active_Inference", "maintainer", "认知世界模型第五层→主动推理", "tier2")

# ── 朱军 ──
add_edge("Vidu", "Gen_Video_concept", "evolution", "国产Sora级视频世界模型 (U-ViT)", "tier2")
add_edge("Zhu_Jun", "Spatial_Intel", "related", "扩散模型→3D生成(ProlificDreamer)", "tier2")

# ── 曹越 ──
add_edge("MAGI_1", "Gen_Video_concept", "evolution", "自回归视频世界模型（Physics-IQ 56%）", "tier2")
add_edge("Cao_Yue", "Gen_Video_concept", "maintainer", "自回归路线: 时序因果建模→视频世界模型", "tier2")

# ── 汪军 ──
add_edge("Wang_Jun", "Model_Based_RL", "maintainer", "多智能体RL / OpenR推理框架", "tier2")

# ── 张伟楠 ──
add_edge("Zhang_Weinan", "Model_Based_RL", "maintainer", "基于模型的RL / 决策大模型 / Decision Transformer", "tier2")

# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 15
data["meta"]["updated"] = "2026-05-25"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v15: 新增10位世界模型学者——陈宝权(空间智能)/李弘扬(驾驶WM)/徐丹飞(机器人WM)/朱森华(类脑JEPA)/俞扬(因果WM)/汪军(多智能体RL)/张伟楠(决策大模型)/杨耀东(AI安全)/朱军(Vidu)/曹越(MAGI-1)，打通UCL汪军→张伟楠/杨耀东师承链")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v13 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
