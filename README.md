# math-core-definitions

[English](README.en.md) | 中文

面向需要整理数学概念清单的读者和研究者的 Codex skill。输入一个或多个含 main.tex 参考书目和数学书籍 PDF 的本地文件夹；技能先提取并缓存各书书末 Index，再筛选、去重、按重要性全局排名，在每个文件夹内生成 core_definitions.tex。

输出只包含连续排名编号、核心与重要数学概念的英文名称，以及可选的宽泛英文主题标题，不解释定义。各文件夹代表使用者预先划分的类别，独立处理和排名。

当前版本：0.2.0，版本来源为 SKILL.md 的 metadata.version。

## 主要功能

- 按 main.tex 中的引用键、MR 编号、书名和作者匹配书籍 PDF。
- 仅提取索引及少量定位材料，不通读正文、不提取整书文本、不对整书 OCR。
- 保留索引页码、子条目和交叉引用，缓存来源及处理状态；有效缓存可复用。
- 根据 Index 筛选核心及重要概念，使用标准英文名称，在类别内部整合同义词和重复项。
- 核心定义在前、重要定义在后，各层次按重要性递减排序；连续编号从 1 开始，1 为最高。
- 按固定 article 模板输出 enumerate 名称列表。默认不分 section，最多 3 个；分段不能改变全局排名或重置编号。
- 提供只读的 Python 格式检查器，检查模板、章节上限、连续编号语法、重复项及示意占位内容。
- 附带可独立使用的两阶段 Markdown 提示词、模板和检查器，无需安装技能即可调用。
- 多目录时，每个目录生成一份独立清单。只有使用者明确要求时才创建新聊天。

这是由 Codex 执行的技能工作流，不是独立运行的 PDF 自动提取程序。脚本负责格式检查，数学筛选由模型完成。

排名用于为后续定理评价提供概念重要性参考。优先考虑概念对本类别中心问题、主要理论、主要定理及关键方法的结构性作用，不以出现频率、难度或教学先后机械排序。名次不是数值分数，不直接代表定理质量，跨类别的名次也不是统一尺度。

## 环境要求

- 能读取本地文件并执行命令的 Codex 环境。
- Python 3：运行格式检查器，仅使用标准库。
- 可用的 PDF 页面读取和文本提取工具；扫描索引另需索引页渲染和 OCR 能力。
- 用于最终验证的 LaTeX 编译工具，例如 Codex 的 compile_latex_document，或已安装的 LaTeX 环境。模板使用 article、fontenc、inputenc、geometry、amsmath、amssymb、enumitem。
- 使用者自行提供 main.tex 和对应书籍 PDF。本仓库不包含书籍、索引数据或生成结果。

## 安装

将仓库克隆为 Codex skills 目录中的 math-core-definitions。若已存在同名目录，先检查现有内容，不要直接覆盖。

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

随后在 Codex 中调用 $math-core-definitions，并提供资料文件夹路径。技能的默认流程不依赖固定学科、书籍数量、模型或机器专属路径。

## 使用与输入输出示例

准备资料，例如：

~~~text
library/
├── topology/
│   ├── main.tex
│   └── algebraic-topology.pdf
└── geometry/
    ├── main.tex
    └── differential-geometry.pdf
~~~

示例文件名仅说明目录布局，实际书籍由使用者提供。在能访问这些相对路径的 Codex 聊天中输入：

~~~text
$math-core-definitions
请处理以下文件夹：
./library/topology
./library/geometry
~~~

预期在每个输入目录新增：

~~~text
core_definitions.tex
.core-definitions-work/
├── index-manifest.json
└── indexes/
    └── 各书的索引文本及必要索引页图像
~~~

最终交付是两份 core_definitions.tex。每份清单整合本目录的可用索引，不跨文件夹重新归类；同一概念可以出现在不同类别中。原 main.tex 和 PDF 保留不变。

生成文档内的条目形式示例：

~~~latex
\begin{enumerate}[series=definitions]
\item Smooth manifold
\item Tangent bundle
\end{enumerate}
~~~

示例展示预期结构，不代表仓库附带了上述书籍、已对这些示例 PDF 完成提取，或已验证示例概念的实际名次。实际排名必须依据各目录的索引材料和筛选规则。

## 不安装技能：使用独立提示词

获取仓库后，可直接使用 [prompts/README.md](prompts/README.md) 中的独立提示词包；同样需要可访问本地资料并处理 PDF、TeX 的执行环境。完整包可复制复用，不依赖技能安装目录。

~~~text
请执行 ./prompts/workflow.md。
INPUT_DIRS：
- ./library/topology
- ./library/geometry
MODE：直接执行
~~~

每个目录仍依次完成索引缓存和排名，输出一份 core_definitions.tex。也可单独调用 [第一步](prompts/01-extract-indexes.md) 缓存 Index，或在已有缓存上调用 [第二步](prompts/02-index-to-core-definitions.md) 重新筛选和排名。第二步 Markdown 内嵌完整模板，可单独提供给执行者。

## 模板、验证与后续调整

- assets/core_definitions.tex 是固定模板。导言区、标题及页面设置保持一致，只填写已排名的名称和可选主题标题。
- references/extract-indexes.md 规定索引提取和缓存。
- references/select-definitions.md 规定筛选、整合、全局重要性排名和输出要求。
- scripts/validate_output.py 只读检查生成的 TeX。运行示例：

~~~sh
python scripts/validate_output.py path/to/core_definitions.tex
~~~

格式检查通过后，技能继续用可用的 LaTeX 工具检查编译。编译应明确选择 core_definitions.tex，避免误编译同目录的 main.tex。内部编译预览不作为 PDF 交付。

如需分段，先形成全局排名，再将其切成最多 3 个自然、连续的大块。每节恰有一个 enumerate，首个列表使用 [series=definitions]，后续列表使用 [resume=definitions]。无法保持排名自然分段时，直接采用默认的无 section 列表。

本版本已验证技能结构、模板和无章节/三章节示例编译，以及格式检查器的接受/拒绝行为；未将真实数学书籍的端到端提取或数学排名质量作为自动化测试。

后续细化输出格式时，应同步修改技能和独立提示词包中的模板、第二步说明和格式检查器。

## 范围与限制

- Index 指书末数学主题索引，不是书前目录。
- 清单覆盖已提取索引中的候选概念，不保证覆盖正文里未被索引收录的全部定义。
- 缺少 PDF、未定位到索引或部分页面不可读时，记录真实状态并继续处理可用材料；没有任何可用索引时不凭常识生成清单。
- 不自动下载书籍。生成结果不包含定义内容、页码、引用、等级标签、数值评分或重要性说明，也不额外交付 PDF 或审查报告。
- 格式检查不能判定数学概念的重要性、排名正确性、同义关系或筛选是否完整，这些仍需模型进行索引依据下的审查。
