# Prompt Optimization Agent for Codex

`prompt-optimization-agent` 是一个面向 Codex 的本地插件。它通过 `$optimize-prompts` Skill 审计、重构、比较和静态验证 Prompt。

它默认不会执行优化后的 Prompt，也不会把未经实证比较的改写声称为“已经证明更优”。

## 安装

插件已经登记到默认个人 marketplace：

```text
~/.agents/plugins/marketplace.json
```

插件源码位于：

```text
~/plugins/prompt-optimization-agent
```

在终端安装或重新安装：

```bash
codex plugin add prompt-optimization-agent@personal
```

安装后新建一个 Codex 对话，使 Skill 和插件元数据进入新线程。

## 快速开始

显式调用 Skill：

```text
使用 $optimize-prompts 优化下面的 Prompt，不要执行优化后的任务：

分析我们的销售下降，并给出专业建议。
```

典型输出包括：

1. 优化后 Prompt；
2. 关键修改；
3. 新增假设和限制；
4. 必要时出现的决策分叉；
5. 与实际验证强度匹配的结论标签。

## 四种使用模式

### 1. 审计但不改写

```text
使用 $optimize-prompts 仅审计下面的 Prompt。检查目标、输入、输出、歧义、冲突、可执行性和可验证性，不要改写。

<粘贴 Prompt>
```

### 2. 审计并优化

```text
使用 $optimize-prompts 审计并优化下面的 Prompt。保持有文本证据的原始意图；重大选择不要静默决定，可以参数化或列出候选版本。

<粘贴 Prompt>
```

### 3. 比较两个版本

```text
使用 $optimize-prompts 比较 Prompt A 和 Prompt B。先建立共同评价标准，再区分信息增益、结构增益和新增约束。没有执行测试时不要宣称哪个版本已经实证更优。

Prompt A:
...

Prompt B:
...
```

### 4. 静态验证

```text
使用 $optimize-prompts 静态验证下面的 Prompt。报告不变量、冲突、未授权的重大语义变化、运行环境依赖和无法由 Prompt 单独保证的事项。

<粘贴 Prompt>
```

## 决策分叉如何工作

插件把语义变化分成五级：

| 等级 | 含义 | 默认处理 |
|---|---|---|
| S0 | 纯措辞或排版 | 自动处理 |
| S1 | 把已有含义明确表达 | 自动处理，必要时披露 |
| S2 | 可逆、低影响默认值 | 标记为假设 |
| S3 | 改变范围、方法、交付物或评价 | 请求授权或保留候选 |
| S4 | 改变目标、风险、权利、合规立场或敏感数据使用 | 必须由有权主体决定 |

例如，“面向技术人员”与“面向管理层”会改变内容粒度，通常属于需要明确处理的决策，而不是简单措辞选择。

## 结论标签

插件按实际验证强度使用标签：

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

## 生成机器可读 POA Case

如需审计工件，可以要求：

```text
使用 $optimize-prompts 优化下面的 Prompt，并同时输出符合 poa-case.schema.json 的 POA Case JSON。
```

保存 JSON 后运行：

```bash
python3 ~/plugins/prompt-optimization-agent/skills/optimize-prompts/scripts/validate_case.py ./poa-case.json
```

机器可读输出：

```bash
python3 ~/plugins/prompt-optimization-agent/skills/optimize-prompts/scripts/validate_case.py ./poa-case.json --json
```

校验器会检查：

- 必需字段和类型；
- 状态是否合法；
- 未决重大决策是否错误进入编译或批准状态；
- S3/S4 变更是否具有授权记录；
- S3/S4 保证标签是否具有相应证据字段；
- 强制性领域约束是否缺乏直接支持。

校验器不会证明事实正确、领域规范适用、任务安全或候选 Prompt 实际性能更好。

## 当前能力边界

当前版本是 Skill 驱动的 MVP：

- 支持语义规格化、审计、决策门控和静态验证；
- 可以使用 Codex 当前可用的检索和文件工具核验资料；
- 不包含持久化 POA 服务、多人审批台或自动基准运行器；
- 不会用 Prompt 代替权限、Schema、代码、组织流程或专业人员；
- 高风险任务只能生成受限候选和复核要求，不能自动取得专业授权。

## 更新插件

修改插件文件后，按 Codex 本地插件开发流程刷新版本并重新安装：

```bash
python3 ~/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py ~/plugins/prompt-optimization-agent
codex plugin add prompt-optimization-agent@personal
```

然后开启新对话进行测试。

## 建议测试提示

低风险示例：

```text
使用 $optimize-prompts 优化：“写一份专业的竞品分析。”
```

多领域示例：

```text
使用 $optimize-prompts 审计一个根据患者数据自动决定保险赔付的 Prompt。不要生成自动决策版本；指出需要哪些权限、证据和人工复核。
```

时效性示例：

```text
使用 $optimize-prompts 优化一个要求依据最新官方 API 文档生成代码的 Prompt。无法确认当前版本时必须保留限制。
```
