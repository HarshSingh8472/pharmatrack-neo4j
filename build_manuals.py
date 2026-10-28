import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_heading_with_spacing(doc, text, level=1):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    run = h.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.bold = True
    if level == 1:
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0x1a, 0x36, 0x5d) # Navy
    elif level == 2:
        run.font.size = Pt(12.5)
        run.font.color.rgb = RGBColor(0x2b, 0x6c, 0xb0) # Slate blue
    else:
        run.font.size = Pt(11.5)
        run.font.color.rgb = RGBColor(0x2d, 0x37, 0x48)
    return h

def add_body_p(doc, text, bold_prefix="", italic_note=""):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
    r_body = p.add_run(text)
    r_body.font.name = 'Times New Roman'
    r_body.font.size = Pt(11)
    if italic_note:
        r_it = p.add_run(italic_note)
        r_it.font.name = 'Times New Roman'
        r_it.font.size = Pt(10.5)
        r_it.font.italic = True
    return p

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F7FAFC")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(code_text.strip())
    r.font.name = 'Consolas'
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(0x1a, 0x20, 0x2c)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

# =============================================================
# BUILD EXP 10 MANUAL
# =============================================================
doc10_path = r"C:\Users\as174\OneDrive\Desktop\mini_project_adb\2026-27 ADB Exp 10 Manual.docx"
doc10 = Document(doc10_path)

# Clear existing body paragraphs after header info
for p in list(doc10.paragraphs):
    p._element.getparent().remove(p._element)

# Title Header
p_exp = doc10.add_paragraph()
p_exp.paragraph_format.space_before = Pt(0)
p_exp.paragraph_format.space_after = Pt(2)
p_exp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_exp.add_run("Experiment No. 10")
r.font.name = 'Times New Roman'
r.font.size = Pt(16)
r.font.bold = True

p_sub = doc10.add_paragraph()
p_sub.paragraph_format.space_after = Pt(14)
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_sub.add_run("MINI PROJECT - I : GRAPH DATABASE DESIGN & MODELING")
r.font.name = 'Times New Roman'
r.font.size = Pt(13)
r.font.bold = True
r.font.color.rgb = RGBColor(0x2b, 0x6c, 0xb0)

# 1. Problem Statement
add_heading_with_spacing(doc10, "1. Problem Statement", level=1)
add_body_p(doc10, 
    "In the global pharmaceutical industry, ensuring patient safety requires complete, immutable end-to-end traceability of prescription drug batches from active pharmaceutical ingredient (API) suppliers to factories, distribution depots, pharmacies, and healthcare clinics. According to the World Health Organization (WHO), counterfeit and substandard medications account for over $200 billion in illicit commerce annually, posing catastrophic public health hazards.",
    bold_prefix="Background & Industry Context: "
)
add_body_p(doc10, 
    "Traditional Relational Database Management Systems (RDBMS) model supply chains using highly normalized tabular schemas across separate tables (Suppliers, PurchaseOrders, ProductionBatches, Shipments, Warehouses, Dispensations). Answering vital traceability questions—such as 'Trace this exact blister pack back 6 tiers to identify the chemical lot and inspection status' or 'Identify all hospitals that received drugs from a contaminated manufacturer'—requires deeply nested, multi-table SQL JOIN operations and recursive Common Table Expressions (CTEs). As data volume expands, recursive relational queries suffer from exponential performance degradation (O(n^k)), high index-lookup latency, and brittle table joins.",
    bold_prefix="The Relational Database Bottleneck: "
)
add_body_p(doc10, 
    "To overcome these limitations, this project designs 'PharmaTrack'—a high-performance Graph Database system built on Neo4j. By utilizing native index-free adjacency, entities (Suppliers, Manufacturers, Batches, Warehouses, Pharmacies, Inspectors) are stored as nodes, while transactions (SUPPLIED, PRODUCED, SHIPPED, STORED, DELIVERED_TO, DISPENSES, AUDITED) are stored as direct physical relationship pointers. This allows provenance tracing, counterfeit isolation, and cold-chain temperature verification to execute in constant O(1) traversal time per relationship hop, regardless of total database size.",
    bold_prefix="The Graph Database Solution: "
)

