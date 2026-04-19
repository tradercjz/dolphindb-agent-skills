<!-- Auto-mirrored from upstream `documentation-main/tutorials/module_development_guide.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 模块开发指南

## 1. 模块基础概念

在使用 DolphinDB
的脚本进行开发时，可以创建可复用模块，以封装自定义函数，比如封装一类业务逻辑（如：因子计算、风控规则、监控告警）。大量函数可以按目录树结构组织在不同模块中，这些模块既可以在系统初始化时预加载，也可以在需要使用时引入。

模块的基本概念和使用方法可以参考模块 。 本教程主要介绍第三方模块开发及上架的要点。

## 2. 模块主体开发过程

### 2.1 环境准备

所有的模块定义默认存放在 [home]/modules 目录下：

* [home] 目录由系统配置参数 *home* 决定，可以通过 `getHomeDir`
  函数查看。
* 节点的模块目录由配置参数 *moduleDir* 来指定，其默认值是相对路径 modules。系统会首先到节点的 home
  目录寻找该目录，如果没有找到，会依次在节点的工作目录与可执行文件所在目录寻找。请注意，单节点模式下，这三个目录默认相同。

开发者开发的模块在部署的时候将会整体放入 modules 目录下。

### 2.2 模块文件准备

发布的模块文件类型分为两种：

* dos文件：明文模块，可以被修改，因此为免费模块。
* dom文件：加密模块，无法被第三方修改，可能为免费或付费模块。具体加密方法会在后续章节中介绍。

从模块架构来看，模块的目录结构有两种：

* 单文件：只包含一个dos/dom文件。以单模块文件ta.dos为例，目录结构即为：

  ```
  [home]/modules/ta.dos
  ```
* 目录架构：可能包含多个dos/dom文件，以及多个嵌套目录。例如
  ta树状模块：

  ```
  [home]/modules/
    |-- ta                                      // 模块名，文件夹
          |-- function1.dos                     // 核心逻辑1
          |-- function2.dos                     // 核心逻辑2
          |-- helper                            // 辅助函数目录
                |-- helperFunction.dos          //辅助函数逻辑3
  ```

  开发者开发模块时，可以根据模块的复杂程度和保密性来选择模块是否加密以及模块的目录架构。

  注：

  开发者在开发过程中，应以 .dos 文件进行开发，.dom
  文件仅在模块发布时进行加密。因此在后续文章中，通用场景均以.dos来指代开发的模块文件。

### 2.3 模块文件内容开发规范

1. 【强制】模块文件第一行只能使用 module
   关键字后接模块名进行声明。模块名推荐用**大驼峰**形式命名，如：FileLog，TaLib。

   ```
   module FileLog::Talib
   ```
2. 【强制】模块声明路径应包含模块路径。例如，现有两个模块 fileUtil 和 dateUtil，它们分别存放于
   modules/fileUtil.dos 与 modules/temporal/dateUtil.dos，那么声明语句分别为
   `module fileUtil` 与 `module
   temporal::dateUtil`。
3. 【强制】**每个**dos/dom文件中，都需要加入函数名为 module\_info
   的函数。每个父模块下的**每个module\_info函数返回值都是完全相同的**。函数 module\_info
   返回一个元数据字典，内容包括：

   1. moduleName：模块父级目录的名字，STRING标量。
   2. moduleVersion：模块自身的版本号，STRING标量；模块必须使用 **语义化版本号（Semantic
      Versioning, SemVer）** 格式进行版本管理，格式为
      `MAJOR.MINOR.PATCH`，例如
      1.0.0；版本号只能递增，如已存在1.1.0版本，则不能发布1.0.x版本。
   3. isFree：模块是否收费，BOOL 标量。若为免费模块，则返回 true。

      例如：

      ```
      def module_info(){
          res = dict(STRING,ANY)
          res["moduleName"] = "LogSearcher"
          res["moduleVersion"] = "1.0.0"
          res["isFree"] = true
          return res
      }
      ```
4. 【建议】在模块声明后，建议加入模块的简要英文介绍，并换行展示。例如：

   ```
   /*
   *  @ brief
   *  This module implements 191 alpha formulas in DolphinDB from GuotaiJunan Securities,
   *  and divides the functions into three categories according to their features.
   *  The development of this module is based on day level data.
   *  @ Author: DolphinDB
   *  @ Last modification time: 2023.01.17
   *  @ DolphinDB server version: 2.00.9
   */
   ```
5. 【建议】对外暴露的函数，定义部分需包含两个内容：1. 英文注释（如有需要）；2. 函数主体。以下为示例：

   ```
   /*
   *  @FunctionName: getTableDiskUsage
   *  @Brief: Get the disk space occupied by the DFS table
   *  @Param: database: the absolute path of the folder where the database is stored
   *  @Param: tableName: the name of dfs table
   *  @Param: byNode=false : a Boolean value, indicating whether the disk usage is displayed by node
   *  @Return: a table containing the disk space occupied by the DFS table
   *  @SampleUsage: getTableDiskUsage("dfs://demodb", "machines", true)
   */
   def getTableDiskUsage(database, tableName, byNode=false){
       if(byNode == true){
           return select sum(diskUsage\1024\1024\1024) diskGB
                       from pnodeRun(getTabletsMeta{"/"+substr(database, 6)+"/%", tableName, true, -1})
                       group by node
       }else {
           return select sum(diskUsage\1024\1024\1024) diskGB
                       from pnodeRun(getTabletsMeta{"/"+substr(database, 6)+"/%", tableName, true, -1})
       }
   }
   ```

   注：

   注释的要点：

   * 需用英文
   * 每个要点以”@“开头，以“:” 冒号分隔关键字和内容。格式保持一致，修改内部内容即可。
   * FunctionName 部分请仅写函数名。
   * Brief 部分请简要概括函数的作用。
   * Param 部分请详细说明每个参数的作用。如果有多个参数，每个参数独立一行，说明其作用和默认值（如有），例如 如
     `@Param: byNode=false : a Boolean
     ...`
   * Return 部分请说明函数的返回值类型和含义。如果函数没有返回值，则应注明“无返回值”。
   * SampleUsage 部分请简单举例如何使用这个函数。

## 3. 模块发布规范

### 3.1 模块加密

开发者如上传的是.dos文件，即明文模块，可以被修改，因此默认是免费模块。但是如开发者想对其上传的模块加密，则应在上传前加密其模块内容。加密方式为调用
`encryptModule` 函数：

`encryptModule(name, [moduleDir], [overwrite=false])`：

* name 用于指定对应的dos文件名字，即每一个模块第一行声明的目录，比如 ta::func。
* moduleDir 用于指定该dos文件所在的目录，默认为 DolphinDB 启动时设置的模块目录。该目录也是输出目录。
* overwrite 如果为 true，即使目标目录下已存在相应的 .dom 文件，也会进行覆盖；若为 false，则不覆盖。

```
encryptModule("mod1", "/home/yxyang/dolphindb/src/modules", true)
```

该函数适用于单个 .dos 文件。如果上传的是多个文件或树状模块，开发者需要对每个文件进行加密操作。

注：

建议加密函数在200版本的server上使用，以确保模块在200和300版本的server上都能使用。

### 3.2 模块打包

无论是上传单一文件的模块还是含有嵌套目录的模块，在上传的时候必须都使用zip压缩打包。
