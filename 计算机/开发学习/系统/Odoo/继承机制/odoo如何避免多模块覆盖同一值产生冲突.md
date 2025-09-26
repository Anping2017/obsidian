## 多个模块覆盖同一个字段时

Odoo 的加载顺序是 **模块安装 / 加载顺序** → **Python 类继承顺序**。

例如：

- 模块 `A` 修改了 `res.partner.email` → `required=True`
    
- 模块 `B` 也修改了 `res.partner.email` → `required=False`
    

最终结果取决于 **哪个模块最后被加载**：

- 如果 `B` 在 `A` 之后加载，则 `required=False` 生效。
    
- 如果 `A` 在 `B` 之后加载，则 `required=True` 生效。
    

### ⚠️ 问题：

这意味着多个模块同时覆盖同一字段时，存在 **覆盖冲突**（last-write-wins，后加载的覆盖前加载的）。

---

## 3. 推荐做法

1. **修改少量属性时** → 直接 `fields.*` 重定义即可。
    
2. **避免冲突时** → 尽量用 `attrs` 或 `views` 层去控制（比如必填/只读等逻辑），少用 `required=True` 这种硬约束。
    
3. **多个模块都要改时** → 在 manifest 里用 `depends` 控制加载顺序，保证最终行为可预期。
    
4. **调试** → 可以在 Odoo shell 里用：