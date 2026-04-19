# Tutorials — curated index

## Contents
- Deployment (standalone / cluster / docker / k8s / cloud)
- Database & tables (engines, partition, in-memory, rebalance)
- Data import & migration (CSV, DataX, from other DBs, Debezium / Kafka CDC)
- SQL & querying (dialect, TopN, DECIMAL, time comparison)
- Streaming & engines (replay, aggregators, HA, order-book, capital-flow)
- Factor calculation (HF/LF, evaluation, attribution, risk model)
- Backtest & simulated matching
- Quant finance cases (OHLC, K-line, CSI1000, volatility, FICC, FX, MVO)
- IoT, machine learning, Python interop
- Performance & tuning, scripting / language advanced
- Admin / security / monitoring
- Plugin development, third-party integrations

281 end-to-end tutorials mirrored from upstream. All are in Chinese, all
are runnable on DolphinDB Server (version usually stated in the tutorial
header). Below: which file to read for which scenario.

Start here: `about_tutorials.md`, `new_users_finance.md`,
`dolphindb_user_guide.md`.

---

## Deployment

| Topic | File |
|-------|------|
| Single-node | `standalone_server.md`, `ARM_standalone_deploy.md` |
| Multi-machine cluster | `single_machine_cluster_deploy.md`, `multi_machine_cluster_deployment.md` |
| HA cluster | `ha_cluster_deployment.md`, `haProxy_best_practices.md`, `haStreaming.md` |
| Docker | `docker_single_deployment.md`, `docker-compose_high_cluster.md` |
| Kubernetes | `k8s_deployment.md`, `k8s_deployment_in_AWS.md`, `k8s_deployment_in_Aliyun.md` |
| Cloud | `cloud_deployment_with_terraform.md`, `edge_to_cloud.md` |
| Linux prep | `prep_linux_for_deploy.md` |
| Scale-out | `scale_out_cluster.md`, `cluster_scaleout_perf_test.md` |
| Startup / crash | `Startup.md`, `node_startup_process_and_questions.md`, `node_startup_exception.md`, `how_to_handle_crash.md` |
| Rolling upgrade | `gray_scale_upgrade_ha.md`, `dolphindb_update.md` |
| Service management | `service_deployment_and_migration.md`, `nginx_dolphindb.md` |

## Database & tables

| Topic | File |
|-------|------|
| Overview | `database.md`, `database_and_table_creation_details.md`, `database_and_table_creation_wizard.md` |
| Storage engines | `tsdb_engine.md`, `tsdb_explained.md`, `textdb.md`, `oltp_in-memory_storage_engine_non-embedded_version_tutorials.md`, `ha_mvcc_table.md` |
| Partition & best practice | `best_practices_for_partitioned_storage.md`, `high_freq_data_storage_and_analysis.md`, `best_practice_for_storage_compute_separation.md` |
| In-memory tables | `in_memory_table.md`, `partitioned_in_memory_table.md`, `cachedtable.md`, `panel_data.md` |
| Add / alter / soft-delete | `add_Column.md`, `soft_delete.md` |
| Storage internals | `redoLog_cacheEngine.md`, `Compute_Node.md` |
| Rebalance | `Data_Move_Rebalance.md`, `repair_chunk_status.md` |

## Data import & migration

