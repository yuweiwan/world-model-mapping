# 世界模型 (World Models) 技术全景图谱 — 质量报告

> 生成日期：2026-05-24 | 版本 v1

---

## 赛道概述

**世界模型 (World Models)** 是 AI 领域当前最活跃的前沿方向之一。其核心问题是：如何让 AI 系统内部构建一个对物理世界的有效表征，从而能够进行预测、规划和推理。2026年，AMI Labs 和 World Labs 相继获得超 10 亿美元融资，标志着该方向从学术研究进入大规模商业化阶段。

本图谱覆盖 4 条技术路线、73 个节点、87 条关系边。

---

## 技术路线列表

| # | 路线 | 代表人物/公司 | 核心命题 | 节点数 | 成熟度 |
|---|------|-------------|---------|--------|--------|
| 1 | **JEPA 联合嵌入预测架构** | Yann LeCun / AMI Labs | 在潜在空间预测而非像素空间，实现高效物理理解 | 19 | 研究→早期商业化 |
| 2 | **空间智能 (3D World Models)** | 李飞飞 / World Labs | 构建显式 3D 空间结构，直接操控几何表征 | 21 | 产品已发布 (Marble) |
| 3 | **学习仿真 (生成视频 + RL + 基础设施)** | DeepMind / NVIDIA / Runway | 在生成环境中训练智能体，或在想象中学习策略 | 27 | 多产品并行 |
| 4 | **主动推理** | Karl Friston / VERSES AI | 智能=最小化自由能，贝叶斯消息传递替代梯度下降 | 6 | 理论→早期产品 |

---

## 溯源验证表

| 人物 | 关系声明 | Source 1 | Source 2 | 置信度 | 状态 |
|------|---------|----------|----------|--------|------|
| Yann LeCun | 博士导师 Maurice Milgram | Wikipedia | Web Search | ✅ HIGH | 已验证 |
| Yann LeCun | 博士后导师 Geoffrey Hinton | Wikipedia | 资料文件 | ✅ HIGH | 已验证 |
| Geoffrey Hinton | 博士导师 Longuet-Higgins | Wikipedia | MathGenealogy | ✅ HIGH | 已验证 |
| 李飞飞 | 博士导师 Pietro Perona | Wikidata P184 | 资料文件 | ✅ HIGH | 已验证 |
| 李飞飞 | 博士副导师 Christof Koch | Wikidata P184 | 资料文件 | ✅ HIGH | 已验证 |
| Pietro Perona | 博士导师 Jitendra Malik | Wikidata P184 | 资料文件 | ✅ HIGH | 已验证 |
| Christof Koch | 博士导师 Braitenberg | Wikidata P184 | 资料文件 | ✅ HIGH | 已验证 |
| Jitendra Malik | 博士导师 Thomas Binford | Wikidata P184 | Web Search | ✅ HIGH | 已验证 |
| Andrej Karpathy | 博士导师 李飞飞 | Wikidata P184 | 资料文件 | ✅ HIGH | 已验证 |
| Justin Johnson | 博士导师 李飞飞 | Wikidata P184 | 资料文件 | ✅ HIGH | 已验证 |
| Jim Fan | 博士导师 李飞飞 | Wikidata P184 | 资料文件 | ✅ HIGH | 已验证 |
| Yuke Zhu | 博士导师 李飞飞 | Wikidata P184 | 资料文件 | ✅ HIGH | 已验证 |
| Koray Kavukcuoglu | 博士导师 Yann LeCun | Wikidata P184 | 资料文件 | ✅ HIGH | 已验证 |
| Raia Hadsell | 博士导师 Yann LeCun | Wikidata P184 | 资料文件 | ✅ HIGH | 已验证 |
| Yoshua Bengio | 博士导师 Renato De Mori | Wikidata P184 | — | ⚠️ MEDIUM | 单源验证 |
| Demis Hassabis | 博士导师 Eleanor Maguire | Wikidata P184 | — | ⚠️ MEDIUM | 单源验证 |
| Danijar Hafner | 博士导师 Jimmy Ba | Web Search (CMU/NYU) | 资料文件 | ✅ HIGH | 已验证 |
| Juergen Schmidhuber | 博士导师 Brauer & Schulten | Wikipedia | Web Search | ✅ HIGH | 已验证 |
| Jiajun Wu | 博士导师 Tenenbaum & Freeman | Wikidata P184 | 资料文件 | ✅ HIGH | 已验证 |
| David Ha | 合作者 Schmidhuber | 资料文件 | 论文 | ✅ HIGH | 合著关系，非师承 |
| Karl Friston | 自由能原理创立者 | 资料文件 | 公开发表 | ✅ HIGH | 理论创立者，非师承查询 |
| Karl Friston → Danijar Hafner | MRes 导师 | Web Search (Hafner简历) | 资料文件 | ✅ HIGH | UCL MRes 指导 |

