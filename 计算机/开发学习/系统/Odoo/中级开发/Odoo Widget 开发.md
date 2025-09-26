# Odoo Widget 开发与使用指南

---

## 1. 核心概念

- **Widget（小部件）** 是 Odoo 前端视图中对字段或表单的自定义展示和交互控件
    
- **作用**：
    
    1. 提供自定义字段展示方式
        
    2. 增强用户交互体验
        
    3. 支持复杂数据可视化
        
- **应用场景**：
    
    - 日期选择器、颜色选择器、进度条、条形图
        
    - 文件上传、图片预览、动态表格
        
    - 自定义表单行为
        

---

## 2. Widget 分类

|分类|描述|示例|
|---|---|---|
|**基础字段 Widget**|改变字段显示样式|`boolean_toggle`, `statusbar`|
|**日期/时间 Widget**|日期或时间选择控件|`date`, `datetime`|
|**文件 Widget**|文件上传或显示|`many2many_binary`, `image`|
|**进度/可视化 Widget**|图表、进度条|`progressbar`, `kanban_badge`|
|**自定义 Widget**|自定义 JS 控件|自定义表单字段展示、复杂交互|

---

## 3. 前端开发结构

### 3.1 目录结构

```
my_module/
├── static/
│   ├── src/js/
│   │   └── my_widget.js
│   └── description/
└── views/
    └── form_view.xml

```

### 3.2 JS Widget 示例（基础写法）

```
odoo.define('my_module.MyWidget', function (require) {
    "use strict";

    var fieldRegistry = require('web.field_registry');
    var FieldChar = require('web.basic_fields').FieldChar;

    var MyWidget = FieldChar.extend({
        // 渲染字段值
        _render: function () {
            this.$el.text("🔥 " + (this.value || ""));
        },
    });

    fieldRegistry.add('my_widget', MyWidget);
});

```

- `_render()` 方法：渲染字段显示
    
- `fieldRegistry.add('my_widget', MyWidget)`：注册自定义 Widget
    

---

## 4. 在 XML 视图中使用 Widget

`<field name="name" widget="my_widget"/>`

- `widget` 属性指定 Widget 类型
    
- 支持系统内置 Widget 和自定义 Widget
    

---

## 5. 内置 Widget 常用示例

|Widget|描述|
|---|---|
|`statusbar`|状态条显示|
|`progressbar`|进度条显示|
|`many2many_tags`|多选标签展示|
|`image`|图片显示与上传|
|`monetary`|货币显示格式|
|`handle`|拖拽排序|
|`radio` / `selection`|单选字段显示|
|`email`|邮件字段超链接|

---

## 6. 高级特性

1. **事件绑定**
    

`this.$el.on('click', this._onClick.bind(this));`

2. **访问 ORM 数据**
    

```
this._rpc({
    model: 'res.partner',
    method: 'search_read',
    args: [[['customer','=',true]], ['name','email']]
}).then(function(result){
    console.log(result);
});

```

3. **组合 Widget**
    

- Widget 内嵌 Widget，例如 Kanban 卡片内使用进度条 Widget
    

4. **动态样式与动画**
    

- 可通过 jQuery / CSS 控制显示效果
    

---

## 7. 实际应用场景

|场景|描述|
|---|---|
|自定义表单字段|特殊显示需求，例如带图标的字符字段|
|仪表盘|进度条、图表、指标显示|
|文件管理|文件上传、图片预览、小组件列表|
|状态控制|状态条、按钮操作、拖拽排序|
|动态数据展示|根据条件动态渲染字段内容|

---

## 8. 开发流程总结

1. **分析需求** → 决定 Widget 类型
    
2. **创建 JS 文件** → 定义 Widget 类
    
3. **注册 Widget** → fieldRegistry.add()
    
4. **XML 视图调用** → `<field name="xxx" widget="my_widget"/>`
    
5. **测试与优化** → 样式、事件绑定、数据渲染