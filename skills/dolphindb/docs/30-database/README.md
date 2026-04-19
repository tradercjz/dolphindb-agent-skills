# 30-database — DFS databases, partitioning, storage engines

## Hand-authored

- `dfs-database.md`           — creating / dropping / inspecting DFS dbs.
- `partitioning.md`           ★ choosing VALUE / RANGE / HASH / LIST / COMPO.
- `tsdb-engine.md`            — TSDB specifics (sortColumns, keepDuplicates).
- `olap-engine.md`            — OLAP specifics.
- `pkey-engine.md`            — primary-key engine + `upsert!`.
- `limits-and-best-practices.md` — partition count, chunk size, concurrency.

## Full reference pages

From `db_distr_comp/db/*.md` upstream, in this directory:

| Topic | File |
|-------|------|
| Architecture | `db_architecture.md` |
| Partitioning | `db_partitioning.md` |
| TSDB | `tsdb.md` |
| OLAP | `olap.md` |
| PKEY | `pkey_engine.md` |
| IMOLTP | `imoltp.md` |
| VectorDB | `vectordb.md` |
| TextDB | `textdb.md` |
| IOTDB | `iotdb.md` |
| Catalog | `catalog.md` |
| HA / Raft | `ha.md`, `recovery.md` |
| Transactions | `transaction.md` |
| Storage/Compute separation | `storage_compute_separation.md` |
| Tiered storage | `tiered_storage.md` |
| Rebalance | `rebalance.md` |
| RDMA | `rdma.md` |
| DR | `three_centers_in_two_places.md` |
| Multimodal | `multimodal_storage.md` |
| Limits | `limits.md` |
