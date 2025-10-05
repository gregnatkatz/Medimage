#!/bin/bash


if [[ $EUID -ne 0 ]]; then
    echo "This script must be run with sudo"
    exit 1
fi

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

prepare_system() {
    log "Preparing system for Medical AI Models deployment"
    
    log "Updating package lists"
    apt-get update || error "Failed to update package lists"
    
    log "Installing essential dependencies"
    apt-get install -y \
        build-essential \
        git \
        wget \
        curl \
        software-properties-common \
        python3 \
        python3-pip \
        python3-venv \
        libssl-dev \
        libffi-dev \
        || error "Failed to install dependencies"
    
    log "Installing Azure CLI"
    curl -sL https://aka.ms/InstallAzureCLIDeb | bash
    
    log "Installing Miniconda"
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh \
        && bash miniconda.sh -b -p $HOME/miniconda3 \
        && rm miniconda.sh \
        || error "Failed to install Miniconda"
    
    $HOME/miniconda3/bin/conda init bash
    
    log "Checking for NVIDIA GPU"
    if lspci | grep -i nvidia; then
        log "NVIDIA GPU detected. Installing CUDA and GPU drivers"
        
        wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
        mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
        apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
        add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
        
        apt-get update
        apt-get install -y cuda-toolkit-11-6 nvidia-driver-510 \
            || log "Warning: GPU driver installation may have partial failures"
    else
        log "No NVIDIA GPU detected. Skipping GPU driver installation"
    fi
    
    apt-get autoremove -y
    apt-get clean
    
    log "System preparation complete"
}

main() {
    log "Starting Medical AI Models System Preparation"
    
    prepare_system
    
    echo -e "${BLUE}
====================================================
Medical AI Models System Preparation Complete

Next steps:
1. Close and reopen your terminal
2. Run: python medical_ai_deployment.py

For GPU-enabled systems, verify CUDA installation:
- Run: nvidia-smi
- Verify CUDA version: nvcc --version
====================================================
${NC}"
}

main
