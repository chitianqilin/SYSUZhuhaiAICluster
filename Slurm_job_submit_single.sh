#!/bin/bash
### Job queue
#SBATCH -p x86_64
###  Number of cores
#SBATCH -n 1
### Number of GPUs
#SBATCH -G 0   # Need #SBATCH -p x86_64_GPU
#SBATCH --output=/share/home/$USER/logs/slurm_outputs/slurm_outputs_%j.log
#SBATCH --error=/share/home/$USER/logs/slurm_errors/slurm_errors_%j.log

# echo $USER_NAME
# echo $USER
# echo $(whoami)
# Email options
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=XXX@XXX.XXX  # change it to your email address
### Job submission with Slurm. See more on https://slurm.schedmd.com/
### Slurm cheatsheet https://slurm.schedmd.com/pdfs/summary.pdf
### For parallel jobs, see https://docs.rc.uab.edu/cheaha/slurm/slurm_tutorial/#example-3-parallel-jobs
### For array jobs, see https://docs.rc.uab.edu/cheaha/slurm/slurm_tutorial/#example-4-array-job
### Job ID and Environment Variables
### Job arrays will have additional environment variables set.
### SLURM_ARRAY_JOB_ID will be set to the first job ID of the array.
### SLURM_ARRAY_TASK_ID will be set to the job array index value.
### SLURM_ARRAY_TASK_COUNT will be set to the number of tasks in the job array.
### SLURM_ARRAY_TASK_MAX will be set to the highest job array index value.
### SLURM_ARRAY_TASK_MIN will be set to the lowest job array index value.

# Setting for Internet
export http_proxy=http://192.168.10.22:3128
export https_proxy=http://192.168.10.22:3128



# Load the environment module (adjust the path as needed for your system)
module load Anaconda/mini3-23.1.0  # Note: Ensure the correct version is loaded
# # conda create -n FlyOrien_env python=3.9
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/share/app_share/install/Miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/share/app_share/install/Miniconda3/etc/profile.d/conda.sh" ]; then
        . "/share/app_share/install/Miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/share/app_share/install/Miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
conda activate your_virtual_env_name



echo "~/logs/slurm_outputs/slurm_outputs_$SLURM_JOB_ID.log"

# 捕获 EXIT 信号，确保终止监控进程
trap 'kill $! 2>/dev/null' EXIT

# 启动监控循环（日志单独保存）
(
  while true; do
    # 获取内存和 Swap 使用量（单位：MB）
    mem_usage=$(free -m | awk '/Mem/{print $3}')
    swap_usage=$(free -m | awk '/Swap/{print $3}')
    # 记录到日志文件
    echo "[$(date)] Memory: ${mem_usage} MB, Swap: ${swap_usage} MB" >> ~/logs/slurm_outputs/slurm_memory_$SLURM_JOB_ID.log
    sleep 5
  done
) &

export PYTHONUNBUFFERED=1
chmod +x ./python_script_to_sub.py
python ./python_script_to_sub.py --experiment FlyOrien --num_input_points 30 --dataset_path dataset/coil_sim_BICUBIC/ --seed 1 --num_KCs 10240 --num_MBONs 72 --PN_sampling_ratio 0.01 --KC_sparseness 0.05 --num_inputs_once 288 --using_binary_KC False --using_binary_weight False --using_DevFly False --normalising_KC True --disable_over_activating_KC True --over_activating_KC_threshold_rate 0.2 --initial_learning_rate 0.75 --lr_decay_factor 1e-05 --sorted_data False --if_center_data True --dtype float32 --test_parallel True --num_workers 4