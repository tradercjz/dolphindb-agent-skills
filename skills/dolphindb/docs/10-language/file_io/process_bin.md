<!-- Auto-mirrored from upstream `documentation-main/progr/file_io/process_bin.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 二进制文件处理

DolphinDB 提供了一系列用于处理二进制文件的函数，包括原始字节读写以及高层次对象读写。

## 读写原始字节

`writeBytes` 函数将整个缓冲区写到文件中，该缓冲区必须是 CHAR 标量或者 CHAR
向量。如果操作成功，函数将返回实际写入成功的字节数；否则抛出
IOException。`readBytes`函数从文件中读取指定数量的字节。如果到达文件尾或遇到了 I/O 错误，则抛出
IOException；否则函数返回包含指定数量字节的缓冲区。因此，编写代码时候首先要知道确定读取字节数。

```
// 定义一个文件拷贝函数
def fileCopy(source, target){
 s = file(source)
 len = s.seek(0,TAIL)
 s.seek(0,HEAD)
 t = file(target,"w")
 if(len==0) return
 do{
    buf = s.readBytes(min(len,1024))
    t.writeBytes(buf)
    len -= buf.size()
 }while(len)

}

fileCopy("test.txt","testcopy.txt");
```

`readBytes`函数总是返回一个新的 CHAR
向量。类似文本文件处理一节中讨论过的，创建新向量缓冲区需要花费时间，为了提高性能，可以创建一个缓冲区并反复重使用这个缓冲区，`read!`函数正是用于此目的。`read!`函数的另一个优点是不需要事先知道需要读取的字节数。如果到达文件尾或者指定数量的字节已经读取完毕，`read!`
直接返回。如果成功读取的字节数少于期望值，则表示已经到达文件尾。

```
// 用read!和write函数定义一个文件拷贝函数
def fileCopy2(source, target){
 s = file(source)
 t = file(target,"w")
 buf = array(CHAR,1024)
 do{
    numByte = s.read!(buf,0,1024)
    t.write(buf,0, numByte)
 }while(numByte==1024)
}

fileCopy2("test.txt","testcopy.txt");
```

文件复制函数的性能主要由写入部分决定的。为了比较 *readBytes* 和 *read!* 的性能，我们设计了以下例子进行对比：

```
fileLen = file("test.txt").seek(0, TAIL)
timer(1000){
   fin = file("test.txt")
   len = fileLen
   do{
      buf = fin.readBytes(min(len,1024))
      len -= buf.size()
   }while(len)
};

Time elapsed: 210.593 ms

timer(1000){
   fin = file("test.txt")
   buf = array(CHAR,1024)
   do{numBytes = fin.read!(buf,0,1024)}while(numBytes==1024)
};

Time elapsed: 194.519 ms
```

由此可见，read! 的速度比 readBytes 要快。

*readRecord!* 函数将二进制文件转换为 DolphinDB 的数据对象。read Record!
函数基于行读取二进制文件，每行包含的记录有相同的数据类型和固定的长度。如一个二进制文件包含了 5 个数据域，分别具有下述数据类型（长度）：CHAR(1),
BOOLEAN(1), SHORT(2), INT(4), LONG(8), 和 DOUBLE(8)，那么 readRecord! 函数将把每行视为 24
个字节。

下例介绍 readRecord! 函数导入一个二进制文件：<https://cdn.dolphindb.cn/zh/tutorials/data/binSample.bin>

创建内存表

```
tb=table(1000:0, `id`date`time`last`volume`value`ask1`ask_size1`bid1`bid_size1, [INT,INT,INT,FLOAT,INT,FLOAT,FLOAT,INT,FLOAT,INT])
```

调用 file 函数打开文件，并通过 readRecord! 函数导入二进制文件，数据会被加载到 tb 表中。

```
dataFilePath="E:/DolphinDB/binSample.bin"
f=file(dataFilePath)
f.readRecord!(tb);
select top 5 * from tb;
```

| id | date | time | last | volume | value | ask1 | ask\_size1 | bid1 | bid\_size1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 20190902 | 91804000 | 0 | 0 | 0 | 11.45 | 200 | 11.45 | 200 |
| 2 | 20190902 | 92007000 | 0 | 0 | 0 | 11.45 | 200 | 11.45 | 200 |
| 3 | 20190902 | 92046000 | 0 | 0 | 0 | 11.45 | 1200 | 11.45 | 1200 |
| 4 | 20190902 | 92346000 | 0 | 0 | 0 | 11.45 | 1200 | 11.45 | 1200 |
| 5 | 20190902 | 92349000 | 0 | 0 | 0 | 11.45 | 5100 | 11.45 | 5100 |

readRecord! 函数不支持字符串类型的数据，上表中 date 列和 time 列的数据类型为 INT。可以使用 temporalParse
函数进行日期和时间类型数据的格式转换，再使用 replaceColumn! 函数替换表中原有的列。

```
tb.replaceColumn!(`date, tb.date.string().temporalParse("yyyyMMdd"))
tb.replaceColumn!(`time, tb.time.format("000000000").temporalParse("HHmmssSSS"))
select top 5 * from tb;
```

| id | date | time | last | volume | value | ask1 | ask\_size1 | bid1 | bid\_size1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2019.09.02 | 09:18:04.000 | 0 | 0 | 0 | 11.45 | 200 | 11.45 | 200 |
| 2 | 2019.09.02 | 09:20:07.000 | 0 | 0 | 0 | 11.45 | 200 | 11.45 | 200 |
| 3 | 2019.09.02 | 09:20:46.000 | 0 | 0 | 0 | 11.45 | 1200 | 11.45 | 1200 |
| 4 | 2019.09.02 | 09:23:46.000 | 0 | 0 | 0 | 11.45 | 1200 | 11.45 | 1200 |
| 5 | 2019.09.02 | 09:23:49.000 | 0 | 0 | 0 | 11.45 | 5100 | 11.45 | 5100 |

## 读写多字节整型和浮点数

*write* 函数把指定的缓冲区转换为字节流，并保存到文件中。缓冲区可以是各种数据类型的标量或向量。如果发生了错误，将抛出
IOException；否则函数返回写入的元素的个数（而不是字节数）。*read!*
函数将给定数量的元素读取到缓冲区。例如，如果缓冲区是INT向量，该函数将把文件中的字节转换为INT。*write* 和 *read*
函数都涉及到流和字节之间的转换问题以及计算机科学中多字节的大小端问题。大端模式把数据的高字节保存在内存的低地址中，而小端模式把数据的低字节保存在内存的低地址中。*write*
函数通常使用操作系统的大小端模式。如果文件的大小端模式和操作系统的大小端模式不同，*read!* 函数将转换大小端模式。在使用 *file*
函数打开文件时，有一个可选的布尔参数，用来表示文件是否采用小端模式。默认情况下，采用操作系统的大小端模式。

```
x=10h
y=0h
file("C:/DolphinDB/test.bin","w").write(x);

