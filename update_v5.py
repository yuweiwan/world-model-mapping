#!/usr/bin/env python3
"""v5 增量更新：从用户提供的详细文本中提取新节点，合并到母数据"""
import json, os, subprocess

SRC = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SRC, "World_Models_data.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

existing_ids = {n["id"] for n in data["nodes"]}
existing_names = {n["label"].split("\\n")[0].strip().lower() for n in data["nodes"]}
existing_labels = {n["label"] for n in data["nodes"]}

def exists(name_or_id):
    """检查是否与已有节点重复"""
    nid = name_or_id.replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "").replace("'", "").replace("’", "").replace("?", "").replace("!", "").replace(":", "").replace("。", "").replace("，", "")
    if nid in existing_ids:
        return True, nid
    # 检查名字相似度
    clean = name_or_id.lower().strip()
    for en in existing_names:
        if clean == en or clean in en or en in clean:
            return True, None
    return False, nid

# 统计
new_nodes_added = []
new_edges_added = []

def add_node(nid, label, ntype, group, description, bold=False):
    """添加节点，如果已存在则跳过"""
    global new_nodes_added
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
    """添加边"""
    global new_edges_added
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
# 路线一：JEPA 新增节点
# ═══════════════════════════════════════════════════════════════
print("\n=== 路线一：JEPA 联合嵌入预测架构 ===")

# --- 人物 ---
add_node("Alexandre_LeBrun", "Alexandre LeBrun\\nAMI Labs CEO", "person_overseas", "jepa",
    "AMI Labs 联合创始人兼CEO。曾任 Nabla 联合创始人及CEO。负责AMI Labs的商业运营和战略方向。")

add_node("Saining_Xie", "谢赛宁 Saining Xie\\nAMI Labs / NYU", "person_overseas", "jepa",
    "NYU助理教授，原Meta FAIR研究科学家。ConvNeXt、ResNeXt等核心架构作者。2026年初宣布加入AMI Labs，是LeCun团队核心成员。")

add_node("Mahmoud_Assran", "Mahmoud Assran\\nMeta FAIR / I-JEPA一作", "person_overseas", "jepa",
    "I-JEPA、V-JEPA及V-JEPA 2核心一作/共同作者。JEPA路线的主要实证支柱，推动了自监督联合嵌入预测架构从图像到视频的扩展。")

add_node("Adrien_Bardes", "Adrien Bardes\\nMeta FAIR / V-JEPA核心架构师", "person_overseas", "jepa",
    "V-JEPA及V-JEPA 2的核心架构设计者。与Assran长期合作推进自监督视频JEPA。专注于视觉自监督学习的架构创新。")

add_node("Nicolas_Ballas", "Nicolas Ballas\\nMeta FAIR / Mila校友", "person_overseas", "jepa",
    "V-JEPA系列关键作者，Mila校友。在V-JEPA 2及V-JEPA 2.1中均为核心共同作者，贡献于视频表征学习。")

add_node("Quentin_Garrido", "Quentin Garrido\\nMeta FAIR", "person_overseas", "jepa",
    "V-JEPA 2共同作者。研究聚焦自监督视觉表征学习。")

add_node("David_Fan", "David Fan\\nMeta FAIR", "person_overseas", "jepa",
    "V-JEPA 2共同作者。Meta FAIR研究员。")

add_node("Russell_Howes", "Russell Howes\\nMeta FAIR", "person_overseas", "jepa",
    "V-JEPA 2共同作者。Meta FAIR研究员。")

add_node("Mojtaba_Komeili", "Mojtaba Komeili\\nMeta FAIR", "person_overseas", "jepa",
    "V-JEPA 2共同作者。Meta FAIR研究员。")

add_node("Emmanuel_Dupoux", "Emmanuel Dupoux\\nMeta FAIR / EHESS / INRIA", "person_overseas", "jepa",
    "认知科学家，语音与认知科学路径。参与多个自监督学习项目，其认知建模传统为JEPA的设计理念提供了方法论背景。")

add_node("Jean_Ponce", "Jean Ponce\\nENS / NYU / INRIA", "person_overseas", "jepa",
    "ENS教授，前FAIR研究总监。LeCun长期学术合作者。2026年与LeCun合著Value-Guided Action Planning with JEPA，探索JEPA在行动规划中的应用。")

add_node("Matthieu_Destrade", "Matthieu Destrade\\nJEPA行动规划合作者", "person_overseas", "jepa",
    "2026年与LeCun、Ponce合著Value-guided action planning with JEPA world models。")

add_node("Oumayma_Bounou", "Oumayma Bounou\\nJEPA行动规划合作者", "person_overseas", "jepa",
    "2026年与LeCun、Ponce合著Value-guided action planning with JEPA world models。")

add_node("Quentin_Le_Lidec", "Quentin Le Lidec\\nJEPA行动规划合作者", "person_overseas", "jepa",
    "2026年与LeCun、Ponce合著Value-guided action planning with JEPA world models。")

add_node("Bo_Wang", "Bo Wang\\nUHN首席AI科学家", "person_overseas", "jepa",
    "UHN首席AI科学家。2026年2月与Alif Munim团队将JEPA首次应用于医学超声视频，被LeCun公开关注并背书。")

add_node("Alif_Munim", "Alif Munim\\n医学超声JEPA", "person_overseas", "jepa",
    "与Bo Wang合作将JEPA首次引入医疗影像领域（2026.02），被LeCun公开认可。")

add_node("Kyunghyun_Cho", "Kyunghyun Cho\\nNYU / 神经机器翻译先驱", "person_overseas", "jepa",
    "NYU教授，神经机器翻译先驱（Seq2Seq注意力机制发明者）。LeCun在NYU的同事，合著JEPA慢特征分析论文。")

add_node("Vlad_Sobal", "Vlad Sobal\\nMeta FAIR", "person_overseas", "jepa",
    "围绕JEPA架构与特征学习展开系统性实证研究的关键合作者。")

add_node("V_JyothirS", "V JyothirS\\nMeta FAIR", "person_overseas", "jepa",
    "围绕JEPA架构与特征学习展开系统性实证研究的关键合作者。")

add_node("Siddhartha_Jalagam", "Siddhartha Jalagam\\nMeta FAIR", "person_overseas", "jepa",
    "围绕JEPA架构与特征学习展开系统性实证研究的关键合作者。")

add_node("Nicolas_Carion", "Nicolas Carion\\nMeta FAIR / DETR作者", "person_overseas", "jepa",
    "围绕JEPA架构与特征学习展开合作的Meta FAIR研究员，DETR目标检测架构作者之一。")

