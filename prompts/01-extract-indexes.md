# 第一步入口：核对、复用与读取 Index

版本：0.3.0。开始前完整读取同目录 [prompt.txt](prompt.txt)、[core-definitions-rules.txt](core-definitions-rules.txt)、[preamble.tex](preamble.tex)、[template.tex](template.tex)。四件套是完整规范，本入口只限定本次执行阶段。

按规则 PURPOSE AND INPUT 及 A1–A6 处理用户指定学科的实际材料。可输入书籍 PDF、Index 摘录、转移缓存或有明确标签的附件；`main.tex` 和原 PDF 都不是必需条件。

本阶段核对每个输入、复用现有可读材料；仅在源 PDF 可用时修复受影响的索引部分。读完全部可用主题索引和含概念名称的符号索引，保留候选及可用来源位置，尚不做最终准入或重要性排名。不读正文，不做整书提取或 OCR。

常规缓存位置为 `INPUT_DIR/.core-definitions-work/indexes`，manifest 位于其父目录；也可沿用已有清晰布局或用户指定位置。新便携记录用相对路径，重定位旧路径时保留书籍身份。

完成条件是每个输入均已交代、全部可用相关 Index 均已读取并可供下一阶段定位，不表示原件完整或所有缺口已恢复。按规则记录当前观察、继承声明、实际覆盖、版次差异和未决问题。

单独调用时仅交代缓存位置和实际材料缺口，不生成最终 TeX。由 [workflow.md](workflow.md) 调用时，完成后继续 [第二步](02-index-to-core-definitions.md)。无可用 Index 时报告缺口，不伪造材料。
