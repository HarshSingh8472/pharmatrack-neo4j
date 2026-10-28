import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import os

output_dir = r"C:\Users\as174\OneDrive\Desktop\mini_project_adb\pharmatrack-neo4j\diagrams"
os.makedirs(output_dir, exist_ok=True)

# -------------------------------------------------------------
# DIAGRAM 1: GRAPH SCHEMA / DATA MODEL
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
G_schema = nx.DiGraph()

nodes_schema = {
    "Supplier": {"color": "#2ecc71", "pos": (0, 2)},
    "Manufacturer": {"color": "#3498db", "pos": (2.5, 2)},
    "Batch": {"color": "#e67e22", "pos": (5, 2)},
    "Inspector": {"color": "#f1c40f", "pos": (5, 3.8)},
    "Warehouse": {"color": "#9b59b6", "pos": (7.5, 2)},
    "Pharmacy": {"color": "#1abc9c", "pos": (10, 2)},
}

for node, data in nodes_schema.items():
    G_schema.add_node(node)

schema_edges = [
    ("Supplier", "Manufacturer", "SUPPLIED\n[ingredient, date]"),
    ("Manufacturer", "Batch", "PRODUCED\n[mfgDate, units]"),
    ("Manufacturer", "Warehouse", "SHIPPED\n[tempCelsius, carrier]"),
    ("Warehouse", "Batch", "STORED\n[shelfZone, entryDate]"),
    ("Warehouse", "Pharmacy", "DELIVERED_TO\n[qty, invoiceNo]"),
    ("Pharmacy", "Batch", "DISPENSES\n[batchId]"),
    ("Inspector", "Batch", "AUDITED\n[outcome, certNo]"),
]

for u, v, lbl in schema_edges:
    G_schema.add_edge(u, v, label=lbl)

pos = {n: d["pos"] for n, d in nodes_schema.items()}
node_colors = [nodes_schema[n]["color"] for n in G_schema.nodes()]

nx.draw_networkx_nodes(G_schema, pos, node_color=node_colors, node_size=3800, edgecolors="#2c3e50", linewidths=2, ax=ax)
nx.draw_networkx_labels(G_schema, pos, font_size=11, font_family="sans-serif", font_weight="bold", font_color="#ffffff", ax=ax)

# Draw curved edges
edge_list = list(G_schema.edges())
nx.draw_networkx_edges(G_schema, pos, edgelist=edge_list, edge_color="#34495e", arrowsize=20, arrowstyle="-|>", node_size=3800, width=2, connectionstyle="arc3,rad=0.1", ax=ax)

# Edge labels
edge_labels = {(u, v): d["label"] for u, v, d in G_schema.edges(data=True)}
nx.draw_networkx_edge_labels(G_schema, pos, edge_labels=edge_labels, font_size=8, font_family="sans-serif", font_color="#2c3e50", bbox=dict(boxstyle="round,pad=0.2", fc="#ffffff", ec="#bdc3c7", lw=1))

ax.set_title("PharmaTrack: Graph Database Schema Architecture", fontsize=15, fontweight="bold", pad=25, color="#1a252f")
ax.axis("off")
plt.tight_layout()
schema_path = os.path.join(output_dir, "graph_schema.png")
plt.savefig(schema_path, bbox_inches="tight")
plt.close()
print("Saved schema diagram to:", schema_path)

# -------------------------------------------------------------
# DIAGRAM 2: FULL SEEDED GRAPH NETWORK
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
G_full = nx.DiGraph()

