import numpy as np

""" 环境设定
T   1   2   3
 4   5   6   7
 8   9  10  11
12  13  14   T

非终止状态 𝒮 = {1, …, 14}。两个 T 是同一个终止状态。
动作 𝒜 = {上, 下, 左, 右}，转移是确定的；会走出网格的动作让状态保持不变。
每一步转移的奖励都是 −1，直到进入终止状态。
不打折：γ = 1。回合制任务。
策略 π：四个动作各 0.25 的概率。

vπ(s) = E[Gt | St = s] = E[Rt+1 + γGt+1 | St = s] = E[Rt+1 + γvπ(St+1) | St = s] = ∑a π(a|s) ∑s',r p(s', r | s, a) [r + γvπ(s')] = ∑s'[∑r p(s', r | s)] [r(s, s') + γvπ(s')] = ∑s' p(s' | s) [r(s, s') + γvπ(s')]
"""

STATE_SIZE=16
#       0     1     2     3     4     5     6     7     8     9     10    11    12    13    14    15
p_s0 = [1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
p_s1 = [0.25, 0.25, 0.25, 0.00, 0.00, 0.25, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
p_s2 = [0.00, 0.25, 0.25, 0.25, 0.00, 0.00, 0.25, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
p_s3 = [0.00, 0.00, 0.25, 0.50, 0.00, 0.00, 0.00, 0.25, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
p_s4 = [0.25, 0.00, 0.00, 0.00, 0.25, 0.25, 0.00, 0.00, 0.25, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
p_s5 = [0.00, 0.25, 0.00, 0.00, 0.25, 0.00, 0.25, 0.00, 0.00, 0.25, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
p_s6 = [0.00, 0.00, 0.25, 0.00, 0.00, 0.25, 0.00, 0.25, 0.00, 0.00, 0.25, 0.00, 0.00, 0.00, 0.00, 0.00]
p_s7 = [0.00, 0.00, 0.00, 0.25, 0.00, 0.00, 0.25, 0.25, 0.00, 0.00, 0.00, 0.25, 0.00, 0.00, 0.00, 0.00]
p_s8 = [0.00, 0.00, 0.00, 0.00, 0.25, 0.00, 0.00, 0.00, 0.25, 0.25, 0.00, 0.00, 0.25, 0.00, 0.00, 0.00]
p_s9 = [0.00, 0.00, 0.00, 0.00, 0.00, 0.25, 0.00, 0.00, 0.25, 0.00, 0.25, 0.00, 0.00, 0.25, 0.00, 0.00]
p_s10 = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.25, 0.00, 0.00, 0.25, 0.00, 0.25, 0.00, 0.00, 0.25, 0.00]
p_s11 = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.25, 0.00, 0.00, 0.25, 0.25, 0.00, 0.00, 0.00, 0.25]
p_s12 = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.25, 0.00, 0.00, 0.00, 0.50, 0.25, 0.00, 0.00]
p_s13 = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.25, 0.00, 0.00, 0.25, 0.25, 0.25, 0.00]
p_s14 = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.25, 0.00, 0.00, 0.25, 0.25, 0.25]
p_s15 = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00]


P_sn = np.array([p_s0, p_s1, p_s2, p_s3, p_s4, p_s5, p_s6, p_s7, p_s8, p_s9, p_s10, p_s11, p_s12, p_s13, p_s14, p_s15])
R_sn = -1.0 * (P_sn != 0)

def solve_two_array(θ=1e-4, γ=1.0, P_sn=P_sn, R_sn=R_sn, STATE_SIZE=STATE_SIZE, T_self_reword=0, max_round=10000):
    R_sn[0, 0] = T_self_reword
    R_sn[STATE_SIZE-1, STATE_SIZE-1] = T_self_reword
    v_k = np.zeros(STATE_SIZE)
    i = 0
    while True:
        i+=1
        v_k1 = np.zeros(STATE_SIZE)
        for s in range(STATE_SIZE):
            v_k1[s] =np.sum([P_sn[s][s_] * (R_sn[s][s_] + γ * v_k[s_]) for s_ in range(STATE_SIZE)])

        # print(np.max(v_k1 - v_k))
        if np.max(np.abs(v_k1 - v_k)) < θ or i >= max_round:
            break
        v_k = v_k1.copy()
    return v_k1, i

def solve_in_place(θ=1e-4, γ=1.0, P_sn=P_sn, R_sn=R_sn, STATE_SIZE=STATE_SIZE, T_self_reword=0, max_round=10000, reverse=False):
    R_sn[0, 0] = T_self_reword
    R_sn[STATE_SIZE-1, STATE_SIZE-1] = T_self_reword
    v_k = np.zeros(STATE_SIZE)
    i = 0
    while True:
        i += 1
        vk_backup = v_k.copy()
        if not reverse:
            for s in range(STATE_SIZE):
                v_k[s] = np.sum([P_sn[s][s_] * (R_sn[s][s_] + γ * v_k[s_]) for s_ in range(STATE_SIZE)])
        else:
            for s in range(STATE_SIZE-1, -1, -1):
                v_k[s] = np.sum([P_sn[s][s_] * (R_sn[s][s_] + γ * v_k[s_]) for s_ in range(STATE_SIZE)])

        # print(np.max(v_k - vk_backup))
        if np.max(np.abs(v_k - vk_backup)) < θ or i >= max_round:
            break
    return v_k, i