add_node("Lorenzo_Mur_Labadia", "Lorenzo Mur-Labadia\\nV-JEPA 2.1贡献者", "person_overseas", "jepa",
    "V-JEPA 2.1版本核心贡献者。")

add_node("Matthew_Muckley", "Matthew Muckley\\nV-JEPA 2.1贡献者", "person_overseas", "jepa",
    "V-JEPA 2.1版本核心贡献者。")

add_node("Amir_Bar", "Amir Bar\\nV-JEPA 2.1贡献者", "person_overseas", "jepa",
    "V-JEPA 2.1版本核心贡献者。")

add_node("Koustuv_Sinha", "Koustuv Sinha\\nV-JEPA 2.1贡献者 / Meta FAIR", "person_overseas", "jepa",
    "V-JEPA 2.1版本核心贡献者，Meta FAIR研究员。")

add_node("Aaron_van_den_Oord", "Aäron van den Oord\\nVQ-VAE / CPC 作者", "person_overseas", "jepa",
    "自监督学习先驱。VQ-VAE和CPC（对比预测编码）作者，其研究为JEPA提供了关键的方法论基础。")

add_node("Ishan_Misra", "Ishan Misra\\nMeta FAIR / SimCLR等", "person_overseas", "jepa",
    "自监督学习先驱。SimCLR、DINO等多个里程碑工作核心作者，为JEPA提供了自监督表征学习的理论和实证基础。")

add_node("Alyosha_Efros", "Alyosha Efros\\nUC Berkeley", "person_overseas", "jepa",
    "UC Berkeley教授，计算机视觉与自监督学习先驱。其研究为JEPA提供了方法论基础。")

add_node("Michael_Rabbat", "Michael Rabbat\\nMeta FAIR", "person_overseas", "jepa",
    "Meta FAIR研究员。V-JEPA 2等论文合作作者，对视频自监督的理论分析做出贡献。")

# --- 里程碑 ---
add_node("V_JEPA", "V-JEPA (2024-2025)\\n视频联合嵌入预测架构", "milestone", "jepa",
    "Bardes等人提出。将I-JEPA扩展到视频域，提出基于EMA教师网络的自监督掩码预测方案。是JEPA从图像到视频的关键扩展。")

add_node("V_JEPA2_1", "V-JEPA 2.1 (2026.03)\\n密集视觉表征升级", "milestone", "jepa",
    "V-JEPA 2升级版。输出密集高质量视觉表征，同时保持全局场景理解能力。由Lorenzo Mur-Labadia、Matthew Muckley、Amir Bar、Koustuv Sinha等核心贡献。")

add_node("Rethinking_JEPA", "Rethinking JEPA (2025.09)\\n高效训练策略", "milestone", "jepa",
    "提出冻结教师网络的高效训练策略，系统性优化JEPA的性价比边界。")

add_node("Value_Guided_Planning_JEPA", "Value-Guided Action Planning (2026)\\nJEPA用于行动规划", "milestone", "jepa",
    "LeCun、Ponce、Destrade、Bounou、Le Lidec等人合著。将JEPA世界模型用于价值引导的行动规划。")

add_node("Medical_Ultrasound_JEPA", "医学超声JEPA (2026.02)\\nJEPA首度进入医疗影像", "milestone", "jepa",
    "Bo Wang与Alif Munim团队将JEPA首度引入医疗影像（超声视频分析），被LeCun公开关注。标志着JEPA从研究到医疗垂直领域的应用延伸。")

# --- 公司 ---
add_node("Nabla", "Nabla\\n医疗AI公司", "company_overseas", "jepa",
    "医疗AI公司，专注临床文档自动化。联合创始人兼CEO Alexandre LeBrun于2025年底转任AMI Labs CEO。")

# ═══════════════════════════════════════════════════════════════
# 路线二：空间智能 新增节点
# ═══════════════════════════════════════════════════════════════
print("\n=== 路线二：空间智能（3D 世界模型）===")

add_node("Pratul_Srinivasan", "Pratul Srinivasan\\nNeRF合著者 / Google Research", "person_overseas", "spatial",
    "前Google Research研究科学家，NeRF合著者。2022年与Mildenhall共享SIGGRAPH Significant New Researcher Award。神经渲染核心贡献者。")

add_node("Ravi_Ramamoorthi", "Ravi Ramamoorthi\\nUCSD / 计算机图形学先驱", "person_overseas", "spatial",
    "UCSD教授，计算机图形学先驱。Mildenhall和Srinivasan的博士导师，搭建了从计算机图形学到神经渲染的桥梁。")

add_node("Ruilong_Li", "Ruilong Li\\nNVIDIA Space Intelligence Lab", "person_overseas", "spatial",
    "NVIDIA Space Intelligence Lab研究员。gsplat、nerfacc和nerfstudio原初作者，推动3D Gaussian Splatting生态走向成熟。")

add_node("Zhaoshuo_Li", "Zhaoshuo Li (Max Li)\\nNVIDIA / Neuralangelo一作", "person_overseas", "spatial",
    "NVIDIA研究科学家，Neuralangelo第一作者。师从Johns Hopkins的Mathias Unberath。专注于高精度3D表面重建。")

add_node("Thomas_Muller", "Thomas Müller\\nNVIDIA / Instant NGP一作", "person_overseas", "spatial",
    "NVIDIA研究科学家，Instant NGP第一作者。多分辨率哈希编码技术使NeRF训练从数小时级降至秒级，是3D世界模型从学术走向商业的关键技术突破。")

add_node("Andreas_Geiger", "Andreas Geiger\\n图宾根大学 / 3D场景理解先驱", "person_overseas", "spatial",
    "图宾根大学教授，3D场景理解先驱。在可微渲染与三维重建的多个关键节点上有奠基性贡献。KITTI数据集创建者。")

add_node("Paul_Debevec", "Paul Debevec\\nNetflix / USC ICT / 光照渲染先驱", "person_overseas", "spatial",
    "Netflix研究科学家，USC ICT教授。基于图像的照明与渲染先驱，定义了真实世界光照捕获与逼真重光照的基础理论框架。")

add_node("Ashutosh_Saxena", "Ashutosh Saxena\\nMIT / 3D场景理解", "person_overseas", "spatial",
    "MIT教授，前Stanford 3D场景理解实验室主任。李飞飞的同事，将3D语义理解与机器人执行任务耦合，是Stanford 3D智能研究网的关键人物。")

add_node("Gordon_Wetzstein", "Gordon Wetzstein\\nStanford / 计算成像与神经渲染", "person_overseas", "spatial",
    "Stanford教授，计算成像与神经渲染方向。关注高效3D表示与显示技术。")

