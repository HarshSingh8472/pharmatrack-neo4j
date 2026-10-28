import os
from flask import Flask, render_template, jsonify, request
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

NEO4J_URI = os.getenv("NEO4J_URI", "neo4j+s://12a3ba9d.databases.neo4j.io")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "12a3ba9d")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "9NiLss2g1BmDObmtgWXgOLq3rVFBCAx4AfUmaFwhDKA")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

def get_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

def get_session(driver):
    db = os.getenv("NEO4J_DATABASE", "").strip()
    if db and db != "neo4j":
        return driver.session(database=db)
    return driver.session()

# Color palette for graph visualization
GROUP_COLORS = {
    "Supplier": {"background": "#2ecc71", "border": "#27ae60", "highlight": "#2ecc71"},
    "Manufacturer": {"background": "#3498db", "border": "#2980b9", "highlight": "#3498db"},
    "Batch": {"background": "#e67e22", "border": "#d35400", "highlight": "#e67e22"},
    "Warehouse": {"background": "#9b59b6", "border": "#8e44ad", "highlight": "#9b59b6"},
    "Pharmacy": {"background": "#1abc9c", "border": "#16a085", "highlight": "#1abc9c"},
    "Inspector": {"background": "#f1c40f", "border": "#f39c12", "highlight": "#f1c40f"},
    "Counterfeit": {"background": "#e74c3c", "border": "#c0392b", "highlight": "#e74c3c"}
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/stats")
def get_stats():
    try:
        with get_driver() as driver:
            with get_session(driver) as session:
                node_cnt = session.run("MATCH (n) RETURN count(n) AS c").single()["c"]
                rel_cnt = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
                batch_cnt = session.run("MATCH (b:Batch) RETURN count(b) AS c").single()["c"]
                fake_cnt = session.run("MATCH (b:Batch) WHERE b.status CONTAINS 'COUNTERFEIT' OR b.status = 'SUSPICIOUS' RETURN count(b) AS c").single()["c"]
                return jsonify({
                    "status": "connected",
                    "nodes": node_cnt,
                    "relationships": rel_cnt,
                    "batches": batch_cnt,
                    "counterfeits": fake_cnt
                })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/graph")
def get_graph():
    try:
        with get_driver() as driver:
            with get_session(driver) as session:
                query = """
                MATCH (n)
                OPTIONAL MATCH (n)-[r]->(m)
                RETURN n, r, m
                """
                result = session.run(query)
                nodes_dict = {}
                edges = []

                for record in result:
                    n = record["n"]
                    r = record["r"]
                    m = record["m"]

                    if n and n.element_id not in nodes_dict:
                        labels = list(n.labels)
                        label = labels[0] if labels else "Node"
                        props = dict(n)
                        display_name = props.get("name") or props.get("batchId") or props.get("id") or label
                        
                        group = label
                        if label == "Batch" and ("COUNTERFEIT" in props.get("status", "") or props.get("status") == "SUSPICIOUS"):
                            group = "Counterfeit"

                        nodes_dict[n.element_id] = {
                            "id": n.element_id,
                            "label": f"{display_name}\n({label})",
                            "group": group,
                            "color": GROUP_COLORS.get(group, {"background": "#95a5a6", "border": "#7f8c8d"}),
                            "properties": props,
                            "nodeType": label
                        }

                    if m and m.element_id not in nodes_dict:
                        labels = list(m.labels)
                        label = labels[0] if labels else "Node"
                        props = dict(m)
                        display_name = props.get("name") or props.get("batchId") or props.get("id") or label

                        group = label
                        if label == "Batch" and ("COUNTERFEIT" in props.get("status", "") or props.get("status") == "SUSPICIOUS"):
                            group = "Counterfeit"

                        nodes_dict[m.element_id] = {
                            "id": m.element_id,
                            "label": f"{display_name}\n({label})",
                            "group": group,
                            "color": GROUP_COLORS.get(group, {"background": "#95a5a6", "border": "#7f8c8d"}),
                            "properties": props,
                            "nodeType": label
                        }

                    if r:
                        edges.append({
                            "id": r.element_id,
                            "from": n.element_id,
                            "to": m.element_id,
                            "label": r.type,
                            "properties": dict(r),
                            "arrows": "to"
                        })

                return jsonify({
                    "nodes": list(nodes_dict.values()),
                    "edges": edges
                })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/trace/<batch_id>")
def trace_batch(batch_id):
    try:
        with get_driver() as driver:
            with get_session(driver) as session:
                query = """
                MATCH (s:Supplier)-[r1:SUPPLIED]->(m:Manufacturer)-[r2:PRODUCED]->(b:Batch {batchId: $batch_id})<-[r3:STORED]-(w:Warehouse)-[r4:DELIVERED_TO]->(p:Pharmacy)
                RETURN s, r1, m, r2, b, r3, w, r4, p
                """
                result = session.run(query, batch_id=batch_id)
                records = []
                for rec in result:
                    records.append({
                        "supplier": dict(rec["s"]),
                        "supplied_props": dict(rec["r1"]),
                        "manufacturer": dict(rec["m"]),
                        "produced_props": dict(rec["r2"]),
                        "batch": dict(rec["b"]),
                        "warehouse": dict(rec["w"]),
                        "stored_props": dict(rec["r3"]),
                        "pharmacy": dict(rec["p"]),
                        "delivery_props": dict(rec["r4"])
                    })
                return jsonify({"batchId": batch_id, "trace": records})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/counterfeits")
def detect_counterfeits():
    try:
        with get_driver() as driver:
            with get_session(driver) as session:
                query = """
                MATCH (p:Pharmacy)-[r:DISPENSES]->(b:Batch)
                WHERE NOT (:Manufacturer)-[:PRODUCED]->(b)
                RETURN p.name AS pharmacy, b.batchId AS batchId, b.drugName AS drugName, b.status AS status
                """
                result = session.run(query)
                data = [dict(record) for record in result]
                return jsonify({"counterfeits": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/coldchain")
def audit_coldchain():
    try:
        with get_driver() as driver:
            with get_session(driver) as session:
                query = """
                MATCH (m:Manufacturer)-[s:SHIPPED]->(w:Warehouse)-[:STORED]->(b:Batch)
                RETURN b.batchId AS batchId, b.drugName AS drug, m.name AS manufacturer, 
                       w.name AS warehouse, s.carrier AS carrier, s.tempCelsius AS tempCelsius
                """
                result = session.run(query)
                data = [dict(record) for record in result]
                return jsonify({"logistics": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/quarantine/<batch_id>", methods=["POST"])
def quarantine_batch(batch_id):
    try:
        with get_driver() as driver:
            with get_session(driver) as session:
                query = """
                MATCH (b:Batch {batchId: $batch_id})
                SET b.status = 'QUARANTINED_COUNTERFEIT', b.flaggedDate = date()
                RETURN b.batchId AS batchId, b.status AS status
                """
                result = session.run(query, batch_id=batch_id).single()
                if result:
                    return jsonify({"success": True, "batchId": result["batchId"], "status": result["status"]})
                else:
                    return jsonify({"success": False, "message": "Batch not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/reset", methods=["POST"])
def reset_database():
    try:
        with get_driver() as driver:
            with get_session(driver) as session:
                session.run("MATCH (n) DETACH DELETE n")
                seed_script = """
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
                CREATE (p3)-[:DISPENSES]->(b3)

                CREATE (ins1)-[:AUDITED {auditDate: '2026-03-12', outcome: 'PASSED', certNo: 'CERT-2026-09'}]->(b1)
                CREATE (ins1)-[:AUDITED {auditDate: '2026-05-17', outcome: 'PASSED', certNo: 'CERT-2026-44'}]->(b2)
                """
                session.run(seed_script)
                return jsonify({"success": True, "message": "Database reset and seeded successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"🚀 PharmaTrack Dashboard running at http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
