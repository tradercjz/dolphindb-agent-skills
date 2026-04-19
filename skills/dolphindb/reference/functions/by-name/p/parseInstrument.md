# parseInstrument

首发版本：3.00.4

## 语法

`parseInstrument(obj)`

## 详情

将输入的金融工具产品描述（*obj*）转换成一个 INSTRUMENT 类型对象（金融工具），用于后续建模和定价。可解析的金融工具详见下文说明。

**注意：**`parseInstrument`
会在序列化或反序列化过程中保留非标准标量或向量字段（即不属于金融工具预定义属性的字段）。

## 参数

**obj** 可以是字典、由字典组成的元组、内存表、字符串标量或向量，表示要解析的金融工具描述。注意，如果 *obj*
指定为表，则该表只能存储单一类型的金融工具。

## 返回值

一个 INSTRUMENT 类型对象，表示金融工具。

## 例子

使用字典存储付息债的描述，通过 `parseInstrument` 解析该字典，以获得该付息债的 INSTRUMENT 类型对象。

```
bond = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "FixedRateBond",
    "instrumentId": "230205.IB",
    "start": "2023.03.06",
    "maturity": "2033.03.06",
    "issuePrice": 100.0,
    "coupon": 0.0302,
    "calendar": "CFET",
    "frequency": "Annual",
    "dayCountConvention": "ActualActualISDA",
    "subType": "CDB_BOND",
    "issuer": "国家开发银行"
}
parseInstrument(bond)
```

通过 `parseInstrument` 解析由字典组成的元组，得到3个债券的 INSTRUMENT 类型对象。

```
bond1 = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "DiscountBond",
    "instrumentId": "259924.IB",
    "start": 2025.04.17,
    "maturity": 2025.07.17,
    "issuePrice": 99.664,
    "dayCountConvention": "ActualActualISDA",
    "subType": "TREASURY_BOND",
    "issuer": "中华人民共和国财政部"
}

bond2 = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "ZeroCouponBond",
    "instrumentId": "250401.IB",
    "start": 2025.01.09,
    "maturity": 2026.02.05,
    "coupon": 0.0119,
    "dayCountConvention": "ActualActualISDA",
    "subType": "CDB_BOND",
    "issuer": "国家农业发展银行"
}

parseInstrument([bond,bond1,bond2])
```

使用内存表存储金融工具描述，其每一列代表一个字段。通过 `parseInstrument` 解析该表，得到 INSTRUMENT
类型对象。

注意：如果某个产品缺少内存表中某列对应的字段，则在插入该产品的数据时，该字段将被设置为 NULL。

```
create table t (
    productType STRING,
    assetType STRING,
    bondType STRING,
    version INT,
    instrumentId STRING,
    start DATE,
    maturity DATE,
    issuePrice DOUBLE,
    coupon DOUBLE,
    calendar STRING,
    frequency STRING,
    dayCountConvention STRING,
    subType STRING,
    issuer STRING
)
go

insert into t values( "Cash", "Bond", "FixedRateBond", 0, "230205.IB", 2023.03.06, 2033.03.06, 100.0, 0.0302, "CFET", "Annual", "ActualActualISDA", "CDB_BOND", "国家开发银行")
insert into t values( "Cash", "Bond", "DiscountBond", 0, "259924.IB", 2025.04.17, 2025.07.17, 99.664, NULL, NULL, NULL, "ActualActualISDA", "TREASURY_BOND", "中华人民共和国财政部")
insert into t values( "Cash", "Bond", "ZeroCouponBond", 0, "250401.IB", 2025.01.09, 2026.02.05, NULL, 0.0119, NULL, NULL, "ActualActualISDA", "CDB_BOND", "国家农业发展银行")

parseInstrument(t)
```

使用字符串描述金融工具，通过 `parseInstrument` 解析该字符串，得到 INSTRUMENT 类型对象。

