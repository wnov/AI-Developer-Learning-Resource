# S1.4 策略改进：题设脚本

理论会话 S1.4（2026-10-02）用到的计算都集成在 `s1_4.py`，改题设只改命令行参数，不用改代码。

```
python labs/1-policy-improvement/s1_4.py                        # 等概率随机策略 π，π′ 只把状态 6 改成向左
python labs/1-policy-improvement/s1_4.py --change 6=left 9=up   # 同时改多个状态
python labs/1-policy-improvement/s1_4.py --change 6=down --q 6 5 # 另外打印状态 5 的 q_π
python labs/1-policy-improvement/s1_4.py --gamma 0.9
```

输出：v_π、被改状态的 q_π(s,·)、v_π′、差值 d = v_π′ − v_π。

你自己的检查（例如数经过状态 6 的次数）如果交给 AI 写，在沙箱里写，见 `tools/sandbox.sh`；收回后放在本目录的 `ai/` 下。环境用 `rl_lab.gridworld.GridWorld`，其中 `rollout(pi, start)` 返回一条轨迹 `[(S_t, A_t, R_{t+1}), ...]`，`policy_with({6: "left"})` 构造 π′。
