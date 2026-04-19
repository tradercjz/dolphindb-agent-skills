# Operators — `=` vs `==`, `!`, `<-`, `{}`

## Assignment vs equality

DolphinDB's rules are **context-dependent**:

| Where | `=` means | `==` means |
|-------|-----------|------------|
| Script statement | assignment | equality |
| `where` clause in SQL | equality | (equivalent to `=`) |
| `group by` / `context by` / expressions inside `select` | equality | equality |
| Inside `if(...)` | equality | equality |

Safe rule: **use `==` for equality in script code**, **use `=` inside SQL
`where` clauses** to match idiomatic DolphinDB style. Either works in SQL;
`==` is allowed.

```dolphindb
// script
x = 42             // assignment
if(x == 42) { ... }

// SQL
select * from t where sym = `AAPL    // idiomatic
select * from t where sym == `AAPL   // also accepted
```

## `<-` (left arrow)

`<-` is used in two specialized contexts:

- **Keyword-argument passing** in some system APIs: `createXxx(a=1, b<-2)`.
  It is functionally equivalent to `=` for kwargs.
- **Sink expression** in a few streaming utilities.

For most user code you will not write `<-`.

## `!` suffix — in-place mutation

Any built-in function ending in `!` mutates its first argument and returns
a status or the new size, not a new object.

```dolphindb
t.append!(newRows)      // appends, mutates t
sort!(v)                // sorts v in place
ffill!(v)               // forward-fill nulls in place
```

Pair the `!` version with the immutable version when available:
- `sort(v)` → returns a new sorted vector.
- `sort!(v)` → sorts v in place.

## `{}` — partial application (function currying)

`f{a, b}` binds the first two args of `f` to `a, b` and returns a new
function.

```dolphindb
add = def(x, y): x + y
inc  = add{1,}        // partial: add with first arg = 1
inc(41)               // 42

// common in subscribe handlers
subscribeTable(..., handler = append!{myEngine}, ...)
```

Positional placeholders work too: `f{, x}` leaves the first arg free and
binds the second.

## Arithmetic / comparison

Standard infix: `+ - * / % ** < <= > >= == !=`. Operate element-wise on
vectors/matrices. There is no `and` / `or` keyword — use `&&` and `||`
(short-circuit) or `and` / `or` words (both accepted).

```dolphindb
(v > 0) && (v < 100)
```

## Bitwise

`& | ^ ~ << >>` — integer bitwise. Not commonly needed in analytics code.

## Membership / ranges

- `a in [1,2,3]` — element-in-vector, returns BOOL.
- `a between 1 : 10` — inclusive range, returns BOOL.
- `a like "AA%"` — SQL-style wildcard string match.

## Element access (`[]`, `@`, `.`)

```dolphindb
v[3]          // index
v[0:3]        // slice
v[v > 0]      // boolean mask
t[`sym]       // column by name
t[2:5]        // row slice
t.sym         // column as attribute

eachAt(add, [1,2,3], [10,20,30])    // same as add @ pair
1 @ [10,20,30]    // returns 20 (index-at)
```

See `operators/eachAt.md` for `@`.

## Higher-order / apply operators

| Op | Name | What |
|----|------|------|
| `each`       | apply | `each(f, xs)` |
| `eachLeft`   | `lf`  | `eachLeft(f, x, ys)` |
| `eachRight`  | `rf`  | `eachRight(f, xs, y)` |
| `loop`       | generic apply | |
| `reduce`     | fold | |
| `accumulate` | scan | |
| `peach`      | parallel each | |

Use these to vectorize Python-style for-loops.

## Traps

- **Forgetting `!`** when you want mutation. `sort(v)` does not change `v`.
- **Operator precedence** mostly matches C, but prefer parentheses — the
  language allows unusual combinations (e.g. `v > 0 and v < 100` works but
  `v > 0 & v < 100` needs `(v>0) & (v<100)`).
- **`=` in a user-defined function body as a default** is unusual:
  `def f(x=1) {}` is allowed and `=` is literal default binding.

## See also

- `operators/*.md` — full operator reference.
