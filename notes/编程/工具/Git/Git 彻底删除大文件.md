---
tags: 
- Git
---

# Git 彻底删除大文件

## 0. Intro

网上能搜到的资料大部分都是通过 git filter-branch 删除文件，不仅速度慢，还容易出问题，现在官方在使用 git filter-branch 时推荐 git filter-repo，因此尝试一下官方推荐的方法。

## 1. 安装 git-filter-repo

 [git-filter-repo 安装指南](https://github.com/newren/git-filter-repo/blob/main/INSTALL)

这里选择通过 pip 安装，windows 需要手动安装 python 或者 conda

```bash
pip install git-filter-repo
```

## 2. 找出要删除的大文件

按照文件大小升序排列并取最后 40 个文件

```bash
git rev-list --objects --all | grep "$(git verify-pack -v .git/objects/pack/*.idx | sort -k 3 -n | tail -40 | awk '{print$1}')"
```

注意嵌套语句会导致排序错乱，可以拆开逐个寻找文件
```bash
git verify-pack -v .git/objects/pack/*.idx | sort -k 3 -n | tail -40
git rev-list --objects --all | grep 文件对应的id
```

## 3. 彻底删除大文件

 [git-filter-repo 说明文档](https://htmlpreview.github.io/?https://github.com/newren/git-filter-repo/blob/docs/html/git-filter-repo.html)

由于之前不小心上传了大量 csv 文件，因此使用正则匹配将所有 csv 文件删除

```bash
git filter-repo --force --invert-paths --path-regex .+\.csv
```

## 4. 强制推送到远端

由于修改了历史的 commit，因此仓库无法正常推送到远端，需要进行强制推送

```bash
git push -f origin master
```

## 5. 额外说明
以上命令都是在 linux 下，如果使用 windows 系统的话，可以先通过 conda 安装 git-filter-repo，再通过 git 自带的 MINGW 运行linux风格命令，最后通过 conda 运行 `git filter-repo`
