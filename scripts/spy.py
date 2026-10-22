#!/usr/bin/env python3
"""
谁是卧底 · 身份分配器

用法（玩法组一起签出时也可以走统一入口 `game spy …`，参数一模一样）：
  # 名单模式（推荐）—— 自动算人数、随机发身份到具体人头
  python3 spy.py --list "甲,乙,丙,丁"
  python3 spy.py --list "1【甲】2【乙】3【丙】至"
  python3 spy.py --file players.txt

  # 纯人数模式
  python3 spy.py --total 12

  # 按人排除身份（参数是玩家编号，逗号分隔，1-indexed）
  python3 spy.py --list "1【甲】2【乙】3【丙】4【丁】" \
    --exclude-angel "2,7" --exclude-whiteboard "2,3"

  # 指定卧底人数（覆盖比例计算）
  python3 spy.py --list "..." --undercover 3

  # 固定身份（按序号锁定）
  python3 spy.py --list "1【甲】2【乙】..." --fixed "10:天使"

  # 默认单轮输出，预览分布加 -n
  python3 spy.py --list "..." -n 5
"""

import argparse
import math
import random
import re
import sys
from pathlib import Path


# ── 身份配置 ──────────────────────────────────────────
ANGEL = "天使"
WHITEBOARD = "白板"
CIVILIAN = "平民"
UNDERCOVER = "卧底"

ROLE_META = {
    ANGEL:      {"team": "好人方", "info": "同时知道双边词汇",  "emoji": "👼"},
    WHITEBOARD: {"team": "第三方", "info": "只有一个提示词",     "emoji": "⬜"},
    CIVILIAN:   {"team": "好人方", "info": "知道自己的词",      "emoji": "🙋"},
    UNDERCOVER: {"team": "坏人方", "info": "知道自己的词(卧底词)", "emoji": "😈"},
}
ROLE_ORDER = [ANGEL, WHITEBOARD, UNDERCOVER, CIVILIAN]


# ── 核心逻辑 ──────────────────────────────────────────

def parse_ratio(s: str) -> tuple[int, int]:
    parts = s.split(":")
    if len(parts) != 2:
        raise ValueError(f"比例格式应为 A:B，收到: {s}")
    return int(parts[0]), int(parts[1])


def roll_evil_count(remaining: int, ratio_good: int, ratio_evil: int) -> int:
    """在比例附近随机取卧底人数"""
    expected = remaining * ratio_evil / (ratio_good + ratio_evil)
    lo = max(1, math.floor(expected))
    hi = min(remaining - 1, math.ceil(expected))
    if lo == hi:
        return lo
    # 概率加权：越靠近期望值越可能出现
    candidates = list(range(lo, hi + 1))
    weights = [1.0 / (abs(c - expected) + 0.5) for c in candidates]
    evil = random.choices(candidates, weights=weights, k=1)[0]
    return min(evil, remaining - evil)  # 不超过半


def one_round(players: list[str], ratio_good: int, ratio_evil: int,
              has_angel: bool, has_whiteboard: bool,
              exclude_angel: set[str] | None = None,
              exclude_whiteboard: set[str] | None = None,
              fixed_evil: int | None = None,
              fixed: dict[int, str] | None = None) -> dict:
    """一轮随机分配，返回 {身份: [名字, ...]}
    
    exclude_angel: 不能当天使的玩家名字集合
    exclude_whiteboard: 不能当白板的玩家名字集合
    fixed_evil: 固定卧底人数（覆盖比例计算）
    fixed: {序号: 身份} 固定玩家到指定身份
    """
    total = len(players)
    if total < 4:
        raise ValueError(f"至少需要4人，给了{total}人")
    pool = list(players)
    random.shuffle(pool)

    seats = {r: [] for r in ROLE_ORDER}
    taken = set()

    # 先处理 fixed 分配：根据序号把玩家固定到身份
    fixed_indices: set[int] = set()
    if fixed:
        # 把 fixed 的玩家从 pool 中取出放入对应身份
        fixed_players = {}
        for idx, role in fixed.items():
            if 1 <= idx <= len(players):
                fixed_players[players[idx-1]] = role
                fixed_indices.add(idx)
        for name, role in fixed_players.items():
            seats[role].append(name)
            taken.add(name)
        # 从 pool 中移除已被固定分配的人
        pool = [p for p in pool if p not in taken]
    
    if has_angel:
        candidates = [p for p in pool if not exclude_angel or p not in exclude_angel]
        if not candidates:
            raise ValueError("所有人都被排除天使，无法分配")
        chosen = random.choice(candidates)
        seats[ANGEL].append(chosen)
        taken.add(chosen)
    if has_whiteboard:
        candidates = [p for p in pool if p not in taken and (not exclude_whiteboard or p not in exclude_whiteboard)]
        if not candidates:
            raise ValueError("剩余玩家都被排除白板，无法分配")
        chosen = random.choice(candidates)
        seats[WHITEBOARD].append(chosen)
        taken.add(chosen)

    rest = [p for p in pool if p not in taken]
    remaining = len(rest)
    if remaining < 2:
        raise ValueError(f"剩余{remaining}人，至少需要2人")
    
    if fixed_evil is not None:
        evil = min(fixed_evil, remaining)
    else:
        evil = roll_evil_count(remaining, ratio_good, ratio_evil)
    good = remaining - evil

    random.shuffle(rest)
    for i in range(evil):
        seats[UNDERCOVER].append(rest[i])
    for i in range(evil, evil + good):
        seats[CIVILIAN].append(rest[i])
    return seats