# 2. Objectives
add_heading_with_spacing(doc10, "2. Objectives", level=1)
objectives = [
    ("Design a Graph Data Model: ", "Formulate a property graph schema that accurately represents physical supply chain tiers, intermediate custody handoffs, and regulatory oversight."),
    ("Establish Node & Edge Schemas: ", "Identify distinct node labels and rich property sets representing critical product attributes (batch numbers, expiry dates, dosage, dosage form) and logistics metrics (transit temperature, carrier, timestamps)."),
    ("Enable Rapid Provenance & Track-and-Trace: ", "Formulate traversable graph structures capable of tracing complete lineage from raw chemical supplier to dispensing pharmacy in a single query."),
    ("Implement Counterfeit & Anomaly Detection: ", "Structure the graph model to detect broken custody chains, unauthorized suppliers, and counterfeit drugs dispensed without valid manufacturer pedigree."),
    ("Cold-Chain Logistics Compliance: ", "Store and evaluate environmental telemetry (temperature logging) along shipping edges to flag compromised temperature-sensitive medications like Insulin.")
]
for pfx, desc in objectives:
    add_body_p(doc10, desc, bold_prefix=f"•  {pfx}")

# 3. Graph Schema / Model
add_heading_with_spacing(doc10, "3. Graph Schema / Model", level=1)
add_body_p(doc10, 
    "The PharmaTrack property graph model consists of 6 primary Node labels and 7 directed Relationship types. Nodes encapsulate domain entities along with descriptive properties, while relationships represent physical flow of goods, processing transformations, and regulatory audits.",
    bold_prefix="Architecture Overview: "
)

add_heading_with_spacing(doc10, "3.1 Entities (Nodes) and Attributes (Properties)", level=2)
tbl_nodes = doc10.add_table(rows=7, cols=3)
tbl_nodes.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Node Label", "Description", "Key Properties & Data Types"]
for col_idx, h_text in enumerate(headers):
    cell = tbl_nodes.cell(0, col_idx)
    set_cell_background(cell, "2B6CB0")
    set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
    p = cell.paragraphs[0]
    r = p.add_run(h_text)
    r.font.name = 'Times New Roman'
    r.font.bold = True
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

node_rows = [
    ("Supplier", "Provides raw chemical ingredients / APIs", "id (String, Unique), name (String), country (String), certified (Boolean)"),
    ("Manufacturer", "Licensed pharmaceutical factory producing batches", "id (String, Unique), name (String), city (String), gmpCompliant (Boolean)"),
    ("Batch", "Physical production lot of manufactured medication", "batchId (String, Unique), drugName (String), mfgDate (Date), expiryDate (Date), status (String)"),
    ("Warehouse", "Regional logistics center & cold-storage depot", "id (String, Unique), name (String), city (String), coldChainSupported (Boolean)"),
    ("Pharmacy", "Licensed dispensary or hospital pharmacy", "id (String, Unique), name (String), licenseNo (String), city (String)"),
    ("Inspector", "Regulatory authority conducting compliance audits", "id (String, Unique), name (String), agency (String)")
]

for row_idx, data in enumerate(node_rows, start=1):
    bg_col = "FFFFFF" if row_idx % 2 != 0 else "EDF2F7"
    for col_idx, text in enumerate(data):
        cell = tbl_nodes.cell(row_idx, col_idx)
        set_cell_background(cell, bg_col)
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        if col_idx == 0:
            r.font.bold = True

doc10.add_paragraph().paragraph_format.space_after = Pt(6)

add_heading_with_spacing(doc10, "3.2 Relationships between Entities", level=2)
tbl_rels = doc10.add_table(rows=8, cols=4)
tbl_rels.alignment = WD_TABLE_ALIGNMENT.CENTER
rel_headers = ["Relationship Type", "Source -> Target", "Description", "Edge Properties"]
for col_idx, h_text in enumerate(rel_headers):
    cell = tbl_rels.cell(0, col_idx)
    set_cell_background(cell, "2B6CB0")
    set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
    p = cell.paragraphs[0]
    r = p.add_run(h_text)
    r.font.name = 'Times New Roman'
    r.font.bold = True
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

