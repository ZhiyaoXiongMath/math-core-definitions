---
name: math-core-definitions
description: 从一个或多个包含 main.tex 参考书目与数学书籍 PDF 的本地分类文件夹提取书末 Index，筛选核心定义与重要定义的英文名称，按重要性全局排名并生成 core_definitions.tex。用于为后续定理评价提供概念重要性参考；默认不分 section，最多 3 个，不解释定义或通读正文。
metadata:
  version: "0.2.0"
---

# 数学核心定义名称与重要性排名

输入只需一个或多个资料文件夹的路径，每个目录含 main.tex 和书籍 PDF。每个目录是用户已经确定的一个大类，独立输出 core_definitions.tex。

本技能为后续定理评价提供“涉及概念的重要性”参考。排名针对本类别内的概念，不直接计算定理质量，不把术语排名当作定理创新性或证明深度的分数。

## 输入与边界

- main.tex 只用于确认书目、作者、引用键或 MR 编号。
- 提取依据是书末 Index；只读取定位所需的少量书签、目录、封面及索引页。不通读正文，不提取整书文本，不对整书 OCR。
- 保留 main.tex、原始 PDF 及用户的目录分类，不跨目录重新归类。
- 不要求额外参数，不自动联网补书或创建新聊天。用户明确要求新聊天时，才为各目录独立派发，并使用用户指定的模型设置。

## 两步执行

### 第一步：提取 Index

读取并执行 [references/extract-indexes.md](references/extract-indexes.md)。

先完成本目录各书可取得 Index 的提取与缓存，记录不可用材料，再进入第二步。缓存使用 INPUT_DIR/.core-definitions-work，可靠的已有缓存可复用。本阶段不筛选或排序索引词。

### 第二步：筛选、全局排名并生成 TeX

第一步完成后读取并执行 [references/select-definitions.md](references/select-definitions.md)，无需中途确认。

- 仍只保留核心定义与重要定义。先去重、规范名称，再形成整个目录的一份全局重要性序列。
- 核心定义排在重要定义之前；各层次内部从重要到次重要排序。重要性依据以本类别主要理论、中心问题、主要定理和关键方法中的结构性作用为主。
- 排名优先于逻辑依赖顺序、字母顺序、书籍次序和主题分组。最终用连续编号表示排名，1 为最高。
- 默认不使用 section；确有必要时最多 3 个宽泛 section，且分段不得改变全局排名，编号不得重置。不要为凑够 3 段细分分类。
- 最终只列名称与排名编号，不写定义、等级标签、数值评分、理由或来源注释。

必须使用 [assets/core_definitions.tex](assets/core_definitions.tex)。导言区、固定标题及页面设置不变。正文可以是一份无 section 的 enumerate，或至多 3 个 section 下连续编号的 enumerate；详细语法见第二步说明。

## 检查与交付

1. 对照索引审查筛选、同义整合及全局排名，确认没有为分组或依赖顺序牺牲重要性排序。
2. 运行只读格式检查：
   ~~~text
   python <SKILL_DIR>/scripts/validate_output.py <INPUT_DIR>/core_definitions.tex
   ~~~
   SKILL_DIR 为本技能实际目录。修正格式问题直至通过。脚本检查模板、0–3 个 section 和连续编号结构，不判断数学重要性。
3. 编译检查新文件。使用 compile_latex_document 时显式给出输出路径、所在目录和 mainFile="core_definitions.tex"，避免编译原 main.tex。
4. 没有任何可用 Index 时，不凭空生成清单；说明原因并继续其他目录。
5. 每个目录只交付 core_definitions.tex；缓存保留供复用。索引不完整或编译无法验证时，在聊天中简短说明，不写进 TeX。
6. 后续仅在用户要求修改规范时更新模板、第二步说明与检查器，不因一次提取任务自行改版。
