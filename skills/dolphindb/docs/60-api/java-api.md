# Java API

Package: `com.xxdb` (Maven: `com.dolphindb:jdbc` for JDBC; `com.dolphindb:api-java` for the native API).

## Connect

```java
import com.xxdb.DBConnection;
import com.xxdb.data.*;

DBConnection conn = new DBConnection();
conn.connect("localhost", 8848, "admin", "123456");
```

Pool for concurrent use:

```java
import com.xxdb.DBConnectionPool;
DBConnectionPool pool = new DBConnectionPool(
    new ExclusiveDBConnectionPool("localhost", 8848, "admin", "123456", 8, false, false));
```

## Run a script

```java
BasicTable t = (BasicTable) conn.run(
    "select top 10 * from loadTable('dfs://demo',`trades)");

for (int r = 0; r < t.rows(); r++) {
    String sym = t.getColumn("sym").getString(r);
    double px  = t.getColumn("px").getDouble(r);
    System.out.println(sym + " " + px);
}
```

Return types:

| DolphinDB | Java |
|-----------|------|
| scalar    | `BasicInt`, `BasicDouble`, `BasicString`, ... |
| vector    | `BasicIntVector`, `BasicDoubleVector`, ... |
| table     | `BasicTable` |
| dict      | `BasicDictionary` |

## Upload / append

```java
List<String> colNames = Arrays.asList("sym", "px");
List<Vector> cols = Arrays.asList(
    new BasicStringVector(new String[]{"AAPL","MSFT"}),
    new BasicDoubleVector(new double[]{100.0, 260.0})
);
BasicTable t = new BasicTable(colNames, cols);

Map<String, Entity> vars = new HashMap<>();
vars.put("jt", t);
conn.upload(vars);
conn.run("loadTable('dfs://demo',`trades).append!(jt)");
```

High-throughput ingest: `PartitionedTableAppender`,
`MultithreadedTableWriter` (same as the Python API).

## Subscribe to a stream

```java
import com.xxdb.streaming.client.*;

PollingClient client = new PollingClient("localhost", 8849);   // local port
TopicPoller poller = client.subscribe("localhost", 8848, "ticks", "javaDemo", -1);

while (true) {
    ArrayList<IMessage> msgs = poller.poll(1000);
    for (IMessage m : msgs) {
        // m.getValue(i) returns the i-th column value
    }
}
```

## JDBC

```java
Class.forName("com.dolphindb.jdbc.Driver");
Connection c = DriverManager.getConnection(
    "jdbc:dolphindb://localhost:8848?user=admin&password=123456");
PreparedStatement ps = c.prepareStatement("select * from t where sym=?");
ps.setString(1, "AAPL");
ResultSet rs = ps.executeQuery();
```

## See also

- `type-mapping.md` for full type table.
- Upstream external manual: <https://docs.dolphindb.cn/zh/javadoc/newjava.html>.
