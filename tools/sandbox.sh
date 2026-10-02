#!/usr/bin/env bash
# 给“AI 生成代码”准备一个和课程隔离的目录。
#
# 为什么要隔离：在本仓库里运行别的 AI，它会读到 CLAUDE.md、learner.md、log/ 等课程上下文
# （Claude Code 会从当前目录一路向上加载 CLAUDE.md），输出受课程影响；它也可能改写 log，
# 污染学习记录。沙箱放在仓库外面，里面只有公共环境 rl_lab/ 和需求说明 SPEC.md。
#
# 用法（在仓库根目录）：
#   tools/sandbox.sh new <名字> [需求说明文件]
#       建 $RL_SANDBOX/<名字>/（默认 ~/rl-sandbox/<名字>/），放入 rl_lab/ 和 SPEC.md。
#       然后在那个目录里打开你的 AI 工具，让它只按 SPEC.md 写代码。
#   tools/sandbox.sh collect <名字> <实验目录>
#       把沙箱里 AI 写的文件（rl_lab/ 除外）复制到 <实验目录>/ai/<名字>/，原样保留，再由你提交。
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
BASE="${RL_SANDBOX:-$HOME/rl-sandbox}"

usage() { sed -n '2,15p' "$0"; exit 1; }

cmd="${1:-}"; name="${2:-}"
[[ -z "$cmd" || -z "$name" ]] && usage
dir="$BASE/$name"

case "$cmd" in
  new)
    mkdir -p "$BASE"
    base_real="$(cd "$BASE" && pwd -P)"
    repo_real="$(cd "$REPO" && pwd -P)"
    if [[ "$base_real/" == "$repo_real/"* ]]; then
      echo "沙箱目录 $BASE 在仓库里面，起不到隔离作用。请把 RL_SANDBOX 设到仓库外。" >&2; exit 1
    fi
    if [[ -e "$dir" ]]; then echo "$dir 已存在，换个名字或先删掉。" >&2; exit 1; fi
    mkdir -p "$dir/rl_lab"
    cp "$REPO/rl_lab/__init__.py" "$REPO/rl_lab/gridworld.py" "$dir/rl_lab/"
    if [[ -n "${3:-}" ]]; then
      cp "$3" "$dir/SPEC.md"
    else
      printf '# 需求说明\n\n（把你写的需求说明贴在这里）\n' > "$dir/SPEC.md"
    fi
    cat > "$dir/README.md" <<'EOF'
# 独立编码任务

按 SPEC.md 实现代码，放在本目录。可以使用 rl_lab/（网格世界环境，见 rl_lab/gridworld.py 的说明），不要修改它。
只在本目录内工作，不要读取或修改本目录以外的文件。
EOF
    echo "沙箱已建好：$dir"
    echo "下一步：编辑 $dir/SPEC.md，然后在该目录里打开 AI 工具。"
    ;;
  collect)
    dest="${3:-}"; [[ -z "$dest" ]] && usage
    [[ -d "$dir" ]] || { echo "找不到 $dir" >&2; exit 1; }
    out="$REPO/$dest/ai/$name"
    mkdir -p "$out"
    (cd "$dir" && find . -type f ! -path './rl_lab/*' ! -name '*.pyc' ! -path '*/__pycache__/*' -print0 \
      | xargs -0 -I{} cp --parents {} "$out/")
    echo "已复制到 $out："
    (cd "$out" && find . -type f | sort)
    ;;
  *) usage ;;
esac
