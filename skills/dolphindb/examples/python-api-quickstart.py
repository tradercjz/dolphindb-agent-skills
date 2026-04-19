"""End-to-end Python API quickstart.

Requirements:
    pip install dolphindb pandas numpy

Before running, ensure:
    - A DolphinDB server is listening on localhost:8848 with admin/123456.
    - `examples/create-dfs-and-load.dos` has been executed on that server.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import dolphindb as ddb


def main() -> None:
    s = ddb.session()
    s.connect("localhost", 8848, "admin", "123456")
    try:
        # 1. Simple query
        print(s.run("1 + 2"))                 # -> 3

        # 2. Table query → pandas DataFrame
        df = s.run("""
            select top 5 sym, ts, price, volume
            from loadTable('dfs://demo', `trades)
            where sym = `AAPL
            order by ts
        """)
        print("\n--- first 5 AAPL rows ---")
        print(df)

        # 3. Upload a DataFrame and append to a DFS table
        new_rows = pd.DataFrame({
            "sym":    pd.Series(["AAPL", "AAPL"], dtype="object"),
            "ts":     pd.to_datetime(["2024-01-02 15:59:00", "2024-01-02 15:59:30"]),
            "price":  np.array([101.5, 101.8], dtype="float64"),
            "volume": np.array([100, 200], dtype="int32"),
        })
        s.upload({"chunk": new_rows})
        s.run("""
            // cast sym column to SYMBOL to match the DFS schema
            t = table(symbol(chunk.sym) as sym, timestamp(chunk.ts) as ts,
                      double(chunk.price) as price, int(chunk.volume) as volume)
            loadTable('dfs://demo', `trades).append!(t)
        """)

        # 4. Confirm
        count = s.run("exec count(*) from loadTable('dfs://demo', `trades)")
        print(f"\ntotal rows: {count}")

        # 5. A rolling-window query (context by)
        ma = s.run("""
            select sym, ts, price, mavg(price, 5) as ma5
            from loadTable('dfs://demo', `trades)
            where sym = `AAPL and date(ts) = 2024.01.02
            context by sym csort ts
            limit 10
        """)
        print("\n--- rolling ma5 for AAPL ---")
        print(ma)
    finally:
        s.close()


if __name__ == "__main__":
    main()