```
bond1Str = '{"productType": "Cash","assetType": "Bond","bondType": "FixedRateBond","coupon": 0.0302,"frequency": "Annual","version": 0,"instrumentId": "230205.IB","nominal": 100,"start": "2023.03.06","maturity": "2033.03.06","dayCountConvention": "ActualActualISDA","calendar": "CFET","currency": "CNY","cashflow": [{"paymentDate": "2024.03.06","coupon": 3.026804551238871,"notional": 0,"total": 3.026804551238871},{"paymentDate": "2025.03.06","coupon": 3.01319544876113,"notional": 0,"total": 3.01319544876113},{"paymentDate": "2026.03.06","coupon": 3.02,"notional": 0,"total": 3.02},{"paymentDate": "2027.03.06","coupon": 3.02,"notional": 0,"total": 3.02},{"paymentDate": "2028.03.06","coupon": 3.026804551238871,"notional": 0,"total": 3.026804551238871},{"paymentDate": "2029.03.06","coupon": 3.01319544876113,"notional": 0,"total": 3.01319544876113},{"paymentDate": "2030.03.06","coupon": 3.02,"notional": 0,"total": 3.02},{"paymentDate": "2031.03.06","coupon": 3.02,"notional": 0,"total": 3.02},{"paymentDate": "2032.03.06","coupon": 3.026804551238871,"notional": 0,"total": 3.026804551238871},{"paymentDate": "2033.03.06","coupon": 3.01319544876113,"notional": 100,"total": 103.013195448761123}],"discountCurve": "","spreadCurve": "","subType": "CDB_BOND","issuePrice": 100,"issuer": "国家开发银行"}'

parseInstrument(bondStr)
```

通过 `parseInstrument` 解析该字符串向量，得到多个 INSTRUMENT 类型对象。

```
bond2Str = '{"productType": "Cash","assetType": "Bond","bondType": "DiscountBond","issuePrice": 99.664000000000001,"version": 0,"instrumentId": "259924.IB","nominal": 100,"start": "2025.04.17","maturity": "2025.07.17","dayCountConvention": "ActualActualISDA","calendar": "","currency": "CNY","cashflow": [{"paymentDate": "2025.07.17","coupon": 0,"notional": 100,"total": 100}],"discountCurve": "","spreadCurve": "","subType": "TREASURY_BOND","issuer": "中华人民共和国财政部"}'
bond3Str = '{"productType": "Cash","assetType": "Bond","bondType": "ZeroCouponBond","coupon": 0.0119,"version": 0,"instrumentId": "250401.IB","nominal": 100,"start": "2025.01.09","maturity": "2026.02.05","dayCountConvention": "ActualActualISDA","calendar": "","currency": "CNY","cashflow": [{"paymentDate": "2026.01.09","coupon": 1.190000000000002,"notional": 0,"total": 1.190000000000002},{"paymentDate": "2026.02.05","coupon": 0.088027397260282,"notional": 100,"total": 100.088027397260276}],"discountCurve": "","spreadCurve": "","subType": "CDB_BOND","issuer": "国家农业发展银行"}'

parseInstrument([bond1Str,bond2Str,bond3Str])
```

## 金融工具支持与字段要求

INSTRUMENT 为 DophinDB 在 3.00.4 版本上新增的数据类型，用于支持金融工具的存储，为后续各类金融产品的定价与风险计量提供基础。

在金融工具的描述中，需要包含若干关键字段，`parseInstrument`
将根据这些字段生成相应的金融工具对象。请注意，"version" 为系统保留字段，为避免冲突，请勿将此名称用于自定义字段。

目前支持的金融工具类型如下：

### 贴现债

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| productType | STRING | 固定填 "Cash" | 是 |
| assetType | STRING | 固定填 "Bond" | 是 |
| bondType | STRING | 固定填 "DiscountBond" | 是 |
| nominal | DOUBLE | 名义金额，默认值 100 | 否 |
| instrumentId | STRING | 债券代码，如 "259926.IB" | 否 |
| start | DATE | 起息日 | 是 |
| maturity | DATE | 到期日 | 是 |
| dayCountConvention | STRING | 日期计数惯例，可选 "ActualActualISDA", "ActualActualISMA", "Actual365", "Actual360" | 是 |
| issuePrice | DOUBLE | 发行价格 | 是 |
| currency | STRING | 货币，默认为 "CNY" | 否 |
| cashFlow | TABLE | 债券现金流表 | 否 |
| discountCurve | STRING | 定价时参考的贴现曲线名称，如 "CNY\_TRASURY\_BOND" | 否 |
| spreadCurve | STRING | 定价时参考的利差曲线名称 | 否 |
| subType | STRING | 债券子类型，中国债券可选值为：   * "TREASURY\_BOND"：国债 * "CENTRAL\_BANK\_BILL"：央行票据 * "CDB\_BOND"：政策性金融债（国开） * "EIBC\_BOND"：政策性金融债（进出口行） * "ADBC\_BOND"：政策性金融债（农发行）。 * "MTN"：中期票据 * "CORP\_BOND"：企业债。 * "UNSECURED\_CORP\_BOND"：无担保企业债 * "SHORT\_FIN\_BOND"：短期融资券 * "NCD"：同业存单 * "LOC\_GOV\_BOND"：地方政府债 * "COMM\_BANK\_FIN\_BOND"：商业银行普通金融债 * "BANK\_SUB\_CAP\_BOND"：商业银行二级资本债 * "ABS"：资产支持证券 * "PPN"：非公开发行债 | 否 |
| creditRating | STRING | 信用等级类型，可选值为："B", "BB", "BBB", "BBB+", "A-", "A", "A+", "AA-", "AA", "AA+", "AAA-", "AAA", "AAA+" | 否 |

