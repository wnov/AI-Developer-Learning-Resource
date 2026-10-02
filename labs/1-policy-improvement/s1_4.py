"""S1.4 策略改进 —— 共写脚本（样例）

读法：从上往下，依次是 第 0 部分 题设 → 第 1 部分 已学过的公式 → 第 2 部分 本节课的公式 → 第 3 部分 题目。
- 标【你来写】的函数由你实现：docstring 里有公式、书页和参数说明。
- 其余部分是我写的，每段注释都写明它对应哪个数学对象。
运行：python s1_4.py。要跑哪些题，在文件最后的 RUN 里选。
"""
import numpy as np

# =====================================================================
# 第 0 部分：题设（先验条件）—— SB 例 4.1，书第 76 页（PDF 第 98 页）
# =====================================================================

# 状态：𝒮⁺ = {0, …, 15}。0 和 15 是同一个终止状态 T，非终止状态 𝒮 = {1, …, 14}。
#      0   1   2   3
#      4   5   6   7
#      8   9  10  11
#     12  13  14  15
N_STATES = 16
TERMINAL = [0, 15]

# 动作：𝒜 = {上, 下, 左, 右}
ACTIONS = ["up", "down", "left", "right"]

# 奖励：每一步 r = −1，包括进入 T 的那一步
REWARD = -1.0

# 折扣：γ = 1
GAMMA = 1.0


def next_state(s, a):
    """动态 p(s′|s,a)。

    这里转移是确定的：s 执行 a 只会到一个 s′（概率 1），所以用一个函数直接返回这个 s′。
    走出网格时留在原地。
    """
    row, col = divmod(s, 4)
    if a == "up":
        row -= 1
    elif a == "down":
        row += 1
    elif a == "left":
        col -= 1
    elif a == "right":
        col += 1
    if 0 <= row < 4 and 0 <= col < 4:
        return row * 4 + col
    return s


# 策略 π(a|s)：16×4 的数组，pi[s, i] = 在 s 选 ACTIONS[i] 的概率，每行和为 1。
# 题设的 π 是等概率随机，每个动作 0.25。
PI_RANDOM = np.full((N_STATES, len(ACTIONS)), 0.25)


# =====================================================================
# 第 1 部分：已学过的公式 —— 策略评估（实验 1 你已实现，这里直接给出）
# =====================================================================

def evaluate(pi):
    """求 v_π：解线性方程组 (I − γP_π) v = r_π（SB 式 4.4 的矩阵形式，书第 74 页）。

    P_π(s, s′) = Σ_a π(a|s) p(s′|s,a)    固定策略后，从 s 一步到 s′ 的概率
    r_π(s)     = Σ_a π(a|s) · r          固定策略后，s 的期望即时奖励
    T 不参与方程，v(T) 固定为 0（进入 T 后不再有奖励）。
    """
    P = np.zeros((N_STATES, N_STATES))
    r = np.zeros(N_STATES)
    for s in range(N_STATES):
        if s in TERMINAL:
            continue
        for i, a in enumerate(ACTIONS):
            P[s, next_state(s, a)] += pi[s, i]
            r[s] += pi[s, i] * REWARD
    keep = [s for s in range(N_STATES) if s not in TERMINAL]
    A = np.eye(len(keep)) - GAMMA * P[np.ix_(keep, keep)]
    v = np.zeros(N_STATES)
    v[keep] = np.linalg.solve(A, r[keep])
    return v


# =====================================================================
# 第 2 部分：本节课的公式 ——【你来写】
# =====================================================================

def q_pi(v, s, a):
    """【你来写】动作价值 q_π(s, a)，SB 式 4.6（书第 78 页，PDF 第 100 页）：

        q_π(s, a) = Σ_{s′, r} p(s′, r | s, a) [ r + γ v_π(s′) ]

    含义：在 s 先执行 a，之后一直按 π 走的期望回报。
    本题转移是确定的（用 next_state），奖励固定为 REWARD，求和只剩一项。
    参数：v 是长度 16 的 v_π 数组；s 是状态编号；a 是动作名，例如 "left"。
    返回：一个数。
    """
    raise NotImplementedError("q_pi 还没写")


def gain(v, s, a):
    """【你来写】改动的单步收益（今天推出来的量）：

        g(s) = q_π(s, π′(s)) − v_π(s)

    参数：a 就是 π′(s)，也就是 π′ 在 s 选的动作。
    """
    raise NotImplementedError("gain 还没写")


def change_policy(pi, changes):
    """构造 π′：复制 π，再把 changes 里的状态改成确定性地选指定动作。

    changes 例子：{6: "left"} 表示 π′(6) = 左，其余状态和 π 一样。
    """
    pi_new = pi.copy()
    for s, a in changes.items():
        pi_new[s] = 0.0
        pi_new[s, ACTIONS.index(a)] = 1.0
    return pi_new


def show(title, x):
    print(title)
    print(np.round(np.asarray(x).reshape(4, 4), 3), "\n")


# =====================================================================
# 第 3 部分：题目 —— 每题写明“对题设做了什么调整”
# =====================================================================

def problem_2A():
    """题 2A：求状态 6 四个动作的 q_π(6, a)，验证它们的平均等于 v_π(6)。
    对题设的调整：无（π 是等概率随机）。
    依据：v_π(s) = Σ_a π(a|s) q_π(s, a)，SB 式 3.13 的形式。
    """
    v = evaluate(PI_RANDOM)
    show("v_π：", v)
    qs = [q_pi(v, 6, a) for a in ACTIONS]
    print("q_π(6, ·)：", {a: round(float(q), 3) for a, q in zip(ACTIONS, qs)})
    print(f"平均：{np.mean(qs):.3f}    v_π(6)：{v[6]:.3f}\n")


def problem_2B():
    """题 2B：只在状态 6 改成“总是向左”，比较 v_π′ 和 v_π。
    对题设的调整：π → π′，π′(6) = 左，其余状态不变。
    看什么：d = v_π′ − v_π，以及 d(6) 和 g(6) 的关系。
    """
    changes = {6: "left"}
    v = evaluate(PI_RANDOM)
    v_new = evaluate(change_policy(PI_RANDOM, changes))
    print(f"g(6) = {gain(v, 6, 'left'):.3f}\n")
    show("v_π′：", v_new)
    show("d = v_π′ − v_π：", v_new - v)


RUN = [problem_2A, problem_2B]   # 要跑哪些题就放哪些

if __name__ == "__main__":
    for problem in RUN:
        print("=" * 20, problem.__name__, "=" * 20)
        problem()
