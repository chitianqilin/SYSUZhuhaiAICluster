# Neurobot实验室使用珠海AI算力集群的方法

魏天骐 中山大学人工智能学院Neurobot实验室

本文面向的读者为中山大学人工智能学院Neurobot实验室成员或参与科研的同学，针对中山大学高性能计算公共平台（珠海校区）的具体情况，提供一种使用Visual Studio Code进行远程开发和任务提交的方法参考。中山大学的其它成员亦可参考本文。若需分发，请注明原文来源作者。

## 一、背景知识

### （一）现有资料

#### 1. 算力集群平台

中山大学高性能计算公共平台（珠海校区）<https://sse.sysu.edu.cn/article/840>

高性能计算公共平台（珠海校区）使用指南
<https://sse.sysu.edu.cn/sites/default/files/2025-01/%E9%99%84%E4%BB%B68%EF%BC%9A%E9%AB%98%E6%80%A7%E8%83%BD%E8%AE%A1%E7%AE%97%E5%85%AC%E5%85%B1%E5%B9%B3%E5%8F%B0%EF%BC%88%E7%8F%A0%E6%B5%B7%E6%A0%A1%E5%8C%BA%EF%BC%89%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%972.2.pdf>

***注意，在后文中，本文假设读者已经阅读过上述指南。***

#### 2. Slurm

与个人使用的工作站不同，服务器集群通常使用SGE或Slurm进行任务管理。学习使用Slurm，可参考 <https://slurm.schedmd.com/> ， Slurm cheatsheet中整理了一些常用指令 <https://slurm.schedmd.com/pdfs/summary.pdf> ， 其中sbatch为最常用的提交任务的命令，job_array 是最便于尝试不同参数组合的任务类型。更多信息，可参考如下内容：

- sbatch  <https://hpc.pku.edu.cn/_book/guide/slurm/sbatch.html>
- job_array <https://slurm.schedmd.com/job_array.html>
- For array job examples, see <https://docs.rc.uab.edu/cheaha/slurm/slurm_tutorial/#example-4-array-job>
- For parallel job examples, see <https://docs.rc.uab.edu/cheaha/slurm/slurm_tutorial/#example-3-parallel-jobs>

#### 3. Visual Studio Code

本文主要使用Visual Studio Code作为例子示范如何高效地使用算力集群平台。相关文档请见：
<https://code.visualstudio.com/docs>

### （二）申请账号

参考中山大学高性能计算公共平台（珠海校区）网页 <https://sse.sysu.edu.cn/article/840> ，相关信息如下：

