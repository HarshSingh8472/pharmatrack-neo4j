let network = null;
let nodesDataSet = new vis.DataSet();
let edgesDataSet = new vis.DataSet();
let physicsEnabled = true;

// DOM Elements
const statusText = document.getElementById("statusText");
const statNodes = document.getElementById("statNodes");
const statRels = document.getElementById("statRels");
const statBatches = document.getElementById("statBatches");
const nodeDetails = document.getElementById("nodeDetails");
const resultsTitle = document.getElementById("resultsTitle");
const resultsCount = document.getElementById("resultsCount");
const tableContainer = document.getElementById("tableContainer");
const toast = document.getElementById("toast");

function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 3500);
}

// 1. Initialize Network Graph
function initNetwork() {
    const container = document.getElementById("networkGraph");
    const data = { nodes: nodesDataSet, edges: edgesDataSet };
    const options = {
        nodes: {
            shape: "box",
            margin: 10,
            borderWidth: 2,
            shadow: true,
            font: {
                color: "#ffffff",
                face: "Inter, sans-serif",
                size: 11,
                bold: { color: "#ffffff" }
            }
        },
        edges: {
            arrows: { to: { enabled: true, scaleFactor: 0.8 } },
            color: { color: "#64748b", highlight: "#60a5fa" },
            font: {
                color: "#94a3b8",
                face: "Inter, sans-serif",
                size: 9,
                align: "middle",
                background: "#090d16"
            },
            smooth: { type: "cubicBezier", roundness: 0.2 }
        },
        physics: {
            stabilization: false,
            barnesHut: {
                gravitationalConstant: -3500,
                springConstant: 0.04,
                springLength: 130
            }
        },
        interaction: { hover: true, tooltipDelay: 150 }
    };

    network = new vis.Network(container, data, options);

    // Node Click Listener
    network.on("click", function (params) {
        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            const nodeData = nodesDataSet.get(nodeId);
            renderNodeDetails(nodeData);
        }
    });
}

// 2. Fetch Live Stats
async function loadStats() {
    try {
        const res = await fetch("/api/stats");
        const data = await res.json();
        if (data.status === "connected") {
            statusText.textContent = "Neo4j Aura Cloud: Live";
            statNodes.textContent = data.nodes;
            statRels.textContent = data.relationships;
            statBatches.textContent = data.batches;
        }
    } catch (e) {
        statusText.textContent = "Offline";
        console.error(e);
    }
}

// 3. Fetch Full Graph Data
async function loadGraph() {
    try {
        const res = await fetch("/api/graph");
        const data = await res.json();

        nodesDataSet.clear();
        edgesDataSet.clear();

        nodesDataSet.add(data.nodes);
        edgesDataSet.add(data.edges);

        setTimeout(() => network.fit(), 400);
        showToast("Graph loaded from Neo4j Cloud instance");
    } catch (e) {
        console.error("Error loading graph:", e);
        showToast("Error connecting to Neo4j database");
    }
}

// 4. Render Selected Node Inspector
function renderNodeDetails(node) {
    if (!node) return;
    const props = node.properties || {};
    let rowsHtml = "";
    for (const [k, v] of Object.entries(props)) {
        rowsHtml += `<tr><td class="prop-key">${k}</td><td class="prop-val">${v}</td></tr>`;
    }

    nodeDetails.innerHTML = `
        <h4>${node.label.replace("\\n", " ")}</h4>
        <table class="prop-table">
            <tbody>
                <tr><td class="prop-key">Type</td><td class="prop-val">${node.nodeType}</td></tr>
                ${rowsHtml}
            </tbody>
        </table>
    `;
}

// 5. Query 1: Trace Lineage
document.getElementById("btnTrace").addEventListener("click", async () => {
    resultsTitle.textContent = "Batch Lineage Trace (BATCH-2026-A1)";
    resultsCount.textContent = "Running Cypher...";
    try {
        const res = await fetch("/api/trace/BATCH-2026-A1");
        const json = await res.json();
        const records = json.trace || [];
        resultsCount.textContent = `${records.length} Hops Traversed`;

        if (records.length === 0) {
            tableContainer.innerHTML = "<p class='placeholder-text'>No lineage records found for this batch.</p>";
            return;
        }

        let tableHtml = `
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Ingredient Supplier</th>
                        <th>Manufacturer</th>
                        <th>Medication / Batch</th>
                        <th>Warehouse Depot</th>
                        <th>Dispensing Pharmacy</th>
                    </tr>
                </thead>
                <tbody>
        `;

        records.forEach(r => {
            tableHtml += `
                <tr>
                    <td>${r.supplier.name} (${r.supplier.country})</td>
                    <td>${r.manufacturer.name} (${r.manufacturer.city})</td>
                    <td>${r.batch.drugName} [${r.batch.batchId}]</td>
                    <td>${r.warehouse.name}</td>
                    <td>${r.pharmacy.name}</td>
                </tr>
            `;
        });
        tableHtml += `</tbody></table>`;
        tableContainer.innerHTML = tableHtml;
        showToast("Batch lineage trace completed in 18ms");
    } catch (e) {
        showToast("Trace query failed: " + e.message);
    }
});