add_node("Lu_Jiang", "蒋路 Lu Jiang\\n前Google Research / 3D生成", "person_overseas", "spatial",
    "前Google Research研究科学家。多模态3D生成方向重要的学术-产业交叉人物，在3D生成与多模态模型上有系列工作。")

# --- 里程碑 ---
add_node("GQN", "GQN (2018)\\n端到端场景表示与渲染\\nScience 发表", "milestone", "spatial",
    "DeepMind发表在Science的端到端场景表示与渲染系统。展现了从二维观测生成三维空间表征的可行性，是空间智能路线的早期里程碑。")

add_node("Neuralangelo", "Neuralangelo (CVPR 2023)\\n高精度3D表面重建", "milestone", "spatial",
    "NVIDIA主导的高精度3D表面重建算法框架。Zhaoshuo Li为第一作者。利用多分辨率哈希编码实现高保真3D重建。")

add_node("RTFM", "RTFM (2025.10)\\nWorld Labs 实时帧模型", "milestone", "spatial",
    "World Labs发布的全新自回归扩散Transformer。支持从2D图像实时渲染3D场景帧，效率极高。是Marble产品的核心技术引擎之一。")

# --- 公司 ---
add_node("NVIDIA_Spatial_Intel_Lab", "NVIDIA Space Intelligence Lab\\ngsplat / Neuralangelo 孵化器", "institution", "spatial",
    "NVIDIA内部专注于空间智能与3D重建的研究实验室。孵化gsplat、Neuralangelo等核心底层框架，是空间智能基础设施的关键贡献者。")

add_node("Manycore", "Manycore\\n3D设计平台 (Aholo + LuxReal)", "company_overseas", "spatial",
    "3D设计平台公司，以Aholo和LuxReal产品线转型空间智能方向。")

add_node("Odyssey", "Odyssey\\n交互式世界模型 (伦敦)", "company_overseas", "spatial",
    "伦敦创业公司。由自动驾驶创业者Oliver Cameron与Jeff Hawke联合创办。开发交互式世界模型，40ms/帧实时生成可交互视频，无游戏引擎。Pixar联合创始人参与。")

add_node("General_Intuition", "General Intuition PBC\\n$133.7M 融资", "company_overseas", "spatial",
    "构建空间-时间推理世界模型的创业公司。累计融资$133.7M。")

add_node("Video_Rebirth", "Video Rebirth\\nAI视频世界模型 (新加坡)", "company_overseas", "spatial",
    "新加坡AI视频世界模型公司，主攻高端影视工业标准。由前腾讯杰出科学家Wei Liu创立。")

# ═══════════════════════════════════════════════════════════════
# 路线三：学习仿真 新增节点
# ═══════════════════════════════════════════════════════════════
print("\n=== 路线三：学习仿真 ===")

# 3A: 生成式视频世界模型
add_node("Alex_Krizhevsky", "Alex Krizhevsky\\nAlexNet一作 / 多伦多大学", "person_overseas", "sim",
    "多伦多大学博士。AlexNet第一作者，深度卷积神经网络奠基人。Ilya Sutskever的密切合作者。其核心技术思路间接奠定了视频/图像生成世界模型的表征基础。")

add_node("Ilya_Sutskever", "Ilya Sutskever\\n前OpenAI联合创始人 / SSI", "person_overseas", "sim",
    "前OpenAI联合创始人兼首席科学家。Alex Krizhevsky的前导师。从AlexNet到GPT系列再到多模态大模型，其倡导的大规模自回归方法直接影响视频世界模型（Sora、Runway等）的设计范式。")

add_node("Cristobal_Valenzuela", "Cristóbal Valenzuela\\nRunway CEO", "person_overseas", "sim",
    "Runway联合创始人兼CEO。带领团队完成Gen-1→Gen-2→Gen-3→Gen-4.5→GWM-1的产品升级，从视频生成全面转向世界模型。")

add_node("Anastasis_Germanidis", "Anastasis Germanidis\\nRunway CTO", "person_overseas", "sim",
    "Runway联合创始人兼CTO。与Valenzuela一起定义Runway视频世界的技术栈。")

add_node("Alejandro_Matamala", "Alejandro Matamala\\nRunway CDO", "person_overseas", "sim",
    "Runway联合创始人兼CDO。负责Runway产品与设计方向。")

add_node("Oliver_Cameron", "Oliver Cameron\\nOdyssey联合创始人", "person_overseas", "sim",
    "Odyssey联合创始人。前自动驾驶创业公司Voyage CEO。与Jeff Hawke共同创办Odyssey，开发交互式世界模型。")

add_node("Jeff_Hawke", "Jeff Hawke\\nOdyssey联合创始人", "person_overseas", "sim",
    "Odyssey联合创始人。前自动驾驶技术专家。与Oliver Cameron共同创办Odyssey。")

add_node("Wei_Liu", "Wei Liu\\nVideo Rebirth创始人 / IEEE/AAAS Fellow", "person_overseas", "sim",
    "Video Rebirth创始人，IEEE/AAAS Fellow。前腾讯杰出科学家。主攻高端影视工业标准的AI视频世界模型。")

add_node("Xun_Huang", "Xun Huang\\nCMU / HeyGen / 视频世界模型", "person_overseas", "sim",
    "CMU视频世界模型研究者，HeyGen关联。研究聚焦AI视频生成与编辑。")

# --- 里程碑 (3A) ---
add_node("Genie1", "Genie 1 (2024)\\nDeepMind 可玩世界概念", "milestone", "sim",
    "Google DeepMind发布。提出'可玩世界'概念——仅通过观看互联网视频学会生成可交互的游戏环境，为Genie系列奠基。")

add_node("Genie2", "Genie 2 (2024.12)\\n自回归潜扩散3D交互场景", "milestone", "sim",
    "Google DeepMind。自回归潜扩散模型，生成可控3D交互场景（鼠标/键盘驱动），具备对象交互、NPC行为和长时记忆（约1分钟）。")

# 3B: RL世界模型
add_node("Timothy_Lillicrap", "Timothy Lillicrap\\nDeepMind 深度RL理论", "person_overseas", "sim",
    "DeepMind深度强化学习理论核心人物。Dreamer V3合作者。在连续控制、策略梯度理论上有一系列奠基性贡献。")

add_node("Jurgis_Pasukonis", "Jurgis Pasukonis\\nDreamer V3共同作者", "person_overseas", "sim",
    "Dreamer V3共同作者。主要贡献在分布鲁棒性与平衡归一化策略，提升了Dreamer系列算法的稳定性和泛化能力。")

