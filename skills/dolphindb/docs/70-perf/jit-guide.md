# JIT — `@jit` compilation guide

## Contents
- When JIT helps (table)
- How to mark + verify compilation
- Supported types & control flow
- Supported built-ins
- `@state` + `@jit` combo for HF factors
- Common traps (silent interpreter fallback, etc.)
- Microbenchmark template + when to prefer vectorized SQL


DolphinDB's JIT compiles marked functions to native code via LLVM. It
can 10× – 50× imperative (loop-heavy) code. But it's picky: not every
function benefits, and a wrong signature silently falls back to
interpreter mode.

## When JIT helps

| Pattern | JIT gain |
|---------|----------|
| Tight `for` / `while` loops over scalars | **huge** (10–50×) |
| Row-by-row logic that resists vectorization (stateful iteration, if/else forks on each element) | large |
| Factor compute inside reactive state engine (one row at a time) | large |
| Options pricing, root-finding, bisection, simulation | large |
| Already vectorized SQL (`select sum(x * y) ...`) | **none** — SQL engine is faster |
| Pure table ops (`join`, `group by`, `pivot`) | **none** |
| I/O bound (DFS read, network) | **none** |

Rule: JIT is for **CPU-bound scalar logic**. For array math, use the
vectorized path.

## How to mark

```dolphindb
@jit
def bsCall(spot, strike, r, t, sigma) {
    d1 = (log(spot / strike) + (r + 0.5 * sigma * sigma) * t) / (sigma * sqrt(t))
    d2 = d1 - sigma * sqrt(t)
    return spot * cdfNormal(0, 1, d1) - strike * exp(-r * t) * cdfNormal(0, 1, d2)
}

// compiles on first call; subsequent calls run native
bsCall(100.0, 100.0, 0.02, 1.0, 0.20)
```

Check it compiled:

```dolphindb
getJITFunctions()                              // list compiled
getFunctionView("bsCall").jit                  // boolean
```

## Supported types inside a JIT body

- Scalars: `BOOL`, `CHAR`, `SHORT`, `INT`, `LONG`, `FLOAT`, `DOUBLE`,
  and time types (which are integer underneath).
- Vectors: `INT[]`, `DOUBLE[]`, `LONG[]`, `TIMESTAMP[]`, etc. (limited
  element access; not all vector ops).
- **Not supported:** `STRING`, `SYMBOL`, tables, dictionaries, sets,
  arrays-of-arrays, `ANY` vector. If you use these, JIT silently falls
  back to interpreter (no warning), and you lose the speedup.

## Supported control flow

- `if / else`, `for (i in 0..n-1)`, `while`, `break`, `continue`.
- Nested functions and recursion: OK if the callee is also `@jit` or a
  JIT-friendly builtin.
- `try/catch`: **not supported**. Don't throw inside JIT.
- `return` once at the end, or multiple returns: both OK.

## Supported built-ins

Most arithmetic, math, and elementary functions (`log`, `exp`, `sqrt`,
`pow`, `sin`, `cos`, `abs`, `min`, `max`, `round`, …), time arithmetic
(`temporalAdd`), comparisons, and vector element access.

Anything table-shaped, SQL, or string-manipulating will either not compile
or will fall back.

## `@state` + `@jit` in reactive engines

```dolphindb
@state
@jit
def momentum(close) {
    return close / prev(close, 20) - 1
}
```

Order of the decorators doesn't matter. `@state` makes it usable in
`reactiveStateEngine`, `@jit` makes the per-row path native. This combo
is the biggest win for HF factor streaming (L2 tick rates).

## Common traps

- **Silent interpreter fallback** when you use an unsupported feature.
  Verify with `getFunctionView("fn").jit == true`.
- **First call is slow** — it includes compile time. Pre-warm:
  `bsCall(1.0, 1.0, 0.0, 1.0, 0.1)` in `initialize`.
- **Global variables** are captured by value at compile time — changes
  after compile are invisible to the JIT code. Pass as arguments.
- **Partial apply** (`f{x, _, _}`) inside a JIT function blocks
  compilation in some versions. Prefer explicit args.
- **`print`, `writeLog`, `throw`** are all non-JIT. Remove for prod; add
  a non-JIT wrapper for debug.
- **Type stability:** if `x` is `DOUBLE` in one call and `INT` in the
  next, the JIT compiles per-signature — avoid mixing.

## Microbenchmark template

```dolphindb
n = 1000000
xs = rand(100.0, n)

// baseline
start = now(); 
interp = each(bsCall{_, 100.0, 0.02, 1.0, 0.20}, xs); 
print("interp: " + (now() - start) + "ms")

// jit-warm already
start = now()
jit = bsCall(xs, 100.0, 0.02, 1.0, 0.20)      // if function is vector-friendly
print("jit vec: " + (now() - start) + "ms")
```

## When to prefer vectorized SQL instead

```dolphindb
// JIT: ~ 50ms for 1M rows
res = each(bsCall, spots, strikes, rs, ts, sigmas)

// SQL-vectorized (builtin normcdf is vectorized): ~ 20ms, no compile
d1 = (log(spot / strike) + (r + 0.5 * sigma * sigma) * t) / (sigma * sqrt(t))
d2 = d1 - sigma * sqrt(t)
res = spot * cdfNormal(0, 1, d1) - strike * exp(-r * t) * cdfNormal(0, 1, d2)
```

If the computation can be expressed as a single vectorized SQL
expression, prefer it. JIT's niche is stateful loops and conditionals.

## See also

- `../tutorials/jit.md` — comprehensive upstream tutorial.
- `../tutorials/IV_Greeks_Calculation_for_ETF_Options_Using_JIT.md` —
  worked case.
- `../backtest/factors.md` — `@state` + `@jit` for HF factors.
- `query-optimization.md`, `memory-threading.md`.
