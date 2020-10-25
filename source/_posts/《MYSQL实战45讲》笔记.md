---
title: 《MYSQL实战45讲》笔记
date: 2020-03-31 11:34:28
tags: MYSQL
---
# 基本

1. 基本架构
    {% asset_img 0.png%}
￼
2. Mysql长链接使内存使用涨得快：
    - 定期断开长连接。
    - 如果你用的是 MySQL 5.7 或更新版本，可以在每次执行一个比较大的操作后，通过执行 mysql_reset_connection 来重新初始化连接资源。


3. WAL 的全称是 Write-Ahead Logging，它的关键点就是先写日志，再写磁盘。redo log 主要节省的是随机写磁盘的 IO 消耗（转成顺序写），而 change buffer 主要节省的则是随机读磁盘的 IO 消耗。
   - 得益于：
     - redo log 和 binlog 都是顺序写，磁盘的顺序写比随机写速度要快；
     - 组提交机制，可以大幅度降低磁盘的 IOPS 消耗。

4. change buffer：当需要更新一个数据页时，如果数据页在内存中就直接更新，而如果这个数据页还没有在内存中的话，在不影响数据一致性的前提下，InnoDB 会将这些更新操作缓存在 change buffer 中，这样就不需要从磁盘中读入这个数据页了。在下次查询需要访问这个数据页的时候，将数据页读入内存。
    - 何时触发merge：访问这个数据页会；系统有后台线程会定期 merge；在数据库正常关闭（shutdown）的过程中。

5. 脏页：当内存数据页跟磁盘数据页内容不一致的时候，我们称这个内存页为“脏页”。脏页什么时候引起flush写入磁盘：
    - InnoDB 的 redo log 写满了。这时候系统会停止所有更新操作，把 checkpoint 往前推进，redo log 留出空间可以继续写。
    - 系统内存不足。当需要新的内存页，而内存不够用的时候，就要淘汰一些数据页，空出内存给别的数据页使用。如果淘汰的是“脏页”，就要先将脏页写到磁盘。
    - 系统“空闲”的时候。
    - MySQL 正常关闭的时候。
6. InnoDB 刷脏页的控制策略：
    - innodb_io_capacity 参数会告诉 InnoDB 你的磁盘能力。这个值我建议你设置成磁盘的 IOPS。
    - innodb_max_dirty_pages_pct 是脏页比例上限，默认值是 75%。
    - 合理地设置 innodb_io_capacity 的值，并且平时要多关注脏页比例，不要让它经常接近 75%。
    - innodb_flush_neighbors=0，只刷自己脏页，不刷邻居。
7. 如果你创建的表没有主键，或者把一个表的主键删掉了，那么 InnoDB 会自己生成一个长度为 6 字节的 rowid 来作为主键。
8. join算法：
    1.  Index Nested-Loop Join（NLJ）：先遍历表 驱动表t1，然后根据从表 t1 中取出的每行数据中的 a 值，去被驱动表 t2 根据索引中查找满足条件的记录。
    2.  Block Nested-Loop Join（BNL）：把驱动表 t1 的数据读入线程内存 join_buffer 中，再扫描被驱动表 t2，把表 t2 中的每一行取出来，跟 join_buffer 中的数据做对比（内存操作），满足 join 条件的，作为结果集的一部分返回。
        - join_buffer 的大小是由参数 join_buffer_size 设定的，默认值是 256k。
        - 如果放不下驱动表 t1 的所有数据话，策略就是分段放。
    3. Batched Key Access(BKA)：NLJ的优化，把表 t1 的数据取出来一部分，先放到一个临时内存join_buffer。在用BNL算法处理。
    4. 如果可以使用 Index Nested-Loop Join 算法，也就是说可以用上被驱动表上的索引，其实是没问题的；如果使用 Block Nested-Loop Join 算法，扫描行数就会过多。尤其是在大表上的 join 操作，这样可能要扫描被驱动表很多次，会占用大量的系统资源。所以这种 join 尽量不要用。
    5. 在决定哪个表做驱动表的时候，应该是两个表按照各自的条件过滤，过滤完成之后，计算参与 join 的各个字段的总数据量，数据量小的那个表，就是“小表”，应该作为驱动表。
    6. 大表 join 操作虽然对 IO 有影响，但是在语句执行结束后，对 IO 的影响也就结束了。但是，对 Buffer Pool 的影响就是持续性的，需要依靠后续的查询请求慢慢恢复内存命中率。