rel_rows = [
    ("SUPPLIED", "Supplier -> Manufacturer", "Raw ingredient or API shipment", "ingredient (String), date (Date), lotNo (String)"),
    ("PRODUCED", "Manufacturer -> Batch", "Manufacturing output linking factory to batch", "date (Date), totalUnits (Integer)"),
    ("SHIPPED", "Manufacturer -> Warehouse", "Wholesale logistics transit with cold telemetry", "dispatchDate (Date), carrier (String), tempCelsius (Float)"),
    ("STORED", "Warehouse -> Batch", "Inventory holding in climate-controlled zone", "shelfZone (String), entryDate (Date)"),
    ("DELIVERED_TO", "Warehouse -> Pharmacy", "Distribution shipment to retail/hospital pharmacy", "deliveryDate (Date), qtyReceived (Integer)"),
    ("DISPENSES", "Pharmacy -> Batch", "Retail dispensing connection to patient stock", "batchId (String)"),
    ("AUDITED", "Inspector -> Batch", "Regulatory quality assurance inspection", "auditDate (Date), outcome (String), certNo (String)")
]

for row_idx, data in enumerate(rel_rows, start=1):
    bg_col = "FFFFFF" if row_idx % 2 != 0 else "EDF2F7"
    for col_idx, text in enumerate(data):
        cell = tbl_rels.cell(row_idx, col_idx)
        set_cell_background(cell, bg_col)
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        if col_idx == 0:
            r.font.bold = True

doc10.add_paragraph().paragraph_format.space_after = Pt(8)

add_heading_with_spacing(doc10, "3.3 Graph Schema Design Diagram", level=2)
add_body_p(doc10, 
    "Figure 1 below illustrates the formal Graph Schema/Model for the PharmaTrack system. Directed edges represent the sequence of manufacturing, custody transfer, and auditing operations, demonstrating how any end-consumer batch can be traversed backwards to source suppliers in O(1) graph hops.",
    bold_prefix="Schema Visualization: "
)

schema_img_path = r"C:\Users\as174\OneDrive\Desktop\mini_project_adb\pharmatrack-neo4j\diagrams\graph_schema.png"
if os.path.exists(schema_img_path):
    p_img = doc10.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.add_run().add_picture(schema_img_path, width=Inches(6.0))
    
    p_cap = doc10.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(12)
    r_cap = p_cap.add_run("Figure 1: PharmaTrack Graph Schema Architecture (Entities, Relationships, and Properties)")
    r_cap.font.name = 'Times New Roman'
    r_cap.font.size = Pt(10)
    r_cap.font.bold = True
    r_cap.font.italic = True

# Save Exp 10 in destination folder
exp10_target = r"C:\Users\as174\OneDrive\Desktop\mini_project_adb\pharmatrack-neo4j\2026-27 ADB Exp 10 Manual.docx"
doc10.save(exp10_target)
print("Successfully generated and saved Exp 10 Manual to:", exp10_target)

# =============================================================
# BUILD EXP 11 MANUAL
# =============================================================
doc11_path = r"C:\Users\as174\OneDrive\Desktop\mini_project_adb\2026-27 ADB Exp 11 Manual.docx"
doc11 = Document(doc11_path)

# Clear existing body paragraphs
for p in list(doc11.paragraphs):
    p._element.getparent().remove(p._element)

# Title Header
p_exp11 = doc11.add_paragraph()
p_exp11.paragraph_format.space_before = Pt(0)
p_exp11.paragraph_format.space_after = Pt(2)
p_exp11.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_exp11.add_run("Experiment No. 11")
r.font.name = 'Times New Roman'
r.font.size = Pt(16)
r.font.bold = True

p_sub11 = doc11.add_paragraph()
p_sub11.paragraph_format.space_after = Pt(14)
p_sub11.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_sub11.add_run("MINI PROJECT - II : GRAPH DATABASE IMPLEMENTATION & CYPHER CRUD OPERATIONS")
r.font.name = 'Times New Roman'
r.font.size = Pt(13)
r.font.bold = True
r.font.color.rgb = RGBColor(0x2b, 0x6c, 0xb0)

