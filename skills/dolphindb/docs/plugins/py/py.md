<!-- Auto-mirrored from upstream `documentation-main/plugins/py/py.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# Py（3.6/3.7版本）

利用 python C-API 协议，实现在 DolphinDB 内调用 Python 环境中的第三方库。本插件使用了 [pybind11](https://github.com/pybind/pybind11) 库。

目前，DolphinDB 提供支持 Python 3.6 的插件 py 和 py36，以及支持 Python 3.7 的插件 py37。用户可根据 Python 版本选择相应插件。

## 安装插件

### 版本要求

| 插件 | DolphinDB 版本 | Pyhton 版本 | 系统或架构 |
| --- | --- | --- | --- |
| py | 2.00.10 or higher | Python3.6 | Linux x64 and Linux JIT |
| py36 | 2.00.14 or higher | Python3.6 | Linux x64 and Linux JIT |
| py37 | 2.00.14 or higher | Python3.7 | Linux x64 and Linux JIT |

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   * Python 3.6 环境可选择安装 py 或 py36 插件。

   ```
   installPlugin("py")
   // 或者 installPlugin("py36")
   ```

   * Python 3.7 环境可以选择安装 py37 插件。

   ```
   installPlugin("py37")
   ```
3. 修改配置参数，添加 globalDynamicLib 参数。如果是单节点模式，则在 dolphindb.cfg 中配置该参数；如果是集群模式，则在 cluster.cfg 中配置该参数。

   **注：** 可使用 `find /path_to_python -name "libpython*"` 查找 libpythonxxx 路径，并将其填写到 globalDynamicLib 参数中。"/path\_to\_python" 应根据 Python 安装方式设置：若为系统安装，可填写 /usr；若为 Conda 安装，则填写 Conda 的安装目录。

   * Python 3.6 的配置如下：

   ```
   globalDynamicLib=/path_to_libpython3.6m.so/libpython3.6m.so
   ```

   * Python 3.7 的配置如下：

   ```
   globalDynamicLib=/path_to_libpython3.7m.so/libpython3.7m.so
   ```
4. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("py")
   // 或 loadPlugin("py36")
   // 或 loadPlugin("py37")
   ```

**注意：**

* 由于数据类型转换时会用到 numpy 和 pandas 中的数据类型，因此 Python 环境中需要安装 numpy 和 pandas 模块。如果不安装 numpy 和 pandas 模块，加载时将会导致系统崩溃（常见出错信息如下）。

  ```
   terminate called after throwing an instance of 'pybind11::error_already_set'
     what():  ModuleNotFoundError: No module named 'numpy'
  ```
* 当使用 Anaconda 时，由于其包含的 libstdc++.so.6 动态库版本较新，可能与 DolphinDB 使用的旧版本不兼容。为避免版本冲突，建议按以下步骤操作：

  + 使用 pip uninstall pandas 命令卸载当前版本的 pandas。
  + 使用 pip install pandas 命令重新安装 pandas。
  + 对于其他需要链接到 libstdc++.so.6 的模块，也应该使用 pip uninstall 和 pip install 来重新安装。
  + 避免使用 conda install 命令安装 pandas，因为这可能会链接到较新版本的 libstdc++.so.6，导致插件加载失败。另外，还可以尝试以下方法，无需重新安装模块：将 Anaconda 的 lib 目录下的 libstdc++.so.6 文件复制到 DolphinDB 的相应目录下（为了防止意外，请先备份原有的 libstdc++.so.6 文件）。

## 接口说明

### toPy

**语法**

```
py::toPy(obj)
```

**详情**

将 DolphinDB 对象转换为 Python 对象。目前支持转换的数据类型见 DolphinDB 对象转成 Python 对象。

**参数**

**obj** 需要转换的 DolphinDB 对象。

**例子**

```
 x = 1 2 3 4;
 pyArray = py::toPy(x);

 y = 2 3 4 5;
 d = dict(x, y);
 pyDict = py::toPy(d);
```

### fromPy

**语法**

```
py::fromPy(obj, [includeIndex=false])
```

**详情**

将 Python 对象转换为 DolphinDB 对象，目前支持的数据类型见 Python 对象转成 DolphinDB 对象。pandas.DataFrame 转换成 table 保留 index 的例子见 Dataframe 转换成 table 保留 index。

**参数**

**obj** 需要转换的 Python 对象。

**includeIndex** 布尔值，表示是否将 pandas.DataFrame 的 index 作为转换后的 table 的第一列。默认值为 false，表示舍弃 pandas.DataFrame 的 index 列。仅当 *obj* 为 pandas.DataFrame 时才需设置该参数。

**例子**

```
 x = 1 2 3 4;
 l = py::toPy(x);
 re = py::fromPy(l);
 re;
```

### importModule

**语法**

