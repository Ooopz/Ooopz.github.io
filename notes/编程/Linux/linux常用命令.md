---
tags: 
- 运维/命令
---

# linux常用命令

## netstat -nat 和 ss -nat

`netstat -nat` 和 `ss -nat` 两个命令都可以查看系统的TCP连接，但是 `ss -nat` 的速度优于 `netstat -nat`

## tar

常用命令：

| 参数 | 说明                                                                                                           |
| ---- | -------------------------------------------------------------------------------------------------------------- |
| `-x` | 从档案文件中**释放**文件。                                                                                     | 
| `-c` | **创建**新的档案文件。如果用户想备份一个目录或是一些文件，就要选择这个选项。                                   |
| `-r` | 把要存档的文件追加到档案文件的末尾。                                                                           |
| `-t` | 列出档案文件的内容，查看已经备份了哪些文件。                                                                   |
| `-u` | 更新文件。就是说，用新增的文件取代原备份文件，如果在备份文件中找不到要更新的文件，则把它追加到备份文件的最后。 |
| `-j` | 代表使用‘bzip2’程序进行文件的压缩(tar.bz2)。                                                                   |
| `-z` | 用gzip来压缩/解压缩文件(tar.gz)。                                                                              |
| `-v` | 详细报告tar处理的文件信息。如无此选项，tar不报告文件信息。                                                     |
| `-b` | 该选项是为磁带机设定的，其后跟一数字，用来说明区块的大小，系统预设值为20（20×512 bytes）。                     |
| `-f` | 使用档案文件或设备，这个选项通常是必选的。                                                                     |
| `-k` | 保存已经存在的文件。例如把某个文件还原，在还原的过程中遇到相同的文件，不会进行覆盖。                           |
| `-m` | 在还原文件时，把所有文件的修改时间设定为。                                                                     |
| `-M` | 创建多卷的档案文件，以便在几个磁盘中存放。                                                                     |
| `-w` | 每一步都要求确认。                                                                                             |

```bash
# 解压
tar -zxvf targetFile.tar targetFolder/
```

```bash
# 压缩
tar -zcvf targetFile.tar targetFolder/
```

## docker

通过 docker 启动 rabbitmq

```bash
docker run -d --name rabbitmq -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin -e RABBITMQ_DEFAULT_VHOST=airflow_mq -p 15672:15672 -p 5672:5672 rabbitmq:management
```
