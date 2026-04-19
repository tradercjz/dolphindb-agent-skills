<!-- Auto-mirrored from upstream `documentation-main/stream/cross_cluster_sub.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# иЈ®йЫЖзЊ§иКВзВєйЧіиЃҐйШЕ

жЬђиКВдїЛзїНиЈ®йЫЖзЊ§иКВзВєйЧіиЃҐйШЕжµБе§ДзРЖзїУжЮЬзЪДдЇ§дЇТжЦєеЉПгАВеѓєдЇОиЈ®йЫЖзЊ§иКВзВєйЧіиЃҐйШЕпЉМеПСеЄГзЂѓдЄОиЃҐйШЕзЂѓдЄНеЬ®еРМдЄАдЄ™йЫЖзЊ§пЉМеЬ®иЃҐйШЕжЧґйЬАи¶БжМЗеЃЪињЬз®ЛињЮжО•зЪДеП•жЯДгАВ

дЄЛйЭҐдЄЇдї•йАРзђФжИРдЇ§жХ∞жНЃдЄЇдЊЛдїЛзїНиЃҐйШЕжµБжХ∞жНЃзїУжЮЬиЃҐйШЕеПКеЖЩеЕ•жХ∞жНЃеЇУзЪДжµБз®ЛгАВ

1. еПСеЄГзЂѓеИЫеїЇдЄАдЄ™еЕ±дЇЂзЪДжµБжХ∞жНЃи°® *tglobal*гАВ

   ```
   name = `ChannelNo`ApplSeqNum`MDStreamID`BidApplSeqNum`OfferApplSeqNum`SecurityID`SecurityIDSource`TradePrice`TradeQty`ExecType`TradeTime`LocalTime`SeqNo`DataStatus`TradeMoney`TradeBSFlag`BizIndex`OrderKind`Market
   type = [INT,LONG,SYMBOL,LONG,LONG,SYMBOL,SYMBOL,DOUBLE,INT,SYMBOL,TIMESTAMP,TIME,LONG,INT,DOUBLE,SYMBOL,LONG,SYMBOL,SYMBOL]
   share streamTable(100:0, name, type) as tglobal
   ```
