

首先介绍我的环境，ubuntu20.4 Anaconda3,

最近搞机器学习，jupyter notebook 画个决策树没有包graphviz 。。。

然后   安装graphviz     $   conda install graphviz

**问题：**报错（网上很多类似的安装指令变来变去都如下报错误）

Collecting package metadata (current_repodata.json): doneSolving environment: failed with initial frozen solve. Retrying with flexible solve.Solving environment: failed with repodata from current_repodata.json, will retry with next repodata source.Collecting package metadata (repodata.json): / - failed

CondaError: KeyboardInterrupt

尝试了在Anaconda里边安装，速度很慢，

更换了下载源依然很慢，

！！！（估计是有什么问题）

**解决方法** 查阅资料   graphviz   适用最高版本python3.6

方法（1）把 conda 的python版本降级（缺点：一些包的版本过高，需要重装）

```bash
conda install python=3.6.10```


方法（2）创建虚拟环境

## 我是用的方法二  （缺点：很多包需要重新在虚拟环境安装）

在Anaconda 创建了虚拟环境，选择python3.6

打开Anaconda ----终端输入指令

```bash
anaconda-navigator```


 

再安装graphviz  一分钟安装成功！！！

那么能不能用？ 当让不可以了

需要终端安装一个插件，指令如下，目的是为了使用jupyter时能选择刚刚创建的虚拟环境，，

```bash
conda install nb_conda```


输入y  然后enter 即可  ，安装结束，我们打开jupyter notebook

```bash
jupyter notebook```



![./figures/8e76dd8358a14fdb88a2f2c8b95975d5.png](./figures/8e76dd8358a14fdb88a2f2c8b95975d5.png)


画的决策树，，




![./figures/935c303f141a47269e9112189dddcd9d.png](./figures/935c303f141a47269e9112189dddcd9d.png)


 

 

到此结束了；我安装了三个包  scikit-learn, numpy, matplotlib 目前够用后边缺啥装啥。



虚拟环境安装包的指令（不需要进入虚拟环境）

conda install -n 环境名 包名

例如： conda install -n ml scikit-learn



如果jupyter notebook 新建   ** 没有虚拟环境**，可以尝试安装  ipykernel

在base和新建的虚拟环境都要装，不懂的执行一遍命令就行！！

```bash
conda install ipykernel
conda install -n 环境名 ipykernel
```


### 扩展一些指令：


```bash
#创建虚拟环境
conda create -n your_env_name python=X.X（3.6、3.7等）
 
#激活虚拟环境
source activate your_env_name(虚拟环境名称)
conda activate your_env_name(虚拟环境名称) （新的）
 
#退出虚拟环境
source deactivate your_env_name(虚拟环境名称)
conda deactivate 
 
#删除虚拟环境
conda remove -n your_env_name(虚拟环境名称) --all
 
#查看安装了哪些包
conda list
 
#安装包
conda install package_name(包名)
conda install scrapy==1.3 # 安装指定版本的包
conda install -n 环境名 包名 # 在conda指定的某个环境中安装包
 
#查看当前存在哪些虚拟环境
conda env list 
#或 
conda info -e
#或
conda info --envs
 
#检查更新当前conda
conda update conda
 
#更新anaconda
conda update anaconda
 
#更新所有库
conda update --all
 
#更新python
conda update python```




#   希望对你们有帮助，有问题的可以私聊或者评论，本人每天都看，乐意提供帮助！！

