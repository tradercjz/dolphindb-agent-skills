# DolphinDB Web — browser admin UI reference

18 pages mirrored from upstream `db_distr_comp/db_man/web/`. These
cover the built-in web console at `http://<controller>:<port>/`: how to
use each panel, not the underlying CLI / function calls.

## Contents
- Getting started & intro
- Cluster / overview
- Access, config, plugins
- Stream graph & monitor
- Data & query tools
- Jobs, logs, sessions
- Utilities (git tabs, regular inspection, CEP, Kafka/MQTT, features)

---

## Getting started & intro

| File | What's in it |
|------|-------------|
| `GettingStart.md` | First-use tour of the web console. |
| `intro.md`        | One-paragraph overview. |

## Cluster / overview

| File | |
|------|--|
| `cluster_overview.md` | Cluster topology panel — nodes, roles, status. |

## Access, config, plugins

| File | |
|------|--|
| `access_man.md`       | User / role / privilege UI. Mirror of `authentication` + ACL concepts. |
| `cfg_man.md`          | Cluster / node config editor. |
| `feature_settings.md` | Toggling optional server features from the UI. |
| `plugin_management.md`| Install / load / unload plugins from UI. |

## Stream graph & monitor

| File | |
|------|--|
| `stream_graph.md`   | DAG visualisation of stream tables, engines, and subscribers. |
| `stream_monitor.md` | Throughput / backlog / handler stats for live streams. |

## Data & query tools

| File | |
|------|--|
| `querybuilder.md` | Visual query builder on top of DFS tables. |
| `Shell.md`        | Web-based DolphinDB shell — interactive scripts, charts, markdown. |
| `cep.md`          | CEP engine status + rule inspection in UI. |

## Jobs, logs, sessions

| File | |
|------|--|
| `job_man.md`           | Batch / scheduled job manager. |
| `log.md`               | Log viewer. |
| `session_management.md`| Kill / inspect live sessions. |

## Utilities

| File | |
|------|--|
| `git_multiple_tabs.md` | Multi-tab editor with Git integration. |
| `regulr_inspection.md` | "Regular inspection" periodic health reports. |
| `kafka_mqtt.md`        | UI for configuring Kafka / MQTT ingestion. |

## See also

- `../README.md` — full 90-admin hub (cluster, ACL, backup, monitoring).
- `../omc/` — Operations & Management Console (separate product).
- `../../../reference/plugins-catalog.md` — plugin one-liners.
