<!-- Auto-mirrored from upstream `documentation-main/progr/data_types_forms/vector.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 向量

## 概述

向量是一个以给定顺序保存多个对象的容器。向量中元素的索引从0开始。向量中的元素可以被修改。向量中的数据可以是不同的类型，
但是当向量中的所有元素都是相同类型时性能最佳。本节讨论由相同数据类型的多个标量元素组成的向量（也称为“强类型向量”）。 下一节 Tuple (ANY Vector)
讨论由不同数据类型的元素或不是标量的元素组成的向量（也称为“元组”或“ANY向量”）。

## 创建向量

创建一个向量可使用以下方法：

* 以空格分隔元素。

  ```
  x = 3 6 1 5 9;
  x;
  // output: [3,6,1,5,9]
  // 类型向量始终显示在方括号内，而元组总是显示在圆括号内。

  x=10 2.5;
  typestr x;
  // output： FAST DOUBLE VECTOR
  // 注意这是DOUBLE类型向量，不是一个元组。系统把10解释为DOUBLE类型，不是INT类型。

  x = 3 NULL 6 1 NULL 9;
  x;
  // output: [3,,6,1,,9]

  typestr x;
  // output: FAST INT VECTOR
  ```

  若字符向量的所有元素均为字母或单词，我们提供一个使用反引号“`”的快捷方式来创建此字符向量：

  ```
  x=`IBM`MS`GOOG`YHOO`EBAY;
  x;
  // output: ["IBM","MS","GOOG","YHOO","EBAY"]
  ```

  若字符串向量的元素包含空格，必须使用双引号或单引号来创建字符串向量。

  ```
  x="Goldman Sachs" ‘Morgan Stanley’;
  x;
  // output: ["Goldman Sachs","Morgan Stanley"]
  ```
* 以逗号分隔元素，，外面加上中括号。向量内的元素可以跨行书写。

  ```
  x = [3,6,1,5,9];
  x;
  // output: [3,6,1,5,9]

  size x;
  // output: 5

  // 也可跨行书写
  x = [3,6,1
  ,5,9]
  x
  // output: [3,6,1,5,9]

  // 用以下代码和x比较：
  y = [3 6 1 5 9];
  y;
  // output: ([3,6,1,5,9])

  size y;
  // output: 1
  // 因为我们没有用逗号分隔y中的值，所以y被看成是只包含单个元素的向量。
  ```
* 用 seq 定义向量：

  ```
  x=1..10
  x;
  // output: [1,2,3,4,5,6,7,8,9,10]
  ```
* 随机序列向量。下面这个例子说明了如何用 rand 函数产生一个随机向量。

  ```
  x=rand(3,10);
  // 用0,1和2生成一个长度为10的随机向量。
  x;
  // output: [0,0,2,1,1,2,1,1,2,0]

  timestamp=09:30:00+rand(60,5);
  timestamp;
  // output: [09:30:25,09:30:00,09:30:40,09:30:19,09:30:53]

  price=5.0+rand(100.0,5)
  price;
  // output: [32.826156,13.066499,52.872136,70.885178,104.408126]
  ```
* 使用 array 函数。

  ```
  x = array(INT, 0);
  //初始化一个空的int类型向量。
  x;
  // output: []

  x.append!(1..10);
  // 在创建一个向量后，可以用 append! 函数扩展它。
  x;
  // output: [1,2,3,4,5,6,7,8,9,10]
  ```

  DolphinDB在`array`函数中提供了一个 *capacity*
  参数。如果正确使用，可以提升性能。详情请参考 array 函数。
* 矩阵中的某列。例如，下例中矩阵m的第一列：

  ```
  m=1..6$2:3;
  m;
  ```

  | #0 | #1 | #2 |
  | --- | --- | --- |
  | 1 | 3 | 5 |
  | 2 | 4 | 6 |

  ```
  m[0];
  // output: [1,2]
  ```
* 数据表中的某列。例如，trades.qty 表示数据表 trades 中的 qty 列。

  ```
  trades=table(`A`B`C as sym, 100 200 300 as qty);
  trades.qty;
  // output: [100, 200, 300]
  ```

### **创建 SYMBOL 类型向量**

1. 使用函数 array来创建。

   ```
   syms=array(SYMBOL, 0, 100);    // 创建长度为100的空符号数组;
   typestr syms;
   ```

   返回：FAST SYMBOL
   VECTOR

   ```
   syms.append!(`IBM`C`MS);
   syms;
   ```

   返回：["IBM","C","MS"]
2. 通过类型转换：

   ```
   syms=`IBM`C`MS;
   typestr syms;
   ```

   返回：STRING
   VECTOR

   ```
   sym=syms$SYMBOL; // 转换为符号向量;
   typestr sym;
   ```

   返回： FAST SYMBOL
   VECTOR

   ```
   typestr syms;
   ```

   返回：STRING
   VECTOR
