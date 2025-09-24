### Odoo 计划任务 (`ir.cron`)

在 Odoo 中，计划任务 (`ir.cron`) 是一种内置的自动化机制，用于定期执行服务器端的后台任务。它允许你安排一个特定的服务器动作或 Python 方法，使其在指定的时间间隔内自动运行。这对于执行数据清理、定期报告生成、邮件发送、数据同步或任何需要自动执行的重复性任务非常有用。

---

#### 核心功能与工作原理

`ir.cron` 的核心是一个数据库表，用于存储所有计划任务的配置。Odoo 的核心引擎会定期检查这个表，并根据任务的**下一次运行时间 (`nextcall`)** 来决定是否执行。

一个计划任务主要由以下几个关键部分组成：

1. **名称 (`name`)**: 用于识别任务的唯一描述性名称，例如“每日销售报告生成”。
    
2. **模型 (`model_id`)**: 任务要操作的模型。
    
3. **方法 (`function`)**: 任务要执行的方法。这个方法必须是模型上的一个方法。
    
4. **下一次运行时间 (`nextcall`)**: Odoo 计划任务的调度引擎将查看此字段，以确定何时运行任务。
    
5. **时间间隔 (`interval_number` 和 `interval_type`)**:
    
    - **`interval_number`**: 间隔的数值，例如 1、2、10。
        
    - **`interval_type`**: 间隔的类型，例如 `minutes`（分钟）、`hours`（小时）、`days`（天）、`weeks`（周）、`months`（月）。
        
6. **间隔类型 (`doall`)**:
    
    - `doall=False`（默认值）：任务只会按计划执行一次，然后 `nextcall` 会更新为下一次的计划时间。
        
    - `doall=True`：任务会尝试执行所有错过的执行，这在服务器停机后恢复时非常有用。例如，如果任务每小时运行一次，但服务器停机了 3 小时，它会依次执行 3 次任务。
        

---

#### 配置与使用

你可以在 Odoo 的后台界面或通过 XML 数据文件来配置计划任务。

##### 1. 通过 Odoo 后台界面配置

- 确保你已启用**开发者模式**。
    
- 导航到 **设置 -> 技术 -> 自动化 -> 计划任务**。
    
- 点击“创建”按钮，填写以下字段：
    
    - **名称**: “每日数据清理”
        
    - **模型**: `my.module.name` (你想要执行方法的模型)
        
    - **方法**: `_clean_up_data` (你定义的 Python 方法名)
        
    - **执行频率**: 设置 `interval_number` 和 `interval_type`，例如 `1 days`（每天）。
        
    - **下一次运行时间**: 设置首次运行的时间。
        
    - **用户**: 任务将以哪个用户的权限来执行。通常选择 `OdooBot` 或一个具有足够权限的系统用户。
        

##### 2. 通过 XML 数据文件配置 (推荐方式)

在模块开发中，推荐使用 XML 数据文件来定义计划任务。这确保了任务可以在模块安装和更新时自动创建和配置。

在你的模块的 `data/` 目录中创建一个 XML 文件，例如 `cron_jobs.xml`：

XML

```
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <record id="ir_cron_daily_data_cleanup" model="ir.cron">
            <field name="name">每日数据清理</field>
            <field name="interval_number">1</field>
            <field name="interval_type">days</field>
            <field name="nextcall">2023-01-01 02:00:00</field>
            <field name="numbercall">-1</field> <field name="doall">False</field>
            <field name="active" eval="True"/>
            <field name="user_id" ref="base.user_root"/>
            <field name="model_id" ref="model_my_module_name"/>
            <field name="state">code</field>
            <field name="code">model._clean_up_data()</field>
        </record>
    </data>
</odoo>
```

**代码解释**:

- `noupdate="1"`: 确保在模块后续更新时，这个计划任务的配置不会被覆盖。
    
- `model="ir.cron"`: 指定要创建的记录模型是 `ir.cron`。
    
- `name`, `interval_number`, `interval_type`: 对应计划任务的基本配置。
    
- `numbercall`: 设置为 `-1` 表示任务将**无限次**执行。
    
- `user_id`: 引用了 `base.user_root`，表示以管理员权限运行。
    
- `model_id`: 引用了你的自定义模型，例如 `model_my_module_name`。
    
- `state`: 设置为 `code`，表示要执行一段 Python 代码。
    
- `code`: 这段代码将在任务运行时执行。`model` 是一个特殊变量，代表 `model_id` 中指定的模型对象。
    

然后，在你的 Python 模型中定义这个方法：

Python

```
# models/my_module_name.py
from odoo import models, fields

class MyModule(models.Model):
    _name = 'my.module.name'
    _description = 'My Module'

    def _clean_up_data(self):
        """
        这个方法将被计划任务调用，用于清理数据。
        """
        # 编写数据清理的逻辑
        records_to_clean = self.search([('create_date', '<', '2023-01-01')])
        records_to_clean.unlink() # 删除旧记录
```

---

#### 计划任务与服务器动作的关系

在 Odoo 中，计划任务和服务器动作经常一起使用。一个计划任务可以配置为执行一个**服务器动作** (`ir.actions.server`)。

**`ir.cron`** 负责**调度**，即**何时**运行。 **`ir.actions.server`** 负责**执行**，即**运行什么**。

通过将计划任务与服务器动作关联，你可以利用服务器动作的配置化能力，而无需在 Python 代码中硬编码逻辑。

**示例 XML**:

XML

```
<record id="ir_cron_data_processing" model="ir.cron">
    <field name="name">数据处理任务</field>
    <field name="interval_number">1</field>
    <field name="interval_type">hours</field>
    <field name="numbercall">-1</field>
    <field name="doall">False</field>
    <field name="active" eval="True"/>
    <field name="user_id" ref="base.user_root"/>
    <field name="state">action</field>
    <field name="model_id" ref="base.model_ir_actions_server"/>
    <field name="code">action = model.browse(ref('my_module.my_server_action')).run()</field>
</record>
```

在这个例子中，`ir.cron` 并不直接调用某个模型的方法，而是执行一段 Python 代码，这段代码负责找到并运行一个名为 `my_server_action` 的服务器动作。这是一种更灵活的组织方式。