# Section 4: Cypher Queries: Perform CRUD Operations
add_heading_with_spacing(doc11, "4. Cypher Queries: Perform CRUD Operations", level=1)
add_body_p(doc11, 
    "The PharmaTrack database is deployed on Neo4j AuraDB (Cloud Instance ID: 12a3ba9d). Implementation is executed using Cypher, Neo4j's declarative graph query language. CRUD (Create, Read, Update, Delete) operations are executed below to demonstrate full lifecycle data management, path traversal, counterfeit detection, and recall quarantine.",
    bold_prefix="Implementation Environment: "
)

add_heading_with_spacing(doc11, "4.1 CREATE: Database Seeding, Nodes, and Relationships", level=2)
add_body_p(doc11, 
    "Uniqueness constraints and index structures are first established to guarantee data integrity across batch IDs and facility codes. Subsequently, nodes and directional relationships are instantiated using declarative CREATE blocks:",
    bold_prefix="Query Execution: "
)

cypher_create = """// 1. Establish Schema Constraints
CREATE CONSTRAINT IF NOT EXISTS FOR (b:Batch) REQUIRE b.batchId IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (s:Supplier) REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (m:Manufacturer) REQUIRE m.id IS UNIQUE;

// 2. Instantiate Verified Nodes
CREATE (s1:Supplier {id: 'SUP-01', name: 'Apex BioChem Ltd', country: 'Germany', certified: true})
CREATE (s2:Supplier {id: 'SUP-02', name: 'Global Solvents Co', country: 'India', certified: true})
CREATE (s3:Supplier {id: 'SUP-03', name: 'Rogue Chemical Trading', country: 'Unknown', certified: false})

CREATE (m1:Manufacturer {id: 'MFG-01', name: 'PharmaCore Labs', city: 'Basel', gmpCompliant: true})
CREATE (m2:Manufacturer {id: 'MFG-02', name: 'HealthGen Pharma', city: 'Mumbai', gmpCompliant: true})

CREATE (b1:Batch {batchId: 'BATCH-2026-A1', drugName: 'Amoxicillin 500mg', mfgDate: '2026-03-10', expiryDate: '2028-03-10', status: 'ACTIVE'})
CREATE (b2:Batch {batchId: 'BATCH-2026-B2', drugName: 'Insulin Glargine', mfgDate: '2026-05-15', expiryDate: '2027-05-15', status: 'ACTIVE'})
CREATE (b3:Batch {batchId: 'BATCH-FAKE-X9', drugName: 'Insulin Glargine', mfgDate: '2026-06-01', expiryDate: '2027-06-01', status: 'SUSPICIOUS'})

CREATE (w1:Warehouse {id: 'WH-CENTRAL', name: 'Euro Hub Logistics', city: 'Frankfurt', coldChainSupported: true})
CREATE (w2:Warehouse {id: 'WH-SOUTH', name: 'Metropolis Cold Storage', city: 'Munich', coldChainSupported: true})

CREATE (p1:Pharmacy {id: 'PHARM-01', name: 'City Central Pharmacy', city: 'Frankfurt', licenseNo: 'LIC-8821'})
CREATE (p2:Pharmacy {id: 'PHARM-02', name: 'St. Jude Hospital Pharmacy', city: 'Munich', licenseNo: 'LIC-4412'})
CREATE (p3:Pharmacy {id: 'PHARM-03', name: 'Discount Meds Online', city: 'Berlin', licenseNo: 'LIC-0000'})

CREATE (ins1:Inspector {id: 'INS-01', name: 'Dr. Elena Rostova', agency: 'European Medicines Agency'})

// 3. Connect Relationships
CREATE (s1)-[:SUPPLIED {ingredient: 'Active Amoxicillin Powder', date: '2026-02-15', lotNo: 'LOT-901'}]->(m1)
CREATE (s2)-[:SUPPLIED {ingredient: 'Biosynthetic Peptide', date: '2026-04-10', lotNo: 'LOT-554'}]->(m2)
CREATE (s3)-[:SUPPLIED {ingredient: 'Unverified Reagents', date: '2026-05-20', lotNo: 'LOT-000'}]->(m2)

CREATE (m1)-[:PRODUCED {date: '2026-03-10', totalUnits: 50000}]->(b1)
CREATE (m2)-[:PRODUCED {date: '2026-05-15', totalUnits: 20000}]->(b2)

CREATE (m1)-[:SHIPPED {dispatchDate: '2026-03-14', carrier: 'DHL Pharma', tempCelsius: 4.5}]->(w1)
CREATE (m2)-[:SHIPPED {dispatchDate: '2026-05-18', carrier: 'Kuehne+Nagel', tempCelsius: 3.8}]->(w2)

CREATE (w1)-[:STORED {shelfZone: 'Cold-A2', entryDate: '2026-03-15'}]->(b1)
CREATE (w2)-[:STORED {shelfZone: 'DeepFreeze-01', entryDate: '2026-05-19'}]->(b2)

CREATE (w1)-[:DELIVERED_TO {deliveryDate: '2026-03-20', qtyReceived: 5000}]->(p1)
CREATE (w2)-[:DELIVERED_TO {deliveryDate: '2026-05-25', qtyReceived: 3000}]->(p2)

CREATE (p1)-[:DISPENSES]->(b1)
CREATE (p2)-[:DISPENSES]->(b2)
CREATE (p3)-[:DISPENSES]->(b3) // Rogue batch with NO verified factory origin!

CREATE (ins1)-[:AUDITED {auditDate: '2026-03-12', outcome: 'PASSED', certNo: 'CERT-2026-09'}]->(b1)
CREATE (ins1)-[:AUDITED {auditDate: '2026-05-17', outcome: 'PASSED', certNo: 'CERT-2026-44'}]->(b2);"""
add_code_block(doc11, cypher_create)

