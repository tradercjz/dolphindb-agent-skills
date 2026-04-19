<!-- Auto-mirrored from upstream `documentation-main/plugins/signal/signal.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 3. 示例

在运行以下示例前，请先按照前文的“安装插件”步骤，完成 signal 插件的安装和加载。

**例1 dct 离散余弦变换**

```
X = [1,2,3,4]
signal::dct(X)
// output: [5,-2.23044235292127,-2.411540739456585E-7,-0.15851240125353]
```

**例2 dst 离散正弦变换**

```
X = [1,2,3,4]
signal::dst(X)
// output: [15.388417979126893,-6.88190937668141,3.632712081813623,-1.624597646358306]
```

**例3 dwt 离散小波变换**

```
X = [1,2,3]
signal::dwt(X)
// output：
cA                cD
----------------- ------------------
2.121320343559643 -0.707106781186548
4.949747468305834 -0.707106781186548
```

**例4 idwt 反离散小波变换**

```
X = [2.121320343559643,4.949747468305834]
Y = [-0.707106781186548,-0.707106781186548]
signal::dwt(x,y)
// output: [1,2,3.000000000000001,4.000000000000001]
```

**例5 dctParallel 离散余弦变换分布式版本**

```
f1=0..9999
f2=1..10000
t=table(f1,f2)
db = database("dfs://rangedb_data", RANGE, 0 5000 10000)
signaldata = db.createPartitionedTable(t, "signaldata", "f1")
signaldata.append!(t)
signaldata=loadTable(db,"signaldata")
ds=sqlDS(<select * from signaldata >)
signal::dctParallel(ds);
```

**例6 fft 一维快速傅立叶变换**

```
X = [1,2,3,4]
signal::fft(X);
// output: [10+0i,-2+2i,-2+0i,-2-2i]
```

**例7 ifft 一维快速傅立叶逆变换**

```
X = [1,2,3,4]
signal::ifft(X);
// output: [2.5+0i,-0.5-0.5i,-0.5+0i,-0.5+0.5i]
```

**例8 fft2 二维快速傅立叶变换**

```
X = matrix([1,2,3,4],[4,3,2,1])
signal::fft2(X);
// output:
#0    #1
----- -----
20+0i 0+0i
0+0i  -4+4i
0+0i  -4+0i
0+0i  -4-4i
```

**例9 fft2 二维快速傅立叶逆变换**

```
X = matrix([1,2,3,4],[4,3,2,1])
signal::ifft2(X);
// output:
#0     #1
------ ---------
2.5+0i 0+0i
0+0i   -0.5-0.5i
0+0i   -0.5+0i
0+0i   -0.5+0.5i
```

**例10 secc 波形互相关**

```
x=[1, 2, 1, -1, 0, 3];
y=matrix([1,3,2],[4,1,5]);
signal::secc(x,y,4);
// output:
#0                 #1
------------------ -----------------
0.981980506061966  0.692934867183583
0.327326835353989  0.251976315339485
-0.377964473009227 0.327326835353989
0.422577127364258  0.536745040121693
```
