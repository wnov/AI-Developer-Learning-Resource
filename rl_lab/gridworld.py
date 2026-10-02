"""SB 例 4.1 的网格世界，题设做成参数。

状态编号（和实验 1 的 policy_eval.py 一致，0 和 15 是同一个终止状态 T）：

     0   1   2   3
     4   5   6   7
     8   9  10  11
    12  13  14  15

动作编号：0 上、1 下、2 左、3 右。走出网格的动作让状态保持不变。

本文件只提供环境和策略的表示、精确求解 v_π、由 v 算 q、采样轨迹。
策略迭代、价值迭代等算法不在这里，由学习者或 AI 实现。
"""

import numpy as np

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
ACTIONS = {"up": UP, "down": DOWN, "left": LEFT, "right": RIGHT}
ACTION_NAMES = ["up", "down", "left", "right"]
_MOVES = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}


class GridWorld:
    """
    参数
    - gamma：折扣因子。
    - step_reward：每一步的奖励（包括进入 T 的那一步）。
    - terminal_self_reward：None 表示 T 是真正的终止状态（v(T)=0，进入 T 后不再有奖励）；
      给一个数表示把 T 当普通状态处理：在 T 执行任何动作都回到 T，奖励为这个数
      （实验 1 扰动第 4、5 项的错误设定）。
    """

    def __init__(self, gamma=1.0, step_reward=-1.0, terminal_self_reward=None, size=4):
        self.size = size
        self.nS = size * size
        self.nA = 4
        self.terminals = (0, self.nS - 1)
        self.gamma = gamma
        self.step_reward = step_reward
        self.terminal_self_reward = terminal_self_reward

        # P[s, a, s']：转移概率；R[s, a]：期望即时奖励（这里转移是确定的）
        self.P = np.zeros((self.nS, self.nA, self.nS))
        self.R = np.zeros((self.nS, self.nA))
        for s in range(self.nS):
            for a in range(self.nA):
                if s in self.terminals:
                    self.P[s, a, s] = 1.0
                    self.R[s, a] = 0.0 if terminal_self_reward is None else terminal_self_reward
                else:
                    self.P[s, a, self.next_state(s, a)] = 1.0
                    self.R[s, a] = step_reward

    def is_terminal(self, s):
        return s in self.terminals

    def next_state(self, s, a):
        """确定性转移：s 执行 a 后到达的状态。"""
        r, c = divmod(s, self.size)
        dr, dc = _MOVES[a]
        r2, c2 = r + dr, c + dc
        if not (0 <= r2 < self.size and 0 <= c2 < self.size):
            return s
        return r2 * self.size + c2

    # ---------- 策略 ----------
    # 策略统一用 nS×nA 的数组表示，pi[s, a] = π(a|s)，每行和为 1。

    def uniform_policy(self):
        return np.full((self.nS, self.nA), 1.0 / self.nA)

    def policy_with(self, overrides, base=None):
        """在 base（默认等概率随机）上改若干状态。

        overrides：{状态: 动作}，动作可以是名字 "left"、编号 2（确定性），
        或长度为 4 的概率向量。例：policy_with({6: "left"})。
        """
        pi = self.uniform_policy() if base is None else np.array(base, dtype=float)
        for s, act in overrides.items():
            if isinstance(act, str):
                act = ACTIONS[act]
            if np.isscalar(act):
                row = np.zeros(self.nA)
                row[int(act)] = 1.0
            else:
                row = np.asarray(act, dtype=float)
            pi[s] = row
        return pi

    def deterministic_policy(self, actions):
        """actions：长度 nS 的动作编号数组 → nS×nA 的 one-hot 策略。"""
        pi = np.zeros((self.nS, self.nA))
        pi[np.arange(self.nS), np.asarray(actions, dtype=int)] = 1.0
        return pi

    # ---------- 固定策略后的矩阵 ----------

    def P_pi(self, pi):
        """P_π[s, s'] = Σ_a π(a|s) p(s'|s,a)"""
        return np.einsum("sa,sat->st", pi, self.P)

    def r_pi(self, pi):
        """r_π[s] = Σ_a π(a|s) r(s,a)"""
        return np.sum(pi * self.R, axis=1)

    def evaluate_exact(self, pi):
        """解 (I − γP_π) v = r_π，返回长度 nS 的 v_π。

        T 为真正的终止状态且 γ = 1 时，只在非终止状态上解，v(T) 固定为 0。
        其余情况在全部状态上解；矩阵奇异时 numpy 抛出 LinAlgError，不做掩盖。
        """
        P, r = self.P_pi(pi), self.r_pi(pi)
        v = np.zeros(self.nS)
        if self.terminal_self_reward is None and self.gamma == 1.0:
            idx = [s for s in range(self.nS) if s not in self.terminals]
            A = np.eye(len(idx)) - self.gamma * P[np.ix_(idx, idx)]
            v[idx] = np.linalg.solve(A, r[idx])
        else:
            v = np.linalg.solve(np.eye(self.nS) - self.gamma * P, r)
        return v

    def q_from_v(self, v):
        """q[s, a] = r(s,a) + γ Σ_{s'} p(s'|s,a) v(s')"""
        return self.R + self.gamma * self.P @ v

    # ---------- 采样 ----------

    def rollout(self, pi, start, max_steps=1000, rng=None):
        """按策略 pi 从 start 出发采样一条轨迹。

        返回 [(S_t, A_t, R_{t+1}), ...]。T 为真正的终止状态时，进入 T 即结束；
        否则一直走到 max_steps。从终止状态出发时返回空列表。
        """
        rng = np.random.default_rng() if rng is None else rng
        traj = []
        s = start
        for _ in range(max_steps):
            if self.terminal_self_reward is None and self.is_terminal(s):
                break
            a = rng.choice(self.nA, p=pi[s])
            s2 = int(rng.choice(self.nS, p=self.P[s, a]))
            traj.append((s, int(a), float(self.R[s, a])))
            s = s2
        return traj

    # ---------- 打印 ----------

    def show(self, values, fmt="{:8.3f}"):
        """把长度 nS 的数组按网格打印。"""
        values = np.asarray(values)
        for r in range(self.size):
            print("".join(fmt.format(x) for x in values[r * self.size:(r + 1) * self.size]))

    def show_policy(self, pi):
        """打印每个状态概率最大的动作（并列时全部列出），T 显示为 T。"""
        arrows = "↑↓←→"
        for r in range(self.size):
            cells = []
            for c in range(self.size):
                s = r * self.size + c
                if self.is_terminal(s):
                    cells.append("T")
                else:
                    best = np.flatnonzero(np.isclose(pi[s], pi[s].max()))
                    cells.append("".join(arrows[a] for a in best))
            print(" ".join(f"{x:>4}" for x in cells))