9.  MySQL 是“边读边发的”，取数据发数据流程：
    1.  获取一行，写到 net_buffer 中。这块内存的大小是由参数 net_buffer_length 定义的，默认是 16k。
    2.  重复获取行，直到 net_buffer 写满，调用网络接口发出去。
    3.  如果发送成功，就清空 net_buffer，然后继续取下一行，并写入 net_buffer。
    4.  如果发送函数返回 EAGAIN 或 WSAEWOULDBLOCK，就表示本地网络栈（socket send buffer）写满了，进入等待。直到网络栈重新可写，再继续发送。
    5.  对于正常的线上业务来说，如果一个查询的返回结果不会很多的话，我都建议你使用 mysql_store_result 这个接口，直接把查询结果保存到本地内存。如果返回数据很多，使用mysql_use_result。
10. 一个稳定服务的线上系统，要保证响应时间符合要求的话，内存命中率要在 99% 以上。（执行 show engine innodb status，查询Buffer pool hit rate）。
11. InnoDB 内存管理用的是最近最少使用 (Least Recently Used, LRU) 算法。优化：按照 5:3 的比例把整个 LRU 链表分成了 young 区域和 old 区域。处于 old 区域的数据页，每次被访问的时候，若这个数据页在 LRU 链表中存在的时间超过了 1 秒，才把它移动到链表头部。
12. 自增id不连续原因：
    - 唯一键冲突
    - 事务回滚
    - 批量插入数据
13. 在生产上，尤其是有批量插入数据（包含的语句类型是 insert … select、replace … select 和 load data 语句）的场景时，从并发插入数据性能的角度考虑，建议设置：innodb_autoinc_lock_mode=2 ，并且 binlog_format=row
14. insert … select 是很常见的在两个表之间拷贝数据的方法。你需要注意，在可重复读隔离级别下，这个语句会给 select 的表里扫描到的记录和间隙加读锁。
15. 如果 insert 和 select 的对象是同一个表，则有可能会造成循环写入。
16. insert 语句如果出现唯一键冲突，会在冲突的唯一值上加共享的 next-key lock(S 锁)。因此，碰到由于唯一键约束导致报错后，要尽快提交或回滚事务，避免加锁时间过长。
17. 主备间事务同步过程：备库 B 跟主库 A 之间维持了一个长连接。主库 A 内部有一个线程，专门用于服务备库 B 的这个长连接。
    - 在备库 B 上通过 change master 命令，设置主库 A 的 IP、端口、用户名、密码，以及要从哪个位置开始请求 binlog，这个位置包含文件名和日志偏移量。
    - 在备库 B 上执行 start slave 命令，这时候备库会启动两个线程。其中 io_thread 负责与主库建立连接。主库 A 校验完用户名、密码后，开始按照备库 B 传过来的位置，从本地读取 binlog，发给 B。
    - 备库 B 拿到 binlog 后，写到本地文件，称为中转日志（relay log）。
    - sql_thread 读取中转日志，解析出日志里的命令，并执行。
18. 主备延迟原因：
    - 备库所在机器的性能要比主库所在的机器性能差
    - 备库的压力大
    - 大事务
    - 备库的并行复制能力
19. 备库并行复制策略（v_5.7.22）：
    - COMMIT_ORDER，根据同时进入 prepare 和 commit 来判断是否可以并行的策略。
    - WRITESET，表示的是对于事务涉及更新的每一行，计算出这一行的 hash 值，组成集合 writeset。如果两个事务没有操作相同的行，也就是说它们的 writeset 没有交集，就可以并行。
    - WRITESET_SESSION，是在 WRITESET 的基础上多了一个约束，即在主库上同一个线程先后执行的两个事务，在备库执行的时候，要保证相同的先后顺序。
