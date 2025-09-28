# 📩 Odoo `mail` 模块详解

## 一、模块作用

- 提供 **统一的消息系统**（Message Bus）。
    
- 实现 **内部消息、邮件、通知、讨论线程**。
    
- 提供 **关注者（followers）机制**，支持记录级别的订阅/通知。
    
- 集成 **邮件网关**（从邮箱收发邮件）。
    

📌 形象理解：  
👉 `base` 管理 **数据结构**，  
👉 `web` 管理 **界面**，  
👉 `mail` 管理 **沟通和消息流**。

---

## 二、核心模型

### 1. `mail.thread`

- 抽象模型（abstract model），业务模型只要继承它，就有消息功能。
    
- 提供 **chatter（聊天记录面板）**。
    
- 常见字段：
    
    - `message_ids` → 消息记录
        
    - `message_follower_ids` → 关注者
        
    - `activity_ids` → 活动/提醒
        

例子：销售订单继承 `mail.thread`

```
class SaleOrder(models.Model):
    _inherit = ["mail.thread", "mail.activity.mixin"]

```

---

### 2. `mail.message`

- 存储所有消息记录。
    
- 字段：
    
    - `body` → 消息正文
        
    - `subject` → 主题
        
    - `author_id` → 发送者（`res.partner`）
        
    - `model` + `res_id` → 消息关联的业务对象
        
    - `message_type` → 类型（email、comment、notification）
        

---

### 3. `mail.followers`

- 关注者表。
    
- 谁订阅了某个业务对象，就存储在这里。
    
- 字段：
    
    - `res_model`, `res_id` → 关注的对象
        
    - `partner_id` → 关注者
        

---

### 4. `mail.activity`

- 待办事项/提醒系统。
    
- 字段：
    
    - `res_model`, `res_id` → 关联业务对象
        
    - `activity_type_id` → 活动类型（电话、会议、任务）
        
    - `date_deadline` → 截止日期
        

---

## 三、消息与通知机制

### 1. 消息创建流程

当你在 `chatter` 里写消息时：

1. 前端调用 `message_post` 方法。
    
2. ORM 创建 `mail.message` 记录。
    
3. 根据 `followers`，推送通知。
    
4. 如果消息类型是 `email`，通过外发服务器发送邮件。
    

例子：

```
self.message_post(
    body="Order confirmed!",
    subject="Confirmation",
    message_type="comment",
    subtype_xmlid="mail.mt_note"
)

```

---

### 2. 关注者机制

- 每个记录可以有多个关注者（followers）。
    
- 关注者可选择订阅哪些事件（创建、更新、活动）。
    
- 新消息发布 → 通知所有关注者。
    

---

### 3. 通知机制

- `mail.notification` 模型负责存储通知。
    
- 支持 **多渠道通知**：
    
    - **Odoo 内部通知**（界面小铃铛）
        
    - **邮件通知**
        
    - **实时推送（bus 模块）**
        

📌 数据流：

```
message_post()
   ↓
mail.message
   ↓
mail.followers (找关注者)
   ↓
mail.notification
   ↓
- Odoo 客户端通知
- 邮件发送

```

---

## 四、与其他模块的结合

### 1. 与 `bus` 模块

- `bus` 提供实时推送（WebSocket 长连接）。
    
- 当有新消息时，通知会即时推送到前端。
    

### 2. 与 `mail.activity.mixin`

- 给业务模型添加 **待办提醒** 功能。
    
- 例如：销售订单到期时，提醒销售人员。
    

---

## 五、可视化结构

```
业务模型 (sale.order, project.task...)
     ↑ 继承
mail.thread (消息系统)
     │
 ┌───┴─────────────────────┐
 │                         │
mail.message          mail.activity
 (消息内容)           (提醒/待办)
     │
     ↓
mail.followers → 订阅者 (res.partner)
     ↓
mail.notification → 通知记录
     ↓
- Odoo 前端通知 (bus 实时推送)
- 邮件发送 (SMTP)

```

---

## 六、典型使用场景

1. **销售订单确认** → 记录一条消息 → 通知销售经理
    
2. **项目任务** → 分配任务 → 生成 `mail.activity` 提醒
    
3. **客户邮件** → 通过邮件网关 → 转成 `mail.message` → 显示在 `chatter`
    
4. **内部讨论** → 用户在记录下评论 → followers 都收到消息
    

---

## 七、总结

- `mail` 模块为 Odoo 提供 **统一的消息系统**。
    
- 核心模型：
    
    - `mail.thread` → 消息框架
        
    - `mail.message` → 消息存储
        
    - `mail.followers` → 订阅机制
        
    - `mail.activity` → 待办提醒
        
    - `mail.notification` → 通知管理
        
- 通知可通过 **Odoo 客户端、邮件、bus 实时推送** 发送。
    
- 几乎所有业务模型都继承 `mail.thread`，因此消息和通知功能是全局的。