下例定义了一个贴现债券的 INSTRUMENT 对象。

```
bond = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "DiscountBond",
    "instrumentId": "259924.IB",
    "start": 2025.04.17,
    "maturity": 2025.07.17,
    "issuePrice": 99.664,
    "dayCountConvention": "ActualActualISDA"
}
instrument = parseInstrument(bond)
print(instrument)
```

### 零息债

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| productType | STRING | 固定填 "Cash" | 是 |
| assetType | STRING | 固定填 "Bond" | 是 |
| bondType | STRING | 固定填 "ZeroCouponBond" | 是 |
| nominal | DOUBLE | 名义金额，默认值 100 | 否 |
| instrumentId | STRING | 债券代码，如 "250401.IB" | 否 |
| start | DATE | 起息日 | 是 |
| maturity | DATE | 到期日 | 是 |
| coupon | DOUBLE | 票面利率，如 0.03 表示 3% | 是 |
| frequency | STRING | 付息频率 | 否 |
| dayCountConvention | STRING | 日期计数惯例，可选 "ActualActualISDA", "ActualActualISMA", "Actual365", "Actual360" | 是 |
| currency | STRING | 货币，默认为 "CNY" | 否 |
| cashFlow | TABLE | 债券现金流表 | 否 |
| discountCurve | STRING | 定价时参考的贴现曲线名称，如 "CNY\_TRASURY\_BOND" | 否 |
| spreadCurve | STRING | 定价时参考的利差曲线名称 | 否 |
| subType | STRING | 债券子类型，中国债券可选值为：   * "TREASURY\_BOND"：国债 * "CENTRAL\_BANK\_BILL"：央行票据 * "CDB\_BOND"：政策性金融债（国开） * "EIBC\_BOND"：政策性金融债（进出口行） * "ADBC\_BOND"：政策性金融债（农发行）。 * "MTN"：中期票据 * "CORP\_BOND"：企业债。 * "UNSECURED\_CORP\_BOND"：无担保企业债 * "SHORT\_FIN\_BOND"：短期融资券 * "NCD"：同业存单 * "LOC\_GOV\_BOND"：地方政府债 * "COMM\_BANK\_FIN\_BOND"：商业银行普通金融债 * "BANK\_SUB\_CAP\_BOND"：商业银行二级资本债 * "ABS"：资产支持证券 * "PPN"：非公开发行债 | 否 |
| creditRating | STRING | 信用等级类型，可选值为："B", "BB", "BBB", "BBB+", "A-", "A", "A+", "AA-", "AA", "AA+", "AAA-", "AAA", "AAA+" | 否 |

下例定义了一个零息债的 INSTRUMENT 对象。

```
bond = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "ZeroCouponBond",
    "instrumentId": "250401.IB",
    "start": 2025.01.09,
    "maturity": 2026.02.05,
    "coupon": 0.0119,
    "dayCountConvention": "ActualActualISDA"
}
instrument = parseInstrument(bond)
print(instrument)
```