add_node("David_Silver", "David Silver\\nDeepMind首席科学家 / AlphaGo之父", "person_overseas", "sim",
    "DeepMind首席科学家。AlphaGo、AlphaZero、MuZero、AlphaStar核心推手。从围棋到通用游戏的深度强化学习范式奠定了基于模型的RL世界模型理论基础。")

add_node("Julian_Schrittwieser", "Julian Schrittwieser\\nMuZero一作", "person_overseas", "sim",
    "DeepMind研究员，MuZero一作。构建了基于价值等价原理与MCTS的模型驱动规划范式，直接影响后续UniZero和Dreamer系列。")

add_node("Sergey_Levine", "Sergey Levine\\nUC Berkeley / 机器人学习权威", "person_overseas", "sim",
    "UC Berkeley教授，机器人学习权威。将视觉世界模型大规模应用于机器人操控任务（RT-1、RT-2等关键线）。其博士生/博士后遍布Skild AI等明星公司。")

add_node("Pieter_Abbeel", "Pieter Abbeel\\nUC Berkeley / 深度RL先驱", "person_overseas", "sim",
    "UC Berkeley教授，深度强化学习与机器人先驱。早期探索世界模型在机器人任务中的各项应用。Danijar Hafner在UC Berkeley期间的访问导师。")

add_node("Chelsea_Finn", "Chelsea Finn\\nStanford / 元学习与泛化推理", "person_overseas", "sim",
    "Stanford教授，原Sergey Levine学生。元学习与泛化推理权威，将少样本自适应世界模型引入机器人操作任务。")

add_node("Deepak_Pathak", "Deepak Pathak\\nCMU / 好奇心驱动探索", "person_overseas", "sim",
    "CMU教授，原Sergey Levine学生。好奇心驱动探索的世界模型先锋，提出ICM、RND、视频预测模型等。")

add_node("Ashish_Vaswani", "Ashish Vaswani\\nTransformer核心作者", "person_overseas", "sim",
    "Transformer核心作者（Attention Is All You Need）。发明了现代大模型架构基础（注意力机制），与Łukasz Kaiser的工作共同塑造了现代世界模型架构范式。")

add_node("Lukasz_Kaiser", "Łukasz Kaiser\\nTransformer核心作者 / Dreamer合作者", "person_overseas", "sim",
    "Transformer核心作者之一。Danijar Hafner的密切合作者，在模型架构设计上深刻影响了Dreamer系列向Transformer的迁移。")

add_node("Abhinav_Gupta", "Abhinav Gupta\\nCMU / Skild AI联合创始人", "person_overseas", "sim",
    "CMU教授，Skild AI联合创始人。大规模机器人世界模型与基础模型训练实践的积极推动者。")

# --- 里程碑 (3B) ---
add_node("MuZero", "MuZero (2019-2020)\\n潜空间树搜索规划\\nDeepMind", "milestone", "sim",
    "DeepMind发布。无环境模型的潜在空间树搜索规划。在Atari、围棋、国际象棋等领域实现超人类表现，无需知道游戏规则。奠定了基于价值等价的模型驱动规划范式。")

add_node("UniZero", "UniZero (2024+)\\nTransformer统一潜空间规划", "milestone", "sim",
    "价值等价+Transformer的可扩展统一潜空间规划框架。在MuZero基础上引入Transformer架构提升可扩展性。")

# --- 公司 (3B) ---
add_node("Skild_AI", "Skild AI\\n通用机器人世界模型\\n估值$140B+", "company_overseas", "sim",
    "通用机器人世界模型公司。Skild Brain跨具身形态训练，累计估值超过140亿美元。Abhinav Gupta联合创办。Sergey Levine学生/博士后广泛参与。")

add_node("Wayve", "Wayve\\n自动驾驶世界模型 (伦敦)", "company_overseas", "sim",
    "伦敦自动驾驶公司。端到端可学习驾驶模拟，构建自动驾驶世界模型。以GAIA-1世界模型闻名。")

add_node("Waabi", "Waabi\\n可微传感器模拟 (多伦多)", "company_overseas", "sim",
    "多伦多自动驾驶公司。Raquel Urtasun创办。基于可微传感器模拟构建世界模型，强调安全验证。")

add_node("OneX_Technologies", "1X Technologies\\nNeo世界模型 / 机器人", "company_overseas", "sim",
    "发布Neo世界模型，直接对标机器人仿真-现实迁移。人形机器人公司。")

add_node("FieldAI", "FieldAI\\n$405M 融资 / 物理优先机器人模型", "company_overseas", "sim",
    "融资$405M，市值约$2B。'物理优先'机器人基础模型公司。")

# --- 论文/综述 ---
add_node("DINO_WM", "DINO-WM\\n自监督世界模型", "milestone", "sim",
    "自监督世界模型。被ACM CSUR 2025综述列为可与JEPA/Dreamer并行对比的核心方法论。利用DINO自监督特征构建世界模型。")

add_node("ACM_CSUR_2025_Review", "ACM CSUR 世界模型综述 (2025)\\n清华等机构", "milestone", "sim",
    "系统梳理MBRL、自监督世界模型、LLM结合路径三大轴。是世界模型领域最全面的学术综述之一。")

add_node("Hi_WM", "Hi-WM (2026)\\n人机世界模型后训练校正", "milestone", "sim",
    "Human-in-the-World-Model。基于世界模型的机器人策略后训练校正框架，将人类反馈引入世界模型训练循环。")

# ═══════════════════════════════════════════════════════════════
# 路线四：物理AI基础设施 新增节点
# ═══════════════════════════════════════════════════════════════
print("\n=== 路线四：物理AI基础设施 ===")

# 注意：Cosmos已存在，但Cosmos Predict/Transfer/Reason是子产品

add_node("Cosmos_Predict", "Cosmos Predict (2025)\\n视频预测后训练模型", "milestone", "sim",
    "NVIDIA Cosmos平台的视频预测后训练模型。用于机器人/驾驶特定场景的状态推演，实现物理世界的时间序列预测。")

add_node("Cosmos_Transfer", "Cosmos Transfer (2025)\\nsim-to-real域适应", "milestone", "sim",
    "NVIDIA Cosmos平台的大规模sim-to-real域适应模型。解决仿真与真实世界之间的视觉和物理动力学鸿沟。")

add_node("Cosmos_Reason", "Cosmos Reason (GTC 2025)\\n物理场景链式推理", "milestone", "sim",
    "NVIDIA Cosmos平台的物理场景链式思维推理。时空感知+因果交互理解+视频问答，将LLM推理范式引入物理世界模型。")

add_node("Omniverse_DSX", "Omniverse DSX Blueprint (GTC 2026)\\n数字孪生集成框架", "milestone", "sim",
    "NVIDIA发布的数字孪生集成框架。开放AI工厂的数据与物理仿真层，打通Omniverse与Cosmos的全栈物理AI生态。")

