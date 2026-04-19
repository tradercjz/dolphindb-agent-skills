# Functions

## Named function

```dolphindb
def add(x, y) {
    return x + y
}

// single-expression form
def square(x): x * x
```

Defaults:

```dolphindb
def greet(name, salut="Hello") {
    return salut + ", " + name
}
```

Positional and keyword arguments:

```dolphindb
greet("Ada")                     // -> "Hello, Ada"
greet("Ada", salut="Hi")         // -> "Hi, Ada"
```

## Anonymous function

```dolphindb
f = def(x, y) { return x + y }
```

## Lambda

Arrow form for single expressions (most concise):

```dolphindb
f = x -> x * 2
g = (a, b) -> a + b
each(x -> x*x, 1..5)             // [1,4,9,16,25]
```

## Partial application — `f{a, b}`

Binds some arguments, returns a function of the remaining ones. See
`operators.md`.

```dolphindb
inc = add{1, }           // partial on first arg
inc(41)                  // 42

// canonical streaming pattern
subscribeTable(..., handler = myHandler{, aggTable})
```

## Higher-order functions

| Function | Role |
|----------|------|
| `each(f, xs)` | element-wise apply |
| `eachLeft(f, x, ys)` | fix first arg |
| `eachRight(f, xs, y)` | fix last arg |
| `peach(f, xs)` | parallel each |
| `pcall(f, xs)` | parallel call |
| `reduce(f, xs, init)` | fold |
| `accumulate(f, xs, init)` | scan |
| `loop(f, xs)` | like each but returns last |
| `map(f, xs)` | SQL map applied to a vector (not Python map) |

Full list under `../../reference/functions/by-theme/高阶函数.md`.

## Return multiple values

Return a tuple or dict:

```dolphindb
def stats(x) {
    return (mean(x), std(x))
}
(m, s) = stats(1..100)          // tuple destructure
```

## Recursion

Allowed. Stack-based — deep recursion may hit limits; prefer iterative.

## Function references

- `funcByName("mavg")` — look up function by name string.
- `funcDef(f)` — introspect a function.

## OOP (classes)

```dolphindb
class Account {
    var balance = 0.0
    def Account(initial) { self.balance = initial }
    def deposit(x) { self.balance += x }
}

a = Account(100.0)
a.deposit(50.0)
```

See `class_objects.md`, `inheritance.md`,
`member_function.md`.

## Traps

- **Shadowing**: parameter name shadowing a global is allowed and silent.
- **`def f(x)` without body** — legal (returns nothing) but rarely intended.
- **Lambdas can't contain statements** — they are expression-only. Use
  `def` for multi-statement functions.

## See also

- `named_func.md`, `anonym_func.md`, `lambda.md`,
  `partial_app.md`, `func_progr.md`.
