---
name: spy-game
tier: T2  # T分级: T2=直接做 / T1=先请示 / T0=一律拒
description: 谁是卧底直播游戏——完整裁判工具包。规则·出题方法论·验证·灵感·翻车分析。直播间出题向。
tags: []
related_skills: [ruozhiba-wordbank]
---

# 谁是卧底 · 技能索引

> 直播间实体规则 + 出题方法论 + 裁判工具包。
> 跟 `ruozhiba-wordbank` 是两回事——那个是贴吧砸场子防御用的。

---

## 功能文件速查

触发对应场景，读对应文件：

| 场景 | 打开 | 定位 |
|------|------|------|
| 游戏进行中，查规则 | `rules.md` | 黑板原文·身份卡·胜负·禁用 |
| 要分配身份 | `rules.md` → 裁判工具 | `scripts/spy.py` 用法 |
| 要出题了，怎么造好题 | `methodology.md` | 核心公式·好题五要素·失败模式·白板 |
| 有了候选对，验证能不能用 | `verification.md` | 6轮多轮验证·前置双筛·零索引·跨源 |
| 没题了，去哪找灵感 | `inspiration.md` | 用户认知库·按季扫描·配向策略 |
| 有了一个角色，想找同类 | `tag-matching.md` | 属性拆解→逐维搜索→匹配排序 |
| 要汇报结果 | `reporting.md` | 卡片格式·emoji纪律 |
| 翻车了，要分析 | `crash-analysis.md` | 翻车分析·新规全量回顾·玩家反馈 |

---

## 数据文件

| 文件 | 用途 |
|------|------|
| `references/可用词库.md` | 可上桌的词库（已实况验证 + 推荐新增 + 待观察） |
| `references/新番出题候选_2024_2026.md` | 按季度整理的出题候选作品 |
| `references/player-feedback-signals.md` | 玩家原话→问题类型映射 |

> **出题史**（已出过的题）与**淘汰记录**属私档，不在本仓——本地存档在 `workspace/records/spy-game/`。

## 工具

| 工具 | 位置 |
|------|------|
| 身份分配器 | `scripts/spy.py`（详见 `rules.md` → 裁判工具；统一入口 `game spy …`） |

---

## 相关技能

| 技能 | 关系 |
|------|------|
| `ruozhiba-wordbank` | 逻辑陷阱防御，跟出题无关 — 不要混用 |