3. 使用随机函数 rand。

   ```
   syms=`IBM`C`MS;
   symRand=rand(syms, 10);  //生成一个随机的symbol类型向量
   symRand;
   ```

   得到：["IBM","IBM","IBM","MS","C","C","MS","IBM","C","MS"]

   ```
   typestr symRand;
   ```

   返回：FAST
   SYMBOL VECTOR

   注：

   在上面的例子中，当
   `rand` 函数的输入是一个字符串向量时，它会生成一个 symbol
   类型的向量。`rand`
   函数不会更改任何其他的输入数据类型。之所以设计这个函数时有意做出这个例外，这是因为基于字符串向量生成随机向量时，在大多数情况下，用户希望使用
   symbol 类型向量。

## 访问向量

我们可以使用 X[Y] 的形式访问向量，其中 Y 可以是整数，布尔向量，整数向量或数据对。

* 按位置访问向量。要访问向量 X 中的第i个元素，使用 X[i]。i 从0开始。

  ```
  x=3 6 1 5 9;
  x[1];
  // output: 6
  ```
* 使用布尔索引访问向量 X 的子向量。只返回布尔索引向量中 true 对应的元素。布尔索引向量应与 X
  所含元素数量一致。

  ```
  x=3 6 1 5 9;
  y= true false true false false;
  x[y];
  // output: [3,1]

  x[x>3];
  // output: [6,5,9]

  x[x%3==0];
  // output: [3,6,9]
  ```
* 使用索引向量访问向量 X 的子向量。索引向量包含要保留的元素的位置索引。

  ```
  x=3 6 1 5 9;
  y=4 0 2;
  x[y];
  // output: [9,3,1]
  ```
* 使用 X[a:b] 的格式访问向量X的子向量，其中
  0<=a,b<=size(X)。索引的上限边界不在范围内。

  ```
  x=3 6 1 5 9;
  x[1:3];
  // output: [6,1]

  x[3:1];
  // output: [1,6]
  // 反方向

  x[1:];
  // output: [6,1,5,9]
  // 从位置1开始访问向量的剩余部分
  x[:3];
  // output: [3,6,1]
  // 访问向量的前三个元素

  x[:];
  // output: [3,6,1,5,9]
  // 访问向量的所有元素
  ```

  函数 size 返回向量的所有元素数量，而 count 返回向量中的非NULL值的所有元素的数量。

  ```
  x=3 6 NULL 5 9;
  size x;
  // output: 5
  count x;
  // output: 4
  ```

## 修改向量

向量的元素可以被修改或删除；也可以给向量增加新的元素。但是，不可在向量里除了最后一个位置以外的其它位置插入元素。

我们可以使用 pop!
函数来删除向量的最后一个元素。也可以使用 remove!
函数来删除向量指定位置的元素。

```
x = 3 6 1 5 9;
x[1]=4;
x;
// output: [3,4,1,5,9]

x.append!(10 11 12);
// output: [3,4,1,5,9,10,11,12]
x;
// output: [3,4,1,5,9,10,11,12]

x.pop!();
// output: 12
x;
// output: [3,4,1,5,9,10,11]

// 删除 x 中第一个元素（从0开始编号）
x.remove!(0)
x;
// output: [4,1,5,9,10,11]
// 删除 x 中多个元素
x.remove!(2 4)
x;
// output: [4,1,9,11]
```

我们使用 y=x 时，系统将创建一个 x 的拷贝，并把它赋值给 y。因此，"y=x; y[i]=a;"不会影响向量 x。这一点我们和 Python 是不同的。

```
x = 3 6 1 5 9;
y=x;
y;
// output: [3,6,1,5,9]