20. 检测数据库是否正常：
    - health_check表
    - 检测performance_schema信息
21. grant 语句会同时修改数据表和内存，判断权限的时候使用的是内存数据。因此，规范地使用 grant 和 revoke 语句，是不需要随后加上 flush privileges 语句的。flush privileges 语句本身会用数据表的数据重建一份内存权限数据，所以在权限数据可能存在不一致的情况下再使用。


# 日志
1. MySQL 的“双 1”配置，指的就是 sync_binlog 和 innodb_flush_log_at_trx_commit 都设置成 1。也就是说，一个事务完整提交前，需要等待两次刷盘，一次是 redo log（prepare 阶段），一次是 binlog。
2. binlog cache 是每个线程自己维护的，而 redo log buffer 是全局共用的。因为binlog 是不能“被打断的”。一个事务的 binlog 必须连续写，因此要整个事务完成后，再一起写到文件里。而 redo log 并没有这个要求。
   {% asset_img 4.png%}
3. 日志逻辑序号LSN，LSN 是单调递增的，用来对应 redo log 的一个个写入点。每次写入长度为 length 的 redo log， LSN 的值就会加上 length。组提交：当其中一个事务redo log写盘的时候，其他小于该lsn的其他事务在redo log buffer 也会顺带写盘。
4. 两阶段提交：数据库备份恢复/扩容一般用全量备份加上应用 binlog 来实现的，数据库奔溃后状态恢复使用redo log，因为两个是独立的逻辑，如果不是两阶段提交，那么数据库的状态就有可能和用它的日志恢复出来的库的状态不一致。
    1. 流程
        - 执行器先找引擎取 ID=2 这一行。ID 是主键，引擎直接用树搜索找到这一行。如果 ID=2 这一行所在的数据页本来就在内存中，就直接返回给执行器；否则，需要先从磁盘读入内存，然后再返回。
        - 执行器拿到引擎给的行数据，把这个值加上 1，比如原来是 N，现在就是 N+1，得到新的一行数据，再调用引擎接口写入这行新数据。
        - 引擎将这行新数据更新到内存中，同时将这个更新操作记录到 redo log 里面，此时 redo log 处于 prepare 状态。然后告知执行器执行完成了，随时可以提交事务。
        - 执行器生成这个操作的 binlog，并把 binlog 写入磁盘。
        - 执行器调用引擎的提交事务接口，引擎把刚刚写入的 redo log 改成提交（commit）状态，更新完成。
    2. crash：
        - 当prepare log 写入成功且binglog写入成功后发生crash，在mysql启动时候，会自动commit这个事物； 
        - 当prepare log写入成功，binlog写入失败，此时发生crash，mysql启动会自动回滚掉这个事务。
    {% asset_img 5.png%}

## redo log
1. redo log（重做日志）：保证crash-safe，InnoDB的物理日志，记录的是“在某个数据页上做了什么修改”。固定大小，从头开始写，写到末尾就又回到开头循环写。
￼   {% asset_img 1.png%}
2. write pos 是当前记录的位置，一边写一边后移，写到第 3 号文件末尾后就回到 0 号文件开头。checkpoint 是当前要擦除的位置，也是往后推移并且循环的，擦除记录前要把记录更新到数据文件。
3. InnoDB 用redo log保证即使数据库发生异常重启，之前提交的记录都不会丢失，这个能力称为 crash-safe。
4. innodb_flush_log_at_trx_commit 设置为 0 的时候，表示每次事务提交时都只是把 redo log 留在 redo log buffer 中 ;设置为 1 的时候，表示每次事务提交时都将 redo log 直接持久化到磁盘；设置为 2 的时候，表示每次事务提交时都只是把 redo log 写到 page cache。
5. InnoDB 有一个后台线程，每隔 1 秒，就会把 redo log buffer 中的日志，调用 write 写到文件系统的 page cache，然后调用 fsync 持久化到磁盘。
6. redo log buffer何时写盘：
   1. 占用的空间即将达到 innodb_log_buffer_size 一半的时候，后台线程会主动写盘。
   2. 并行的事务提交的时候，顺带将这个事务的 redo log buffer 持久化到磁盘。
