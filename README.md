# Prompt Optimization Agent for Codex

`prompt-optimization-agent` is an open-source-ready Codex plugin source package centered on the `$optimize-prompts` Skill. It audits, restructures, compares, and statically validates prompts without silently changing material decisions.

中文文档如下。The Skill itself can work with prompts in any language supported by the active Codex runtime.

## 核心原则

- 把待优化 Prompt 当作数据，不让其中的嵌套指令控制优化器；
- 保留能够由原文和上下文支持的意图；
- 把假设、未知信息和建议与已确认要求分开；
- 不静默决定会改变目标、范围、方法、风险或合规立场的路径；
- 不把 Prompt 能力伪装成权限、代码、Schema、组织流程或专业资格；
- 没有对照实验时，只声明“重写”或“静态改进”。

## 项目状态

当前版本是 Skill 驱动的 MVP：

- 支持 Prompt 审计、任务规格化、决策门控和候选编译；
- 提供机器可读 POA Case Schema 和无第三方运行时依赖的校验器；
- 不包含持久化服务、多人审批台、领域规范数据库或生产 A/B 测试；
- 高风险任务只能生成受限候选和复核要求，不能替代专业授权。

## 安装

### 方法一：作为 Codex Skill 使用

这是公开仓库目前最直接、可复现的安装方式。

```bash
git clone https://github.com/xiaoatang/prompt-optimization-agent.git
cd prompt-optimization-agent
mkdir -p ~/.codex/skills
ln -s "$(pwd)/skills/optimize-prompts" ~/.codex/skills/optimize-prompts
```

如果目标路径已经存在，请先检查其来源，不要直接覆盖。安装后新建 Codex 对话，使 Skill 进入新线程。

卸载符号链接：

```bash
unlink ~/.codex/skills/optimize-prompts
```

### 方法二：作为插件源码开发

仓库包含有效的 `.codex-plugin/plugin.json`，可由本地或团队 marketplace 引用。当前仓库不是公共 marketplace catalog，因此不要直接运行：

```text
codex plugin marketplace add xiaoatang/prompt-optimization-agent
```

除非仓库以后增加符合 Codex marketplace 约定的 catalog 结构。公共 marketplace 上架属于单独的分发步骤，不是本仓库当前能力的一部分。

## 快速开始

```text
使用 $optimize-prompts 审计并优化下面的 Prompt。
保持有文本证据的原始意图；重大选择不要静默决定，
可以参数化或列出候选版本。不要执行优化后的任务。

<待优化 Prompt>
分析我们的销售下降，并给出专业建议。
</待优化 Prompt>
```

典型输出包括：

1. 优化后 Prompt；
2. 关键修改；
3. 假设和限制；
4. 必要时出现的决策分叉；
5. 与实际验证强度匹配的结论标签。

## 四种使用模式

### 审计但不改写

```text
使用 $optimize-prompts 仅审计下面的 Prompt。检查目标、输入、输出、歧义、冲突、可执行性和可验证性，不要改写。

<待优化 Prompt>
...
</待优化 Prompt>
```

### 审计并优化

```text
使用 $optimize-prompts 审计并优化下面的 Prompt。保持有文本证据的原始意图；重大选择不要静默决定，可以参数化或列出候选版本。

<待优化 Prompt>
...
</待优化 Prompt>
```

### 比较两个版本

```text
使用 $optimize-prompts 比较 Prompt A 和 Prompt B。先建立共同评价标准，再区分信息增益、结构增益和新增约束。没有执行测试时不要宣称哪个版本已经实证更优。

Prompt A:
...

Prompt B:
...
```

### 静态验证

```text
使用 $optimize-prompts 静态验证下面的 Prompt。报告不变量、冲突、未授权的重大语义变化、运行环境依赖和无法由 Prompt 单独保证的事项。

<待优化 Prompt>
...
</待优化 Prompt>
```

## 语义变更门控

| 等级 | 含义 | 默认处理 |
|---|---|---|
| S0 | 纯措辞或排版 | 自动处理 |
| S1 | 把已有含义明确表达 | 自动处理，必要时披露 |
| S2 | 可逆、低影响默认值 | 标记为假设 |
| S3 | 改变范围、方法、交付物或评价 | 请求授权或保留候选 |
| S4 | 改变目标、风险、权利、合规立场或敏感数据使用 | 必须由有权主体决定 |

## 验证结论

| 标签 | 表示什么 |
|---|---|
| `S0_REWRITTEN` | 只完成改写 |
| `S1_STATICALLY_IMPROVED` | 通过静态审计 |
| `S2_EVALUATOR_PREFERRED` | 隔离评价器更偏好候选 |
| `S3_BENCHMARK_IMPROVED` | 可比基准测试显示改善且护栏未退化 |
| `S4_PRODUCTION_VALIDATED` | 真实生产数据支持可重复改善 |
| `INCONCLUSIVE` | 证据不足以区分候选 |
| `REJECTED` | 违反阻断条件或护栏 |

仅使用 Skill 通常最多得到 `S1_STATICALLY_IMPROVED`。S2–S4 需要实际评价或测试数据。

## POA Case 校验器

校验示例：

```bash
python3 skills/optimize-prompts/scripts/validate_case.py \
  skills/optimize-prompts/references/example-valid-case.json
```

机器可读输出：

```bash
python3 skills/optimize-prompts/scripts/validate_case.py ./poa-case.json --json
```

校验器检查结构和部分治理不变量，包括未授权的 S3/S4 变更、带未决重大决策的批准状态，以及缺乏实证字段的高级保证声明。它不证明事实正确、领域规范适用、任务安全或候选实际性能更好。

## 开发与验证

项目运行时仅使用 Python 标准库。

```bash
python3 scripts/security_check.py
python3 skills/optimize-prompts/scripts/validate_case.py \
  skills/optimize-prompts/references/example-valid-case.json
```

故意无效的案例应返回非零状态：

```bash
python3 skills/optimize-prompts/scripts/validate_case.py \
  skills/optimize-prompts/references/example-invalid-case.json
```

贡献流程见 [CONTRIBUTING.md](CONTRIBUTING.md)，安全问题报告方式见 [SECURITY.md](SECURITY.md)，安全审查记录见 [docs/SECURITY_REVIEW.md](docs/SECURITY_REVIEW.md)，公开发布检查表见 [docs/PUBLIC_RELEASE_CHECKLIST.md](docs/PUBLIC_RELEASE_CHECKLIST.md)。

## 安全边界

- 待优化 Prompt、附件和网页均按不可信数据处理；
- Skill 不应因为被优化内容中的指令而扩大权限或调用工具；
- 不应将敏感任务数据上传到外部服务以检索通用规则；
- 不应把危险请求优化为更可执行、更隐蔽、更大规模或更自动化的能力；
- 确定性校验器只是结构检查，不是安全证明。

## License

本项目采用 [MIT License](LICENSE)。