### 固定利率债

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| productType | STRING | 固定填 "Cash" | 是 |
| assetType | STRING | 固定填 "Bond" | 是 |
| bondType | STRING | 固定填 "FixedRateBond" | 是 |
| nominal | DOUBLE | 名义金额，默认值 100 | 否 |
| instrumentId | STRING | 债券代码，如 "250401.IB" | 否 |
| start | DATE | 起息日 | 是 |
| maturity | DATE | 到期日 | 是 |
| coupon | DOUBLE | 票面利率，如0.03表示3% | 是 |
| frequency | STRING | 付息频率 | 是 |
| dayCountConvention | STRING | 日期计数惯例，可选 "ActualActualISDA", "ActualActualISMA", "Actual365", "Actual360" | 是 |
| currency | STRING | 货币，默认为 "CNY" | 否 |
| cashFlow | TABLE | 债券现金流表 | 否 |
| discountCurve | STRING | 定价时参考的贴现曲线名称，如 "CNY\_TRASURY\_BOND" | 否 |
| spreadCurve | STRING | 定价时参考的利差曲线名称 | 否 |
| subType | STRING | 债券子类型，中国债券可选值为：   * "TREASURY\_BOND"：国债 * "CENTRAL\_BANK\_BILL"：央行票据 * "CDB\_BOND"：政策性金融债（国开） * "EIBC\_BOND"：政策性金融债（进出口行） * "ADBC\_BOND"：政策性金融债（农发行）。 * "MTN"：中期票据 * "CORP\_BOND"：企业债。 * "UNSECURED\_CORP\_BOND"：无担保企业债 * "SHORT\_FIN\_BOND"：短期融资券 * "NCD"：同业存单 * "LOC\_GOV\_BOND"：地方政府债 * "COMM\_BANK\_FIN\_BOND"：商业银行普通金融债 * "BANK\_SUB\_CAP\_BOND"：商业银行二级资本债 * "ABS"：资产支持证券 * "PPN"：非公开发行债 | 否 |
| creditRating | STRING | 信用等级类型，可选值为："B", "BB", "BBB", "BBB+", "A-", "A", "A+", "AA-", "AA", "AA+", "AAA-", "AAA", "AAA+" | 否 |

下例定义了一个固定利率债的 INSTRUMENT 对象。

```
bond = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "FixedRateBond",
    "instrumentId": "240021.IB",
    "start": 2024.10.25,
    "maturity": 2025.10.25,
    "issuePrice": 100,
    "coupon": 0.0133,
    "frequency": "Annual",
    "dayCountConvention": "ActualActualISDA"
}
instrument = parseInstrument(bond)
print(instrument)
```

### 含权债

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| productType | STRING | 固定填 "Cash" | 是 |
| assetType | STRING | 固定填 "Bond" | 是 |
| bondType | STRING | 固定填 "OptionBond" | 是 |
| nominal | DOUBLE | 名义金额，默认值100 | 否 |
| instrumentId | STRING | 债券代码，如 "242659.SH" | 否 |
| start | DATE | 起息日 | 是 |
| maturity | DATE | 到期日 | 是 |
| coupon | DOUBLE | 票面利率，如0.03表示3% | 是 |
| frequency | DOUBLE | 付息频率，如1表示每年付息1次 | 是 |
| principalRatio | DOUBLE 类型向量 | 提前偿还型债券的本金摊还比例向量。  向量长度等于债券期限，各元素表示对应期间偿还的本金占初始本金的比例，且所有元素之和为1。默认为空。 | 否 |
| exerciseDates | DATE 类型向量 | 含权债为行权时间的向量。默认为空。 | 否 |
| hasCallOption | BOOL | 该债券发行人是否有赎回权 | 是 |
| hasPutOption | BOOL | 该债券投资者是否有回售权 | 是 |
| hasCouponAdjust | BOOL | 该债券发行人是否有票面利率调整权 | 是 |
| newCoupon | DOUBLE | 票面利率调整后的新利率。当 `hasCouponAdjust = true` 且已到调整时点时生效。若 newCoupon 为空（默认值），则仍使用原票面利率。 | 否 |
| dayCountConvention | STRING | 日期计数惯例，可选 "ActualActualISDA", "ActualActualISMA", "Actual365", "Actual360"，国债默认为 "Actual365"，其他默认为 "ActualActualISMA" | 是 |
| subType | STRING | 债券子类型，中国债券可选值为：   * "TREASURY\_BOND"：国债 * "CENTRAL\_BANK\_BILL"：央行票据 * "CDB\_BOND"：政策性金融债（国开） * "EIBC\_BOND"：政策性金融债（进出口行） * "ADBC\_BOND"：政策性金融债（农发行）。 * "MTN"：中期票据 * "CORP\_BOND"：企业债。 * "UNSECURED\_CORP\_BOND"：无担保企业债 * "SHORT\_FIN\_BOND"：短期融资券 * "NCD"：同业存单 * "LOC\_GOV\_BOND"：地方政府债 * "COMM\_BANK\_FIN\_BOND"：商业银行普通金融债 * "BANK\_SUB\_CAP\_BOND"：商业银行二级资本债 * "ABS"：资产支持证券 * "PPN"：非公开发行债   默认值为空。 | 否 |
| creditRating | STRING | 信用等级类型，可选值为："B", "BB", "BBB", "BBB+", "A-", "A", "A+", "AA-", "AA", "AA+", "AAA-", "AAA", "AAA+"。默认值为空。 | 否 |

