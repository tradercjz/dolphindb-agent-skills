<!-- Auto-mirrored from upstream `documentation-main/tutorials/interface_development.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# coding: utf-8

def query(session, startDate, endDate, cols='"*"', security='NULL'):
    script = 'query({}, {}, {}, {})'.format(startDate, endDate, cols, security)
    return session.run(script)

def queryRecentYear(session, startDate='NULL', endDate='NULL', cols='"*"', security='NULL'):
    script = 'queryRecentYear({}, {}, {}, {})'.format(startDate, endDate, cols, security)
    return session.run(script)

def queryFirst10Col(session, startDate, endDate, cols='NULL', security='NULL'):
    script = 'queryFirst10Col({}, {}, {}, {})'.format(startDate, endDate, cols, security)
    return session.run(script)

def queryCond(session, startDate, endDate, cols='NULL', security='NULL'):
    script = 'queryCond({}, {}, {}, {})'.format(startDate, endDate, cols, security)
    return session.run(script)
```

接下来，给出一些结合 Python 客户端二次封装后的取数接口的示例。

* 在 Python API 中创建 session，登录用户 testUser2 的账号

  ```
  import pandas as pd
  import dolphindb as ddb
  import query

  # 建立会话并登陆账号
  s = ddb.session("192.198.1.38", 8200, 'testUser2', '123456')
  ```
* 使用全表访问接口访问数据

  ```
  # 访问全表数据
  df = query.query(session=s, startDate='2015.01.01', endDate='2024.12.31')

  # 访问2024年2月指定证券、指定列的数据
  df = query.query(session=s, startDate='2024.02.01', endDate='2024.02.29', security='`000001', cols='`SecurityID`date`time`col1`col2`col3`col4`col5`col6`col7`col8`col9`col10')
  ```
* 使用行级别访问接口访问数据

  ```
  # 访问近1年所有数据
  df = query.queryRecentYear(session=s)

  # 访问指定日期开始、指定列的数据
  df = query.queryRecentYear(session=s, startDate='2024.07.01', cols='`SecurityID`date`time`col2`col3')
  ```
* 使用列级别访问接口访问数据

  ```
  # 访问2023年指定证券、允许访问的所有列的数据
  df = query.queryFirst10Col(session=s, startDate='2023.01.01', endDate='2023.12.31', security='`000008`000009`000010')

  # 访问2022年12月指定列的数据
  df = query.queryFirst10Col(session=s, startDate='2022.12.01', endDate='2022.12.31', cols='`SecurityID`date`time`col4`col5`col6')
  ```
* 使用行列级别访问接口访问数据

  ```
  # 访问2021年1月允许访问的所有列的数据
  df = query.queryCond(session=s, startDate='2021.01.01', endDate='2021.01.31')

  # 访问2021年指定列的数据
  df = query.queryCond(session=s, startDate='2021.01.01', endDate='2021.12.31', cols='`SecurityID`date`time`col47`col48`col49')
  ```

### 4.4 其它 API 取数接口示例

为了方便读者快速扩展该取数接口的设计方法，本教程提供了以下几种常用 API 语言的示例代码，通过 run(funcName, args...) 的规范 rpc 接口来调用，大家可以根据标准接口进行二次封装，对外提供更加便捷的数据访问接口。

* C++ 示例

  ```
  # 建立会话并登陆账号
  DBConnection conn;
  conn.connect("192.198.1.38", 8200, "testUser2", "123456");

  # 访问全表数据
  ConstantSP startDate = Util::createDate(2015, 1, 1);
  ConstantSP endDate = Util::createDate(2024, 12, 31);
  ConstantSP cols = Util::createString("*");
  vector<ConstantSP> funcArgs = {startDate, endDate, cols};
  auto tb = conn.run("query", funcArgs);
  ```
* Java 示例

  ```
  // 建立会话并登陆账号
  DBConnection conn= new DBConnection();
  conn.connect("192.198.1.38", 8200, "testUser2", "123456");

  // 访问全表数据
  BasicDate startDate = new BasicDate(LocalDate.of(2015,1,1));
  BasicDate endDate = new BasicDate(LocalDate.of(2024,12,31));
  BasicString cols = new BasicString("*");
  List<Entity> funcArgs = Arrays.asList(startDate, endDate, cols);
  BasicTable tb = (BasicTable)conn.run("query", funcArgs);
  ```
* C# 示例

  ```
  // 建立会话并登陆账号
  DBConnection conn = new DBConnection();
  conn.connect("192.198.1.38", 8200, "testUser2", "123456");

  // 访问全表数据
  BasicDate startDate = new BasicDate(new DateTime(2015, 1, 1));
  BasicDate endDate = new BasicDate(new DateTime(2024, 12, 31));
  BasicString cols = new BasicString("*");
  List<IEntity> funcArgs = new List<IEntity> { startDate, endDate, cols };
  BasicTable tb = (BasicTable)conn.run("query", funcArgs);
  ```
* JavaScript 示例

  ```
  // 建立会话并登陆账号
  let ddb = new DDB('ws://192.198.1.38:8200', { username: 'testUser2', password: '123456' })
  await ddb.connect()

  // 访问全表数据
  const start = '2015.01.01'
  const end = '2024.12.31'
  const tb = await ddb.execute(`query(${start}, ${end}, "*")`)
  ```

## 5. 总结

本教程适用于基于 DolphinDB 搭建数据中台，如何设计对外取数接口的场景。主要解决了数据访问权限和客户端取数接口封装的问题。

本教程主要提供了 Python 客户端二次封装取数接口的方法，该方法也适用于 C++、Java 和 C# 等 DolphinDB 支持的 API。

## 6. 常见问题解答（FAQ）

本章将针对教程使用过程中经常遇到的报错及相关问题做出解答，并提供对应的解决方案。

### 6.1 Not granted to read [xxx]

调用函数视图访问数据时报如下错误：

```
t = queryRecentYear(2023.06.01) => queryRecentYear: throw "Not granted to read data before " + start => Not granted to read data before 2023.06.28
t = queryFirst10Col(2023.01.01, 2023.12.31, ["SecurityID","date","time","col40","col50"]) => queryFirst10Col: throw "Not granted to read columns " + toStdJson(distinct(cols[notGranted])) => Not granted to read columns ["col50","col40"]
```

造成问题原因：

* 没有权限访问相关的行或列

解决方案：

* 修改相关参数，在权限内访问数据

```
t = queryRecentYear(startDate=2023.07.01)
t = queryFirst10Col(startDate=2023.01.01, endDate=2023.12.31, cols=`SecurityID`date`time`col5`col6`col7)
```

## 7. 附录

* DolphinDB 示例代码：[数据接口开发.dos](script/ID/dit.dos)
* Python 示例代码：[4.2 原生 Python API 取数接口示例.py](script/ID/4.2.py) [query.py](script/ID/query.py) [4.3 二次封装的 Python API 取数接口示例.py](script/ID/4.3.py)
* C++ 示例代码：[main.cpp](script/ID/main.cpp)
* Java 示例代码：[Main.java](script/ID/Main.java)
* C# 示例代码：[Program.cs](script/ID/Program.cs)
* JavaScript 示例代码：example.html