# ── 输出 ──────────────────────────────────────────────

def print_header(players: list[str], ratio_good: int, ratio_evil: int,
                 has_angel: bool, has_whiteboard: bool):
    print(f"\n🧩 谁是卧底 · 身份分配")
    print(f"  共 {len(players)} 人参加")
    if len(players) <= 20:
        for i, name in enumerate(players, 1):
            print(f"    {i:2d}. {name}")
    print(f"  分配比: 好人:卧底 = {ratio_good}:{ratio_evil}")
    parts = []
    if has_angel: parts.append("天使")
    if has_whiteboard: parts.append("白板")
    print(f"  固定: {' '.join(parts)}")


def print_round(seats: dict, label: str = ""):
    title = f"  🎭 身份分配结果" + (f"（{label}）" if label else "")
    print(f"\n{'=' * 52}")
    print(f"  {title}")
    print(f"{'=' * 52}")
    for role in ROLE_ORDER:
        names = seats.get(role, [])
        if not names:
            continue
        m = ROLE_META[role]
        print(f"\n  {m['emoji']} {role}（{m['team']}·{m['info']}）")
        for n in names:
            print(f"    ▸ {n}")

    # 汇总
    total = sum(len(v) for v in seats.values())
    good = len(seats[ANGEL]) + len(seats[CIVILIAN])
    evil = len(seats[UNDERCOVER])
    third = len(seats[WHITEBOARD])
    print(f"\n  {'─' * 52}")
    print(f"  📊 好人{good} / 卧底{evil} / 白板{third}   卧底占比{evil/total*100:.1f}%")
    print(f"{'=' * 52}")


def print_summary(evil_counts: list[int], total: int):
    print(f"\n{'=' * 52}")
    print(f"  📈 合计 {len(evil_counts)} 轮")
    print(f"     卧底范围: {min(evil_counts)}~{max(evil_counts)} 人")
    most = max(set(evil_counts), key=evil_counts.count)
    print(f"     最常见: {most} 卧底（{most/total*100:.1f}%）")
    print(f"     平均占比: {sum(evil_counts)/len(evil_counts)/total*100:.1f}%")
    print(f"{'=' * 52}\n")


# ── 名单解析 ──────────────────────────────────────────

def parse_player_list(text: str) -> list[str]:
    """从各种格式的文本中提取玩家名字"""
    names = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        # 优先匹配 【名字】 格式（兼容 "3【丙】至"）
        brackets = re.findall(r'【(.+?)】', line)
        if brackets:
            names.extend(brackets)
            continue
        # 逗号分割
        if "，" in line or "," in line:
            names.extend(p.strip() for p in re.split(r'[，,]', line) if p.strip())
            continue
        # 空格分割（多于一个词时）
        parts = line.split()
        if len(parts) > 1:
            names.extend(parts)
        else:
            names.append(line)
    # 清理尾部标点
    cleaned = [n.strip().rstrip("。，,）)】").rstrip("至") for n in names if n.strip()]
    # 去重保序
    seen = set()
    return [x for x in cleaned if not (x in seen or seen.add(x))]


