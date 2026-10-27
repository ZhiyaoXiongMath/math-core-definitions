# math-core-definitions

[English](README.en.md) | 中文

面向需要整理数学概念清单的读者和研究者的 Codex skill。按用户指定的学科范围，从全部可用书籍 Index 中筛选核心与重要概念、规范英文名称并全局排名。每个学科独立生成可编译的 `CLASS_core_definitions.tex`，只列自动编号和概念名称，不解释定义。

当前版本：**0.3.0**，以 [SKILL.md](SKILL.md) 的 `metadata.version` 为准。

## 主要功能与边界

- 接受书籍 PDF、Index 摘录、转移缓存及带明确学科标签的附件。`main.tex` 和原 PDF 均非必需；有书目或 manifest 时用来识别书籍，没有时盘点实际输入。
- 复用可读缓存，重定位历史路径。有 PDF 时仅修复受影响的索引部分；只读必要的封面、目录、书签和 Index 页，不读正文、不做整书提取或 OCR，不自动下载书籍。
- 读完全部可用主题索引及含概念名称的符号索引，保留父子条目和交叉引用。所供 Index 决定候选依据，用户学科范围决定重要性；不从常识或旧生成清单补候选。
- 统一准入标准，合并真正同义项；每个特例、构造和可复用工具须独立达到核心或重要标准，不设数量、书籍或主题配额。
- 所有核心概念先于所有重要概念，各层按对主要理论、重大结果和方法的结构性作用排序。仅在无法可靠区分重要性时按规范英文名字母顺序打破并列。
- **必须保留内部来源记录**：将最终名次、名称、层次对应到至少一个真实 Index 条目的书籍标识、缓存文件和可用位置，并保留已知同义合并的来源链接。
- 使用固定模板；默认无 section，最多 3 个宽泛英文 section，只能切分既有排名，不能重排条目或重置编号。一项一源码行。
- 覆盖旧结果前创建不冲突的备份并核验字节一致；先检查候选再替换。保留来源文件、索引和工作记录，PDF 仅在用户要求时交付。
- 提供只读 Python 格式检查器和可独立复制使用的[提示词包](prompts/README.md)。

这是由 Codex 执行的技能工作流；脚本只检查格式，数学筛选与来源复核由模型完成。名次是学科内的序数，不是数值评分，不跨学科比较，也不代表具体定理的质量、创新性或证明深度。频次、难度、基础性和教学顺序不提供自动优先权。

## 环境要求

- 能读取材料并执行命令的 Codex 环境。
- Python 3：格式检查器仅使用标准库，不需要额外 Python 包。
- 处理原 PDF 时需要 PDF 页面读取和文本提取工具；扫描索引另需索引页渲染与 OCR 能力。只有可读 Index 缓存时，不要求补交原 PDF。
- 用于验证实际输出的标准 LaTeX 编译器，例如 pdfLaTeX，以及 PDF 渲染或查看工具。模板使用 `article`、`cmap`、`fontenc`、`inputenc`、`geometry`、`amsmath`、`amssymb`、`enumitem`。
- 使用者自行提供资料。本仓库不包含书籍、提取出的 Index 或生成清单。

## 安装

将仓库克隆为 Codex skills 目录中的 `math-core-definitions`。若已存在同名目录，先检查现有内容，不要直接覆盖。

PowerShell：

~~~powershell
$skillsRoot = if ($env:CODEX_HOME) {
    Join-Path $env:CODEX_HOME 'skills'
} else {
    Join-Path $env:USERPROFILE '.codex\skills'
}
New-Item -ItemType Directory -Force -Path $skillsRoot | Out-Null
git clone https://github.com/ZhiyaoXiongMath/math-core-definitions.git (Join-Path $skillsRoot 'math-core-definitions')
~~~

macOS / Linux：

~~~sh
if [ -n "$CODEX_HOME" ]; then
    skills_root="$CODEX_HOME/skills"
else
    skills_root="$HOME/.codex/skills"
fi
mkdir -p "$skills_root"
git clone https://github.com/ZhiyaoXiongMath/math-core-definitions.git "$skills_root/math-core-definitions"
~~~

