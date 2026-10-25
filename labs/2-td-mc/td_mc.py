"""实验 3：随机游走上的 TD(0) vs MC —— 共写脚本

读法：从上往下，依次是 第 0 部分 题设 → 第 1 部分 已学过的公式 → 第 2 部分 本次的公式 → 第 3 部分 题目。
- 标【你来写】的函数由你实现：docstring 里有公式、书页和参数说明。
- 其余部分是我写的，每段注释都写明它对应哪个数学对象。
运行：conda activate rl，然后 python td_mc.py。要跑哪些题，在文件最后的 RUN 里选。
图存在本目录的 img/ 下。
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt   # noqa: E402
import numpy as np                # noqa: E402

IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")

# =====================================================================
# 第 0 部分：题设 —— SB 例 6.2 随机游走，书第 125 页（PDF 第 147 页）
# =====================================================================
#
#   [左端] ← A ⇄ B ⇄ C ⇄ D ⇄ E → [右端]
#     0      1   2   3   4   5      6
#
# 状态：0 和 6 是两个终止状态；1..5 对应书上的 A..E。数组下标就是状态编号。
N_STATES = 7
TERMINAL = [0, 6]
NAMES = ["左端", "A", "B", "C", "D", "E", "右端"]

# 每局都从 C 出发
START = 3

# 动态：每一步向左、向右各 1/2（没有动作，是 MRP）
# 奖励：只有走进右端（状态 6）的那一步 r = +1，其余每一步 r = 0
RIGHT_END = 6

# 折扣：γ = 1（书上的设定）
GAMMA = 1.0

# 真实值 v_π：A..E 依次是 1/6, 2/6, 3/6, 4/6, 5/6（书第 125 页给出）；终止状态为 0
# 记号和 SB 一致：小写 v_pi 是真实值（题设决定的固定数，算法看不到，这里只用来打分和出题）；
# 大写 V 是算法手里的估计表（下面的 V_INIT 和各函数的参数 V）。
v_pi = np.array([0, 1, 2, 3, 4, 5, 0]) / 6.0

# 初始估计：非终止状态 V = 0.5，终止状态 V = 0（书第 125 页：“initialized to the intermediate value V(s) = 0.5”）
V_INIT = np.array([0, 0.5, 0.5, 0.5, 0.5, 0.5, 0])


def generate_episode(rng):
    """按题设跑一局，返回 (states, rewards)。

    下标约定（和 SB 一致，写代码时最容易错一位）：
      states  = [S_0, S_1, …, S_T]      长度 T+1，S_0 = C，S_T 是终止状态
      rewards = [R_1, R_2, …, R_T]      长度 T，rewards[t] 是从 S_t 走到 S_{t+1} 拿到的 R_{t+1}
    """
    states, rewards = [START], []
    s = START
    while s not in TERMINAL:
        s_next = s + (1 if rng.random() < 0.5 else -1)
        rewards.append(1.0 if s_next == RIGHT_END else 0.0)
        states.append(s_next)
        s = s_next
    return states, rewards


# =====================================================================
# 第 1 部分：已学过的公式
# =====================================================================

def returns(rewards, gamma):
    """一局里每个时刻的回报 G_t，倒序用递推式 G_t = R_{t+1} + γ G_{t+1}（SB 式 3.9，书第 55 页），G_T = 0。

    S2.1 讲 first-visit MC 算法框时你手算过（W3-T1 单元 1）。
    返回列表 G，G[t] = G_t，t = 0, …, T−1。
    """
    G = [0.0] * len(rewards)
    g = 0.0
    for t in reversed(range(len(rewards))):
        g = rewards[t] + gamma * g
        G[t] = g
    return G


def rms_error(V):
    """估计表 V 和真实值 v_pi 在 5 个非终止状态上的均方根误差（书第 125 页右图的纵轴）。"""
    return float(np.sqrt(np.mean((V[1:6] - v_pi[1:6]) ** 2)))


# =====================================================================
# 第 2 部分：本次的公式 ——【你来写】
# =====================================================================

def td_target(V, r, s_next, gamma):
    """【你来写】TD(0) 的目标：SB 式 6.2 方括号里的前半部分（书第 120 页，PDF 第 142 页）

        TD 目标 = R_{t+1} + γ V(S_{t+1})

    参数：
      V       长度 7 的数组，当前的估计表。只读，不要改它。
      r       这一步拿到的奖励 R_{t+1}
      s_next  走到的下一个状态 S_{t+1}（可能是终止状态，那里 V = 0）
      gamma   折扣 γ
    返回：一个数。
    """
    return r + gamma * V[s_next]


def td0_episode(V, states, rewards, alpha, gamma):
    """【你来写】用一局轨迹做 TD(0) 更新，SB 式 6.2（书第 120 页，PDF 第 142 页）：

        V(S_t) ← V(S_t) + α [ R_{t+1} + γ V(S_{t+1}) − V(S_t) ]
                              └──── td_target ────┘
                            └────────── δ_t（式 6.5）──────────┘

    按 t = 0, 1, …, T−1 的顺序，边走边更新（书第 120 页 Tabular TD(0) 算法框）：
    第 t 步更新完 V(S_t)，第 t+1 步算目标时，用的就是已经改过的表。
    复用 td_target，不要重写 R + γV。

    参数：
      V        长度 7 的数组。直接在 V 上原地修改；终止状态的 V 始终保持 0，不要更新。
      states   [S_0, …, S_T]，见 generate_episode
      rewards  [R_1, …, R_T]，rewards[t] 是 R_{t+1}
      alpha    步长 α
      gamma    折扣 γ
    返回：None（结果就在 V 里）。
    """
    for i, state in enumerate(states[:-1]):
        reward = rewards[i]
        s_next = states[i+1]
        V[state] = V[state] + alpha * (reward + gamma * V[s_next] - V[state])


def mc_episode(V, states, rewards, alpha, gamma):
    """【你来写】用一局轨迹做 constant-α MC 更新，SB 式 6.1（书第 119 页，PDF 第 141 页）：

        V(S_t) ← V(S_t) + α [ G_t − V(S_t) ]

    一局结束后才更新：先用 returns 算出这一局所有的 G_t，再按 t = 0, 1, …, T−1 逐个更新。
    every-visit：同一个状态在一局里出现几次，就更新几次（每次用各自那一刻的 G_t）。
    复用 returns，不要重写 G 的递推。

    参数和返回：同 td0_episode。
    """
    G_t = 0
    state_reversed = states[::-1]
    rewards_reversed = rewards[::-1]
    for i, state in enumerate(state_reversed[1:]):
        G_t = rewards_reversed[i] + gamma * G_t
        V[state] = V[state] + alpha * (G_t - V[state])

# =====================================================================
# 外围代码（我写的）：多局、多次重复、画图
# =====================================================================

UPDATE = {"TD": td0_episode, "MC": mc_episode}


def run(method, alpha, n_episodes=100, n_runs=100, gamma=GAMMA, seed=0):
    """重复 n_runs 次独立实验，每次从 V_INIT 开始跑 n_episodes 局。

    返回长度 n_episodes+1 的数组：第 k 个数 = 跑完 k 局后的 RMS 误差，对 n_runs 次取平均（第 0 个是初始误差）。
    这就是书第 125 页右图的画法。
    """
    curve = np.zeros(n_episodes + 1)
    for i in range(n_runs):
        rng = np.random.default_rng(seed + i)
        V = V_INIT.copy()
        curve[0] += rms_error(V)
        for k in range(1, n_episodes + 1):
            states, rewards = generate_episode(rng)
            UPDATE[method](V, states, rewards, alpha, gamma)
            assert V[0] == 0 and V[6] == 0, "终止状态的 V 被改了"
            curve[k] += rms_error(V)
    return curve / n_runs


def show(title, V):
    print(title, "  ".join(f"{NAMES[s]}={V[s]:.4f}" for s in range(1, 6)))


# =====================================================================
# 第 3 部分：题目 —— 每题写明“在练什么”和“对题设做了什么调整”
# =====================================================================

def problem_A():
    """题 A：同一局轨迹，TD 和 MC 各改了哪些格子？

    在练什么：写完代码后的第一个自查——用一局能手算的轨迹核对实现，以后写任何 RL 更新都先这样做。
    顺带看到 TD 和 MC 传递信息的方式不同：TD 每步只往前看一格。

    场景和前提：
    - 题设同第 0 部分。对题设的调整：不随机采样，固定用书第 125 页举的那一局：
          C, 0, B, 0, C, 0, D, 0, E, 1, 右端
      即 states = [3, 2, 3, 4, 5, 6]，rewards = [0, 0, 0, 0, 1]。
    - V 从 V_INIT 开始（A..E 都是 0.5），α = 0.1，γ = 1。只跑这一局。
    - 单元 4 第 1 步：V 是真实值时，这局五个 δ 不全为 0。这里 V 全是 0.5，情况不同。

    运行前先写下预测（写在冒号后面）：
    (1) TD：这一局里五个 δ_t 各是多少？跑完后哪些格子变了，变成多少？
        提示：边走边更新，前面的更新会不会影响后面的 δ？
        你的预测：
    (2) MC：这一局的 G_0..G_4 各是多少？跑完后哪些格子变了，变成多少？
        提示：C 出现了两次（t=0 和 t=2），every-visit 要更新两次，第二次从第一次的结果接着算。
        你的预测：
    (3) 一句话：为什么这一局 TD 只改了你说的那几格？
        你的预测：
    """
    states, rewards = [3, 2, 3, 4, 5, 6], [0.0, 0.0, 0.0, 0.0, 1.0]
    for method in ["TD", "MC"]:
        V = V_INIT.copy()
        UPDATE[method](V, states, rewards, 0.1, GAMMA)
        show(f"{method} 一局之后：", V)


def problem_B():
    """题 B：TD 和 MC，谁学得快、谁学得准？（书第 125 页右图，先预测，跑完再看书）

    在练什么：用误差曲线判断两种估计方法的好坏——这是以后调 PPO 的 λ、调 critic 学习率时看的同一种图。
    对应单元 4 的 GAE 小题：λ=0 一头是 TD，λ=1 一头是 MC。

    场景和前提：
    - 题设同第 0 部分。V 从 V_INIT 开始，γ = 1，每种设置跑 100 局，重复 100 次取平均。
    - 对题设的调整：比较 7 种设置——TD 的 α = 0.05、0.1、0.15；MC 的 α = 0.01、0.02、0.03、0.04。
      （和书上一样。MC 用更小的 α，原因是它的目标噪声大，这一点题 C 会量出来。）
    - 纵轴是 5 个状态的 RMS 误差。初始 V 全是 0.5，初始误差 = 0.236。

    运行前先写下预测：
    (1) 前 20 局：TD（α=0.1）和 MC（α=0.02）哪条曲线降得快？
        你的预测：TD下降快
    (2) 第 100 局：两者谁的误差低？
        你的预测：MC误差低
    (3) 同一种方法，α 大一些（比如 TD 的 0.15 对 0.05），曲线前段和后段各有什么不同？为什么？
        提示：α 大 = 每次往目标挪得多，目标本身有噪声时会怎样？
        你的预测：α越大，前段收敛越快，后段波动越大
    """
    settings = [("TD", a) for a in (0.05, 0.1, 0.15)] + [("MC", a) for a in (0.01, 0.02, 0.03, 0.04)]
    os.makedirs(IMG_DIR, exist_ok=True)
    plt.figure(figsize=(7, 4.5))
    shades = {"TD": iter(plt.cm.Blues(np.linspace(0.45, 0.95, 3))),
              "MC": iter(plt.cm.Reds(np.linspace(0.4, 0.95, 4)))}
    for method, alpha in settings:
        curve = run(method, alpha)
        print(f"{method} α={alpha:<5} 第 0/10/20/50/100 局后 RMS："
              + "  ".join(f"{curve[k]:.3f}" for k in (0, 10, 20, 50, 100)))
        plt.plot(curve, color=next(shades[method]),
                 linestyle="-" if method == "TD" else "--", linewidth=1.2,
                 label=f"{method} alpha={alpha}")
    plt.xlabel("episodes")
    plt.ylabel("RMS error (avg over 5 states, 100 runs)")
    plt.legend(fontsize=8)
    plt.tight_layout()
    path = os.path.join(IMG_DIR, "problem_B.png")
    plt.savefig(path, dpi=120)
    print("图：", path)


def problem_C():
    """题 C：MC 和 TD 给 V(C) 的“参考答案”，离正确答案有多远？

    在练什么：看清两种方法各自错在哪里——MC 每局的参考答案很吵，但平均是对的；
    TD 的参考答案安静，但表不准时会一直偏。GAE 的 λ 就是在这两种毛病之间调（单元 4 的小题）。

    题设（同第 0 部分，这里重述）：
    - γ = 1。每局从 C 出发，每步向左、向右各 1/2；只有走进右端的那一步 r = +1，其余每一步 r = 0。
    - 我们想估计 v_pi(C)，正确答案是 0.5。

    “参考答案”是什么：每跑完一局，两种方法都会拿一个数去更新 V(C)（式 6.1、6.2 方括号里减号前面那一项）：
    - MC：这一局从右端结束就给 1，从左端结束就给 0（就是 G_0，和 V 表无关）。
    - TD：只看第一步走到哪一格，走到 B 就给表里的 V(B)，走到 D 就给 V(D)（就是 R_1 + γV(S_1)，这一步 R_1 = 0）。

    这题不更新 V，只看这些参考答案。两种 V 表（环境不变，只改 TD 要查的表）：
    - 情况 1：表是准的，V(B) = 2/6，V(D) = 4/6。
    - 情况 2：表在 B、D 不准，V(B) = V(D) = 0.8。

    运行前先写下预测（先手算 4 局，再推广）：
          局   轨迹                          MC 参考答案   TD 参考答案（情况 1）
          1    C → D → E → 右端               1            V(D) = 4/6
          2    C → B → A → 左端               0            V(B) = 2/6
          3    C → D → C → B → A → 左端       0            V(D) = 4/6
          4    C → B → C → D → E → 右端       1            V(B) = 2/6
    (1) 情况 1：每一局里，MC 的参考答案离 0.5 差多少？TD 的呢？
        你的预测：
    (2) 情况 2：这 4 局里 MC 那一列变不变？TD 那一列变成什么，每局离 0.5 差多少？
        你的预测：
    (3) 程序会跑 20000 局，打印每种参考答案的“平均”“偏差 = 平均 − 0.5”“方差”。
        方差 = 每局“离平均差多少”的平方，再取平均。按你 (1)(2) 的数，猜四个方差各是多少：
        情况 1 的 MC、TD；情况 2 的 MC、TD。
        你的预测：
    (4) 用 (1)–(3) 的数回答两件事：
        - V 表不准时（情况 2），哪种参考答案受影响，哪种不受？
        - V 表准时（情况 1），哪种参考答案更吵？为什么？
          提示：MC 的结局取决于整局里每一步往哪走，TD 只取决于第一步（后面的随机性被表里的一个数替代了）。
        这两点分别对应 GAE 里 λ 的哪一头（λ=1 是 MC，λ=0 是 TD）？
        你的预测：
    """
    cases = {"情况 1（V 准）": v_pi.copy(), "情况 2（V(B)、V(D) 高估成 0.8）": v_pi.copy()}
    cases["情况 2（V(B)、V(D) 高估成 0.8）"][[2, 4]] = 0.8
    rng = np.random.default_rng(0)
    episodes = [generate_episode(rng) for _ in range(20000)]
    for name, V in cases.items():
        mc = np.array([returns(rw, GAMMA)[0] for _, rw in episodes])
        td = np.array([td_target(V, rw[0], st[1], GAMMA) for st, rw in episodes])
        print(name)
        for label, x in [("MC 目标 G_0", mc), ("TD 目标 R_1+γV(S_1)", td)]:
            print(f"  {label:<22} 取值 {sorted({round(float(v), 4) for v in x})}  平均 {x.mean():.4f}  "
                  f"偏差 {x.mean() - 0.5:+.4f}  方差 {x.var():.4f}")


RUN = [problem_A, problem_B, problem_C]   # 要跑哪些题就放哪些；先只跑 problem_A 自查

if __name__ == "__main__":
    for problem in RUN:
        print("=" * 20, problem.__name__, "=" * 20)
        problem()
