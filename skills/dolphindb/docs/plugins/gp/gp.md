<!-- Auto-mirrored from upstream `documentation-main/plugins/gp/gp.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# GP

DolphinDB 的 gp 插件可以使用 vector 、table 类型的数据进行画图，并绘绘制好的文件保存到本地。gp 插件基于 gnuplot 开发。

## 安装插件

### 版本要求

DolphinDB Server: 2.00.10 及更高版本。目前仅支持 Linux 的 X86-64 位版本。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。
   若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/) 进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins("gp")
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("gp")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("gp")
   ```

## 用户接口

### plot

**语法**

```
plot(data, style, filePath, [option])
```

**详情**

使用 DolphinDB 中的数据进行画图，并以 eps, png 或 jpeg 的文件格式保存到本地。

**参数**

**data** 可以是一个向量、由向量组成的 tuple 或一个表，表示画图数据。若为表，则用其第一列和第二列分别作为 x 轴、y 轴数据。

**style** STRING 类型标量，表示画图的样式。可选值包括："line", "point", "linesoint", "impulses", "dots", "step", "errorbars", "histogram", "boxes", "boxerrorbars", "ellipses", "circles"。

**filePath** STRING 类型标量，表示图片的保存路径。目前支持 eps、png 和 jpeg 格式，需指定以".eps"、".png"、".jpeg" 结尾的字符串。如果字符串不以".png"、".jpeg"结尾，则文件将以 eps 格式输出。

**option** 一个字典，表示画图特性。包含以下键值：

* title: STRING 类型标量或向量，表示每个数据组的标识。
* xRange: 数值型向量，表示图片的 X 轴范围。为数值类型的向量，包含两个元素。
* yRange: 图片的 Y 轴范围。为数值类型的向量，包含两个元素。
* xLabel: STRING 类型标量，表示 X 轴标签。
* yLabel: STRING 类型标量，表示 Y 轴标签。
* size: 图片比例，1 为初始长度。为数值类型的向量，包含两个元素，表示长和宽的比列。
* xTics: 数值型标量，表示 X 轴的单位间隔。
* yTics: 数值型标量，表示 Y 轴的单位间隔。
* resolution: INT 类型的向量，图片像素。在 png 和 jpeg 图像里支持。
* 以下属性可以设置每个独立图像的特性。
* lineColor: STRING 类型标量，表示线条颜色。包含以下值："black", "red", "green", "blue", "cyan", "magenta", "yellow", "navy", "purple", "olive", "orange", "violet", "pink", "white", "gray"。
* lineWidth: 数值型标量或向量，表示线条宽度。
* pointType: 整型标量或向量，表示画点的形状。取值为 0 到 13，对应下图中从左到右的形状。
  ![](images/pointType.png)
  * pointSize: 数值型标量或向量，表示点的大小。
  * smooth: STRING 类型标量或向量，表示数据平滑程度。可以为 "csplines" 或者是 "bezier"。

**例子**

```
data=(rand(20,20),rand(20,20),rand(20,20),rand(20,20),rand(20,20),rand(20,20),rand(20,20),rand(20,20),rand(20,20),rand(20,20),rand(20,20),rand(20,20),rand(20,20),rand(20,20),rand(20,20))
prop=dict(STRING,ANY)
prop[`lineColor]=["black", "red", "green", "blue", "cyan", "magenta", "yellow", "navy", "purple", "olive",  "orange", "violet", "pink", "white", "gray"]
prop["xTics"]=2
prop["yTics"]=5
prop["title"]="l"+string(1..15)
re=plot(data,"line",WORK_DIR+"/test.eps",prop)
re=plot(data,"line",WORK_DIR+"/test.png",prop)
re=plot(data,"line",WORK_DIR+"/test.jpeg",prop)
```