y[1]=5;
y;
// output: [3,5,1,5,9]

x;
// output: [3,6,1,5,9]
```

如果我们使用 &y=x，x 和 y 都指向同一个对象。修改 x 或 y 也将自动更新另一个。

```
x = 3 6;
&y=x;
y;
// output: [3,6]

y[1]=5;
x;
// output: [3,5]

x[0]=6;
y;
// output: [6,5]
```

若需替换子向量，可以使用以下语句：x[begin:end] = y。y 可为一个向量或标量。请注意不包含上限边界值。

```
x = 3 4 1 5 9;
x[3:5]=7..8;
x;
// output: [3,4,1,7,8]

x[2:]=1;
x;
// output: [3,4,1,1,1]

x[:]=2;
x;
// output: [2,2,2,2,2]
```

用一个布尔表达式替换一个子向量：x[boolean expression] = y

```
x=`IBM`MS`GOOG`YHOO`EBAY;
x[x==`MS]=`GS
x;
// output: ["IBM","GS","GOOG","YHOO","EBAY"]

x=1..10;
x[x%3==0]=99;
x;
// output: [1,2,99,4,5,99,7,8,99,10]

x=6 4 2 0 2 4 6;
x[x>3];
// output: [6,4,4,6]

shares=500 1000 1000 600 2000;
prices=25.5 97.5 19.2 38.4 101.5;
prices[shares>800];
// output: [97.5,19.2,101.5]
```

## 往向量中追加不同类型的数据

如果在强类型向量中增加与现有数据类型不同类型的数据会发生什么？此操作只有在新数据能够被转化为与向量相同的数据类型时才能成功，否则操作失败。例如，我们不能往一个 INT
向量中增加 STRING 类型的数据。

```
// 往一个INT的向量里追加一个STRING
x=1 2 3;
typestr x;
// output: FAST INT VECTOR
x.append!(`orange);
// output: Incompatible type. Expected: INT, Actual: STRING

// 往一个INT的向量里追加一个DOUBLE
x.append!(4.3);
// output: [1,2,3,4]
typestr x;
// output: FAST INT VECTOR

// 往一个INT的向量里追加一个BOOL
x.append!(false);
// output: [1,2,3,4,0]
typestr x;
// output: FAST INT VECTOR

// 往一个STRING的向量里追加一个INT
x=`C `GS `MS;
x.append!(4);
// output: ["C","GS","MS","4"]
x[3];
// output: 4
typestr x[3];
// output: STRING
```

## 向量处理常用函数

函数 reverse 把输入的向量的元素按相反顺序输出为一个新的向量。

```
x=1..10;
y=reverse x;
y;
// output: [10,9,8,7,6,5,4,3,2,1]
x;
// output: [1,2,3,4,5,6,7,8,9,10]
```

函数 shuffle 把输入的向量中的元素随机打乱顺序后输出为一个新的向量。

```
x=1..10;
shuffle x;
// output: [9,2,10,3,1,6,8,4,5,7]
x;
// output: [1,2,3,4,5,6,7,8,9,10]
```

和函数 *shuffle* 不同，函数 shuffle! 函数会把输入的向量中的元素随机打乱顺序以改变输入向量，而不输出一个新的向量。

```
x=1..10;
shuffle!(x);
// output: [8,10,1,3,2,4,7,5,6,9]
x;
// output: [8,10,1,3,2,4,7,5,6,9]
```

函数 join 将两个向量连接后返回一个新的向量。

```
x=1..3;
y=4..6;
z=join(x, y);
z;
// output: [1,2,3,4,5,6]
x join y join y;
// output: [1,2,3,4,5,6,4,5,6]
```

函数 cut(X, a) 将向量拆分成子向量，其中 a 是每个子向量的元素数量。要合并向量列表，请使用函数
flatten。

```
x=1..10;
x cut 2;
// output: [[1,2],[3,4],[5,6],[7,8],[9,10]]  // 这是一个元组。

x cut 3;
// output: [[1,2,3],[4,5,6],[7,8,9],[10]]   // 剩下的“10”这个元素构成一个元组。
x cut 5;
// output: [[1,2,3,4,5],[6,7,8,9,10]]

x cut 9;
// output: [[1,2,3,4,5,6,7,8,9],[10]]

flatten (x cut 9);
// output: [1,2,3,4,5,6,7,8,9,10]
```

