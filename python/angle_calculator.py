"""
角度计算模块
计算人体关节角度
"""

import numpy as np
import math
from typing import List, Optional, Dict
from config import LandmarkIndex


class AngleCalculator:
    """角度计算器类"""
    
    @staticmethod
    def calculate_angle(p1: Dict, p2: Dict, p3: Dict) -> float:
        """
        计算三个点形成的角度
        p2是顶点（关节点）
        
        Args:
            p1, p2, p3: 包含 'x', 'y', 'z' 的关键点字典
            
        Returns:
            角度值（度数，0-180）
        """
        # 提取坐标
        a = np.array([p1['x'], p1['y']])
        b = np.array([p2['x'], p2['y']])
        c = np.array([p3['x'], p3['y']])
        
        # 计算向量
        ba = a - b
        bc = c - b
        
        # 计算角度
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
        
        # 限制在[-1, 1]范围内，避免数值误差
        cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
        
        angle = np.arccos(cosine_angle)
        angle_degrees = np.degrees(angle)
        
        return angle_degrees
    
    @staticmethod
    def calculate_vertical_angle(p1: Dict, p2: Dict) -> float:
        """
        计算两点连线与垂直方向的夹角
        用于计算身体倾斜度
        
        Args:
            p1: 上方点
            p2: 下方点
            
        Returns:
            与垂直方向的夹角（度数）
        """
        dx = p2['x'] - p1['x']
        dy = p2['y'] - p1['y']
        
        # 计算与垂直方向的角度
        angle = abs(math.degrees(math.atan2(dx, dy)))
        
        return angle
    
    def get_squat_angles(self, landmarks: List) -> Dict[str, float]:
        """
        获取深蹲相关的所有角度
        
        Args:
            landmarks: 关键点列表
            
        Returns:
            包含各个角度的字典
        """
        if landmarks is None or len(landmarks) < 33:
            return {}
        
        angles = {}
        
        try:
            # 左膝关节角度（髋-膝-踝）
            left_knee_angle = self.calculate_angle(
                landmarks[LandmarkIndex.LEFT_HIP],
                landmarks[LandmarkIndex.LEFT_KNEE],
                landmarks[LandmarkIndex.LEFT_ANKLE]
            )
            angles['left_knee'] = left_knee_angle
            
            # 右膝关节角度
            right_knee_angle = self.calculate_angle(
                landmarks[LandmarkIndex.RIGHT_HIP],
                landmarks[LandmarkIndex.RIGHT_KNEE],
                landmarks[LandmarkIndex.RIGHT_ANKLE]
            )
            angles['right_knee'] = right_knee_angle
            
            # 平均膝关节角度
            angles['knee_avg'] = (left_knee_angle + right_knee_angle) / 2
            
            # 左髋关节角度（肩-髋-膝）
            left_hip_angle = self.calculate_angle(
                landmarks[LandmarkIndex.LEFT_SHOULDER],
                landmarks[LandmarkIndex.LEFT_HIP],
                landmarks[LandmarkIndex.LEFT_KNEE]
            )
            angles['left_hip'] = left_hip_angle
            
            # 右髋关节角度
            right_hip_angle = self.calculate_angle(
                landmarks[LandmarkIndex.RIGHT_SHOULDER],
                landmarks[LandmarkIndex.RIGHT_HIP],
                landmarks[LandmarkIndex.RIGHT_KNEE]
            )
            angles['right_hip'] = right_hip_angle
            
            # 平均髋关节角度
            angles['hip_avg'] = (left_hip_angle + right_hip_angle) / 2
            
            # 躯干倾斜角度（肩部中点到髋部中点）
            shoulder_mid = {
                'x': (landmarks[LandmarkIndex.LEFT_SHOULDER]['x'] + landmarks[LandmarkIndex.RIGHT_SHOULDER]['x']) / 2,
                'y': (landmarks[LandmarkIndex.LEFT_SHOULDER]['y'] + landmarks[LandmarkIndex.RIGHT_SHOULDER]['y']) / 2,
                'z': (landmarks[LandmarkIndex.LEFT_SHOULDER]['z'] + landmarks[LandmarkIndex.RIGHT_SHOULDER]['z']) / 2
            }
            hip_mid = {
                'x': (landmarks[LandmarkIndex.LEFT_HIP]['x'] + landmarks[LandmarkIndex.RIGHT_HIP]['x']) / 2,
                'y': (landmarks[LandmarkIndex.LEFT_HIP]['y'] + landmarks[LandmarkIndex.RIGHT_HIP]['y']) / 2,
                'z': (landmarks[LandmarkIndex.LEFT_HIP]['z'] + landmarks[LandmarkIndex.RIGHT_HIP]['z']) / 2
            }
            trunk_tilt = self.calculate_vertical_angle(shoulder_mid, hip_mid)
            angles['trunk_tilt'] = trunk_tilt
            
        except Exception as e:
            print(f"计算深蹲角度时出错: {e}")
        
        return angles
    
    def get_pushup_angles(self, landmarks: List) -> Dict[str, float]:
        """
        获取俯卧撑相关的所有角度
        
        Args:
            landmarks: 关键点列表
            
        Returns:
            包含各个角度的字典
        """
        if landmarks is None or len(landmarks) < 33:
            return {}
        
        angles = {}
        
        try:
            # 左肘关节角度（肩-肘-腕）
            left_elbow_angle = self.calculate_angle(
                landmarks[LandmarkIndex.LEFT_SHOULDER],
                landmarks[LandmarkIndex.LEFT_ELBOW],
                landmarks[LandmarkIndex.LEFT_WRIST]
            )
            angles['left_elbow'] = left_elbow_angle
            
            # 右肘关节角度
            right_elbow_angle = self.calculate_angle(
                landmarks[LandmarkIndex.RIGHT_SHOULDER],
                landmarks[LandmarkIndex.RIGHT_ELBOW],
                landmarks[LandmarkIndex.RIGHT_WRIST]
            )
            angles['right_elbow'] = right_elbow_angle
            
            # 平均肘关节角度
            angles['elbow_avg'] = (left_elbow_angle + right_elbow_angle) / 2
            
            # 左肩关节角度（髋-肩-肘）
            left_shoulder_angle = self.calculate_angle(
                landmarks[LandmarkIndex.LEFT_HIP],
                landmarks[LandmarkIndex.LEFT_SHOULDER],
                landmarks[LandmarkIndex.LEFT_ELBOW]
            )
            angles['left_shoulder'] = left_shoulder_angle
            
            # 右肩关节角度
            right_shoulder_angle = self.calculate_angle(
                landmarks[LandmarkIndex.RIGHT_HIP],
                landmarks[LandmarkIndex.RIGHT_SHOULDER],
                landmarks[LandmarkIndex.RIGHT_ELBOW]
            )
            angles['right_shoulder'] = right_shoulder_angle
            
            # 平均肩关节角度
            angles['shoulder_avg'] = (left_shoulder_angle + right_shoulder_angle) / 2
            
            # 身体水平度（肩-髋-踝的角度）
            left_body_angle = self.calculate_angle(
                landmarks[LandmarkIndex.LEFT_SHOULDER],
                landmarks[LandmarkIndex.LEFT_HIP],
                landmarks[LandmarkIndex.LEFT_ANKLE]
            )
            right_body_angle = self.calculate_angle(
                landmarks[LandmarkIndex.RIGHT_SHOULDER],
                landmarks[LandmarkIndex.RIGHT_HIP],
                landmarks[LandmarkIndex.RIGHT_ANKLE]
            )
            angles['body_angle'] = (left_body_angle + right_body_angle) / 2
            
        except Exception as e:
            print(f"计算俯卧撑角度时出错: {e}")
        
        return angles
    
    @staticmethod
    def draw_angle_on_frame(frame, point, angle_value, color=(255, 255, 0)):
        """
        在图像上绘制角度值
        
        Args:
            frame: 输入图像
            point: 标注位置 (x, y)
            angle_value: 角度值
            color: 文本颜色
        """
        if point is not None:
            text = f"{int(angle_value)}°"
            cv2.putText(
                frame,
                text,
                point,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2,
                cv2.LINE_AA
            )

