"""S1.4 策略改进 —— 题设脚本。改下面“题设”里的值，然后运行：python s1_4.py

网格（SB 例 4.1），0 和 15 是同一个终止状态 T：
     0   1   2   3
     4   5   6   7
     8   9  10  11
    12  13  14  15
每步奖励 −1，走出网格则原地不动。π = 四个动作各 0.25。
"""
import numpy as np

# ======== 题设：只改这里 ========
GAMMA = 1.0
CHANGES = {6: "left"}   # π′ 相对 π 改动的状态：{状态: 动作}，动作取 "up" "down" "left" "right"
GREEDY_ALL = False      # True 时忽略 CHANGES，π′ 在每个状态都取 q_π 最大的动作（并列取第一个）
# ================================

ACTIONS = ["up", "down", "left", "right"]
MOVES = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
TERMINAL = (0, 15)


def next_state(s, a):
    r, c = divmod(s, 4)
    r2, c2 = r + MOVES[a][0], c + MOVES[a][1]
    return r2 * 4 + c2 if 0 <= r2 < 4 and 0 <= c2 < 4 else s


def evaluate(policy):
    """policy[s] = {动作: 概率}。解 (I − γP_π) v = r_π，T 的值固定为 0。"""
    P, r = np.zeros((16, 16)), np.zeros(16)
    for s in range(16):
        if s in TERMINAL:
            continue
        for a, p in policy[s].items():
            P[s, next_state(s, a)] += p
            r[s] += p * (-1)
    idx = [s for s in range(16) if s not in TERMINAL]
    v = np.zeros(16)
    v[idx] = np.linalg.solve(np.eye(14) - GAMMA * P[np.ix_(idx, idx)], r[idx])
    return v


def q_of(v, s, a):
    return -1 + GAMMA * v[next_state(s, a)]


def show(name, x):
    print(name)
    print(np.round(np.asarray(x).reshape(4, 4), 3), "\n")


pi = {s: {a: 0.25 for a in ACTIONS} for s in range(16)}
v = evaluate(pi)

if GREEDY_ALL:
    CHANGES = {s: max(ACTIONS, key=lambda a: q_of(v, s, a)) for s in range(16) if s not in TERMINAL}
pi_new = {s: ({CHANGES[s]: 1.0} if s in CHANGES else pi[s]) for s in range(16)}
v_new = evaluate(pi_new)

print(f"GAMMA = {GAMMA}，π′ 改动：{CHANGES}\n")
show("v_π：", v)
for s in CHANGES:
    print(f"q_π({s}, ·)：", {a: round(q_of(v, s, a), 3) for a in ACTIONS}, f"  v_π({s}) = {v[s]:.3f}")
print()
show("v_π′：", v_new)
show("d = v_π′ − v_π：", v_new - v)
