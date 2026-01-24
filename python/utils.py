"""
工具函数模块
提供通用的辅助函数
"""

import os
import logging
from datetime import datetime
from config import LOG_CONFIG


def setup_logger(name: str = "VirtualTrainer") -> logging.Logger:
    """
    设置日志记录器
    
    Args:
        name: 日志记录器名称
        
    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_CONFIG['level']))
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(LOG_CONFIG['format'])
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器
    if LOG_CONFIG['save_to_file']:
        os.makedirs(LOG_CONFIG['log_dir'], exist_ok=True)
        log_file = os.path.join(
            LOG_CONFIG['log_dir'],
            f"trainer_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def ensure_dir(directory: str):
    """
    确保目录存在，不存在则创建
    
    Args:
        directory: 目录路径
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"创建目录: {directory}")


def format_duration(seconds: float) -> str:
    """
    格式化时长显示
    
    Args:
        seconds: 秒数
        
    Returns:
        格式化的字符串（如 "1.5s"）
    """
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    else:
        return f"{seconds:.1f}s"


def calculate_fps(frame_times: list) -> float:
    """
    计算帧率
    
    Args:
        frame_times: 帧时间戳列表
        
    Returns:
        平均帧率
    """
    if len(frame_times) < 2:
        return 0.0
    
    time_diffs = [frame_times[i] - frame_times[i-1] 
                  for i in range(1, len(frame_times))]
    avg_time = sum(time_diffs) / len(time_diffs)
    
    return 1.0 / avg_time if avg_time > 0 else 0.0


def moving_average(data: list, window_size: int = 5) -> list:
    """
    计算移动平均
    
    Args:
        data: 数据列表
        window_size: 窗口大小
        
    Returns:
        平滑后的数据
    """
    if len(data) < window_size:
        return data
    
    result = []
    for i in range(len(data)):
        start = max(0, i - window_size + 1)
        end = i + 1
        result.append(sum(data[start:end]) / (end - start))
    
    return result


def print_system_info():
    """打印系统信息"""
    import sys
    import cv2
    import mediapipe as mp
    
    print("=" * 60)
    print("系统信息")
    print("=" * 60)
    print(f"Python版本: {sys.version}")
    print(f"OpenCV版本: {cv2.__version__}")
    print(f"MediaPipe版本: {mp.__version__}")
    print("=" * 60)


def check_dependencies() -> bool:
    """
    检查所有依赖是否安装
    
    Returns:
        True如果所有依赖都可用
    """
    required_modules = [
        'cv2',
        'mediapipe',
        'numpy',
        'pandas',
        'sklearn',
        'requests',
        'flask'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"缺少以下依赖: {', '.join(missing)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    return True


def get_project_root() -> str:
    """
    获取项目根目录
    
    Returns:
        项目根目录路径
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(current_dir)