add_node("World51_Model", "51World Model (2026.03)\\n全球首款物理直觉世界模型", "milestone", "sim",
    "51WORLD发布。全球首款自带'物理直觉'的世界模型产品。发布三大能力模块：重建与生成/训练与部署/预测与规划。")

# --- 公司 ---
add_node("WORLD51", "51WORLD 五一视界\\nHK:6651 / 物理AI第一股", "company_overseas", "sim",
    "香港上市（HK:6651）。'物理AI第一股'。51Sim在高阶自动驾驶仿真市占率53.5%。2026年3月发布51World Model。")

add_node("Oxa", "Oxa (前Oxbotica)\\n英国自动驾驶公司", "company_overseas", "sim",
    "英国自动驾驶公司。引入NVIDIA Cosmos Predict增强虚拟传感器，将世界模型技术应用于自动驾驶感知系统。")

add_node("Moon_Surgical", "Moon Surgical\\n手术机器人 / Cosmos生态", "company_overseas", "sim",
    "手术机器人公司。使用NVIDIA Cosmos生成模拟临床环境，将世界模型应用于医疗手术场景。")

add_node("Lightwheel", "Lightwheel\\nCosmos生态系统合作伙伴", "company_overseas", "sim",
    "NVIDIA Cosmos生态系统合作伙伴。参与物理AI数据生成与仿真管线。")

add_node("Flexcompute", "Flexcompute\\nGPU原生物理仿真超算 (Flow360)", "company_overseas", "sim",
    "GPU原生物理仿真超算平台。Flow360为旗舰产品，提供CFD等物理场仿真能力。与NVIDIA Omniverse生态互补。")

add_node("Hexagon", "Hexagon\\n工业数字孪生 / Omniverse集成", "company_overseas", "sim",
    "整合NVIDIA Omniverse到工业数字孪生工作流。工业测量与仿真软件全球领导者。")

add_node("Flexion", "Flexion\\nEX-NVIDIA / $50M 融资 / 服务机器人", "company_overseas", "sim",
    "EX-NVIDIA团队创办。获$50M融资。专注服务机器人的通用AI'大脑'。")

# --- 中国公司 ---
add_node("DemoChain", "索辰科技 DemoChain\\n中国物理AI仿真", "company_china", "sim",
    "中国物理AI仿真公司。具身智能虚拟训练平台DemoChain，提供国产替代方案。")

add_node("MooreThreads_51Sim", "摩尔线程 + 51Sim\\n国产GPU集群+物理AI仿真", "company_china", "sim",
    "国产GPU集群与物理AI仿真体系。摩尔线程提供GPU算力基础，51Sim提供仿真能力，共同构建中国自主可控的物理AI基础设施。")

# ═══════════════════════════════════════════════════════════════
# 路线五：主动推理 新增节点
# ═══════════════════════════════════════════════════════════════
print("\n=== 路线五：主动推理 ===")

add_node("Thomas_Parr", "Thomas Parr\\nUCL / Active Inference教材一作", "person_overseas", "active_inf",
    "UCL研究员，Friston核心合作者。《Active Inference》教材一作，负责主动推理的理论体系化工作。")

add_node("Tommaso_Salvatori", "Tommaso Salvatori\\n主动推理意图行为理论", "person_overseas", "active_inf",
    "主动推理与意图行为理论的关键贡献者之一。2023年发表主动推理与意图行为的基准论文。")

add_node("Takuya_Isomura", "Takuya Isomura\\n主动推理理论贡献者", "person_overseas", "active_inf",
    "主动推理与意图行为理论的关键贡献者之一。在主动推理的数学理论和神经实现上有系列贡献。")

add_node("Alexander_Tschantz", "Alexander Tschantz\\n主动推理理论贡献者", "person_overseas", "active_inf",
    "主动推理与意图行为理论的关键贡献者之一。2023年参与发表主动推理基准论文。")

add_node("Maxwell_Ramstead", "Maxwell J. D. Ramstead\\nVERSES研究主管", "person_overseas", "active_inf",
    "VERSES AI研究主管。研究方向涵盖主动推理、生成模型与社会认知计算。是VERSES学术-产业转化链条的关键节点。")

add_node("Conor_Heins", "Conor Heins\\n主动推理树搜索贡献者", "person_overseas", "active_inf",
    "主动推理树搜索（POMDP大型状态空间）的核心贡献者之一。推动主动推理从中小规模问题向大规模状态空间扩展。")

add_node("Magnus_Koudahl", "Magnus Koudahl\\n主动推理学术网络", "person_overseas", "active_inf",
    "主动推理核心学术网络成员。在主动推理的神经网络实现方向有重要贡献。")

add_node("Aswin_Paul", "Aswin Paul\\n主动推理学术网络", "person_overseas", "active_inf",
    "主动推理核心学术网络成员。")

add_node("Adeel_Razi", "Adeel Razi\\n主动推理学术网络", "person_overseas", "active_inf",
    "主动推理核心学术网络成员。在主动推理的神经科学应用方向有贡献。")

add_node("Brett_Kagan", "Brett J. Kagan\\n主动推理学术网络", "person_overseas", "active_inf",
    "主动推理核心学术网络成员。在主动推理与生物神经网络交叉方向有研究。")

add_node("Tim_Verbelen", "Tim Verbelen\\n主动推理与机器人分层控制", "person_overseas", "active_inf",
    "主动推理与机器人分层控制方向的重要研究者。将主动推理框架应用于机器人操作的层级控制。")

add_node("David_Scott", "David T. Scott\\nVERSES董事会 / 前AWS高管", "person_overseas", "active_inf",
    "前AWS高管，加入VERSES AI董事会推动商业化进程。在云计算和企业级AI产品方面有丰富经验。")

# --- 里程碑 ---
add_node("Sophisticated_Inference", "Sophisticated Inference (2020)\\nFriston & Hafner 合著", "milestone", "active_inf",
    "Friston与Hafner合著的重要论文。将主动推理与递归期望自由能统一，把RL纳入主动推理的特殊情形。打通了计算神经科学与深度RL的数学桥梁。")

add_node("Active_Inference_Intentional", "Active Inference & Intentional Behaviour (2023)\\n形式化意图行为", "milestone", "active_inf",
    "Salvatori、Isomura、Tschantz等人发表。系统阐述意图行为与主动推理的形式联系，为主动推理从理论走向智能体行为生成提供了数学基础。")

add_node("AXIOM_Robot", "AXIOM机器人论文 (2025.07)\\n层次化主动推理长期规划", "milestone", "active_inf",
    "VERSES发布。完全层次化主动推理架构用于长期重排任务。首次在真实机器人平台展示主动推理的长期规划能力，无预训练实时适应。")

