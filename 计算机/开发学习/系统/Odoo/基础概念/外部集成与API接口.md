Odoo提供了强大的API接口，用于与其他系统进行数据同步和功能集成。Odoo的核心API基于RPC（远程过程调用）协议，并提供了两种实现方式：`XML-RPC`和`JSON-RPC` 。  

`JSON-RPC`因其轻量和高效的特性，在现代集成中更受青睐 。大多数API交互都围绕一个通用的  

`execute_kw`方法展开，该方法允许远程客户端调用任何Odoo模型上的任何方法，如`search`、`read`、`create`等，从而实现了与Odoo后端ORM的紧密集成 。  

Odoo的RPC API设计与它的ORM（面向对象方法调用）架构紧密相关。`execute_kw`方法完美地映射了这种方法调用模式，使得远程客户端能够像本地Python代码一样操作ORM。相比之下，将每个ORM方法都映射到单独的REST端点会复杂得多。因此，RPC协议与Odoo内部架构的契合度更高。

除了核心的RPC接口，Odoo社区也提供了用于实现REST API的模块。这允许开发者使用标准的HTTP方法（GET, POST, PUT, DELETE）来与Odoo进行交互，这对于习惯RESTful范式的开发者来说更为友好 。  

下表对比了Odoo主要的API接口类型：

|特性|XML-RPC|JSON-RPC|REST API|
|---|---|---|---|
|**协议**|HTTP/HTTPS|HTTP/HTTPS|HTTP/HTTPS|
|**请求/响应格式**|XML|JSON|JSON/XML|
|**核心概念**|远程方法调用|远程方法调用|资源导向的CRUD操作|
|**主要方法**|`execute_kw`|`execute_kw`|GET, POST, PUT, DELETE|
|**适用场景**|传统集成，兼容性好|现代、轻量级集成|习惯RESTful范式，多用于Web服务集成|