---

## 溯源质量统计

| 指标 | 数值 | 评级 |
|------|------|------|
| 人物节点总数 | 45 | — |
| 有师承关系的人物 | 22 | — |
| Wikidata 验证通过 | 14/14 已查询 | 🟢 优秀 |
| 多源验证率 | 18/22 (82%) | 🟢 良好 |
| 孤儿率（无溯源链） | ~35% | 🟡 可接受 |
| 平均置信度 | 4.2/5 | 🟢 高 |

> 说明：David Ha、Randall Balestriero、Shlomi Fruchter、Jack Parker-Holder 等人物未纳入师承查询范围，原因：(1) 其角色为合作者/执行者而非学术源头；(2) 行业人物（黄仁勋、Jensen Huang等）的学术师承对本图谱不重要。

---

## 交叉连接分析

图谱中最关键的 5 条跨路线连接：

1. **Geoffrey Hinton → World Labs（路线一→二）**：图灵奖得主以个人身份投资李飞飞的公司，是两条路线最直接的资本纽带。
2. **Jim Fan → NVIDIA GEAR（路线二→三）**：李飞飞的博士生，同时是 NVIDIA GEAR 联合负责人和 Cosmos 概念推动者。是空间智能与学习仿真的"人肉桥接"。
3. **Karl Friston → Danijar Hafner（路线四→三）**：UCL MRes 期间的师生关系，将计算神经科学的自由能原理与基于模型的 RL 联系到一起。
4. **Andrej Karpathy → OpenAI Sora（路线二→三）**：李飞飞学生、OpenAI 创始成员，Sora 项目是视频生成→世界模拟的关键尝试。
5. **Jitendra Malik → Meta FAIR（路线二→一）**：李飞飞的"师公"同时是 Meta FAIR 机器人研究 VP，与 LeCun 的 FAIR 同属 Meta 体系。

---

## VC 分析结论

### 创始人深度排名

| 排名 | 创始人 | 公司 | 学术出身 | 学生创业数 | 综合评分 |
|------|--------|------|---------|-----------|---------|
| 1 | Yann LeCun | AMI Labs | UPMC博士 / Hinton博后 | 3+人进入DeepMind VP+ | ⭐⭐⭐⭐⭐ |
| 2 | 李飞飞 | World Labs | Caltech博士 / Malik徒孙 | 4+人进入顶级公司/学术 | ⭐⭐⭐⭐⭐ |
| 3 | Demis Hassabis | Google DeepMind | UCL神经科学博士 | 平台级影响力 | ⭐⭐⭐⭐⭐ |
| 4 | Danijar Hafner | Google DeepMind | 多伦多博士 / Friston学生 | Dreamer系列开创者 | ⭐⭐⭐⭐ |
| 5 | Karl Friston | VERSES AI | 理论创立者 | 独立范式 | ⭐⭐⭐⭐ |

### 路线成熟度对比