函数 take(X, n) 从向量X的第一个元素开始，获取 n 个元素。如果 n 大于 X 的元素数量，则取尽 X
的元素后，返回到 X 的第一个元素继续获取，依次循环。

```
x=3 6 1 5 9;
x take 3;
// output: [3,6,1]
take(x,12);
// output: [3,6,1,5,9,3,6,1,5,9,3,6]
```

以下3个函数使得处理时间序列分析中的领先滞后关系非常方便。

* prev(X)：将 X 的所有元素往右移动一个位置。
* next(X)：将 X 的所有元素往左移动一个位置。
* move(X,a)：如果 a 是正数，将 X 的所有元素往右移动 a 个位置；如果 a
  是负数，将 X 的所有元素往左移动 a 个位置。

```
x=3 6 1 5 9;
y=prev x;
y;
// output: [,3,6,1,5]

z = next x;
z;
// output: [6,1,5,9,]

v=x move 2;
v;
// output: [,,3,6,1]

x move -2;
// output: [1,5,9,,]
```

## 在向量里搜索

对 X 中的每个元素，函数 in(X,Y) 检查它是否存在于向量 Y 中。

```
x = 4 5 16;
y = 3 6 1 5 9 4 19 31 2 8 7 2;
x in y;
// output: [1,1,0]
// 4和5都在 y 中; 16不在 y 中

in(x,y);
// output: [1,1,0]
```

函数 at 返回满足给定条件的向量 X 中的元素的位置。

```
x=1 2 3 2 1;
at(x==2);
// output: [1,3]

at(x>2);
// output: [2]
```

对 Y 中的每个元素，函数 find(X, Y) 返回其在向量 X
中第一次出现的位置，其中Y可以是标量或向量。若其在向量X中不存在，则函数返回-1。

```
x = 8 6 4 2 0 2 4 6 8;
find(x,2);
// output: 3

y= 6 0 7;
x find y;
// output: [1,4,-1]
```

当用 *find*
函数在一个大向量中搜索另一个大向量中的元素时，系统将自动构建一个字典来优化性能。然而，当在一个大向量中仅搜索几个值时，系统不会构造一个字典来优化性能。在搜索中是否建立字典是系统动态确定的。如果我们有一个已经排序的向量，而且只需要搜索少量的数据，应当使用
binsrch 函数，因为构建大型数据集的字典可能需要大量的时间和内存。

函数 binsrch(X, Y) 返回向量 X 中 Y 的每个元素首次出现的位置，其中Y可以是标量或向量。X
必须按升序排序。如果 Y 的某个元素不在X中，则返回-1。

```
x = 1..10;
x binsrch 2;
// output: 1
y= 4 5 12;
x binsrch y;
// output: [3,4,-1]
```

函数 searchK(X, a) 返回向量 X 中第 a 小的值，其中 X 必须是向量，a 必须是标量。向量 X
不需要排序。

```
x=9 9 6 6 6 3 0 0;
searchK(x,1);
// output: 0
searchK(x,2);
// output: 0
searchK(x,3);
// output: 3
searchK(x,4);
// output: 6
searchK(x,5);
// output: 6
searchK(x,6);
// output: 6
searchK(x,7);
// output: 9
```

当我们计算某个特定日期的股票的市盈率时，我们使用最近公布的收益，而不是当天公布的收益，因为企业收益一年只会宣布4次。在这种情况下，可以使用 asof 函数。

假设一个向量 X 已经按升序排列，对于向量 Y 中的每个元素 y, 函数 asof(X, Y) 返回 X 中不大于 y 的最后一个元素的索引。实际应用中，X 和 Y 经常都是时间类型。另请参见
"asof-join"。

```
// 电话号码更改的数据
x=[2005.12.01, 2007.03.15, 2010.12.24, 2013.08.31];
y="(201) 1234-5678" "(212) 8467-5523" "(312) 1258-6679" "(212) 4544-8888";

// 取得 2005.12.01 和 2010.12.25两天的电话号码
y[asof(x, [2005.12.01,2010.12.25])];
// output: ["(201) 1234-5678","(312) 1258-6679"]
```

