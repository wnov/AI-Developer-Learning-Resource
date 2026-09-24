# RL 学习系统

一个由 Claude 运行的交互式强化学习学习项目。Claude 不做讲师，而是维护学习状态、选择下一步、施加压力、纠正错误；主动思考的一方始终是学习者。

完整协议见 [`CLAUDE.md`](CLAUDE.md)。

## 结构

| 文件 / 目录 | 内容 |
| --- | --- |
| [`CLAUDE.md`](CLAUDE.md) | 学习系统协议：会话类型、流程、掌握等级规则 |
| [`graph.md`](graph.md) | 概念依赖图：主干 S1–S5 + 分支 B1–B4 占位 |
| [`learner.md`](learner.md) | 学习者模型：各节点掌握等级、证据、兴趣信号 |
| [`plan.md`](plan.md) | 当前计划、阶段时间表、调整记录、协议待改 |
| `log/` | 每次会话记录，`YYYY-MM-DD.md` |
| [`refs/`](refs/README.md) | 参考资料（SB、DS、CS285、论文） |
| `labs/` | 交互实验和算法实现，`labs/<阶段编号>-<算法名>/` |

## 主干

1. 表格方法基础：MDP、Bellman 方程、策略迭代、价值迭代
2. 无模型预测与控制：MC、TD、SARSA、Q-learning、off-policy
3. 函数逼近：半梯度、致命三角、DQN、Double DQN
4. 策略梯度：REINFORCE、baseline、actor-critic、GAE
5. 现代算法：TRPO、PPO、SAC

主干完成后，根据 `learner.md` 中的兴趣信号，在 B1 offline RL / B2 world model / B3 RLHF / B4 探索中选择方向展开。

## 使用

1. 把参考资料放进 `refs/`（见 `refs/README.md`）。
2. 在本目录启动 Claude Code，它会读取 `CLAUDE.md` 并按开场流程开始。
3. 第一次会话是诊断，不讲新内容。
