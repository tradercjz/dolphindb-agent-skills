# bool

## 语法

`bool(X)`

## 详情

把输入转换为布尔值。

## 参数

**X** 可以是任意的数据类型。

## 返回值

布尔类型，其数据形式同 *X*。

## 例子

```
x=bool();
x;
```

返回：null

```
typestr x;
```

返回：BOOL

```
bool(`true);
```

返回：true

```
bool(`false);
```

返回：false

```
bool(`true`false)
```

返回：[true, false]

```
bool(100.2);
```

返回：true

```
bool(0);
```

返回：false
