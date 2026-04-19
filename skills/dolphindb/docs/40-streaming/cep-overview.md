# CEP — Complex Event Processing

DolphinDB's CEP engine lets you define **event types**, **monitors** (FSM-
like rules), and **listeners** in DolphinDB script. It is suited to
patterns that are awkward to express as stream-engine cascades — e.g.
multi-event sequences, conditional routing.

## Core concepts

- **Event class** — a typed record with declared fields, defined with
  `defineEvent`.
- **Monitor** — an object class (`class Monitor`) whose methods react to
  incoming events. Functions: `onload`, `onEvent<EventClass>`.
- **Engine** — `createCEPEngine(name, monitors, ...)` spawns a CEP engine
  that feeds monitors.

## Minimal example

```dolphindb
// Define event classes
defineEvent("Tick",  {sym:SYMBOL, px:DOUBLE, ts:TIMESTAMP})
defineEvent("Alert", {sym:SYMBOL, reason:STRING, ts:TIMESTAMP})

class PriceJumpMonitor {
    def onload() { lastPx = dict(SYMBOL, DOUBLE) }
    def onTick(e) {
        if(lastPx.contains(e.sym) && abs(e.px - lastPx[e.sym]) > 1.0) {
            emit(Alert(e.sym, "jump", e.ts))
        }
        lastPx[e.sym] = e.px
    }
}

engine = createCEPEngine(name="pj",
                         monitors=[PriceJumpMonitor()],
                         eventSchema=[Tick, Alert])

// push events in
engine.appendEvent(Tick(`AAPL, 100.0, now()))
```

## When to choose CEP vs a stream engine

- **CEP**: stateful, per-key FSMs; sequence detection ("buy after cancel
  within 5s"); multi-event pattern matching; user-defined classes.
- **Stream engine**: pure aggregation / windowed join / reactive state
  computation; higher throughput.

If your logic fits `reactiveStateEngine + asof + timeseries`, pick those.
If it doesn't, CEP is the escape hatch.

## See also

- `cep.md`, `cep_engine.md`, `cep_basic_concept.md`,
  `cep_events_defining.md`, `cep_monitor_defining.md`,
  `cep_monitoring.md`, `cep_application.md`.