# ── 入口 ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="谁是卧底 · 身份分配器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--total", "-t", type=int, help="总人数（纯人数模式）")
    source.add_argument("--list", "-l", type=str, help="玩家名单")
    source.add_argument("--file", "-f", type=str, help="从文件读名单")

    parser.add_argument("--ratio", "-r", default="3:1", help="好人:卧底比例（默认 3:1）")
    parser.add_argument("--no-angel", action="store_true", help="无天使")
    parser.add_argument("--no-whiteboard", action="store_true", help="无白板")
    parser.add_argument("--exclude-angel", type=str, help="不能当天使的玩家编号，逗号分隔（如 \"2,7,11\"）")
    parser.add_argument("--exclude-whiteboard", type=str, help="不能当白板的玩家编号，逗号分隔（如 \"2,11\"）")
    parser.add_argument("--undercover", "-u", type=int, help="固定卧底人数（覆盖比例计算）")
    parser.add_argument("--fixed", type=str, nargs="*", default=[],
                        help="固定身份，格式: \"序号:身份\" 如 \"10:天使\"")
    parser.add_argument("--trials", "-n", type=int, default=1, help="模拟轮数（默认 1，加 -n 看分布）")

    args = parser.parse_args()
    rg, re_ = parse_ratio(args.ratio)
    ha, hw = not args.no_angel, not args.no_whiteboard

    # 解析排除名单（编号→名字）
    ex_angel_nums = set()
    ex_wb_nums = set()
    if args.exclude_angel:
        ex_angel_nums = {int(x.strip()) for x in args.exclude_angel.split(",")}
    if args.exclude_whiteboard:
        ex_wb_nums = {int(x.strip()) for x in args.exclude_whiteboard.split(",")}

    # 解析固定身份
    fixed: dict[int, str] = {}
    for f in args.fixed:
        m = re.match(r'(\d+):(.+)', f)
        if not m:
            print(f"❌ fixed 格式错误: {f}（应为 \"序号:身份\"）", file=sys.stderr)
            sys.exit(1)
        idx, role = int(m.group(1)), m.group(2).strip()
        if role not in [ANGEL, WHITEBOARD, UNDERCOVER, CIVILIAN]:
            print(f"❌ 未知身份: {role}", file=sys.stderr)
            sys.exit(1)
        fixed[idx] = role

    # 确定玩家名单
    if args.total:
        t = args.total
        fixed_cnt = (1 if ha else 0) + (1 if hw else 0)
        if t - fixed_cnt < 2:
            print(f"❌ 剩余{(t - fixed_cnt)}人不够，至少需要 {fixed_cnt+2} 人", file=sys.stderr)
            sys.exit(1)
        players = [f"玩家{i+1}" for i in range(t)]
        ex_angel = {players[i-1] for i in ex_angel_nums if 1 <= i <= t} if ex_angel_nums else None
        ex_wb = {players[i-1] for i in ex_wb_nums if 1 <= i <= t} if ex_wb_nums else None
        print(f"🧩 身份分配模拟（{t}人）")
        print(f"  固定: {'天使 ' if ha else ''}{'白板 ' if hw else ''}")
        print(f"  剩余 {t - fixed_cnt} 人 → 好人:卧底 = {rg}:{re_}")
    else:
        text = Path(args.file).read_text(encoding="utf-8") if args.file else args.list
        players = parse_player_list(text)
        if not players:
            print("❌ 未能解析出玩家名字", file=sys.stderr)
            sys.exit(1)
        ex_angel = {players[i-1] for i in ex_angel_nums if 1 <= i <= len(players)} if ex_angel_nums else None
        ex_wb = {players[i-1] for i in ex_wb_nums if 1 <= i <= len(players)} if ex_wb_nums else None
        print_header(players, rg, re_, ha, hw)
        if ex_angel:
            print(f"  🚫 排除天使: {', '.join(sorted(ex_angel))}")
        if ex_wb:
            print(f"  🚫 排除白板: {', '.join(sorted(ex_wb))}")

    # 跑 N 轮
    evil_counts = []
    for t in range(args.trials):
        seats = one_round(players, rg, re_, ha, hw,
                          exclude_angel=ex_angel,
                          exclude_whiteboard=ex_wb,
                          fixed_evil=args.undercover,
                          fixed=fixed)
        evil_counts.append(len(seats[UNDERCOVER]))
        if args.total:
            # 纯人数模式：简略行
            g = len(seats[ANGEL]) + len(seats[CIVILIAN])
            e = len(seats[UNDERCOVER])
            w = len(seats[WHITEBOARD])
            print(f"  第 {t+1:2d} 轮  │  天使[{g - (g - 1 if ha else 0)}] "
                  f"白板[{w}] 平民[{g - (1 if ha else 0)}] 卧底[{e}]  │  {g+e+w}人")
        else:
            print(f"\n{'─' * 52}")
            print(f"  🔄 第 {t+1} 轮")
            print_round(seats)

    print_summary(evil_counts, len(players))


if __name__ == "__main__":
    main()
