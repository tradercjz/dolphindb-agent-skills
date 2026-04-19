# C++ API

Header: `#include "DolphinDB.h"`, namespace `dolphindb`.

## Connect

```cpp
#include "DolphinDB.h"
using namespace dolphindb;

DBConnection conn;
conn.connect("localhost", 8848, "admin", "123456");
```

## Run a script

```cpp
ConstantSP t = conn.run("select top 10 * from loadTable('dfs://demo',`trades)");

TableSP tbl = (TableSP) t;
for (int r = 0; r < tbl->rows(); ++r) {
    std::string sym = tbl->getColumn(0)->getString(r);
    double      px  = tbl->getColumn(1)->getDouble(r);
}
```

Return type is always `ConstantSP` (a smart pointer base type). Cast to
`TableSP`, `VectorSP`, `DictionarySP` as needed.

## Upload / append

```cpp
vector<string> colNames = {"sym", "px"};
vector<DATA_TYPE> colTypes = {DT_SYMBOL, DT_DOUBLE};
TableSP t = Util::createTable(colNames, colTypes, 0, 1000);

((VectorSP)(t->getColumn(0)))->appendString(new string[]{"AAPL","MSFT"}, 2);
((VectorSP)(t->getColumn(1)))->appendDouble(new double[]{100.0, 260.0}, 2);

conn.upload("cppTable", vector<ConstantSP>{t});
conn.run("loadTable('dfs://demo',`trades).append!(cppTable)");
```

High-throughput writers:
- `PartitionedTableAppender`
- `MultithreadedTableWriter`

## Subscribe

```cpp
ThreadedClient client(8849);
ThreadSP t = client.subscribe("localhost", 8848, [](Message msg) {
    // msg is a TableSP row snapshot
}, "ticks", "cppDemo", -1);
t->join();
```

## Build

Linking requires `libDolphinDBAPI.so` (or `.dll` / `.dylib`) plus its
dependencies. Minimum C++14. See the official cpp manual for concrete
Makefile/CMake recipes.

## See also

- `type-mapping.md`.
- `cpp/` subdirectory and external manual
  <https://docs.dolphindb.cn/zh/cppdoc/cpp_api.html>.