7. 如果把 innodb_flush_log_at_trx_commit 设置成 1，那么 redo log 在 prepare 阶段就要持久化一次
8.  每秒一次后台轮询刷盘，再加上崩溃恢复这个逻辑，InnoDB 就认为 redo log 在 commit 的时候就不需要 fsync 了，只会 write 到文件系统的 page cache 中就够了。

## binlog
1.  binlog（归档日志）：Server层日志。逻辑日志，记录的是这个语句的原始逻辑，比如“给 ID=2 这一行的 c 字段加 1 ”。binlog 是可以追加写入的，写完一个文件新增一个文件。sync_binlog 这个参数设置成 1 的时候，表示每次事务的 binlog 都持久化到磁盘。
2. sync_binlog=0 的时候，表示每次提交事务都只 write，不 fsync；sync_binlog=1 的时候，表示每次提交事务都会执行 fsync；sync_binlog=N(N>1) 的时候，表示每次提交事务都 write，但累积 N 个事务后才 fsync。
3. binlog格式：
    - statement：SQL 语句的原文
    - row：记录操作的完整内容，容易恢复数据。
    - mixed：MySQL 自己会判断这条 SQL 语句是否可能引起主备不一致，如果有可能，就用 row 格式，否则就用 statement 格式。
4. 用 binlog 来恢复数据的标准做法是：用 mysqlbinlog 工具解析出来，然后把解析结果整个发给 MySQL 执行。
5. 把参数 log_slave_updates 设置为 on，表示备库执行 relay log 后生成 binlog。
6. MySQL 在 binlog 中记录了这个命令第一次执行时所在实例的 server id。每个库在收到从自己的主库发过来的日志后，先判断 server id，如果跟自己的相同，表示这个日志是自己生成的，就直接丢弃这个日志。

## redo log 与 binlog区别
1. redo log 是 InnoDB 引擎特有的；binlog 是 MySQL 的 Server 层实现的，所有引擎都可以使用。
2. redo log 是物理日志，记录的是“在某个数据页上做了什么修改”；binlog 是逻辑日志，记录的是这个语句的原始逻辑，比如“给 ID=2 这一行的 c 字段加 1 ”。
3. redo log 是循环写的，空间固定会用完；binlog 是可以追加写入的。“追加写”是指 binlog 文件写到一定大小后会切换到下一个，并不会覆盖以前的日志。
4. redo log buffer 是所有线程共用的， binlog buffer是每个线程独有的。因为binlog 是不能“被打断的”。一个事务的 binlog 必须连续写，因此要整个事务完成后，再一起写到文件里。

# 事务
1. 事务支持是在引擎层实现的。数据表中的一行记录，其实可能有多个版本 (row)，每个版本有自己的 row trx_id。
    {% asset_img 2.png%}
2. 显式启动事务语句， begin 或 start transaction。配套的提交语句是 commit，回滚语句是 rollback。set autocommit=1，自动提交。
3. begin/start transaction 命令并不是一个事务的起点，在执行到它们之后的第一个操作 InnoDB 表的语句，事务才真正启动。start transaction with consistent snapshot会马上启动一个事务。
4. 视图：InnoDB 在实现 MVCC 时用到的一致性读视图，即 consistent read view，用于支持 RC（Read Committed，读提交）和 RR（Repeatable Read，可重复读）隔离级别的实现。
5. 一致性视图：InnoDB 为每个事务构造了一个数组，用来保存这个事务启动瞬间，当前正在“活跃”（启动但未提交）的所有事务 ID。数组里面事务 ID 的最小值记为低水位，当前系统里面已经创建过的事务 ID 的最大值加 1 记为高水位。这个视图数组和高水位，就组成了当前事务的一致性视图（read-view）。
 {% asset_img 2.png%}
    - 如果落在绿色部分，表示这个版本是已提交的事务或者是当前事务自己生成的，这个数据是可见的；
    - 如果落在红色部分，表示这个版本是由将来启动的事务生成的，是肯定不可见的；
    - 如果落在黄色部分，那就包括两种情况
        - 若 row trx_id 在数组中，表示这个版本是由还没提交的事务生成的，不可见；
        - 若 row trx_id 不在数组中，表示这个版本是已经提交了的事务生成的，可见。
