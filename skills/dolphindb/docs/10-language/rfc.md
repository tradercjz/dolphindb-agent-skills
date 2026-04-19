<!-- Auto-mirrored from upstream `documentation-main/progr/rfc.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 远程函数调用

有两种方式可以执行远程调用：

* 远程调用一个内置函数
* 远程运行一个用户定义的本地函数

## 语法

建立一个远程连接：

```
host = xdb(URL, Port)
```

远程调用：

```
host("functionName", functionParameters)
```

或

```
remoteRun(host, "functionName", functionParameters)
remoteRunWithCompression(host, "functionName", functionParameters) // 压缩传输
```

## 远程系统函数调用

```
h=xdb("localhost",80);
h("sum",rand(100, 1000));
// output
50971

remoteRun(h, "sum", rand(100, 1000));
// output
48704

remoteRunWithCompression(h, "sum", rand(100, 1000))
// output
49964
```

## 远程用户定义函数调用

```
def f1(a): sin(rand(100.0,a))
def f2(a,b):return b+f1(a)
pools=each(xdb, "localhost",82)
result = peach(remoteRun{, f2, 100, 0.5}, pools) // result = peach(remoteRunWithCompression{, f2, 100, 0.5}, pools)
result;
```
