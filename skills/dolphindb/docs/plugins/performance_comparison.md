<!-- Auto-mirrored from upstream `documentation-main/plugins/performance_comparison.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 快照数据回调
def on_quote(context, quote, location, dest):
    #...
    # 策略逻辑
    ask_volume_sum = sum(x for x in quote.ask_volume)
    bid_volume_sum = sum(x for x in quote.bid_volume)
    if bid_volume_sum > 2 * ask_volume_sum and ask_volume_sum > 0:
        position = get_position(quote.instrument_id, context.book)
        if not position or position.volume < MAX_POSITION:
            order_id = context.insert_order(quote.instrument_id,
              quote.exchange_id, source, account, quote.ask_price[0], ORDER_VOLUME,
              PriceType.Limit, Side.Buy, Offset.Open)
    if ask_volume_sum > 2 * bid_volume_sum and bid_volume_sum > 0:
        position = get_position(quote.instrument_id, context.book)
        if position and position.volume > ORDER_VOLUME:
            order_id = context.insert_order(quote.instrument_id,
              quote.exchange_id, source, account, quote.bid_price[0], ORDER_VOLUME,
              PriceType.Limit, Side.Sell, Offset.Close)
```

**DolphinDB 实现**

下面是 DolphinDB
的主要策略实现代码，完整实现脚本可见附件：

```
def onSnapshot(mutable context, msg, indicator){
	maxP = context["MAX_POSITION"]
	orderV = context["ORDER_VOLUME"]
	istock = msg.symbol
	ask_volume_sum = sum(msg.offerQty)
	bid_volume_sum = sum(msg.bidQty)
	if (ask_volume_sum > 0){
	    if (bid_volume_sum > 2*ask_volume_sum){
	        posL = Backtest::getPosition(context["engine"],istock).longPosition
	        if(posL < maxP){
	            buyPrice = msg.bidPrice[1]
	            Backtest::submitOrder(context["engine"],
					(istock,context["tradeTime"], 5, buyPrice, orderV, 1),'oimOBUY')
	        }
	    }
	}
	if (bid_volume_sum > 0){
	    if (2*bid_volume_sum < ask_volume_sum){
	        posH = Backtest::getPosition(context["engine"],istock).shortPosition[0]
	        if(posH >= orderV){
	            sellPrice = msg.offerPrice[1]
	            Backtest::submitOrder(context["engine"],
					(istock,context["tradeTime"], 5, sellPrice, orderV, 2),'oimOSELL')
	        }
	    }
	}
}
```

**性能对比测试**

下面展示**功夫量化**和 DolphinDB 的性能测试。

使用八支股票一个月的快照共 85 万条行情作为测试数据，通过功夫 Windows 客户端软件云提交到服务器测试功夫量化的运行效率(纯 Python 接口)，并对比
DolphinDB 的性能，得到以下结果：

|  | **DolphinDB（JIT）**  **V3.00.2.1** | **DolphinDB（非JIT）**  **V3.00.2.1** | **功夫量化**  **V2.7.6** |
| --- | --- | --- | --- |
| **运行时间** | 1.1s | 5.7s | 124s |

由于 DolphinDB 数据库带来的数据传输速度提升以及 C++ 框架的加持， DolphinDB 的回测速度相比功夫量化的 Python
接口版本明显更快。

## 小结

在交易性能测试对比之余，下面还添加了功能对比测试的表格，以供参考。

