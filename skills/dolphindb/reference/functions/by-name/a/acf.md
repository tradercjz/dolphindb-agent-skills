# acf

## 语法

`acf(X, maxLag)`

## 详情

计算 *X* 的1阶至 *maxLag* 阶的自相关系数。

该函数 与 statsmodels.tsa.stattools.acf
在自相关系数计算方面功能基本一致，具体实现差异如下：

| 维度 | DolphinDB `acf` | Python `statsmodels.tsa.acf` |
| --- | --- | --- |
| lag 参数 | 必须指定 *`maxLag`* | 可选，默认 `min(10 * np.log10(nobs), nobs - 1)` |
| 计算方法 | 去均值+归一化 | 去均值 + 归一化（默认）；支持通过 *adjusted* 参数调整归一化方式 |
| FFT 加速 | 支持（不可修改） | 支持（*fft* 参数） |
| 置信区间 | 不支持 | 支持设置置信区间（*alpha* 参数）和置信区间方法（*bartlett\_confint* 参数） |
| 显著性检验 | 不支持 | 支持（*qstat* 参数） |
| 缺失值处理 | 不支持（报错） | 支持（*missing* 参数） |
| 返回结果 | 1 至 *maxLag* 阶自相关系数向量 | 自相关系数数组 + 可选置信区间 |

## 参数

**X** 是一个向量。

**maxLag** 是一个非负整数，指定计算自相关系数的最大滞后阶数。

## 返回值

长度为 *maxLag* + 1 的向量。

## 例子

```
n=10000
x=array(DOUBLE, n, n, NULL)
x[0]=1
r=rand(0.05, n)-0.025
for(i in 0:(n-1)){
   x[i+1]=-0.8*x[i]+r[i]
}

acf = acf(x, 20)
plot(acf,chartType=BAR)
```

相关函数： autocorr