下例定义了一个含权债的 INSTRUMENT 对象。

```
optionBond = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "OptionBond",
    "instrumentId": "242659.SH",
    "nominal": 100.0,
    "start": 2025.03.26,
    "maturity": 2030.03.26,
    "coupon": 0.0207,
    "frequency": "Annual",
    "exerciseDates": [2028.03.26],
    "hasCallOption": true,
    "hasPutOption": true,
    "hasCouponAdjust": true,
    "dayCountConvention": "ActualActualISMA"
}
instrument = parseInstrument(optionBond)
print(instrument)
```

### 国债期货

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| productType | STRING | 固定值为 "Futures" | 是 |
| futuresType | STRING | 固定值为 "BondFutures" | 是 |
| nominal | DOUBLE | 名义金额，默认值 100 | 是 |
| instrumentId | STRING | 国债期货代码，如 "T2509" | 否 |
| maturity | DATE | 到期日 | 是 |
| settlement | DATE | 结算日 | 是 |
| underlying | 字典 | 固定利率债券结构，表示标的可交割债券 | 是 |
| nominalCouponRate | DOUBLE | 名义票面利率 | 是 |

下例定义了一个国债期货的 INSTRUMENT 对象。

```
bond ={
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "FixedRateBond",
    "instrumentId": "220010.IB",
    "start": 2020.12.25,
    "maturity": 2031.12.25,
    "issuePrice": 100.0,
    "coupon": 0.0149,
    "frequency": "Annual",
    "dayCountConvention": "ActualActualISDA"
}

futures =  {
    "productType": "Futures",
    "futuresType": "BondFutures",
    "instrumentId": "T2509",  //期货代码
    "nominal": 100.0,
    "maturity": "2022.09.09",
    "settlement": "2022.09.11",
    "underlying": bond,
    "nominalCouponRate": 0.03  //与国债期货品种匹配的名义利率，可从中金所获取
}
instrument = parseInstrument(futures)
print(instrument)
```

### 存款

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| productType | STRING | 固定填 "Cash" | 是 |
| assetType | STRING | 固定填 "Deposit" | 是 |
| notional | ANY 向量 | 名义本金，格式如 ["USD", 1.0]。 | 是 |
| instrumentId | STRING | 存款参考利率指数，如 "SHIBOR\_3M" | 否 |
| start | DATE | 起息日 | 是 |
| maturity | DATE | 到期日 | 是 |
| rate | DOUBLE | 存款利率 | 是 |
| dayCountConvention | STRING | 日期计数惯例, 可选 "ActualActualISDA", "ActualActualISMA", "Actual365", "Actual360" | 是 |
| payReceive | STRING | 收付标识，"Pay" 表示支付，"Receive" 表示收取 | 是 |
| disconutCurve | STRING | 定价时参考的贴现曲线名称，人民币存款默认为 "CNY\_FR\_007" | 否 |
| calendar | STRING | 交易日历 | 否 |

下例定义了一个存款的 INSTRUMENT 对象。

```
deposit =  {
    "productType": "Cash",
    "assetType": "Deposit",
    "start": 2025.05.15,
    "maturity": 2025.08.15,
    "rate": 0.02,
    "dayCountConvention": "Actual360",
    "notional":["CNY", 1E6],
    "payReceive": "Receive"
}
instrument = parseInstrument(deposit)
print(instrument)
```