def solve_matric(γ=1.0, P_sn=P_sn, STATE_SIZE=STATE_SIZE, T_self_reword=0):
    R = np.array([-1.] * STATE_SIZE)
    V = np.array([0.] * STATE_SIZE)
    R[0] = T_self_reword
    R[STATE_SIZE-1] = T_self_reword
    if γ==1.0 and T_self_reword!=0.0:
        V = np.linalg.solve(np.eye(STATE_SIZE)- γ*P_sn, R)
    elif γ!=1.0:
        V = np.linalg.solve(np.eye(STATE_SIZE)- γ*P_sn, R)
    else: # γ==1.0 and T_self_reword==0.0, V[T]=0
        V[1:-1] = np.linalg.solve(np.eye(STATE_SIZE - 2)- γ*P_sn[1:-1, 1:-1], R[1:-1])
    return V

if __name__ == "__main__":
    print("Task1:")
    print("θ\tround inplace\tround two_array\terror inplcae\terror two_array")
    solution_matric = solve_matric()
    for m in [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8]:
        solution_inplace, round_inplace = solve_in_place(θ=m)
        solution_two_array, round_two_array = solve_two_array(θ=m)
        error_inplace = np.max(np.abs(solution_inplace - solution_matric))
        error_two_array = np.max(np.abs(solution_two_array - solution_matric))
        print(f"{m}\t{round_inplace}\t{round_two_array}\t{error_inplace:.2e}\t{error_two_array:.2e}")

    print("\nTask2:")
    γ=0.9
    solution_matric = solve_matric(γ=γ)
    solution_inplace, round_inplace = solve_in_place(γ=γ)
    solution_two_array, round_two_array = solve_two_array(γ=γ)
    error_inplace = np.max(np.abs(solution_inplace - solution_matric))
    error_two_array = np.max(np.abs(solution_two_array - solution_matric))
    print("v inplcae:")
    print(solution_inplace.reshape(4, 4).tolist())
    print(f"round inplace: {round_inplace}")
    print(f"error inplace: {error_inplace}")
    print("v two_array:")
    print(solution_two_array.reshape(4, 4).tolist())
    print(f"round two_array: {round_two_array}")
    print(f"error two_array: {error_two_array}")

    print("\nTask3:")
    print("round inplace\t round inplace reverse")
    θ = 1e-4
    solution_inplace, round_inplace = solve_in_place(θ=θ)
    solution_inplace_reverse, round_inplace_reverse = solve_in_place(θ=θ, reverse=True)
    print(f"{round_inplace}\t{round_inplace_reverse}")

    print("\nTask4:")
    print("T_self_reword = -1, γ = 1, max_round=10000")
    print("round inplace < 10000?\tround two_array < 10000?\tv_inplace[1]\tv_inplcae[T]\tv_two_array[1]\tv_two_array[1]\tv_two_array[T]")
    T_self_reword = -1
    γ = 1
    max_round=10000
    solution_inplace, round_inplace = solve_in_place(γ=γ, T_self_reword=T_self_reword, max_round=max_round)
    solution_two_array, round_two_array = solve_two_array(γ=γ, T_self_reword=T_self_reword, max_round=max_round)
    print(f"{round_inplace<10000}\t{round_two_array<10000}\t{solution_inplace[1]}\t{solution_inplace[0]}\t{solution_two_array[1]}\t{solution_two_array[0]}")

    print("T_self_reword = -1, γ = 0.9, max_round=10000")
    print("round inplace < 10000?\tround two_array < 10000?\tv_inplace[1]\tv_inplcae[T]\tv_two_array[1]\tv_two_array[1]\tv_two_array[T]")
    T_self_reword = -1
    γ = 0.9
    max_round=10000
    solution_inplace, round_inplace = solve_in_place(γ=γ, T_self_reword=T_self_reword, max_round=max_round)
    solution_two_array, round_two_array = solve_two_array(γ=γ, T_self_reword=T_self_reword, max_round=max_round)
    print(f"{round_inplace, round_inplace<10000}\t{round_two_array, round_two_array<10000}\t{solution_inplace[1]}\t{solution_inplace[0]}\t{solution_two_array[1]}\t{solution_two_array[0]}")

    print("\nTask5:")
    print("T_self_reword = -1, γ = 0.9:")
    T_self_reword = -1
    γ = 0.9
    solution_matric = solve_matric(γ=γ, T_self_reword=T_self_reword)
    print(solution_matric)
    print("T_self_reword = -1, γ = 1:")
    T_self_reword = -1
    γ = 1
    solution_matric = solve_matric(γ=γ, T_self_reword=T_self_reword)
    print(solution_matric)
