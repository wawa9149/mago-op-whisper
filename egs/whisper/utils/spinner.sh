#!/bin/bash
# encoding: utf-8
# Copyright (c) 2024- SATURN
# AUTHORS
# Sukbong Kwon (Galois)

function shutdown() {
  tput cnorm # reset cursor
}
trap shutdown EXIT

function cursorBack() {
  echo -en "\033[$1D"
}

function spinner() {
  #make sure we use non-unicode character type locale
  #that way it works for any locale as long as the font supports the characters)
  local LC_CTYPE=C
  local pid=$1 # Process Id of the previous running command

  spinner_index=11

  case ${spinner_index} in
  0)
    local spin='⠁⠂⠄⡀⢀⠠⠐⠈'
    local charwidth=1
    ;;
  1)
    local spin='-\|/'
    local charwidth=1
    ;;
  2)
    local spin="▁▂▃▄▅▆▇█▇▆▅▄▃▂▁"
    local charwidth=1
    ;;
  3)
    local spin="▉▊▋▌▍▎▏▎▍▌▋▊▉"
    local charwidth=1
    ;;
  4)
    local spin='←↖↑↗→↘↓↙'
    local charwidth=1
    ;;
  5)
    local spin='▖▘▝▗'
    local charwidth=1
    ;;
  6)
    local spin='┤┘┴└├┌┬┐'
    local charwidth=1
    ;;
  7)
    local spin='◢◣◤◥'
    local charwidth=1
    ;;
  8)
    local spin='◰◳◲◱'
    local charwidth=1
    ;;
  9)
    local spin='◴◷◶◵'
    local charwidth=1
    ;;
  10)
    local spin='◐◓◑◒'
    local charwidth=1
    ;;
  11)
    local spin='⣾⣽⣻⢿⡿⣟⣯⣷'
    local charwidth=1
    ;;
  esac

  local delay=0.1   # delay between updates
  local i=0         # index into the string while
  tput civis        # cursor invisible
  while kill -0 $pid 2>/dev/null; do
    local i=$(((i + $charwidth) % ${#spin}))
    printf "%s" "${spin:$i:$charwidth}"
    cursorBack 1
    sleep $delay
  done
  tput cnorm
  wait $pid # capture exit code
  return $?
}

function colorful_spinner() {
  local pid=$1
  local colors=("\033[31m" "\033[32m" "\033[33m" "\033[34m" "\033[35m" "\033[36m")
  local spin=("⠋" "⠙" "⠹" "⠸" "⠼" "⠴" "⠦" "⠧" "⠇" "⠏")

  local i=0
  tput civis # 커서 숨기기
  while kill -0 $pid 2>/dev/null; do
    local color=${colors[$((i % ${#colors[@]}))]}
    local symbol=${spin[$((i % ${#spin[@]}))]}
    printf "%b%s\033[0m" "$color" "$symbol"
    cursorBack 1
    sleep 0.1
    i=$((i + 1))
  done
  tput cnorm # 커서 복원
  wait $pid
  return $?
}
