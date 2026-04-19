<!-- Auto-mirrored from upstream `documentation-main/plugins/uniqueid.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# UniqueID

DolphinDB 推出了 UniqueID 插件，用于生成唯一 ID。相比于长度较长且不便于记忆的 UUID，该插件提供了一种更简洁的自增 ID 方案。用户可自定义初始
ID，由服务器统一管理并自增生成唯一 ID，客户端可随时获取，满足生产环境中对短且易读唯一标识符的需求。

## 在插件市场安装插件

### 版本要求

* DolphinDB Server: 2.00.13
* OS: x86-64 Linux

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   ```
   login("admin", "123456");
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("UniqueID");
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("UniqueID");
   ```

## 接口说明

### createGenerator

**语法**

`UniqueID::createGenerator(name[, initUid = 1]);`

**参数**

**name** STRING 类型标量，表示 ID 生成器的名称。

**initUid** 可选参数，LONG 类型标量，表示 ID 生成器的初始值，支持负数。默认值为 1。

**详情**

创建并返回名为 *name* 的 ID 生成器 。

### getGenerator

**语法**

`UniqueID::getGenerator(name);`

**参数**

**name** STRING 类型标量，表示 ID 生成器的名称。

**详情**

返回名为 *name* 的 ID 生成器。

### newUid

**语法**

`UniqueID::newUid(generator[, size=1]);`

**参数**

**generator** ID 生成器，接口 `createGenerator` 或
`getGenerator` 的返回值。

**size** 可选参数，整型标量，表示要生成的 ID 的个数，默认值为 1。

**详情**

*generator* 生成器生成并返回 *size* 个 ID。

返回值为 LONG 类型的标量或向量。

### listGenerators

**语法**

`UniqueID::listGenerator();`

**详情**

获取当前服务器上所有 ID 生成器的名称及当前最新 ID。

返回值为一个表。

### destroyGenerator

**语法**

`UniqueID::destroyGenerator(name|generator);`

**参数**

**name** STRING 类型标量，表示 ID 生成器的名称。

**generator** ID 生成器，接口 `createGenerator` 或
`getGenerator` 的返回值。

**详情**

销毁指定的 ID 生成器。

无返回值。

## 示例

```
gen = UniqueID::createGenerator("mygen",10);
id = UniqueID::newUid(gen);
print(id);
// output:10
ids = UniqueID::newUid(gen, 5);
print(ids);
// [11,12,13,14,15]
UniqueID::destroyGenerator(gen);
// 或 UniqueID::destroyGenerator("mygen");
```
