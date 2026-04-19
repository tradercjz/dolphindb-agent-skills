<!-- Auto-mirrored from upstream `documentation-main/progr/data_mani/null_scalar.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 空值标量

```
x=1.0+5.6*3+NULL+3;
x==NULL;
// output
1

typestr x;
// output
DOUBLE

x= x + `;
x==NULL;
// output
1

x=1
x==1<NULL;
// output
0

x==1 || NULL;
// output
1

NULL==NULL;
// output
1

!NULL==NULL;
// output
1
```