| Topic | File |
|-------|------|
| Generic import | `import_data.md`, `import_csv.md`, `data_import_details.md`, `data_ETL.md`, `LoadDataForPoc.md`, `stockdata_csv_import_demo.md` |
| DataX | `datax_writer.md` |
| From MySQL / Postgres / Oracle / SQLServer / Greenplum / Redshift / InfluxDB / ClickHouse / kdb / OceanBase | `MySQL_to_DolphinDB.md`, `migrate_data_from_Postgre_and_Greenplum_to_DolphinDB.md`, `Oracle_to_DolphinDB.md`, `SQLServer_to_DolphinDB.md`, `Migrate_data_from_Redshift_to_DolphinDB.md`, `Migrate_data_from_InfluxDB_to_DolphinDB.md`, `ClickHouse_to_DolphinDB.md`, `kdb_to_dolphindb.md`, `OceanBase_to_DolphinDB.md` |
| Python file formats | `Python_HDF5_vs_DolphinDB.md`, `DolphinDB_VS_PythonFile_Storage.md`, `pickle_comparison.md` |
| Exchange / historical / L2 | `exchdata_exchange_historical_stock_data_auto_import_module_tutorial.md`, `ImportTLData_toturial.md`, `amd_best_prac.md`, `best_practice_for_mdl.md`, `insight_plugin.md`, `instrument_and_mktdata.md` |
| Debezium / Kafka CDC | `Debezium_and_Kafka_data_sync.md`, `Debezium_Kafka_Oracle_sync.md`, `Debezium_Kafka_PostgreSQL_sync.md`, `debezium_kafka_real_time_synchronization_of_oracle_11g_data.md`, `kafka_mqtt.md` |
| Cross-cluster sync | `data_sync_among_clusters.md`, `async_replication.md` |

## SQL & querying

| Topic | File |
|-------|------|
| Standard SQL, DolphinDB dialect | `std_sql_ddb.md`, `ddb_sql_cases.md`, `DolphinDB_Explain.md`, `sql_performance_optimization_wap_di_rv.md` |
| TopN | `DolphinDB_TopN.md` |
| Decimal semantics | `DECIMAL.md`, `DECIMAL_Calculation_Characteristics.md` |
| Time comparison | `ddb_comparison_rules_of_time_types.md`, `timezone.md` |
| Cachedtable / stored results | `cachedtable.md` |
| Best-price selection | `best_price_selection.md` |

## Streaming & engines

| Topic | File |
|-------|------|
| Intro | `streaming_tutorial.md`, `getting_started_with_cep_engine.md`, `StreamEngineParser.md` |
| Replay | `data_replay.md`, `stock_market_replay.md`, `stock_market_replay_2.md`, `appendices_market_replay_bp.md` |
| Aggregators / timer | `stream_aggregator.md`, `streaming_timer.md`, `reactive_state_engine.md`, `stateful_stream_operators.md` |
| Autopipe | `streaming_auto_sub.md`, `streaming_auto_sub_2.md` |
| HA streaming | `haStreaming.md` |
| Realtime correlation / IOPV | `streaming-real-time-correlation-processing.md`, `streaming-real-time-correlation-processing_2.md`, `streaming_IOPV.md`, `streaming_IOPV_2.md` |
| Capital flow (daily / order-by-order) | `streaming_capital_flow_daily.md`, `streaming_capital_flow_daily_2.md`, `streaming_capital_flow_order_by_order.md`, `streaming_capital_flow_order_by_order_2.md` |
| Anomaly alerts | `Anomaly_Detection_Engine.md`, `streaming_engine_anomaly_alerts.md`, `streaming_engine_anomaly_alerts_2.md` |
| Futures trading | `stream_computing_in_futures_trading.md` |
| Financial quant | `str_comp_fin_quant.md`, `str_comp_fin_quant_2.md` |
| Order-book snapshot | `orderBookSnapshotEngine.md`, `insight_plugin_orderbook_engine_application.md` |
| Order splitting CEP | `order_splitting_with_cep.md`, `order_splitting_with_cep_advanced.md` |
| Stock price increment | `rt_stk_price_inc_calc.md`, `rt_stk_price_inc_calc_2.md` |
| L2 stock data | `l2_stk_data_proc.md`, `l2_stk_data_proc_2.md` |

## Factor calculation

| Topic | File |
|-------|------|
| Best practices (core) | `best_practice_for_factor_calculation.md`, `best_practices_for_multi_factor.md` |
| Evaluation / attribution | `factor_evaluation_framework.md`, `factor_attribution_analysis.md`, `Practical_Factor_Analysis_Modeling.md` |
| Risk model | `multi_factor_risk_model.md` |
| HF / LF factors | `hf_factor_streaming.md`, `hf_factor_streaming_2.md`, `hf_to_lf_factor.md`, `l2_snapshot_factor_calc.md`, `l2_snapshot_factor_calc_2.md` |
| Fund factor | `fund_factor_contrasted_by_py.md` |
| Brinson / Campisi | `brinson.md`, `campisi.md` |