6. 更新数据都是先读后写的，而这个读，只能读当前的值，称为“当前读”（current read）。select 语句如果加锁（lock in share mode / for update），也是当前读。
7. 可重复读的核心就是一致性读（consistent read）；而事务更新数据的时候，只能用当前读。如果当前的记录的行锁被其他事务占用的话，就需要进入锁等待。
8. 唯一索引的更新就不能使用 change buffer，实际上也只有普通索引可以使用。因为唯一索引更新时需要将数据页读入内存，判断到没有冲突。
9. 收缩表空间：只是 delete 掉表里面不用的数据的话，只是把记录的位置，或者数据页标记为了“可复用”，但磁盘文件的大小是不会变的。重建表方法：
    - alter table A engine=InnoDB
    - Online DDL    
10. count在Inndb需要把数据一行一行地从引擎里面读出来，然后累积计数。按照效率排序的话，count(字段)< count(主键 id)< count(1)~ count(*)。
11. 幻读：指的是一个事务在前后两次查询同一个范围的时候，后一次查询看到了前一次查询没有看到的行。幻读仅专指“新插入的行”。在可重复读隔离级别下，普通的查询是快照读，是不会看到别的事务插入的数据的。因此，幻读在“当前读”下才会出现。


# 索引与排序

1. 索引：
    - 主键索引的叶子节点存的是整行数据。在 InnoDB 里，主键索引也被称为聚簇索引（clustered index）。
    - 非主键索引的叶子节点内容是主键的值。在 InnoDB 里，非主键索引也被称为二级索引（secondary index）。
    - 主键长度越小，普通索引的叶子节点就越小，普通索引占用的空间也就越小。
2. 覆盖索引：索引 k 已经“覆盖了”我们的查询需求，不再需要回表查整行记录，我们称为覆盖索引。
3. 最左前缀原则：最左前缀可以是联合索引的最左 N 个字段，也可以是字符串索引的最左 M 个字符。
4. 索引下推：可以在索引遍历过程中，对索引中包含的字段先做判断，直接过滤掉不满足条件的记录，减少回表次数。
5. 索引基数采样统计：InnoDB 默认会选择 N 个数据页，统计这些页面上的不同值，得到一个平均值，然后乘以这个索引的页面数，就得到了这个索引的基数。
6. 索引统计信息不准确导致的问题，以用 analyze table 来解决。
7. 字符串创建索引也可用前缀索引，定义好长度，就可以做到既节省空间，又不用额外增加太多的查询成本。前缀的区分度不够好的情况时：
    - 倒序存储。
    - 使用 hash 字段。
8. 全字段排序：
    - 初始化 sort_buffer，确定放入 name、city、age 这三个字段；
    - 从索引 city 找到第一个满足 city='杭州’条件的主键 id，也就是图中的 ID_X；
    - 到主键 id 索引取出整行，取 name、city、age 三个字段的值，存入 sort_buffer 中；
    - 从索引 city 取下一个记录的主键 id；
    - 重复步骤 3、4 直到 city 的值不满足查询条件为止，对应的主键 id 也就是图中的 ID_Y；
    - 对 sort_buffer 中的数据按照字段 name 做快速排序（可能在内存中完成，也可能需要使用外部排序（归并排序算法），这取决于排序所需的内存和参数 sort_buffer_size）；按照排序结果取前 1000 行返回给客户端。
