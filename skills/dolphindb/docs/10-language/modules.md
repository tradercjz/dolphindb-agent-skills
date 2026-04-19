# Modules

DolphinDB modules group related functions into importable units.

## Layout

Module files live under the server's `<home>/modules/` directory (path is
server-configurable). Each file starts with:

```dolphindb
module myLib::utils
```

Sub-modules use `::`: `module myLib::math::stats`.

## Export

Every top-level `def` in a module file is exported unless marked `local`:

```dolphindb
module myLib::math

local def _internal(x): x * 2        // not exported
def square(x): x * x                 // exported
```

Exported names can be called as `myLib::math::square(3)` after import.

## Use

```dolphindb
use myLib::math                     // enables square() unqualified
use myLib::math as m                // enables m::square()
```

## File organization

```
modules/
  myLib/
    math.dos
    stats.dos
  bigProj/
    engine/
      core.dos
      init.dos                  // optional: runs at module load
```

## Init code

A `module` file may contain top-level statements after `module ...;`. They
run **once at import time** in a dedicated namespace.

## Installing shared modules

```dolphindb
// runtime module install from the marketplace
installModule("myLib")
```

## Traps

- **File name must match module name**. `module myLib::utils` must live at
  `modules/myLib/utils.dos`.
- **Circular imports** are detected and error out.
- **Exported state** (mutable variables) is shared across sessions. Use a
  dict keyed by session for per-session state.

## See also

- `progr_intro.md`, `lang_intro.md`, upstream
  `tutorials/tu_modules.md`.
