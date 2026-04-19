# files

## 语法

`files(directory, [pattern])`

## 详情

该函数必须要用户登录后才能执行。

如果没有指定 *pattern*，返回一个包含目录中的文件和子目录信息的表。

如果指定了 *pattern*，返回一个包含文件名中包含了pattern 的文件和子目录的表。

## 参数

**directory** 是表示目录路径的字符串。

**pattern** 是表示在该目录下搜索的文件名的模式的字符串。

## 返回值

一个表，包含如下字段：

* fileName：文件/目录名。
* isDir：是否是目录。
* fileSize：文件大小。
* lastAccessed：最后访问时间。
* lastModified：最后修改时间。

## 例子

```
files("/home/06_DolphinDB/01_App/DolphinDB_Win_V0.2");
```

| filename | isDir | fileSize | lastAccessed | lastModified |
| --- | --- | --- | --- | --- |
| LICENSE\_AND\_AGREEMENT.txt | false | 22558 | 2026.03.24 03:55:19.119 | 2026.03.24 03:55:19.907 |
| README\_WIN.txt | false | 5104 | 2026.03.24 03:51:56.331 | 2026.03.24 03:51:59.091 |
| server | true | 0 | 2026.03.24 06:11:27.922 | 2026.03.24 03:55:19.183 |
| THIRD\_PARTY\_SOFTWARE\_LICENS... | false | 8435 | 2026.03.24 03:48:44.566 | 2025.06.13 02:36:47.453 |

```
files("/home/06_DolphinDB/01_App/DolphinDB_Win_V0.2", "readme%");
```

| filename | isDir | fileSize | lastAccessed | lastModified |
| --- | --- | --- | --- | --- |
| README\_WIN.txt | false | 5104 | 2026.03.24 03:48:41.830 | 2025.12.26 08:29:33.239 |

```
select * from files("/home/06_DolphinDB/01_App/DolphinDB_Win_V0.2") where filename like "README%";
```

| filename | isDir | fileSize | lastAccessed | lastModified |
| --- | --- | --- | --- | --- |
| README\_WIN.txt | false | 5104 | 2026.03.24 03:48:41.830 | 2025.12.26 08:29:33.239 |
