#!/usr/bin/env python3
"""v14 增量更新：合并 NVIDIA_Spatial_Intel_Lab → NVIDIA，清理冗余描述"""
import json, os, subprocess

SRC = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SRC, "World_Models_data.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

changes = []

# ═══════════════════════════════════════════════════════════════
# 1. 更新 Ruilong_Li 的 label 和 description
# ═══════════════════════════════════════════════════════════════
for node in data["nodes"]:
    if node["id"] == "Ruilong_Li":
        old_label = node["label"]
        node["label"] = "Ruilong Li\nNVIDIA 研究科学家"
        changes.append(f"更新 Ruilong_Li label: '{old_label}' → '{node['label']}'")

        old_desc = node["description"]
        node["description"] = "NVIDIA 研究科学家。gsplat、nerfacc和nerfstudio原初作者，推动3D Gaussian Splatting生态走向成熟。"
        changes.append(f"更新 Ruilong_Li description")
        break

# ═══════════════════════════════════════════════════════════════
# 2. 重定向边：NVIDIA_Spatial_Intel_Lab → NVIDIA
# ═══════════════════════════════════════════════════════════════
edges_to_remove = []
edges_to_add = []

for edge in data["edges"]:
    if edge["source"] == "NVIDIA_Spatial_Intel_Lab":
        edges_to_remove.append(edge)
        new_edge = edge.copy()
        new_edge["source"] = "NVIDIA"
        new_edge["label"] = "NVIDIA 孵化"
        edges_to_add.append(new_edge)
        changes.append(f"重定向边: NVIDIA_Spatial_Intel_Lab → {edge['target']} → NVIDIA → {edge['target']}")

    elif edge["target"] == "NVIDIA_Spatial_Intel_Lab":
        edges_to_remove.append(edge)
        new_edge = edge.copy()
        new_edge["target"] = "NVIDIA"
        edges_to_add.append(new_edge)
        changes.append(f"重定向边: {edge['source']} → NVIDIA_Spatial_Intel_Lab → {edge['source']} → NVIDIA")

for e in edges_to_remove:
    data["edges"].remove(e)
for e in edges_to_add:
    data["edges"].append(e)

# ═══════════════════════════════════════════════════════════════
# 3. 删除 NVIDIA_Spatial_Intel_Lab 节点
# ═══════════════════════════════════════════════════════════════
data["nodes"] = [n for n in data["nodes"] if n["id"] != "NVIDIA_Spatial_Intel_Lab"]
changes.append("删除节点: NVIDIA_Spatial_Intel_Lab")

# ═══════════════════════════════════════════════════════════════
# 4. 检查其他 NVIDIA 相关冗余
# ═══════════════════════════════════════════════════════════════
print("=== NVIDIA 相关节点筛查 ===")
nvidia_related = []
for node in data["nodes"]:
    desc = node.get("description", "")
    label = node.get("label", "")
    nid = node["id"]
    if "NVIDIA" in desc or "NVIDIA" in label or "nvidia" in nid.lower():
        nvidia_related.append(f"  [{node['type']}] {nid}: {label.split(chr(10))[0]}")

print(f"NVIDIA 相关节点 ({len(nvidia_related)}):")
for item in sorted(nvidia_related):
    print(item)

# ═══════════════════════════════════════════════════════════════
# 5. 保存 & 统计
# ═══════════════════════════════════════════════════════════════
data["meta"]["version"] = 16
data["meta"]["updated"] = "2026-05-25"
data["meta"]["node_count"] = len(data["nodes"])
data["meta"]["edge_count"] = len(data["edges"])
data["meta"]["changelog"].append("v16: 合并NVIDIA_Spatial_Intel_Lab→NVIDIA主节点，重定向3条边，更新Ruilong_Li描述，清理NVIDIA节点冗余")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"v14 更新完成！")
print(f"变更摘要:")
for c in changes:
    print(f"  - {c}")
print(f"  总节点数: {len(data['nodes'])}")
print(f"  总边数:   {len(data['edges'])}")
print(f"{'='*60}")

print("\n运行 rebuild_v4.py ...")
subprocess.run(["python", os.path.join(SRC, "rebuild_v4.py")])
