<!-- Auto-mirrored from upstream `documentation-main/plugins/odbc/odbc_faq.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# Oracle 的 ODBC 驱动，包含 SQLDriverConnectW 的实现
nm -D /usr/local/oracle/instantclient_21_7/libsqora.so.21.1 | grep SQLDriverConnectW
0000000000076730 T SQLDriverConnectW
```

### 常见系统各数据库的ODBC 驱动推荐列表

| 数据库/操作系统 | ubuntu | CentOS 7 | CentOS 8 | Rocket 8 | Alpine |
| --- | --- | --- | --- | --- | --- |
| MySQL | 官方驱动(8.18版本以下） | 官方驱动(8.18版本以下） | CentOS 7系统的官方驱动(8.18版本以下） | CentOS 7系统的官方驱动(8.18版本以下） | CentOS 7系统的官方驱动(8.18版本以下） |
| SQL Server | odbc 插件目录下的 FreeTDS 用于连接 SQL Server 的 ODBC 驱动 | odbc 插件目录下的 FreeTDS 用于连接 SQL Server 的 ODBC 驱动 | odbc 插件目录下的 FreeTDS 用于连接 SQL Server 的 ODBC 驱动 | odbc 插件目录下的 FreeTDS 用于连接 SQL Server 的 ODBC 驱动 | odbc 插件目录下的 FreeTDS 用于连接 SQL Server 的 ODBC 驱动 |
| SQLite | 官方驱动 | 官方驱动 | 官方驱动 | 官方驱动 | 官方驱动 |
| Oracle | 官方驱动 | 官方驱动 | 官方驱动 | 官方驱动 | 官方驱动 |
| ClickHouse | 官方驱动（1.1.10以上） | 官方驱动（1.1.10以上） | 官方驱动（1.1.10以上） | 官方驱动（1.1.10以上） | 官方驱动（1.1.10以上） |
| PostgreSQL | 官方驱动 | 官方驱动 | 官方驱动 | 官方驱动 | 官方驱动 |
