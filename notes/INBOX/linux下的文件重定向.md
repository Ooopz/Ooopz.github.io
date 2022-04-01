---
tags:
- linux
- 待整理
---

# linux下的文件重定向

## 前言：

所以说学习没有捷径，那些"速成"的东西只是暂时的绕开了你“终归绕不开”的问题而已。

在你上来就跟着速成材料写着 "2>/dev/null"的时候，实际上你至少绕开了这样几个知识点：

1.  File descriptor
2.  Stdin, stdout, stderr
3.  Shell redirection
4.  Duplicate file descriptor

...(还有根多关联知识)

## 正文：

-   **File descriptor**

首先什么是File descriptor（简称fd），这是Linux系统或者说很多类Unix系统上的一个概念，而其它操作系统上也有类似的概念，只是可能不叫这个名字。本来文件描述符的概念可能是一个初学者在学习完编程语言（如C语言）后，学习一本叫《[unix高级环境编程](https://www.zhihu.com/search?q=unix%E9%AB%98%E7%BA%A7%E7%8E%AF%E5%A2%83%E7%BC%96%E7%A8%8B&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A2304247674%7D)》(俗称《APUE》)的书的时候首次接触到的（当然你也可能是学习别的类似的书），但是如果你说你是在《[深入理解Linux内核](https://www.zhihu.com/search?q=%E6%B7%B1%E5%85%A5%E7%90%86%E8%A7%A3Linux%E5%86%85%E6%A0%B8&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A2304247674%7D)》里第一次接触到的，那我只能表示小伙子你跨度稍微有点大，但是这不重要，只要你都看得懂这不妨碍你将来成为大师的脚步。

言归正传，一般人第一次了解[文件描述符](https://www.zhihu.com/search?q=%E6%96%87%E4%BB%B6%E6%8F%8F%E8%BF%B0%E7%AC%A6&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A2304247674%7D)可能是从Linux的open系统调用开始的，因为这大概是Linux系统中最常见最常用的一个能让你得到一个文件描述符的系统调用。比如常见的：

```text
int fd;
fd = open(pathname, O_RDWR);
```

如果open没有返回错误，那么这个时候你就得到了一个文件描述符。如果更准确的说，是你当前的进程创建了一个文件描述符来追踪你刚刚open的pathname。从数据类型上看，一个文件描述符似乎就是一个整数，更确切的说是一个大于等于0的整数。为什么一个整数可以代表一个打开的文件？因为一般情况下（使用CLONE_FILES/CLONE_FS等的情况除外）Linux内核为每个进程创建一个fdtable，参考linux/fdtable.h中的files_struct结构：

```c
/*                                                                                                                                                                                             
 * Open file table structure                                                                                                                                                                   
 */
struct files_struct {
  /*                                                                                                                                                                                           
   * read mostly part                                                                                                                                                                          
   */
        atomic_t count;
        bool resize_in_progress;
        wait_queue_head_t resize_wait;

        struct fdtable __rcu *fdt;
        struct fdtable fdtab;
  /*                                                                                                                                                                                           
   * written part on a separate cache line in SMP                                                                                                                                              
   */
        spinlock_t file_lock ____cacheline_aligned_in_smp;
        unsigned int next_fd;
        unsigned long close_on_exec_init[1];
        unsigned long open_fds_init[1];
        unsigned long full_fds_bits_init[1];
        struct file __rcu * fd_array[NR_OPEN_DEFAULT];
};
```

每个进程的task_struct结构中有一个files成员，指向进程相关的文件描述符表：

```c
struct task_struct {
...
        /* Open file information: */
        struct files_struct             *files;
...
}
```

当然，作为初学者不需要深入到这么多，只需要知道每个进程有一个文件描述符表，而文件描述符就是这个表的索引值，所以它才是个整数，因为它就相当于数组下标。而每个文件描述符对应的表项都可以追溯到这个文件所在文件系统的具体信息（参考struct file结构等）。所以当你打开一个文件时不是只创建了一个整数值，而是创建了很多进程和文件系统之间的关联数据，然后把这些数据保存在一个表里，最后只给你返回一个表的索引值，我们通常管索引值叫文件描述符。

-   **Stdin, stdout, stderr**

上面我们知道每个进程都有一个文件描述符表，记录了这个进程打开的文件（或输入输出资源，因为Linux里有一切皆文件的概念，所以我们就都统称为文件了）。文件描述符的数值和文件之间一般是没有必然关系的，同一个文件每次打开都不一定得到同一个数值。但是其中有三个特别的文件描述符是固定的，它们就是0, 1和2。这三个值分别对应标准输入(standard input，简称stdin)，标准输出(standard output，简称stdout)和标准错误(standard error，简称stderr)。在Linux系统上，一个进程在创建的时候，一般就默认初始化这三个文件描述符，并给它们固定的数值，所以0肯定是只标准输入，1肯定是指标准输出，2肯定是标准错误。

那什么是标准输入、标准输出和标准错误呢？在原始的理解上，对于计算机来说，键盘输入就是标准输入，显示器输出就是标准输出，而标准错误也是一个输出，它和标准输出在表现形式上差不多，但是它是一个可以和标注输出分开操作（如重定向）的输出，一般专门用来输出错误信息提示。在现代计算机上，标准输入、标准输出和标准错误被进行了抽象，比如在交互式的shell上它们可能都指向字符终端，通过字符终端输入、输出等：

```text
$ ls -l /proc/$$/fd
total 0
lrwx------. 1 test test 64 Jan  9 16:39 0 -> /dev/pts/7
lrwx------. 1 test test 64 Jan  9 16:39 1 -> /dev/pts/7
lrwx------. 1 test test 64 Jan  9 16:39 2 -> /dev/pts/7
```

但是这并不影响你对它们的理解。如果说的更直接一点，你在用scanf和printf写C语言程序的时候，比如：

```c
#include <stdio.h>

int main()
{
        char str[128];
        scanf("%s", str);
        printf("stdout: %s\n", str);
        fprintf(stderr, "stderr: %s\n", str);
        return 0;
}
```

编译执行如下：

```text
$ gcc -o mytest mytest.c -Wall
$ ./mytest 
hello
stdout: hello
stderr: hello
```

在执行之初，程序会先停在scanf处等待输入，我输入了一个"hello"，所以第一个hello是我手敲到终端上的输入数据，而第二个"hello"是程序接收了我输入的数据后输出到终端上来的，第三个"hello"也是程序输出到终端上来的，表现形式上和第二个一样，但实际上它们是两个不同的输出流，只是都流到了终端上而已。

在这个初学者也能看懂的例子里，scanf就是在从标准输入接受的"hello"，而printf就是把"hello"写到了标准输出，fprintf(stderr, ...)就是把"hello"写到标准错误。而样子就是你们看到的，这就是标准输入、标准输出和标准错误。

-   **Shell redirection**

上面我们知道了文件描述符的概念，接下来就要引入一个概念叫"Redirection（重定向）"。Redirection是Shell中常见的概念，而不是Linux内核里的，甚至也不是C标准库里的概念。它是Shell（比如bash）提出来的概念，它“重定向”的就是文件描述符。

比如标准输入(0)默认对应的是终端输入，但是你可以利用bash的重定位语法，将标准输入重定向到一个普通文件，比如还是上面的程序，本来我们是通过终端上手动输入"hello"来把数据给标准输入，现在我们想办法通过一个文件来做一下：

```text
$ echo hello >ifile
$ ./mytest <ifile
stdout: hello
stderr: hello
```

可以看到这次没有用我手动从终端输入"hello"，因为我将标准输入重定向到了ifile这个文件中，这样mytest进程就直接读取ifile的内容作为标准输入的内容了。

而这里面用到的shell（bash）语法就是：

```text
[n]<word
```

它的作用就是当前进程想要读取文件描述符n的时候，这个输入流的源点将被重定位到word所代表的文件上。而中括号一般表示可选项，说明n是可选的，如果你写了就是指定一个文件描述符的数值，如果你不写就使用默认值，默认值是0，也就是标准输入。

同理，我既然可以重定向输入，我也可以重定向输出：

```text
$ ./mytest >ofile 2>efile
hello
$ cat ofile
stdout: hello
$ cat efile
stderr: hello
```

这里用到的语法是：

```text
[n]>[|]word
```

这里的"|"我这里不想解释，因为它不会影响重定向输出的语义，它只是涉及"override noclobber"的问题，解释起来要稍微偏题了，而且我不想单纯做一个文档的翻译机，请还不会的读者去翻看bash的manual（我后面也会贴出来）。我们只着重讨论重定向输出的问题，所以[n]>word的意思就是当前进程对文件描述符的输出流重定向到word所代表的文件。同样n是可选项，默认是1，也就是标准输出。所以上面我们才将上面"1>ofile 2>efile"里的"1"省略了，但是不影响程序执行的意思，我们也可以看到本来应该输出到终端上的标准输出和标准错误被分别输出到了两个文件里。

当然，关于重定向还有很多语法上的变化，具体请自己阅读bash的手册中Redirections部分：

[bash#Redirections​www.gnu.org/software/bash/manual/bash.html#Redirections](https://link.zhihu.com/?target=https%3A//www.gnu.org/software/bash/manual/bash.html%23Redirections)

我还是那句话，单纯的翻译机我不想做，世界上最远的距离就是，权威的文档就在你的眼前时，你却非要绕开去从不名来源的地方各种道听途说。这说明你离你想掌握的东西还相去很远。

言归正传，我们上面说重定向是shell里的概念，那这个概念对应Linux的什么系统调用呢？

-   **Duplicate file descriptor**

上面我们知道了文件描述符的概念，也解释了shell中的重定向操作。接下来我们就说一下重定向是怎么做到的。当我们得到一个文件描述符，我们可以的操作有很多，比如常见的read(fd, ...)/write(fd, ...)/fchmod(fd, ...)/fcntl(fd, ...)等。但是有一个操作（系统调用）比较特别，叫dup(), dup2()等。它的作用是Duplicate一个文件描述符，通俗理解就是拷贝得到一个文件描述符的副本。

```text
DUP(2)                                                                           Linux Programmer's Manual                                                                          DUP(2)

NAME
       dup, dup2, dup3 - duplicate a file descriptor

SYNOPSIS
       #include <unistd.h>

       int dup(int oldfd);
       int dup2(int oldfd, int newfd);

DESCRIPTION
       The dup() system call creates a copy of the file descriptor oldfd, using the lowest-numbered unused file descriptor for the new descriptor.
...
       The dup2() system call performs the same task as dup(), but instead of using the lowest-numbered unused file descriptor, it uses the file descriptor number specified in newfd. If
       the file descriptor newfd was previously open, it is silently closed before being reused.
...
```

比如dup(oldfd)，就是从文件描述符表中找到最小的一个还没有用到的文件描述符（文件描述符一般从0向上分配），然后将文件描述符oldfd拷贝一份到新的文件描述符上。也就是说这时你得到了两个索引值不同但是指向目标相同的文件描述符。

注意这里是duplicate，不是move，所以dup后相当于一式两份。比如我想对上面程序的标准错误做一次duplication，让另一个文件描述符也指向标准错误的输出位置，我可以这样：

```text
#include <stdio.h>
#include <unistd.h>

int main()
{
        char str[128];
        scanf("%s", str);
        printf("stdout: %s\n", str);

        int copy_fd;
        copy_fd = dup(2);
        fprintf(stderr, "stderr: %s\n", str);
        dprintf(copy_fd, "copy_fd:%d: %s\n", copy_fd, str);
        return 0;
}
```

执行测试：

```text
$ ./mytest 
hello
stdout: hello
stderr: hello
copy_fd:3: hello
```

前面的都一样，最后一个"hello"就是dup(2)那行等到一个文件描述符2的副本，我们看到这个副本的文件描述符是3，操作文件描述符2或者3相当于操作同一个文件（在本例中都是输出终端）

而dup2(oldfd, newfd)和dup(oldfd)的区别就是你可以手动指定一个文件描述符newfd，将oldfd拷贝（/覆盖）到newfd上，同时如果newfd是打开(open)状态的，则会被默默的关掉(close)。这个dup2()系统调用是很常用的，也是实现“重定向”的一个“主要”手段。比如我修改上面的C语言程序，不借助Shell的重定向语法，直接用dup2()系统调用实现">ofile"这个功能：

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int main()
{
        char str[128];
        scanf("%s", str);

        int fd;
        fd = open("ofile", O_WRONLY|O_TRUNC|O_CREAT, 0644);
        if (fd < 0) {
                perror("open");
                return 1;
        }
        if (dup2(fd, 1) < 0) {
                perror("dup2");
                return 2;
        }
        printf("stdout: %s\n", str);
        fprintf(stderr, "stderr: %s\n", str);
        return 0;
}
```

执行:

```text
$ ./mytest 
hello
stderr: hello
$ cat ofile
stdout: hello
```

可以看到我没用使用">ofile"，但是./mytest的执行结果中输出到标准输出的内容没有输出到终端，而是输出到了ofile这个文件里了。

原因就是我们首先通过open("ofile")得到一个指向ofile的文件描述符fd，然后我们通过dup2(fd, 1)将ofile的文件描述符duplicate到文件描述符1上（这实际上相当于覆盖了文件描述符1），这样文件描述符1和fd就都指向ofile文件了，然后再用printf向标准输出输出数据时，就被输出到了ofile文件中。

如果你还是有所怀疑，我们可以用strace实际追踪一下"./mytest >ofile"的执行过程：

```text
$ strace -o log ./mytest >ofile
hello
stderr: hello
$ less log
...
read(0, "hello\n", 1024)                = 6
openat(AT_FDCWD, "ofile", O_WRONLY|O_CREAT|O_TRUNC, 0644) = 3
dup2(3, 1)                              = 1
write(2, "stderr: hello\n", 14)         = 14
write(1, "stdout: hello\n", 14)         = 14
...
```

由于输出较多，我们只关注重要的这几行，可以看到"./mytest >ofile"在执行的时候实际上是：

```text
read(0, "hello\n", 1024)                = 6
```

从标准输入（0），读取“hello\n”，实际读取了6个字符。

```text
openat(AT_FDCWD, "ofile", O_WRONLY|O_CREAT|O_TRUNC, 0644) = 3
```

打开ofile文件，得到文件描述符3.

```text
dup2(3, 1)                              = 1
```

将文件描述符3（就是上面打开ofile时得到的文件描述符）拷贝到文件描述符1的位置，也就是文件描述符1（标准输出）现在指向了文件描述符3对应的文件ofile。

```text
write(2, "stderr: hello\n", 14)         = 14
```

向标准错误(2)写入"stderr: hello\n"，由于我们没有重定向标准错误，所以这个内容还是输出到终端上。

```text
write(1, "stdout: hello\n", 14)         = 14
```

向标准输出（1）写入"stdout: hello\n"，由于我们用dup2()将标准输出重定向到了ofile，所以这个字符串没有显示在终端上，而是出现在了ofile文件里（如上面的执行结果）。

-   **题外话：/dev/null**

鉴于题目特别问了/dev/null，我就稍微说一下。如果你只是想快速的理解一下，那/dev/null就是Linux内核创建的一个字符设备，也是一个文件。所以你可以open它得到文件描述符，基于上面我对文件描述符的各种说明，你应该能知道2>/dev/null就是：

```text
fd = open(/dev/null, ...);
dup2(fd, 2);
```

的意思，也就是将/dev/null替换为标准错误的目标文件。而这个/dev/null是一个几乎不管向它写入什么，都只返回成功，但是什么都没真的写入的文件。换句话说就是个“无底洞”，扔进去的东西肯定算扔进去了，但是扔进去就看不见了。

如果你特别感兴趣它是怎么做到的，可以去看linux/drivers/char/mem.c这个文件（里面也有/dev/zero等文件的实现）。通过它的file operations的定义我们可以看到它支持的操作，以及实现：

```text
static const struct file_operations null_fops = {
        .llseek         = null_lseek,
        .read           = read_null,
        .write          = write_null,
        .read_iter      = read_iter_null,
        .write_iter     = write_iter_null,
        .splice_write   = splice_write_null,
};
```

比如为什么写进去只返回成功，什么也没发生，可以参考其write操作所对应的write_null函数实现：

```text
static ssize_t write_null(struct file *file, const char __user *buf,
                          size_t count, loff_t *ppos)
{
        return count;
}
```

看了之后就是这样，就一个return语句。如果你理解write系统调用:

```text
ssize_t write(int fd, const void *buf, size_t count);
```

你看到这个函数应该就能很轻易的明白它的意思了，因为它根本没有处理来自用户传入的在buf中的数据，它就单纯的返回count，而这个count就是write系统调用完全成功的时候返回的数值，表示实际写入了多少字节。这就相当于老师给你留了作业，你什么都不写，但是你就说你都写完了。老师留抄写10遍，你就说10遍写完了。老师留抄写100遍，你就说100遍写完了。/dev/null这个文件的write实现就是这样的。

所以根本没有什么魔法，更没有什么替你“把标准错误删除”这种费尽的操作。就是单纯的你重定向给它，它得到数据后什么也没做就返回了成功，仅此而已。

## 结语：

到此，我尽量说明了理解Linux中shell“重定向”原理的基本知识。当然这还不是全部，只能算是刚进门吧。作为一个[软件工程师](https://www.zhihu.com/search?q=%E8%BD%AF%E4%BB%B6%E5%B7%A5%E7%A8%8B%E5%B8%88&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A2304247674%7D)，我们不能把知识停留在操作和语法的表面上，而是应该尽量去理解操作背后的过程，由此才能深入对系统的理解。并不是说写"module_init(xxx)"就一定比写"echo something > file"高级，高不高级看你对自己所写内容的理解程度。