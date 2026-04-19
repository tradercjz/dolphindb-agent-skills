# Control flow

DolphinDB has standard imperative control flow. Prefer **vectorized**
expressions wherever possible — a `for`-loop of a scalar op is 10–1000×
slower than the vector equivalent.

## `if` / `else`

```dolphindb
if(x > 0) {
    doSomething()
} else if(x == 0) {
    doZero()
} else {
    doNeg()
}
```

Inline form: `iif(cond, a, b)` — ternary, returns a or b, both branches are
evaluated (use with care for side effects).

## `for`

```dolphindb
for (i in 0..9) {
    print(i)
}

for (r in t) {          // iterate table rows; r is a dict
    print(r.sym)
}
```

Idiomatic DolphinDB code rarely loops over rows. Use vector ops or
`each(f, xs)` instead.

## `while` / `do..while`

```dolphindb
while(x > 0) { x -= 1 }

do { x -= 1 } while(x > 0)
```

## `break` / `continue`

As in C.

## `try` / `catch`

```dolphindb
try {
    riskyCall()
} catch(ex) {
    print("failed: " + ex)
}
```

`ex` is a string containing the error message + RefId (if any).

## `return`

In a function:

```dolphindb
def f(x) {
    if(x < 0) return int()    // null int
    return x * 2
}
```

An expression at the tail of a function body is an implicit return:

```dolphindb
def f(x): x * 2
```

## `throw`

```dolphindb
if(not isValid(x)) throw "x is required"
```

## Traps

- **`for` over a large vector is slow.** Rewrite with `each`, `map`, or
  plain vector ops: `v * 2` instead of `for(i in size(v)) { v[i] = v[i]*2 }`.
- **`return` inside `try`** still triggers `catch` if an exception was
  raised before the return.
- **No `switch`** — use `if..else if..else` or a lookup dict.

## See also

- `statements/*.md`.
