# 第二步入口：统一筛选、全局排名与交付

版本：0.3.0。开始前完整读取同目录 [prompt.txt](prompt.txt)、[core-definitions-rules.txt](core-definitions-rules.txt)、[preamble.tex](preamble.tex)、[template.tex](template.tex)。必须同时提供四件套；此 Markdown 不内嵌模板，也不能单独替代规则。

使用用户学科目录内的实际 Index 材料、已有 manifest 和候选来源记录。先确认规则 A 的材料核对与全部可用索引读取已完成；未完成时补做所需核对，不要求缺席的 PDF 或 `main.tex`，不因历史路径失效弃用可读缓存。

执行规则 B1–D5：统一准入标准，规范名称并合并真正同义项，再形成整个学科的全局排名；保留与最终条目一致的名次、名称、层次及 Index 来源对应记录。不得沿用旧清单作为候选依据或默认顺序。

执行规则 E1–F4：从同目录 `template.tex` 生成完整独立候选，保留固定导言区和框架，按规定检查内容、来源及格式。`CLASS` 取学科文件夹完整名称，保留空格和大小写；目标为 `INPUT_DIR/CLASS_core_definitions.tex`。

可运行本包的只读检查器，路径含空格时加引号：

~~~text
python <PROMPT_DIR>/scripts/validate_output.py "<CANDIDATE_TEX>"
~~~

明确编译实际完整候选并检查渲染结果。覆盖旧输出前创建不冲突且已核验字节一致的备份；通过所需检查后原样复制候选，不把失败候选标为已接受。区分通过、未执行和失败，编译器不可用与编译失败分别披露。

每学科交付一个目标 TeX；PDF 仅在用户要求时交付。来源缺口、未决材料、版次差异及未完成检查在聊天中简短披露，内部索引与来源记录留在工作缓存。完整规则以四件套为准。