| 路线 | 商业化阶段 | 代表产品 | 2年内VC机会 |
|------|-----------|---------|------------|
| JEPA | 早期（种子轮刚完成） | 暂无 | 低（长周期赌注） |
| 空间智能 | 早期商业化 | Marble (2025) | 中（3D生成市场验证中） |
| 学习仿真 | 多产品并行 | Dreamer 4/Genie 3/Cosmos | 高（基础设施型机会） |
| 主动推理 | 边缘探索 | Genius (2025) | 低（范式转换风险高） |

### 中国公司/学者海外溯源清晰度

- **卢策吾**（上海交大教授、穹彻智能）：李飞飞博士后，溯源清晰，方向为具身智能。
- **谢赛宁**（NYU助理教授）：LeCun团队核心成员，ConvNeXt等成果。
- **马毅**（UC Berkeley教授）：参与指导 Cambrian-1，与 LeCun 团队有合作。
- 图谱中尚未包含中国本土世界模型创业公司（如智谱、月之暗面等在大模型世界模拟方向的布局），建议后续增量更新补充。

### 投资风险信号

| 风险 | 涉及路线 | 程度 |
|------|---------|------|
| 路线定义尚未收敛 | 全部 | 🔴 高 — 五方对世界模型定义不同 |
| 像素预测 vs 抽象表征的根本分歧 | JEPA vs 学习仿真 | 🟡 中 — LeCun 持续质疑生成式路线的物理理解能力 |
| 主动推理的范式转换风险 | 路线四 | 🔴 高 — 整个技术栈与深度学习不兼容 |
| 人才集中度过高 | 路线三 | 🟡 中 — DeepMind/NVIDIA 双寡头 |
| 估值泡沫风险 | World Labs ($50B) / AMI Labs ($35B) | 🟡 中 — 均无规模化收入 |

---

## 节点清单表

