### Obsidian Annotator 插件简介

这是一个用于 Obsidian 的插件 (https://obsidian.md)，它允许你打开并注释 PDF 和 EPUB 文件。

该插件基于 [Hypothesis](https://web.hypothes.is/) 的技术，但进行了修改，使注释存储在本地 Markdown 文件中，而不是互联网上。

#### 演示

点击以下链接观看演示：  
annotator demo

**警告！** 在上面的 gif 中，我使用了 Dataview 语法来指定注释目标。如果你没有安装 Dataview 插件，你必须将注释目标写入文件的 frontmatter，如下所示：

`--- annotation-target: https://arxiv.org/pdf/2104.13478.pdf ---`

#### 已知问题

- 该插件在 iOS 16.3 或更高版本上无法正常工作。请查看 [#289 issue](https://github.com/obsidianmd/obsidian/issues/289) 状态以获取最新信息。
    
- 如果注释在不同平台上进行了更改，Reader 不会显示这些注释。
    

---

### 开始使用

1. 在 Obsidian 笔记的 frontmatter 中添加 `annotation-target` 属性，并将其值设置为 EPUB 或 PDF 文件的位置。位置可以是本地文件（如 `Pdfs/mypdf.pdf`）或在线文件（如 `https://arxiv.org/pdf/2104.13478.pdf`）。
    
2. 在打开的笔记窗格中，选择“更多选项”（右上角的三个点），应该会出现一个新的选项“注释（annotate）”。
    
3. 插件会自动尝试根据文件路径确定文件类型（EPUB 或 PDF）。如果插件无法识别，你也可以手动在 frontmatter 中添加 `annotation-target-type` 属性，并指定文件类型。
    
4. 如果安装了 Dataview 插件，你还可以使用 Dataview 属性来指定注释目标。在这种情况下，可以使用 Obsidian 风格的链接，而不是纯文本路径。
    

**警告！** 切勿重命名原始的 PDF 或 EPUB 文件，否则插件将失去注释与文件之间的关联。

---

### 注释

注释过程很直观，只需用鼠标选择文本即可开始注释。

未来可能会加入高亮和图像/区域高亮等功能，但这些功能需要首先在 Hypothesis 中进行更新。相关问题可参考：

- [GitHub Issue #198](https://github.com/hypothesis/product-backlog/issues/198)
    
- [GitHub Issue #669](https://github.com/hypothesis/product-backlog/issues/669)
    

#### Markdown 中的注释

要返回到常规的 Obsidian Markdown 编辑模式，可以选择“更多选项” → “以 MD 格式打开”。每个注释都有一个与之关联的引用块和块引用。在修改这些块时要小心。

- 对 `PREFIX`、`HIGHLIGHT` 和 `POSTFIX` 进行轻微修改通常是可以的，但如果修改过大，Hypothesis 可能无法再识别对应的文本。
    
- `COMMENT` 区域可以自由编辑（但要确保它仍然是引用块的一部分）。
    
- `TAGS` 区域应该包含以逗号分隔的 Obsidian 标签（例如：`#tag1, #tag2, #tag3`）。
    

---

### 暗黑模式

该插件内置了暗黑模式支持。要切换暗黑模式，请选择“更多选项” → “切换暗黑模式”。  
你还可以在插件的设置页面调整暗黑模式的行为。

---

### 链接到注释

Obsidian 链接到注释的块引用时，点击链接会打开对应的文件，并滚动到与之关联的高亮文本。如果文件已经在一个窗格中打开，则点击链接会使该窗格滚动到注释所在位置。