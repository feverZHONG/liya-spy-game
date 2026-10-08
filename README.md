# 谁是卧底 · 直播间裁判工具包

> 直播间版「谁是卧底」的完整裁判档：黑板规则、出题方法论、词库与验证流程、灵感来源、翻车分析，外加一个身份分配器 CLI。
> 规则档是原样搬的「黑板原文」——游戏进行时查它一眼就够。

## 这是什么

| 你要干什么 | 打开 |
|:---|:---|
| 游戏进行中查规则（身份 / 胜负 / 禁用） | `rules.md` |
| 要出题了，怎么造好题 | `methodology.md` |
| 有了候选词对，验证能不能用 | `verification.md` |
| 没题了，去哪找灵感 | `inspiration.md` |
| 有了一个角色，想找同类 | `tag-matching.md` |
| 要汇报结果（卡片格式） | `reporting.md` |
| 翻车了，要分析 | `crash-analysis.md` |
| 玩家抱怨 → 是哪类题的问题 | `references/player-feedback-signals.md` |

**两个特殊身份**：天使（同时知道两个词）、白板（只有共同点提示词，靠全场发言反推）。描述禁用红线、好题五要素、6 轮验证流程、按季扫描找题、翻车分类表，都在上面这些文件里。

## 身份分配器

```bash
# 名单模式（推荐）：自动算人数、随机发身份到具体人头
python3 scripts/spy.py --list "1【甲】2【乙】3【丙】4【丁】"

# 按人数 / 改比例 / 固定身份 / 按人排除
python3 scripts/spy.py --total 12 --ratio 4:1
python3 scripts/spy.py --list "..." --fixed "3:天使"
python3 scripts/spy.py --list "..." --exclude-angel "2,7" --no-whiteboard

# 想预览分布（默认只出一轮，别让玩家看见概率）
python3 scripts/spy.py --list "..." -n 5
```

**纪律**：默认只输出一轮的最终名单。卧底占比 15%~25% 合理，超过 30% 好人压力大。

## 词库

- `references/可用词库.md` —— 已实况验证 + 推荐新增 + 待观察
- `references/二次元卧底词库_v3.md` —— 词库拆分索引
- `references/新番出题候选_2024_2026.md` —— 按季度整理的候选作品

**出题史与淘汰记录不在本仓**——那是直播记录（哪题出过、哪题翻车），属出题方私档。本仓给的是词库与**怎么挑词**的方法。

## 提思路 / 提修正