add_heading_with_spacing(doc11, "4.2 READ / QUERY: Provenance Tracing & Counterfeit Detection", level=2)

add_body_p(doc11, 
    "Traces the complete physical lineage of batch 'BATCH-2026-A1' from the chemical ingredient supplier through manufacturing, warehousing, and down to the dispensing pharmacy.",
    bold_prefix="Query 1 (End-to-End Batch Provenance Trace): "
)
q1_code = """MATCH (s:Supplier)-[:SUPPLIED]->(m:Manufacturer)-[:PRODUCED]->(b:Batch {batchId: 'BATCH-2026-A1'})<-[:STORED]-(w:Warehouse)-[:DELIVERED_TO]->(p:Pharmacy)
RETURN s.name AS Supplier, m.name AS Manufacturer, b.drugName AS Drug, 
       w.name AS Warehouse, p.name AS Pharmacy;"""
add_code_block(doc11, q1_code)

add_body_p(doc11, 
    "Scans all dispensing pharmacies to identify drug batches that lack a verified manufacturing link (`WHERE NOT (:Manufacturer)-[:PRODUCED]->(b)`), immediately flagging counterfeit stock.",
    bold_prefix="Query 2 (Counterfeit & Broken Chain Detection): "
)
q2_code = """MATCH (p:Pharmacy)-[:DISPENSES]->(b:Batch)
WHERE NOT (:Manufacturer)-[:PRODUCED]->(b)
RETURN p.name AS SuspiciousPharmacy, b.batchId AS SuspiciousBatch, 
       b.drugName AS DrugName, b.status AS CurrentStatus;"""
add_code_block(doc11, q2_code)

add_body_p(doc11, 
    "Verifies transit telemetry along SHIPPED relationships for temperature-sensitive drugs like Insulin to ensure the cold-chain threshold (< 5°C) was never breached during transit.",
    bold_prefix="Query 3 (Cold-Chain Logistics Audit): "
)
q3_code = """MATCH (m:Manufacturer)-[s:SHIPPED]->(w:Warehouse)-[:STORED]->(b:Batch {drugName: 'Insulin Glargine'})
RETURN b.batchId AS Batch, m.name AS Manufacturer, w.name AS Warehouse, 
       s.carrier AS Carrier, s.tempCelsius AS TransitTemperatureCelsius;"""
