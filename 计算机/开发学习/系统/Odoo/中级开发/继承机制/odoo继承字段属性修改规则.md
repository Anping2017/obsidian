# Odoo 字段覆盖常见问题笔记

## ❓ Q1: 覆盖字段时具体怎么写？

**答案**：直接用相同字段名重定义，只写需要修改的属性即可。

- Odoo 会把你写的属性覆盖原定义。
    
- 没写的属性会继承原来的定义。
    
- 字段类型必须保持一致，否则报错。
    
[[odoo继承字段属性哪些可以改]]

---

## ❓ Q2: 如果多个模块覆盖同一个字段，会发生什么？

**答案**：遵循“最后加载的模块生效”。

- Odoo 加载顺序 = `__manifest__.py` → `depends` 指定先后。
    
- 如果 A 改成 `required=True`，B 改成 `required=False`，那么 **后加载的 B 覆盖 A**。
    
- 推荐：在 `manifest` 里通过 `depends` 明确控制模块加载顺序，避免冲突。
    
[[odoo如何避免多模块覆盖同一值产生冲突]]

---

## ✅ 案例：修改 `device.model` 的 `device_brand_id`

假设原始定义是：

`device_brand_id = fields.Many2one(     'device.brand',     string="Brand",     required=False,     ondelete="set null", )`

👉 只想改成必填：

`from odoo import models, fields  class DeviceModelInherit(models.Model):     _inherit = "device.model"      device_brand_id = fields.Many2one(         'device.brand',         required=True   # 只写要修改的属性     )`

结果：

- `string="Brand"` 保持不变
    
- `ondelete="set null"` 保持不变
    
- 只有 `required` 变成 `True`
    

---

## 🔍 如何分析最终字段定义？

进入 Odoo shell：

`env['device.model']._fields['device_brand_id']`

可以看到当前字段的最终属性（string、required、ondelete 等），确认覆盖是否生效。

[[几种常用方法可以检查字段]]

---
