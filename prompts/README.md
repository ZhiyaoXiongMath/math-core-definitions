# 数学核心定义独立提示词包 / Standalone prompt pack

[中文](#中文) | [English](#english)

## 中文

版本：**0.3.0**。本目录可整体复制使用，不依赖已安装的 skill。执行环境仍需读取所供材料；格式检查器需要 Python 3 标准库，最终编译与目视检查需要 pdfLaTeX 等标准编译器及 PDF 渲染或查看工具。处理原 PDF 时才需要相应页面提取工具，扫描 Index 另需页面 OCR。

本包按用户指定学科，从全部可用 Index 中筛选核心与重要英文概念名并全局排名。接受书籍 PDF、仅有 Index 的摘录或缓存、带明确标签的附件，不要求必有 `main.tex` 或原 PDF。不读正文，不以常识或旧清单补候选；名次是学科内序数，不是定理评分，也不能跨学科比较。

### 完整四件套与入口

开始执行前必须完整读取以下四个文件，生成期间保持它们原样。它们共同构成完整规范，阶段 Markdown 不能单独代替其中任何文件。

| 文件 | 用途 |
| --- | --- |
| [core-definitions-rules.txt](core-definitions-rules.txt) | PURPOSE AND INPUT 与 A–F 全部具体规则。 |
| [prompt.txt](prompt.txt) | 总体执行要求。 |
| [preamble.tex](preamble.tex) | 固定导言区片段，不单独编译。 |
| [template.tex](template.tex) | 完整模板，已内嵌导言区，不再次加载 `preamble.tex`。 |
| [workflow.md](workflow.md) | 从材料核对到检查交付的完整流程入口。 |
| [01-extract-indexes.md](01-extract-indexes.md) | 仅执行材料核对、Index 读取与缓存。 |
| [02-index-to-core-definitions.md](02-index-to-core-definitions.md) | 在材料核对后筛选、排名、检查并生成 TeX。 |
| [scripts/validate_output.py](scripts/validate_output.py) | 只读格式检查器，默认读取本目录 `template.tex`。 |

### 使用示例

向可访问文件的执行者提供整个包及材料，发送：

~~~text
请执行 ./prompts/workflow.md，完整读取同目录四件套。
INPUT_DIRS：
- ./library/Differential Geometry
- ./library/Topology
~~~

`Differential Geometry` 可包含书目和书籍 PDF；`Topology` 也可只有 `.core-definitions-work/indexes/` 与现有 manifest。预期输出分别为：

~~~text
library/Differential Geometry/Differential Geometry_core_definitions.tex
library/Topology/Topology_core_definitions.tex
~~~

`CLASS` 取学科文件夹完整名称，保留空格和大小写；带标签附件使用同标签工作目录。各学科独立处理。该例说明输入输出约定，不代表本包附带书籍或已验证示例排名。

只需第一步时，将调用入口改为 `01-extract-indexes.md`；已有材料、只需重新筛选排名时改为 `02-index-to-core-definitions.md`。两者仍需完整四件套。已有缓存可位于其他清晰布局；不需要为调整排名而重提取有效 Index。

### 检查与交付

从本包目录运行，例如：

~~~sh
python scripts/validate_output.py "../library/Differential Geometry/Differential Geometry_core_definitions.tex"
~~~

最终 TeX 只含固定标题、允许的宽泛英文节标题、自动连续编号和英文概念名。默认无 section，最多 3 个且不能改变排名或重置编号。模板使用 `article`、`cmap`、`fontenc`、`inputenc`、`geometry`、`amsmath`、`amssymb`、`enumitem`，生成文件独立于本包。

必须保留与最终名次、名称、层次对应的真实 Index 来源记录；覆盖旧输出前创建不冲突的备份并核验字节一致。先检查实际完整候选，再替换结果。格式检查不证明来源或数学质量，还需实际编译并检查截断、缺字和编号。通过、未执行和失败分别记录。

每学科交付一个 TeX，PDF 仅在用户要求时交付。工作索引、来源记录和备份留在缓存；缺页、版次差异、未决材料及未完成检查在聊天中简短说明，不写进 TeX。缺席原件不能声称已验证，部分来源不能称完整，无可用 Index 时不编造清单。

## English

Version: **0.3.0**. Copy this entire directory to use it independently of an installed skill. The execution environment needs access to the supplied materials. The checker uses Python 3's standard library; compilation and visual inspection require a standard compiler such as pdfLaTeX and a PDF renderer or viewer. Source PDFs require page-reading/extraction tools, and scanned Index pages additionally require OCR.

The pack selects core and important English concept names from all usable Indexes and ranks them globally within each user-designated subject. It accepts book PDFs, Index-only excerpts or caches, and clearly labelled attachments. Neither `main.tex` nor original PDFs are mandatory. Do not read book bodies or add unsupported candidates from general knowledge or old generated lists. Ranks are within-subject positions, not theorem scores or a scale shared across subjects.

### Mandatory quartet and entrypoints

Before execution, read [core-definitions-rules.txt](core-definitions-rules.txt), [prompt.txt](prompt.txt), [preamble.tex](preamble.tex) and [template.tex](template.tex) completely. Keep them unchanged during generation. Together they are the complete specification; no stage Markdown replaces any of these files. The complete template already embeds the preamble: do not load the fragment again or compile it on its own.

- [workflow.md](workflow.md) runs the full workflow.
- [01-extract-indexes.md](01-extract-indexes.md) only accounts for inputs and reads/caches usable Index material.
- [02-index-to-core-definitions.md](02-index-to-core-definitions.md) selects, ranks, checks and saves the TeX after the input review.
- [scripts/validate_output.py](scripts/validate_output.py) checks structural format without modifying the output. Its default template is `template.tex` in this directory.

### Usage example

Supply the pack and source materials to an executor with file access, then request:

~~~text
Execute ./prompts/workflow.md and read the complete quartet beside it.
INPUT_DIRS:
- ./library/Differential Geometry
- ./library/Topology
~~~

The first folder may contain a bibliography and book PDFs; the second may contain only `.core-definitions-work/indexes/` and an existing manifest. The expected outputs are:

~~~text
library/Differential Geometry/Differential Geometry_core_definitions.tex
library/Topology/Topology_core_definitions.tex
~~~

`CLASS` is the full subject-folder name, preserving spaces and capitalization. For labelled attachments, use a working folder with that label. Process subjects independently. This example illustrates the input/output contract; no books or verified example rankings are included.

For stage one alone, invoke `01-extract-indexes.md`. To repeat selection and ranking on existing material, invoke `02-index-to-core-definitions.md`. Both still require the complete quartet. Reuse other clear cache layouts and do not re-extract valid Indexes merely because the ranking rules change.

### Checks and delivery

From this package directory, for example:

~~~sh
python scripts/validate_output.py "../library/Differential Geometry/Differential Geometry_core_definitions.tex"
~~~

The final TeX contains only the fixed title, permitted broad English section headings, automatic continuous ranks and English concept names. Use no sections by default, at most three without reordering items or resetting ranks. The template uses `article`, `cmap`, `fontenc`, `inputenc`, `geometry`, `amsmath`, `amssymb` and `enumitem`; the generated file is independent of this pack.

Retain factual Index provenance corresponding to every final rank, name and tier. Before replacing an output, create a non-colliding backup and verify identical bytes. Check the actual complete candidate before replacement. The checker does not prove source support or mathematical quality: compile and visually inspect the candidate for clipping, missing glyphs and numbering. Record passed, unperformed and failed checks separately.

Deliver one TeX per subject; deliver PDFs only when requested. Keep working Indexes, provenance and backups in the cache. Briefly disclose source gaps, edition differences, unresolved material and incomplete checks outside the TeX. Do not claim to have verified absent originals or call partial sources complete; do not fabricate a list when no Index is usable.
