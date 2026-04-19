# nunique

## 语法

`nunique(X, [ignoreNull=false])`

## 详情

*X* 是向量/数组向量时，计算 *X* 中唯一值的数量。

*X* 是元组时，其内每个向量位于相同位置的元素组成一个 key，计算唯一 key 的数量。

**注意**：在 SQL-92 中，通常使用 COUNT(DISTINCT ...) 统计唯一值的数量。DolphinDB 目前不支持这种用法，不过，可以使用
`nunique` 函数来实现相同的目的。也就是说， DolphinDB 中的
`nunique(...)` 等价于 SQL-92 中的 COUNT(DISTINCT ...)，具体可见下面例子说明。

## 参数

**X** 是一个向量/数组向量，或包含多个等长向量的元组。

**ignoreNull** 是一个布尔值，表示是否忽略 *X* 中 NULL 值。若指定
*ignoreNull*=true，则统计唯一值时将不考虑 NULL 值；否则将会统计 NULL 值。默认值为 false。请注意，当 *X*
是元组或数组向量时，不可指定 *ignoreNull*=true。

## 返回值

INT 类型标量。

## 例子

```
v = [1,3,1,-6,NULL,2,NULL,1];
nunique(v);
// output: 5

//指定 ignorNull = true，统计唯一值时将不考虑 NULL 值
nunique(v,true);
// output: 4

a = array(INT[], 0, 10).append!([1 2 3, 3 5, 6 8 8, 9 10])
nunique(a)
// output: 8
```

```
t=table(1 2 4 8 4 2 7 1 as id, 10 20 40 80 40 20 70 10 as val);
select nunique([id,val]) from t;
```

| nunique |
| --- |
| 5 |

```
dbName = "dfs://testdb"
if(existsDatabase(dbName)){
   dropDatabase(dbName)
}

db=database("dfs://testdb", VALUE, 2012.01.11..2012.01.29)

n=100
t=table(take(2012.01.11..2012.01.29, n) as date, symbol(take("A"+string(21..60), n)) as sym, take(100, n) as val)

pt=db.createPartitionedTable(t, `pt, `date).append!(t)
select nunique(date) from pt group by sym
```

以下分别给出 MySQL 和 DolphinDB 中统计唯一用户数的示例。

MySQL 代码示例如下，返回结果为 4。

```
CREATE TABLE orders (
    order_id INT,
    user_id INT,
    product_id INT,
    order_date DATE
);

INSERT INTO orders VALUES
(1, 1001, 101, '2026-01-01'),
(2, 1002, 101, '2026-01-02'),
(3, 1001, 102, '2026-01-03'),
(4, 1003, 101, '2026-01-04'),
(5, 1002, 102, '2026-01-05'),
(6, 1004, 103, '2026-01-06'),
(7, 1001, 101, '2026-01-07');

SELECT count(distinct user_id) AS unique_users
FROM orders;
```

DolphinDB 代码示例，返回结果也是
4。

```
CREATE TABLE orders (
    order_id INT,
    user_id INT,
    product_id INT,
    order_date DATE
);

INSERT INTO orders VALUES(1, 1001, 101, '2026-01-01')
INSERT INTO orders VALUES(2, 1002, 101, '2026-01-02')
INSERT INTO orders VALUES(3, 1001, 102, '2026-01-03')
INSERT INTO orders VALUES(4, 1003, 101, '2026-01-04')
INSERT INTO orders VALUES(5, 1002, 102, '2026-01-05')
INSERT INTO orders VALUES(6, 1004, 103, '2026-01-06')
INSERT INTO orders VALUES(7, 1001, 101, '2026-01-07')

select nunique(user_id) FROM orders;
```