>（二）申请组账户变更（老用户）
>
>已有组账户如需新增子账号、注销子账号等，请填写[《高性能计算公共平台（珠海校区）组账户变更申请表》（附件5）](https://sse.sysu.edu.cn/sites/default/files/2025-01/%E9%99%84%E4%BB%B65%EF%BC%9A%E9%AB%98%E6%80%A7%E8%83%BD%E8%AE%A1%E7%AE%97%E5%85%AC%E5%85%B1%E5%B9%B3%E5%8F%B0%EF%BC%88%E7%8F%A0%E6%B5%B7%E6%A0%A1%E5%8C%BA%EF%BC%89%E7%BB%84%E8%B4%A6%E6%88%B7%E5%8F%98%E6%9B%B4%E7%94%B3%E8%AF%B7%E8%A1%A8.zip)，作为附件发送至邮箱（<hpczh@mail.sysu.edu.cn>），邮件主题请填写“高性能计算公共平台-组账户变更”。平台确认批准后，邮箱返回变更信息。

Neurobot组的组账户为weitq3。填写好该表后与实验室科研助理洪爱施老师沟通。

### （三）主要服务器信息

如[高性能计算公共平台（珠海校区）使用指南](https://sse.sysu.edu.cn/sites/default/files/2025-01/%E9%99%84%E4%BB%B68%EF%BC%9A%E9%AB%98%E6%80%A7%E8%83%BD%E8%AE%A1%E7%AE%97%E5%85%AC%E5%85%B1%E5%B9%B3%E5%8F%B0%EF%BC%88%E7%8F%A0%E6%B5%B7%E6%A0%A1%E5%8C%BA%EF%BC%89%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%972.2.pdf)所述:

>### 1.1 超算组成
>
>超算主要由四部分组成：跳板服务器、登陆服务器、计算服务器、调度系统
>
>- 跳板服务器。一台既连接了校园网又连接了超算内网的服务器。用户通过该机器可以从校园网中访问处于内网中的超算集群。IP地址为：172.16.108.134 ，端口为22。
>- 登陆服务器。专门给用户远程登陆使用的服务器。IP地址为：192.168.10.15 ，端口为22。用户凭集群及密码登入服务器，然后在服务器上可进行文件上传下载、文件编辑、程序编译、软件安装、计算任务提交等操作，但不能直接运行计算任务，否则会导致机器卡顿，影响其他用户登陆及使用。
>- 计算服务器。专门用来运行计算任务的服务器。计算服务器配置：Intel(R) Xeon(R) Gold 6348 CPU \56核\512G内存\8块Nvidia A800 80G显存，总共7台。
>- 调度系统。所有计算服务器由调度系统分配管理。用户首先向调度系统申请计算资源，然后再由调度系统将计算任务投放到分配的计算服务器上运行。

### （四）主要使用步骤

参考[高性能计算公共平台（珠海校区）使用指南](https://sse.sysu.edu.cn/sites/default/files/2025-01/%E9%99%84%E4%BB%B68%EF%BC%9A%E9%AB%98%E6%80%A7%E8%83%BD%E8%AE%A1%E7%AE%97%E5%85%AC%E5%85%B1%E5%B9%B3%E5%8F%B0%EF%BC%88%E7%8F%A0%E6%B5%B7%E6%A0%A1%E5%8C%BA%EF%BC%89%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%972.2.pdf)所述，并稍加完善后，关键内容如下:

>### 1.2 使用步骤
>
>1. 用户先登陆跳板机。为了保证安全，目前超算集群的服务器节点放置在内网中，只有跳板机节点既连接校园网也连接内网。ssh登陆到跳板机后，同一个Terminal中的后续指令即从跳板机发出，且可与内网中的其它服务器通讯。跳板机既不做计算工作，也不做任务脚本的提交工作。
>2. 再通过跳板机登陆到登陆节点。登陆到跳板机后，我们可以通过ssh嵌套等方式登陆到登陆节点，进行任务脚本的编写和提交，由内网中其它服务器节点完成计算。
>3. 编写计算任务提交脚本。该脚本是一个基于linux指令的.sh文件，包含了向调度系统申请计算资源的指令，以及定义程序运行命令的参数。
>4. 执行任务提交脚本。使用sbatch命令提交脚本文件，将计算任务投放到计算服务器上运行。
>5. 执行squeue、sinfo、scontrol、sacct等命令查看程序运行状态。

### （五）推荐软件

#### 1. 客户端基础软件

基础软件可作为初步尝试时使用的软件，其指令步骤较为具体清晰，但是效率上限较低。

- Linux Terminal / Windows CMD / Windows Powershell，使用ssh指令可以连接到远程计算机，使用scp可复制文件。
- ssh 图形化客户端， 例如 Windows下的[Xshell](https://www.xshell.com/zh/xshell/)、[Bitvise SSH Client](https://bitvise.com/ssh-client)。 注意，Linux下直接使用 Terminal的ssh指令。
- SFTP 图形化客户端， 例如 Windows下的[Xftp](https://www.xshell.com/zh/xftp/)、[Bitvise SSH Client](https://bitvise.com/ssh-client), Linux下直接使用系统的文件管理器。
上述软件的相关教程可在其官网或三方平台查询。其中，ssh和scp教程很多；Xshell和Xftp除官方教程外，还有[高性能计算公共平台（珠海校区）使用指南](https://sse.sysu.edu.cn/sites/default/files/2025-01/%E9%99%84%E4%BB%B68%EF%BC%9A%E9%AB%98%E6%80%A7%E8%83%BD%E8%AE%A1%E7%AE%97%E5%85%AC%E5%85%B1%E5%B9%B3%E5%8F%B0%EF%BC%88%E7%8F%A0%E6%B5%B7%E6%A0%A1%E5%8C%BA%EF%BC%89%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%972.2.pdf)中所述教程。

#### 2. 客户端IDE软件

实验室建议成员在入门后使用IDE软件完成具体工作，IDE全称Integrated Development Environment，意为集成开发环境。实验室建议使用的IDE为[Virtual Studio Code（VSCode）](https://code.visualstudio.com/)，进行远程开发。VSCode中[Remote](https://code.visualstudio.com/docs/remote/remote-overview)系列插件集成了ssh、scp、远程文件预览、编辑、编译、执行等功能，在登录服务器端后可自动完成服务器端VSCode服务的配置，且无需超级用户权限。配置好后，即可像在本地开发一样在服务器中完成开发。

## 二、 客户端配置

本使用方法主要针对Visual Studio Code，未具体考虑具体的操作系统。在实践过程中，若有不同，欢迎提出改进意见。

### （一）配置VSCode

### 1. 安装Remote插件

参考<https://code.visualstudio.com/>以及<https://code.visualstudio.com/docs/remote/remote-overview>，安装VSCode和Remote插件。

### 2. 配置ssh config文件

在windows下，ssh的配置文件通常位于C:\Users\%USERNAME%\.ssh，其中，%USERNAME%表示你在客户端的用户名。配置文件的名字为config。

在本文所述的使用场景中，config的内容如下所示：

``` bash
Host AIClusterJumper
    HostName 172.16.108.134
    User ##YourUsername##
    Port 22

Host AIClusterReception
    HostName 192.168.10.15
    User ##YourUsername##
    Port 22
    ProxyCommand ssh -W %h:%p AIClusterJumper
```

其中AIClusterJumper为跳板机，AIClusterReception为登录节点，这两个名字可以随便起，但是对应的IP一定是172.16.108.134和192.168.10.15。将上述##YourUsername##替换为你从集群管理员那里申请到的用户名。%h 和 %p 是特殊的占位符，用于动态替换对应主机名和端口号。

在配置config文件后，在需要打开服务器端的文件夹或项目时，VSCode的Remote-SSH插件会自动使用该配置文件进行远程连接。

### （二）配置VPN

如果你在校外或没有接入校园网，需要使用学校的VPN服务以接入中山大学的内网。具体请参考<https://inc.sysu.edu.cn/service/vpn>.

###  （三） 使用VSCode连接集群服务器

在连接校园网或者VPN后，打开VSCode，点击左侧Remote Explore按钮，在Remote Explore中点击AIClusterReception后面Connect in New Window按钮，即可按照弹出的提示，逐步操作连接服务器。常见提示包括：

1. 选择平台服务器类型：Select the platform of the remote host "AlClusterReception"。选择Linux。
2. 确认服务器指纹："AlClusterReception" has fingerprint "SHA256 ......"。选择Continue。
3. 输入跳板机中你的用户名下对应密码："Enter password for username@172.16.108.134"。输入密码。
4. 输入登录节点中你的用户名下对应密码："Enter password for username@192.168.10.15"。输入密码。
5. 兼容性提示："You are about to connect to an OS version that is unsupported by Visual Studio Code."。选择Allow。

VSCode此时会自动安装服务器端的vscode-server。至此，客户端的VSCode只是一个前台界面，你此界面中的所有操作都会被映射到服务器端的vscode-server，包括在VSCode左侧Explorer界面中的文件操作、Source Control界面中的操作，使用VSCode执行代码的操作、VSCode集成Terminal中的操作。

# 三、Slurm Script的写法

## （一）语句类型

如项目附带文件[Slurm_job_submit_single.sh](./Slurm_job_submit_single.sh)和[Slurm_job_submit.sh](Slurm_job_submit.sh)所示。Script中的语句分为三大类型：注释、Slurm指令、Linux指令。其中：

- Slurm指令以#SBATCH开头，必须放在Script开始的地方，注意，*在所有的lurm指令都结束前的任何行都不可以有任何Linux指令*。
- 注释以#开头，所以Slurm指令是一种特殊的注释，Linux会去忽视，但是Slurm会去读取。
- Linux指令与正常的sh文件相同。

## （二） 任务管理参数

超算任务与个人计算机或工作站不同，任务调度需要考虑多用户的请求及资源分配。因此，提交用户任务时需要说明

- 任务类型，或在哪个任务队列中排队。例如使用GPU就需要在 x86_64_GPU 队列，而无需GPU时可用 x86_64 队列。
- CPU核数
- GPU卡数
- 在常见的Slurm管理器中，一般允许提交对内存的需求以及时长需求，但是高性能计算公共平台（珠海校区）似乎对此没有限制。时长需求的缺乏导致经常可以看到僵尸进程。

更详细的信息请参考[Slurm_job_submit_single.sh](./Slurm_job_submit_single.sh)、[Slurm_job_submit.sh](Slurm_job_submit.sh)以及 <https://slurm.schedmd.com/>. 

## （三） 服务器端必要指令

### 1. 联网

由于服务器默认不连校园网及外网，为便于配置服务器工作环境或使用git，需要将跳板机设置为HTTP和HTTPS的代理。跳板机的内网IP为192.168.10.22，指令为：

``` bash
export http_proxy=http://192.168.10.22:3128
export https_proxy=http://192.168.10.22:3128
```

### 2. 激活模块

为兼容不同用户对不同版本软件的需求，当用户登录服务器后，环境是简单干净、没有载入软件包的。若需要使用Python虚拟环境，需要手动载入Anaconda。*注意，建议任何情况下，只要使用Python就使用虚拟环境*。

``` bash
module load Anaconda/mini3-23.1.0
```

module是由 [Environment Modules](https://modules.sourceforge.net/) 软件包提供的。Anaconda/mini3-23.1.0 貌似是目前（2025-02-01）服务器中唯一的Python虚拟环境管理软件。用户可以使用module avail 来查看所有可用模块。

如<https://hpc.pku.edu.cn/_book/guide/soft/module.html>所示，更多的指令包括：

``` bash
module help       # 显示帮助信息
module avail      # 显示已经安装的软件环境
module load       # 导入相应的软件环境
module unload     # 删除相应的软件环境
module list       # 列出已经导入的软件环境
module purge      # 清除所有已经导入的软件环境
module switch [mod1] mod2 # 删除mod1并导入mod2
```

### 3. Python虚拟环境

在载入Anaconda/mini3-23.1.0后，用户可以正常使用[Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)命令来配置Python虚拟环境。具体可参考 <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>。

配置过程可以使用VSCode的Terminal进行。在VSCode连接集群服务器后，Terminal中的指令是直接执行在服务器上的。

在配置完成后，我们可以在Script中通过如下指令在执行任务前启动虚拟环境。

``` bash
conda activate your_virtual_env_name
```

然而，因为某种配置的原因，服务器无法自动初始化conda，所以，我们需要在Script中加入如下指令启用conda：

``` bash
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
```
然后就可以正常使用conda activate了。

## （四）任务类型相关配置

### 1. 单任务的授权与提交

在Script中，若只需简单地提交单个任务，只需要赋予执行权限，并执行对应代码即可。

``` bash
chmod +x ./python_script_to_sub.py
python ./python_script_to_sub.py
```

然而，由于Python输出Buffer会抑制及时地将Python的打印输出存到文件或Terminal中。为及时地看到输出，可以更改PYTHONUNBUFFERED的参数为1，以关闭Buffer：

``` bash
export PYTHONUNBUFFERED=1
```

更多信息可参考 <https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED> 和 <https://docs.python.org/3/using/cmdline.html#cmdoption-u>。

提交单个任务的例子请参考[Slurm_job_submit_single.sh](./Slurm_job_submit_single.sh)。

### 2 Job array

对于需要执行大量相似独立任务的情况，Job array是一种很好的提交和管理方式。与提交单个任务的的Script相比，包含Job array信息的Script会为各子Task提供对应的 Task ID，以及整体任务的 Job ID，分别对应 SLURM_ARRAY_TASK_ID 和 SLURM_ARRAY_JOB_ID。根据<https://slurm.schedmd.com/job_array.html> 更多的环境变量如下：

> Job arrays will have additional environment variables set.
>
> -   SLURM_ARRAY_JOB_ID will be set to the first job ID of the array.
> -   SLURM_ARRAY_TASK_ID will be set to the job array index value.
> -   SLURM_ARRAY_TASK_COUNT will be set to the number of tasks in the job array.
> -   SLURM_ARRAY_TASK_MAX will be set to the highest job array index value.
> -   SLURM_ARRAY_TASK_MIN will be set to the lowest job array index value.

> - SLURM_ARRAY_JOB_ID 将被设置为作业数组的第一个作业 ID。
> - SLURM_ARRAY_TASK_ID 将被设置为作业数组的索引值。
> - SLURM_ARRAY_TASK_COUNT 将被设置为作业数组中的任务数量。
> - SLURM_ARRAY_TASK_MAX 将被设置为作业数组的最高索引值。
> - SLURM_ARRAY_TASK_MIN 将被设置为作业数组的最低索引值。

通过将SLURM_ARRAY_TASK_ID 和 SLURM_ARRAY_JOB_ID 传入被提交的程序，可以用于区分不同的子任务或将结果存储到不同的位置。

Job array由 #SBATCH --array 这一Slurm指令触发。例如，若想执行第1到第32号Task，则在Script开头加入如下指令：

``` bash
#SBATCH --array=1-32
```

### 3. 输出文件

与在Terminal中直接执行一个任务不同，通过Slurm提交的工作并没有一个直接允许用户观察的窗口，去直接实时查看打印输出与报错。因此，Slurm存在一个将这类输出转存到文件的方法。通过在Slurm指令中设置 --output 文件目录以及 --error 文件目录，可以将 stdout 与 stderr 流转录到对应文件中。若$USER 代表用户名，在单任务Script中，建议将地址设置为：

``` bash
#SBATCH --output=/share/home/$USER/logs/slurm_outputs/slurm_outputs_%j.log
#SBATCH --error=/share/home/$USER/logs/slurm_errors/slurm_errors_%j.log
```

其中，%j 会被 Slurm 自动替换为 Job ID.

在 Job Array 任务中，建议将地址设置为：

``` bash
#SBATCH --output=/share/home/$USER/logs/slurm_outputs/slurm_outputs_%A_%a.log
#SBATCH --error=/share/home/$USER/logs/slurm_errors/slurm_errors_%A_%a.log
```

其中，%A 和 %a 会本别被Slurm 自动替换为 Job ID 和 Task ID。

通过使用VSCode直接点击打开对应文件，可以以近似实时的方式查看输入。在Terminal中也可打开并查看对应文件。

### 4. Job array的推荐使用方法

**原始代码根据Task ID修改自身行为。** 在此方法中，Task ID作为关键参数传递给原始可执行代码，原始可执行代码据此切换行为。有点是不需要生成太多的Script，缺点是需要额外写原始代码管理不同Task的参数。

**提前生成不同的任务Script，并根据Task ID调用。** 为了减小修改原始代码的工作量，保留兼容性，可以将不同Task所需的参数的排列组合置于一个文件中，并另写一个自动生成Script的代码，用于生成不同任务的Script。 在本文中，建议采用此方法，灵活性最高。更具体地，以Python为例：

1. 在待提交执行的主程序 [python_script_to_sub.py](./python_script_to_sub.py) 中配置argparse，以接受参数输入。
2. 将需提交的参数名、参数值组合依次排列在CSV表格[HyperParamsYourExperimentName.csv](./HyperParamsYourExperimentName.csv)中，每个Task ID对应一行。
3. 使用[batch_script_generator.py](./batch_script_generator.py) 生成子任务Script。
4. 使用 sbatch指令提交[Slurm_job_submit.sh](./Slurm_job_submit.sh) 文件。

其中，[batch_script_generator.py](./batch_script_generator.py) 中 experiment_name 与 StartStr 变量要按照需求修改。[Slurm_job_submit.sh](./Slurm_job_submit.sh)中 #SBATCH --array 后的Task ID范围要按照需求修改。

# 四、任务提交与监测

##  （一） 任务提交

任务提交通常使用sbatch执行。

> - **sbatch** is used to submit a job script for later execution. The script will typically contain one or more srun commands to launch parallel tasks.
> - **sbatch** 用于提交作业脚本以供稍后执行。该脚本通常包含一个或多个 srun 命令来启动并行任务。

提交任务前，需检查[Slurm_job_submit.sh](./Slurm_job_submit.sh) 中调用的子任务Script路径是否是从工作目录开始的。确认是后，cd到工作目录下，使用如下指令提交Job array任务：

``` bash
sbatch Slurm_job_submit.sh
```

或者使用如下指令提交单个任务：

``` bash
sbatch Slurm_job_submit_single.sh
```

建议在提交Job array任务之前先用[Slurm_job_submit_single.sh](./Slurm_job_submit_single.sh)测试单个任务是否正常工作。

## （二） 任务状态监测

### 1. 主要监测指令

在工作开启后，要关注执行过程是否正常。除查看输出、报错文件外，还可以通过Slurm指令关注提交的任务是否被执行等状态。

如在https://slurm.schedmd.com/quickstart.html所述：

> - **sacct** is used to report job or job step accounting information about active or completed jobs.
> - **scancel** is used to cancel a pending or running job or job step. It can also be used to send an arbitrary signal to all processes associated with a running job or job step.
> - **scontrol** is the administrative tool used to view and/or modify Slurm state. Note that many scontrol commands can only be executed as user root.
> - **sinfo** reports the state of partitions and nodes managed by Slurm. It has a wide variety of filtering, sorting, and formatting options.
> - **sprio** is used to display a detailed view of the components affecting a job's priority.
> - **squeue** reports the state of jobs or job steps. It has a wide variety of filtering, sorting, and formatting options. By default, it reports the running jobs in priority order and then the pending jobs in priority order.

> - **sacct** 用于报告活动或已完成作业的作业或作业步骤的会计信息。
> - **scancel** 用于取消挂起或正在运行的作业或作业步骤。它还可以用于向与正在运行的作业或作业步骤相关的所有进程发送任意信号。
> - **scontrol** 是用于查看和/或修改 Slurm 状态的管理工具。请注意，许多 scontrol 命令只能由 root 用户执行。
> - **sinfo** 报告由 Slurm 管理的分区和节点的状态。它具有多种过滤、排序和格式化选项。
> - **sprio** 用于显示影响作业优先级的组件的详细视图。
> - **squeue** 报告作业或作业步骤的状态。它具有多种过滤、排序和格式化选项。默认情况下，它按优先级顺序报告正在运行的作业，然后按优先级顺序报告挂起的作业。

其中，**squeue** 与 **scancel** 最为常用。

### 2. 监测输出文件

通过配置 #SBATCH --output 和 #SBATCH --error，文件的打印输出和报错输出是可以被准实时监测的。根据Script中配置的路径，打开对应文件，可查看近期输出。其中，报错文件也可以包括Slurm在执行过程中的一些报错。

### 3. 监测内存占用

该集群似乎未配置内存占用监测，一个粗糙的替代可以是加在Script中的如下代码：

``` bash
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
``` 

该段Script可以把整个节点的内存占用情况存在 ~/logs/slurm_outputs/slurm_memory_$SLURM_JOB_ID.log 中，以便准实时查看。

***

## License

This project is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)**.  
For more details, see the [LICENSE](LICENSE) file or visit [https://creativecommons.org/licenses/by-nc-sa/4.0/](https://creativecommons.org/licenses/by-nc-sa/4.0/).

Copyright (c) 2025 Tianqi Wei

本作品采用 [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/) 进行许可。
您可以自由地共享、复制、修改和创作衍生作品，但必须注明原作者，且不得用于商业用途。基于本作品创作的衍生作品必须以相同的许可证发布。
更多信息请参考<https://creativecommons.org/licenses/by-nc-sa/4.0/>