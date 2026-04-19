# geoWithin

## 语法

`geoWithin(X, polygonVertices,
[containBoundary=true])`

## 详情

判断点 *X* 是否在多边形 *polygonVertices* 中。

## 参数

**X** 是一个 POINT 类型的标量或向量，表示一个或多个点。

**polygonVertices** 是一个 POINT 类型向量，表示一个多边形。

**containBoundary** 是一个布尔标量，表示是否包含边界上的点，默认值是true。

## 返回值

布尔标量或向量。

## 例子

```
point1 = point(1,1)
point2 = point(2,3)
point3 = point(2,1)
polygon = [point(0,0),point(0,2),point(2,2),point(2,0)]
geoWithin([point1,point2],polygon)
// output:[true,false,true]
geoWithin([point1,point2,point3],polygon,false)
//output:[true,false,false]
```
