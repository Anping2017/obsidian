## 🔍 检查字段最终定义的方法

### 1. **Odoo Shell（最精确）**

`env['device.model']._fields['device_brand_id']`

可以直接看到字段对象，打印出来会显示字段的完整配置（string、required、readonly、ondelete 等）。

---

### 2. **调试模式（界面）**

- 打开 **开发者模式**（Odoo 设置 → 启用开发者模式）。
    
- 进入目标模型（例如设备管理 → 设备），打开某条记录。
    
- 点击 **🐞调试工具 → 查看字段**。
    
    - 会列出该视图中所有字段的技术信息，包括 `字段名、标签、类型、必填/只读` 等。
        

👉 适合前端确认某个字段最终表现。

---

### 3. **ir.model.fields 表（数据库层面）**

Odoo 把所有字段的元数据存储在 `ir.model.fields` 表里。你可以通过 UI 或 SQL 查询：

`SELECT name, field_description, ttype, required, readonly FROM ir_model_fields WHERE model = 'device.model' AND name = 'device_brand_id';`

👉 适合批量检查或在没有 shell 的情况下确认。

---

### 4. **在代码里调试（logging）**

在自定义模块里临时加一段日志：

`import logging _logger = logging.getLogger(__name__)  class DeviceModelInherit(models.Model):     _inherit = "device.model"      def _debug_field(self):         field = self._fields['device_brand_id']         _logger.info("Device Brand Field: %s", field.__dict__)`

然后在 Odoo 日志里就能看到该字段的完整定义。

---

## ✅ 对比总结

|方法|精度|使用场景|
|---|---|---|
|Odoo shell|⭐⭐⭐⭐|开发调试最常用|
|调试模式（UI）|⭐⭐⭐|界面上直观验证|
|ir.model.fields 表|⭐⭐|数据库层面检查，适合批量|
|日志打印|⭐⭐|无法进 shell 时，调试代码时|

---

👉 推荐：

- **开发阶段** → 用 Odoo shell。
    
- **功能验证** → 用调试模式 UI。
    
- **部署/排错** → 用 SQL 或日志。