<!-- Auto-mirrored from upstream `documentation-main/tutorials/market_condition_adjustments.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 股票复权因子和复权行情计算

量化交易中，经常需要对股票历史行情进行**复权处理**，以消除分红、送股、拆股等权息事件对股价走势的影响。本教程面向已掌握 DolphinDB
基础操作（部署、建表、代码调试）的初级量化用户，指导如何基于未复权的股票日 K
数据计算**前复权**和**后复权**因子，并生成相应的复权行情数据。我们将结合**“涨跌幅复权”**算法解释计算逻辑，在 DolphinDB
中逐步实现。

## 1. 未复权行情

未复权行情指未经任何权息调整的股票价格历史，即交易当日的收盘价直接反映市场的实际交易价格。不复权数据会在分红、配股或拆股等权息事件发生后出现价格的非自然跳变。例如，某股票在除权除息日前股价为10元，因10送10拆股，除权日开盘价骤降为5元。如果直接使用未复权价格绘制K线图，将看到股价在除权日出现约50%的断崖式下跌。但这并非公司基本面变化导致的真实跌幅，而是拆股造成的名义价格变化。未复权行情虽然保留了所有历史交易的真实价格，但无法直观体现股票真实涨跌幅，历史K线存在明显的“缺口”。

在未复权数据中，常见字段包括交易日期、股票代码、开盘价、收盘价、最高价、最低价和昨日收盘价等。例如：

```
trade_date   ts_code     open     close    pre_close   ...
2008.06.12   600519.SH   157.48   151.21   157.49      ...
2008.06.13   600519.SH   148.11   149.49   151.21      ...
2008.06.16   600519.SH   147.70   144.50   148.65      ...
2008.06.17   600519.SH   143.51   141.97   144.50      ...
```

上表展示了贵州茅台(600519.SH)在2008年6月12日至17日的未复权行情片段。其中2008.06.16为除权除息日，可见未复权数据的
pre\_close（昨日收盘价）在除权日发生了跳变：2008.06.16的 pre\_close 为148.65**，**而上一个交易日2008.06.13的
close
为149.49。这种跳变使2008.06.16的日K线相较前一日出现缺口。如果不进行复权处理，直接计算涨跌幅会产生误导。例如2008.06.16未复权收盘价144.50相对上一个交易日的实际收盘149.49看似下跌了3.3%（`(144.5-149.49)\149.49`），但事实上这包含了分红/拆股因素，并非投资者实际持股损失。

**复权**就是针对这类情况，对历史股价进行权息修正，使不同日期的股价具有可比性。通过复权，可将除权前后的行情曲线平滑对接，保持股价走势的连续性和涨跌幅的准确性。复权方式主要有两种：**后复权**（保持初始价不变，调整未来价）和**前复权**（保持当前价不变，调整历史价）。下面我们分别介绍后复权和前复权的计算方法，并使用
DolphinDB 实现复权因子计算和复权行情的生成。

## 2. 复权解释

**后复权**是以上市首日（或选定基准日）的价格为基准，对后续股价进行调整。通俗来说，后复权假设投资者始终持有最初的一股股票并参与所有分红送股，将这些权息折算成股价增长。因此，后复权后的当前股价会高于实际价，体现累计权息收益（股票真实价值的增加）。使用后复权行情可以方便地看到如果从初始买入并持有至今，股票价格累积上涨了多少。但是，由于配股等可能需要额外投入，后复权计算的收益率不一定等同于投资者实际收益，只是一种理论上的累计增值表现。

**前复权**是以最新价为基准，将过去的历史价格进行调整。这种处理保持近期股价的真实水平，并将除权前的价格向下平移，使整个价格序列衔接连续。

### 2.1 后复权

要生成后复权行情，需要先计算**后复权因子**。后复权因子是一组随时间变化的倍率，用于把未复权价格调整到以初始价格为基准的水平。“涨跌幅复权法”定义后复权因子的公式为：

`后复权因子 = （前一交易日的收盘价 ÷ 当日的昨日收盘价）向后累乘`

这里的“当日的昨日收盘价”指未复权数据中的 pre\_close（通常由交易所提供，遇除权日该值已按权息调整）。根据该公式：

* 若当天无权息事件，则当日的昨日收盘价 = 昨日收盘价，后复权因子 = 昨收/昨收 = 1，因子保持不变。
* 若当天为除权除息日，则当日的昨日收盘价经过权息调整，与昨日实际收盘价不同，后复权因子 = 前一交易日的收盘 ÷ 当日的昨日收盘价，将大于 1。

后复权因子在上市首日定义为1。当无权息事件时，因子不变；每遇到一次除权除息，因子按照上述比值乘上一个放大倍数。这意味着后复权因子等于历次权息比率的累积乘积，最终将用于放大未复权价格。

![](images/market_condition_adjustments/2-1.png)

图 1. 图 2-1 后复权因子和行情计算示意图

如上图所示，贵州茅台(600519.SH)在2002.07.25发生第一次10转1股派6元(含税)：

* 未复权行情中，2002.07.25为第一个除权日，当日的昨日收盘价从36.40降至32.55（红框标示）
* 根据公式计算得到后复权因子为1.11828（36.40\32.55）
* 后复权行情等于未复权行情中的所有与价格相关的字段乘以后复权因子，图中以开盘价 open 为例展示了计算逻辑

通过后复权因子的累乘，我们将所有历史价格都折算到了以最初价格为基准的水平。**后复权行情**可以用未复权行情乘以对应日期的后复权因子得到。

### 2.2 前复权

同理，要生成前复权行情，需要先计算**前复权因子**。前复权因子用于将未复权历史价格按一定比例缩减。根据“涨跌幅复权”算法，前复权因子的定义如下：

`前复权因子 = （当日的昨日收盘价 ÷ 前一交易日的收盘价）向前累乘`

其原理与后复权因子互为一个缩放比例：当发生权息时，未复权前收价降低，导致前复权因子小于1；无权息时，当日前收与昨日收盘相等，则前复权因子 =
1。前复权因子在最新一次除权除息日后的首个交易日被重置为1。换言之，每遇一次新的权息事件，前复权因子会跳变到较小的值（因为当日前收价经调整比昨日实际收盘价低），随后又逐日增大回至1，直至下一次权息事件。

![](images/market_condition_adjustments/2-2.png)

图 2. 图 2-2 前复权因子和行情计算示意图

如上图所示，贵州茅台(600519.SH)在2002.07.25发生第一次10转1股派6元(含税)：

* 未复权行情中，2002.07.25为第一个除权日，当日的昨日收盘价从36.40降至32.55（红框标示）
* 根据公式计算得到前复权因子为0.89423（32.55\36.40）
* 前复权行情等于未复权行情中的所有与价格相关的字段乘以前复权因子，图中以开盘价 open 为例展示了计算逻辑

概括而言，**前复权因子**通过将未复权价格依次乘上这些小于1的因子，可以把过去的股价调整到和当前价格同一个基准之下。

## 3. 生产代码实现

### 3.1 未复权行情存储

以附录未复权 csv 行情数据为例，该数据通常由交易所提供，遇除权日对当日的昨收价按权息调整。

创建数据库和分区表：

```
if(not existsDatabase("dfs://stock_day_k")){
    create database "dfs://stock_day_k"
    partitioned by VALUE(2025.01M..2025.05M),
    engine="OLAP"
}else{
    print("The database has created.")
}

