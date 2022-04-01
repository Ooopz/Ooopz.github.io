---
tags: 
- 运维/配置
---

# Ubuntu配置shadowsocks-libev

## 0 简单版

```bash
apt install shadowsocks-libev -y 
nohup ss-server -s 0.0.0.0 -p 65534 -l 8388 -k 123456 -m chacha20-ietf-poly1305 &
```

服务端口  65534， 本地端口 8388，密码 123456，加密方式 chacha20-ietf-poly1305

## 1 安装

Ubuntu 下直接 apt 安装，注意权限不够则命令前加 sudo：

```bash
apt install shadowsocks-libev
```

其他系统没有包可以手动编译

## 2 配置文件修改

### 2.1 服务配置

修改服务配置文件:

```bash
vim /etc/shadowsocks-libev/config.json
```

复制粘贴到文件中

```json
{
    "server":"0.0.0.0",
    "server_port":65534,
    "local_port":1080,
    "password":"123456",
    "timeout":60,
    "method":"chacha20-ietf-poly1305",
    "fast_open": true
}
```

### 2.2 启动文件

创建 Shadowsocks-libev.service 配置文件用于 systemctl 控制：

```bash
vim /etc/systemd/system/shadowsocks-libev.service
```

复制粘贴到文件中

```yaml
[Unit]
Description=Shadowsocks-libev Server
After=network.target

[Service]
Type=simple
ExecStartPre=/bin/sh -c 'ulimit -n 51200'
ExecStart=/usr/local/bin/ss-server -c /etc/shadowsocks-libev/config.json -u
Restart=on-abort

[Install]
WantedBy=multi-user.target
```

### 2.3 优化吞吐量

新建配置文件：

```bash
vim /etc/sysctl.d/local.conf
```

复制粘贴：

```yaml
#max open files
fs.file-max = 51200
#max read buffer
net.core.rmem_max = 67108864
#max write buffer
net.core.wmem_max = 67108864
#default read buffer
net.core.rmem_default = 65536
#default write buffer
net.core.wmem_default = 65536
#max processor input queue
net.core.netdev_max_backlog = 4096
#max backlog
net.core.somaxconn = 4096
#resist SYN flood attacks
net.ipv4.tcp_syncookies = 1
#reuse timewait sockets when safe
net.ipv4.tcp_tw_reuse = 1
#turn off fast timewait sockets recycling
net.ipv4.tcp_tw_recycle = 0
#short FIN timeout
net.ipv4.tcp_fin_timeout = 30
#short keepalive time
net.ipv4.tcp_keepalive_time = 1200
#outbound port range
net.ipv4.ip_local_port_range = 10000 65000
#max SYN backlog
net.ipv4.tcp_max_syn_backlog = 4096
#max timewait sockets held by system simultaneously
net.ipv4.tcp_max_tw_buckets = 5000
#turn on TCP Fast Open on both client and server side
net.ipv4.tcp_fastopen = 3
#TCP receive buffer
net.ipv4.tcp_rmem = 4096 87380 67108864
#TCP write buffer
net.ipv4.tcp_wmem = 4096 65536 67108864
#turn on path MTU discovery
net.ipv4.tcp_mtu_probing = 1

net.ipv4.tcp_congestion_control = bbr
```

运行：

```bash
sysctl --system
```

编辑配置文件 limits.conf

```bash
vim /etc/security/limits.conf
```

在文件结尾添加两行：

```yaml
* soft nofile 51200
* hard nofile 51200
```

### 2.4 开启 Google BBR

运行 `lsmod | grep bbr`，如果结果中没有 `tcp_bbr`，则先运行：

```bash
modprobe tcp_bbr  
echo "tcp_bbr" >> /etc/modules-load.d/modules.conf
```

运行：

```bash
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf  
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
```

运行：

```bash
sysctl -p
```

保存生效。运行：

```bash
sysctl net.ipv4.tcp_available_congestion_control
sysctl net.ipv4.tcp_congestion_control
```

若均有 bbr，则开启 BBR 成功。

## 3 启动

启动 Shadowsocks：

```bash
systemctl start shadowsocks-libev
```

设置开机启动

```bash
systemctl enable shadowsocks-libev
```