随后在 Codex 中调用 `$math-core-definitions` 并提供资料路径或带明确学科标签的附件。默认不创建新聊天。

## 使用与输入输出示例

以下是布局示例，实际资料由使用者提供；第二个学科仅有缓存：

~~~text
library/
├── Differential Geometry/
│   ├── main.tex
│   └── differential-geometry.pdf
└── Topology/
    └── .core-definitions-work/
        ├── index-manifest.json
        └── indexes/
            └── topology-index.txt
~~~

在能访问这些路径的 Codex 聊天中输入：

~~~text
$math-core-definitions
请处理以下学科目录：
./library/Differential Geometry
./library/Topology
~~~

预期交付：

~~~text
library/Differential Geometry/Differential Geometry_core_definitions.tex
library/Topology/Topology_core_definitions.tex
~~~

`CLASS` 取学科文件夹的**完整名称，保留空格和大小写**；文档标题始终为 `Core Mathematical Definitions`。带标签附件使用该标签命名工作目录。每个目录独立筛选和排名，不移动书籍或跨目录重分类；同一概念可出现在不同学科清单中。

工作缓存保留索引、材料状态、最终来源对应记录及必要备份，可沿用合理的已有布局，不强制固定 schema。生成列表的结构例如：

~~~latex
\begin{enumerate}[series=definitions]
\item Smooth manifold
\item Tangent bundle
\end{enumerate}
~~~

此片段只展示格式，不声称已从示例 PDF 提取材料或验证这些概念的实际名次。实际名单必须有 Index 依据。

## 不安装技能：使用独立提示词

[独立提示词包](prompts/README.md) 包含同版完整四件套、阶段入口和检查器，可将整个 `prompts/` 文件夹复制到其他位置使用，不依赖技能安装目录。

~~~text
请执行 ./prompts/workflow.md，完整读取同目录四件套。
INPUT_DIRS：
- ./library/Differential Geometry
- ./library/Topology
~~~

[第一步](prompts/01-extract-indexes.md) 可单独用于核对、提取和缓存 Index；[第二步](prompts/02-index-to-core-definitions.md) 可用于基于现有材料筛选、排名和生成文件。两个入口都必须连同四件套使用，阶段 Markdown 不内嵌或替代完整规范。

## 规范、检查与验证范围

开始任务前完整读取 [core-definitions-rules.txt](references/core-definitions-rules.txt)、[prompt.txt](references/prompt.txt)、[preamble.tex](assets/preamble.tex) 和 [template.tex](assets/template.tex)。四件套是完整规范，辅助说明不能缩减其中规则；生成期间保持原样。模板已内嵌导言区，不再次加载 `preamble.tex`，生成的完整 TeX 不依赖技能或提示词包。

在仓库根目录对实际完整候选运行检查，例如：

~~~sh
python scripts/validate_output.py "library/Differential Geometry/Differential Geometry_core_definitions.tex"
~~~

格式检查涵盖固定模板、0–3 个 section、连续自动编号语法、一项一行、占位项及常见禁用命令。之后明确选择同一完整候选，用 pdfLaTeX 等编译并查看渲染结果，检查截断、缺字和编号。可先在工作缓存临时目录以最终文件名编译，检查后原样复制；不要用 `main.tex`、导言片段或旧输出代替。区分通过、未执行和失败，编译器不可用不等于编译失败。

本版本已通过 14 个格式检查器测试方法，并完成一个仅有缓存的合成材料示例：17 个条目、最终来源对应、旧文件备份、实际 pdfLaTeX 编译和渲染检查。该验证不代表真实书籍的端到端提取测试，也不证明数学排名质量；测试产生的私人工作文件不随仓库发布。

索引可能有缺页、OCR 疑点或版次差异，应如实记录并在交付时简短披露。缓存哈希相符只证明字节一致，不能证明 OCR 正确或缺席原书的完整性。部分材料可支持有限范围结果，不能称为完整；没有任何可用 Index 时不生成清单。TeX 中不写解释、来源、层次、分数或报告，内部记录留在工作缓存。

修改规范时应同步更新技能、独立提示词包的四件套、阶段说明及检查器。
