<!-- Auto-mirrored from upstream `documentation-main/plugins/plg_dev_adv.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 插件开发深度解析

DolphinDB 支持动态加载外部插件，以扩展系统功能。插件用 C++ 编写，需要编译成 *.so* 或 *.dll* 共享库文件。插件使用的整体流程请参考：插件介绍与使用，开发插件的方法和注意事项请参考 DolphinDB 插件开发教程。本文着重解析插件开发中的一些其他常见问题。

## 1. 创建对象

编写插件时，DolphinDB 中的大部分数据对象都可以用 Constant 类型来表示（标量、向量、矩阵、表，等等），使用时调用 ConstantSP 进行操作，ConstantSP 是一个经过封装的智能指针，会在变量的引用计数为 0 时自动释放内存，不需要用户手动释放。从它派生的其它常用变量类型有：VectorSP（向量）、TableSP（表）等。

### 1.1. 创建标量

插件中创建标量可以直接用 new 语句创建头文件 ScalarImp.h 中声明的类型对象，并将它赋值给一个 ConstantSP；也可以使用 `Util::createConstant` 创建指定类型的标量，并用对应的 `set` 方法赋值，这种方法比较麻烦，不推荐使用。

```
ConstantSP i = new Int(1);                 // 相当于 1i
ConstantSP i1 = Util::createConstant(DT_INT);
i1->setInt(1);                             // 也相当于 1i

ConstantSP s = new String("DolphinDB");    // 相当于"DolphinDB"
ConstantSP s1 = Util::createConstant(DT_STRING);
s1->setString("DolphinDB");                // 也相当于"DolphinDB"

ConstantSP d = new Date(2020, 11, 11);     // 相当于 2020.11.11
ConstantSP d1 = Util::createConstant(DT_DATE);
//由于日期类型没有对应的 set 方法，而 date 在 dolphindb 中存储为 int，为从 1970.01.01 开始经过的天数，所以可以通过换算，并用 setInt 进行赋值
d1->setInt(18577);                         // 也相当于 2020.11.11

ConstantSP voidConstant = new Void();      // 创建一个 void 类型变量，常用于表示空的函数参数
```

### 1.2. 创建非标量

对于非标量，头文件 Util.h 中声明了一系列函数，用于快速创建某个类型的非标量对象。

#### 1.2.1. 创建 Vector

`Util::createVector` 可以创建指定类型的 Vector 对象，需要传入数据类型和长度；`Util::createRepeatingVector` 可以创建相同值的 Vector 对象，需要传入 ConstantSP 对象和长度；`Util::createIndexVector` 可以创建连续的一组数的 Vector 对象，需要传入起始数据和长度：

```
VectorSP v = Util::createVector(DT_INT, 10);     // 创建一个初始长度为 10 的 int 类型向量
v->setInt(0, 60);                                // 相当于 v[0] = 60

VectorSP t = Util::createVector(DT_ANY, 0);      // 创建一个初始长度为 0 的 any 类型向量（元组）
t->append(new Int(3));                           // 相当于 t.append!(3)
t->get(0)->setInt(4);                            // 相当于 t[0] = 4
// 这里不能用 t->setInt(0, 4)，因为 t 是一个元组，setInt(0, 4) 只对 int 类型的向量有效

ConstantSP tem = new Double(2.1);                // 相当于 2.1
VectorSP v1 = Util::createRepeatingVector(tem, 10); // 创建一个初始长度为 10，所有数据为 2.1 的向量

VectorSP seq = Util::createIndexVector(5, 10);   // 创建一个长度为 10，起始值为 5 的向量，相当于 5..14
int seq0 = seq->getInt(0);                       // 相当于 seq[0]
```

#### 1.2.2. 创建 Matrix

`Util::createMatrix`可以创建指定类型的 Matrix 对象，需要传入数据类型、列数、行数以及列容量；`Util::createDoubleMatrix` 可以创建 double 类型的 Matrix 对象，需要传入列数与行数：

```
ConstantSP m = Util::createMatrix(DT_INT, 3, 10, 3); // 创建一个 10 行 3 列，列容量为 3 的 int 类型矩阵
ConstantSP seq = Util::createIndexVector(1, 10);     // 相当于 1..10
m->setColumn(0, seq);                                // 相当于 m[0]=seq

