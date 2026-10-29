import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

output_dir = r"C:\Users\as174\OneDrive\Desktop\mini_project_adb\pharmatrack-neo4j\diagrams"
os.makedirs(output_dir, exist_ok=True)

# Common styling: Neo4j Browser dark theme
NEO4J_DARK = "#2a2c33"
NEO4J_PANEL = "#202226"
NEO4J_TEXT = "#e1e4e8"
NEO4J_LINE = "#6c757d"

# ==============================================================================
# DIAGRAM 1: GRAPH SCHEMA / DATA MODEL (ZERO OVERLAP)
# ==============================================================================
fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300, facecolor=NEO4J_DARK)
ax.set_facecolor(NEO4J_DARK)

# Draw Neo4j Browser Top Header
header_rect = patches.Rectangle((0, 7.8), 15, 0.7, facecolor=NEO4J_PANEL, edgecolor="#3c3f47", lw=1)
ax.add_patch(header_rect)
ax.text(0.4, 8.15, "neo4j$ CALL db.schema.visualization()", color="#569cd6", fontsize=11, fontfamily="monospace", va="center", weight="bold")
ax.text(14.5, 8.15, "SCHEMA MODEL", color="#4ec9b0", fontsize=9, fontfamily="sans-serif", va="center", ha="right", weight="bold")

schema_nodes = [
    {"label": "Supplier", "color": "#10b981", "x": 1.8, "y": 4.5, "props": "id, name,\ncountry, certified"},
    {"label": "Manufacturer", "color": "#3b82f6", "x": 4.8, "y": 4.5, "props": "id, name,\ncity, gmpCompliant"},
    {"label": "Batch", "color": "#f59e0b", "x": 8.0, "y": 4.5, "props": "batchId, drugName,\nmfgDate, expiryDate"},
    {"label": "Inspector", "color": "#eab308", "x": 8.0, "y": 7.0, "props": "id, name,\nagency"},
    {"label": "Warehouse", "color": "#8b5cf6", "x": 11.0, "y": 4.5, "props": "id, name,\ncity, coldChain"},
    {"label": "Pharmacy", "color": "#06b6d4", "x": 13.5, "y": 4.5, "props": "id, name,\nlicenseNo, city"}
]

# Draw nodes
for n in schema_nodes:
    # Outer glow
    circle_glow = patches.Circle((n["x"], n["y"]), 0.85, facecolor="none", edgecolor=n["color"], lw=2.5, alpha=0.3)
    ax.add_patch(circle_glow)
    # Circle node
    circle = patches.Circle((n["x"], n["y"]), 0.75, facecolor=n["color"], edgecolor="#ffffff", lw=2)
    ax.add_patch(circle)
    # Label inside circle
    ax.text(n["x"], n["y"], n["label"], color="#ffffff", fontsize=10.5, weight="bold", ha="center", va="center", fontfamily="sans-serif")
    # Properties badge below circle
    ax.text(n["x"], n["y"] - 1.25, n["props"], color="#9ca3af", fontsize=7.5, ha="center", va="top", fontfamily="monospace",
            bbox=dict(boxstyle="round,pad=0.3", fc="#1e222b", ec="#374151", lw=1))

schema_edges = [
    # (x1, y1, x2, y2, label, label_x, label_y)
    (1.8 + 0.75, 4.5, 4.8 - 0.75, 4.5, "[:SUPPLIED]", 3.3, 4.8),
    (4.8 + 0.75, 4.5, 8.0 - 0.75, 4.5, "[:PRODUCED]", 6.4, 4.8),
    (8.0, 7.0 - 0.75, 8.0, 4.5 + 0.75, "[:AUDITED]", 8.7, 5.7),
    (4.8, 4.5 - 0.75, 11.0, 4.5 - 0.75, "[:SHIPPED {tempCelsius}]", 7.9, 2.2), # Curved downward
    (11.0 - 0.75, 4.5, 8.0 + 0.75, 4.5, "[:STORED]", 9.5, 4.8),
    (11.0 + 0.75, 4.5, 13.5 - 0.75, 4.5, "[:DELIVERED_TO]", 12.25, 4.8),
    (13.5, 4.5 + 0.75, 8.0, 4.5 + 0.75, "[:DISPENSES]", 10.7, 6.4) # Curved upward
]

