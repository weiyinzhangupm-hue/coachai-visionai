"""
动作追踪模块
追踪运动的重复次数和状态
"""

import time
import numpy as np
from typing import Dict, List, Optional
from collections import deque
from config import ExerciseType, SQUAT_THRESHOLDS, PUSHUP_THRESHOLDS, MOTION_COUNTER_CONFIG


class MotionTracker:
    """动作追踪器类"""
    
    def __init__(self, exercise_type: ExerciseType):
        """
        初始化动作追踪器
        
        Args:
            exercise_type: 运动类型（深蹲或俯卧撑）
        """
        self.exercise_type = exercise_type
        self.rep_count = 0
        self.state = "UP"  # 状态：UP（上）或 DOWN（下）
        self.state_frame_count = 0  # 当前状态持续帧数
        
        # 历史数据
        self.angle_history = deque(maxlen=MOTION_COUNTER_CONFIG['state_change_threshold'])
        self.timestamp_history = []
        self.rep_timestamps = []  # 每次完成动作的时间戳
        
        # 单次动作数据
        self.current_rep_start_time = None
        self.current_rep_angles = []
        
        # 统计信息
        self.total_duration = 0
        self.rep_durations = []
        
    def update(self, angles: Dict[str, float]) -> bool:
        """
        更新追踪器状态
        
        Args:
            angles: 当前帧的角度字典
            
        Returns:
            如果完成了一次完整动作返回 True，否则返回 False
        """
        current_time = time.time()
        rep_completed = False
        
        # 根据运动类型选择关键角度
        if self.exercise_type == ExerciseType.SQUAT:
            key_angle = angles.get('knee_avg', 180)
            down_threshold = SQUAT_THRESHOLDS['knee_angle_down']
            up_threshold = SQUAT_THRESHOLDS['knee_angle_up']
        elif self.exercise_type == ExerciseType.PUSHUP:
            key_angle = angles.get('elbow_avg', 180)
            down_threshold = PUSHUP_THRESHOLDS['elbow_angle_down']
            up_threshold = PUSHUP_THRESHOLDS['elbow_angle_up']
        else:
            return False
        
        # 添加到历史记录
        self.angle_history.append(key_angle)
        
        # 状态机逻辑
        if self.state == "UP":
            # 检查是否进入DOWN状态
            if key_angle < down_threshold:
                self.state_frame_count += 1
                if self.state_frame_count >= MOTION_COUNTER_CONFIG['state_change_threshold']:
                    self.state = "DOWN"
                    self.state_frame_count = 0
                    self.current_rep_start_time = current_time
                    self.current_rep_angles = [key_angle]
            else:
                self.state_frame_count = 0
                
        elif self.state == "DOWN":
            # 记录下降过程的角度
            self.current_rep_angles.append(key_angle)
            
            # 检查是否返回UP状态
            if key_angle > up_threshold:
                self.state_frame_count += 1
                if self.state_frame_count >= MOTION_COUNTER_CONFIG['state_change_threshold']:
                    # 完成一次完整动作
                    rep_duration = current_time - self.current_rep_start_time
                    
                    # 验证动作时长是否合理
                    if (MOTION_COUNTER_CONFIG['min_rep_duration'] <= rep_duration <= 
                        MOTION_COUNTER_CONFIG['max_rep_duration']):
                        self.rep_count += 1
                        self.rep_timestamps.append(current_time)
                        self.rep_durations.append(rep_duration)
                        rep_completed = True
                    
                    # 重置状态
                    self.state = "UP"
                    self.state_frame_count = 0
                    self.current_rep_angles = []
            else:
                self.state_frame_count = 0
        
        return rep_completed
    
    def get_current_state(self) -> str:
        """获取当前状态"""
        return self.state
    
    def get_rep_count(self) -> int:
        """获取重复次数"""
        return self.rep_count
    
    def get_motion_features(self) -> Dict:
        """
        提取运动特征（用于机器学习）
        
        Returns:
            包含运动特征的字典
        """
        features = {
            'rep_count': self.rep_count,
            'avg_duration': 0.0,
            'std_duration': 0.0,
            'avg_speed': 0.0,
            'min_angle': 0.0,
            'max_angle': 0.0,
            'angle_range': 0.0,
        }
        
        # 计算平均和标准差
        if len(self.rep_durations) > 0:
            features['avg_duration'] = np.mean(self.rep_durations)
            features['std_duration'] = np.std(self.rep_durations)
            features['avg_speed'] = 1.0 / features['avg_duration']  # 次/秒
        
        # 计算角度特征
        if len(self.current_rep_angles) > 0:
            features['min_angle'] = np.min(self.current_rep_angles)
            features['max_angle'] = np.max(self.current_rep_angles)
            features['angle_range'] = features['max_angle'] - features['min_angle']
        
        return features
    
    def get_last_rep_duration(self) -> Optional[float]:
        """获取最近一次动作的时长"""
        if len(self.rep_durations) > 0:
            return self.rep_durations[-1]
        return None
    
    def get_average_speed(self) -> float:
        """
        获取平均速度（次/秒）
        
        Returns:
            平均速度
        """
        if len(self.rep_durations) > 0:
            avg_duration = np.mean(self.rep_durations)
            return 1.0 / avg_duration
        return 0.0
    
    def get_speed_trend(self) -> str:
        """
        获取速度趋势（用于疲劳检测）
        
        Returns:
            'increasing', 'stable', 'decreasing'
        """
        if len(self.rep_durations) < 3:
            return 'stable'
        
        # 比较最近3次和之前3次的平均时长
        recent = np.mean(self.rep_durations[-3:])
        previous = np.mean(self.rep_durations[-6:-3]) if len(self.rep_durations) >= 6 else recent
        
        if recent > previous * 1.2:
            return 'decreasing'  # 速度变慢
        elif recent < previous * 0.8:
            return 'increasing'  # 速度变快
        else:
            return 'stable'
    
    def reset(self):
        """重置计数器"""
        self.rep_count = 0
        self.state = "UP"
        self.state_frame_count = 0
        self.angle_history.clear()
        self.timestamp_history.clear()
        self.rep_timestamps.clear()
        self.rep_durations.clear()
        self.current_rep_angles = []
        self.current_rep_start_time = None

