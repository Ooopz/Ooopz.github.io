---
tags: 
- clickhouse
---

# Clickhouse 基础配置

## 1. 开启 RBAC

clickhouse 支持 RBAC 权限管理，要开启功能需要先修改配置文件

首先打开 `/etc/clickhouse-server/users.xml` 在默认账号 default 配置中增加 access_management 配置项，然后重启 clickhouse 服务，在用 default 账号创建完成超级管理员账号后，推荐在配置文件中注释掉 default 账号。
```xml
<users>
    <default>
        <access_management>1</access_management>
    </default>
</users>
```

## 2. 创建用户以及角色

 [创建用户](https://clickhouse.com/docs/en/sql-reference/statements/create/user/)
```sql
CREATE USER 'read' IDENTIFIED WITH sha256_password by '940527';  
CREATE USER 'dba' IDENTIFIED WITH sha256_password by '700712';
```

 [添加角色](https://clickhouse.com/docs/en/sql-reference/statements/create/role)
```sql
CREATE ROLE READ_ONLY;  
CREATE ROLE DBA;
```

 [授予权限](https://clickhouse.com/docs/en/sql-reference/statements/grant/)
```sql
GRANT SELECT ON *.* TO READ_ONLY WITH GRANT OPTION;  
GRANT ALL ON *.* TO DBA WITH GRANT OPTION;
```

 [将角色赋予用户](https://clickhouse.com/docs/en/sql-reference/statements/grant/)
```sql
GRANT READ_ONLY TO 'read';  
GRANT DBA TO 'dba';
```