add_code_block(doc11, q3_code)

add_heading_with_spacing(doc11, "4.3 UPDATE: Property Mutation & Batch Quarantine", level=2)
add_body_p(doc11, 
    "When counterfeit stock or contamination is verified, the batch status is updated to 'QUARANTINED_COUNTERFEIT' and an immutable inspection flag timestamp is added using the SET clause:",
    bold_prefix="Query 4 (Quarantine / Recall Update): "
)
q4_code = """MATCH (b:Batch {batchId: 'BATCH-FAKE-X9'})
SET b.status = 'QUARANTINED_COUNTERFEIT', b.flaggedDate = '2026-10-28'
RETURN b.batchId AS Batch, b.status AS UpdatedStatus, b.flaggedDate AS FlagDate;"""
add_code_block(doc11, q4_code)

add_heading_with_spacing(doc11, "4.4 DELETE: Relationship & Node Cleanup", level=2)
add_body_p(doc11, 
    "Removes uncertified or blacklisted supplier connections while preserving core enterprise nodes:",
    bold_prefix="Query 5 (Rogue Relationship Deletion): "
)
q5_code = """MATCH (s:Supplier {id: 'SUP-03'})-[r:SUPPLIED]->()
DELETE r
RETURN count(r) AS DeletedRelationships;"""
add_code_block(doc11, q5_code)

# Section 5: Output Screenshots & Results
add_heading_with_spacing(doc11, "5. Output Screenshots & Execution Results", level=1)
add_body_p(doc11, 
    "The following figures display the visual graph outputs generated in the Neo4j instance along with query result tables:",
    bold_prefix="Execution Visualizations: "
)

net_img_path = r"C:\Users\as174\OneDrive\Desktop\mini_project_adb\pharmatrack-neo4j\diagrams\full_graph_network.png"
if os.path.exists(net_img_path):
    p_img1 = doc11.add_paragraph()
    p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img1.paragraph_format.space_before = Pt(6)
    p_img1.paragraph_format.space_after = Pt(2)
    p_img1.add_run().add_picture(net_img_path, width=Inches(6.0))
    
    p_cap1 = doc11.add_paragraph()
    p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap1.paragraph_format.space_after = Pt(10)
    r_cap1 = p_cap1.add_run("Figure 2: Full Neo4j Instance Graph Visualization (Suppliers, Batches, Warehouses, Pharmacies)")
    r_cap1.font.name = 'Times New Roman'
    r_cap1.font.size = Pt(10)
    r_cap1.font.bold = True
    r_cap1.font.italic = True

trace_img_path = r"C:\Users\as174\OneDrive\Desktop\mini_project_adb\pharmatrack-neo4j\diagrams\provenance_trace.png"
if os.path.exists(trace_img_path):
    p_img2 = doc11.add_paragraph()
    p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img2.paragraph_format.space_before = Pt(6)
    p_img2.paragraph_format.space_after = Pt(2)
    p_img2.add_run().add_picture(trace_img_path, width=Inches(5.8))
    
    p_cap2 = doc11.add_paragraph()
    p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap2.paragraph_format.space_after = Pt(10)
    r_cap2 = p_cap2.add_run("Figure 3: Query 1 Visual Traversal Result (End-to-End Batch Provenance)")
    r_cap2.font.name = 'Times New Roman'
    r_cap2.font.size = Pt(10)
    r_cap2.font.bold = True
    r_cap2.font.italic = True

add_heading_with_spacing(doc11, "5.1 Tabular Query Results", level=2)

# Table for Query 1 Output
add_body_p(doc11, "Query 1 Output Table (Batch Lineage):", bold_prefix="Result Table 1: ")
t1 = doc11.add_table(rows=2, cols=5)
t1.alignment = WD_TABLE_ALIGNMENT.CENTER
headers1 = ["Supplier", "Manufacturer", "Drug", "Warehouse", "Pharmacy"]
for c_idx, h in enumerate(headers1):
    c = t1.cell(0, c_idx)
    set_cell_background(c, "2B6CB0")
    set_cell_margins(c, top=80, bottom=80, left=100, right=100)
    p = c.paragraphs[0]
    r = p.add_run(h)
    r.font.name = 'Times New Roman'
    r.font.bold = True
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
data1 = ["Apex BioChem Ltd", "PharmaCore Labs", "Amoxicillin 500mg", "Euro Hub Logistics", "City Central Pharmacy"]
for c_idx, d in enumerate(data1):
    c = t1.cell(1, c_idx)
    set_cell_background(c, "EDF2F7")
    set_cell_margins(c, top=60, bottom=60, left=100, right=100)
    p = c.paragraphs[0]
    r = p.add_run(d)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(9.5)

