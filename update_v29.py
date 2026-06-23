#!/usr/bin/env python3
"""v29 增量更新：破壳机器人(许华哲新创/家庭具身世界模型)"""
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
# 1. 公司节点
# ═══════════════════════════════════════════════════════════════
print("\n=== 公司节点 ===")

add_node("PokeRobot",
    "破壳 PokeRobot\\n通用家庭机器人 (2026.3)\\n天使轮数千万美元",
    "company_overseas", "sim",
    "2026年3月由清华助理教授许华哲创立于北京。定位C端家庭机器人——"
    "「会主动干活的家庭成员」，能完成洗衣收纳、精细清洁、多步骤家务串联。"
    "技术路线放弃主流VLA架构，采用UAG架构构建端到端「视频→动作」世界模型，"
    "第一代32B参数具身世界模型已完成首轮训练，RL贯穿预训练与部署全流程。"
    "天使轮数千万美元：云启资本领投，顺为资本/小米战投/弘晖基金/"
    "百度风投/英诺天使/水木清华校友基金跟投，星海图种子轮孵化投资。"
    "许华哲激进判断：两年内中国将出现可用的家庭机器人。"
)

# ═══════════════════════════════════════════════════════════════
# 2. 新增边
# ═══════════════════════════════════════════════════════════════
print("\n=== 新增关系边 ===")

add_edge("Xu_Huazhe", "PokeRobot", "founded",
    "创始人兼CEO (2026.3至今) / 离开星海图独立创业", "tier1")

add_edge("Xu_Huazhe", "Galbot", "employed",
    "前联合创始人兼首席科学家 (2023-2026.2)", "tier1")

add_edge("PokeRobot", "Galbot", "related",
    "星海图内部孵化+种子轮投资 / 许华哲离职创业", "tier2")

add_edge("PokeRobot", "Model_Based_RL", "maintainer",
    "「视频→动作」世界模型 / 32B具身世界模型", "tier1")

# ═══════════════════════════════════════════════════════════════
# 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 33
data["meta"]["updated"] = "2026-05-26"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v33: 破壳机器人PokeRobot(许华哲2026年新创/C端家庭机器人/视频→动作世界模型/天使轮数千万美元/星海图孵化+小米战投)")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v29 更新完成！")
print(f"  新增节点: {len(new_nodes_added)}")
for n in new_nodes_added:
    print(f"    - {n}")
print(f"  新增边:   {len(new_edges_added)}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
