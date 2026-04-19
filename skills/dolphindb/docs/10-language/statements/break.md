<!-- Auto-mirrored from upstream `documentation-main/progr/statements/break.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# break

## 详情

break 语句用于跳出一层循环。

## 例子

```
def printloop(a,b){
   for(s in a:b){
       print "outer "+string(s)
       for(t in a:b){
           print "inner "+string(t)
           if (mod(t,10)==1){
                   break
           }
       }
   }
};

printloop(9,15);

// 当t=11时跳出循环内层循环，外层循环继续执行，共执行了6次
```
