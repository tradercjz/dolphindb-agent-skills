<!-- Auto-mirrored from upstream `documentation-main/mcp/develop_mcp_tool.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# MCP 工具开发指南

## 开发流程概述

DolphinDB MCP 工具的开发遵循以下标准流程:

1. **定义函数**：实现工具的核心业务逻辑。
2. **编写描述**：为大模型提供详细的调用指南。
3. **注册工具**：使用 `addMCPTool` 或 `updateMCPTool`将工具注册到 MCP Server。
4. **发布工具**：使用 `publishMCPTools` 将工具发布，使客户端可以调用。

## 函数定义

### 参数类型限制

由于 MCP 工具参数通过大模型以 JSON 格式传入，目前支持的类型如下：

| DolphinDB 类型 | JSON 类型 | 说明 |
| --- | --- | --- |
| STRING | string | 字符串 |
| TEMPORAL (DATE 等) | string | 时间类型，传入字符串后转换 |
| DOUBLE | number | 数值类型 |
| BOOL | boolean | 布尔类型 |
| STRING[] | array\<string\> | 字符串数组 |
| TEMPORAL[] | array\<string\> | 时间数组 |
| DOUBLE[] | array\<number\> | 数值数组 |
| BOOL[] | array\<boolean\> | 布尔数组 |

**注意**：DICT 类型不能直接作为 MCP 函数参数传入，但可以通过 JSON 字符串方式传入，再在函数内使用
`parseExpr().eval()` 解析成字典对象。

### 参数设计

* **直观性**：参数名应：具有自然语言含义，例如使用 *stockCodes* 而非 *codes*。
* **明确性**：当参数有限定取值时，应在描述中完整列出所有可能值。
* **会话管理**：若需保存一次工具调用的中间结果，建议包含 *sessionId* 和 *resultTableName*
  参数，用于共享内存表管理。

### 返回值设计

* **表格数据**：建议使用 `toStdJson(t[0:min(10, t.size())])`
  返回前10行样例。
* **状态信息**：返回操作结果、共享表名、数据量等关键信息。
* **精炼性**：避免返回过多数据，防止上下文过长。

### 示例函数代码

```
def get_stock_basic_info(stockCodes, resultTableName, sessionId){
    // 1. 加载数据并筛选
    t = select * from loadTable("dfs://basic_factor", "stock_basic")
        where ts_code in stockCodes or symbol in stockCodes

    // 2. 会话管理 - 条件性共享内存表
    if (trim(sessionId) != "") {
        if (trim(resultTableName) != "") {
            resultName = resultTableName + "_" + sessionId
            share(t, resultName)
            return "查询成功：共享表名 " + resultName +
                   "\n前10行数据：\n" + toStdJson(t[0:min(10, t.size())])
        }
    }

    // 3. 直接返回结果
    return "查询成功：前10行数据：\n" + toStdJson(t[0:min(10, t.size())])
}
```

## 工具描述编写

工具描述是大模型理解并正确调用 MCP 工具的关键，必须包含以下几个部分。

### 描述结构模板

```
description_xxx = '
[功能概述] - 一句话说明工具的核心功能

参数说明：
- 参数1: 类型，描述
- 参数2: 类型，描述（如有限定取值，列举所有可能值）
- sessionId: STRING，当前会话唯一id，用于生成唯一的共享表名。如果为空，则不共享内存表，直接返回查询结果
- resultTableName: STRING，共享内存表名，用于后续分析。建议使用有意义的名称如 "xxx"

返回：
- 操作结果信息，包含共享表名（如果有）和前10行样例数据

示例代码：

// 示例1 - 完整使用（含中间表管理）
函数名([参数值], "table_name", "session123")

// 示例2 - 简化使用（不共享内存表）
函数名([参数值], "", "")
'
```

### 描述编写要点

**功能概述**

* 开门见山，用一句话说明工具的用途。
* 示例：“从 DolphinDB 基础信息表 stock\_basic 加载指定股票代码的基础信息”。

**参数说明**

* 每个参数必须包含名称、类型、详细描述。
* 列表类型使用 STRING[]、DATE[] 等表示。
* 对于有限定取值的参数，明确列出所有可能值。
* 示例：

  ```
  - stockCodes: STRING[]，股票代码列表
  - dates: DATE[]，日期范围列表
  ```

**返回说明**

* 明确说明返回内容的格式和包含的信息。
* 示例：“操作结果信息，包含共享表名（如果有）和前10行样例数据”。

**示例代码**

* 提供至少2个示例，覆盖主要使用场景。
* 使用注释说明每个示例的场景。

### 完整示例

```
description_select_stocks_by_factors = '
用于从 DolphinDB 表 day_factor 中根据用户输入的指标和筛选条件进行选股。支持用户输入的筛选条件，并基于最新交易日的数据进行筛选。

参数说明：
- factors: STRING[]，用户输入的指标列表，支持现有指标（如 "pe", "pb"）
- conditions: STRING[]，筛选条件列表，每个条件是一个字符串表达式（如 "pe < 15", "pb > 1"）
- resultTableName: STRING，共享内存表名，用于后续分析。建议使用有意义的名称如 "selected_stocks"
- sessionId: STRING，当前会话唯一id，用于生成唯一的共享表名。如果为空，则不共享内存表，直接返回查询结果

返回：
- 操作结果信息，包含共享表名（如果有）和前10行样例数据

示例：

// 按指标 "pe", "pb" 选股，筛选条件为 "pe < 15", "pb > 1"
select_stocks_by_factors(["pe", "pb"], ["pe < 15", "pb > 1"], "selected_stocks", "session123")

// 不共享内存表的简化调用
select_stocks_by_factors(["rev_yoy", "profit_yoy"], ["rev_yoy > 10", "profit_yoy > 5"], "", "")
'
```

## 工具注册与发布

MCP 工具开发完成后，需要先注册，再发布给客户端使用。

### 条件注册

使用 `addMCPTool` 或 `updateMCPTool` 将函数注册为 MCP
工具。

推荐使用以下模板注册工具：

```
if (`tool_name in (exec name from listMCPTools())) {
  updateMCPTool(`tool_name, tool_function,
                `param1`param2`param3,
                ["TYPE1", "TYPE2", "TYPE3"],
                description_tool_name)
} else {
  addMCPTool(`tool_name, tool_function,
             `param1`param2`param3,
             ["TYPE1", "TYPE2", "TYPE3"],
             description_tool_name)
}
```

若需要更新已有 MCP 工具，使用 `updateMCPTool`，参数与 `addMCPTool`
类似。

### 发布工具

使用 `publishMCPTools()` 将已注册的工具发布，使客户端可以调用。

发布后，客户端即可在工具列表中选择和启用工具。

```
publishMCPTools(`tool_name)
```