full_nodes = {
    # Suppliers
    "SUP-01\nApex BioChem": {"type": "Supplier", "color": "#2ecc71", "pos": (0, 3.5)},
    "SUP-02\nGlobal Solvents": {"type": "Supplier", "color": "#2ecc71", "pos": (0, 1.5)},
    "SUP-03\nRogue Chemical": {"type": "Supplier", "color": "#e74c3c", "pos": (0, -0.5)},
    # Manufacturers
    "MFG-01\nPharmaCore Labs": {"type": "Manufacturer", "color": "#3498db", "pos": (3, 3.5)},
    "MFG-02\nHealthGen": {"type": "Manufacturer", "color": "#3498db", "pos": (3, 1.0)},
    # Batches
    "BATCH-A1\nAmoxicillin": {"type": "Batch", "color": "#e67e22", "pos": (6, 4.0)},
    "BATCH-B2\nInsulin": {"type": "Batch", "color": "#e67e22", "pos": (6, 1.5)},
    "BATCH-FAKE-X9\nCounterfeit": {"type": "Batch", "color": "#e74c3c", "pos": (6, -1.0)},
    # Inspector
    "INS-01\nDr. Elena": {"type": "Inspector", "color": "#f1c40f", "pos": (6, 5.8)},
    # Warehouses
    "WH-CENTRAL\nEuro Hub": {"type": "Warehouse", "color": "#9b59b6", "pos": (9, 3.5)},
    "WH-SOUTH\nMetro Cold": {"type": "Warehouse", "color": "#9b59b6", "pos": (9, 1.5)},
    # Pharmacies
    "PHARM-01\nCity Central": {"type": "Pharmacy", "color": "#1abc9c", "pos": (12, 4.0)},
    "PHARM-02\nSt. Jude Hosp": {"type": "Pharmacy", "color": "#1abc9c", "pos": (12, 1.5)},
    "PHARM-03\nDiscount Meds": {"type": "Pharmacy", "color": "#e74c3c", "pos": (12, -1.0)},
}

for n, d in full_nodes.items():
    G_full.add_node(n, **d)

full_edges = [
    ("SUP-01\nApex BioChem", "MFG-01\nPharmaCore Labs", "SUPPLIED"),
    ("SUP-02\nGlobal Solvents", "MFG-02\nHealthGen", "SUPPLIED"),
    ("MFG-01\nPharmaCore Labs", "BATCH-A1\nAmoxicillin", "PRODUCED"),
    ("MFG-02\nHealthGen", "BATCH-B2\nInsulin", "PRODUCED"),
    ("MFG-01\nPharmaCore Labs", "WH-CENTRAL\nEuro Hub", "SHIPPED (4.5°C)"),
    ("MFG-02\nHealthGen", "WH-SOUTH\nMetro Cold", "SHIPPED (3.8°C)"),
    ("WH-CENTRAL\nEuro Hub", "BATCH-A1\nAmoxicillin", "STORED"),
    ("WH-SOUTH\nMetro Cold", "BATCH-B2\nInsulin", "STORED"),
    ("WH-CENTRAL\nEuro Hub", "PHARM-01\nCity Central", "DELIVERED"),
    ("WH-SOUTH\nMetro Cold", "PHARM-02\nSt. Jude Hosp", "DELIVERED"),
    ("PHARM-01\nCity Central", "BATCH-A1\nAmoxicillin", "DISPENSES"),
    ("PHARM-02\nSt. Jude Hosp", "BATCH-B2\nInsulin", "DISPENSES"),
    ("PHARM-03\nDiscount Meds", "BATCH-FAKE-X9\nCounterfeit", "DISPENSES [UNVERIFIED]"),
    ("INS-01\nDr. Elena", "BATCH-A1\nAmoxicillin", "AUDITED (PASSED)"),
    ("INS-01\nDr. Elena", "BATCH-B2\nInsulin", "AUDITED (PASSED)"),
]

for u, v, lbl in full_edges:
    G_full.add_edge(u, v, label=lbl)

pos_full = {n: d["pos"] for n, d in full_nodes.items()}
colors_full = [d["color"] for n, d in full_nodes.items()]

nx.draw_networkx_nodes(G_full, pos_full, node_color=colors_full, node_size=2800, edgecolors="#2c3e50", linewidths=1.8, ax=ax)
nx.draw_networkx_labels(G_full, pos_full, font_size=8, font_family="sans-serif", font_weight="bold", font_color="#ffffff", ax=ax)