2. иЃҐйШЕзЂѓеИЫеїЇдЄАдЄ™еИЖеЄГеЉПжХ∞жНЃи°®пЉМзФ®дЇОе≠ШеВ®иЃҐйШЕеИ∞зЪДжХ∞жНЃгАВ

   ```
   if(existsDatabase("dfs://tradeDB"))
       dropDatabase("dfs://tradeDB")
   db1 = database(, VALUE, 2020.01.01..2021.01.01)
   db2 = database(, HASH, [SYMBOL, 50])
   db = database("dfs://tradeDB", COMPO, [db1, db2], , "TSDB")
   name = `ChannelNo`ApplSeqNum`MDStreamID`BidApplSeqNum`OfferApplSeqNum`SecurityID`SecurityIDSource`TradePrice`TradeQty`ExecType`TradeTime`LocalTime`SeqNo`DataStatus`TradeMoney`TradeBSFlag`BizIndex`OrderKind`Market
   type = [INT,LONG,SYMBOL,LONG,LONG,SYMBOL,SYMBOL,DOUBLE,INT,SYMBOL,TIMESTAMP,TIME,LONG,INT,DOUBLE,SYMBOL,LONG,SYMBOL,SYMBOL]
   t = db.createPartitionedTable(table=table(1:0, name, type), tableName="tradeTB", partitionColumns=`TradeTime`SecurityID, sortColumns=[`SecurityID, `TradeTime])
   ```
3. еИЫеїЇи°® *tglobal* зЪДжЬђеЬ∞иЃҐйШЕпЉМserver еПВжХ∞йЬАиЃЊзљЃдЄЇињЬз®ЛињЮжО•зЪДеП•жЯДпЉЫ *handler* иЃЊзљЃдЄЇйЬАи¶БеЖЩеЕ•зЪДи°®
   *trades*пЉМ*batchSize* еТМ *throttle* еЇФж†єжНЃйЬАж±ВеРИзРЖиЃЊзљЃпЉМеЕЈдљУеПВжХ∞еРЂдєЙиІБsubscribeTableгАВ

   ```
   trade = loadTable("dfs://tradeDB", "tradeTB")
   pubNodeHandler=xdb("YOUR_IP",8892)
   subscribeTable(server=pubNodeHandler, tableName="tglobal", actionName="insertDB", offset=0, handler=trade, msgAsTable=true, batchSize=100000, throttle=60)
   ```
4. еРСеПСеЄГзЂѓжµБжХ∞жНЃи°® *tglobal* еЖЩеЕ•ж®°жЛЯжХ∞жНЃгАВ

   ```
   for(i in 1..100){
       insertData = [rand(100,1),long(i),string(i),long(i),long(i),string(i),string(i),rand(1.0,1),rand(100,1),string(i),timestamp('2021.01.04T09:30:02.000'),time('09:30:02.000'),long(i),rand(100,1),rand(1.0,1),string(i),long(i),string(i),string(i)]
       insert into tglobal values(insertData)
   }
   ```
5. жЯ•зЬЛеЖЩеЕ•жО•жФґзЂѓеЇУи°®зЪДжХ∞жНЃгАВ

   ```
   select * from loadTable("dfs://tradeDB","tradeTB") limit 5

   // output
   ChannelNo	ApplSeqNum	MDStreamID	BidApplSeqNum	OfferApplSeqNum	SecurityID	SecurityIDSource	TradePrice	TradeQty	ExecType	TradeTime	LocalTime	SeqNo	DataStatus	TradeMoney	TradeBSFlag	BizIndex	OrderKind	Market
   60	43	43	43	43	43	43	0.7538	56	43	2021.01.04T09:30:02.000	09:30:02.000	43	92	0.6234	43	43	43	43
   56	59	59	59	59	59	59	0.1549	48	59	2021.01.04T09:30:02.000	09:30:02.000	59	94	0.428	59	59	59	59
   60	92	92	92	92	92	92	0.198	13	92	2021.01.04T09:30:02.000	09:30:02.000	92	87	0.2109	92	92	92	92
   57	41	41	41	41	41	41	0.0822	30	41	2021.01.04T09:30:02.000	09:30:02.000	41	32	0.2611	41	41	41	41
   7	61	61	61	61	61	61	0.7593	81	61	2021.01.04T09:30:02.000	09:30:02.000	61	15	0.7564	61	61	61	61
   ```
6. ељУжµБжХ∞жНЃиЃҐйШЕзїУжЭЯжЧґпЉМеПѓдї•еПЦжґИиЃҐйШЕеєґеПЦжґИеѓєжµБжХ∞жНЃи°®зЪДеЃЪдєЙпЉМеПЦжґИжµБжХ∞жНЃи°®еЃЪдєЙйЬАеЬ®еѓєиѓ•и°®зЪДиЃҐйШЕеЕ®йГ®еПЦжґИеРОињЫи°МгАВ

   ```
   //еПЦжґИиЃҐйШЕ
   unsubscribeTable(tableName="tglobal", actionName="insertDB")
   //еПЦжґИеЃЪдєЙжµБжХ∞жНЃи°®
   undef(`tglobal, SHARED)
   ```

**зЫЄеЕ≥дњ°жБѓ**

* [undef](../funcs/u/undef.html "undef")
* [database](../funcs/d/database.html "database")
* [streamTable](../funcs/s/streamTable.html "streamTable")
* [subscribeTable](../funcs/s/subscribeTable.html "subscribeTable")
* [unsubscribeTable](../funcs/u/unsubscribeTable.html "unsubscribeTable")
* [createPartitionedTable](../funcs/c/createPartitionedTable.html "createPartitionedTable")

Copyright

**¬©2026 жµЩж±ЯжЩЇиЗЊзІСжКАжЬЙйЩРеЕђеПЄ жµЩICPе§З18048711еПЈ-3**