9. rowid排序：如果 MySQL 实在是担心排序内存太小，会影响排序效率，才会采用 rowid 排序算法。
    - 初始化 sort_buffer，确定放入两个字段，即 name 和 id；
    - 从索引 city 找到第一个满足 city='杭州’条件的主键 id，也就是图中的 ID_X；
    - 到主键 id 索引取出整行，取 name、id 这两个字段，存入 sort_buffer 中；
    - 从索引 city 取下一个记录的主键 id；重复步骤 3、4 直到不满足 city='杭州’条件为止，也就是图中的 ID_Y；
    - 对 sort_buffer 中的数据按照字段 name 进行排序；遍历排序结果，取前 1000 行，并按照 id 的值回到原表中取出 city、name 和 age 三个字段返回给客户端。
10. order by rand() 使用了内存临时表，内存临时表排序的时候使用了 rowid 排序方法。
11. 如果临时表大小超过了 tmp_table_size，那么内存临时表就会转成磁盘临时表。
12. 对索引字段做函数操作，可能会破坏索引值的有序性，因此优化器就决定放弃走树搜索功能。可能导致全索引扫描。比如隐式类型转换、字符编码转换。
    - 隐式类型转换：当字符串与数字比较时，是字符串转成数字。
    - 字符集 utf8mb4 是 utf8 的超集，所以当这两个类型的字符串在做比较的时候，MySQL 内部的操作是，先把 utf8 字符串转成 utf8mb4 字符集，再做比较。

# 锁
1. 全局锁：
    - 命令是 Flush tables with read lock (FTWRL)。
    - 典型使用场景是，做全库逻辑备份。
2. 表级锁：有两种，表锁、元数据锁。
    - 元数据锁MDL不需要显式使用，在访问一个表的时候会被自动加上。
    - 当对一个表做增删改查操作的时候，加MDL读锁；当要对表做结构变更操作的时候，加MDL写锁。
3. 行锁：
    - 两阶段锁协议： 在InnoDB事务中，行锁是在需要的时候才加上的，但并不是不需要了就立刻释放，而是要等到事务结束时才释放。
4. 死锁：
    - 设置超时：innodb_lock_wait_timeout
    - 发起死锁检测：innodb_deadlock_detect=on
    - 死锁检测要耗费大量的 CPU 资源
    - 热点行更新导致的性能问题：控制并发度；通过将一行改成逻辑上的多行来减少锁冲突。
5. 间隙锁：产生幻读的原因是，行锁只能锁住行，但是新插入记录这个动作，要更新的是记录之间的“间隙”。因此，为了解决幻读问题，InnoDB 只好引入间隙锁 (Gap Lock)。
    - 跟间隙锁存在冲突关系的，是“往这个间隙中插入一个记录”这个操作。间隙锁之间都不存在冲突关系。
    - 间隙锁和行锁合称 next-key lock，每个 next-key lock 是前开后闭区间。
    - 间隙锁的引入，可能会导致同样的语句锁住更大的范围，这其实是影响了并发度的。
    - 间隙锁是在可重复读隔离级别下才会生效，需要把 binlog 格式设置为 binlog_format=row。
6. 加锁规则：
    - 原则 1：加锁的基本单位是 next-key lock。next-key lock 是前开后闭区间。
    - 原则 2：查找过程中访问到的对象才会加锁。
    - 优化 1：索引上的等值查询，给唯一索引加锁的时候，next-key lock 退化为行锁。
    - 优化 2：索引上的等值查询，向右遍历时且最后一个值不满足等值条件的时候，next-key lock 退化为间隙锁。
    - 一个 bug：唯一索引上的范围查询会访问到不满足条件的第一个值为止。
7. 锁是加在索引上的。
8. 以覆盖索引查找时，lock in share mode 只锁覆盖索引。for update 系统会认为你接下来要更新数据，因此会顺便给主键索引上满足条件的行加上行锁。


# 常见问题：
1. 崩溃后如何恢复：
2. 为什么会突然慢
3. 如何调优
4. 主从怎么实现的
5. 