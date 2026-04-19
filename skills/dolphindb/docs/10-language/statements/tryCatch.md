<!-- Auto-mirrored from upstream `documentation-main/progr/statements/tryCatch.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# try-catch

## 语法

```
try

{ ... }

catch(ex)

{ ... }
```

## 详情

首先执行 *try* 语句块。若没有异常发生，跳过 *catch* 语句块，*try* 语句执行结束；否则如果在 *try*
语句块的执行过程中发生了一个异常，错误消息将会存放在变量 *ex* 中，然后再执行 *catch* 语句块。

## 例子

```
1/`7
// output
Arguments for div method can not be string.

try {1/`7} catch(ex){print "oops, please make sure they are all numbers"};
// output
oops, please make sure they are all numbers

ex;
// output
"SYSTEM_Operator" : "Arguments for div method can not be string."
```
