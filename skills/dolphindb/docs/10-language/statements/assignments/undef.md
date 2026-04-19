<!-- Auto-mirrored from upstream `documentation-main/progr/statements/assignments/undef.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 取消变量

通过取消变量或函数定义来释放内存。详情请参考 undef.

```
undef all;

x=1;
undef(`x, VAR);

x=1; y=2;
undef(`x`y, VAR);

share table(1..3 as x, 4..6 as y) as t;
undef(`t, SHARED);

def f(a){return a+1};
undef(`f, DEF);

a=1; b=2;
undef all, VAR;
//取消定义所有变量，但不包括函数定义。
```
