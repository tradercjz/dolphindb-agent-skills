# Cluster management

## Node types recap

- **Controller** (1 or 3 for Raft HA) — metadata + coordination.
- **Data nodes** — store DFS chunks, run queries.
- **Compute nodes** — stateless, pair with remote data nodes.
- **Agents** — one per host, starts/stops local node processes.

## Config files

| File | Purpose |
|------|---------|
| `dolphindb.cfg` | Standalone config. |
| `controller.cfg` | Controller config. |
| `cluster.cfg` | Cluster-wide settings. |
| `cluster.nodes` | Node inventory (alias / host / port / type / group). |
| `agent.cfg` | Per-host agent config. |

## Start / stop

```bash
# start everything via agent (typical production)
./startAgent.sh

# stop via the web admin or:
curl http://host:8900/startup?action=stopAll
```

Always start **controller** first, then agents/data-nodes.

## Inspect

```dolphindb
getClusterPerf()                    // per-node perf snapshot
getClusterChunksStatus()            // chunk distribution / health
getClusterDFSDatabases()
getActiveMaster()                   // current Raft leader
getClusterReplicationStatus()       // data replication
getPerf()                           // local node counters
```

## Add / remove nodes

- Add: edit `cluster.nodes`, restart agent + node.
- Remove: `removeNode(nodeAlias)`; the controller rebalances.

## Rebalance

```dolphindb
rebalanceChunksAmongDataNodes()     // move chunks to equalize load
rebalanceChunksWithinDataNode()     // within-node volumes
```

## Rolling upgrade

1. Upgrade controllers first (one at a time if HA).
2. Upgrade data nodes one by one.
3. Upgrade compute nodes / web.
4. Verify with `version()` and run smoke queries.

## Recovery

Chunk recovery runs automatically after node restart. Monitor:

```dolphindb
getRecoveryTaskStatus()
getRecoveryWorkerNum()
```

## See also

- Other files in this directory (`cluster_manage.md`, `perf_man.md`, `multi_cluster_management.md`, `cluster_async_replc.md`, etc.).
- `backup-restore.md`, `security.md`.
- Upstream: `documentation-main/tutorials/single_machine_cluster_deploy.md`
  and friends.
