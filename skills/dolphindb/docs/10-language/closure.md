<!-- Auto-mirrored from upstream `documentation-main/progr/closure.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 闭包

闭包是一个函数对象，它能保存该函数对象的作用域中的值，不论这个函数对象的作用域是否已经失效。

当lambda表达式被定义在另一个函数中时，它将自动得到父函数作用域的访问权。

```
g=def(a){return def(b): a pow b};
g(10)(5);
// output
100000

def mixture(a,b){return def(c): c*(a-b)+(1-c)*(a+b)};
g=mixture(10,5);
g(0.1);
// output
14

def f(a,b){return def(x): a*x+b*(1-x)};
f(5,10)(0.2);
// output
9
```