```
py::importModule(moduleName)
```

**详情**

导入 Python 模块（子模块），需要确保环境中已安装对应模块。可用 pip3 list 查看安装情况，若未安装则需通过 pip3 install 命令进行安装。

注：如果需要导入自定义的模块，则需要将该模块文件拷贝到 sys.path 打印的 lib 路径下或者 dolphindb 所在的目录下。

**参数**

**moduleName** STRING 类型标量，表示需要导入的模块名称。

**例子**

```
np = py::importModule("numpy"); //导入 numpy

linear_model = py::importModule("sklearn.linear_model"); //导入 sklearn 子模块 linear_model
```

### cmd

**语法**

```
py::cmd(script)
```

**详情**

运行 Python 脚本。

**参数**

**script** STRING 类型标量，要运行的 Python 脚本。

**例子**

```
 sklearn = py::importModule("sklearn"); //导入 sklearn
 py::cmd("from sklearn import linear_model"); //从 sklearn 导入 linear_model 模块
```

### getObj

**语法**

```
py::getObj(module, objName)
```

**详情**

获取模块（或对象）的子模块（或属性）。获取子模块时要确保子模块已经导入，若没有导入，可用 `py::cmd` 执行 `from ... import ...` 语句导入。

**参数**

**module** 预先导入的模块，如 `py::importModule` 的返回值。

**objName** STRING 类型标量，表示目标对象名称。

**例子**

```
np = py::importModule("numpy"); //导入 numpy
random = py::getObj(np, "random"); //获取 numpy 子模块 random

sklearn = py::importModule("sklearn"); //导入 sklearn
py::cmd("from sklearn import linear_model"); //导入sklearn子 模块
linear_model = py::getObj(sklearn, "linear_model");  //获取 sklearn 子模块 linear_model
```

注：导入 numpy 时会自动导入 random 子模块，所以无需运行 py::cmd("from numpy import random") 便可通过 `py::getObject` 获取子模块；而导入 sklearn 时不会自动导入子模块，所以需要通过 `py::cmd("from sklearn import linear_model")` 导入子模块后才能执行 `py::getObject` 获取子模块。若只使用子模块功能可通过 linear\_model=py::importModule("sklearn.linear\_model") 获取子模块，这种方式更加方便。

### getFunc

**语法**

```
py::getFunc(module, funcName, [convert=true])
```

**详情**

获取 Python 模块内的静态方法。返回 *funcName* 函数对象，该函数对象可直接接受 DolphinDB 的数据类型作为入参，无需预先转换。目前函数不支持关键字参数，若设置 *convert*=true，则在能够转换的情况下，调用函数对象的返回结果是 DolphinDB 对象，否则返回结果是 Python 对象；若设置 *convert*=false，则调用函数对象的返回结果是 Python 对象。

**参数**

**module** 预先导入的模块，如 `py::importModule` 和 `py::getObj` 的返回值。

**funcName** STRING 类型标量，需要获取的函数名称。

**convert** 布尔值，表示在调用该函数后结果是否自动转换成 DolphinDB 对应的数据类型，默认为 true。

**例子**

```
np = py::importModule("numpy"); //导入 numpy
eye = py::getFunc(np, "eye"); //获取 numpy 中的 eye 函数

np = py::importModule("numpy"); //导入 numpy
random = py::getObj(np, "random"); //获取 numpy 子模块 random
randint = py::getFunc(random, "randint"); //获取 random 中的 randint 函数
```

### getInstanceFromObj

**语法**

```
py::getInstanceFromObj(obj, [args])
```

**详情**

通过预先获得的 Python 类对象获取 Python 类实例对象。返回的对象支持以 " `.` " 方式访问类属性与类方法。在能够进行数据类型转换时返回 DolphinDB 数据类型，否则返回 Python 对象。

**参数**

**obj** 预先获得的 Python 类对象，如 `py::getObj` 的返回值。

**args** 要传给实例对象的参数，若没有则不填。

**例子**

```
 sklearn = py::importModule("sklearn");
 py::cmd("from sklearn import linear_model");
 linearR = py::getObj(sklearn,"linear_model.LinearRegression")
 linearInst = py::getInstanceFromObj(linearR);
```

### getInstance

**语法**

```
py::getInstance(module, objName, [args])
```

**详情**

直接从模块中获取 Python 类实例对象。返回的对象支持以 " `.` " 方式访问类属性与类方法。在能够进行数据类型转换时返回 DolphinDB 对象，否则返回 Python 对象。

注意：`py::getFunc` 获取的是模块中的静态方法。如果要调用实例方法，需要用 `py::getInstanceFromObj` 或 `py::getInstance` 获取类实例对象，然后通过 " `.` " 的方式访问类方法。

**参数**

**module** 预先导入的模块，如 `py::importModule` 的返回值。

