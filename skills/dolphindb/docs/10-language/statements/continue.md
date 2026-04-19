<!-- Auto-mirrored from upstream `documentation-main/progr/statements/continue.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# continue

## 详情

continue语句用于提前结束本次循环。

## 例子

```
def printloop(a,b){
    for(s in a:b){
        if(mod(s,10)==1)
            continue
            print s
    }
}

printloop(10,13);
// output
10
12
// 当s=11时跳过该次循环
```
