# getJobReturn

## 语法

`getJobReturn(jobId, [blocking=false])`

## 详情

取得批处理作业返回的对象。详情请参考 BatchJobManagement。

## 参数

**jobId** 是批处理作业的 ID，是一个字符串。

**blocking** 是一个布尔值，表示是否采用阻塞模式。默认值为 false。如果 *blocking* 为
false，在批处理作业没有完成的情况下，函数会抛出异常。如果 *blocking* 为 true，直到批处理作业完成后，函数才会返回值。

## 返回值

取决于批处理作业自身的返回值。

## 例子

```
def job1(n){
   s = 0
   for (x in 1 : n) {
       s += sum(sin rand(1.0, 100000000)-0.5)
       print("iteration " + x + " " + s)
   }
   return s
}

job1_ID=submitJob("job1_ID","", job1, 100);
getJobReturn(job1_ID);
```

返回：

```
The job [job1_ID20210428] is not complete yet.
```

批处理作业完成后，重新执行`getJobReturn`：

```
getJobReturn(job1_ID);
```

返回：-13318.181243

如需在工作完成后通过 `getJobReturn` 返回结果，可设置 *blocking*
参数为 true。这在批处理作业中非常有用。

```
job1_ID = submitJob("job1_ID","", job1, 100)
getJobReturn(job1_ID, true);
```

返回：25,199.851552887143