ConstantSP dm = Util::createDoubleMatrix(3, 5);      // 创建一个 5 行 3 列的 double 类型矩阵
```

#### 1.2.3. 创建 Set

`Util::creatSet`可以创建指定类型的 Set 对象，需要传入数据类型、SymbolBaseSP 和长度。SymbolBaseSP 与 symbol 类型相关，一个 symbol 类型数据被 DolphinDB 系统内部存储为一个整数，通过 SymbolBaseSP 映射到对应的字符，若不需要使用可设置为 nullptr：

```
//创建一个初始容量为 0 的 float 类型的集合，第二个参数为 SymbolBaseSP，与 symbol 类型相关，常设置为 nullptr
SetSP s = Util::createSet(DT_FLOAT, nullptr, 0);
s->append(new Float(2.5));                         //相当于 s.append!(2.5)
```

#### 1.2.4. 创建 Dictionary

`Util::createDictionary` 可以创建 Dictionary 对象，需要传入 key 数据类型、SymbolBaseSP、value 数据类型、SymbolBaseSP，创建之后可以调用 `set` 设置 key 和 value：

```
VectorSP keyVec = Util::createIndexVector(1, 5);        // 相当于 1..5，作为 key 值
VectorSP valVec = Util::createVector(DT_DOUBLE, 0, 5);  // 创建一个初始长度为 0，容量为 5 的 double 类型，作为 value
std::vector<double> tem{2.5, 3.3, 1.0, 6.6, 8.8};
valVec->appendDouble(tem.data(), tem.size());           // 向 valVec 添加数据
//创建一个 key 类型为 int、value 类型为 double 的字典对象，第 2、第 4 参数为 SymbolBaseSP，与 symbol 类型相关，非 symbol 类型则设置为 nullptr
DictionarySP d = Util::createDictionary(DT_INT, nullptr, DT_DOUBLE, nullptr);
d->set(keyVec, valVec);                                 // 设置 key 和 value
```

#### 1.2.5. 创建 Table

`Util::createTable`可以创建 Table 对象，常用以下两种方法创建 Table 对象：一是传入列名 vector、列类型、行数、行容量；二是传入列名 vector 和列向量 vector。

```
//方法一
std::vector<std::string> colNames{"col1", "col2", "col3"};         // 存放列名
std::vector<DATA_TYPE> colTypes{DT_INT, DT_BOOL, DT_STRING};       // 存放列类型
//创建一张包含三列的表，列名为 col1, col2, col3, 列类型分别为 int, bool, string 的 0 行、容量为 100 的空表
TableSP t1= Util::createTable(colNames, colTypes, 0, 100);

