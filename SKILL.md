---
name: math-core-definitions
description: 从一个或多个包含 main.tex 参考书目与数学书籍 PDF 的本地文件夹提取书末 Index，再根据索引筛选、整合核心数学概念的英文名称，按固定模板在各目录生成 core_definitions.tex。适用于只需要定义名称的索引驱动清单，不用于解释定义或通读书籍综述。
metadata:
  version: "0.1.0"
---

# 数学核心定义名称提取

输入只需一个或多个资料文件夹的路径；每个目录含 main.tex 和书籍 PDF。输出为各资料目录中的 core_definitions.tex。

## 输入与边界

- main.tex 是参考书目，用于确认书名、作者、引用键或 MR 编号，不是定义来源。
- 核心筛选依据是书末 Index。只读取定位所需的少量目录、书签、封面及索引页；不通读正文，不提取整书文本，不对整书 OCR。
- 各目录独立整合。保留 main.tex 和原始 PDF；不同目录可以包含同一概念。
- 默认直接执行。不要求用户提供其他参数，不自行创建新聊天。用户明确要求派发新对话时，才为各目录创建独立本地聊天，并沿用用户指定的模型设置。
- 不自动联网补书或读取其他分类资料。

## 两步执行

对每个输入目录依次完成以下阶段，不在中间请求再次确认。

### 第一步：提取 Index

读取并执行 [references/extract-indexes.md](references/extract-indexes.md)。

先完成该目录所有可取得 Index 的提取及缓存，记录缺失或不可读情况，再进入第二步。缓存使用 INPUT_DIR/.core-definitions-work，已有可靠缓存可复用。

### 第二步：筛选并生成 TeX

第一步完成后，读取并执行 [references/select-definitions.md](references/select-definitions.md)。

仅根据缓存的 Index 和数学知识筛选概念，不回到正文逐条核验。每个输出条目应有索引依据，不能凭常识扩充未见于索引的概念。

必须使用 [assets/core_definitions.tex](assets/core_definitions.tex) 作为输出模板。该初版模板的导言区、文档标题、页面设置和文档框架固定；仅替换、增加主题 section 和其中的 itemize 条目。禁止自行改版。具体格式见第二步说明。

## 检查与交付

1. 逐项对照索引检查术语、筛选、同义合并及分类。
2. 运行只读格式检查：
   ~~~text
   python <SKILL_DIR>/scripts/validate_output.py <INPUT_DIR>/core_definitions.tex
   ~~~
   SKILL_DIR 是当前安装的本技能目录，路径按实际环境解析。根据错误修正输出，直至通过。
3. 使用可用的 LaTeX 工具编译检查。调用 compile_latex_document 时显式指定新文件路径、所在目录和 mainFile="core_definitions.tex"，避免误编译原 main.tex。无需打开其他编辑器标签或导出 PDF。
4. 若没有任何可用 Index，不生成凭空推测的清单；简短说明原因，继续处理其他输入目录。
5. 最终交付各目录的 core_definitions.tex 文件入口。不交付 PDF、定义解释或审查报告。缓存保留供后续复用。
6. 缺失索引、部分可读或无法验证编译时，在聊天中简短说明实际范围；不得声称已逐页阅读正文。

## 后续格式调整

初版格式由 assets/core_definitions.tex 管理。用户进一步规范格式时，同步更新模板、第二步说明与格式检查器；仅在用户授权修改技能时更新这些资源，不因一次提取任务擅自改变模板。
