<!-- Auto-mirrored from upstream `documentation-main/tutorials/unit_testing.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# DolphinDB 单元测试教程

单元测试是对软件中的最小可测试单元（如函数或方法）进行检查和验证。DolphinDB 提供了简单易用的单元测试框架，主要目的是在代码发布之前进行自动化的回归测试，以确保本次改动不会对数据库其他功能造成影响。用户可以通过编写单元测试用例来确保升级前后的数据符合预期。本文将详细介绍在 DolphinDB 中如何编写和执行单元测试。

## 1. 测试用例编写

DolphinDB 的单元测试用例编写需要遵循一定的规则，一个不够严谨的测试用例，可能会导致测试结果有误差。本节将详细介绍测试用例的语法规则，不同对象如何进行断言比较，测试用例中变量的处理，以及如何在测试文件中导入外部变量。通过本节的学习，可以基本掌握 DolphinDB 的单元测试用例编写。

### 1.1 语法规则

一个测试文件通常包含多个测试用例。一个完整的测试用例由测试用例声明和测试主体部分构成。一个正向的测试用例主体包括测试脚本和断言。以下详细介绍测试用例声明和断言的使用语法及应遵循的规则。

```
@testing:case="function_sum"
re = sum(1 NULL 2)
assert 1, eqObj(re,3)
```

#### 1.1.1 测试用例声明

在 DolphinDB 中，使用
`@testing:case="testName"`
标签为脚本声明测试用例。测试用例的命名应与测试内容相关，以便于理解和维护。每个测试用例声明应具有唯一名称。如果存在重复的测试用例名，在执行单元测试时，若断言未通过，将无法确定是哪个测试用例失败。为了便于区分，不同测试用例之间应有空行隔开。以下是两个不同测试用例的声明示例：

```
@testing:case="function_sum_int"
re = sum(1 NULL 2)
assert 1, eqObj(re,3)
@testing:case="function_sum_overflow"
assert 1, sum(int(2147483647..2147483649)) == 0
```

测试用例声明还可以包含可选属性。例如，若测试某种语法错误而预期抛出异常的场景，需要加上
`syntaxError=1`
属性:

```
@testing:case="parse_constant_vector_void_type", syntaxError=1
{,}
```

若测试非语法层面的预期异常场景，例如函数参数输入错误，需要加上
`exception=1`
的属性：

```
@testing:case="sum_not_support_matrix_zero_column", exception=1
m = matrix(`INT, 10, 0);
sum(m)
```

默认情况下，即没有指定任何属性时，表示该测试用例是一个正向的测试用例，预期不会抛出异常。

#### 1.1.2 断言

DolphinDB 测试框架中的断言方法与其他语言提供的断言方法有所不同。例如 Python 语言的 unittest 测试框架，提供了多种不同的断言方法来比较不同的数据类型结果是否符合预期：assertEqual(a, b) 验证 a 和 b 是否相等，assertNotEqual(a, b) 验证 a 和 b 是否不相等，assertTrue(x) 验证 x 是否为 True 等。而在 DolphinDB 中的断言统一使用
`assert`
语句，使用语法如下：

```
assert <expr>
```

或

```
assert <subCase>, <expr>
```

其中
`<subCase>`
是一个字符串，即使未使用引号，也会被解析为字符串；
`expr`
是一个布尔值或返回布尔值的表达式。同一个测试用例中，如果包含多个断言，每个
`<subCase>`
应保持唯一性。否则，在执行单元测试时 ，如果某个测试用例中有断言失败，无法根据测试结果定位到具体是哪个断言失败。

从使用语法中可以看出，无论要判断何种情况下，实际输出结果是否符合预期，只需要确保
`<expr>`
最终返回的结果是布尔值即可。返回 true 表示断言通过；返回 false 表示断言失败，测试用例返回的实际结果与预期不一致：

```
@testing:case="function_sum_int"
re = sum(1 2)
assert 1, eqObj(re,3) //pass
assert 2, eqObj(re,0) //fail
```

注意如果
`<expr>`
返回的结果是布尔向量，则向量内的元素都为 true，才算断言通过：

```
@testing:case="function_cumsum_int"
re = cumsum(1 2 3)
assert 1, eqObj(re,[1,3,6]) //pass
assert 2, eqObj(re,[1,2,6]) //fail
```

在一般测试场景中，
`<expr>`
是一个表达式。在DolphinDB 中，支持表达式的数据类型主要包括：标量、数据对、向量、矩阵和集合。如果需要判断两个表或者字典是否相等，则需要采用绕行的方法。在第1.3节中，将介绍在典型的测试场景下，如何有效的将测试用例返回的各种形式的测试结果和预期结果进行比较。

#### 1.1.3 断言异常类型

其他语言的测试框架中，通常在异常用例处理中可以测试是否抛出了指定异常类型，例如 Python 的 pytest框架使用
`pytest.raises()`
来断言某个函数或方法是否会抛出特定类型的异常:

```
import pytest
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
def test_divide_by_non_zero():
    with pytest.raises(TypeError):
        divide(10, "hello")
```

在第一个测试函数
`test_divide_by_zero`
中，期望
`divide`
函数在除以零时抛出
`ZeroDivisionError`
异常，因此使用
`pytest.raises`
来检查这个异常是否被正确抛出。在第二个测试函数
`test_divide_by_non_zero`
中，期望在
`divide`
函数传入一个非零整数和一个字符串作为除数时会抛出
`TypeError`
异常。同样使用
`pytest.raises`
来检查这个异常是否被抛出。

在 DolphinDB 中，判断非语法层面的异常用例时，只支持
`exception=1`
属性。如果需要进一步判断异常的类型，应使用
`try-catch`
语句捕获异常信息，并通过 assert 断言异常类型和信息是否符合预期。此时，用例声明中不需要添加
`exception=1`
属性，因为该用例的异常已被捕获：

```
@testing:case="sum_not_support_matrix_zero_column"
try{
	m = matrix(`INT, 10, 0);
	sum(m)
}catch(ex){
	assert 1,eqObj(ex[0],"SYSTEM_Runtime")//断言异常类型
	assert 2,eqObj(ex[1],"The column number of matrix must be greater than 0.")//断言异常信息
}
```

### 1.2 比较方法

在编写正向测试用例时，通常需要比较两个对象，并对比较结果进行断言。在 DolphinDB 中，针对不同的比较对象，需根据具体情况选用合适的比较方法，以确保测试结果的可靠性。本节将介绍在 DolphinDB 单元测试中，不同比较方法的使用场景。

#### 1.2.1 eq、eqObj 的使用场景

在比较测试用例返回的实际结果与预期是否一致时，通常存在两种场景。第一种场景要求实际测试结果的类型和值都与预期结果一致；第二种场景则只需确保测试结果的值与预期值一致，不考虑类型。在第一种场景下，我们使用
eqObj
函数进行比较，该函数检查两个对象的类型和值是否相同。仅当类型和值都相同时，此函数才返回 true；如果值相同但类型不同，则函数返回 false:

```
eqObj(1.0,1)
//output:false
```

在测试用例中体现如下：

```
@testing:case="function_sum_double"
re = sum(1.0 2.0)
assert 1,eqObj(re,3.0)
//pass
assert 2,eqObj(re,3)
//fail
```

对与第二种场景，我们使用
`eq(X, Y)`
或
`X==Y`
进行比较，因为对与
`eq(X, Y)`
或
`X==Y`
，当 X 和 Y 的类型不同，但值相同时，返回的结果仍为 true:

```
eq(1.0,1)
//output:true
1.0==1
//output:true
```

在测试用例中体现如下：

```
@testing:case="function_sum_double"
re = sum(1.0 2.0)
assert 1,re==3.0
//pass
assert 2,re==3
//pass
```

如果比较的两个对象是浮点数，并且计算得到的小数位很长，一般只需要保证结果在一定的误差范围内即可，这种情况我们也推荐使用
`eqObj`
函数来比较，因为
`eqObj`
比较时可以指定
`precision`
参数，指定该参数时，该函数返回的结果，等价于
`abs(obj1-obj2)<=pow(10,-precision)`
返回的结果来判断 obj1 和 obj2 的值是否相等。例如：

```
eqObj(1.00115, 1.00135, 4)
//output:false
eqObj(1.00115, 1.00125, 4)
//output:true
```

#### 1.2.2 表对象的比较

如果测试用例中，需要验证一个数据表的结果是否符合预期，无法直接使用 `eq（==）` 或者
`eqObj` 函数，因为这两个比较方法不支持表对象，此时，我们需要通过 values 函数将表格的列转换为一个
tuple，然后使用在高阶函数 each 内使用 `eq（==）` 或 `eqObj`
来逐列对比两个表的值，返回结果是与列数相等的布尔向量，这种比较方法可以直观的看出两个表的哪一列不相同：

```
@testing:case="function_cumsum_table"
re = cumsum(table(1 2 3 as x, 4 5 6 as y))
ex = table(1 2 6 as x,4 9 15 as y)
assert 1,each(eqObj, t1.values(), t2.values())
```

### 1.3 变量的处理

DolphinDB 每执行完一次单元测试后，都会清除测试用例中所有的非共享变量。而共享变量则需要在测试用例中手动去清除，例如共享内存表，共享流表，共享引擎，在 DolphinDB 中使用
`undef`
函数来清除共享变量:

```
t = table(1 2 3 as id, 4 5 6 as value);
share t as st;
undef(`st, SHARED)
```

如果是在集群，可能在其他节点中定义了共享变量，那么需要使用以下命令来获取共享变量。

```
select * from pnodeRun(objs{true}) where shared=true
```

取消各个节点中的共享变量：

```
@testing:case="clear_shared_variable"
shareObjs = select * from pnodeRun(objs{true}) where shared=true
if(shareObjs.size()>0){
	for(i in shareObjs){
		rpc(i[`node], undef, i[`name], SHARED)
	}
}
```

如果是共享持久化的流数据表，需要先
`clearTablePersistence`
，再 undef 变量。也可以直接使用
`dropStreamTable`
清除共享表名并删除该持久化流数据表。

建议在测试用例末尾将所有共享变量清除，避免对其他测试用例造成影响。另外如果测试用例中使用了流订阅，流数据引擎，也建议在用例末尾取消订阅，并删除所有的流数据引擎，因为执行完单元测试后，这些也不会自动清除。

### 1.4 外部变量导入

如果某个目录中包含多个测试文件，这些测试文件使用到了一些相同的的函数定义及变量值，则可以将这些函数定义和变量放在一个单独的 settings.txt 文件中，然后在测试用例文件开头使用
`include`
语句来导入settings.txt 脚本文件，这样该测试文件中就可以直接使用 settings.txt 文件中的变量，例如某个目录中多个测试文件中都需要导入 trade.csv 文件用于测试，则可以将 trade.csv 的路径赋值给
`DATA_DIR`
变量，将该变量放在 settings.txt 文件中：

```
DATA_DIR = "/hdd/DATA_DIR"
```

然后在测试用例文件开头导入 settings.txt 文件，下面的例子中
`setup`
目录和测试文件是在同级目录，这里填的是相对路径，

```
#include "setup/settings.txt"
```

也可以写成绝对路径：

```
#include "/home/test/setup/settings.txt"
```

## 2. 执行单元测试

DolphinDB 提供了多种方式对单个测试文件，或测试目录中的多个测试文件执行单元测试，并返回测试结果到指定文件或终端。包括使用 test 函数对测试脚本执行单元测试，以及通过 GUI 客户端和
VSCode 插件来手动执行单元测试，下面分别介绍这如何使用这三种方法来执行单元测试。

### 2.1 使用 test 函数执行单元测试

test
函数可以对单个脚本文件或测试目录中的所有脚本文件（注：不包括子目录下的脚本文件）执行单元测试，该函数需要登录管理员账户才可以使用，如果没有指定
`outputFile` 参数，测试结果将会打印在控制台，如果指定了
`outputFile` 参数，测试结果将会输出到指定的 `outputFile` 文件中。

例如，使用 test 函数对 test\_function\_sum.txt 单个文件执行单元测试，并且没有指定
`outputFile`:

```
test("/home/xfhang/WORK_DIR/test/test_function_sum.txt")
```

测试结果将会打印在客户端的控制台：

![](image/unit_testing/1.PNG)

图 1. 图 2-1

可以看到控制台打印的信息包含正在执行的测试用例名，测试用例执行时间，以及测试结果部分，测试结果包含失败的用例个数和总的用例数，以及断言失败的用例名和断言编号，图 2-1 中
`#Fail/#Total Testing Cases: 1/3`
，1 表示的是失败的用例个数，3表示的是总的用例数；
`test_function_sum_int_1`
表示的是失败的用例名\_断言编号；

使用 test 函数对 test\_function\_sum.txt 单个文件执行单元测试，并且指定
`outputFile`:

```
test("/home/xfhang/test/test_function_sum.txt","/home/xfhang/output/test_function_sum_output.txt")
```

测试用例结束完成后，测试结果部分将会输出到 /home/xfhang/output/ 目录下的test\_function\_sum\_output.txt 文件中，而正在执行的测试用例仍会打印到控制台中。

使用 test 函数对 test 目录下的所有文件执行单元测试,并且没有指定
`outputFile`：

```
test("/home/xfhang/WORK_DIR/test/")
```

控制台打印的测试结果部分如下：

![](image/unit_testing/2.PNG)

图 2. 图 2-2

图 2-2 中
`#Fail/#Total Testing Cases: 2/6`
，6表示的是 test 目录下的所有测试文件用例数总和, 2表示所有文件失败用例数总和，并将每个测试文件失败的用例打印出来。如果指定了 outputFile，则会将图中的结果输出到指定的文件中。

### 2.2 使用 GUI 客户端执行单元测试

DolphinDB GUI 客户端安装及使用教程见：GUI
客户端，导入测试目录后，右键点击需要执行单元测试的文件名，然后点击 Unit Test 选项，即可对该测试文件执行单元测试，例如图 2-3 中对
test 目录下的 test\_function\_avg.txt 文件执行单元测试，也可以右键点击 test 目录名，此时会对 test
目录下的所有脚本文件(不包括子目录下的脚本文件)执行单元测试，并将结果打印在 Log 栏。

![](image/unit_testing/3.PNG)

图 3. 图 2-3

需要注意的是当 GUI 和 DolphinDB server 不在一个机器上时，可能需要把本地最新编辑的测试脚本文件同步到远程服务器上。为此, GUI 提供了
Synchronize to Server，即文件同步功能。右击需要同步的目录或者文件名，并选择 Synchronize to
server，将其传送到服务器的对应目录。具体操作见 Synchronize
to Server（数据同步）。

### 2.3 使用 VS Code 插件执行单元测试

DolphinDB 的 VS Code 插件可用于编写 DolphinDB 脚本并运行。DolphinDB VSCode 安装及使用教程见：VS Code 插件。在 VSCode
中，右键点击单个文件，再点击 DolphinDB: Unit Test
按钮就可以测试单个文件。右键点击一个目录时，则执行这个目录下所有脚本文件的测试用例。测试结果会打印在 VSCode 终端。

点击单元测试后，VS Code 插件会将该文件或目录上传到 `getHomeDir()/uploads/` 下，并执行
`test` 函数:
`test("getHomeDir()/uploads/filename")`
。如果要更改文件上传目录，可以在 VS Code 插件的配置文件中配置 mappings 属性。本地目录与上传路径的对应关系在 DolphinDB VSCode
安装及使用教程有详细说明。

VS Code 插件不会删除服务器上的文件。在上传文件时，如果服务器上有同名文件，则覆盖同名文件。在上传本地目录时，如果服务器上有同名目录，会覆盖该目录下的同名文件，但如果本地目录不包含文件 a.dos，而服务器上同名目录包含文件 a.dos，上传本地目录时服务器上的 a.dos 也不会被删除。

## 3. 代码管理最佳实践

图 3-1 展示了在 DolphinDB GUI 中导入 ta 模块代码管理目录后的目录结构:

![](image/unit_testing/4.PNG)

图 4. 图 3-1

目录结构如下: 根目录名为
`ta`
，其下有 src 和 test 两个子目录。src 目录包含 ta.dos 模块的源码，该模块封装了一系列函数。test 目录用于测试 ta.dos 中的函数，包含 setup 目录和以 test\_ta\_function\_\*.txt 命名的测试用例文件，
`setup`
目录和测试用例文件位于同一层级。在
`setup`
目录下，
`data`
目录用于存放测试用例所需的数据文件，而
`settings.txt`
文件定义了多个测试用例文件使用的公共变量。本实例中
`settings.txt`
内容为测试用例使中使用到的数据文件路径:

```
DATA_DIR = "/home/xfhang/dolphindbmodules/ta/test/setup/data"
```

每个测试文件开头必须包含以下内容:

```
#include "setup/settings.txt"
use ta
```

即导入 settings.txt 文件并使用 ta 模块，然后编写对应 ta 模块函数的测试用例。在执行测试用例前，需要将 ta.dos 文件上传到 /modules/ 目录下才能使用该模块。可以手动上传该文件，或通过 DolphinDB VSCode 插件右键自动上传到 /modules/ 目录。然后，按照第2节介绍的单元测试执行方式，对整个 test 目录或 目录下的单个测试文件进行单元测试。
