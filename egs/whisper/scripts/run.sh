#!/bin/bash
# encoding: utf-8
# Copyright (c) 2025- SATURN
# AUTHORS
# Sukbong Kwon (Galois)

model_root=
model_name=tiny
out_dir=exp/whisper
nocuda=true
n_gpu=
lang=ko
task=transcribe


[ -f ./path.sh ] && . ./path.sh
. ./utils/parse_options.sh || exit 1;

help_message=(
"usage: run.sh [options] <audio file>
main options:
    --lang <str>        : language code (default=en)
    --model_root <path> : model root directory (default=models/mstudio/speech_recognition/whisper)
    --model_name <path> : model name (default=small.en)
    --out_dir <path>    : output directory (default=exp/whisper)
    <audio>
")

# Check input file
if [ $# != 1 ]; then
  printf "${help_message}\n" 1>&2
  exit 1;
fi
audio=$1

# Load 'spinner' function
. ./utils/spinner.sh

options=""
if [ ${nocuda} == true ]; then
  options="--nocuda"
fi

[ ! -z ${model_root} ] && options="--model-root ${model_root}"

# Set CUDA_VISIBLE_DEVICES
cuda_visible_devices=""
if [ ! -z ${n_gpu} ]; then
  cuda_visible_devices="CUDA_VISIBLE_DEVICES=${n_gpu}"
fi

# Run transcribe
eval "${cuda_visible_devices} python local/transcribe.py \
    --model-name ${model_name} \
    ${options} \
    --lang ${lang} \
    --out-dir ${out_dir} \
    --task ${task} \
    ${audio} &"

colorful_spinner $!
exit $?

