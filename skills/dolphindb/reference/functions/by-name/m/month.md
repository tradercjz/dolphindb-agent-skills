# month

## 语法

`month(X)`

## 详情

返回对应的月份。

## 参数

**X** 可以是时间标量或向量。

## 返回值

MONTH 类型标量或向量。

## 例子

```
month();
```

返回：null

```
month(`2012.12);
```

返回：2012.12M

```
month(2012.12.23);  // 把一个 DATE 类型的数据转换成 MONTH 类型。
```

返回：2012.12M

```
month(now());  // 把一个 TIMESTAMP 类型的数据转换成 MONTH 类型。
```

返回：2024.02M

**相关信息**

* [second](../s/second.html "second")
* [minute](minute.html "minute")
* [hour](../h/hour.html "hour")
* [date](../d/date.html "date")
* [year](../y/year.html "year")
