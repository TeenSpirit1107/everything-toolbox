#!/usr/bin/env bash
echo "==== System Cleaner for Ubuntu ===="
echo "==== Author: Yimeng (Rosalind) ===="
echo "==== Github Profile: https://github.com/TeenSpirit1107 ===="
echo "==== Email: yimengteng@link.cuhk.edu.cn ===="
if [ "$#" -eq 0 ]; then
  echo "Usage: $0 <pid1> [pid2 pid3 ...]"
  exit 1
fi

for pid in "$@"; do
  echo "================ PID=$pid ================"
  if [ -d "/proc/$pid" ]; then
    echo "[exe]    $(readlink -f /proc/$pid/exe)"
    echo "[cwd]    $(readlink -f /proc/$pid/cwd)"
    echo "[cmd]    $(tr '\0' ' ' < /proc/$pid/cmdline)"
    echo "[user]   $(ps -o user= -p $pid)"
    echo "[ppid]   $(ps -o ppid= -p $pid | tr -d ' ')"
    echo "[lstart] $(ps -o lstart= -p $pid)"
    echo "[etime ] $(ps -o etime= -p $pid)"
    echo "[etimes] $(ps -o etimes= -p $pid) sec"
    echo "[parents]"
    pstree -sp $pid || true
  else
    echo "PID $pid doesn't exist (may have exited)."
  fi
  echo
done