|  | **DolphinDB V3.00.2.1** | **Backtrader V1.9.78.123** | **MetaTrader 4** | **VNPY V3.0** | **功夫量化 V2.7.6** |
| --- | --- | --- | --- | --- | --- |
| **跨品种** | ✔ | ✔ | × | × | ✔ |
| **订单延迟模拟** | ✔ | ×  需在代码中手动模拟延迟 | × | × | ✔ |
| **并行回测** | ✔ | ×  需要利用multiprocessor并行 | ×  需要多个MT4实例 | × | ✔ |
| **按交易所规则模拟撮合** | ✔ | ×  仅支持简单的撮合模型 | × | × | ✔ |
| **手续费** | ✔ | ✔ | ✔ | ✔ | ✔ |
| **实时保证金计算与风控** | ✔ | /  不涉及 | × | × | ✔ |
| **摩擦成本估计** | 综合考虑量价得出，可设置模拟交易比例 | 通过设置滑点估计摩擦成本 | 弱，无法动态模拟 | 通过设置滑点估计摩擦成本 | 通过订单参数模拟到达交易所时间，不支持设置成交比例 |
| **分红** | ✔ | ✔  需要手动设置策略模拟分红 | /  不涉及 | × | ✔ |
| **逐笔回测** | ✔ | × | × | × | ✔ |
| **支持行情预处理生成信号** | ✔ | ✔ | 只支持预处理 | × | × |
| **指标计算** | ✔ | 支持分钟频以上行情的部分指定指标的计算 | ✔  只有20个左右的指标，自定义实现复杂 | 支持分钟频以上行情的20个以下的内置指标的计算 | ✔ |
| **组合策略回测** | ✔ | ✔ | × | × | ✔ |

* 相比 DolphinDB 回测平台，Backtrader
  对于超高频交易的支持较弱；对于订单延迟、复杂的模拟撮合等功能，用户需要在策略中手动实现。此外，Backtrader
  缺乏内置的风险管理功能（如实时保证金计算）。相比之下， DolphinDB 支持更全面，可以通过各种接口获得相应的参数和功能。
* 对比 MT4， DolphinDB
  功能性更全，对并行化回测支持良好。在资产规模较大、资产品种更灵活、以及回测表现对市场流动性更敏感的中高频回测场景中，DolphinDB
  有明显的易用性优势。
* DolphinDB 的风控系统相比 VNPY 有显著的优势：对于期货交易，内嵌的风险控制系统非常重要，如果需要用户从零开发，将付出大量的时间成本。而在使用
  DolphinDB 回测平台时，仅需输入一些形式参数即可； VNPY 仅支持单支标的的回测，DolphinDB
  支持多标的同时回测。另外，DolphinDB 支持逐笔高频回测，而 VNPY 对高频回测的支持有限。
* DolphinDB 相比于功夫量化支持沪深 A 股更高精度的逐笔回测， 在使用脚本编写策略时，支持使用 JIT 技术来提升策略执行效率。

综上所述，DolphinDB 回测框架已经实现了多资产覆盖、模拟回测仿真和风险控制系统。与 Backtrader、VNPY、功夫量化相比， DolphinDB
在回测速度上实现了数量级的飞跃，在功能上更加完善。对比 MT4，DolphinDB 使用 JIT
后，让脚本语言编写的策略逼近编译型语言的性能；在业务功能方面，DolphinDB 对并行回测和高频交易的支持更佳。

## 附录

**测试代码**

**功夫量化 level2行情订单不平衡策略回测**

* 订单不平衡策略 DolphinDB 实现：<data/Kungfu_v.s._DolphinDB.dos>
* 订单不平衡策略 功夫量化 实现：<data/Kungfu_OrderBookImbalance.txt>

**backtrader 股票分钟CTA**

* onBarDemo 策略 DolphinDB 实现：<data/backtrader_v.s._DolphinDB.dos>
* onBarDemo 策略 Python Backtrader 实现：<data/PythonBacktrader_onBarCTA.txt>
* onBarDemo 策略数据：<data/mink_data.csv>

**MT4 RSi+布林带趋势策略**

* RSI + 布林带策略 DolphinDB 实现：<data/MT4_v.s._DolphinDB.dos>
* RSI + 布林带策略 MT4 实现：<data/MT4_BollingBand.mq4>

**VNPY 期货CTA策略**

* 期货 CTA 策略 DolphinDB 实现：<data/VNPY_v.s._DolphinDB.dos>
* 期货 CTA 策略 VNPY 实现：<data/VNPY_CTA.py>
