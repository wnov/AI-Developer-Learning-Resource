# 参考资料

把以下资料放进本目录，Claude 解释时会锚定并标注出处。文件名带上缩写，便于引用。

自动下载：`bash refs/fetch.sh`（必备资料），`bash refs/fetch.sh stage | window | all` 下载其余部分。已存在的文件会跳过；链接失效时脚本会列出失败项。

优先级：**必备**是首次诊断和阶段 1 前就要放好的；**阶段论文**到对应阶段再放；**窗口论文**在阶段末窗口会话前放；**补充**可选，不作为主要出处。

## 必备：三套主干资料

| 缩写 | 资料 | 获取 | 建议文件名 |
| --- | --- | --- | --- |
| SB | Sutton & Barto《Reinforcement Learning: An Introduction》第 2 版（2020） | 作者官网免费 PDF：http://incompleteideas.net/book/the-book-2nd.html （直链 http://incompleteideas.net/book/RLbook2020.pdf ） | `SB2.pdf` |
| DS | David Silver UCL RL 课程（2015），10 讲 slides + 视频 | slides：https://www.davidsilver.uk/teaching/ ；视频：https://www.youtube.com/playlist?list=PLqYmG7hTraZDM-OYHWgPebj2MfCFzFObQ | `DS-L01.pdf` … `DS-L10.pdf` |
| CS285 | Berkeley CS285 Deep RL（Sergey Levine） | 课程主页：https://rail.eecs.berkeley.edu/deeprlcourse/ ；视频：https://www.youtube.com/playlist?list=PL_iWQOsE6TfX7MaC6C3HcdOf1g337dlC9 | `CS285-<主题>.pdf` |

DS 讲次与 `graph.md` 的对应：

| 讲次 | 主题 | 用于 |
| --- | --- | --- |
| L2 | Markov Decision Processes | S1.1–S1.3 |
| L3 | Planning by Dynamic Programming | S1.4–S1.5 |
| L4 | Model-Free Prediction | S2.1–S2.3 |
| L5 | Model-Free Control | S2.4–S2.7 |
| L6 | Value Function Approximation | S3.1 |
| L7 | Policy Gradient Methods | S4.1 |
| L8 | Integrating Learning and Planning | B2 |
| L9 | Exploration and Exploitation | B4 |

CS285 只需下载以下几讲的 slides（讲次每学期可能变动，以课程主页为准）：

| 主题 | 用于 | 建议文件名 |
| --- | --- | --- |
| Policy Gradients | S4.1–S4.2 | `CS285-policy-gradients.pdf` |
| Actor-Critic Algorithms | S4.3–S4.4 | `CS285-actor-critic.pdf` |
| Value Function Methods | S3.1–S3.2 | `CS285-value-functions.pdf` |
| Deep RL with Q-Functions | S3.3–S3.4 | `CS285-deep-q.pdf` |
| Advanced Policy Gradients | S5.1 | `CS285-advanced-pg.pdf` |

## 阶段论文

| 节点 | 论文 | 链接 | 建议文件名 |
| --- | --- | --- | --- |
| S3.3 | Mnih et al. 2015, Human-level control through deep reinforcement learning（Nature） | https://www.nature.com/articles/nature14236 ；无付费墙的前身版本 arXiv 1312.5602 | `DQN-2015.pdf` |
| S3.4 | van Hasselt et al. 2016, Deep Reinforcement Learning with Double Q-learning | https://arxiv.org/abs/1509.06461 | `DDQN-2016.pdf` |
| S4.4 | Schulman et al. 2016, High-Dimensional Continuous Control Using GAE | https://arxiv.org/abs/1506.02438 | `GAE-2016.pdf` |
| S5.1 | Schulman et al. 2015, Trust Region Policy Optimization | https://arxiv.org/abs/1502.05477 | `TRPO-2015.pdf` |
| S5.2 | Schulman et al. 2017, Proximal Policy Optimization Algorithms | https://arxiv.org/abs/1707.06347 | `PPO-2017.pdf` |
| S5.3 | Haarnoja et al. 2018, Soft Actor-Critic | https://arxiv.org/abs/1801.01290 ；自动调温度的版本见 https://arxiv.org/abs/1812.05905 | `SAC-2018.pdf`、`SAC-2018b.pdf` |

## 窗口论文

与 `plan.md` 阶段时间表一一对应。窗口会话只看问题设定和核心方法图。

| 阶段末 | 分支 | 论文 | 链接 | 建议文件名 |
| --- | --- | --- | --- | --- |
| 1 | B2 | Schrittwieser et al. 2020, MuZero | https://arxiv.org/abs/1911.08265 | `W-MuZero.pdf` |
| 2 | B1 | Kumar et al. 2020, Conservative Q-Learning（CQL） | https://arxiv.org/abs/2006.04779 | `W-CQL.pdf` |
| 3 | B4 | Burda et al. 2018, Random Network Distillation（RND） | https://arxiv.org/abs/1810.12894 | `W-RND.pdf` |
| 4 | B2 | Hafner et al. 2023, DreamerV3 | https://arxiv.org/abs/2301.04104 | `W-DreamerV3.pdf` |
| 5 | B3 | Ouyang et al. 2022, InstructGPT | https://arxiv.org/abs/2203.02155 | `W-InstructGPT.pdf` |

## 补充（可选）

不作为主要出处；引用时标注来源名称。

| 资料 | 用途 | 链接 |
| --- | --- | --- |
| SB 中译本《强化学习（第 2 版）》，俞凯等译 | 中文对照阅读，章节编号与原书一致 | 电子工业出版社 |
| OpenAI Spinning Up | 策略梯度推导和算法伪代码的简明版本，阶段 4–5 对照 | https://spinningup.openai.com/ |
| The 37 Implementation Details of PPO | 阶段 5 实验块：PPO 跑不起来时逐条排查 | https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/ |
| CleanRL | 单文件参考实现。按协议，只在自己实现跑通或卡住后用来对照 | https://github.com/vwxyzjn/cleanrl |
| Gymnasium 文档 | 实验环境 API（CartPole、CliffWalking、Pendulum） | https://gymnasium.farama.org/ |
