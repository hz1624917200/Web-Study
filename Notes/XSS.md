# XSS

## Introduction by LLM

XSS（Cross-Site Scripting，跨站脚本攻击）是CTF（Capture The Flag）比赛中的常见Web安全漏洞。XSS漏洞的核心在于攻击者能够向目标网站注入恶意代码（通常是JavaScript），并在其他用户浏览该网站时执行这些代码。XSS攻击可以分为以下几类：

1. **反射型XSS（Reflected XSS）：** 这种类型的XSS是指攻击者将恶意代码作为输入数据发送给服务器，服务器处理后将其返回给用户浏览器并执行。典型的例子是通过URL参数传递恶意脚本。举例：

   ```
   html
   Copy code
   <script>alert('XSS');</script>
   ```

   如果一个网站直接将用户输入的数据展示在页面上而没有适当过滤，就可能导致反射型XSS。

2. **存储型XSS（Stored XSS）：** 存储型XSS是指恶意脚本被永久存储在目标服务器上，例如在数据库中，之后每次用户访问该网站时，恶意脚本都会被执行。常见的场景是留言板、评论区或论坛等用户生成内容的区域。举例：

   ```
   html
   Copy code
   <script>alert('Stored XSS');</script>
   ```

   当攻击者将这个脚本提交到留言板，所有访问该留言板的用户都会执行这个脚本。

3. **基于DOM的XSS（DOM-based XSS）：** 这种类型的XSS不需要通过服务器端，而是直接在客户端执行恶意代码。通常是由于客户端脚本不安全地操作DOM（文档对象模型）导致的。例如，一个网站通过URL的哈希值来显示某些内容，如果没有适当的处理就会导致XSS。举例：

   ```
   javascript
   Copy code
   var hash = location.hash;
   document.body.innerHTML = hash;
   ```

   如果用户访问 `http://example.com/#<script>alert('DOM XSS');</script>`，恶意脚本就会执行。

### 如何防御XSS攻击

1. **输入验证和过滤：** 对用户输入的数据进行严格验证和过滤，确保只接受合法的输入。可以使用白名单策略，只允许特定的字符或格式。
2. **输出编码：** 对输出到HTML、JavaScript、CSS等不同上下文的数据进行适当的编码。例如，在HTML中输出用户输入时，应该进行HTML实体编码。
3. **使用安全的API：** 避免直接操作DOM，可以使用安全的API来处理用户输入。例如，使用 `textContent` 而不是 `innerHTML`。
4. **内容安全策略（CSP）：** 通过设置CSP头，可以限制浏览器加载的资源，防止恶意脚本的执行。例如，只允许加载特定来源的脚本。
5. **使用框架自带的安全机制：** 现代Web开发框架（如React, Angular等）通常自带防御XSS的机制，尽量使用这些框架自带的方法来处理用户输入和输出。

### Example

BUUOJ XSS Course 1

**典型的XSS Payload**

```html
<script>alert('XSS');</script>
<img src=# onerror=alert('xss')>
```

* 1被禁用（script），2有效