# Draw straight arrows
for e in [schema_edges[0], schema_edges[1], schema_edges[2], schema_edges[4], schema_edges[5]]:
    ax.annotate("", xy=(e[2], e[3]), xytext=(e[0], e[1]),
                arrowprops=dict(arrowstyle="-|>", color="#94a3b8", lw=2, mutation_scale=18))
    ax.text(e[5], e[6], e[4], color="#38bdf8", fontsize=8.5, weight="bold", ha="center", va="center", fontfamily="monospace",
            bbox=dict(boxstyle="round,pad=0.25", fc="#111827", ec="#38bdf8", lw=1))

# Draw curved SHIPPED arrow (Manufacturer -> Warehouse)
ax.annotate("", xy=(11.0 - 0.4, 4.5 - 0.7), xytext=(4.8 + 0.4, 4.5 - 0.7),
            arrowprops=dict(arrowstyle="-|>", color="#a78bfa", lw=2, mutation_scale=18, connectionstyle="arc3,rad=-0.35"))
ax.text(7.9, 2.4, "[:SHIPPED {tempCelsius, carrier}]", color="#c084fc", fontsize=8.5, weight="bold", ha="center", va="center", fontfamily="monospace",
        bbox=dict(boxstyle="round,pad=0.25", fc="#111827", ec="#a78bfa", lw=1))

# Draw curved DISPENSES arrow (Pharmacy -> Batch)
ax.annotate("", xy=(8.0 + 0.5, 4.5 + 0.6), xytext=(13.5 - 0.5, 4.5 + 0.6),
            arrowprops=dict(arrowstyle="-|>", color="#22d3ee", lw=2, mutation_scale=18, connectionstyle="arc3,rad=-0.3"))
ax.text(10.7, 6.3, "[:DISPENSES]", color="#22d3ee", fontsize=8.5, weight="bold", ha="center", va="center", fontfamily="monospace",
        bbox=dict(boxstyle="round,pad=0.25", fc="#111827", ec="#22d3ee", lw=1))