**objName** STRING 类型标量，目标对象名称。

**args** 要传给实例对象的参数，若没有则不填。

**例子**

```
linear_model = py::importModule("sklearn.linear_model"); //导入 sklearn 子模块 linear_model
linearInst = py::getInstance(linear_model,"LinearRegression")
```

### reloadModule

```
py::reloadModule(module)
```

**详情**

如果修改了之前导入的模块，重新执行 `importModule` 并不能导入修改后的模块，需要调用 `reloadModule` 重新导入该模块才能获取到修改后的模块。

**参数**

**module** 预先导入的模块，如 `py::importModule` 的返回值。

**例子**

```
model = py::importModule("fibo"); //fibo 为上文中自定义的模块

model = py::reloadModule(model);  //如果修改了 fibo.py，则需要调用 reloadModule 重新导入该模块才能获取到修改后的模块
```

## 实例

### 加载插件并初始化

```
loadPlugin("py");
use py;
```

### 数据结构互转

```
x = 1 2 3 4;
y = 2 3 4 5;
d = dict(x, y);
pyDict = py::toPy(d);
Dict = py::fromPy(pyDict);
Dict;
```

### 调用系统库打印 Python 默认路径

```
sys = py::importModule("sys");
path = py::getObj(sys, "path");
dpath = py::fromPy(path);
dpath;
```

### 导入 numpy 并执行静态方法

```
np = py::importModule("numpy"); //导入 numpy
eye = py::getFunc(np, "eye"); //获取 numpy 中的 eye 函数
re = eye(3); //执行 eye 函数生成对角矩阵
re;

random = py::getObj(np, "random"); //获取 numpy 子模块 random
randint = py::getFunc(random, "randint"); //获取 random 中的 randint 函数
re = randint(0,1000,[2,3]); //执行 randint 函数
re;
```

### 导入 sklearn 并执行实例方法

```
//方法一
linear_model = py::importModule("sklearn.linear_model"); //导入 sklearn 子模块 linear_model
linearInst = py::getInstance(linear_model,"LinearRegression")
//方法二
sklearn = py::importModule("sklearn"); //导入 sklearn
py::cmd("from sklearn import linear_model"); //从 sklearn 导入 linear_model 模块
linearR = py::getObj(sklearn,"linear_model.LinearRegression")
linearInst = py::getInstanceFromObj(linearR);

X = [[0,0],[1,1],[2,2]];
Y = [0,1,2];
linearInst.fit(X, Y); //调用 fit 函数
linearInst.coef_; // output: [0.5,0.5]
linearInst.intercept_; // output: 1.110223E-16 ~ 0
Test = [[3,4],[5,6],[7,8]];
re = linearInst.predict(Test); //调用 predict 函数
re; //output: [3.5, 5.5, 7.5]

datasets = py::importModule("sklearn.datasets");
load_iris = py::getFunc(datasets, "load_iris"); //获取静态函数 load_iris
iris = load_iris(); //调用静态函数 load_iris

datasets = py::importModule("sklearn.datasets");
decomposition = py::importModule("sklearn.decomposition");
PCA = py::getInstance(decomposition, "PCA");
py_pca=PCA.fit_transform(iris['data'].row(0:3)); //取 iris['data'] 前三行数据进行训练
py_pca.row(0);  //output:[0.334781147691283, -0.011991887788418, 2.926917846106032e-17]
```

**注意**：DolphinDB 中若要从矩阵中取行数据要用 `row` 函数，如上例中的 iris['data'].row(0:3) 为取前三行数据。iris['data'][0:3] 为取前三列数据。

### 导入自定义模块并调用其中的静态方法

本例中我们自己实现了一个如下所示的 Python 模块，里面有两个静态方法，fib(n) 打印从 0 到 n 的 Fibonacci 数列，fib2(n) 返回从 0 到 n 的 Fibonacci 数列。我们将该模块保存为 fibo.py，并将其拷贝到 dolphindb 所在的目录下（或者拷贝到 sys.path 打印的 lib 路径下）：

```
def fib(n):    # write Fibonacci series up to n
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()

def fib2(n):   # return Fibonacci series up to n
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a+b
    return result
```

之后我们便能加载插件，在 dolphindb 中导入该模块进行使用：

```
loadPlugin("py"); //加载插件

fibo = py::importModule("fibo");  //导入该模块
fib = py::getFunc(fibo,"fib");  //获取模块中的 fib 函数
fib(10);  //调用 fib 函数，打印出 0 1 1 2 3 5 8
fib2 = py::getFunc(fibo,"fib2"); //获取模块中的 fib2 函数
re = fib2(10);  //调用 fib2 函数
re;   //output: 0 1 1 2 3 5 8
```

### DataFrame 转换成 table 并保留index