//方法二
VectorSP v1 = Util::createIndexVector(0, 5);                       // 相当于 0..4
VectorSP v2 = Util::createRepeatingVector(new String("Demo"), 5);  // 创建一个长度为 5，所有数据为"Demo"的向量
VectorSP v3 = Util::createRepeatingVector(new Double(2.5), 5);     // 创建一个长度为 5，所有数据为 2.5 的向量
std::vector<ConstantSP> columns;                                   // 存放列向量
//添加列向量
columns.emplace_back(v1);
columns.emplace_back(v2);
columns.emplace_back(v3);
//用上述创建的列名 vector 和列向量 vector 来创建 table 对象
TableSP t2 = Util::createTable(colNames, columns);
```

#### 1.2.6. 创建 PartialFunction

编写插件时，有时需要固定一个函数的部分参数，产生一个参数较少的函数，这个可以通过 `Util::createPartialFunction` 创建部分应用来实现。在如下所示例子中，`myFunc1`函数需要两个整数参数，计算后返回结果；`myFunc2`函数固定了`myFunc1`第一个参数，返回只需传入一个整数参数的新函数。实现步骤为：

* 首先使用 `Util::createSystemFunction`  创建一个系统函数 `temFunc`，参数为 `myFunc1` 以及参数个数;
* 然后使用 `Util::createPartialFunction` 创建一个部分应用，参数为前面创建的 `temFunc` 以及需要固定的参数。

```
ConstantSP myFunc1(Heap* heap, vector<ConstantSP>& arguments) {
    if (arguments[0]->getType() != DT_INT || arguments[1]->getType() != DT_INT) {
        throw IllegalArgumentException("myFunc1", "argument must be two integral scalars!");
    }
    int a = arguments[0]->getInt();
    int b = arguments[1]->getInt();
    int result = a * b - (a + b);
    return new Int(result);
}
FunctionDefSP myFunc2(Heap* heap, vector<ConstantSP>& arguments) {
    FunctionDefSP temFunc = Util::createSystemFunction("temFunc", myFunc1, 2, 2, false);
    ConstantSP a = new Int(10);
    vector<ConstantSP> args = {a};
    return Util::createPartialFunction(temFunc, args); //固定第一个参数为 10
}
```

插件描述文件命名为 *PluginTest.txt*，内容如下：

```
test,libPluginTest.so
myFunc1,myFunc1,system,2,2,0
myFunc2,myFunc2,system,0,0,0
```

在 DolphinDB 中加载插件并调用函数：

```
loadPlugin("Path_to_PluginTest.txt/PluginTest.txt");  // 加载插件
re1 = test::myFunc1(10, 5);  // re1值为35
newFunc= test::myFunc2();    // 获得一个只需一个参数的新函数
re2 = newFunc(5);            // 调用新函数，re2值为35
```

PartialFunction 更常用的场景是调用 DolphinDB 内置函数时用于固定部分参数。以下例子摘自 DolphinDBPlugin\opc\src\opc\_main.cpp，其中 subscribeTag 的第 3 个参数 handler 可以是表或一元函数，当传入的参数值是表时，调用了 DolphinDb 内置函数 `append!(obj, newData)`，因为 `append!` 有 2 个参数，所以用 `createPartialFunction` 把 table 参数固定，也变为一元函数，这样不管参数值是表或函数，都可以用 `FunctionDef::Call` 调用。

```
ConstantSP subscribeTag(Heap *heap, vector<ConstantSP> &arguments) {
    std::string usage = "Usage: subscribe(conn,Tag,handler). ";

    OPCClient *conn;

    //skipped...

    if (!arguments[2]->isTable() && (arguments[2]->getType() != DT_FUNCTIONDEF)) {
        throw IllegalArgumentException(__FUNCTION__, usage + "handler must be a  table or a unary function.");
    }else if (arguments[2]->getType() == DT_FUNCTIONDEF) {
        if (FunctionDefSP(arguments[2])->getMaxParamCount() < 1 || FunctionDefSP(arguments[2])->getMinParamCount() > 1)
            throw IllegalArgumentException(__FUNCTION__, usage + "handler must be a table or a unary function.");
    }

    FunctionDefSP handler;
    //skipped...

    if (arguments[2]->getType() == DT_FUNCTIONDEF) {
        handler = FunctionDefSP(arguments[2]);
    } else {
        TableSP table = arguments[2];
        FunctionDefSP func = conn->session->getFunctionDef("append!");
        vector<ConstantSP> params(1, table);
        handler = Util::createPartialFunction(func, params);
    }

    //skipped...

    return new Void();
}
```

## 2. 高效读写 Vector 和内存表中的数据

在编写插件时往往需要对 Vector 和内存表中的数据进行读写。DolphinDB 提供了许多读写的接口函数，如果使用不当将影响读写效率，因此下面将介绍如何使用 DolphinDB 提供的这些接口函数实现对 Vector 和内存表的高效读写。

### 2.1. Vector

#### 2.1.1. 读取数据

DolphinDB 中的 Vector 是一个抽象的类，具有多种实现方式。最常见的是实现是常规数组（regular vector），数据存储在连续的内存块中。当使用 Util::createVector 函数创建一个 Vector 时，如果元素个数不超过 1048576 (220) 时，返回的必定是连续存储的常规数组。为了避免由于内存碎片而找不到大块的连续内存，DolphinDB 也提供了 big array，数据分段存储在多个不连续的内存中，每段的元数个数是 1048576 (220) 。除了上面常见的两种实现方式，还有诸如 repeating vector，sub vector 等。

因此，要访问 Vector 的数据，除非明确知道 Vector 是 FastVector 模式（即 isFastMode = true），否则不能直接使用数据的指针对数据进行操作。在编写插件时，最好使用以下介绍的几种接口对 Vector 中的数据进行读写。下面以 int 类型为例，其他数据类型都有类似的接口：

##### 2.1.1.1. int getInt(int index)

`getInt(int index)`是直接通过下标获取对应位置的元素：

```
VectorSP pVec = Util::createVector(DT_INT, 100000000);
int tmp;
for(int i = 0; i < pVec->size(); ++i) {
    tmp = pVec->getInt(i) ;
}
```

##### 2.1.1.2. bool getInt(int start, int len, int\* buf)

第二种方法是用 `getInt(int start, int len, int* buf)`批量（如每次读取 1024 个）将数据复制到指定的 buffer：

```
VectorSP pVec = Util::createVector(DT_INT, 100000000);
int tmp;
const int BUF_SIZE = 1024;
int buf[BUF_SIZE];
int start = 0;
int N = pVec->size();
while (start < N) {
    int len = std::min(N - start, BUF_SIZE);
    pVec->getInt(start, len, buf);
    for (int i = 0; i < len; ++i) {
        tmp = buf[i];
    }
    start += len;
}
```

##### 2.1.1.3. const int\* getIntConst(int start, int len, int\* buf)

第三种是用`getIntConst(int start, int len, int* buf)`批量（如每次读取 1024 个）获取只读的 buffer。这个方法与前一种方法的区别在于，当指定区间的数组内存空间是连续的时候，并不复制数据到指定的缓冲区，而是直接返回内存地址，这样提升了读的效率。

```
VectorSP pVec = Util::createVector(DT_INT, 100000000);
int tmp;
const int BUF_SIZE = 1024;
int buf[BUF_SIZE];
int start = 0;
int N = pVec->size();
while (start < N) {
    int len = std::min(N - start, BUF_SIZE);
    const int* p = pVec->getIntConst(start, len, buf);
    for (int i = 0; i < len; ++i) {
        tmp = p[i];
    }
    start += len;
}
```

当数据量比较大时，推荐使用后两种方法，因为第一种方法每次都需要调用虚函数，开销较大，而后两种方法由于 cache 命中率较高、虚函数调用次数少，性能较好。下表为分别采用上述三种方法从 vector 中读取 1 亿个 int 并将其赋值给另一个数所花费的时间：

| 函数 | int getInt(int index) | bool getInt(int start, int len, int\* buf) | const int\* getIntConst(int start, int len, int\* buf) |
| --- | --- | --- | --- |
| 花费时间 | 575.775 ms | 222.789 ms | 121.326 ms |

##### 2.1.1.4. 读取 String 与 Symbol 类型 Vector

String 类型与 Symbol 类型的 Vector 可以通过 `getString(INDEX index)` 访问下标的方式来获取数据，然而每次都会调用虚函数，效率低，要实现高效读取数据与上述其他类型有所区别，所以下面将单独介绍。

###### 2.1.1.4.1. 读取 String 类型 Vector

因为 String 类型的数组在内存中连续存储，所以可以用 `getDataArray` 函数获得数组数据的指针，将其转成 DolphinSring 类型，然后对其进行操作：

```
ConstantSP readString(Heap *heap, vector<ConstantSP> &arguments) {
    if (!(arguments[0]->isVector() && arguments[0]->getType() == DT_STRING)) {
        throw IllegalArgumentException("readString", "argument must be a string vector");
    }
    VectorSP pVec = arguments[0]; //aruments[0] 为需要获取数据的 String 类型的 Vector
    size_t size = pVec->size();
    DolphinString *pDolString = (DolphinString *)pVec->getDataArray(); //获取数据指针
    for (size_t i = 0; i < size; i++) {
        std::cout << pDolString[i].getString() << std::endl; //读取数据
    }
    return new Void();
}
```

###### 2.1.1.4.2. 读取 Symbol 类型 Vector

一个 symbol 类型数据被 DolphinDB 系统内部存储为一个整数，需要通过 SymbolBaseSP 来映射到对应的字符，所以可以先通过上述高效读取 int 类型数组的方法先获取 symbol，然后通过 SymbolBaseSP 得到对应的字符：

```
ConstantSP readSymbol(Heap *heap, vector<ConstantSP> &arguments) {
    if (!(arguments[0]->isVector() && arguments[0]->getType() == DT_SYMBOL)) {
        throw IllegalArgumentException("readSymbol", "argument must be a symbol vector");
    }
    VectorSP pVec = arguments[0]; //aruments[0] 为需要获取数据的 Symbol 类型的 Vector
    int buf[1024];
    int start = 0;
    int N = pVec->size();
    SymbolBaseSP pSymbol = pVec->getSymbolBase(); //获取 SymbolBaseSP
    while (start < N) {
        int len = std::min(N - start, 1024);
        pVec->getInt(start, len, buf);
        for (int i = 0; i < len; ++i)
        {
            std::cout << pSymbol->getSymbol(buf[i]).getString() << std::endl; //读取数据
        }
        start += len;
    }
    return new Void();
}
```

#### 2.1.2. 更新数据

同理，更新一个 Vector 中的数据也不建议直接使用数据的指针进行操作，建议使用下面介绍的方法更新 Vector 中的数据，下面同样以 int 类型为例，其他数据类型有类似的接口：

##### 2.1.2.1. void setInt(int index,int val)

`setInt(int index,int val)`是直接通过下标更新单个数据点：

```
const int size = 100000000;
VectorSP pVec = Util::createVector(DT_INT, size);
for(int i = 0; i < size; ++i) {
    pVec->setInt(i, i);
}
```

##### 2.1.2.2. bool setInt(INDEX start, int len, const int\* buf)

`setInt(INDEX start, int len, const int* buf)`是批量更新 len 长度的连续数据点：

```
const int size = 100000000;
const int BUF_SIZE = 1024;
int tmp[1024];
VectorSP pVec = Util::createVector(DT_INT, size);
int start = 0;
while(start < size) {
    int len =  std::min(size - start, BUF_SIZE);
    for(int i = 0; i < len; ++i) {
        tmp[i] = i;
    }
    pVec->setInt(start, len, tmp);
    start += len;
}
```

##### 2.1.2.3. bool setData(INDEX start, int len, void\* buf)

`setData(INDEX start, int len, void* buf)`也是是批量更新 len 长度的连续数据点，但是不负责检查数据类型：

```
const int size = 100000000;
const int BUF_SIZE = 1024;
int tmp[1024];
VectorSP pVec = Util::createVector(DT_INT, size);
int start = 0;
while(start < size) {
    int len =  std::min(size - start, BUF_SIZE);
    for(int i = 0; i < len; ++i) {
        tmp[i] = i;
    }
    pVec->setData(start, len, tmp);
    start += len;
}
```

##### 2.1.2.4. 使用 int\* getIntBuffer(INDEX start, int len, int\* buf) 获取 buffer 后用 setInt 进行批量更新

先使用 `getIntBuffer` 获取向量中的一段 buffer，修改数据后再用 `setInt` 批量更新：

```
const int size = 100000000;
const int BUF_SIZE = 1024;
int buf[1024];
VectorSP pVec = Util::createVector(DT_INT, size);
int start = 0;
while(start < size) {
    int len =  std::min(size - start, BUF_SIZE);
    int* p = pVec->getIntBuffer(start, len, buf);
    for(int i = 0; i < len; ++i) {
        p[i] = i;
    }
    pVec->setInt(start, len, p);
    start += len;
}
```

上面介绍的四种方法，`setInt(int index,int val)` 更新单个数据会反复调用虚函数，效率最低；而 `setData` 不检查类型，这两种方法都不推荐。建议使用 `setInt(INDEX start, int len, const int* buf)` 批量进行更新，而在 `setInt` 之前使用 `getIntBuffer` 先获取一段 buff，修改数据之后然后再调用 `setInt` 能提高效率。这是因为 `` 方法一般情况下会直接返回内部地址，只有在区间 [start, start + len) 跨越 vector 的内存交界处时，才会将数据拷贝至用户传入的 buffer。而 setInt 方法会判断传入的 buffer 地址是否为内部存储的地址，如果是则直接返回，否则进行内存拷贝。所以先调用 `getIntBuffer` 再调用 setInt 会减少内存拷贝的次数，从而提高效率。下表为分别采取上述四个方法更新 vector 中 1 亿个数据所花费的时间：

| 方法 | void setInt(int index,int val) | bool setInt(INDEX start, int len, const int\* buf) | bool setData(INDEX start, int len, void\* buf) | 使用 getIntBuffer 获取 buffer 后用 setInt 进行批量更新 |
| --- | --- | --- | --- | --- |
| 花费时间 | 445.679 ms | 226.483 ms | 225.877 ms | 126.297 ms |

### 2.2. Table

对于 Table 类型可用 `getColumn` 函数获取某一列的 Vector 指针，然后使用 [Vector 一节](#vector)介绍的方法对得到的整列数据进行处理，实现高效读取：

```
TableSP ddbTbl = input;
for (size_t i = 0; i < columnSize; ++i) {
    ConstantSP col = input->getColumn(i);
// ...
}
```

向 Table 中添加数据，可以使用 `bool append(vector<ConstantSP>& values, INDEX& insertedRows, string& errMsg)` 方法，如果插入成功，返回 true，并向 insertedRows 中写入插入的行数；否则返回 false，并在 errMsg 中写入出错信息，并不会抛出异常，需要用户处理出错的情况。本例中传入两个 Table 对象，将第二个 Table 的数据添加到第一个 Table 中，两个 Table 的列数需要相同，否则会出错：

```
ConstantSP append(Heap *heap, vector<ConstantSP> &arguments) {
    if (!(arguments[0]->isTable() && arguments[1]->isTable())) {
        throw IllegalArgumentException("append", "arguments need two tables");
    }
    TableSP t1 = arguments[0];
    TableSP t2 = arguments[1];
    size_t columnSize = t2->columns();
    std::vector<ConstantSP> dataToAppend;
    for (size_t i = 0; i < columnSize; i++) {
        dataToAppend.emplace_back(t2->getColumn(i));
    }
    INDEX insertedRows;
    std::string errMsg;
    bool success = t1->append(dataToAppend, insertedRows, errMsg);
    if (!success)
        std::cerr << errMsg << std::endl;
    return new Void();
}
```

注意若表是分区表，需要调用 DolphinDB 内置函数 `append!` 来写入数据，示例如下（摘自 DolphinDBPlugin/opcua/src/opc\_ua.cpp 中的 handlerTheAnswerChanged 函数）：

```
if(t->isSegmentedTable()){
    vector<ConstantSP> args = {t, resultTable};
    Heap* h = sub->getHeap();
    h->currentSession()->getFunctionDef("append!")->call(h, args);
}
```

## 3. 插件中创建后台线程

编写插件时，如果需要创建线程，不建议使用 `pthread_create` 等函数直接创建线程，这样创建的线程没有初始化 DolphinDB 中的一些随机数，在执行线程函数时可能会出错。建议使用 `new` 语句创建在头文件 *Concurrent.h* 中声明的 Thread 对象，它需要传入一个 RunnableSP 对象，所以需要用户实现一个 Runnable 对象的派生类，并完成纯虚函数 `void run()` 的实现，用 `void run()` 来执行线程函数，然后将 Runnable 派生类对象的 SmartPointer 传给 Thread。本例中 DemoRun 为 Runnable 的派生类，`void run()` 函数读取一个整型数组的数据并打印，`createThread` 函数创建了一个线程通过 `start()` 函数来执行 DemoRun 的 `run()` 函数，并 `join()` 回收该线程：

```
class DemoRun : public Runnable {
public:
    DemoRun(ConstantSP data) : data_(data) {}
    ~DemoRun() {}
    void run() override {
        size_t size = data_->size();
        for (size_t i = 0; i < size; ++i) {
            std::cout << data_->getInt(i) << std::endl;
        }
    }
private:
    ConstantSP data_;
};

