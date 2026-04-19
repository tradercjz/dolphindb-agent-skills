<!-- Auto-mirrored from upstream `documentation-main/tools/superset.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 根据提示输入用户名及密码
flask fab create-admin
superset init
```

![](images/superset/1-1.png)

图 1. 图 1-1 初始化 Superset

如图，Superset 初始化完成。

### 1.3 启动 Superset

启动 Superset，`-p` 选项可以指定服务端口，`-h` 指定监听地址。

```
superset run -h 0.0.0.0 -p 8088 --with-threads --reload --debugger
```

启动后，可通过浏览器输入地址 http://*ip:8088* ( -p 所指定的端口）访问。

![](images/superset/1-2.png)

图 2. 图 1-2 Superset登录界面

至此，Superset 部署完成。更多配置和管理方式，请参考 [Configuring Superset | Superset](https://superset.apache.org/docs/configuration/configuring-superset)。

## 2. 数据准备

由于 Superset 使用 catalog，schema 等概念来访问数据库，故需使用3.00.0及以上版本的
DolphinDB。准备可视化分析所需的案例数据集，包括创建 catalog、 snapshot 行情信息表，并使用 MockData 模块模拟一天的股票行情数据。

```
use MockData

createCatalog("stock")
use catalog stock

//创建行情分布式表snapshot
t = stockSnapShotPT("dfs://level2", "snapshot")
createSchema("stock", "dfs://level2", "level2")
// 生成模拟数据
data = stockSnapshot(2020.01.06, 100)
tableInsert(t, data)

select * from data limit 100

//创建共享表
tmp = select * from level2.snapshot limit 100000
share tmp as snapshotg
```

## 3. 连接至DolphinDB

案例数据准备完成之后，分别创建 DolphinDB 连接及数据集，使得 Superset 可以访问并使用 DolphinDB 中的数据。

### 3.1 创建连接

先点击右上角的 *Settings*，然后点击 *Database Connections*。

![](images/superset/3-1.png)

图 3. 图 3-1 添加数据库连接

点击右上角的 *+ DATABASE* 选项，选择连接的数据库为 DolphinDB。

![](images/superset/3-2.png)

图 4. 图 3-2 添加 DolphinDB 数据库连接

按照`dolphindb://user:password@host:port/catalog`的形式输入连接所需的参数，参数说明如下：

| **参数名称** | **说明** |
| --- | --- |
| user | 数据库用户名 |
| password | 数据库用户对应的密码 |
| host | DolphinDB 所在服务器的主机名或 IP |
| port | DolphinDB 监听端口 |
| catalog | 数据库目录名称 |

点击 *TEST CONNECTION* 测试连接能否成功，最后点击 *CONNECT* 连接数据库。

![](images/superset/3-3.png)

图 5. 图 3-3 配置数据库连接

成功连接后进入数据库界面，页面会展示出相关连接信息。

### 3.2 创建 dataset

Superset 使用数据集（dataset）管理数据，并以此做为图表的数据源。

![](images/superset/3-4.png)

图 6. 图 3-4 创建 dataset

点击 *+DATASET*，依次选择数据库连接，SCHEMA，TABLE，点击 *CREATE DATASET AND CREATE
CHART*，后续的步骤 *CREATE CHART* 可以先忽略。除了分布式表，也可以选择 \_shared\_table
来选取共享内存表。在操作时，若 Superset 查询的库表并非最新的元信息（Superset
为了提高与数据库交互的效率，一般会缓存数据库元信息这种不太更新的数据），可以点击刷新按钮更新元数据。

## 4. 可视化分析

至此准备工作已经完成，进入数据可视化分析环节。可视化的魅力在于，能直观地展示数据情况，使得用户能够洞见数据中隐含的规律。以下案例将通过 Superset
绘制图表分析股票数据 ，包括市场深度趋势、成交量分布、行情展示等。

### 4.1 市场深度趋势图

市场深度指的是买卖挂单的数量和流动性情况，它反映了市场的供需情况。绘制折线趋势图，查看个股的买卖盘口深度随时间的变化趋势。

首先点击上方导航栏的 *Charts*，点击右上角的 *+ CHART* 进入创建图表的界面。然后选择上文中创建的 snapshot
数据集，选择图表为 Line Chart，点击 *CREATE NEW CHART*。

![](images/superset/4-1.png)

图 7. 图 4-1 创建趋势图

图表相关配置项说明如下，后文不再赘述。

* X-AXIS

X 轴，对于趋势图，通常是选择时间字段。

* TIME GRAIN

时间粒度，对 X 轴的时间列进行聚合，使得图表在更大的时间粒度（Minute，Day，Month等）上展示。

* FILTERS

过滤器，对应于 SQL 中的 where 条件。

* METRICS

图表展示的指标，建议选择 *CUSTOM SQL* 进行手动编写，比较高效。

![](images/superset/4-2.png)

图 8. 图 4-2 设置自定义 METRICS

分别输入 `sum(rowSum(OfferOrderQty))`,
`sum(rowSum(BidOrderQty))` 计算买卖队列。*CUSTOM SQL*
输入框中可以使用所有合法的 DolphinDB SQL，包括使用内置函数与自定义函数。因此您可以借助 DolphinDB
的分析能力（函数库及编程语言）完成一些复杂指标的可视化。 点击 *CREATE CHART* 生成图表。

![](images/superset/4-3.png)

图 9. 图 4-3 图表编辑界面

对于复杂的 SQL， 可以通过右上角的扩展菜单 *View query* 确认通过界面配置而生成的 SQL 是否正确。这也是常用的一个 debug
技巧。对于上述图表，SQL 如下。

```
SELECT minute(_"TradeTime") as _"minute_TradeTime", SUM(rowSum(OfferOrderQty)) as _"SUM_rowSum_OfferOrderQty", SUM(rowSum(BidOrderQty)) as _"SUM_rowSum_BidOrderQty"
FROM snapshotg
WHERE _"TradeTime" >= time("09:30:00.000") && _"TradeTime" < time("11:30:00.000") GROUP BY minute(_"TradeTime") ORDER BY _"SUM_rowSum_OfferOrderQty" desc
 LIMIT 10000;
```

最后，点击右上角的 *SAVE*，输入 *CHART NAME* 保存图表。

**图表调整**

在图表编辑 *CUSTOMIZE* 栏页中，可以对图表的格式进行调整。

![](images/superset/4-4.png)

图 10. 图 4-4 图表格式调整

例如给 X，Y 轴加上标签，调整 X, Y 轴的单位显示格式等。

### 4.2 最新行情信息

查看某个股票的最新的100笔行情信息，包括交易时间、价格、买卖10档量价（ArrayVector类型）等。

首先选择 Table，然后 FILTERS 中拖拽 SecurityID 选择股票。请注意字符串不需要手动加上引号或者双引号。接着，设置 ORDERING
按交易时间倒序，ROW LIMIT 选项设置为50。

![](images/superset/4-5.png)

图 11. 图 4-5 Table 图表编辑

图中，如果要调整字段展示格式的（默认是显示为 datetime 类型），选择 *CUSTOMIZE → CUSTOMIZE COLUME* →
%Y-%m-%d , 将 tradeDate 显示为日期格式。

![](images/superset/4-6.png)

图 12. 图 4-6 时间格式显示调整

### 4.3 成交量分布图

使用柱状图查看 “000076” 和 “000024” 股票每分钟的成交量。

首先，选择 Bar Char 图表，按照下图配置查询参数。然后 DIMENSIONS 中选择 “SecurityID”，FILTERS 筛选器中拖拽
“SecurityID”，“TradeDate” 字段，选择目标股票及交易日期。

![](images/superset/4-7.png)

图 13. 图 4-7 柱状图编辑

在 CUSTOMIZE中 可以选择水平/垂直控制柱形图的方向，点击 *DATA ZOOM* 可以缩放 X 轴范围，对感兴趣的 X
轴区间进行详细展示。

![](images/superset/4-8.png)

图 14. 图 4-8 柱状图 CUSTOMIZE

### 4.4 市场成交词云图

词云图可以非常直观地显示热点事件，在股票市场中，适合显示热门股票。

首先，选择 WordCloud 图表，按照下图配置查询参数。

![](images/superset/4-9.png)

图 15. 图 4-9 词云图编辑

然后，DIMENSION 选择 ”SecurityID“，METRIC 设置为 sum(totalValueTrade)， 以成交金额控制词条的大小。

![](images/superset/4-10.png)

图 16. 图 4-10 词云图 CUSTOMIZE

在 CUSTOMIZE 菜单栏中可以控制词条旋转的方向（随机、水平、平方）及字体大小。

### 4.5 总成交量图

使用 BIG NUMBER 图表展示个股在某个交易日的总成交量。

首先，选择 Big Number 图表，按照下图配置查询参数。然后在 METRIC 里写入 sum(NumTrades) 计算成交量，接着 FILTERS
中选择对应得股票。

![](images/superset/4-11.png)

图 17. 图 4-11 Big Number 图编辑

### 4.6 使用仪表盘

#### 4.6.1 创建仪表盘

仪表盘可以组合多个图表，展示多维度数据情况，并形成一定的叙事逻辑。使得用户能够从不同视角分析业务表现，发现规律和潜在问题。

点击 *Dashboards* 菜单创建仪表盘，将右侧的图表拖入仪表盘中，图表可以进行拖拽改变位置和大小。

![](images/superset/4-12.png)

图 18. 图 4-12 Dashboards 编辑

点击右上角 … 按钮，选择菜单中的 Edit properties 调整仪表盘属性，可以设置仪表盘的名称、权限、色彩主题等。

![](images/superset/4-13.png)

图 19. 图 4-13 仪表盘设置

#### 4.6.2 共享仪表盘

可以通过 Share → Copy permanlink to clipboard 可以获取仪表盘 URL 进行团队共享，访问者需要具备登录
Superset 的权限。Superset 支持工程化的权限管理，包括创建用户/组、设置图表的访问、编辑权限。在 Settings → List
Users/List Roles 可以对用户、角色的权限进行设置。

![](images/superset/4-14.png)

图 20. 图 4-14 用户与权限管理

默认生成的 URL 形如
http://*ip:port*/superset/dashboard/p/8pGRY22dK9D/，比较难以记忆，可以在 URL SLUG
设置一个助记码，如图4-13中的 stockMarket，并通过

http://*ip:port*/superset/dashboard/stockMarket 访问该仪表盘。

## 5. 总结

本文讲解了如何结合 DolphinDB 和 Superset 进行可视化分析，通过与 DolphinDB 的集成，Superset
可以实现一些复杂统计分析的可视化。总体而言，Superset 是一个图表丰富、简单易用的可视化软件。它通过调用 pydolphindb 的相关元数据接口来实现与
DolphinDB 交互数据，目前有些功能尚未完全兼容，说明如下:

* 在 Superset 所展示的数据中，您会观察到 TIME 类型的字段会加上固定的日期部分 1970-01-01, 这是因为 Superset 统一使用
  pandas.datetime 来显示时间，故必须要将 DolphinDB TIME 转为 YYYY-MM-dd HH:mm:ss 的形式。
* TIME GRAIN 不支持 Week，Month，Quarter 。
* 暂不支持Handlebars 图、Event Flow 图，Map 图。

有关 Superset 各图表的使用细节请参阅 [Exploring Data in Superset](https://superset.apache.org/docs/using-superset/exploring-data)。

另外需要说明的是，模拟数据和真实的市场数据差距较大，使得部分图表的展示效果可能与业务直觉不相符，仅用于学习和参考。
