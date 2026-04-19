# notIn

首发版本：3.00.3

## 语法

`notIn(X, Y)`

## 详情

* 若 *Y* 是标量：
  + 当 Y 是非时间类型时，检查 *X* 和 *Y* 是否不相等；
  + 当 *Y* 是时间类型时，检查 *X* 中的每个元素是否不在 *Y* 中。
  + 当 *Y* 是空值时，无论 *X* 为何值都返回 true。
* 若 *Y* 是向量，检查 *X* 中的每一个元素是否不在 *Y* 中。
* 若 *Y* 是字典，检查 *X* 中的每一个元素是否不是 *Y* 中的键。
* 若 *Y* 是单列内存表，检查 *X* 中的每一个元素是否不是 *Y* 唯一列中的值。**注：**
  表中单列的类型不能是数组向量。
* 若 *Y* 是键值表或索引内存表，检查 *X* 中的每一个元素是否不是 *Y* 中的主键。*X* 中元素的个数必须与
  *Y* 中主键列的个数一致。

## 参数

**X** 可以是标量、向量、元组、矩阵、数组向量、字典、单列内存表、键值内存表或索引内存表。

**Y** 可以是标量、向量、字典、单列内存表、键值内存表或索引内存表。

## 返回值

布尔类型标量或向量。

## 例子

```
x=18:21:35+0..2
y=18:21:35
notIn(x,y)
// output: [false,true,true]

notIn(3 3 5 2, 2 3);
// output: [false,false,true,false]

x=dict(INT,DOUBLE);
x[1, 2, 3]=[4.5, 6.6, 3.2];
x;
/* output
3->3.2
1->4.5
2->6.6
*/

notIn(1..6, x);
// output: [false,false,false,true,true,true]

t = table(1 3 5 7 9 as id)
2 3 notIn t
// output: [true,false]

kt = keyedTable(`name`id,1000:0,`name`id`age`department,[STRING,INT,INT,STRING])
insert into kt values(`Tom`Sam`Cindy`Emma`Nick, 1 2 3 4 5, 30 35 32 25 30, `IT`Finance`HR`HR`IT)
notIn((`Tom`Cindy, 1 3), kt);
// output: [false,false]

t1 = indexedTable(`sym`side, 10000:0, `sym`side`price`qty, [SYMBOL,CHAR,DOUBLE,INT])
insert into t1 values(`IBM`MSFT`GOOG, ['B','S','B'], 10.01 10.02 10.03, 10 10 20)
notIn((`IBM`MSFT, ['S','S']), t1);
// output: [true,false]
```

*X* 为浮点型，*Y* 为整型，数据类型不一致，会将 *X* 转换为与 *Y* 一致的类型进行比较。

```
notIn(10, NULL)
// output: true

notIn('a', 97)
// output: false

notIn(1, 1.1 1.2 1.3)
// output: true

notIn(float(1.1 2.2 3.3 4.4 5.5 6.6 7.7 8.8), 1..9)
// output: [false,false,false,false,false,false,false,false]
```

`notIn` 可以搭配 `select` 使用，用于限定条件的筛选的范围：

```
select * from kt where name notIn [`Tom, `Cindy];
```

| name | id | age | department |
| --- | --- | --- | --- |
| Sam | 2 | 35 | Finance |
| Emma | 4 | 25 | HR |
| Nick | 5 | 30 | IT |

`notIn` 亦可应用于对分布式表的查询中：

```
login(`admin,`123456)
dbName="dfs://database1"
if(existsDatabase(dbName)){
	dropDatabase(dbName)
}
db=database(dbName,VALUE,2019.01.01..2019.01.03)
n=100
datetime=take(2019.01.01 +0..100,n)
sym = take(`C`MS`MS`MS`IBM`IBM`IBM`C`C$SYMBOL,n)
price= take(49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29,n)
qty = take(2200 1900 2100 3200 6800 5400 1300 2500 8800,n)
t=table(datetime, sym, price, qty)
trades=db.createPartitionedTable(t,`trades,`datetime).append!(t)

select * from trades where sym notIn `IBM`C
```

相关函数：in
