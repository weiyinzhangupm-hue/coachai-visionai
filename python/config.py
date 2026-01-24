"""
配置文件 - 虚拟健身教练系统
包含所有全局配置参数
"""

from enum import Enum

# ============== 摄像头设置 ==============
CAMERA_INDEX = 0  # 默认摄像头
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
CAMERA_FPS = 30

# ============== MediaPipe配置 ==============
# 模型复杂度: 0=Lite, 1=Full, 2=Heavy
MP_MODEL_COMPLEXITY = 1
MP_MIN_DETECTION_CONFIDENCE = 0.5  # 最小检测置信度
MP_MIN_TRACKING_CONFIDENCE = 0.5   # 最小追踪置信度
MP_SMOOTH_LANDMARKS = True          # 平滑关键点
MP_ENABLE_SEGMENTATION = False      # 是否启用分割（不需要）

# ============== MediaPipe关键点索引 ==============
# 根据MediaPipe Pose定义的33个关键点
class LandmarkIndex:
    # 面部
    NOSE = 0
    LEFT_EYE_INNER = 1
    LEFT_EYE = 2
    LEFT_EYE_OUTER = 3
    RIGHT_EYE_INNER = 4
    RIGHT_EYE = 5
    RIGHT_EYE_OUTER = 6
    LEFT_EAR = 7
    RIGHT_EAR = 8
    MOUTH_LEFT = 9
    MOUTH_RIGHT = 10
    
    # 上肢
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_WRIST = 15
    RIGHT_WRIST = 16
    
    # 手部
    LEFT_PINKY = 17
    RIGHT_PINKY = 18
    LEFT_INDEX = 19
    RIGHT_INDEX = 20
    LEFT_THUMB = 21
    RIGHT_THUMB = 22
    
    # 下肢
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28
    
    # 脚部
    LEFT_HEEL = 29
    RIGHT_HEEL = 30
    LEFT_FOOT_INDEX = 31
    RIGHT_FOOT_INDEX = 32

# ============== 运动类型定义 ==============
class ExerciseType(Enum):
    SQUAT = "squat"      # 深蹲
    PUSHUP = "pushup"    # 俯卧撑
    UNKNOWN = "unknown"  # 未知

# ============== 深蹲动作阈值 ==============
SQUAT_THRESHOLDS = {
    'knee_angle_down': 100,      # 膝盖角度小于此值认为处于下蹲状态
    'knee_angle_up': 160,        # 膝盖角度大于此值认为处于站立状态
    'hip_angle_min': 70,         # 髋关节最小角度（完全下蹲）
    'hip_angle_max': 170,        # 髋关节最大角度（站立）
    'back_angle_min': 45,        # 背部倾斜最小角度
    'back_angle_max': 90,        # 背部倾斜最大角度
}

# ============== 俯卧撑动作阈值 ==============
PUSHUP_THRESHOLDS = {
    'elbow_angle_down': 90,      # 肘关节角度小于此值认为处于下降状态
    'elbow_angle_up': 160,       # 肘关节角度大于此值认为处于撑起状态
    'shoulder_angle_min': 30,    # 肩关节最小角度
    'shoulder_angle_max': 100,   # 肩关节最大角度
    'body_angle_min': 160,       # 身体保持水平的最小角度
    'body_angle_max': 190,       # 身体保持水平的最大角度
}

# ============== 动作计数器设置 ==============
MOTION_COUNTER_CONFIG = {
    'min_rep_duration': 0.5,     # 最小单次动作时长（秒）
    'max_rep_duration': 10.0,    # 最大单次动作时长（秒）
    'state_change_threshold': 3, # 状态改变需要的连续帧数
}

# ============== 特征提取配置 ==============
FEATURE_CONFIG = {
    'history_length': 30,        # 保留历史帧数
    'normalization_method': 'minmax',  # 归一化方法: 'minmax' 或 'standard'
}

# ============== REST API配置 ==============
API_CONFIG = {
    'base_url': 'http://localhost:5000',
    'classify_endpoint': '/classify',
    'feedback_endpoint': '/feedback',
    'timeout': 5.0,              # 请求超时时间（秒）
}

# ============== UI配置 ==============
UI_CONFIG = {
    'window_name': 'Virtual Trainer',
    'font_scale': 0.7,
    'font_thickness': 2,
    'text_color': (0, 255, 0),   # 绿色 (BGR)
    'error_color': (0, 0, 255),  # 红色 (BGR)
    'skeleton_color': (245, 117, 66),  # 骨架颜色
    'angle_color': (255, 255, 0),      # 角度标注颜色
}

# ============== 日志配置 ==============
LOG_CONFIG = {
    'level': 'INFO',             # DEBUG, INFO, WARNING, ERROR
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'save_to_file': True,
    'log_dir': 'results/logs',
}

# ============== 数据采集配置 ==============
DATA_COLLECTION_CONFIG = {
    'save_video': True,
    'save_features': True,
    'video_format': 'mp4',
    'fps': 30,
}

