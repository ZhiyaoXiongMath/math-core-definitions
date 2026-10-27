# 数学核心定义：完整工作流入口

版本：0.3.0。此入口可随整个提示词包独立使用；它不是完整规范的替代品。

开始前完整读取同目录的四件套：[prompt.txt](prompt.txt)、[core-definitions-rules.txt](core-definitions-rules.txt)、[preamble.tex](preamble.tex)、[template.tex](template.tex)。执行其 PURPOSE AND INPUT 及 A–F 全部规则，生成期间保持四件套原样。

用户提供一个或多个学科目录（`INPUT_DIR` 或 `INPUT_DIRS`），或具有明确学科标签的附件。不要要求额外的 PDF、`main.tex` 或固定缓存布局；仅在分组确有歧义时询问。

对每个学科依次执行：

1. [第一步](01-extract-indexes.md)：按规则 A 核对所有输入，复用或按需修复 Index，并读完全部可用索引。每个输入已交代即可继续，不要求缺失材料全部恢复。
2. [第二步](02-index-to-core-definitions.md)：按规则 B–F 统一筛选、规范名称、全局排名、保留最终来源记录，检查并保存结果。无需中途确认。

`CLASS` 是学科文件夹完整名称，保留空格与大小写；带标签附件使用同标签工作目录。最终每学科交付 `INPUT_DIR/CLASS_core_definitions.tex`，不跨学科重分类。没有可用 Index 的学科报告缺口并继续其他学科。

仅在用户明确要求新聊天时才派发，并使用用户指定的范围和可用模型设置。普通调用直接执行；不自动创建聊天、下载书籍或扩大学科范围。

检查器位于 [scripts/validate_output.py](scripts/validate_output.py)，默认使用本目录的 `template.tex`。它只检查格式，不能代替内容、来源、实际编译和渲染检查。完整使用说明见 [README.md](README.md)。
