<!-- Auto-mirrored from upstream `documentation-main/tools/sqltools.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# DolphinDB SQLTools 扩展使用指南

SQLTools 是一款轻量级的 Visual Studio Code 数据库管理扩展，通过插件驱动架构支持 MySQL、PostgreSQL、SQLite、Oracle
等主流数据库，为用户提供连接管理、SQL 查询、智能提示、查询历史等一站式高效开发体验。

DolphinDB VSCode Extension for SQLTools 是 vscode-sqltools 扩展的一个数据库驱动包，允许用户在 Visual Studio
Code 环境中通过 SQLTools 框架连接并操作 DolphinDB 数据库。用户可以在 Visual Studio Code 扩展商店中搜索并安装 DolphinDB
Driver For SQLTools。

**注：**当前扩展已在 **SQLTools v0.28.4 测试版本** 中完成验证和测试。

## 使用方法

### 1. 启动配置界面

点击 VSCode 活动栏中的 **SQLTools** 数据库图标，进入连接配置界面。

![](images/sqltools/1_1.png)

### 2. 选择数据库驱动

在 **Select your database driver** 字段中，选择 **DolphinDB** 驱动。

![](images/sqltools/1_2.png)

### 3. 配置连接信息

填写连接详细信息，标有星号 (\*) 的字段为必填项。

![](images/sqltools/1_3.png)

**配置项说明：**

* Connection Name\*：用于唯一标识不同连接的字符串。建议使用节点别名，例如 `local8848` 或
  `dnode1`。
* IP\*：目标节点的 IP 地址，例如 `localhost`。
* Port\*：节点所使用的端口号，例如 `8848`。
* Username：用于身份验证的用户名。默认管理员用户为 admin。
* Password：用于身份验证的密码。默认管理员密码为 123456。您可以登录后使用 `changePwd`
  函数修改密码。
* Auto Login：是否启用自动登录。默认值为 false。如果已提供用户名和密码，您可以选择启用此选项，以便在启动时自动完成身份验证。
* Show Records Default Limit：查询结果中每页默认显示的记录条数。

### 4. 测试并保存连接

完成配置后，点击 **TEST CONNECTION** 按钮以验证连接是否成功。

![](images/sqltools/1_4.png)

测试成功后，点击 **SAVE CONNECTION** 保存连接信息。

### 5. 连接并开始编写脚本

保存后，系统将显示基本的连接信息。确认信息无误后，点击 **CONNECT NOW** 建立连接。连接成功后，扩展会自动创建一个新的 SQL
文件供您编写脚本。

![](images/sqltools/1_5.png)

## 用户界面说明

![](images/sqltools/2_1.png)

### SQL Tools 区域

SQL Tools 区域显示了不同的连接信息。每个连接下包含三个子目录：

1. **数据库**
   * 包含分布式数据库和表的元数据信息。
   * 信息包括：数据库名、表名、列名和列类型。
2. **内存表**
   * 包含内存表的元数据信息。
   * 信息包括：表名、列名和列类型。
3. **变量**
   * 包含其他变量的信息。
   * 信息包括：变量名和变量类型（例如，矩阵、标量、集合等）。

### 对象操作

对于表类型对象，提供以下操作：

* 点击对象右侧的 **放大镜按钮** 来预览表数据。![](images/sqltools/2_2.png)
* 点击对象右侧的 **+ 按钮** 可生成对应的 `INSERT` 语句模板。![](images/sqltools/2_3.png)

### 脚本执行与结果

在脚本编辑器中编写 DolphinDB 脚本后，点击 **Run on active connection** 执行脚本。

![](images/sqltools/2_4.png)

**右侧的结果域将显示：**

* 脚本执行后返回的结果。
* 通过 `Show Table Records` 和 `Describe Table`
  命令查询得到的表记录和表结构信息。![](images/sqltools/2_5.png)

注：

在 DolphinDB 中执行包含多条语句的脚本时，结果区域默认只返回最后一条语句的结果。

* **结果区域功能按钮：**
  + **CONSOLE**：切换到 SQL 终端，输出详细的执行信息（通常包括返回对象的维度、类型和数据格式等）。
  + **RE-RUN QUERY**：重新执行当前语句。
  + **EXPORT**：将执行结果导出为 JSON 或 CSV 格式文件。
  + **OPEN**：将执行结果在新的标签页中以 CSV 或 JSON 格式打开查看。![](images/sqltools/2_6.png)

### 查询历史

左侧的 **QUERY HISTORY** 区域会保存针对特定连接的所有查询历史记录，方便用户回溯和再次执行。