create table "dfs://stock_day_k"."stock_day_k"(
    trade_date  DATE[comment="交易日"],
    ts_code     SYMBOL[comment="股票代码"],
    open        DOUBLE[comment="开盘价"],
    high        DOUBLE[comment="最高价"],
    low         DOUBLE[comment="最低价"],
    close       DOUBLE[comment="收盘价"],
    pre_close   DOUBLE[comment="昨日收盘价"],
    vol         DOUBLE[comment="成交量"],
    amount      DOUBLE[comment="成交额"]
)
partitioned by trade_date
```

导入未复权 csv 行情数据，读者根据实际的csv文件路径修改：

```
csvPath = "/hdd/hdd2/tutorial/stock_adj/600519.csv"
data = loadText(csvPath)
loadTable("dfs://stock_day_k", "stock_day_k").append!(data)
```

查看贵州茅台(600519.SH)在2008年6月12日至17日的未复权行情片段：

```
stock_day_k = loadTable("dfs://stock_day_k", "stock_day_k")

select
    top 10 trade_date,ts_code,open,close,pre_close
from stock_day_k
where ts_code="600519.SH", trade_date>=2008.06.12
```

返回：

![](images/market_condition_adjustments/3-1.png)

### 3.2 后复权计算和存储

创建存储后复权因子和行情的数据库和分区表：

```
if(not existsDatabase("dfs://stock_back")){
    create database "dfs://stock_back"
    partitioned by VALUE(2025.01M..2025.05M),
    engine="OLAP"
}else{
    print("The database has created.")
}

