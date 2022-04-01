---
tags: 
- 运维/配置
---

# 配置 so 文件

## 1. 加入到环境变量

修改系统文件 `/etc/ld.so.conf`，添加路径，运行 `ldconfig` 命令

或在 `/etc/ld.so.conf.d` 目录下新建一个 conf 文件，其中保存目录，再运行 `ldconfig` 命令

## 2. 查看 so 文件函数
1.  `nm -D XXX.so`
2.  `objdump -tT  XXX.so`
