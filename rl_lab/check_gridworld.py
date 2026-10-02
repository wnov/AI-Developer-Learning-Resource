"""公共环境的自检：和学习者实验 1 的 P_sn、SB 图 4.1 对照。

运行：python -m rl_lab.check_gridworld （在仓库根目录）
"""

import pathlib
import sys

import numpy as np

from rl_lab.gridworld import GridWorld

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main():
    env = GridWorld()
    pi = env.uniform_policy()

    # 1. 转移矩阵和学习者实验 1 手写的 P_sn 完全一致
    sys.path.insert(0, str(ROOT / "labs" / "1-policy-evaluation"))
    import policy_eval  # noqa: E402

    assert np.allclose(env.P_pi(pi), policy_eval.P_sn), "P_π 与实验 1 的 P_sn 不一致"

    # 2. v_π 与 SB 图 4.1 最后一格（书第 77 页）一致
    fig41 = np.array([0, -14, -20, -22, -14, -18, -20, -20,
                      -20, -20, -18, -14, -22, -20, -14, 0], dtype=float)
    assert np.allclose(env.evaluate_exact(pi), fig41), "v_π 与 SB 图 4.1 不一致"

    # 3. v_π = Σ_a π(a|s) q_π(s,a)
    v = env.evaluate_exact(pi)
    assert np.allclose(np.sum(pi * env.q_from_v(v), axis=1)[1:-1], v[1:-1])

    # 4. γ=1 且 T 自环奖励 −1 时矩阵奇异；γ=0.9 时所有状态为 −10（实验 1 扰动 4、5）
    try:
        GridWorld(terminal_self_reward=-1).evaluate_exact(pi)
        raise AssertionError("应当奇异")
    except np.linalg.LinAlgError:
        pass
    assert np.allclose(GridWorld(gamma=0.9, terminal_self_reward=-1).evaluate_exact(pi), -10)

    print("rl_lab 自检通过：P_π 与实验 1 一致，v_π 与 SB 图 4.1 一致，扰动 4/5 的结果与实验 1 一致")


if __name__ == "__main__":
    main()