create table "dfs://stock_back"."stock_back"(
    trade_date  DATE[comment="交易日"],
    ts_code     SYMBOL[comment="股票代码"],
    open        DOUBLE[comment="开盘价"],
    high        DOUBLE[comment="最高价"],
    low         DOUBLE[comment="最低价"],
    close       DOUBLE[comment="收盘价"],
    pre_close   DOUBLE[comment="昨日收盘价"],
    vol         DOUBLE[comment="成交量"],
    amount      DOUBLE[comment="成交额"],
    adj_back    DOUBLE[comment="后复权因子值"]
)
partitioned by trade_date
```

根据计算公式从未复权行情得到后复权因子和后复权行情，并且存入相应的库表：

```
//计算后复权因子
def calOneCodeFunc(code){
    /*@test
    code = "600519.SH"
    */
    //把1个票1天的未复权行情查到内存
    one_code_data =
        select *
        from loadTable("dfs://stock_day_k", "stock_day_k")
        where ts_code=code
    //停牌交易日close价格为NULL，特殊处理当日的收盘价
    update one_code_data
    set fill_close=iif(close==NULL and pre_close==prev(close),
                        prev(close),
                        iif(close==NULL,pre_close,close))
    //计算后复权因子
    update one_code_data
    set adj_back=iif(cumcount(fill_close)==1, 1, cumprod(prev(fill_close)\pre_close))
    //包含复权因子和复权行情的表
    result =
        select
            trade_date,
            ts_code,
            open*adj_back as open,
            high*adj_back as high,
            low*adj_back as low,
            close*adj_back as close,
            pre_close*adj_back as pre_close,
            vol,
            amount,
            adj_back
        from one_code_data
    return result
}
//处理未复权行情表内全部股票
calCodes = exec distinct ts_code from loadTable("dfs://stock_day_k", "stock_day_k")
//按照股票代码并行计算
stock_back = ploop(calOneCodeFunc, calCodes).unionAll()
//写入后复权分区表
loadTable("dfs://stock_back", "stock_back").append!(stock_back)
```

部分重要除权日的数据查询：

```
select *
from loadTable("dfs://stock_back", "stock_back")
where ts_code="600519.SH", trade_date in [2002.07.25,2003.07.14,2004.07.01]
```

返回：

![](images/market_condition_adjustments/3-2.png)

### 3.3 前复权计算和存储

创建存储前复权因子和行情的数据库和分区表：

```
if(not existsDatabase("dfs://stock_pre")){
    create database "dfs://stock_pre"
    partitioned by VALUE(2025.01M..2025.05M),
    engine="OLAP"
}else{
    print("The database has created.")
}

create table "dfs://stock_pre"."stock_pre"(
    trade_date  DATE[comment="交易日"],
    ts_code     SYMBOL[comment="股票代码"],
    open        DOUBLE[comment="开盘价"],
    high        DOUBLE[comment="最高价"],
    low         DOUBLE[comment="最低价"],
    close       DOUBLE[comment="收盘价"],
    pre_close   DOUBLE[comment="昨日收盘价"],
    vol         DOUBLE[comment="成交量"],
    amount      DOUBLE[comment="成交额"],
    adj_pre     DOUBLE[comment="前复权因子值"]
)
partitioned by trade_date
```

根据计算公式从未复权行情得到前复权因子和前复权行情，并且存入相应的库表：

```
def calOneCodeFunc(code){
    /*@test
    code = "600519.SH"
    */
    //把1个票1天的未复权行情查到内存
    one_code_data =
        select *
        from loadTable("dfs://stock_day_k", "stock_day_k")
        where ts_code=code
    //停牌交易日close价格为NULL，特殊处理当日的收盘价
    update one_code_data
    set fill_close=iif(close==NULL and pre_close==prev(close),
                        prev(close),
                        iif(close==NULL,pre_close,close))
    //计算后复权因子
    update one_code_data
    set adj_back=iif(cumcount(fill_close)==1, 1, cumprod(prev(fill_close)\pre_close))
    //计算前复权因子
    update one_code_data
    set adj_pre=adj_back/last(adj_back)
    //包含复权因子和复权行情的表
    result =
        select
            trade_date,
            ts_code,
            open*adj_pre as open,
            high*adj_pre as high,
            low*adj_pre as low,
            close*adj_pre as close,
            pre_close*adj_pre as pre_close,
            vol,
            amount,
            adj_pre
        from one_code_data
    return result
}
//处理未复权行情表内全部股票
calCodes = exec distinct ts_code from loadTable("dfs://stock_day_k", "stock_day_k")
//按照股票代码并行计算
stock_pre = ploop(calOneCodeFunc, calCodes).unionAll()
//写入前复权分区表
loadTable("dfs://stock_pre", "stock_pre").append!(stock_pre)
```

部分重要除权日的数据查询：

```
select *
from loadTable("dfs://stock_pre", "stock_pre")
where ts_code="600519.SH", trade_date in [2002.07.25,2003.07.14,2004.07.01]
```

返回：

![](images/market_condition_adjustments/3-3.png)

## 4. 常见问题解答（FAQ）

### 4.1 复权因子计算结果不正确

**已知可能原因：**

1. 未复权行情数据不完整，特别是在停牌期间的数据，可以把附录给到的贵州茅台数据作为基准，对比实际库里面的股票数据是否完整，特别注意2006.05.19-2006.05.24期间的数据值是否一致
2. 未复权行情数据不正确，可以用附录的样例数据做交叉校验

**处理方法：**

* 补齐数据，保证未复权行情数据的数据质量

### 4.2 与三方数据厂商有误差

**已知可能原因：**

1. 小数点保留位数
2. 复权计算方法有差异

**处理方法：**

* 保证未复权数据质量的前提下，可以根据真实数据推导，详细分析误差原因后进行决策

## 5. 附录

未复权csv行情数据：[600519.csv](script/market_condition_adjustments/600519.csv)

后复权csv行情数据：[600519\_back.csv](script/market_condition_adjustments/600519_back.csv)

前复权csv行情数据：[600519\_pre.csv](script/market_condition_adjustments/600519_pre.csv)

教程代码：[stock\_adj.dos](script/market_condition_adjustments/stock_adj.dos)