## Backtest & simulated matching

See **`../backtest/README.md`** for the decision hub.

| Topic | File |
|-------|------|
| Intro / margin-trading usage | `backtest_introduction_usage.md` |
| Stock | `stock_backtest.md`, `daily_stock_portfolio_backtest.md` |
| Futures CTA | `cta_strategy_implementation_and_backtesting.md`, `cta.md`, `futures_minute_frequency_cta_strategy_backtest_example.md` |
| Options | `backtest_volatility_timing_vertical_spread.md`, `IV_Greeks_Calculation_for_ETF_Options_Using_JIT.md` |
| Multi-asset | `multi_asset_backtest.md` |
| MES | `backtesting_using_MatchingEngineSimulator.md`, `matching_engine_simulator.md` |

## Quant finance — cases

| Topic | File |
|-------|------|
| Overview | `quant_finance_examples.md`, `new_users_finance.md`, `orca_finance.md`, `orca_finance_position.md` |
| OHLC / K-line | `OHLC.md`, `OHLC_2.md`, `k_line_calculation.md`, `k_line_calculation .md`, `displaying_the_dolphindb_k-line_with_klinechart.md` |
| CSI 1000 index | `CSI_1000.md`, `CSI_1000_2.md` |
| Volatility ML | `ml_volatility.md`, `ml_volatility_2.md`, `volatility_prediction.md` |
| FICC | `ficc_func_uasge_and_performance.md`, `ficc_funcs_application.md` |
| FX swap / curve / surface | `FxSwapValuation.md`, `curve_surface_builder.md` |
| Portfolio MVO / SOCP | `MVO.md`, `socp_usage_case.md`, `monte_carlo_simulation.md` |
| Public fund analysis | `public_fund_basic_analysis.md` |
| Financial mock data | `financial_mock_data_generation_module.md` |
| Vanna / gplearn / shark | `vanna.md`, `gplearn.md`, `shark_gplearn_application.md`, `shark_graph.md` |
| Market condition adjustments | `market_condition_adjustments.md` |
| Probabilistic / statistical | `probabilistic_and_statistical_analysis.md`, `empyrical.md` |
| Trip duration forecast | `forecast_taxi_trip_dura.md`, `forecast_taxi_trip_dura_2.md` |

## IoT

| Topic | File |
|-------|------|
| Overview / demo | `iot_examples.md`, `iot_demo.md`, `iot_demo_2.md`, `ddb_str_app_iot.md`, `ddb_str_app_iot_2.md` |
| Anomaly / O&M | `iot_anomaly_detection.md`, `iot_anomaly_detection_2.md`, `Iot_intelligent_O&M.md` |
| kNN, vibration, waveform | `knn_iot.md`, `knn_iot_2.md`, `random_vibr_sig_analysis.md`, `random_vibr_sig_analysis_2.md`, `waveform_data_storage.md`, `waveform_data_storage_2.md`, `Virbration_Monitor_Fault_Diagnose.md` |
| Earthquake / electricity | `earthquake_prediction_ddb_ml.md`, `earthquake_prediction_ddb_ml_2.md`, `efficient_power_trading_solutions.md` |
| Node-RED / Telegraf / Grafana | `node_red_tutorial_iot.md`, `ddb_telegraf_grafana.md` |
| Driving habits | `behavioral_profiling_of_driving_habits.md` |
| Multi-source fusion | `iot_multisource_fusion_query.md`, `iot_query_case.md` |

## Machine learning / AI

| Topic | File |
|-------|------|
| General ML | `machine_learning.md`, `ai_dataloader_ml.md` |
| LibTorch | `dolphindb_tensor_libtorch_tutorial.md` |

## Python interop

