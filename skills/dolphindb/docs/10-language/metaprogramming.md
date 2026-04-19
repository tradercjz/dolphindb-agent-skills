# Metaprogramming — building SQL and code at runtime

DolphinDB lets you **construct SQL expressions, function calls, and entire
queries as values**, then evaluate them. This is heavily used by streaming
engines (e.g. `<[ avg(price), sum(volume) ]>` as `metrics`) and by ORM-style
client libraries.

## Metacode literal — `< ... >`

Wrap any expression in angle brackets to get its AST as a value:

```dolphindb
expr = <price * volume>
typestr(expr)                     // METACODE
eval(expr)                        // evaluates in the caller's scope

// vector of metacodes
metrics = <[avg(price), sum(volume) as vol, first(price) as open]>
```

`<[ ... ]>` is a vector of metacode expressions, very common as the
`metrics` argument of stream engines.

## `sqlCol`, `sqlColAlias`

Build column lists dynamically:

```dolphindb
cols = sqlCol(`sym`price, mavg{, 5})    // each column wrapped with mavg(_, 5)
```

## `sql()` — build a full query

```dolphindb
q = sql(
    select  = sqlCol(`sym, avg, "avgPx"),
    from    = t,
    where   = <sym in `AAPL`MSFT>,
    groupBy = sqlCol(`sym)
)
eval(q)
```

This is how ORMs / clients construct parameterized SQL without string
concatenation.

## `makeCall`, `partial`

```dolphindb
call = makeCall(mavg, <price>, 5)
eval(call)                           // equivalent to mavg(price, 5)
```

## `expr`, `exprSchema`, `parseExpr`

```dolphindb
e = parseExpr("x + 1")
eval(e)                          // evaluates against current scope
```

## Macros

`def f() { ... }` with `@` on a parameter defines a macro-argument that
receives its argument **unevaluated** (as metacode):

```dolphindb
def log(@e) { print("eval: " + string(e) + " = " + string(eval(e))) }
log(x * 2)
```

See `macrovariations.md`.

## When to use metaprogramming

- Building queries whose **columns or predicates depend on runtime data**.
- Defining the `metrics` parameter of a streaming engine.
- Implementing ORM layers or dynamic report builders.

Avoid in performance-critical inner loops — `eval` has a small overhead.

## Traps

- **Scope**: `eval(expr)` evaluates in the **caller's** scope, so local
  variables are visible. Changes of scope across module boundaries can be
  surprising — pass data explicitly.
- **Partial application vs metacode**: `mavg{, 5}` is a partially-applied
  function; `<mavg(price, 5)>` is metacode. Engines want metacode for
  `metrics`.

## See also

- `metaProgr_func.md`, `macrovariations.md`.
- `../../reference/functions/by-theme/元编程.md`.
