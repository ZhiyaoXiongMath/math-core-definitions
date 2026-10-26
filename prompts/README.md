# 数学定义名称提取与重要性排名提示词

版本：0.2.0。提供一个或多个含 main.tex 与数学书籍 PDF 的文件夹，即可在每个目录生成 core_definitions.tex。文件夹已代表用户分好的大类。

流程严格分两步：先提取并缓存各书书末 Index，再根据 Index 筛选核心定义和重要定义、合并同义项，并按重要性全局排序。

排序用于为后续定理评价提供概念重要性参考，不直接计算定理质量。输出只包含英文名称和连续排名编号，不写定义、解释、等级标签或数值评分。

## 本版的排序与分段规则

- 核心定义在前，重要定义在后，各层次内按重要性递减排列。
- 主要依据是概念对本类别中心问题、主要理论、主要定理与关键方法的结构性作用，不以出现频率、难度或教学先后机械排名。
- 编号从 1 连续递增，1 为最高；它表示顺序，不表示数值分数。
- 默认不使用 section。确有必要时最多 3 个，3 是上限而不是目标。
- 分段不能改变全局排名，编号不能在 section 中重置；无法自然分段时直接使用一份总列表。
- 每个输入目录独立排名，不跨类别重新归类或删除重复概念。

## 文件说明

| 文件 | 用途 |
| --- | --- |
| [workflow.md](workflow.md) | 主入口，串联两步流程；用户要求时为各目录派发新对话。 |
| [01-extract-indexes.md](01-extract-indexes.md) | 第一步，只提取和缓存 Index，可单独调用。 |
| [02-index-to-core-definitions.md](02-index-to-core-definitions.md) | 第二步，完整的筛选、全局排名和输出提示词，内嵌模板，可单独调用。 |
| [assets/core_definitions.tex](assets/core_definitions.tex) | 默认无 section 的固定 LaTeX 模板。 |
| [scripts/validate_output.py](scripts/validate_output.py) | 检查模板、0–3 个 section 与连续编号语法。 |
| README.md | 使用说明。 |

整个文件夹可直接复制复用，不依赖已安装的 skill。两个阶段 Markdown 也能分别使用；只提供第二步 Markdown 时，可使用其中内嵌的完整模板。

## 准备输入

~~~text
某个已分类的资料文件夹/
├── main.tex
├── 书籍一.pdf
└── 书籍二.pdf
~~~

main.tex 确定书目范围。Index 指书末数学索引，书前目录只用于定位。不要通读正文，不要先提取整书文本再查找 Index，也不要进行整书 OCR。

## 在当前对话执行

替换路径后发送：

~~~text
请执行 <提示词目录的绝对路径>/workflow.md。
INPUT_DIR：<含 main.tex 和 PDF 的资料文件夹地址>
MODE：直接执行

先缓存 Index，再生成按重要性全局排名的 core_definitions.tex。
默认不分 section，最多 3 个，排名编号连续。
~~~

多个目录时将 INPUT_DIR 改为 INPUT_DIRS，并逐行列出路径。

## 派发独立新对话

~~~text
请执行 <提示词目录的绝对路径>/workflow.md。
INPUT_DIRS：
- <第一个资料文件夹地址>
- <第二个资料文件夹地址>

MODE：每个目录派发一个新本地对话
MODEL：gpt-6-astra
THINKING：ultra

每个对话依次完成 Index 缓存和核心定义重要性排名。
默认不分 section，最多 3 个，编号跨 section 连续。
返回新对话入口并跟进至交付。
~~~

模型及推理档位可以在调用时指定，执行环境须核实支持情况。

## 单独使用某一步

仅提取索引：

~~~text
请执行 <提示词目录的绝对路径>/01-extract-indexes.md。
INPUT_DIR：<资料文件夹地址>
本次只提取并缓存 Index。
~~~

已有索引，仅重新筛选和排名：

~~~text
请执行 <提示词目录的绝对路径>/02-index-to-core-definitions.md。
INPUT_DIR：<资料文件夹地址>
复用已有 Index，按重要性重新排名并生成 core_definitions.tex。
~~~

缓存不在默认位置时可指定 INDEX_DIR 和 MANIFEST_PATH。不需要为调整排名规则重新读取书籍。

## 输出与检查

~~~text
资料文件夹/
├── main.tex
├── 原有书籍.pdf
├── core_definitions.tex
└── .core-definitions-work/
    ├── index-manifest.json
    └── indexes/
~~~

使用完整提示词包时，可运行：

~~~text
python <提示词目录>/scripts/validate_output.py <资料目录>/core_definitions.tex
~~~

检查器验证固定格式、章节上限和连续编号结构，不评判数学重要性；重要性顺序仍需对照索引和筛选规则复核。输出还需编译检查，不另交付 PDF。

本版已统一文件名为 core_definitions.tex。若使用了旧版的 core-definitions.tex，新结果使用新文件名，旧文件不自动删除。

索引缺失或不可读时如实记录并继续处理可用材料。基于 Index 的清单不声称覆盖正文中未被索引收录的全部定义。