1

file("C:/DolphinDB/test.bin","r",true).read!(y);                // 假定文件是小端字节顺序

1

y;

10

file("C:/DolphinDB/test.bin","r",false).read!(y);                // 假定文件是大端字节顺序

1

y;

2560
```

我们进行了一个简单的试验：写一个值为10的 SHORT 类型整数到文件中，然后通过两种字节顺序来把该整数读取到另一个 SHORT
整型变量中。与预期一致，两个值分别为10和2560。如果在同一台机器上执行所有的操作，那么不需要考虑大小端问题。但是在一个分布式系统中，必须要注意网络字节流和文件的大小端模式。上述例子使用了一个标量作为缓冲区用来读写。我们再给出一个使用INT向量作为缓冲区的例子。该例子生成100万个0-10000之间的随机整数，保存它们到一个文件中，然后将他们读到一个小缓冲区中并求和。

```
n=1000000
x=rand(10000,n)
file("test.bin","w").write(x,0,n)
sum=0
buf=array(INT,1024)
fin=file("test.bin")
do{
   len = fin.read!(buf,0, 1024)
   if(len==1024)
      sum +=buf.sum()
   else
      sum += buf.subarray(0:len).sum()
}while(len == 1024)
fin.close()
sum;

4994363593
```

除了数字之外，字符串也可以以二进制形式保存到文件中。NULL 字符（值为0的字节）附加在字符串结尾作为字符串分隔符。所以如果一个字符串的长度为
n，那么实际写入文件的字节数为 n+1。下例展示了 *write* 和 *read!*
函数处理字符串读写。我们首先生成100万个随机股票号并以二进制格式保存到一个文件中。然后使用一个小缓冲区顺序地读出整个文件。在每一次读取之后，我们使用了
*dictUpdate!* 函数来统计词频。

```
file("test.bin","w").write(rand(`IBM`MSFT`GOOG`YHOO`C`FORD`MS`GS`BIDU,1000000));

1000000
```

```
words=dict(STRING,LONG)
buf=array(STRING,1024)
counts=array(LONG,1024,0,1)
fin=file("test.bin")
do{
   len = fin.read!(buf,0,1024)
   if(len==1024)
      dictUpdate!(words, +, buf, counts)
   else
      dictUpdate!(words, +, buf.subarray(0:len), counts.subarray(0:len))
}while(len==1024)
fin.close();

words;

MSFT->111294
BIDU->110800
FORD->110916
GS->111233
MS->110859
C->110591
YHOO->111069
GOOG->111972
IBM->111266

words.values().sum();

1000000
```

## 读写对象

*read!* 和 *write*
函数操作二进制数据时提供了很大的灵活性，但是必须知道读写元素的准确个数以及数据类型，因此当处理复杂数据结构如矩阵、表或元组时，我们需要设计一种复杂的协议来协调读写操作。我们提供了两个高阶函数，readObject 和 writeObject
用来处理对象的读写。所有数据结构包括标量、向量、集合、字典和表都可以使用这两个函数。

```
a1=10.5
a2=1..10
a3=cross(*,1..5,1..10)
a4=set(`IBM`MSFT`GOOG`YHOO)
a5=dict(a4.keys(),125.6 53.2 702.3 39.7)
a6=table(1 2 3 as id, `Jenny`Tom`Jack as name)
a7=(1 2 3, "hello world!", 25.6)

fout=file("test.bin","w")
fout.writeObject(a1)
fout.writeObject(a2)
fout.writeObject(a3)
fout.writeObject(a4)
fout.writeObject(a5)
fout.writeObject(a6)fout.writeObject(a7)
fout.close();
```

上面的脚本写了7种不同类型的对象到一个文件中。下面的脚本从文件中读出这7个对象并打印这些对象的简短描述：

```
fin = file("test.bin")
for(i in 0:7) print typestr fin.readObject()
fin.close();

DOUBLE
FAST INT VECTOR
INT MATRIX
STRING SET
STRING->DOUBLE Dictionary
TABLE
ANY VECTOR
```