### 利率互换

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| productType | STRING | 固定填 "Swap" | 是 |
| swapType | STRING | 固定填 "IrSwap" | 是 |
| irSwapType | STRING | 固定填 "IrFixedFloatingSwap" | 是 |
| notional | ANY 向量 | 名义本金，格式如 ["USD", 1.0] | 是 |
| instrumentId | STRING | 利率互换名称，可填 "CNY\_FR\_007 , "CNY\_SHIBOR\_3M" | 否 |
| start | DATE | 起息日 | 是 |
| maturity | DATE | 到期日 | 是 |
| fixedRate | DOUBLE | 固定端利率 | 是 |
| calender | STRING | 交易日历 | 是 |
| fixedDayCountConvention | STRING | 固定端日期计数惯例，可选 "ActualActualISDA", "ActualActualISMA", "Actual365", "Actual360" | 是 |
| floatingDayCountConvention | STRING | 浮动端日期计数惯例，可选 "ActualActualISDA", "ActualActualISMA", "Actual365", "Actual360" | 是 |
| spread | DOUBLE | 利差 | 是 |
| iborIndex | STRING | 浮动端参考利率，可选FR\_007和SHIBOR\_3M | 是 |
| frequency | STRING | 付息频率 | 是 |
| payReceive | STRING | 收付标识，可选：   * "Pay"：本方支付固定利率、接收浮动利率（pay fixed / receive   floating） * "Receive"：本方接收固定利率、支付浮动利率（receive fixed / pay   floating） | 是 |
| domesticCurve | STRING | 定价时参考的贴现曲线名称 | 否 |
| foreignCurve | STRING | 定价时参考的远期曲线名称 | 否 |

下例定义了一个利率互换的 INSTRUMENT 对象。

```
swap =  {
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
    "notional":["CNY", 1E8]
}
instrument = parseInstrument(swap)
print(instrument)
```

### 外汇远期

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| productType | STRING | 产品名称，固定值为 "Forward" | 是 |
| forwardType | STRING | 远期类型，固定值为 "FxForward" | 是 |
| notional | ANY 向量 | 名义本金，格式如 ["USD", 1.0] | 是 |
| instrumentId | STRING | 金融工具 ID | 否 |
| expiry | DATE | 到期日 | 是 |
| delivery | DATE | 交割日 | 是 |
| currencyPair | STRING | 货币对，格式如："EURUSD"，"EUR.USD" 或 "EUR/USD"。支持如下货币对：   * EURUSD：欧元兑美元 * USDCNY：美元兑人民币 * EURCNY：欧元兑人民币 * GBPCNY：英镑兑人民币 * JPYCNY：日元兑人民币 * HKDCNY：港币兑人民币 | 是 |
| direction | STRING | 交易方向。可选："Buy"、"Sell" | 是 |
| strike | DOUBLE | 执行价格 | 是 |
| domesticCurve | STRING | 定价时参考的本币贴现曲线名称 | 否 |
| foreignCurve | STRING | 定价时参考的外币贴现曲线名称 | 否 |

下例定义了一个外汇远期的 INSTRUMENT 对象。

```
forward =  {
   "productType": "Forward",
    "forwardType": "FxForward",
    "expiry": 2025.09.24,
    "delivery": 2025.09.26,
    "currencyPair": "USDCNY",
    "direction": "Buy",
    "notional": ["USD", 1E8],
    "strike": 7.2
}
instrument = parseInstrument(forward)
print(instrument)
```

### 外汇掉期

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| productType | STRING | 产品名称，固定值为 "Swap" | 是 |
| swapType | STRING | 远期类型，固定值为 "FxSwap" | 是 |
| notional | ANY 向量 | 名义本金，格式如 ["USD", 1.0] | 是 |
| currencyPair | STRING | 货币对，格式如："EURUSD"，"EUR.USD" 或 "EUR/USD"。支持如下货币对：   * EURUSD：欧元兑美元 * USDCNY：美元兑人民币 * EURCNY：欧元兑人民币 * GBPCNY：英镑兑人民币 * JPYCNY：日元兑人民币 * HKDCNY：港币兑人民币 | 是 |
| nearExpiry | DATE | 近端到期日。 | 是 |
| nearDelivery | DATE | 近端交割日，实际资金交割发生的日期。 | 是 |
| direction | STRING | 交易方向，可选值：   * "Buy"：在近端买入外币（买 near），在远端卖出外币（卖 far）。 * "Sell"：在近端卖出外币（卖 near），在远端买回外币（买 far）。 | 是 |
| nearStrike | DOUBLE | 近端行权价格 | 是 |
| farExpiry | DATE | 远端到期日 | 是 |
| farDelivery | DATE | 远端交割日，实际发生第二次资金交换的日期 | 是 |
| farStrike | DOUBLE | 远端行权价格 | 是 |
| domesticCurve | STRING | 定价时参考的本币贴现曲线名称 | 否 |
| foreignCurve | STRING | 定价时参考的外币贴现曲线名称 | 否 |