ConstantSP createThread(Heap *heap, vector<ConstantSP> &arguments) {
    if (!(arguments[0]->isVector() && arguments[0]->getType() == DT_INT)) {
        throw IllegalArgumentException("createThread", "argument must be an integral vector");
    }
    SmartPointer<DemoRun> demoRun = new DemoRun(arguments[0]);
    ThreadSP thread = new Thread(demoRun);
    if (!thread->isStarted()) {
        thread->start();
    }
    thread->join();
    return new Void();
}
```

由于 `join()` 函数会阻塞等待子线程的退出，如果子线程需要长时间后台运行，则上述方法不合理。子线程运行时需要保证 ThreadSP 对象仍然存在，因此可以新建一个类，将 ThreadSP 作为其成员，通过 `new` 语句创建这个类，并用其创建子线程并执行线程函数，然后通过返回 `Util::createResource` 创建的对象来管理这个类的资源释放，因此需要实现一个回调函数 `demoOnClose`，当需要回收资源时会自动调用这个回调函数释放资源，用户也可以通过其他函数来手动释放资源：

```
class DemoRun2 : public Runnable {
public:
    DemoRun2(ConstantSP data) : data_(data) {}
    ~DemoRun2() {}
    void run() override {
        size_t size = data_->size();
        for (size_t i = 0; i < size; ++i) {
            std::cout << data_->getInt(i) << std::endl;
            Util::sleep(2000);
        }
    }
private:
    ConstantSP data_;
};