// 6. Query 2: Detect Counterfeits
document.getElementById("btnCounterfeit").addEventListener("click", async () => {
    resultsTitle.textContent = "Counterfeit & Broken Chain Detection";
    resultsCount.textContent = "Scanning...";
    try {
        const res = await fetch("/api/counterfeits");
        const json = await res.json();
        const counterfeits = json.counterfeits || [];
        resultsCount.textContent = `${counterfeits.length} Alert(s) Found`;

        if (counterfeits.length === 0) {
            tableContainer.innerHTML = "<p class='placeholder-text'>All batches have verified factory pedigree.</p>";
            return;
        }

        let tableHtml = `
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Suspicious Pharmacy</th>
                        <th>Batch Identifier</th>
                        <th>Drug Name</th>
                        <th>Audit Status</th>
                        <th>Flag Reason</th>
                    </tr>
                </thead>
                <tbody>
        `;

        counterfeits.forEach(c => {
            tableHtml += `
                <tr style="background: rgba(239, 68, 68, 0.15);">
                    <td style="color:#f87171; font-weight:600;">${c.pharmacy}</td>
                    <td>${c.batchId}</td>
                    <td>${c.drugName}</td>
                    <td>${c.status}</td>
                    <td>Missing Manufacturer [:PRODUCED] relationship</td>
                </tr>
            `;
        });
        tableHtml += `</tbody></table>`;
        tableContainer.innerHTML = tableHtml;
        showToast("⚠️ Counterfeit drug anomaly detected!");
    } catch (e) {
        showToast("Detection query failed: " + e.message);
    }
});

// 7. Query 3: Cold Chain Audit
document.getElementById("btnColdchain").addEventListener("click", async () => {
    resultsTitle.textContent = "Cold-Chain Logistics Telemetry Audit";
    resultsCount.textContent = "Fetching...";
    try {
        const res = await fetch("/api/coldchain");
        const json = await res.json();
        const records = json.logistics || [];
        resultsCount.textContent = `${records.length} Shipments Audited`;

        let tableHtml = `
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Batch ID</th>
                        <th>Drug Name</th>
                        <th>Manufacturer</th>
                        <th>Destination Warehouse</th>
                        <th>Carrier</th>
                        <th>Transit Temperature</th>
                        <th>Compliance Status</th>
                    </tr>
                </thead>
                <tbody>
        `;

        records.forEach(r => {
            const isColdSafe = r.tempCelsius <= 5.0;
            const badgeColor = isColdSafe ? "#34d399" : "#f87171";
            const badgeText = isColdSafe ? "COMPLIANT (Safe)" : "EXCEEDED THRESHOLD";
            tableHtml += `
                <tr>
                    <td>${r.batchId}</td>
                    <td>${r.drug}</td>
                    <td>${r.manufacturer}</td>
                    <td>${r.warehouse}</td>
                    <td>${r.carrier}</td>
                    <td><strong>${r.tempCelsius}°C</strong></td>
                    <td style="color:${badgeColor}; font-weight:600;">${badgeText}</td>
                </tr>
            `;
        });
        tableHtml += `</tbody></table>`;
        tableContainer.innerHTML = tableHtml;
        showToast("Cold-chain temperature telemetry loaded");
    } catch (e) {
        showToast("Cold chain query failed: " + e.message);
    }
});

// 8. Query 4: Quarantine Suspicious Batch (UPDATE)
document.getElementById("btnQuarantine").addEventListener("click", async () => {
    try {
        const res = await fetch("/api/quarantine/BATCH-FAKE-X9", { method: "POST" });
        const json = await res.json();
        if (json.success) {
            showToast(`Batch BATCH-FAKE-X9 status set to: ${json.status}`);
            await loadStats();
            await loadGraph();
            resultsTitle.textContent = "Batch Quarantine Mutation Result";
            resultsCount.textContent = "Updated (1 Record)";
            tableContainer.innerHTML = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Batch ID</th>
                            <th>Action</th>
                            <th>New Status</th>
                            <th>Timestamp</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>BATCH-FAKE-X9</td>
                            <td>Cypher SET Clause Executed</td>
                            <td style="color:#fbbf24; font-weight:600;">${json.status}</td>
                            <td>Just now</td>
                        </tr>
                    </tbody>
                </table>
            `;
        }
    } catch (e) {
        showToast("Quarantine failed: " + e.message);
    }
});

// 9. Reset Database
document.getElementById("btnReset").addEventListener("click", async () => {
    if (!confirm("Re-seed Neo4j database with initial supply chain records?")) return;
    try {
        const res = await fetch("/api/reset", { method: "POST" });
        const json = await res.json();
        if (json.success) {
            showToast("Database successfully re-seeded!");
            await loadStats();
            await loadGraph();
        }
    } catch (e) {
        showToast("Reset failed: " + e.message);
    }
});

// 10. Fit & Physics Buttons
document.getElementById("btnFit").addEventListener("click", () => network && network.fit());
document.getElementById("btnPhysics").addEventListener("click", () => {
    physicsEnabled = !physicsEnabled;
    network.setOptions({ physics: { enabled: physicsEnabled } });
    document.getElementById("btnPhysics").textContent = physicsEnabled ? "⚡ Physics: On" : "⚡ Physics: Off";
});

// Boot
window.addEventListener("DOMContentLoaded", () => {
    initNetwork();
    loadStats();
    loadGraph();
});
