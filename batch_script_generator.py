import csv
import os

# 实验索引和起始路径
experiment_name = 'YourExperimentName'

# CSV 文件名
csv_filename = f'./HyperParams{experiment_name}.csv'

# 批处理文件夹
BatchFolder = f'./Batches/{experiment_name}'

# 检查批处理文件夹是否存在，如果不存在则创建
if not os.path.exists(BatchFolder):
    os.makedirs(BatchFolder)

# 起始字符串, String copied to every batch file to covey job array <job_id> and <task_id>

StartStr = \
'''# Check if both job ID and task ID are provided as arguments
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Error: Job ID and Task ID are required. Usage: ./Job.sh <job_id> <task_id>"
  exit 1
fi

# Assign the job ID and task ID to variables
job_id=$1
task_id=$2

python ./python_script_to_sub.py  --job_id $job_id --task_id $task_id  '''

# 文件索引
FileIndex = 0

# 读取 CSV 文件
with open(csv_filename, mode='r', newline='') as fileToRead:
    csv_reader = csv.reader(fileToRead, delimiter=',', quotechar='"')
    for row in csv_reader:
        # 跳过空行或只有单个元素的行（通常是标题行）
        if len(row) < 2:
            continue

        # 增加文件索引
        FileIndex += 1

        # 构造命令行参数
        line_ex = ' '.join([f'{param}' if isinstance(param, str) else str(param) for param in row])

        # 写入 shell 脚本文件
        with open(os.path.join(BatchFolder, f'Job_{FileIndex}.sh'), 'w') as fileToWrite:
            fileToWrite.write(f'{StartStr}{line_ex}')

print("批处理文件生成完毕。")