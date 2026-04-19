# deleteMarketHoliday

首发版本：3.00.3

## 语法

`deleteMarketHoliday(marketName)`

## 详情

删除已有的交易日历。

注：

* 该函数只能由管理员调用。
* 该函数仅对当前节点有效。集群环境中，通过 `pnodeRun` 调用该函数，使其在其它节点生效。

## 参数

**marketName** 字符串标量，表示要删除的交易日历标识，例如“XNYS”。

## 返回值

无。

## 例子

```
listAllMarkets()
// Output: ["XTSE","XCSE","XLIM","ADDA","XSTO","XIST","AIXK","SSE","XMIL","XFRA","INE","XMEX","XBUD","XICE","XDUB","SHFE","CMES","XOSL","DCE","CCFX","CFFEX","XIDX","BVMF","XBOG","XKAR","XSAU","XBUE","XTKS","XBSE","XMOS"...]

deleteMarketHoliday("XTSE")
"XTSE" in listAllMarkets()
// Output: false
```

**相关函数：addMarketHoliday**
