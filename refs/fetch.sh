#!/usr/bin/env bash
# 下载 refs/README.md 中列出的资料到本目录。已存在的文件跳过，失败的继续下一个。
# 用法：bash refs/fetch.sh [core|stage|window|all]，默认 core。
set -u
cd "$(dirname "$0")"

core=(
  "SB2.pdf http://incompleteideas.net/book/RLbook2020.pdf"
  "DS-L01.pdf https://www.davidsilver.uk/wp-content/uploads/2020/03/intro_RL.pdf"
  "DS-L02.pdf https://www.davidsilver.uk/wp-content/uploads/2020/03/MDP.pdf"
  "DS-L03.pdf https://www.davidsilver.uk/wp-content/uploads/2020/03/DP.pdf"
  "DS-L04.pdf https://www.davidsilver.uk/wp-content/uploads/2020/03/MC-TD.pdf"
  "DS-L05.pdf https://www.davidsilver.uk/wp-content/uploads/2020/03/control.pdf"
  "DS-L06.pdf https://www.davidsilver.uk/wp-content/uploads/2020/03/FA.pdf"
  "DS-L07.pdf https://www.davidsilver.uk/wp-content/uploads/2020/03/pg.pdf"
  "DS-L08.pdf https://www.davidsilver.uk/wp-content/uploads/2020/03/dyna.pdf"
  "DS-L09.pdf https://www.davidsilver.uk/wp-content/uploads/2020/03/XX.pdf"
  "DS-L10.pdf https://www.davidsilver.uk/wp-content/uploads/2020/03/games.pdf"
  # CS285 讲次按当前学期编号，变动时改这里
  "CS285-policy-gradients.pdf https://rail.eecs.berkeley.edu/deeprlcourse/deeprlcourse/static/slides/lec-5.pdf"
  "CS285-actor-critic.pdf https://rail.eecs.berkeley.edu/deeprlcourse/deeprlcourse/static/slides/lec-6.pdf"
  "CS285-value-functions.pdf https://rail.eecs.berkeley.edu/deeprlcourse/deeprlcourse/static/slides/lec-7.pdf"
  "CS285-deep-q.pdf https://rail.eecs.berkeley.edu/deeprlcourse/deeprlcourse/static/slides/lec-8.pdf"
  "CS285-advanced-pg.pdf https://rail.eecs.berkeley.edu/deeprlcourse/deeprlcourse/static/slides/lec-9.pdf"
)

stage=(
  "DQN-2013.pdf https://arxiv.org/pdf/1312.5602"
  "DDQN-2016.pdf https://arxiv.org/pdf/1509.06461"
  "GAE-2016.pdf https://arxiv.org/pdf/1506.02438"
  "TRPO-2015.pdf https://arxiv.org/pdf/1502.05477"
  "PPO-2017.pdf https://arxiv.org/pdf/1707.06347"
  "SAC-2018.pdf https://arxiv.org/pdf/1801.01290"
  "SAC-2018b.pdf https://arxiv.org/pdf/1812.05905"
)

window=(
  "W-MuZero.pdf https://arxiv.org/pdf/1911.08265"
  "W-CQL.pdf https://arxiv.org/pdf/2006.04779"
  "W-RND.pdf https://arxiv.org/pdf/1810.12894"
  "W-DreamerV3.pdf https://arxiv.org/pdf/2301.04104"
  "W-InstructGPT.pdf https://arxiv.org/pdf/2203.02155"
)

case "${1:-core}" in
  core) items=("${core[@]}") ;;
  stage) items=("${stage[@]}") ;;
  window) items=("${window[@]}") ;;
  all) items=("${core[@]}" "${stage[@]}" "${window[@]}") ;;
  *) echo "用法：$0 [core|stage|window|all]"; exit 1 ;;
esac

failed=()
for item in "${items[@]}"; do
  name=${item%% *}; url=${item#* }
  if [ -s "$name" ]; then echo "跳过  $name（已存在）"; continue; fi
  if curl -fsSL -m 120 -A "Mozilla/5.0" -o "$name.part" "$url" \
     && head -c 5 "$name.part" | grep -q '%PDF'; then
    mv "$name.part" "$name"; echo "完成  $name"
  else
    rm -f "$name.part"; failed+=("$name $url"); echo "失败  $name  $url"
  fi
done

if [ ${#failed[@]} -gt 0 ]; then
  echo; echo "以下 ${#failed[@]} 个下载失败，链接可能已变动，请手动下载或修改本脚本："
  printf '  %s\n' "${failed[@]}"
  exit 1
fi