nx.draw_networkx_edges(G_full, pos_full, edge_color="#7f8c8d", arrowsize=16, arrowstyle="-|>", node_size=2800, width=1.5, connectionstyle="arc3,rad=0.08", ax=ax)
edge_labels_full = {(u, v): d["label"] for u, v, d in G_full.edges(data=True)}
nx.draw_networkx_edge_labels(G_full, pos_full, edge_labels=edge_labels_full, font_size=7, font_family="sans-serif", font_color="#2c3e50", bbox=dict(boxstyle="round,pad=0.15", fc="#f8f9fa", ec="#bdc3c7", lw=0.8))

ax.set_title("Neo4j Live Instance: PharmaTrack Graph Visualization Output", fontsize=15, fontweight="bold", pad=20, color="#1a252f")
ax.axis("off")
plt.tight_layout()
network_path = os.path.join(output_dir, "full_graph_network.png")
plt.savefig(network_path, bbox_inches="tight")
plt.close()
print("Saved full network diagram to:", network_path)

# -------------------------------------------------------------
# DIAGRAM 3: PROVENANCE TRACE (QUERY 1 RESULT)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
G_trace = nx.DiGraph()

trace_nodes = {
    "Supplier:\nApex BioChem": {"pos": (0, 1), "color": "#2ecc71"},
    "Manufacturer:\nPharmaCore": {"pos": (2.5, 1), "color": "#3498db"},
    "Batch:\nBATCH-2026-A1": {"pos": (5, 1), "color": "#e67e22"},
    "Warehouse:\nEuro Hub": {"pos": (7.5, 1), "color": "#9b59b6"},
    "Pharmacy:\nCity Central": {"pos": (10, 1), "color": "#1abc9c"},
}

for n, d in trace_nodes.items():
    G_trace.add_node(n, **d)

trace_edges = [
    ("Supplier:\nApex BioChem", "Manufacturer:\nPharmaCore", "SUPPLIED\n[Active Powder]"),
    ("Manufacturer:\nPharmaCore", "Batch:\nBATCH-2026-A1", "PRODUCED\n[50k units]"),
    ("Warehouse:\nEuro Hub", "Batch:\nBATCH-2026-A1", "STORED\n[Cold-A2]"),
    ("Warehouse:\nEuro Hub", "Pharmacy:\nCity Central", "DELIVERED_TO\n[5k units]"),
]

for u, v, lbl in trace_edges:
    G_trace.add_edge(u, v, label=lbl)

pos_trace = {n: d["pos"] for n, d in trace_nodes.items()}
colors_trace = [d["color"] for n, d in trace_nodes.items()]

nx.draw_networkx_nodes(G_trace, pos_trace, node_color=colors_trace, node_size=3400, edgecolors="#1e272e", linewidths=2, ax=ax)
nx.draw_networkx_labels(G_trace, pos_trace, font_size=8.5, font_family="sans-serif", font_weight="bold", font_color="#ffffff", ax=ax)
nx.draw_networkx_edges(G_trace, pos_trace, edge_color="#2c3e50", arrowsize=18, arrowstyle="-|>", node_size=3400, width=2.5, connectionstyle="arc3,rad=0.08", ax=ax)

edge_labels_trace = {(u, v): d["label"] for u, v, d in G_trace.edges(data=True)}
nx.draw_networkx_edge_labels(G_trace, pos_trace, edge_labels=edge_labels_trace, font_size=7.5, font_color="#2c3e50", bbox=dict(boxstyle="round,pad=0.2", fc="#ffffff", ec="#bdc3c7", lw=1))

ax.set_title("Cypher Query 1: End-to-End Batch Provenance Trace Output", fontsize=13, fontweight="bold", pad=20, color="#1a252f")
ax.axis("off")
plt.tight_layout()
trace_path = os.path.join(output_dir, "provenance_trace.png")
plt.savefig(trace_path, bbox_inches="tight")
plt.close()
print("Saved provenance trace diagram to:", trace_path)
