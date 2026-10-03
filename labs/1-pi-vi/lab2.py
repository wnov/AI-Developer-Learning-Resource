"""实验 2：价值迭代 vs 策略迭代 —— 共写脚本

读法：从上往下，依次是 第 0 部分 题设 → 第 1 部分 已学过的公式 → 第 2 部分 本次的公式 → 第 3 部分 题目。
- 标【你来写】的函数由你实现：docstring 里有公式、书页和参数说明。
- 题设和已学过的公式直接复用 s1_4.py 里的函数，不重抄。
运行：python lab2.py。要跑哪些题，在文件最后的 RUN 里选。
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "1-policy-improvement"))
import s1_4                                   # noqa: E402
from s1_4 import (ACTIONS, N_STATES, PI_RANDOM, TERMINAL,   # noqa: E402
                  change_policy, greedy, q_pi, show)

# =====================================================================
# 第 0 部分：题设 —— SB 例 4.1，书第 76 页（PDF 第 98 页），定义在 s1_4.py 第 0 部分
# =====================================================================
#      0   1   2   3
#      4   5   6   7        0 和 15 是同一个终止状态 T；每步 r = −1
#      8   9  10  11
#     12  13  14  15

_GRID_NEXT_STATE = s1_4.next_state


def _pit_next_state(s, a):
    """“出不去的格子”：状态 5 的四个动作都留在 5（每步仍是 r = −1）。其余格子和原题一样，也能走进 5。"""
    if s == 5:
        return 5
    return _GRID_NEXT_STATE(s, a)


def set_problem(gamma, pit=False):
    """切换题设：折扣 γ，以及是否把状态 5 改成出不去的格子。

    q_pi、greedy 读的是 s1_4.py 里的 GAMMA 和 next_state，所以在这里改那两个名字。
    """
    s1_4.GAMMA = gamma
    s1_4.next_state = _pit_next_state if pit else _GRID_NEXT_STATE


# =====================================================================
# 第 1 部分：已学过的公式
# =====================================================================

def eval_sweep(v, pi):
    """策略评估的一轮 two-array 更新，SB 式 4.5（书第 74 页）。实验 1 你写过同样的东西，这里用 q_pi 写。

        v_{k+1}(s) = Σ_a π(a|s) q_k(s, a)，  q_k(s, a) = r + γ v_k(s′)
    """
    v_new = v.copy()
    for s in range(N_STATES):
        if s in TERMINAL:
            continue
        v_new[s] = sum(pi[s, i] * q_pi(v, s, a) for i, a in enumerate(ACTIONS))
    return v_new


# =====================================================================
# 第 2 部分：本次的公式 ——【你来写】
# =====================================================================

def vi_sweep(v, inplace):
    """【你来写】价值迭代的一轮更新，SB 式 4.10（书第 83 页，PDF 第 105 页）：

        v_{k+1}(s) = max_a Σ_{s′,r} p(s′, r | s, a) [ r + γ v_k(s′) ]

    本题转移确定，方括号里就是 q_pi(v, s, a)，直接复用 q_pi，不要重写 r + γ v。
    按 s = 0, 1, …, 15 的顺序更新，跳过 TERMINAL。

    参数：
      v       长度 16 的数组，上一轮的值 v_k。不要改动它，在副本上写新值。
      inplace False = two-array：右边的 q_pi 一律用上一轮的 v（式 4.10 原样）。
              True  = in-place：右边的 q_pi 用正在写的那张新表，
                      所以前面已经更新过的格子，后面的格子会立刻用到它的新值（SB §4.5，书第 85 页）。
    返回：新的数组 v_{k+1}。

    提示：两种写法只差一处 —— q_pi 的第一个参数传哪张表。
    """
    v_new = v.copy()
    pi = greedy(v_new)
    for s in range(N_STATES):
        if s in TERMINAL:
            continue
        if inplace:
            pi = greedy(v_new)
            opt_action = pi[s]
            v_new[s] = q_pi(v_new, s, opt_action)
        else:
            opt_action = pi[s]
            v_new[s] = q_pi(v, s, opt_action)
    return v_new


# =====================================================================
# 外围代码（我写的）：外层循环、计数、打印
# =====================================================================

def value_iteration(inplace=False, v0=0.0, theta=1e-4, max_sweeps=500, v_true=None):
    """反复调用 vi_sweep，直到一轮里最大变化 Δ < θ（SB 第 83 页算法框的停止条件）。

    v0：非终止状态的初值，T 固定为 0。
    v_true：给出时，记录每轮之后的最大误差 e_k = max_s |v_k(s) − v*(s)|。
    返回 (v, 轮数, 每轮的 Δ, 每轮的 e_k)。
    """
    v = np.full(N_STATES, float(v0))
    v[TERMINAL] = 0.0
    deltas, errors = [], []
    for k in range(1, max_sweeps + 1):
        v_new = vi_sweep(v, inplace)
        deltas.append(float(np.abs(v_new - v).max()))
        v = v_new
        if v_true is not None:
            errors.append(float(np.abs(v - v_true).max()))
        if deltas[-1] < theta:
            break
    return v, k, deltas, errors


def policy_iteration(theta=1e-4, max_sweeps=10000):
    """策略迭代，SB 第 80 页算法框：评估（eval_sweep 反复做到 Δ < θ）→ greedy → 直到策略不再变化。

    评估每次都从上一个策略的 v 接着算（书上的做法）。
    返回 (v, 外层轮数, 评估一共扫了多少轮)。
    """
    pi = PI_RANDOM
    v = np.zeros(N_STATES)
    actions_old = None
    total_sweeps = 0
    for outer in range(1, 100):
        for _ in range(max_sweeps):
            v_new = eval_sweep(v, pi)
            total_sweeps += 1
            done = np.abs(v_new - v).max() < theta
            v = v_new
            if done:
                break
        actions = greedy(v)
        if actions == actions_old:
            return v, outer, total_sweeps
        actions_old = actions
        pi = change_policy(PI_RANDOM, actions)
    return v, outer, total_sweeps


# =====================================================================
# 第 3 部分：题目 —— 每题写明“对题设做了什么调整”
# =====================================================================

def problem_A():
    """题 A：价值迭代和策略迭代，各要扫多少轮？

    场景和前提：
    - 题设同第 0 部分：4×4 网格，0 和 15 是终止状态 T，每步 r = −1。
    - 对题设的调整：分别跑 γ = 1 和 γ = 0.9。θ = 1e-4。价值迭代用 two-array，初值 v0 = 0。
    - 已知：
      · 价值迭代 γ = 1：上次课手算过，v₁、v₂、v₃ 依次是“最多走 1、2、3 步的最好回报”，v₃ = v*。
      · 实验 1：两组数组的策略评估，评估等概率随机策略（γ = 1）扫了 173 轮。
      · 策略迭代的第一轮评估就是评估等概率随机策略；之后对 v_π 贪心（2F 那题：贪心后已经是最优策略）。
    - 策略迭代的“扫了多少轮”= 所有外层轮次里，评估一共扫了多少轮。

    运行前先写下预测（写在冒号后面）：
    (1) γ = 1，价值迭代扫几轮停下？（停止条件：一轮里最大变化 Δ < θ，所以要多扫一轮确认）
        你的预测：4
    (2) γ = 1，策略迭代外层几轮？评估一共大约扫多少轮（数量级即可：几轮、几十轮、几百轮）？
        你的预测：4, 几百轮
    (3) γ = 0.9，价值迭代的轮数变不变？为什么？
        你的预测：不变，因为策略不变，4轮之前Δ不足以下降到足够小
    """
    for gamma in [1.0, 0.9]:
        set_problem(gamma)
        v_vi, n_vi, _, _ = value_iteration()
        v_pi, outer, n_pi = policy_iteration()
        print(f"γ = {gamma}")
        print(f"  价值迭代：扫了 {n_vi} 轮")
        print(f"  策略迭代：外层 {outer} 轮，评估一共扫了 {n_pi} 轮")
        print(f"  两者的 v 最大差：{np.abs(v_vi - v_pi).max():.2e}")
        show("  v*：", v_vi)
    set_problem(1.0)


def problem_B():
    """题 B：two-array 和 in-place 的价值迭代，谁收敛得快？为什么？

    场景和前提：
    - 题设同第 0 部分，对题设的调整：γ = 0.9；初值改成 v0 = −100（T 仍为 0），让初始误差很大，差别看得清楚。
    - 已知 v*（γ = 0.9，上次课给过）：
            0     -1    -1.9  -2.71
           -1     -1.9  -2.71 -1.9
           -1.9   -2.71 -1.9  -1
           -2.71  -1.9  -1     0
    - 已知（上次课）：two-array 时，最大误差 e_k 每轮最多乘 γ：e₀ = 99，e₁ = 89.1，e₂ = 80.19，第 3 轮归零。
    - in-place 按 0 → 15 的顺序更新：更新状态 2 时，状态 1 已经是这一轮的新值。

    运行前先写下预测：
    (1) in-place 扫完第 1 轮后，v(1) 和 v(2) 各是多少？
        提示：v(1) 的四个动作里有一个直接进 T。v(2) 往左一步到 1，用的是 v(1) 的哪一个值？
        你的预测：v(1)=-1,v(2)=-1.9
    (2) in-place 第 1 轮后的最大误差 e₁，比 two-array 的 89.1 大还是小？大概是什么量级？
        你的预测：小，1步好像就收敛了，接近0
    (3) 用一两句话解释：为什么 in-place 更快？用“后更新的格子用到的值，误差是多少”来说。
        你的预测：因为后更新的格子能用到更新后的值，误差更小
    """
    set_problem(0.9)
    v_star, _, _, _ = value_iteration(theta=1e-10)
    for name, inplace in [("two-array", False), ("in-place", True)]:
        v1, _, _, _ = value_iteration(inplace=inplace, v0=-100.0, max_sweeps=1)
        _, n, _, errors = value_iteration(inplace=inplace, v0=-100.0, v_true=v_star)
        print(f"{name}：扫了 {n} 轮；每轮之后的最大误差 e_k = {[round(e, 2) for e in errors]}")
        show(f"  {name} 第 1 轮之后的 v：", v1)
    set_problem(1.0)


def problem_C():
    """题 C：有一个出不去的格子时，γ = 1 的价值迭代还收敛吗？

    场景和前提：
    - 对题设的调整：状态 5 改成出不去的格子 —— 在 5 执行任何动作都留在 5，每步 r = −1。
      其余格子不变，从 1、4、6、9 也能走进 5。
    - 分别跑 γ = 1 和 γ = 0.9，初值 v0 = 0，最多扫 500 轮。
    - 已知（上次课）：γ = 1 时，收缩论证只给出 e_{k+1} ≤ e_k，不再保证收敛；
      原网格在 γ = 1 时仍能收敛，靠的是路径一定会进入 T、v(T) = 0。

    运行前先写下预测：
    (1) γ = 1：扫满 500 轮时，v(5) 是多少？会停下来吗？
        你的预测：-500
    (2) γ = 1：其他格子（比如 4、6）的值受 5 影响吗？为什么？
        提示：式 4.10 里有 max。
        你的预测：受影响，因为5的价值最低，而其他数周围有5的替代品（猜的，因为会改变路径，所以可能价值还是会变）
    (3) γ = 0.9：v(5) 收敛到多少？
        提示：一直留在 5，回报是 −1 − 0.9 − 0.9² − …
        你的预测：-10
    """
    for gamma in [1.0, 0.9]:
        set_problem(gamma, pit=True)
        v, n, deltas, _ = value_iteration()
        print(f"γ = {gamma}：扫了 {n} 轮，最后一轮 Δ = {deltas[-1]:.2e}")
        show("  v：", v)
    set_problem(1.0)


RUN = [problem_A, problem_B, problem_C]   # 要跑哪些题就放哪些

if __name__ == "__main__":
    for problem in RUN:
        print("=" * 20, problem.__name__, "=" * 20)
        problem()