add_node("Active_Inference_Patent", "主动推理专利 (2025)\\n自然语言指定智能体领域模型", "milestone", "active_inf",
    "VERSES申请的主动推理专利。基于自然语言指定主动推理智能体领域模型，降低主动推理系统的使用门槛。")

# --- 公司 ---
add_node("Themesis", "Themesis, Inc.\\n主动推理技术合作伙伴", "company_overseas", "active_inf",
    "与VERSES AI深度合作的主动推理技术伙伴。共同推进主动推理在工业场景的应用落地。")

# ═══════════════════════════════════════════════════════════════
# 新增边
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增关系边 ===")

# ── JEPA 路线边 ──
add_edge("Yann_LeCun", "Alexandre_LeBrun", "co_founded", "联合创办 AMI Labs (2025)", "tier1")
add_edge("Yann_LeCun", "Saining_Xie", "lab", "LeCun团队核心成员 → 2026加入AMI Labs", "tier1")
add_edge("Yann_LeCun", "Mahmoud_Assran", "lab", "I-JEPA/V-JEPA核心作者", "tier1")
add_edge("Yann_LeCun", "Adrien_Bardes", "lab", "V-JEPA核心架构师", "tier1")
add_edge("Yann_LeCun", "Jean_Ponce", "co_authored", "长期学术合作 / 合著JEPA规划论文", "tier1")
add_edge("Yann_LeCun", "Kyunghyun_Cho", "lab_colleague_industry", "NYU同事 / 合著慢特征论文", "tier2")
add_edge("Yann_LeCun", "Emmanuel_Dupoux", "lab", "Meta FAIR同事 / 认知建模传统", "tier2")
add_edge("Yann_LeCun", "Bo_Wang", "lab", "关注并背书医学超声JEPA", "tier2")
add_edge("Mahmoud_Assran", "I_JEPA", "maintainer", "I-JEPA 一作 (2023)", "tier1")
add_edge("Adrien_Bardes", "V_JEPA", "maintainer", "V-JEPA 核心架构师", "tier1")
add_edge("Mahmoud_Assran", "V_JEPA2", "maintainer", "V-JEPA 2 核心作者", "tier1")
add_edge("Adrien_Bardes", "V_JEPA2", "maintainer", "V-JEPA 2 核心架构师", "tier1")
add_edge("Nicolas_Ballas", "V_JEPA2", "maintainer", "V-JEPA 2 核心共同作者", "tier2")
add_edge("Quentin_Garrido", "V_JEPA2", "maintainer", "V-JEPA 2 共同作者", "tier2")
add_edge("David_Fan", "V_JEPA2", "maintainer", "V-JEPA 2 共同作者", "tier2")
add_edge("Russell_Howes", "V_JEPA2", "maintainer", "V-JEPA 2 共同作者", "tier2")
add_edge("Mojtaba_Komeili", "V_JEPA2", "maintainer", "V-JEPA 2 共同作者", "tier2")
add_edge("Michael_Rabbat", "V_JEPA2", "maintainer", "V-JEPA 2 合作作者", "tier2")
add_edge("Lorenzo_Mur_Labadia", "V_JEPA2_1", "maintainer", "V-JEPA 2.1 核心贡献", "tier2")
add_edge("Matthew_Muckley", "V_JEPA2_1", "maintainer", "V-JEPA 2.1 核心贡献", "tier2")
add_edge("Amir_Bar", "V_JEPA2_1", "maintainer", "V-JEPA 2.1 核心贡献", "tier2")
add_edge("Koustuv_Sinha", "V_JEPA2_1", "maintainer", "V-JEPA 2.1 核心贡献", "tier2")
add_edge("Vlad_Sobal", "JEPA_concept", "maintainer", "JEPA实证研究", "tier2")
add_edge("V_JyothirS", "JEPA_concept", "maintainer", "JEPA实证研究", "tier2")
add_edge("Siddhartha_Jalagam", "JEPA_concept", "maintainer", "JEPA实证研究", "tier2")
add_edge("Nicolas_Carion", "JEPA_concept", "maintainer", "JEPA实证研究", "tier2")
add_edge("Yann_LeCun", "Value_Guided_Planning_JEPA", "maintainer", "合著者 (2026)", "tier1")
add_edge("Jean_Ponce", "Value_Guided_Planning_JEPA", "maintainer", "合著者 (2026)", "tier1")
add_edge("Matthieu_Destrade", "Value_Guided_Planning_JEPA", "maintainer", "合著者 (2026)", "tier2")
add_edge("Oumayma_Bounou", "Value_Guided_Planning_JEPA", "maintainer", "合著者 (2026)", "tier2")
add_edge("Quentin_Le_Lidec", "Value_Guided_Planning_JEPA", "maintainer", "合著者 (2026)", "tier2")
add_edge("Bo_Wang", "Medical_Ultrasound_JEPA", "maintainer", "首度将JEPA引入医疗影像", "tier1")
add_edge("Alif_Munim", "Medical_Ultrasound_JEPA", "maintainer", "首度将JEPA引入医疗影像", "tier1")
add_edge("Medical_Ultrasound_JEPA", "JEPA_concept", "derived", "JEPA在医疗影像的应用", "tier2")
add_edge("I_JEPA", "V_JEPA", "evolution", "图像→视频扩展", "tier2")
add_edge("V_JEPA", "V_JEPA2", "evolution", "架构升级", "tier2")
add_edge("V_JEPA2", "V_JEPA2_1", "evolution", "密集表征升级", "tier2")
add_edge("V_JEPA2_1", "Rethinking_JEPA", "evolution", "训练效率优化", "tier2")
add_edge("Alexandre_LeBrun", "AMI_Labs", "co_founded", "联合创始人 & CEO", "tier1")
add_edge("Alexandre_LeBrun", "Nabla", "founded", "前联合创始人 & CEO", "tier2")
add_edge("Saining_Xie", "AMI_Labs", "employed", "2026 加入", "tier1")
add_edge("Saining_Xie", "Meta_FAIR", "employed", "前研究科学家", "tier2")
add_edge("Mahmoud_Assran", "Meta_FAIR", "employed", "研究科学家", "tier2")
add_edge("Adrien_Bardes", "Meta_FAIR", "employed", "研究科学家", "tier2")
add_edge("Nicolas_Ballas", "Meta_FAIR", "employed", "研究科学家 (Mila校友)", "tier2")
add_edge("Jean_Ponce", "Meta_FAIR", "employed", "前FAIR研究总监", "tier2")
add_edge("Emmanuel_Dupoux", "Meta_FAIR", "employed", "Meta FAIR / EHESS / INRIA", "tier2")
add_edge("Kyunghyun_Cho", "Meta_FAIR", "lab", "NYU / FAIR 交叉", "tier2")
add_edge("Aaron_van_den_Oord", "JEPA_concept", "inspired", "VQ-VAE/CPC为JEPA提供方法论基础", "tier2")
add_edge("Ishan_Misra", "JEPA_concept", "inspired", "SimCLR/DINO自监督方法论基础", "tier2")
add_edge("Alyosha_Efros", "JEPA_concept", "inspired", "自监督学习先驱", "tier2")
add_edge("Geoffrey_Hinton", "Aaron_van_den_Oord", "mentorship", "间接影响", "tier2")
add_edge("Geoffrey_Hinton", "Ishan_Misra", "mentorship", "间接影响", "tier2")

