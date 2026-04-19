# yearFrac

首发版本：3.00.5

## 语法

`yearFrac(dayCountConvention, start, end, [referenceStart],
[referenceEnd])`

## 详情

按指定计息规则计算的起止日期之间的年化时间长度，常用于利息、贴现及期权定价等金融计算。

## 参数

**dayCountConvention** STRING 类型标量，表示计息日数规则，可选值为：

* "Actual360": 实际/360
* "Actual365": 实际/365
* "ActualActualISDA"：实际/实际，遵循 ISDA（International Swaps and Derivatives
  Association，国际掉期及衍生工具协会）规则
* "ActualActualISMA": 实际/实际，遵循 ISMA（International Securities Market
  Association，国际证券市场协会）规则

**start** DATE 类型标量，表示开始日期。

**end** DATE 类型标量，表示结束日期。

**referenceStart** 可选参数，DATE 类型标量，表示当前计息区间所属的标准付息周期的参考。仅在
*dayCountConvention* 为 "ActualActualISMA" 时有效。

**referenceEnd** 可选参数，DATE 类型标量，表示当前计息区间所属的标准付息周期的结束日期。仅在
*dayCountConvention* 为 "ActualActualISMA" 时有效。

## 返回值

DOUBLE 类型标量。

## 例子

对于具有固定付息周期的金融产品（如半年付息债券），ActualActualISMA 计息规则需要通过 *referenceStart* 和
*referenceEnd* 指定当前计息区间所属的标准付息周期。

假设某债券每半年付息一次，其付息周期为：2025-01-01 至 2025-07-01，计算该付息周期内一段时间的年化比例：

```
start =  2025.02.15
end = 2025.05.15
referenceStart = 2025.01.01
referenceEnd = 2025.07.01
yearFrac("ActualActualISMA", start, end, referenceStart, referenceEnd)

// output: 0.25
```
