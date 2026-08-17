## Medallion Lakehouse Pipeline on Databricks

### Objective

Build a production-style lakehouse on Databricks that ingests raw trip data incrementally, enforces data quality, and serves an analytics-ready dimensional model — deployable to multiple environments from a single codebase.

### System Architecture

Bronze / silver / gold medallion architecture orchestrated as a **five-task Databricks Workflow DAG**.

```
Raw Files (Volume)
   ↓  Auto Loader (incremental ingestion)
Bronze (raw, append-only Delta tables)
   ↓  Validity rules + cleansing
Silver (validated, conformed Delta tables)
   ↓  Dimensional modeling
Gold (Delta Lake star schema: fact + dimensions)
```

### Key Features

* **Incremental ingestion with Auto Loader** — new files are picked up automatically without full reprocessing.
* **Validity enforcement at the silver layer** — data quality rules filter and quarantine invalid records before they reach analytics tables.
* **Delta Lake star schema at gold** — fact and dimension tables with surrogate keys and foreign key constraints for reliable joins.
* **Databricks Asset Bundle packaging** — dev and prod targets derive every catalog, schema, volume, and job trigger from a single variable set, so environment promotion requires no code changes.
* **Unity Catalog governance** — centralized catalog/schema management, access control, and lineage across all three layers.

### Technologies Used

* Platform: Databricks
* Processing: Apache Spark (PySpark, Spark SQL)
* Storage Format: Delta Lake
* Ingestion: Databricks Auto Loader
* Orchestration: Databricks Workflows (multi-task job DAG)
* Deployment: Databricks Asset Bundles (DABs)
* Governance: Unity Catalog

### Outcome

* End-to-end lakehouse pipeline running as an orchestrated, repeatable workflow rather than ad-hoc notebooks.
* Clean separation between raw, validated, and modeled data, making downstream analytics predictable and auditable.
* Single-source-of-truth configuration enabling identical dev and prod deployments with zero manual setup.

---