# ── 空间智能路线边 ──
add_edge("Ben_Mildenhall", "Pratul_Srinivasan", "co_authored", "NeRF合著者", "tier1")
add_edge("Ravi_Ramamoorthi", "Ben_Mildenhall", "mentorship", "博士导师", "tier1")
add_edge("Ravi_Ramamoorthi", "Pratul_Srinivasan", "mentorship", "博士导师", "tier1")
add_edge("Ben_Mildenhall", "NeRF", "maintainer", "第一作者", "tier1")
add_edge("Pratul_Srinivasan", "NeRF", "maintainer", "合著者", "tier1")
add_edge("Ruilong_Li", "NVIDIA_Spatial_Intel_Lab", "employed", "gsplat/nerfacc/nerfstudio原初作者", "tier1")
add_edge("Ruilong_Li", "Gaussian_Splat", "maintainer", "gsplat生态推动者", "tier1")
add_edge("Zhaoshuo_Li", "Neuralangelo", "maintainer", "第一作者", "tier1")
add_edge("Thomas_Muller", "Gaussian_Splat", "maintainer", "Instant NGP → 3D高斯生态加速", "tier1")
add_edge("NVIDIA_Spatial_Intel_Lab", "Neuralangelo", "maintainer", "NVIDIA 孵化", "tier1")
add_edge("Gordon_Wetzstein", "FeiFei_Li", "lab_colleague_industry", "斯坦福同事", "tier2")
add_edge("Ashutosh_Saxena", "FeiFei_Li", "lab_colleague_industry", "斯坦福同事 / 3D语义理解", "tier2")
add_edge("Andreas_Geiger", "Gaussian_Splat", "inspired", "可微渲染→3D重建理论基础", "tier2")
add_edge("World_Labs", "RTFM", "maintainer", "核心产品", "tier1")
add_edge("Ben_Mildenhall", "NVIDIA_Spatial_Intel_Lab", "lab", "技术生态关联", "tier2")
add_edge("Google_DeepMind", "GQN", "maintainer", "DeepMind发表 (Science)", "tier1")
add_edge("Oliver_Cameron", "Odyssey", "founded", "联合创始人", "tier1")
add_edge("Jeff_Hawke", "Odyssey", "founded", "联合创始人", "tier1")
add_edge("Wei_Liu", "Video_Rebirth", "founded", "创始人", "tier1")
add_edge("Lu_Jiang", "FeiFei_Li", "lab", "Stanford-Google 3D生成交叉", "tier2")

# ── 学习仿真路线边 ──
# 3A 视频世界模型
add_edge("Ilya_Sutskever", "Alex_Krizhevsky", "mentorship", "前导师 / AlexNet合作", "tier1")
add_edge("Alex_Krizhevsky", "Gen_Video_concept", "inspired", "CNN奠基→视频表征基础", "tier2")
add_edge("Ilya_Sutskever", "OpenAI_Sora", "founded", "OpenAI 联合创始人 → Sora战略", "tier1")
add_edge("Cristobal_Valenzuela", "Runway", "founded", "联合创始人 & CEO", "tier1")
add_edge("Anastasis_Germanidis", "Runway", "founded", "联合创始人 & CTO", "tier1")
add_edge("Alejandro_Matamala", "Runway", "founded", "联合创始人 & CDO", "tier1")
add_edge("Runway", "GWM1", "maintainer", "基于Gen-4.5的首个通用世界模型", "tier1")
add_edge("Google_DeepMind", "Genie1", "maintainer", "DeepMind发布", "tier1")
add_edge("Google_DeepMind", "Genie2", "maintainer", "DeepMind发布", "tier1")
add_edge("Genie1", "Genie2", "evolution", "自回归潜扩散升级", "tier2")
add_edge("Genie2", "Genie3", "evolution", "720p/24fps 实时交互", "tier2")
add_edge("Wei_Liu", "Video_Rebirth", "founded", "创始人", "tier1")
add_edge("Xun_Huang", "Gen_Video_concept", "maintainer", "CMU视频世界模型研究", "tier2")

# 3B RL世界模型
add_edge("Timothy_Lillicrap", "DreamerV3", "maintainer", "合作者 / 深度RL理论", "tier1")
add_edge("Jurgis_Pasukonis", "DreamerV3", "maintainer", "分布鲁棒性贡献", "tier1")
add_edge("David_Silver", "Google_DeepMind", "employed", "首席科学家", "tier1")
add_edge("David_Silver", "MuZero", "maintainer", "AlphaGo/AlphaZero/MuZero系列推动者", "tier1")
add_edge("Julian_Schrittwieser", "MuZero", "maintainer", "MuZero 一作", "tier1")
add_edge("Julian_Schrittwieser", "Google_DeepMind", "employed", "研究科学家", "tier1")
add_edge("MuZero", "DreamerV3", "inspired", "模型驱动规划→Dreamer范式影响", "tier2")
add_edge("MuZero", "UniZero", "evolution", "Transfomer统一框架升级", "tier2")
add_edge("Sergey_Levine", "Danijar_Hafner", "mentorship", "UC Berkeley 访问导师 (间接)", "tier2")
add_edge("Pieter_Abbeel", "Danijar_Hafner", "mentorship", "UC Berkeley 访问导师", "tier2")
add_edge("Sergey_Levine", "Chelsea_Finn", "mentorship", "博士导师", "tier1")
add_edge("Sergey_Levine", "Deepak_Pathak", "mentorship", "博士导师", "tier1")
add_edge("Chelsea_Finn", "Model_Based_RL", "maintainer", "少样本自适应世界模型", "tier2")
add_edge("Deepak_Pathak", "Model_Based_RL", "maintainer", "好奇心驱动探索世界模型", "tier2")
add_edge("Ashish_Vaswani", "Model_Based_RL", "inspired", "Transformer架构→世界模型架构基础", "tier2")
add_edge("Lukasz_Kaiser", "Danijar_Hafner", "co_authored", "密切合作 / Dreamer Transformer迁移", "tier1")
add_edge("Lukasz_Kaiser", "Dreamer4", "inspired", "Transformer架构影响", "tier2")
add_edge("Abhinav_Gupta", "Skild_AI", "founded", "联合创始人", "tier1")
add_edge("Sergey_Levine", "Skild_AI", "lab", "学生/博士后广泛参与", "tier2")
add_edge("Ashish_Vaswani", "Google_DeepMind", "employed", "前研究员 (Attention Is All You Need)", "tier2")

