---
tags: 
- clickhouse
---

# Clickhouse 日志表清理

clickhouse 数据库中有两个日志表 `system.query_log` 和 `system.query_thread_log`，如果不处理的话会占用大量空间。

清理方法有三种：

## 1. 设置 TTL 时间

这种方法不需要重启 clickhouse 服务。

```sql
ALTER TABLE system.query_log MODIFY TTL event_date + toIntervalMonth(1);
```

```sql
ALTER TABLE system.query_thread_log MODIFY TTL event_date + toIntervalMonth(1);
```

需要注意的是 clickhouse 的 TTL 是惰性的，数据过期后不会马上被删除，通过 `optmize table query_log` 可以主动触发 TTL。

## 2. 手动删除表分区

这种方法也无需重启服务器，但只是治标不治本，

```sql
SELECT partition 
FROM system.parts 
WHERE database='system' AND table = 'query_log' 
GROUP BY partition 
ORDER BY partition DESC;

ALTER TABLE system.query_log DROP partition '202112';
```

```sql
SELECT partition 
FROM system.parts 
WHERE database='system' AND table = 'query_thread_log' 
GROUP BY partition 
ORDER BY partition DESC;

ALTER TABLE system.query_thread_log DROP partition '202112';
```

需要注意的是 clickhouse 对删除的单表大小有限制（默认 50GB）,可以通过创建 `/var/lib/clickhouse/flags/force_drop_table` 文件后再强制执行删除，这种方法无需重启服务，`force_drop_table` 文件会在强制删表分区后除后被删掉。

## 3. 修改配置文件

这种方法需要重启 clickhouse 服务。

配置文件的路径为 `/etc/clickhouse-server/config.xml` ，可以根据 [query_log 配置说明](https://clickhouse.com/docs/en/operations/server-configuration-parameters/settings/#server_configuration_parameters-query-log) 和 [query_thread_log配置说明](https://clickhouse.com/docs/en/operations/server-configuration-parameters/settings/#server_configuration_parameters-query_thread_log) 对文件进行配置。注意`<partition_by>XXX</partition_by>` 和 `<engine>XXX</engine>` 两个参数无法同时生效。

配置文件示例：

```xml
<query_log>
    <database>system</database>
    <table>query_log</table>
    <engine>Engine = MergeTree PARTITION BY event_date ORDER BY event_time TTL event_date + INTERVAL 30 day</engine>
    <flush_interval_milliseconds>7500</flush_interval_milliseconds>
</query_log>
```

```xml
<query_thread_log>
    <database>system</database>
    <table>query_thread_log</table>
    <partition_by>toMonday(event_date)</partition_by>
    <flush_interval_milliseconds>7500</flush_interval_milliseconds>
</query_thread_log>

```
