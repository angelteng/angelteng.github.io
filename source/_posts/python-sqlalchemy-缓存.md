---
title: python sqlalchemy 缓存
date: 2019-04-01 11:34:42
tags:
- Python
category: Python
---
描述：
    在同一个会话中，使用两次同样的sql查询，即使数据改变了，返回的值相同。

## 原因一：数据库的事务隔离
在数据库系统中，事务隔离级别(isolation level)决定了数据在系统中的可见性。隔离级别从低到高分为四种：未提交读(Read uncommitted)，已提交读(Read committed)，可重复读(Repeatable read)，可串行化(Serializable)。他们的区别如下表所示。

| 隔离级别   | 脏读 | 不可重复读 | 幻读 |
| :-------- | --- | -------- | ------|
|未提交读(RU)| 可能 |	可能	 |可能 |
|已提交读(RC)| 不可能|	可能	 |可能  |
|可重复读(RR)| 不可能|	不可能	 |可能  |
|可串行化	 | 不可能|	不可能	 |不可能 |

对于MySQL来说，默认的事务隔离级别是RR，RR是可重复读的，因此可以解释这个现象。

## 原因二：Sqlaalchemy的会话隔离
看作者在stackoverflow的回答：
“
The usual cause for people thinking there's a "cache" at play, besides the usual SQLAlchemy identity map which is local to a transaction, is that they are observing the effects of transaction isolation. SQLAlchemy's session works by default in a transactional mode, meaning it waits until session.commit() is called in order to persist data to the database. During this time, other transactions in progress elsewhere will not see this data.

However, due to the isolated nature of transactions, there's an extra twist. Those other transactions in progress will not only not see your transaction's data until it is committed, they also can't see it in some cases until they are committed or rolled back also (which is the same effect your close() is having here). A transaction with an average degree of isolation will hold onto the state that it has loaded thus far, and keep giving you that same state local to the transaction even though the real data has changed - this is called repeatable reads in transaction isolation parlance.
”
SQLAlchemy的会话默认在事务模式下工作，这意味着它会等到调用session.commit()才将数据持久保存到数据库中。
由于事务的隔离性，正在进行的其他事务在提交之前不仅不会看到这个事务的数据，在它们被提交或回滚之前它们也无法在某些情况下看到它，这在事务隔离用语中称为可重复读取。

## 解决方法
在MySQL的同一个事务中，多次查询同一行的数据得到的结果是相同的，这里既有SQLAlchemy本身“缓存”结果的原因，也受到数据库隔离级别的影响。如果要强制读取最新的结果，最简单的办法就是在查询前手动COMMIT一次。（commit不仅把所有本地修改写入到数据库，同时也提交了该事务）

参考：
[https://www.jianshu.com/p/c0a8275cce99](https://www.jianshu.com/p/c0a8275cce99)
[https://stackoverflow.com/questions/10210080/how-to-disable-sqlalchemy-caching](https://stackoverflow.com/questions/10210080/how-to-disable-sqlalchemy-caching)
[https://stackoverflow.com/questions/12108913/how-to-avoid-caching-in-sqlalchemy](https://stackoverflow.com/questions/12108913/how-to-avoid-caching-in-sqlalchemy)


