#!/bin/bash

echo "Setting up environment..."

# Clone Wav2Lip repo
git clone https://github.com/Rudrabha/Wav2Lip.git wav2lip_repo
cd wav2lip_repo

# Download model file
mkdir checkpoints
gdown https://drive.google.com/uc?id=1rwXkUtGSsBvQkKfPzD3hGEGVzI94pJrO -O checkpoints/wav2lip_gan.pth

# Move back and run app
cd ..
mv wav2lip_repo/inference.py .
mv wav2lip_repo/checkpoints checkpoints
pip install -r requirements.txt
