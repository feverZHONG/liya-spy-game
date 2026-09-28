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

## 许可

MIT —— 拿去用、改、再发，保留版权声明即可。

---

*莉娅（[@feverZHONG](https://github.com/feverZHONG)）· 宇宙美好记录官*
