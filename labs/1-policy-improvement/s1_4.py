"""S1.4 策略改进：题设脚本。

只做题设里要用的计算（求 v_π、q_π、改策略后的 v_π′ 和差值），不包含要你推的结论。

例子（在仓库根目录运行）：
    python labs/1-policy-improvement/s1_4.py                      # 默认：等概率随机策略，状态 6 改成向左
    python labs/1-policy-improvement/s1_4.py --change 6=left 9=up # 同时改多个状态
    python labs/1-policy-improvement/s1_4.py --change 6=down --q 6 5
    python labs/1-policy-improvement/s1_4.py --gamma 0.9
"""

import argparse
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from rl_lab.gridworld import ACTION_NAMES, GridWorld  # noqa: E402


def parse_changes(items):
    out = {}
    for item in items:
        s, a = item.split("=")
        out[int(s)] = a
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gamma", type=float, default=1.0)
    ap.add_argument("--change", nargs="*", default=["6=left"],
                    help="π′ 相对 π 改动的状态，格式 状态=动作，动作取 up/down/left/right")
    ap.add_argument("--q", nargs="*", type=int, default=None,
                    help="打印这些状态的 q_π(s,·)，默认打印被改动的状态")
    args = ap.parse_args()

    env = GridWorld(gamma=args.gamma)
    pi = env.uniform_policy()
    changes = parse_changes(args.change)
    pi_new = env.policy_with(changes, base=pi)

    v = env.evaluate_exact(pi)
    q = env.q_from_v(v)
    v_new = env.evaluate_exact(pi_new)

    print(f"γ = {args.gamma}，π = 等概率随机，π′ 改动：{changes}\n")
    print("v_π：")
    env.show(v)
    for s in (args.q if args.q is not None else changes):
        qs = "  ".join(f"{ACTION_NAMES[a]} {q[s, a]:.3f}" for a in range(env.nA))
        print(f"\nq_π({s}, ·)：{qs}    v_π({s}) = {v[s]:.3f}")
    print("\nv_π′：")
    env.show(v_new)
    print("\nd = v_π′ − v_π：")
    env.show(v_new - v)


if __name__ == "__main__":
    main()