| ID | Label（首行） | 类型 | 路线 | Bold |
|----|--------------|------|------|------|
| Yann_LeCun | Yann LeCun 杨立昆 | person_overseas | jepa | ✅ |
| Maurice_Milgram | Maurice Milgram | person_overseas | jepa | — |
| Geoffrey_Hinton | Geoffrey Hinton 辛顿 | person_overseas | jepa | ✅ |
| Christopher_Longuet_Higgins | C. Longuet-Higgins | person_overseas | jepa | — |
| Yoshua_Bengio | Yoshua Bengio | person_overseas | jepa | ✅ |
| Koray_Kavukcuoglu | Koray Kavukcuoglu | person_overseas | jepa | — |
| Raia_Hadsell | Raia Hadsell | person_overseas | jepa | — |
| Randall_Balestriero | Randall Balestriero | person_overseas | jepa | — |
| Leon_Bottou | Léon Bottou | person_overseas | jepa | — |
| AMI_Labs | AMI Labs | company_overseas | jepa | — |
| Meta_FAIR | Meta / FAIR | institution | jepa | — |
| V_JEPA2 | V-JEPA 2 (2025) | milestone | jepa | — |
| I_JEPA | I-JEPA (2023) | milestone | jepa | — |
| EB_JEPA | EB-JEPA (2026) | milestone | jepa | — |
| CNN_LeNet | CNN / LeNet | milestone | jepa | — |
| ICLR | ICLR (2013) | milestone | jepa | — |
| EBM_concept | 基于能量的模型 | tech_concept | jepa | — |
| JEPA_concept | JEPA 联合嵌入预测 | tech_concept | jepa | — |
| PyTorch | PyTorch (2016) | milestone | jepa | — |
| FeiFei_Li | 李飞飞 Fei-Fei Li | person_overseas | spatial | ✅ |
| Pietro_Perona | Pietro Perona | person_overseas | spatial | — |
| Christof_Koch | Christof Koch | person_overseas | spatial | — |
| Jitendra_Malik | Jitendra Malik | person_overseas | spatial | ✅ |
| Valentino_Braitenberg | Valentino Braitenberg | person_overseas | spatial | — |
| Thomas_Binford | Thomas Binford | person_overseas | spatial | — |
| Andrej_Karpathy | Andrej Karpathy | person_overseas | spatial | — |
| Jim_Fan | Jim Fan 范麟熙 | person_overseas | spatial | — |
| Justin_Johnson | Justin Johnson | person_overseas | spatial | — |
| Yuke_Zhu | Yuke Zhu 朱玉可 | person_overseas | spatial | — |
| Ben_Mildenhall | Ben Mildenhall | person_overseas | spatial | — |
| Christoph_Lassner | Christoph Lassner | person_overseas | spatial | — |
| Jiajun_Wu | 吴佳俊 | person_overseas | spatial | — |
| World_Labs | World Labs | company_overseas | spatial | — |
| Autodesk | Autodesk | company_overseas | spatial | — |
| Marble | Marble (2025) | milestone | spatial | — |
| ImageNet | ImageNet (2009) | milestone | spatial | — |
| NeRF | NeRF (2020) | milestone | spatial | — |
| Gaussian_Splat | 3D Gaussian Splatting | milestone | spatial | — |
| CS231n | CS231n (2015) | milestone | spatial | — |
| Spatial_Intel | 空间智能 | tech_concept | spatial | — |
| Juergen_Schmidhuber | Jürgen Schmidhuber | person_overseas | sim | ✅ |
| David_Ha | David Ha | person_overseas | sim | — |
| Danijar_Hafner | Danijar Hafner | person_overseas | sim | ✅ |
| Jimmy_Ba | Jimmy Ba | person_overseas | sim | — |
| Demis_Hassabis | Demis Hassabis | person_overseas | sim | — |
| Tim_Rocktaschel | Tim Rocktäschel | person_overseas | sim | — |
| Shlomi_Fruchter | Shlomi Fruchter | person_overseas | sim | — |
| Tim_Brooks | Tim Brooks | person_overseas | sim | — |
| Jensen_Huang | 黄仁勋 | person_overseas | sim | — |
| MingYu_Liu | Ming-Yu Liu | person_overseas | sim | — |
| ChenHsuan_Lin | Chen-Hsuan Lin | person_overseas | sim | — |
| Jack_Parker_Holder | Jack Parker-Holder | person_overseas | sim | — |
| Robin_Kahlow | Robin Kahlow | person_overseas | sim | — |
| Google_DeepMind | Google DeepMind | company_overseas | sim | — |
| NVIDIA | NVIDIA 英伟达 | company_overseas | sim | — |
| Runway | Runway | company_overseas | sim | — |
| OpenAI_Sora | OpenAI (Sora) | company_overseas | sim | — |
| DreamerV3 | DreamerV3 (2023) | milestone | sim | — |
| Dreamer4 | Dreamer 4 (2025) | milestone | sim | — |
| Genie3 | Genie 3 (2025) | milestone | sim | — |
| Cosmos | NVIDIA Cosmos (2025) | milestone | sim | — |
| GWM1 | Runway GWM-1 (2025) | milestone | sim | — |
| SIMA2 | SIMA 2 (2025) | milestone | sim | — |
| World_Models_Paper | 《World Models》(2018) | milestone | sim | — |
| Gen_Video_concept | 生成式世界模型 | tech_concept | sim | — |
| Model_Based_RL | 基于模型的RL | tech_concept | sim | — |
| PhysAI_Infra | 物理AI基础设施 | tech_concept | sim | — |
| Karl_Friston | Karl Friston | person_overseas | active_inf | ✅ |
| VERSES_AI | VERSES AI | company_overseas | active_inf | — |
| FEP | 自由能原理 FEP (2006) | milestone | active_inf | — |
| AXIOM | AXIOM 系统 | milestone | active_inf | — |
| Genius | Genius (2025) | milestone | active_inf | — |
| Active_Inference | 主动推理 | tech_concept | active_inf | — |
