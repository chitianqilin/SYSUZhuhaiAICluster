
import argparse

import numpy as np


def str2bool(v):
    """
    将字符串转换为布尔值。
    'y', 'yes', 't', 'true', 'on' 和 '1' 会被转换为 True；
    'n', 'no', 'f', 'false', 'off' 和 '0' 会被转换为 False。
    对于不在这些值中的输入，将引发 argparse.ArgumentTypeError。
    """
    if v.lower() in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif v.lower() in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
 
# 定义一个函数，用于将字符串转换为numpy数据类型
def str_to_dtype(dtype_str):
    try:
        # 使用getattr从numpy获取对应的数据类型
        dtype = getattr(np, dtype_str)
    except AttributeError:
        # 如果找不到对应的数据类型，则抛出错误
        raise argparse.ArgumentTypeError(f"Unknown dtype: {dtype_str}")
    return dtype

def parse_arguments():
    parser = argparse.ArgumentParser(description='Initialize parameters for the FlyOrien experiment.')
    
    # Experiment name
    parser.add_argument('--experiment', type=str, default='FlyOrien', help='Name of the experiment.')
    
    # Input and label parameters
    parser.add_argument('--num_input_points', type=int, default=30, help='Number of input points.')
    
    # Random seed
    parser.add_argument('--seed', type=int, default=1, help='Random seed for reproducibility.')
    
    # Neuron parameters
    parser.add_argument('--num_PNs', type=int, default=20, help='Number of Projection Neurons (PNs).')
    parser.add_argument('--num_KCs', type=int, default=1000, help='Number of Kenyon Cells (KCs).')
    parser.add_argument('--num_MBONs', type=int, default=10, help='Number of Mushroom Body Output Neurons (MBONs).')
    
    # Sampling and sparsity
    parser.add_argument('--PN_sampling_ratio', type=float, default=0.15, help='PN sampling ratio.')
    parser.add_argument('--KC_sparseness', type=float, default=0.05, help='KC sparseness.')
    
    # Firing and input parameters
    parser.add_argument('--num_inputs_once', type=int, default=10, help='Number of inputs processed once.')
    
    # Binary and model options
    parser.add_argument('--using_binary_KC', type=str2bool, default=False, help='Use binary KCs (accept "True"/"False").')
    parser.add_argument('--using_binary_weight', type=str2bool,  default=False, help='Use binary weights (accept "True"/"False").')
    parser.add_argument('--using_DevFly', type=str2bool, default=False, help='Use DevFly model (accept "True"/"False").')
    
    # Normalization and activation
    parser.add_argument('--normalising_KC', type=str2bool, default=True, help='Normalize KCs (accept "True"/"False").')
    parser.add_argument('--disable_over_activating_KC', type=str2bool, default=False, help='Disable over-activating KCs (accept "True"/"False").')
    parser.add_argument('--over_activating_KC_threshold_rate', type=float, default=1, help='Threshold for over-activating KCs.')
    
    # Learning rate
    parser.add_argument('--initial_learning_rate', type=float, default=0.75, help='Initial learning rate.')
    parser.add_argument('--lr_decay_factor', type=float, default=1e-5, help='Learning rate decay factor.')
    
    # Data processing
    parser.add_argument('--sorted_data', type=str2bool, default=False, help='Sort data before processing (accept "True"/"False").')
    parser.add_argument('--if_center_data', type=str2bool, default=True, help='Center data before processing (accept "True"/"False").')
    
    # set datatype
    parser.add_argument('--dtype', type=str_to_dtype, default=np.float32,
                    help='Specify the numpy data type (default: np.float32).')

    # Parse the arguments
    args = parser.parse_args()
    
    return args

if __name__=="__main__":

    args = parse_arguments()
    print(args)