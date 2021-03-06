---
tags:
- corn表达式
---

# corn 表达式

## 1. 语法格式

cron 表达式是一个字符串，字符串以 5 或 6 个空格隔开，分为 6 或 7 个域，每一个域代表一个含义，cron 有如下两种语法格式：

- Seconds Minutes Hours DayofMonth Month DayofWeek Year
- Seconds Minutes Hours DayofMonth Month DayofWeek

| 字段                   | 允许值                           | 允许的特殊字符              |
| ---------------------- | -------------------------------- | --------------------------- |
| 秒（_Seconds_）        | 0~59 的整数                      | `,` `-` `*` `/`             |
| 分（_Minutes_）        | 0~59 的整数                      | `,` `-` `*` `/`             |
| 小时（_Hours_）        | 0~23 的整数                      | `,` `-` `*` `/`             |
| 日期（_Day-of-Month_） | 1~31 的整数（需要考虑月的天数）  | `,` `-` `*` `/` `?` `L` `W` |
| 月份（_Month_）        | 1~12 的整数或者 JAN-DEC          | `,` `-` `*` `/`             |
| 星期（_Day-of-Week_）  | 1~7 的整数或者 SUN-SAT （1=SUN） | `,` `-` `*` `/` `?` `L` `#` |
| 年(可选)（_Year_）     | 1970~2099                        | `,` `-` `*` `/`             |

## 2. 特殊字符

`*` ：代表所有可能的值。
- `*` 在 Month 中表示每个月，在 Day-of-Month 中表示每天，在 Hours 表示每小时
- 假如：在 Minutes 子表达式中，`*` 即表示*每分钟*都会触发事件。

`-` ：表示指定范围。
- 例如：在 Minutes 子表达式中，`5-20` 表示*从 5 分到 20 分钟*每分钟触发一次

`,`：表示列出枚举值。
- 例如：在 Minutes 子表达式中，`5,20` 表示*在 5 分钟和 20 分钟时*触发。

`/` ：被用于指定增量。
- 例如：在 Minutes 子表达式中，`0/15` 表示*从 0 分钟开始，每 15 分钟执行一次*。`3/20` 表示从第三分钟开始，每 20 分钟执行一次。和 `3,23,43`（表示第 3，23，43 分钟触发）的含义一样。

`?` ：用在 Day-of-Month 和 Day-of-Week 中，指*没有具体的值*。
- 当两个子表达式其中一个被指定了值以后，为了避免冲突，需要将另外一个的值设为 `?`。
- 例如：想在每月 20 日触发调度，不管 20 号是星期几，只能用如下写法：`0 0 0 20 * ?`，其中最后一位只能用 `?`，而不能用 `*`。

`L`：用在 Day-of-Month 和 Day-of-Week 中。指*最后一天或倒数指的天数*。
- 在 Day-of-Month 中，`L` 表示*一个月的最后一天*，一月 31 号，3 月 30 号。
- 在 Day-of-Week 中，`L` 表示*一个星期的最后一天*，也就是 `7` 或者 `SAT`
- 如果 `L` 前有具体内容，它就有其他的含义了。例如：`6L` 表示*这个月的倒数第六天*。`FRIL` 表示*这个月的最后一个星期五*。
- 注意：在使用 `L` 参数时，不要指定列表或者范围，这样会出现问题。

`W`：Workday 的缩写。只能用在 Day-of-Month 字段。用来描叙最接近指定天的工作日。
- 例如：在 Day-of-Month 字段用 `15W` 指*最接近这个月第 15 天的工作日*。
- 如果这个月第 15 天是周六，那么触发器将会在这个月第 14 天即周五触发；如果这个月第 15 天是周日，那么触发器将会在这个月第 16 天即周一触发；如果这个月第 15 天是周二，那么就在触发器这天触发。
- 注意一点：这个用法只会在当前月计算值，不会越过当前月。`W` 字符仅能在 Day-of-Month 指明一天，不能是一个范围或列表。也可以用 `LW` 来指定*这个月的最后一个工作日*。

`#`：只能用在 Day-of-Week 字段。用来指定这个月的第几个周几。
- 例如：在 Day-of-Week 字段用 `6#3` 或 `FRI#3` 指*这个月第 3 个周五*（6 指周五，3 指第 3 个）。如果指定的日期不存在，触发器就不会触发。

## 3. 表达式例子

`0 * * * * ?` 每 1 分钟触发一次

`0 0 * * * ?` 每天每 1 小时触发一次

`0 0 10 * * ?` 每天 10 点触发一次

`0 * 14 * * ?` 在每天下午 2 点到下午 2:59 期间的每 1 分钟触发

`0 30 9 1 * ?` 每月 1 号上午 9 点半

`0 15 10 15 * ?` 每月 15 日上午 10:15 触发

`*/5 * * * * ? ` 每隔 5 秒执行一次

`0 */1 * * * ?` 每隔 1 分钟执行一次

`0 0 5-15 * * ?` 每天 5-15 点整点触发

`0 0/3 * * * ?` 每三分钟触发一次

`0 0-5 14 * * ?` 在每天下午 2 点到下午 2:05 期间的每 1 分钟触发

`0 0/5 14 * * ?` 在每天下午 2 点到下午 2:55 期间的每 5 分钟触发

`0 0/5 14,18 * * ?` 在每天下午 2 点到 2:55 期间和下午 6 点到 6:55 期间的每 5 分钟触发

`0 0/30 9-17 * * ?` 朝九晚五内每半小时触发

`0 0 10,14,16 * * ?` 每天上午 10 点，下午 2 点，4 点

`0 0 12 ? * WED` 表示每个星期三中午 12 点

`0 0 17 ? * TUES,THUR,SAT` 每周二、四、六下午五点

`0 10,44 14 ? 3 WED` 每年三月的每个星期三的下午 2:10 和 2:44 触发

`0 15 10 ? * MON-FRI` 周一至周五的上午 10:15 触发

`0 0 23 L * ?` 每月最后一天 23 点执行一次

`0 15 10 * * ? 2005` 2005 年的每天上午 10:15 触发

`0 15 10 ? * 6L 2002-2005` 2002 年至 2005 年的每月的最后一个星期五上午 10:15 触发

`0 15 10 ? * 6#3` 每月的第三个星期五上午 10:15 触发