下例定义了一个外汇掉期的 INSTRUMENT 对象。

```
swap = {
    "productType": "Swap",
    "swapType": "FxSwap",
    "currencyPair": "EURUSD",
    "direction": "Buy",
    "notional": ["EUR", 1E6],
    "nearStrike": 1.1,
    "nearExpiry": 2025.12.08,
    "nearDelivery": 2025.12.10,
    "farStrike": 1.2,
    "farExpiry": 2026.06.08,
    "farDelivery": 2026.06.10
}
instrument = parseInstrument(swap)
print(instrument)
```

### 外汇欧式期权

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| productType | STRING | 固定填 "Option" | 是 |
| optionType | STRING | 固定填 "EuropeanOption" | 是 |
| assetType | STRING | 固定填 "FxEuropeanOption" | 是 |
| notional | ANY 向量 | 名义本金，格式如 ["USD", 1.0] | 是 |
| instrumentId | STRING | 金融工具 ID | 否 |
| maturity | DATE | 到期日 | 是 |
| underlying | STRING | 货币对，格式如："EURUSD"，"EUR.USD" 或 "EUR/USD"。支持如下货币对：   * EURUSD：欧元兑美元 * USDCNY：美元兑人民币 * EURCNY：欧元兑人民币 * GBPCNY：英镑兑人民币 * JPYCNY：日元兑人民币 * HKDCNY：港币兑人民币 | 是 |
| direction | STRING | 交易方向。可选值为："Buy"、"Sell"。 | 是 |
| strike | DOUBLE | 执行价格。 | 是 |
| dayCountConvention | STRING | 日期计数惯例，可选 "ActualActualISDA", "ActualActualISMA", "Actual365", "Actual360" | 是 |
| payoffType | STRING | 收益类型，可选值为 "Call"、 "Put" | 是 |
| domesticCurve | STRING | 定价时参考的本币贴现曲线名称 | 否 |
| foreignCurve | STRING | 定价时参考的外币贴现曲线名称 | 否 |
| delivery | DATE | 交割日 | 否 |

**注意**：delivery 字段从 version 2 版本开始支持。升级低于 version 2 的旧版本数据到 version 2
或更高版本时，原有记录中缺失的 delivery 字段将自动填充为 maturity + 2。

下例定义了一个 外汇欧式期权的 INSTRUMENT 对象。

```
option =  {
    "productType": "Option",
    "optionType": "EuropeanOption",
    "assetType": "FxEuropeanOption",
    "notional": ["EUR", 1000000.0],
    "strike": 1.2,
    "maturity": "2025.10.08",
    "payoffType": "Call",
    "dayCountConvention": "Actual365",
    "underlying": "EURUSD"
}
instrument = parseInstrument(option)
print(instrument)
```

### 商品期货美式期权

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| productType | STRING | 固定填 "Option" | 是 |
| optionType | STRING | 固定填 "AmericanOption" | 是 |
| assetType | STRING | 固定填 "CmFutAmericanOption" | 是 |
| notionalAmount | DOUBLE | 名义本金额 | 是 |
| notionalCurrency | STRING | 名义本金货币 | 是 |
| instrumentId | STRING | 合约代码，标准格式为：标的期货合约代码+合约到期月份+期权类型代码+行权价格，如白糖期权为 SR2509P6300 = SR+2509+P+6300 | 否 |
| direction | SRTRING | 买卖方向，可选值为 Buy，Sell。默认值为 Buy。 | 否 |
| maturity | DATE | 到期日 | 是 |
| strike | DOUBLE | 执行利率 | 是 |
| payoffType | STRING | 收益类型，可选 Call 和 Put | 是 |
| underlying | STRING | 标的期货合约代码，如 SR2509 | 是 |
| dayCountConvention | STRING | 日期计数惯例, 可选 "ActualActualISDA", "ActualActualISMA", "Actual365", "Actual360" | 是 |
| discountCurve | STRING | 定价时参考的贴现曲线名称，人民币存款默认为 "CNY\_FR\_007" | 否 |

