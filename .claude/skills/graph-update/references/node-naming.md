# 节点 ID 和 Name 命名规则

> 本文档定义新节点的 `id` 和 `name` 字段格式。新建节点时必须参照，确保与已有 569 个节点风格一致。

## ID 格式

### Person ID

**格式**：`名_姓`（英文名用下划线分隔，无空格、无连字符）

**中国人姓名**（姓在前）：
- 单名：`姓_名` → `Zhang_Di`, `Wang_Hao`, `Li_Fei`
- 双名：`姓_名名` → `Wang_Guangrun`, `Chen_Boyuan`, `Liu_Songming`
- 原则：姓在前，不带空格

**外国人姓名**（名在前）：
- 单名：`名_姓` → `Yann_LeCun`, `Judea_Pearl`, `Andrew_Dai`
- 复姓/特殊姓：`名_复姓` → `Christopher_Longuet_Higgins`
- 音译中文名：同中国人规则 → `FeiFei_Li`, `Jiajun_Wu`

**不确定姓名顺序时**：
- 华人/亚裔血统 → 姓在名前（`Chen_Boyuan`）
- 非华人 → 名在姓前（`Jim_Fan`）
- 实在不确定 → 用全名中最常用的形式，保持一致

### Company ID

**格式**：英文名 + 下划线分隔

| 公司类型 | ID 示例 | Name 示例 |
|---------|---------|-----------|
| 纯英文公司 | `NVIDIA`, `Tesla` | `"NVIDIA 英伟达"` |
| 含空格英文名 | `World_Labs`, `Meta_FAIR` | `"World Labs"`, `"Meta FAIR"` |
| 中国公司（有英文名） | `WeRide`, `Agibot` | `"文远知行 WeRide"` |
| 中国公司（拼音） | `Xpeng`, `LiAuto` | `"小鹏汽车 Xpeng Motors"` |
| 中国公司（英文翻译） | `Inverse_Matrix` | `"逆矩阵科技 Inverse Matrix"` |
| 实验室/机构 | `OpenDriveLab`, `Stanford_SVL` | `"OpenDriveLab 开放自动驾驶实验室"` |
| 首字母缩写 | `NVIDIA`, `FAIR` | 保留大写 |

**核心规则**：
1. 优先使用公司官方英文名
2. 多个单词用 `_` 连接（不用空格、不用连字符）
3. 缩写保留大写
4. 中国公司没有英文名时，用拼音

### Product/Paper ID

**格式**：最常用的缩写/代号

| 类型 | ID 示例 | Name 示例 |
|------|---------|-----------|
| 论文有缩写 | `V_JEPA2`, `I_JEPA` | `"V-JEPA 2 (2025)"` |
| 论文无缩写 | `World_Models_Paper` | `"World Models (2018)"` |
| 产品名 | `Cosmos`, `Kling` | `"NVIDIA Cosmos (2025)"` |
| 开源项目 | `PyTorch`, `Genesis_Engine` | `"Genesis Engine"` |
| 概念/术语 | `JEPA_concept`, `EBM_concept` | `"JEPA 联合嵌入预测架构"` |
| 版本号 | `DreamerV3`, `Genie2`, `Pi0_5` | `"Dreamer V3 (2023)"` |
| 多组件产品 | `Cosmos_Predict` | `"Cosmos Predict (2025)"` |

**核心规则**：
1. 用领域内最通行的缩写
2. 版本号跟在大版本后（`DreamerV3`，不是 `Dreamer_V3`）
3. 概念类加 `_concept` 后缀
4. 年份放入 name 而非 id

---

## ID 禁止事项

| ❌ 禁止 | ✅ 正确 |
|--------|--------|
| 中文作为 ID | `王昊` → `Wang_Hao` |
| ID 中有空格 | `World Labs` → `World_Labs` |
| ID 中有连字符（除非原缩写） | `V-JEPA2` → `V_JEPA2` |
| ID 以数字开头 | `3DGS` → `Gaussian_Splat` |
| ID 与已有节点重复 | 先查重再命名 |

---

## Name 格式

### 人物 name

| 人物类型 | 格式 | 示例 |
|---------|------|------|
| 中国大陆学者 | `"中文名 English_Name"` | `"张迪 Zhang Di"` |
| 海外华人（知名） | `"中文名 English_Name"` | `"李飞飞 Fei-Fei Li"` |
| 外国人 | `"English Name"` | `"Yann LeCun"` |
| 外国人（有中文名） | `"English Name 中文名"` | `"Yann LeCun 杨立昆"` |
| 外国人（有中文音译） | `"English Name"` | `"Judea Pearl"` |

### 公司/机构 name

| 机构类型 | 格式 | 示例 |
|---------|------|------|
| 中国公司 | `"中文名 English_Name"` | `"智元机器人 Agibot"` |
| 外国公司 | `"English_Name"` | `"NVIDIA"` |
| 研究机构 | `"中文名 English_Name"` | `"上海人工智能实验室 Shanghai AI Lab"` |

### 产品/论文 name

| 类型 | 格式 | 示例 |
|------|------|------|
| 论文 | `"缩写 (年份)"` | `"V-JEPA 2 (2025)"` |
| 产品 | `"产品名 (发布年份)"` | `"NVIDIA Cosmos (2025)"` |
| 概念 | `"中文名 English_Name"` | `"联合嵌入预测架构 JEPA"` |

---

## 快速参考：已有节点 ID 模式

从现有 569 个节点中提取的典型 ID 模式：

```
Person:   Yann_LeCun, FeiFei_Li, Jim_Fan, Zhang_Di, Chen_Boyuan
Company:  NVIDIA, Meta_FAIR, World_Labs, Tesla, Waabi, WeRide, Agibot
Product:  Cosmos, V_JEPA2, DreamerV3, Genie1, Kling, I_JEPA, DiT_concept
```