ax.set_xlim(0, 15)
ax.set_ylim(1.5, 8.5)
ax.axis("off")
plt.tight_layout()
schema_out = os.path.join(output_dir, "graph_schema.png")
plt.savefig(schema_out, bbox_inches="tight", facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()
print("Generated clean graph_schema.png")

# ==============================================================================
# DIAGRAM 2: FULL SEEDED GRAPH NETWORK (AUTHENTIC NEO4J BROWSER UI)
# ==============================================================================
fig, ax = plt.subplots(figsize=(16, 9.5), dpi=300, facecolor=NEO4J_DARK)
ax.set_facecolor(NEO4J_DARK)

# Neo4j Browser top bar
top_bar = patches.Rectangle((0, 8.8), 16, 0.7, facecolor=NEO4J_PANEL, edgecolor="#3c3f47", lw=1)
ax.add_patch(top_bar)
ax.text(0.4, 9.15, "neo4j$ MATCH (n) OPTIONAL MATCH (n)-[r]->(m) RETURN n, r, m", color="#569cd6", fontsize=11, fontfamily="monospace", va="center", weight="bold")
ax.text(15.6, 9.15, "15 nodes, 16 relationships", color="#4ec9b0", fontsize=9.5, fontfamily="sans-serif", va="center", ha="right", weight="bold")

# Nodes positioned with wide breathing space
nodes_full = [
    # Suppliers (Left)
    {"id": "SUP1", "name": "Apex BioChem", "sub": "Supplier", "color": "#10b981", "x": 1.8, "y": 6.8},
    {"id": "SUP2", "name": "Global Solvents", "sub": "Supplier", "color": "#10b981", "x": 1.8, "y": 4.5},
    {"id": "SUP3", "name": "Rogue Chemical", "sub": "Supplier", "color": "#ef4444", "x": 1.8, "y": 2.2},

    # Manufacturers (Mid-Left)
    {"id": "MFG1", "name": "PharmaCore", "sub": "Manufacturer", "color": "#3b82f6", "x": 5.0, "y": 6.8},
    {"id": "MFG2", "name": "HealthGen", "sub": "Manufacturer", "color": "#3b82f6", "x": 5.0, "y": 3.8},

    # Inspector (Top Center)
    {"id": "INS1", "name": "Dr. Elena", "sub": "Inspector", "color": "#eab308", "x": 8.5, "y": 8.0},

    # Batches (Center)
    {"id": "B1", "name": "Amoxicillin\nA1", "sub": "Batch: Active", "color": "#f59e0b", "x": 8.5, "y": 5.8},
    {"id": "B2", "name": "Insulin\nB2", "sub": "Batch: Active", "color": "#f59e0b", "x": 8.5, "y": 3.8},
    {"id": "B3", "name": "Fake Insulin\nX9", "sub": "Batch: Counterfeit", "color": "#ef4444", "x": 8.5, "y": 1.6},

    # Warehouses (Mid-Right)
    {"id": "WH1", "name": "Euro Hub", "sub": "Warehouse", "color": "#8b5cf6", "x": 12.0, "y": 6.8},
    {"id": "WH2", "name": "Metro Cold", "sub": "Warehouse", "color": "#8b5cf6", "x": 12.0, "y": 3.8},

    # Pharmacies (Right)
    {"id": "PH1", "name": "City Central", "sub": "Pharmacy", "color": "#06b6d4", "x": 14.8, "y": 6.8},
    {"id": "PH2", "name": "St. Jude Hosp", "sub": "Pharmacy", "color": "#06b6d4", "x": 14.8, "y": 3.8},
    {"id": "PH3", "name": "Discount Meds", "sub": "Pharmacy", "color": "#ef4444", "x": 14.8, "y": 1.6},
]

node_dict = {n["id"]: n for n in nodes_full}

edges_full = [
    ("SUP1", "MFG1", "SUPPLIED"),
    ("SUP2", "MFG2", "SUPPLIED"),
    ("SUP3", "MFG2", "SUPPLIED (Unverified)"),
    ("MFG1", "B1", "PRODUCED"),
    ("MFG2", "B2", "PRODUCED"),
    ("INS1", "B1", "AUDITED (Pass)"),
    ("INS1", "B2", "AUDITED (Pass)"),
    ("MFG1", "WH1", "SHIPPED (4.5°C)"),
    ("MFG2", "WH2", "SHIPPED (3.8°C)"),
    ("WH1", "B1", "STORED"),
    ("WH2", "B2", "STORED"),
    ("WH1", "PH1", "DELIVERED_TO"),
    ("WH2", "PH2", "DELIVERED_TO"),
    ("PH1", "B1", "DISPENSES"),
    ("PH2", "B2", "DISPENSES"),
    ("PH3", "B3", "DISPENSES (No Factory Pedigree!)")
]

# Draw edges first
for u, v, lbl in edges_full:
    n1 = node_dict[u]
    n2 = node_dict[v]
    
    # Calculate vector for arrow offset
    dx = n2["x"] - n1["x"]
    dy = n2["y"] - n1["y"]
    dist = (dx**2 + dy**2)**0.5
    if dist == 0: continue
    
    r = 0.55 # Node radius
    start_x = n1["x"] + dx * (r / dist)
    start_y = n1["y"] + dy * (r / dist)
    end_x = n2["x"] - dx * (r / dist)
    end_y = n2["y"] - dy * (r / dist)
    
    edge_col = "#ef4444" if "No Factory" in lbl or "Unverified" in lbl else "#64748b"
    ax.annotate("", xy=(end_x, end_y), xytext=(start_x, start_y),
                arrowprops=dict(arrowstyle="-|>", color=edge_col, lw=1.6, mutation_scale=14))
    
    mid_x = (start_x + end_x) / 2
    mid_y = (start_y + end_y) / 2
    # Slight perpendicular offset for label readability
    lbl_color = "#fca5a5" if "No Factory" in lbl else "#94a3b8"
    ax.text(mid_x, mid_y + 0.16, lbl, color=lbl_color, fontsize=6.8, weight="bold", ha="center", va="center",
            fontfamily="sans-serif", bbox=dict(boxstyle="round,pad=0.15", fc="#111827", ec=edge_col, lw=0.6, alpha=0.9))

# Draw nodes on top
for n in nodes_full:
    # Outer glow
    circle_glow = patches.Circle((n["x"], n["y"]), 0.62, facecolor="none", edgecolor=n["color"], lw=2, alpha=0.35)
    ax.add_patch(circle_glow)
    # Circle body
    circle = patches.Circle((n["x"], n["y"]), 0.52, facecolor=n["color"], edgecolor="#ffffff", lw=1.5)
    ax.add_patch(circle)
    # Text inside circle
    ax.text(n["x"], n["y"], n["name"], color="#ffffff", fontsize=7.5, weight="bold", ha="center", va="center", fontfamily="sans-serif")
    # Subtitle / Type below circle
    ax.text(n["x"], n["y"] - 0.72, n["sub"], color="#cbd5e1", fontsize=6.5, ha="center", va="top", fontfamily="monospace")

ax.set_xlim(0.5, 16)
ax.set_ylim(0.5, 9.6)
ax.axis("off")
plt.tight_layout()
net_out = os.path.join(output_dir, "full_graph_network.png")
plt.savefig(net_out, bbox_inches="tight", facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()
print("Generated clean full_graph_network.png")

# ==============================================================================
# DIAGRAM 3: PROVENANCE TRACE (QUERY 1 VISUALIZATION)
# ==============================================================================
fig, ax = plt.subplots(figsize=(15, 5.5), dpi=300, facecolor=NEO4J_DARK)
ax.set_facecolor(NEO4J_DARK)

# Top Bar
top_bar = patches.Rectangle((0, 4.8), 15, 0.7, facecolor=NEO4J_PANEL, edgecolor="#3c3f47", lw=1)
ax.add_patch(top_bar)
ax.text(0.3, 5.15, "neo4j$ MATCH path=(s:Supplier)-[:SUPPLIED]->(m)-[:PRODUCED]->(b:Batch {batchId:'BATCH-2026-A1'})<-[:STORED]-(w)-[:DELIVERED_TO]->(p) RETURN path", color="#569cd6", fontsize=9.5, fontfamily="monospace", va="center", weight="bold")
ax.text(14.7, 5.15, "1 path (5 nodes, 4 relationships)", color="#4ec9b0", fontsize=9, fontfamily="sans-serif", va="center", ha="right", weight="bold")

trace_nodes = [
    {"name": "Apex BioChem", "type": "Supplier", "sub": "Germany\n(Certified: True)", "color": "#10b981", "x": 1.5, "y": 2.5},
    {"name": "PharmaCore Labs", "type": "Manufacturer", "sub": "Basel\n(GMP Compliant)", "color": "#3b82f6", "x": 4.5, "y": 2.5},
    {"name": "Amoxicillin 500mg", "type": "Batch", "sub": "BATCH-2026-A1\n(Active / Safe)", "color": "#f59e0b", "x": 7.5, "y": 2.5},
    {"name": "Euro Hub Logistics", "type": "Warehouse", "sub": "Frankfurt\n(Cold-Chain: Yes)", "color": "#8b5cf6", "x": 10.5, "y": 2.5},
    {"name": "City Central", "type": "Pharmacy", "sub": "Frankfurt\n(LIC-8821)", "color": "#06b6d4", "x": 13.5, "y": 2.5}
]

# Draw nodes
for n in trace_nodes:
    circle_glow = patches.Circle((n["x"], n["y"]), 0.78, facecolor="none", edgecolor=n["color"], lw=2.5, alpha=0.35)
    ax.add_patch(circle_glow)
    circle = patches.Circle((n["x"], n["y"]), 0.68, facecolor=n["color"], edgecolor="#ffffff", lw=2)
    ax.add_patch(circle)
    ax.text(n["x"], n["y"], n["name"], color="#ffffff", fontsize=8.2, weight="bold", ha="center", va="center", fontfamily="sans-serif")
    ax.text(n["x"], n["y"] - 1.05, n["sub"], color="#cbd5e1", fontsize=7.2, ha="center", va="top", fontfamily="monospace")

trace_arrows = [
    (1.5 + 0.68, 2.5, 4.5 - 0.68, 2.5, "[:SUPPLIED]\n[Lot: LOT-901]", 3.0, 3.2),
    (4.5 + 0.68, 2.5, 7.5 - 0.68, 2.5, "[:PRODUCED]\n[50,000 units]", 6.0, 3.2),
    (10.5 - 0.68, 2.5, 7.5 + 0.68, 2.5, "[:STORED]\n[Zone: Cold-A2]", 9.0, 3.2),
    (10.5 + 0.68, 2.5, 13.5 - 0.68, 2.5, "[:DELIVERED_TO]\n[5,000 units]", 12.0, 3.2),
]

for x1, y1, x2, y2, lbl, lx, ly in trace_arrows:
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="#38bdf8", lw=2.2, mutation_scale=18))
    ax.text(lx, ly, lbl, color="#38bdf8", fontsize=7.8, weight="bold", ha="center", va="center", fontfamily="monospace",
            bbox=dict(boxstyle="round,pad=0.25", fc="#111827", ec="#38bdf8", lw=1))

ax.set_xlim(0, 15)
ax.set_ylim(0.8, 5.5)
ax.axis("off")
plt.tight_layout()
trace_out = os.path.join(output_dir, "provenance_trace.png")
plt.savefig(trace_out, bbox_inches="tight", facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()
print("Generated clean provenance_trace.png")
