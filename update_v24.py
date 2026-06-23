#!/usr/bin/env python3
"""v24 增量更新：张迪（可灵AI→阿里HappyHorse）+ 关联节点"""
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
# 1. 人物
# ═══════════════════════════════════════════════════════════════
print("\n=== 人物节点 ===")

add_node("Zhang_Di",
    "张迪 Zhang Di",
    "person_overseas", "sim",
    "上海交大计算机本硕（2010）。被称为「可灵之父」。"
    "2010-2020：阿里巴巴，阿里妈妈大数据与ML工程架构负责人。"
    "2020-2025.8：快手技术副总裁，大模型与多媒体技术团队负责人，"
    "主导可灵AI从0到1（30+版本迭代，4500万用户，累计生成2亿视频/4亿图片）。"
    "2025.9：短暂加入B站任技术条线负责人（不足3月）。"
    "2025.11：回归阿里，淘天集团未来生活实验室负责人（P11），向CTO郑波汇报。"
    "2026.4：仅用5个月打造HappyHorse-1.0，登顶AI Video Arena双榜。",
    bold=True
)

# ═══════════════════════════════════════════════════════════════
# 2. 产品/里程碑
# ═══════════════════════════════════════════════════════════════
print("\n=== 产品/里程碑节点 ===")

add_node("Kling",
    "可灵AI Kling (2024.6)\\n全球首个用户可用DiT视频模型\\n4500万用户",
    "milestone", "sim",
    "快手推出，张迪主导研发。全球首个用户可用的DiT架构视频生成大模型。"
    "上线后30+版本迭代，2025年Q2营收超2.5亿元（环比增67%）。"
    "可灵2.0在Artificial Analysis图生视频赛道全球榜首。"
    "被视为中国视频生成大模型从学术Demo到亿级用户产品的关键里程碑。"
)

add_node("HappyHorse",
    "快乐马 HappyHorse-1.0\\n阿里AI视频生成 (2026.4)\\n150亿参数·AI Video Arena双榜登顶",
    "milestone", "sim",
    "阿里巴巴淘天集团未来生活实验室，张迪主导研发（仅5个月）。"
    "150亿参数，40层统一自注意力Transformer，将文本/视频/音频三种模态的Token放入同一序列联合建模。"
    "全球首个原生支持音视频联合生成的开源视频大模型，原生支持7种语言唇形同步。"
    "单张H100生成5秒1080p视频仅需约38秒（DMD-2蒸馏至8步去噪）。"
    "2026年4月匿名空降AI Video Arena文生视频+图生视频双榜登顶。"
    "定位电商视频生成、广告素材、短剧，通过阿里云百炼MaaS平台对外提供API。"
)

add_node("Alibaba",
    "阿里巴巴 Alibaba\\nATH 事业群 (2026)\\nAI视频+世界模型双线布局",
    "company_overseas", "sim",
    "阿里巴巴集团。2026年3月成立ATH（Alibaba Token Hub）事业群，CEO吴泳铭亲自挂帅，"
    "整合通义实验室、MaaS业务线、千问事业部等五大板块。"
    "AI视频/世界模型双线并行：HappyHorse（视频生成，张迪主导）+ HappyOyster（可交互AI世界，对标Genie 3）。"
    "依托淘天体系海量商品数据和交易闭环，将AI视频/世界模型嵌入电商操作系统。"
)

# ═══════════════════════════════════════════════════════════════
# 3. 边
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增关系边 ===")

# ── 张迪 → 产品 ──
add_edge("Zhang_Di", "Kling", "maintainer", "技术副总裁/可灵AI技术负责人 (2020-2025)", "tier1")
add_edge("Zhang_Di", "HappyHorse", "maintainer", "核心技术及研发负责人 (2025.11至今)", "tier1")
add_edge("Zhang_Di", "HappyOyster", "maintainer", "ATH 创新事业部 / 可交互AI世界 (2025.11至今)", "tier1")

# ── 张迪 → 阿里 ──
add_edge("Zhang_Di", "Alibaba", "employed", "淘天集团未来生活实验室负责人/P11 (2025.11至今)", "tier1")

# ── 阿里 → 产品 ──
add_edge("Alibaba", "HappyHorse", "maintainer", "淘天集团未来生活实验室出品", "tier1")
add_edge("Alibaba", "HappyOyster", "maintainer", "ATH创新事业部出品 / 可交互AI世界", "tier1")

# ── 产品关联 ──
add_edge("Kling", "HappyHorse", "related", "张迪两个时代的作品：可灵→快乐马", "tier2")
add_edge("HappyHorse", "HappyOyster", "related", "同为阿里ATH体系 / 视频生成+世界模型双线", "tier2")

# ── 世界模型连接 ──
add_edge("Zhang_Di", "Model_Based_RL", "maintainer", "视频生成大模型→世界模型基础设施", "tier2")
add_edge("Kling", "Model_Based_RL", "evolution", "DiT视频生成→世界模型视觉基础", "tier2")
add_edge("HappyHorse", "Model_Based_RL", "evolution", "原生多模态联合建模→世界模型感知", "tier2")

# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 28
data["meta"]["updated"] = "2026-05-26"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v28: 张迪(可灵AI→阿里HappyHorse)+可灵Kling+快乐马HappyHorse+阿里巴巴公司节点，打通快手视频生成→阿里世界模型人才流动链")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v24 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
for n in new_nodes_added:
    print(f"    - {n}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
