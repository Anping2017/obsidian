## 1️⃣ PHP 基础

| 分类        | 内容                                                          |
| --------- | ----------------------------------------------------------- |
| **语法基础**  | PHP 标签、注释、变量、常量、数据类型（字符串、整数、浮点、布尔、数组、对象、NULL）               |
| **运算符**   | 算术、比较、逻辑、赋值、三元、位运算                                          |
| **流程控制**  | if/else、switch、while、for、foreach、break/continue             |
| **函数**    | 内置函数、用户自定义函数、参数传递、返回值                                       |
| **字符串操作** | 拼接、长度、查找、替换、正则、格式化                                          |
| **数组操作**  | 索引数组、关联数组、多维数组、排序、数组函数（array_map、array_filter、array_reduce） |
| **日期/时间** | date(), strtotime(), DateTime 类                             |

---

## 2️⃣ PHP 面向对象（OOP）

| 分类             | 内容                                              |
| -------------- | ----------------------------------------------- |
| **类与对象**       | class、new、属性、方法                                 |
| **访问控制**       | public、protected、private                        |
| **构造/析构函数**    | \__construct(), \__destruct()                   |
| **继承与重写**      | extends、parent::                                |
| **抽象类和接口**     | abstract class、interface                        |
| **静态成员**       | static 属性和方法                                    |
| **命名空间 & use** | 避免类名冲突                                          |
| **魔术方法**       | \__get, \__set, \__call, \__toString, \__invoke |

---

## 3️⃣ PHP 高级特性

|分类|内容|
|---|---|
|**错误与异常**|try/catch, Exception 类, set_error_handler|
|**类型声明**|函数参数和返回值类型, strict_types|
|**命名空间**|PSR-4 自动加载, Composer|
|**Traits**|代码复用机制|
|**匿名函数 / 闭包**|callable, use 关键字|
|**生成器**|yield, 节省内存处理大数据|
|**迭代器 / SPL**|Iterator, ArrayIterator, Countable 等|
|**正则表达式**|preg_match, preg_replace|

---

## 4️⃣ PHP 与 Web 开发

|分类|内容|
|---|---|
|**HTTP 基础**|$_GET, $_POST, $_REQUEST, $_SERVER, header()|
|**Cookie / Session**|setcookie(), session_start(), $_SESSION|
|**文件操作**|fopen, fread, fwrite, file_get_contents, file_put_contents|
|**上传下载**|$_FILES, move_uploaded_file|
|**表单处理**|表单验证, CSRF 防护, XSS 防护|
|**输出与缓冲**|echo, print, output buffering(ob_start, ob_end_flush)|
|**URL 与路由**|$_SERVER['REQUEST_URI'], PATH_INFO|

---

## 5️⃣ PHP 数据库

|分类|内容|
|---|---|
|**MySQL / MariaDB**|mysqli、PDO|
|**CRUD 操作**|SELECT, INSERT, UPDATE, DELETE|
|**预处理语句**|防止 SQL 注入|
|**事务**|beginTransaction, commit, rollback|
|**ORM / 框架 DB 层**|Eloquent, Doctrine|

---

## 6️⃣ PHP 框架与工具

|框架/工具|内容|
|---|---|
|**Laravel**|MVC 架构、路由、控制器、Eloquent ORM、Blade 模板、任务调度、事件系统|
|**Symfony**|组件化、依赖注入、Twig 模板、路由、表单处理|
|**CodeIgniter / ThinkPHP / Yii**|轻量级 MVC 框架|
|**Composer**|PHP 包管理工具、依赖管理、自动加载|
|**PHPUnit**|单元测试、TDD|
|**PHPMailer / SwiftMailer**|邮件发送|

---

## 7️⃣ PHP 与前端交互

|分类|内容|
|---|---|
|**AJAX**|异步请求数据，JSON 格式返回|
|**REST API**|使用 PHP 提供 JSON API，处理 CRUD 请求|
|**WebSocket / Ratchet**|实时通信应用|
|**模板引擎**|Blade, Twig, Smarty|

---

## 8️⃣ PHP 安全与优化

|分类|内容|
|---|---|
|**安全**|SQL 注入、XSS、CSRF、文件上传安全、Session 固化|
|**缓存**|OPcache, Redis, Memcached|
|**性能优化**|代码优化、数据库索引、懒加载、生成器|
|**日志与监控**|error_log(), Monolog|

---

## 9️⃣ PHP 部署与运维

|分类|内容|
|---|---|
|**Web 服务器**|Apache, Nginx|
|**PHP 配置**|php.ini, 扩展安装, FPM|
|**部署工具**|Docker, Git, CI/CD|
|**环境管理**|本地开发、测试、生产环境配置|