## 向量的元素排序

函数 [sort(X, [boolean])](../../funcs/s/sort.html) 对向量 X 的元素进行排序，并返回一个新向量。对于本小节提到的函数，当
boolean 值为 true（默认值）时，按升序排序，否则按降序排列。

```
x = 3 6 1 5 9;
y = sort x;
y;
// output: [1,3,5,6,9]
y = sort(x, false);
// 把x按降序排列。
y;
// output: [9,6,5,3,1]
```

函数 [isort(X, [boolean])](../../funcs/i/isort.html) 返回 sort(X) 的每个元素在X中的位置。X[isort X]
等价于 sort(X)。

```
isort x;
// output: [2,0,3,1,4]
// 2 0 3 1 4 是 1 3 5 6 9 在 x 里面的索引号

isort(x, false);
// output: [4,1,3,0,2]

x[isort x];
// output: [1,3,5,6,9]
```

与之对照，[rank(X, [boolean])](../../funcs/r/rank.html) 返回X的每个元素在 sort(X) 中的位置。

```
rank x;
// output: [1,3,0,2,4]

rank(x, false);
// output: [3,1,4,2,0]
// 向量x中每个元素按降序的排名。
```

函数 sort! 将排序过后的结果赋值给输入变量。

```
x= 3 6 1 5 9;
sort!(x);
// output: [1,3,5,6,9]
x;
// output: [1,3,5,6,9]
```

## 向量和运算符

所有运算符都能用于向量的计算。关于更多的例子和说明，请参考以下章节：

* 运算符
* 函数。

```
x = 1 2 3;
y = 4 5 6;
x * y;
// output: [4,10,18]

x / y;
// output: [0,0,0]
// 当 x 和 y 都是整数时，“/” 表示整数除法，相当于对每个对应的元素使用 floor 函数。

x \ y;
// output: [0.25,0.4,0.5]

3 * x;
// output: [3,6,9]

x ** y;
// output: 32
// 等于 1*4 + 2*5 + 3*6
```

大多数情况下，涉及 NULL 值的运算的结果是 NULL 值，但也有例外。请参考 NULL值的操作。

```
x = 3 NULL 1 NULL 9;
y = 4 5 2 3 NULL;
x+y;
// output: [7,,3,,]
x>0;
// output: [1,0,1,0,1]
```

## 在函数中使用向量

以下是在函数中使用向量的例子。关于更多的例子和说明，请参考 函数。

```
x= 3 6 1 5 9;
avg x;
// output: 4.8

med x;
// output: 5

sum x;
// output: 24

std x;
// output: 3.03315

log x;
// output: [1.098612,1.791759,0,1.609438,2.197225]

exp x;
// output: [20.085537,403.428793,2.718282,148.413159,8103.083928]

x pow 2;
// output: [9,36,1,25,81]

x = 1 2 3;
y = 1 2 2;
x wavg y;
// output: 2.2
// 对向量 x 计算加权平均数，y 为权。相当于 (1*1+2*2+3*2)/(1+2+2)

x = 3 NULL NULL NULL 9;
avg x;
// output: 6
// 计算向量 x 的平均值，忽略 NULL 值。

y = 1 2 3 4 5;
x wavg y;
// output: 8
```

## 函数向量

向量的元素也可以是函数。一个应用场景是：许多函数都使用同一个输入变量，并且这些函数的结果都是相同的数据类型。

```
x=[3.1, 4.5, 6];
desp=[std, avg, sum, median, max, min];
desp(x);
// output: [1.450287,4.533333,13.6,4.5,6,3.1]

// 和函数向量组合使用。
desp=[log, std, avg, sum, median, max, min];
desp(x);
```

| log | std | avg | sum | med | max | min |
| --- | --- | --- | --- | --- | --- | --- |
| 1.131402 | 1.450287 | 4.533333 | 13.6 | 4.5 | 6 | 3.1 |
| 1.504077 | 1.450287 | 4.533333 | 13.6 | 4.5 | 6 | 3.1 |
| 1.791759 | 1.450287 | 4.533333 | 13.6 | 4.5 | 6 | 3.1 |