doc11.add_paragraph().paragraph_format.space_after = Pt(6)

# Table for Query 2 Output
add_body_p(doc11, "Query 2 Output Table (Counterfeit Detection):", bold_prefix="Result Table 2: ")
t2 = doc11.add_table(rows=2, cols=4)
t2.alignment = WD_TABLE_ALIGNMENT.CENTER
headers2 = ["Suspicious Pharmacy", "Suspicious Batch", "Drug Name", "Current Status"]
for c_idx, h in enumerate(headers2):
    c = t2.cell(0, c_idx)
    set_cell_background(c, "E53E3E") # Crimson red
    set_cell_margins(c, top=80, bottom=80, left=100, right=100)
    p = c.paragraphs[0]
    r = p.add_run(h)
    r.font.name = 'Times New Roman'
    r.font.bold = True
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
data2 = ["Discount Meds Online", "BATCH-FAKE-X9", "Insulin Glargine", "SUSPICIOUS"]
for c_idx, d in enumerate(data2):
    c = t2.cell(1, c_idx)
    set_cell_background(c, "FFF5F5")
    set_cell_margins(c, top=60, bottom=60, left=100, right=100)
    p = c.paragraphs[0]
    r = p.add_run(d)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(9.5)

doc11.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 6: Observations
add_heading_with_spacing(doc11, "6. Observations", level=1)
obs_points = [
    ("Traversal Performance & Index-Free Adjacency: ", "In Neo4j, traversing multi-hop supply chain connections occurs in O(1) time per step via direct memory pointers, avoiding relational multi-table JOINs where performance degrades exponentially (O(n^k)) as tables expand."),
    ("Declarative Expressiveness of Cypher: ", "Complex recursive lineage queries that require multi-level CTEs in SQL are expressed intuitively in Cypher using ASCII-art pattern matching: `(Supplier)-[:SUPPLIED]->(Manufacturer)-[:PRODUCED]->(Batch)`."),
    ("Instant Anomaly & Counterfeit Isolation: ", "Graph pattern negation (`WHERE NOT (m:Manufacturer)-[:PRODUCED]->(b)`) allowed instantaneous identification of illegitimate inventory lacking authentic factory genesis."),
    ("Flexible Schema Evolution: ", "Adding environmental metrics (transit temperature, carrier, audit certificates) directly onto relationship edges was achieved seamlessly without altering table schemas or causing database lockups.")
]
for pfx, desc in obs_points:
    add_body_p(doc11, desc, bold_prefix=f"•  {pfx}")

# Section 7: Conclusion
add_heading_with_spacing(doc11, "7. Conclusion", level=1)
add_body_p(doc11, 
    "In this experiment, the PharmaTrack graph database was successfully designed, deployed, and queried on Neo4j AuraDB. The project implemented end-to-end pharmaceutical track-and-trace capabilities, covering CRUD operations with Cypher queries. By modeling supply chain actors as nodes and logistic/regulatory interactions as first-class relationships, the system achieved rapid provenance verification, cold-chain compliance auditing, and automated counterfeit drug isolation. The results confirm that graph databases are substantially superior to traditional relational models for deeply connected, mission-critical provenance tracking.",
    bold_prefix="Summary: "
)

# Save Exp 11 in destination folder
exp11_target = r"C:\Users\as174\OneDrive\Desktop\mini_project_adb\pharmatrack-neo4j\2026-27 ADB Exp 11 Manual.docx"
doc11.save(exp11_target)
print("Successfully generated and saved Exp 11 Manual to:", exp11_target)