在调用某些 Python 函数时，如果返回 DataFrame，若要保留 index 作为转换后 table 的第一列，需要在调用 `getFunc` 时指定 *convert*=false，然后调用 `fromPy` 函数且设置 *includeIndex*=true,将结果转换成 table。

首先实现一个函数返回一个 pandas.DataFrame，将其保存成 demo.py；然后将其拷贝到 dolphindb 所在的目录下（或者拷贝到 sys.path 打印的 lib 路径下）：

```
import pandas as pd
import numpy as np
def createDF():
    index=pd.Index(['a','b','c'])
    df=pd.DataFrame(np.random.randint(1,10,(3,3)),index=index)
    return df
```

之后加载插件，导入模块加载函数并调用，这样返回结果中的第一列便为 dataframe 的 index：

```
loadPlugin("/path/to/plugin/PluginPy.txt"); //加载插件

model = py::importModule("demo");
func1 = py::getFunc(model, "createDF", false)
tem = func1()
re =  py::fromPy(tem, true)
```

## 支持的数据类型

### DolphinDB 对象转成 Python 对象

| DolphinDB 数据类型 | Python 数据类型 |
| --- | --- |
| BOOL | bool |
| CHAR | int64 |
| SHORT | int64 |
| INT | int64 |
| LONG | int64 |
| DOUBLE | float64 |
| FLOAT | float64 |
| STRING | String |
| DATE | datetime64[D] |
| MONTH | datetime64[M] |
| TIME | datetime64[ms] |
| MINUTE | datetime64[m] |
| SECOND | datetime64[s] |
| DATETIME | datetime64[s] |
| TIMESTAMP | datetime64[ms] |
| NANOTIME | datetime64[ns] |
| NANOTIMESTAMP | datetime64[ns] |
| DATEHOUR | datetime64[s] |
| vector | NumPy.array |
| matrix | NumPy.array |
| set | Set |
| dictionary | Dictionary |
| table | pandas.DataFrame |

* DolphinDB CHAR 类型会被转换成 Python int64 类型。
* 向量和矩阵都会转成 numpy.array，时间类型都会转成 Python pandas 中的时间类型，所以 Python 环境中需要安装 numpy 和 pandas 模块。
* 由于 Python pandas 中所有有关时间的数据类型均为 datetime64[ns]，DolphinDB 中 table 的所有时间类型数据均会被转换为 datetime64[ns] 类型。MONTH 类型，如 2012.06M，会被转换为 2012-06-01（即月份当月的第一天）。由于 pandas 时间戳范围限制，MONTH 范围要在 1970.01M-2262.04M 之间，DATE 和 DATETIME 日期范围要在 1677.09.22-2062.04.11 之间。TIME, MINUTE, SECOND 与 NANOTIME 类型不包含日期信息，转换时会自动添加 1970-01-01，例如 13:30m 会被转换为 1970-01-01 13:30:00。
* DolphinDB 中的逻辑型、数值型和时序类型的 NULL 值默认情况下会转换成 NaN 或 NaT；字符串的 NULL 值为空字符串。如果向量中包含 NULL 值，数据类型可能会发生改变，比如 BOOL 类型的向量中如果包含 NULL 值，NULL 会转换成 NaN，因此数据类型变成 float64；BOOL 类型中的 True 会变成 1，False 会变成 0。

### Python 对象转成 DolphinDB 对象

| Python 数据类型 | DolphinDB 数据类型 |
| --- | --- |
| bool | BOOL |
| int8 | CHAR |
| int16 | SHORT |
| int32 | INT |
| int64 | LONG |
| float32 | FLOAT |
| float64 | DOUBLE |
| String | STRING |
| datetime64[M] | MONTH |
| datetime64[D] | DATE |
| datetime64[m] | MINUTE |
| datetime64[s] | DATETIME |
| datetime64[h] | DATEHOUR |
| datetime64[ms] | TIMESTAMP |
| datetime64[us] | NANOTIMESTAMP |
| datetime64[ns] | NANOTIMESTAMP |
| Tuple | vector |
| List | vector |
| Dictionary | dictionary |
| Set | set |
| NumPy.array | vector(1维) / matrix(2维) |
| pandas.DataFrame | table |

* numpy.array 会根据维度转换成向量（1维）或者矩阵（2维）。
* pandas.DataFrame 中的时间数据类型都是 datetime64[ns]，所以在转换成 table 时，时间类型都会转换成 NANOTIMESTAMP 类型。
* 从 pandas.DataFrame 转换成 table 时，如果列名不符合 DolphinDB 要求的列名规范，则会根据以下规则自动调整列名：

  + 若数据中列名存在中文或英文字母、数字或下划线之外的字符，将其转换为下划线。
  + 若数据中列名第一个字符不是中文或英文字母，添加 ”c” 作为该列名首字符。
