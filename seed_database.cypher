// ==============================================================================
// PharmaTrack: Pharmaceutical Supply Chain & Counterfeit Detection Graph
// Neo4j Cypher Schema, Seeding & Query Script
// ==============================================================================

// 1. SCHEMA CONSTRAINTS & INDEXES
CREATE CONSTRAINT IF NOT EXISTS FOR (b:Batch) REQUIRE b.batchId IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (s:Supplier) REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (m:Manufacturer) REQUIRE m.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (w:Warehouse) REQUIRE w.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (p:Pharmacy) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (i:Inspector) REQUIRE i.id IS UNIQUE;

// 2. CLEAR EXISTING DATA (OPTIONAL / RESET)
// MATCH (n) DETACH DELETE n;

// 3. CREATE VERIFIED SUPPLIERS
CREATE (s1:Supplier {id: 'SUP-01', name: 'Apex BioChem Ltd', country: 'Germany', certified: true})
CREATE (s2:Supplier {id: 'SUP-02', name: 'Global Solvents Co', country: 'India', certified: true})
CREATE (s3:Supplier {id: 'SUP-03', name: 'Rogue Chemical Trading', country: 'Unknown', certified: false})

// 4. CREATE PHARMACEUTICAL MANUFACTURERS
CREATE (m1:Manufacturer {id: 'MFG-01', name: 'PharmaCore Labs', city: 'Basel', gmpCompliant: true})
CREATE (m2:Manufacturer {id: 'MFG-02', name: 'HealthGen Pharma', city: 'Mumbai', gmpCompliant: true})

// 5. CREATE PRODUCTION DRUG BATCHES
CREATE (b1:Batch {batchId: 'BATCH-2026-A1', drugName: 'Amoxicillin 500mg', mfgDate: '2026-03-10', expiryDate: '2028-03-10', dosageMg: 500, status: 'ACTIVE'})
CREATE (b2:Batch {batchId: 'BATCH-2026-B2', drugName: 'Insulin Glargine', mfgDate: '2026-05-15', expiryDate: '2027-05-15', dosageMg: 100, status: 'ACTIVE'})
CREATE (b3:Batch {batchId: 'BATCH-FAKE-X9', drugName: 'Insulin Glargine', mfgDate: '2026-06-01', expiryDate: '2027-06-01', dosageMg: 100, status: 'SUSPICIOUS'})

// 6. CREATE LOGISTICS WAREHOUSES
CREATE (w1:Warehouse {id: 'WH-CENTRAL', name: 'Euro Hub Logistics', city: 'Frankfurt', coldChainSupported: true})
CREATE (w2:Warehouse {id: 'WH-SOUTH', name: 'Metropolis Cold Storage', city: 'Munich', coldChainSupported: true})
CREATE (w3:Warehouse {id: 'WH-EAST', name: 'Metro Standard Depot', city: 'Berlin', coldChainSupported: false})

// 7. CREATE PHARMACIES & CLINICS
CREATE (p1:Pharmacy {id: 'PHARM-01', name: 'City Central Pharmacy', city: 'Frankfurt', licenseNo: 'LIC-8821'})
CREATE (p2:Pharmacy {id: 'PHARM-02', name: 'St. Jude Hospital Pharmacy', city: 'Munich', licenseNo: 'LIC-4412'})
CREATE (p3:Pharmacy {id: 'PHARM-03', name: 'Discount Meds Online', city: 'Berlin', licenseNo: 'LIC-0000'})

// 8. CREATE REGULATORY INSPECTOR
CREATE (ins1:Inspector {id: 'INS-01', name: 'Dr. Elena Rostova', agency: 'European Medicines Agency'})

// 9. CREATE RELATIONSHIPS (CHAIN OF CUSTODY)
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
CREATE (p3)-[:DISPENSES]->(b3) // Fake batch sold without factory origin!

CREATE (ins1)-[:AUDITED {auditDate: '2026-03-12', outcome: 'PASSED', certNo: 'CERT-2026-09'}]->(b1)
CREATE (ins1)-[:AUDITED {auditDate: '2026-05-17', outcome: 'PASSED', certNo: 'CERT-2026-44'}]->(b2);

// ==============================================================================
// VERIFICATION QUERIES (CRUD OPERATIONS)
// ==============================================================================

// [READ - Query 1: Full Provenance Trace]
MATCH (s:Supplier)-[:SUPPLIED]->(m:Manufacturer)-[:PRODUCED]->(b:Batch {batchId: 'BATCH-2026-A1'})<-[:STORED]-(w:Warehouse)-[:DELIVERED_TO]->(p:Pharmacy)
RETURN s.name AS Supplier, m.name AS Manufacturer, b.drugName AS Drug, w.name AS Warehouse, p.name AS Pharmacy;

// [READ - Query 2: Counterfeit / Broken Chain Detection]
MATCH (p:Pharmacy)-[:DISPENSES]->(b:Batch)
WHERE NOT (:Manufacturer)-[:PRODUCED]->(b)
RETURN p.name AS SuspiciousPharmacy, b.batchId AS SuspiciousBatch, b.drugName AS DrugName, b.status AS CurrentStatus;

// [READ - Query 3: Cold-Chain Logistics Audit]
MATCH (m:Manufacturer)-[s:SHIPPED]->(w:Warehouse)-[:STORED]->(b:Batch {drugName: 'Insulin Glargine'})
RETURN b.batchId AS Batch, m.name AS Manufacturer, w.name AS Warehouse, s.carrier AS Carrier, s.tempCelsius AS TransitTemp;

// [UPDATE - Query 4: Quarantine Suspicious Batch]
MATCH (b:Batch {batchId: 'BATCH-FAKE-X9'})
SET b.status = 'QUARANTINED_COUNTERFEIT', b.flaggedDate = '2026-10-28'
RETURN b.batchId AS Batch, b.status AS UpdatedStatus, b.flaggedDate AS FlagDate;

// [DELETE - Query 5: Remove Rogue Supplier Connection]
MATCH (s:Supplier {id: 'SUP-03'})-[r:SUPPLIED]->()
DELETE r
RETURN count(r) AS DeletedRelationships;

