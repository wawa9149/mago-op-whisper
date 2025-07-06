#!/bin/bash
# encoding: utf-8
# Copyright (c) 2025 SATURN
# AUTHORS
# Sukbong Kwon (Galois)

venv=../../venv
force=false
cuda=false

# Create python virtual environment and activate it
echo "Installing '${venv}' python virtual environment."
python -m venv ${venv} --without-pip
source ${venv}/bin/activate
curl https://bootstrap.pypa.io/get-pip.py | python

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

if $cuda; then
    # Install pytorch with CUDA support
    echo "Installing pytorch with CUDA support..."
    pip install torch torchaudio
else
    # Install pytorch without CUDA support
    echo "Installing pytorch without CUDA support..."
    pip install torch torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
fi

# Install whisper
pip install --no-cache-dir git+https://github.com/openai/whisper.git

# Install requriements
echo "Installing requirements..."
pip install -r requirements.txt
echo "Done."
