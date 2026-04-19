<!-- Auto-mirrored from upstream `documentation-main/progr/file_io/process_txt.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 文本文件处理

对于基本的文本文件读写操作，我们提供了五个函数：

* *readLine*
* *readLines*
* *readLines!*
* *writeLine*
* *writeLines*

当系统读取文本文件时，回车字符、换行字符或者回车换行字符的组合会被当作行的分隔符。当系统往一个文件中写入一行时，行分隔符会被附加到这行的后面。行分隔符在不同的操作系统上也是不同的。在WINDOWS中，行分隔符为回车符和换行字符的组合。在其他系统中，行分隔符为换行字符。

## 读写单行

writeLine
函数把一行写入到指定文件中。该函数将会自动附加一个行分隔符到写入行的后面。因此该字符串不需要以行分隔符结尾。如果操作成功，函数返回1；否则抛出IOExeception。readLine
函数从给定文件中读取一行。读取的行不包含行分隔符。如果到达文件尾，函数返回一个NULL对象，该对象可以用isVoid函数来判断是否已读完文件。如果由于其他原因该操作失败了，将抛出IOException。

```
x=`IBM`MSFT`GOOG`YHOO`ORCL
eachRight(writeLine, file("test.txt","w"), x)
fin = file("test.txt")
do{
   x=fin.readLine()
   if(x.isVoid()) break
   print x
}while(true);

IBM
MSFT
GOOG
YHOO
ORCL
```

## 读写多行

writeLines
函数往指定文件中写入多行。该函数自动添加换行符到每一行数据后面。如果操作成功，函数返回写入的行数；否则抛出IOException。readLines
函数从文件中读取指定数量的行。默认行数为1024。当到达文件尾或者指定行数全部读完，该函数返回。如果实际读取的行数小于要求读取的行数，那么表明已到达文件尾。如果由于其他原因该操作失败了，抛出IOException。

```
timer(10){
   x=rand(`IBM`MSFT`GOOG`YHOO`ORCL,10240)
   eachRight(writeLine, file("test.txt","w"),x)
   fin = file("test.txt")
   do{ y=fin.readLine() }while(!y.isNull())
   fin.close()
};

Time elapsed: 271.035 ms

timer(10){
   x=rand(`IBM`MSFT`GOOG`YHOO`ORCL,10240)
   file("test.txt","w").writeLines(x)
   fin = file("test.txt")
   do{ y=fin.readLines(1024)}while(y.size()==1024)
   fin.close()
};

Time elapsed: 33.503 ms
```

上例比较了单行处理和多行处理的性能。可以看到，多行处理比单行处理快了约9倍。readLines
函数为每次调用都创建了一个字符串向量。创建向量需要花费时间，所以如果可以把相同向量当作缓冲区使用，就能减少时间开销。`readLines!`函数正是使用这样的方式来提高速度。

下面两个例子每次读取相同数量的数据，执行100次，结果显示：`readLines!`要比`readLines`函数快。

```
timer(100){
   fin = file("test.txt")
   do{ y=fin.readLines(1024) } while(y.size()==1024)
   fin.close()
};

Time elapsed: 79.511 ms

timer(100){
   fin = file("test.txt")
   y=array(STRING,1024)
   do{ lines = fin.readLines!(y,0,1024) } while(lines==1024)
   fin.close()
};

Time elapsed: 56.034 ms
```
