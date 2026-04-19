# return an empty INT VECTOR

x;
// output
[]

typestr x;
// output
FAST INT VECTOR
```

```
x=1..12$3:4;
take(x,2);
```

| col1 | col2 | col3 | col4 |
| --- | --- | --- | --- |
| 1 | 4 | 7 | 10 |
| 2 | 5 | 8 | 11 |

```
take(x,-2);
```

| col1 | col2 | col3 | col4 |
| --- | --- | --- | --- |
| 2 | 5 | 8 | 11 |
| 3 | 6 | 9 | 12 |

```
take(1..3,2 0 2)
// output
[1,1,3,3]
```

```
m=matrix(1 2 3, 4 5 6)
take(m,5)
```

| col1 | col2 |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |
| 1 | 4 |
| 2 | 5 |

```
take(m, 0 2 1)
```

| col1 | col2 |
| --- | --- |
| 2 | 5 |
| 2 | 5 |
| 3 | 6 |

```
t=table(1 2 3 as a, 4 5 6 as b)
take(t,-4)
```

| a | b |
| --- | --- |
| 3 | 6 |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

```
take(t, -2 2 1)
```

| a | b |
| --- | --- |
| 2 | 5 |
| 2 | 5 |
| 3 | 6 |