### 商品期货欧式期权

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| productType | STRING | 固定填 "Option" | 是 |
| optionType | STRING | 固定填 "EuropeanOption" | 是 |
| assetType | STRING | 固定填 "CmFutEuropeanOption" | 是 |
| notionalAmount | DOUBLE | 名义本金额 | 是 |
| notionalCurrency | STRING | 名义本金货币 | 是 |
| instrumentId | STRING | 合约代码，标准格式为：标的期货合约代码+合约到期月份+期权类型代码+行权价格，如白糖期权  SR2509P6300 = SR+2509+P+6300 | 否 |
| direction | SRTRING | 买卖方向 Buy Sell，默认为 Buy | 否 |
| maturity | DATE | 到期日 | 是 |
| strike | DOUBLE | 执行利率 | 是 |
| payoffType | STRING | 枚举，可选 Call 和 Put | 是 |
| underlying | STRING | 标的期货合约代码，如 SR2509 | 是 |
| dayCountConvention | STRING | 日期计数惯例，可选 "ActualActualISDA"、"ActualActualISMA"、"Actual365"、"Actual360" | 是 |
| discountCurve | STRING | 定价时参考的贴现曲线名称，人民币存款默认为 "CNY\_FR\_007" | 否 |

### 权益类美式期权

| **字段名** | **类型** | **描述** | **是否必填** |
| --- | --- | --- | --- |
| productType | STRING | 固定填 "Option" | 是 |
| optionType | STRING | 固定填 "AmericanOption" | 是 |
| assetType | STRING | 固定填 "EqAmericanOption" | 是 |
| notionalAmount | DOUBLE | 名义本金额 | 是 |
| notionalCurrency | STRING | 名义本金货币，默认为 CNY | 是 |
| instrumentId | STRING | 合约代码，如代码 `TCH250328C0040000`的解读如下：   * `TCH`: 标的为腾讯控股 * `250328`: 到期日为2025年3月28日。 * `C`: 期权类型为认购（Call） * `0040000`: 行权价为400.00港元。 | 否 |
| direction | SRTRING | 买卖方向 Buy Sell，默认为 Buy | 否 |
| maturity | DATE | 到期日 | 是 |
| strike | DOUBLE | 执行利率 | 是 |
| payoffType | STRING | 枚举，可选Call和Put | 是 |
| underlying | STRING | 标的期货合约代码，如 `TCH` | 是 |
| dayCountConvention | STRING | 日期计数惯例, 可选 "ActualActualISDA", "ActualActualISMA", "Actual365", "Actual360" | 是 |
| discountCurve | STRING | 定价时参考的贴现曲线名称，人民币存款默认为 "CNY\_FR\_007" | 否 |
| dividendCurve | STRING | 定价时参考的股息曲线名称 | 否 |

### 权益类欧式期权

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| productType | STRING | 固定填 "Option" | 是 |
| optionType | STRING | 固定填 "EuropeanOption" | 是 |
| assetType | STRING | 固定填 “EqEuropeanOption" | 是 |
| notionalAmount | DOUBLE | 名义本金额 | 是 |
| notionalCurrency | STRING | 名义本金货币，默认为 CNY | 否 |
| instrumentId | STRING | 合约代码，如中证 500ETF 期权  510500C2512M04800 | 否 |
| direction | SRTRING | 买卖方向 Buy Sell，默认为 Buy | 否 |
| maturity | DATE | 到期日 | 是 |
| strike | DOUBLE | 执行利率 | 是 |
| payoffType | STRING | 枚举，可选 Call 和 Put | 是 |
| underlying | STRING | 标的期货合约代码，如 510050 | 是 |
| dayCountConvention | STRING | 日期计数惯例，可选 "ActualActualISDA"、"ActualActualISMA"、"Actual365"、"Actual360" | 是 |
| discountCurve | STRING | 定价时参考的贴现曲线名称，人民币存款默认为 "CNY\_FR\_007" | 否 |
| dividendCurve | STRING | 定价时参考的股息曲线名称 | 否 |

### 用户自定义

支持用户自定义金融工具，除 producType 外，所有字段均可自定义。

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| productType | STRING | 固定填 "UserDefined" | 是 |

**相关函数：**bondPricer（债券定价）、irDepositPricer（存款定价）、bondFuturesPricer（国债期货定价）、fxForwardPricer（外汇远期定价）、fxSwapPricer（外汇掉期定价）、irFixedFloatingSwapPricer（利率互换定价）、fxEuropeanOptionPricer（外汇欧式期权定价）