class Demo {
public:
    Demo() {}
    ~Demo() {}
    void createAndRun(ConstantSP data) {
        SmartPointer<DemoRun2> demoRun = new DemoRun2(data);
        thread_ = new Thread(demoRun);
        if (!thread_->isStarted()) {
            thread_->start();
        }
    }
private:
    ThreadSP thread_;
};

static void demoOnClose(Heap* heap, vector<ConstantSP>& args) {
    Demo* pDemo = (Demo*)(args[0]->getLong());
    if(pDemo != nullptr) {
        delete pDemo;
        args[0]->setLong(0);
    }
}

ConstantSP createThread2(Heap *heap, vector<ConstantSP> &arguments) {
    if (!(arguments[0]->isVector() && arguments[0]->getType() == DT_INT)) {
        throw IllegalArgumentException("createThread", "argument must be an integral vector");
    }
    Demo * pDemo = new Demo();
    pDemo->createAndRun(arguments[0]);
    FunctionDefSP onClose(Util::createSystemProcedure("demo onClose()", demoOnClose, 1, 1));
    return Util::createResource(reinterpret_cast<long long>(pDemo), "Demo", onClose, heap->currentSession());
}
```

## 4. 用户权限

在编写插件获取 MQTT、OPC\_UA、Kafka 等中间件的实时数据时，往往需要订阅这些数据，然后将数据写入 Dolphindb 的表中。由于订阅数据函数需要长时间连续运行，所以通常需要用[插件中创建后台线程](#%E6%8F%92%E4%BB%B6%E4%B8%AD%E5%88%9B%E5%BB%BA%E5%90%8E%E5%8F%B0%E7%BA%BF%E7%A8%8B)一节介绍的方法创建新线程来处理订阅消息。当用户订阅流数据表时，需要确保用户具有向保存流数据的表写入数据的权限，所以我们还需要设置用户权限，否则订阅流数据表时会出错。下面介绍如何在插件创建新线程并设置用户权限。

设置用户权限的前提是在创建新线程时创建一个新的会话。会话是一个容器，它具有唯一的 ID 并存储许多已经定义的对象，例如局部变量、共享变量等。创建新会话的方式有多种，如启动命令行窗口、XDB 连接、GUI 连接或 Web URL 连接。会话中的所有变量对于其他会话是不可见的，除非使用语句 share 在会话之间显式共享变量，目前 DolphinDB 仅支持表共享。

创建新线程时，线程函数如果需要用到会话的一些资源（比如调用函数或者访问权限），则需要创建一个新的会话，否则当前会话关闭后（比如在 GUI 里调用，然后关闭 GUI），这些资源自动释放后，如果线程函数仍在执行，会导致程序崩溃。因此在创建新线程时需要创建一个新的会话，即头文件 *CoreConcept.h* 中声明的 Session 对象，然后通过调用其成员函数 `setUser` 来设置权限。而每个 Session 都有一个 Output 类负责输出，而插件中 Output 通常不需要处理输出，所以可以实现一个如下所示的 DummyOutput 作为 Output 的派生类。

本例中 appendTable 为 Runnable 的派生类，在构造函数中用 `heap->currentSession()->copy()` 创建了一个新的会话 session\_，并通过 `setUser` 设置权限，`setOutput` 设置输出，`run` 函数每隔 1s 往内存表添加数据，`stopRun` 函数用于停止线程；Client 负责创建线程并执行线程函数；`subscribe` 为用户接口函数，第一个参数为 table，第二个参数为 table 或回调函数，用户调用 `subscribe` 会每隔 1s 将第一个 table 添加到第二个 table 中（实际订阅第三方数据时，将第一个参数改成订阅的数据），cancelThread 用于停止线程函数：

```
    class DummyOutput: public Output{
    public:
        virtual bool timeElapsed(long long nanoSeconds){return true;}
        virtual bool write(const ConstantSP& obj){return true;}
        virtual bool message(const string& msg){return true;}
        virtual void enableIntermediateMessage(bool enabled) {}
        virtual IO_ERR done(){return OK;}
        virtual IO_ERR done(const string& errMsg){return OK;}
        virtual bool start(){return true;}
        virtual bool start(const string& message){return true;}
        virtual IO_ERR writeReady(){return OK;}
        virtual ~DummyOutput(){}
        virtual OUTPUT_TYPE getOutputType() const {return STDOUT;}
        virtual void close() {}
        virtual void setWindow(INDEX index,INDEX size){};
        virtual IO_ERR flush() {return OK;}
    };

    class Client;
    class appendTable : public Runnable {
    public:
        appendTable(Heap *heap, TableSP table, ConstantSP handle, Client* client)
        : heap_(heap), table_(table), handle_(handle), client_(client) {
            session_ = heap->currentSession()->copy();//创建一个新的会话
            session_->setUser(heap->currentSession()->getUser());//设置权限
            session_->setOutput(new DummyOutput);//设置输出
        }
        ~appendTable() {}
        void run() override {
            while(true) {
                Util::-sleep(1000);
                if(handle_->isTable()) {
                    TableSP result = handle_;
                    std::vector<ConstantSP> dataToAppend = {result, table_};
                    session_->getFunctionDef("append!")->call(session_->getHeap().get(), dataToAppend);
                }
                else{
                    std::vector<ConstantSP> dataToAppend = {table_};
                    ((FunctionDefSP)handle_)->call(session_->getHeap().get(), dataToAppend);
                }
            }
        }
    private:
        Heap* heap_;
        SessionSP session_;
        Client * client_;
        ConstantSP handle_;
        TableSP table_;
    };

    class Client {
    public:
        Client() {}
        ~Client() {}
        void createAndRun(Heap *heap, ConstantSP table, ConstantSP handle) {
            SmartPointer<appendTable> append = new appendTable(heap, table, handle, this);
            thread_ = new Thread(append);
            if (!thread_->isStarted()) {
                thread_->start();
            }
        }
        void cancelThread(){
            thread_->cancel();
        }

    private:
        ThreadSP thread_;
    };

    static void clientOnClose(Heap* heap, vector<ConstantSP>& args) {
        Client* pClient = (Client*)(args[0]->getLong());
        if(pClient != nullptr) {
            delete pClient;
            args[0]->setLong(0);
        }
    }

    ConstantSP subscribe(Heap *heap, vector<ConstantSP> &arguments) {
        if (!arguments[0]->isTable()) {
            throw IllegalArgumentException("subscribe", "First argument must be a table!");
        }
        if (!arguments[1]->isTable() && (arguments[1]->getType() != DT_FUNCTIONDEF)){
            throw IllegalArgumentException("subscribe", "Second argument must be a table or function!");
        }
        Client * pClient = new Client();
        pClient->createAndRun(heap, arguments[0], arguments[1]);
        FunctionDefSP onClose(Util::createSystemProcedure("client onClose()", clientOnClose, 1, 1));
        return Util::createResource(reinterpret_cast<long long>(pClient), "client", onClose, heap->currentSession());
    }

    ConstantSP cancelThread(Heap *heap, vector<ConstantSP> &arguments) {
        if (arguments[0]->getType() != DT_RESOURCE) {
            throw IllegalArgumentException("stopRun", "Argument must be a resource!");
        }
        Client* pClient = (Client*)(arguments[0]->getLong());
        pClient->cancelThread();
        return new Void();
    }
```