- 好题、新玩法、验证流程的改进 → 开 [Issue](https://github.com/feverZHONG/liya-spy-game/issues)
- 想直接改 → Fork + PR

## 姊妹仓库

**同一族（聊天里能玩的东西）**

- [liya-chat-game-referee](https://github.com/feverZHONG/liya-chat-game-referee) —— 回合制棋盘游戏裁判：扫雷 / 五子棋 / 大话骰 / 骗子牌 / 掷骰
- [liya-sea-turtle-soup](https://github.com/feverZHONG/liya-sea-turtle-soup) —— 海龟汤：推理方法论 + 档案流水线

**莉娅名下其他**

- [liya-vision-recognition-traps](https://github.com/feverZHONG/liya-vision-recognition-traps) —— 视觉模型识图陷阱手册
- [liya-subtraction-skill](https://github.com/feverZHONG/liya-subtraction-skill) —— 技能库做减法的方法论
- [liya-persona-authoring](https://github.com/feverZHONG/liya-persona-authoring) —— 人格 / 身份文件的写法
- [liya-sillytavern-cards](https://github.com/feverZHONG/liya-sillytavern-cards) —— 酒馆角色卡写法与工具
- [liya-sillytavern-worldbook](https://github.com/feverZHONG/liya-sillytavern-worldbook) —— 酒馆世界书（Lorebook）：触发链源码实证 + 触发体检 / 模拟 / 生成工具
- [liya-delegation-and-verification](https://github.com/feverZHONG/liya-delegation-and-verification) —— 委派与验收：给子代理写任务书、并行隔离、把「自报」验成事实
- [liya-tavern-card-refinement](https://github.com/feverZHONG/liya-tavern-card-refinement) —— 酒馆角色卡精修：7 字段清单 + 槽位归位 + 6 类断言校验 + 可用性验收（不装酒馆也能量）
- [liya-prose-quality-metrics](https://github.com/feverZHONG/liya-prose-quality-metrics) —— 稿子读起来「平」怎么办：先量再改（对话占比·句长σ·台词宽度·标点谱·段均句）＋ 7 个工具
- [liya-ruozhiba-wordbank](https://github.com/feverZHONG/liya-ruozhiba-wordbank) —— 弱智吧题防御手册：中文互联网逻辑陷阱题 160 道逐题拆解 + 三连防御法（拆前提→指谬误→反杀）
- [liya-subtitle-proofreading](https://github.com/feverZHONG/liya-subtitle-proofreading) —— 字幕校对/重建/外挂 SRT：对照成稿逐处修正 + 按原文重建分块 + md→SRT + 多人语音 ASR 导出件解析（5 个纯标准库工具）
- [liya-corpus-line-mining](https://github.com/feverZHONG/liya-corpus-line-mining) —— 从本地语料／会话库挖可复用原句：候选池筛选 + 人审落库（纯标准库，零依赖）
- [liya-story-revision-plan](https://github.com/feverZHONG/liya-story-revision-plan) —— 小说全稿修订方案：评估／缺口清单／逐章大纲／信息融合／优先级（含标准模板）
- [liya-dev-workflow](https://github.com/feverZHONG/liya-dev-workflow) —— 开发全流程方法论：环境侦查／计划／spike／TDD／迭代脚本／调试／预提交审查／推送排障／同步验收
- [liya-news-verification](https://github.com/feverZHONG/liya-news-verification) —— 验证伞：轻量核查／交付前多源验证／链接危险识别／厂商官宣核实／链接考古（含 link_check 工具族）
- [liya-knowledge-persistence](https://github.com/feverZHONG/liya-knowledge-persistence) —— 知识持久化：信息该放记忆层／文件／技能库的分层规范（附记录完整性、语料减法、归档模式）
- [liya-incident-review](https://github.com/feverZHONG/liya-incident-review) —— 社群事件复盘：素材收集 → 时间线重构 → 交叉验证 → 矛盾管理（输出理解不输出建议）
- [liya-document-translation](https://github.com/feverZHONG/liya-document-translation) —— 论文与长文档翻译：提取全文 → 术语表 → 并行分章 → 质量抽查 → 归档
- [liya-source-code-investigation](https://github.com/feverZHONG/liya-source-code-investigation) —— 外部项目调查：源码审计 / 拆包分层 / 数据实测 / 身份链（结论导向，非取用）
- [liya-character-voice-simulation](https://github.com/feverZHONG/liya-character-voice-simulation) —— 角色声线推演：锚点表双向用——分队推演（隔离上下文）＋ 反查认说话人
- [liya-dialogue-system-builder](https://github.com/feverZHONG/liya-dialogue-system-builder)

## 许可

**双许可**——文档与代码分开：

- **代码**（`scripts/` 下的文件）：**MIT** —— 拿去用、改、再发，保留版权声明即可。
- **文档**（`SKILL.md`、`references/`、本 README 的正文）：**[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)** —— 可以自由使用、改编、连商用都行，**但要署名**（莉娅 / [@feverZHONG](https://github.com/feverZHONG)）并注明来源。

两份许可的全文：`LICENSE`（MIT）／`LICENSE-DOCS`（CC BY 4.0）。

---

*莉娅（[@feverZHONG](https://github.com/feverZHONG)）· 宇宙美好记录官*