| Topic | File |
|-------|------|
| pip / data sync | `pip_ddb.md`, `Python_Celery.md` |
| Function parity | `function_mapping_py.md` |
| Comparison | `DolphinDB_VS_PythonFile_Storage.md`, `Python_HDF5_vs_DolphinDB.md`, `pickle_comparison.md` |
| hybrid paradigms | `hybrid_programming_paradigms.md` |

## Performance & tuning

| Topic | File |
|-------|------|
| API perf | `api_performance.md` |
| Memory | `memory_management.md`, `oom_settlement.md`, `oom_settlement_2.md`, `perf_opti_glibc.md` |
| Threading / jobs | `threading_model.md`, `thread_intro.md`, `thread_intro_2.md`, `job_management_tutorial.md`, `job_management_tutorial_2.md` |
| JIT | `jit.md`, `IV_Greeks_Calculation_for_ETF_Options_Using_JIT.md` |
| SQL optimization | `sql_performance_optimization_wap_di_rv.md`, `DolphinDB_Explain.md`, `DolphinDB_TopN.md` |
| Tracing / stack | `guide_to_obtaining_stack_traces.md`, `faultAnalysis.md` |

## Scripting / language

| Topic | File |
|-------|------|
| Meta-programming | `meta_programming.md`, `macro_var_based_metaprogramming.md`, `metacode_derived_features.md`, `metacode_derived_features_2.md` |
| General computing | `general_computing.md`, `func_progr_cases.md` |
| UDAF | `udaf.md` |
| Window / panel | `window_cal.md`, `panel_data.md` |
| Array vector / matrix | `Array_Vector.md`, `matrix.md` |
| K object | `k.md` |
| Summary / statistics | `generate_large_scale_statistics_with_summary.md` |
| Unit testing | `unit_testing.md` |
| Ten overlooked details | `the_ten_most_overlooked_details_of_programming.md` |
| Modules | `tu_modules.md`, `module_tutorial.md`, `module_development_guide.md`, `module_code_versioning_and_rights_management.md`, `module_doc_writing_guide.md`, `module_testing_guide.md` |

## Admin / security / monitoring

| Topic | File |
|-------|------|
| ACL / security | `ACL_and_Security.md`, `ACL_and_Security_2.md`, `non-standard_permission_management.md`, `user_level_resource_tracking.md`, `oauth.md`, `e6_97_a0_e6_a0_87_e9_a2_9810.md` |
| Backup / restore | `backup-restore-new.md`, `backup_restore_before_208.md`, `restore-backup.md` |
| Cluster monitor | `cluster_monitor.md`, `zabbix_cluster_monitoring.md`, `prometheus_and_ruleEngine_integration.md`, `promethues2.md` |
| Scheduled jobs | `scheduledJob.md`, `scheduledJob_2.md` |
| Log analysis | `best_practices_for_log_monitoring.md`, `log_analysis_tool_user_manual.md`, `log_searcher.md`, `effective-log-storage-and-retrieval.md` |
| Cache clear | `clear_cache.md` |
| Usage guidelines | `usage_guidelines.md` |

## Plugin development

| Topic | File |
|-------|------|
| How to develop | `plugin_development_tutorial.md`, `cpp_data_io.md` |
| Third-party integration examples | `httpclient_msg_case.md`, `redis_plugin_tutorial.md`, `arrow_plugin_usage.md`, `datax_writer.md` |

## Third-party integrations

| Topic | File |
|-------|------|
| Dashboard / BI | `dashboard_tutorial.md`, `web_chart_integration.md`, `data_interface_for_redash.md` |
| Scheduler | `ddb_airflow.md`, `dolphinscheduler_integration.md` |

## Workshops / misc

- `standalone_server.md`, `new_users_finance.md` — day-1 primer.
- `usage_guidelines.md` — things to know before shipping to production.
- `csap.md`, `interface_development.md`, `xtp.md` — interface / adapter case studies.

## Tips

- `*_2.md` files are **extended versions** of the non-`_2` file (same topic, longer case study).
- All tutorials assume a specific DolphinDB version stated in the header; double-check for version-specific API differences.
- Code blocks are directly pastable into the DolphinDB Web notebook once the referenced sample data is loaded.
