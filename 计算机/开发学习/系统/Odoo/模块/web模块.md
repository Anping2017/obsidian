# 🌐 Odoo `web` 模块解析

## 一、作用定位

- `web` 模块是 **Odoo Web 客户端的核心**。
    
- 负责：
    
    - **前端界面框架**（菜单、导航、表单、列表、看板…）
        
    - **Web 框架支持**（RPC 调用、QWeb 渲染）
        
    - **加载流程控制**（从登录 → 加载应用 → 渲染模块 UI）
        
    - **基础 JS 组件库**（字段小部件、视图渲染器）
        

📌 形象理解：  
👉 `base` 模块是后端基石，  
👉 `web` 模块是前端骨架，  
👉 功能模块（sales、stock）都挂在这两个基础上。

---

## 二、核心组件（前端）

### 1. **Web Client**

- **入口点**：`web/static/src/js/core/webclient.js`
    
- 功能：
    
    - 初始化 Odoo 前端
        
    - 管理导航、菜单、Action 加载
        
    - 渲染顶层界面（导航栏、应用菜单、主内容区）
        

```
/** 伪代码结构 */
class WebClient {
    setup() {
        this.router = new Router();   // 处理路由
        this.actionManager = new ActionManager(); // 控制界面动作
    }
}

```

---

### 2. **Action Manager**

- 控制 **动作（actions）** 的加载与执行。
    
- Odoo 的所有界面（表单、列表、看板、报表…）都是通过 **Action** 定义的。
    

📌 举例：

```
<record id="action_partner_form" model="ir.actions.act_window">
    <field name="name">Contacts</field>
    <field name="res_model">res.partner</field>
    <field name="view_mode">tree,form</field>
</record>

```

- `ActionManager` 接收这个定义 → 加载 `res.partner` → 渲染视图。
    

---

### 3. **视图（Views）**

- 类型：`form`, `tree`, `kanban`, `calendar`, `graph`, `pivot` …
    
- 定义在 XML 中，前端通过 JS 渲染器 + 模板加载。
    

📌 例子：

```
<record id="view_partner_tree" model="ir.ui.view">
    <field name="name">res.partner.tree</field>
    <field name="model">res.partner</field>
    <field name="arch" type="xml">
        <tree>
            <field name="name"/>
            <field name="email"/>
        </tree>
    </field>
</record>

```

对应前端：`TreeRenderer` → 渲染 `<table>`。

---

### 4. **Widgets（小部件）**

- 各种表单字段的 JS 实现（如日期选择器、下拉框、标签）。
    
- 位于：`web/static/src/js/fields/`
    

📌 举例：

- `CharField` → 普通输入框
    
- `Many2oneField` → 自动补全选择器
    
- `BooleanField` → 复选框
    

---

### 5. **QWeb 模板引擎**

- Odoo 的前端模板语言（类似 Jinja2/React JSX）。
    
- 用 XML 写 UI，JS 里动态渲染。
    
- 文件位置：`web/static/src/xml/`
    

例子（按钮模板）：

```
<t t-name="ButtonTemplate">
    <button type="button" class="btn btn-primary">
        <t t-esc="widget.label"/>
    </button>
</t>

```

---

## 三、加载流程（从登录到界面）

### 1. 登录

- 用户访问 `/web` → Nginx/Gunicorn → Odoo 控制器。
    
- `web.controllers.main.Home` 渲染入口页面。
    

### 2. 加载 Web Client

- 加载 JS 文件（`web.assets_backend`）。
    
- 初始化 `WebClient` → `ActionManager`。
    

### 3. 加载菜单

- 前端调用 `ir.ui.menu` 获取菜单数据。
    
- 左侧导航栏 + 顶部应用栏渲染。
    

### 4. 加载 Action

- 用户点击菜单 → 触发 `ir.actions.act_window`。
    
- `ActionManager` 根据 `view_mode` 加载对应视图。
    
- 调用后端 ORM（JSON-RPC）获取数据。
    

### 5. 渲染视图

- JS 渲染器（TreeRenderer/FormRenderer/KanbanRenderer）
    
- 绑定 Widgets → 显示在浏览器。
    

---

## 四、数据交互机制

- **RPC 调用**：前端通过 **JSON-RPC** 调用后端控制器（Python）。
    
- Odoo 提供 `rpc.js` 工具封装：
    

```
rpc.query({
    model: 'res.partner',
    method: 'search_read',
    args: [[['is_company','=',true]], ['name','email']],
}).then(function (result) {
    console.log(result);
});

```

对应 SQL（后端 ORM 执行）：

`SELECT id, name, email FROM res_partner WHERE is_company = true;`

---

## 五、核心依赖关系图

```
用户浏览器
   ↓
WebClient (JS)
   ↓
ActionManager → 解析 ir.actions
   ↓
ViewManager → 调用 Renderer
   ↓
Widgets & QWeb Templates
   ↓
JSON-RPC 调用后端 ORM
   ↓
PostgreSQL

```

---

## 六、总结

- **`web` 模块** 是 Odoo Web 客户端的心脏。
    
- 它提供：
    
    - WebClient（主框架）
        
    - ActionManager（动作控制）
        
    - 视图系统（Form/Tree/Kanban…）
        
    - Widgets（字段小部件）
        
    - QWeb（模板引擎）
        
- **加载流程**：登录 → WebClient 初始化 → 加载菜单 → 执行 Action → 渲染视图 → RPC 数据交互。