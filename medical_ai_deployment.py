#!/usr/bin/env python3
"""
Medical AI Models Non-Blocking Deployment Script
Developed by Gregory Katz (@gregorykatz_microsoft)
"""

import os
import sys
import subprocess
import platform
import time
import threading
import queue
import signal
import argparse

class NonBlockingInstaller:
    def __init__(self, models=None, timeout=3600):
        """
        Initialize deployment with optional model selection and timeout
        
        Args:
            models (list): List of models to install
            timeout (int): Deployment timeout in seconds
        """
        self.home_dir = os.path.expanduser('~')
        self.models_dir = os.path.join(self.home_dir, 'medical-ai-models')
        self.log_file = os.path.join(self.models_dir, 'deployment.log')
        self.timeout = timeout
        self.models = models or ['biomedparse', 'medimageparse']
        
        os.makedirs(self.models_dir, exist_ok=True)

    def _log(self, message):
        """
        Thread-safe logging method
        
        Args:
            message (str): Log message to write
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        with threading.Lock():
            with open(self.log_file, 'a') as log:
                log.write(log_entry)
            print(log_entry.strip())

    def _run_command_with_timeout(self, command, error_queue):
        """
        Run a shell command with timeout and capture output
        
        Args:
            command (str): Command to execute
            error_queue (queue.Queue): Queue to pass errors
        """
        try:
            process = subprocess.Popen(
                command, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                preexec_fn=os.setsid
            )
            
            start_time = time.time()
            while process.poll() is None:
                if time.time() - start_time > self.timeout:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                    error_queue.put(f"Timeout occurred for command: {command}")
                    return
                
                time.sleep(1)
            
            stdout, stderr = process.communicate()
            if stdout:
                self._log(f"Command Output: {stdout}")
            if stderr:
                self._log(f"Command Error: {stderr}")
            
        except Exception as e:
            error_queue.put(str(e))

    def install_system_dependencies(self):
        """
        Install system-level dependencies with non-blocking approach
        """
        self._log("Starting system dependencies installation")
        
        system = platform.system().lower()
        
        if system == 'linux':
            commands = [
                'sudo apt-get update',
                'sudo apt-get install -y build-essential cmake git wget curl python3-dev python3-pip libgl1-mesa-glx libglib2.0-0',
                'sudo apt-get install -y nvidia-cuda-toolkit nvidia-container-toolkit || true'
            ]
        elif system == 'darwin':
            commands = [
                'brew update',
                'brew install cmake git wget curl python3'
            ]
        else:
            self._log(f"Unsupported operating system: {system}")
            return False
        
        error_queue = queue.Queue()
        threads = []
        
        for cmd in commands:
            thread = threading.Thread(
                target=self._run_command_with_timeout, 
                args=(cmd, error_queue)
            )
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join(timeout=self.timeout)
        
        if not error_queue.empty():
            while not error_queue.empty():
                self._log(f"Error during installation: {error_queue.get()}")
            return False
        
        return True

    def install_conda(self):
        """
        Install Miniconda with non-blocking approach
        """
        self._log("Starting Conda installation")
        
        conda_path = os.path.join(self.home_dir, 'miniconda3', 'bin', 'conda')
        if os.path.exists(conda_path):
            self._log("Conda is already installed")
            return True
        
        system = platform.system().lower()
        if system == 'linux':
            install_cmd = (
                'wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh '
                '&& bash miniconda.sh -b -p $HOME/miniconda3 '
                '&& rm miniconda.sh '
                '&& $HOME/miniconda3/bin/conda init bash'
            )
        elif system == 'darwin':
            install_cmd = (
                'wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O miniconda.sh '
                '&& bash miniconda.sh -b -p $HOME/miniconda3 '
                '&& rm miniconda.sh '
                '&& $HOME/miniconda3/bin/conda init bash'
            )
        else:
            self._log(f"Unsupported system for Conda installation: {system}")
            return False
        
        error_queue = queue.Queue()
        thread = threading.Thread(
            target=self._run_command_with_timeout, 
            args=(install_cmd, error_queue)
        )
        thread.start()
        thread.join(timeout=self.timeout)
        
        if not error_queue.empty():
            while not error_queue.empty():
                self._log(f"Conda installation error: {error_queue.get()}")
            return False
        
        return True

    def create_environments(self):
        """
        Create Conda environments for specified models
        """
        self._log("Creating model environments")
        
        model_dependencies = {
            'biomedparse': [
                'torch', 'torchvision', 'detectron2', 
                'transformers', 'huggingface-hub'
            ],
            'medimageparse': [
                'azure-ai-ml', 'azure-identity', 
                'pillow', 'numpy', 'requests'
            ],
            'cxrreportgen': [
                'azure-ai-ml', 'azure-identity', 
                'torch', 'transformers'
            ],
            'medimageinsight': [
                'azure-ai-ml', 'azure-identity', 
                'scikit-learn', 'numpy'
            ]
        }
        
        error_queue = queue.Queue()
        threads = []
        
        for model in self.models:
            if model not in model_dependencies:
                self._log(f"Skipping unknown model: {model}")
                continue
            
            env_name = f"medical-ai-{model}"
            
            create_cmd = (
                f'conda create -n {env_name} python=3.9 -y '
                f'&& conda run -n {env_name} pip install {" ".join(model_dependencies[model])}'
            )
            
            thread = threading.Thread(
                target=self._run_command_with_timeout, 
                args=(create_cmd, error_queue)
            )
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join(timeout=self.timeout)
        
        if not error_queue.empty():
            while not error_queue.empty():
                self._log(f"Environment creation error: {error_queue.get()}")
            return False
        
        return True

    def deploy(self):
        """
        Main deployment method with non-blocking approach
        """
        self._log("Starting Medical AI Models Deployment")
        
        try:
            if not self.install_system_dependencies():
                self._log("System dependencies installation failed")
                return False
            
            if not self.install_conda():
                self._log("Conda installation failed")
                return False
            
            if not self.create_environments():
                self._log("Environment creation failed")
                return False
            
            self._log("Medical AI Models Deployment Completed Successfully")
            return True
        
        except Exception as e:
            self._log(f"Deployment failed: {e}")
            return False

def parse_arguments():
    """
    Parse command-line arguments
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Medical AI Models Deployment")
    parser.add_argument(
        '--models', 
        nargs='+', 
        default=['biomedparse', 'medimageparse'],
        help='Specify models to install (default: biomedparse medimageparse)'
    )
    parser.add_argument(
        '--timeout', 
        type=int, 
        default=3600,
        help='Deployment timeout in seconds (default: 3600)'
    )
    return parser.parse_args()

def main():
    """
    Main entry point for the deployment script
    """
    args = parse_arguments()
    
    installer = NonBlockingInstaller(
        models=args.models, 
        timeout=args.timeout
    )
    
    success = installer.deploy()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
