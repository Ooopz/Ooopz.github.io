---
tags: 
- 运维/配置
---

# 系统初始化

## 1. 换源

```bash
echo "
# ubuntu20.04-aliyun
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
" | sudo tee /etc/apt/sources.list
```

顺带更新

```bash
sudo apt update
sudo apt upgrade -y
```

## 2 安装数据库

这里安装 clickhouse 和 mysql，clickhouse 性能够强，mysql 是最常见的关系型数据库，有这两个就够用了

```bash
sudo apt install -y apt-transport-https ca-certificates dirmngr
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv E0C56BD4
echo "deb https://repo.clickhouse.tech/deb/stable/ main/" | sudo tee /etc/apt/sources.list.d/clickhouse.list
sudo apt update
sudo apt install -y clickhouse-server clickhouse-client
```

```bash
sudo apt install mysql-server -y
```

安装完成后启动服务

```bash
sudo service clickhouse-server start
sudo service mysql start
```

看一下端口占用判断服务起来没，如果 3306 和 8123 被占用了，说明服务正常

```bash
ss -tunlp
```

## 3 安装 miniconda

下载后运行，根据提示操作，注意安装的目录
从 [清华镜像站](https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/?C=M&O=D) 里挑一个你想要的版本，替换 wget 后的链接

```bash
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash ./Miniconda3-latest-Linux-x86_64.sh
```

换源以及简单配置一下

```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
conda config --set show_channel_urls true
conda config --set auto_activate_base false
```

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
```

再顺便按个人喜好添加点快捷命令

```bash
echo "
# alias of usual command
alias ca='conda activate'
alias cda='conda deactivate'
alias jl='jupyter lab'
" | sudo tee -a .bashrc
```

```bash
source .bashrc
```

## 4 wsl2 使用

添加宿主机代理，此处的 1080 改成自己的代理端口

```bash
echo "

# commamd of proxy
export HOSTIP=\$(cat /etc/resolv.conf |grep -oP '(?<=nameserver\ ).*')
alias proxy='
    export https_proxy=\"socks5://\${HOSTIP}:1080\";
    export http_proxy=\"socks5://\${HOSTIP}:1080\";
    export all_proxy=\"socks5://\${HOSTIP}:1080\";
'
alias unproxy='
    unset https_proxy;
    unset http_proxy;
    unset all_proxy;
'
" | tee -a .bashrc
```

设置 wsl2 默认浏览器为 edge

```bash
sudo ln /mnt/c/Program\ Files\ \(x86\)/Microsoft/Edge/Application/msedge.exe /usr/bin/msedge -s
sudo ln /usr/bin/msedge /usr/bin/gnome-www-browser -s
sudo rm /usr/bin/x-www-browser
sudo ln /usr/bin/msedge /usr/bin/x-www-browser -s
```
