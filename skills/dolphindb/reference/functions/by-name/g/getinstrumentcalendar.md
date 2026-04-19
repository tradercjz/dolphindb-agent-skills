# getInstrumentCalendar

首发版本：3.00.4.1

## 语法

`getInstrumentCalendar(instrument)`

## 详情

根据输入的金融工具，获取该工具的交易日历。

## 参数

**instrument** INSTRUMENT 类型标量或向量，表示金融工具。

## 返回值

STRING 类型标量或向量。

## 例子

```
swap = {
    "productType": "Swap",
    "swapType": "IrSwap",
    "irSwapType": "IrFixedFloatingSwap",
    "start": 2021.05.15,
    "maturity": 2023.05.15,
    "frequency": "Quarterly",
    "fixedRate": 0.02,
    "calendar": "CFET",
    "fixedDayCountConvention": "Actual365",
    "floatingDayCountConvention": "Actual360",
    "payReceive": "Pay",
    "iborIndex": "SHIBOR_3M",
    "spread": 0.0005,
    "notionalCurrency": "CNY",
    "notionalAmount": 1E8
}
ins = parseInstrument(swap)
getInstrumentCalendar(ins)

// output: CFET
```

**相关函数：**parseInstrument、getInstrumentField、getInstrumentKeys