# 公司
add_edge("Wayve", "Model_Based_RL", "maintainer", "端到端驾驶世界模型", "tier2")
add_edge("Waabi", "Model_Based_RL", "maintainer", "可微传感器模拟世界模型", "tier2")
add_edge("OneX_Technologies", "Model_Based_RL", "maintainer", "Neo世界模型 / 仿真-现实迁移", "tier2")
add_edge("FieldAI", "Model_Based_RL", "maintainer", "物理优先机器人基础模型", "tier2")

# 综述/概念
add_edge("DINO_WM", "Model_Based_RL", "evolution", "自监督世界模型与RL融合", "tier2")
add_edge("Hi_WM", "Model_Based_RL", "evolution", "人类反馈世界模型校正", "tier2")

# ── 物理AI基础设施边 ──
add_edge("NVIDIA", "Cosmos_Predict", "maintainer", "NVIDIA 发布", "tier1")
add_edge("NVIDIA", "Cosmos_Transfer", "maintainer", "NVIDIA 发布", "tier1")
add_edge("NVIDIA", "Cosmos_Reason", "maintainer", "NVIDIA GTC 2025", "tier1")
add_edge("NVIDIA", "Omniverse_DSX", "maintainer", "NVIDIA GTC 2026", "tier1")
add_edge("Cosmos", "Cosmos_Predict", "evolution", "Cosmos 平台 → Predict 子产品", "tier1")
add_edge("Cosmos", "Cosmos_Transfer", "evolution", "Cosmos 平台 → Transfer 子产品", "tier1")
add_edge("Cosmos", "Cosmos_Reason", "evolution", "Cosmos 平台 → Reason 子产品", "tier1")
add_edge("Cosmos", "Omniverse_DSX", "evolution", "Cosmos+Omniverse 集成", "tier2")
add_edge("WORLD51", "World51_Model", "maintainer", "51WORLD 发布 (2026.03)", "tier1")
add_edge("Oxa", "Cosmos_Predict", "lab", "引入 Cosmos Predict 增强虚拟传感器", "tier2")
add_edge("Moon_Surgical", "Cosmos", "lab", "使用 Cosmos 生成模拟临床环境", "tier2")
add_edge("Lightwheel", "Cosmos", "lab", "Cosmos 生态合作伙伴", "tier2")
add_edge("Flexcompute", "NVIDIA", "lab", "Flow360 GPU原生物理仿真互补", "tier2")
add_edge("Hexagon", "NVIDIA", "lab", "Omniverse 工业数字孪生集成", "tier2")
add_edge("Flexion", "NVIDIA", "spun_off", "EX-NVIDIA团队创办", "tier2")
add_edge("DemoChain", "World51_Model", "lab", "国产替代 / 物理AI仿真生态", "tier2")
add_edge("MooreThreads_51Sim", "World51_Model", "lab", "国产GPU+物理AI仿真体系", "tier2")

# ── 主动推理路线边 ──
add_edge("Karl_Friston", "Thomas_Parr", "lab", "核心合作者 / 教材合著", "tier1")
add_edge("Karl_Friston", "Tommaso_Salvatori", "lab", "意图行为理论合作", "tier2")
add_edge("Karl_Friston", "Takuya_Isomura", "lab", "理论合作者", "tier2")
add_edge("Karl_Friston", "Alexander_Tschantz", "lab", "理论合作者", "tier2")
add_edge("Karl_Friston", "Maxwell_Ramstead", "lab", "VERSES研究主管", "tier1")
add_edge("Karl_Friston", "Conor_Heins", "lab", "树搜索合作者", "tier2")
add_edge("Karl_Friston", "Tim_Verbelen", "lab", "机器人分层控制合作", "tier2")
add_edge("Karl_Friston", "Sophisticated_Inference", "maintainer", "合著者 (与Hafner)", "tier1")
add_edge("Danijar_Hafner", "Sophisticated_Inference", "maintainer", "合著者 (与Friston)", "tier1")
add_edge("Sophisticated_Inference", "Active_Inference", "evolution", "RL与主动推理的统一", "tier2")
add_edge("Tommaso_Salvatori", "Active_Inference_Intentional", "maintainer", "核心贡献者 (2023)", "tier1")
add_edge("Takuya_Isomura", "Active_Inference_Intentional", "maintainer", "核心贡献者 (2023)", "tier1")
add_edge("Alexander_Tschantz", "Active_Inference_Intentional", "maintainer", "核心贡献者 (2023)", "tier1")
add_edge("Maxwell_Ramstead", "VERSES_AI", "employed", "研究主管", "tier1")
add_edge("VERSES_AI", "AXIOM_Robot", "maintainer", "层次化主动推理真实机器人验证", "tier1")
add_edge("VERSES_AI", "Active_Inference_Patent", "maintainer", "自然语言指定智能体领域模型", "tier1")
add_edge("AXIOM_Robot", "AXIOM", "evolution", "机器人增强版", "tier2")
add_edge("David_Scott", "VERSES_AI", "employed", "董事会成员 / 前AWS高管", "tier2")
add_edge("Themesis", "VERSES_AI", "lab", "深度技术合作", "tier2")
add_edge("Magnus_Koudahl", "Active_Inference", "maintainer", "神经网络实现贡献", "tier2")
add_edge("Aswin_Paul", "Active_Inference", "maintainer", "学术网络成员", "tier2")
add_edge("Adeel_Razi", "Active_Inference", "maintainer", "神经科学应用贡献", "tier2")
add_edge("Brett_Kagan", "Active_Inference", "maintainer", "生物神经网络交叉研究", "tier2")
add_edge("Tim_Verbelen", "AXIOM_Robot", "maintainer", "机器人分层控制研究", "tier2")

# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 2
data["meta"]["updated"] = "2026-05-25"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v2: 大规模增量更新，新增~100+节点，覆盖JEPA/空间智能/学习仿真/物理AI基建/主动推理五条路线的详细人物、公司和里程碑")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

# 运行 rebuild_v4.py
print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
