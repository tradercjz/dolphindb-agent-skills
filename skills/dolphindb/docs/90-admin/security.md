# Users, groups & access control

## Users / groups

```dolphindb
createUser(userId="alice", password="s3cret", groupIds=`analysts, isAdmin=false)
createGroup(groupId=`analysts)

addGroupMember(userId=`alice, groupId=`analysts)
resetPassword(userId=`alice, newPassword="new-s3cret")
deleteUser(`alice)

getUserList()
getGroupList()
getUserAccess(`alice)
```

Login:

```dolphindb
login(`alice, "s3cret")
logout()
```

## Grant privileges

```dolphindb
grant("alice", TABLE_READ,  "dfs://demo.trades")
grant("alice", TABLE_WRITE, "dfs://demo.trades")
grant("analysts", VIEW_EXEC, "myFuncView")
revoke("alice", TABLE_WRITE, "dfs://demo.trades")
```

Privileges:

| Privilege | Applies to |
|-----------|------------|
| `TABLE_READ` / `TABLE_WRITE` | DFS tables (wildcards allowed). |
| `DB_READ` / `DB_WRITE` / `DB_MANAGE` | DFS databases. |
| `VIEW_EXEC` | Function views. |
| `SCRIPT_EXEC` | Scripting privileges. |
| `DBOBJ_CREATE` / `DBOBJ_DELETE` | Database object creation/drop. |
| `DB_OWNER` | Full DB ownership. |
| `QUERY_RESULT_MEM_LIMIT`, `TASK_GROUP_MEM_LIMIT` | Resource quotas. |

## Function views

Function views encapsulate a script that runs with **elevated privilege**
on behalf of the caller — the classic pattern to let a restricted user run
just one approved query.

```dolphindb
def myView(sym) {
    return select * from loadTable("dfs://demo", `trades) where sym = sym
}

addFunctionView(myView)
grant(`alice, VIEW_EXEC, "myView")
```

`getFunctionViews()`, `dropFunctionView(myView)`.

## LDAP

DolphinDB supports LDAP authentication via the `LDAP` plugin. See
`reference/plugins-catalog.md`.

## Audit

```dolphindb
getAuditLog()
getRecentLoginInfo()
```

## Traps

- **Admin user (`admin`)** has all privileges; never give it out. Create
  per-app accounts with minimum grants.
- **DB_READ grants read on ALL tables in the DB** — use TABLE_READ for
  fine-grained.
- **Function views are cached per session**; drop + recreate to update.

## See also

- `reference/error-codes/INDEX.md` — `S04xxx` admin/permission errors.
- Sibling files in this directory for admin / security topics.
