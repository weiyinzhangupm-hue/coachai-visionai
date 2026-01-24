"""
姿态检测模块
使用MediaPipe进行人体关键点检测
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Tuple, List
from config import (
    MP_MODEL_COMPLEXITY,
    MP_MIN_DETECTION_CONFIDENCE,
    MP_MIN_TRACKING_CONFIDENCE,
    MP_SMOOTH_LANDMARKS,
    MP_ENABLE_SEGMENTATION,
    UI_CONFIG
)


class PoseDetector:
    """人体姿态检测器类"""
    
    def __init__(self):
        """初始化MediaPipe Pose"""
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # 初始化Pose检测器
        self.pose = self.mp_pose.Pose(
            model_complexity=MP_MODEL_COMPLEXITY,
            min_detection_confidence=MP_MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MP_MIN_TRACKING_CONFIDENCE,
            smooth_landmarks=MP_SMOOTH_LANDMARKS,
            enable_segmentation=MP_ENABLE_SEGMENTATION
        )
        
        self.results = None
        
    def detect(self, frame: np.ndarray) -> Optional[List]:
        """
        检测图像中的人体关键点
        
        Args:
            frame: BGR格式的输入图像
            
        Returns:
            检测到的关键点列表，每个关键点包含 (x, y, z, visibility)
            如果未检测到则返回 None
        """
        # 转换BGR到RGB（MediaPipe需要RGB格式）
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 处理图像
        image_rgb.flags.writeable = False  # 提高性能
        self.results = self.pose.process(image_rgb)
        image_rgb.flags.writeable = True
        
        # 检查是否检测到姿态
        if self.results.pose_landmarks:
            landmarks = []
            for landmark in self.results.pose_landmarks.landmark:
                landmarks.append({
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z,
                    'visibility': landmark.visibility
                })
            return landmarks
        
        return None
    
    def draw_landmarks(self, frame: np.ndarray, custom_color: bool = True) -> np.ndarray:
        """
        在图像上绘制检测到的骨架
        
        Args:
            frame: 输入图像
            custom_color: 是否使用自定义颜色
            
        Returns:
            绘制了骨架的图像
        """
        if self.results and self.results.pose_landmarks:
            if custom_color:
                # 使用自定义绘制样式
                self.mp_drawing.draw_landmarks(
                    frame,
                    self.results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.mp_drawing.DrawingSpec(
                        color=UI_CONFIG['skeleton_color'],
                        thickness=2,
                        circle_radius=2
                    ),
                    connection_drawing_spec=self.mp_drawing.DrawingSpec(
                        color=UI_CONFIG['skeleton_color'],
                        thickness=2
                    )
                )
            else:
                # 使用默认样式
                self.mp_drawing.draw_landmarks(
                    frame,
                    self.results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
                )
        
        return frame
    
    def get_landmark_coords(self, landmarks: List, index: int, frame_shape: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        获取指定关键点的像素坐标
        
        Args:
            landmarks: 关键点列表
            index: 关键点索引
            frame_shape: 图像形状 (height, width)
            
        Returns:
            (x, y) 像素坐标，如果不可见则返回 None
        """
        if landmarks is None or index >= len(landmarks):
            return None
        
        landmark = landmarks[index]
        if landmark['visibility'] < 0.5:  # 可见性阈值
            return None
        
        height, width = frame_shape
        x = int(landmark['x'] * width)
        y = int(landmark['y'] * height)
        
        return (x, y)
    
    def is_person_detected(self) -> bool:
        """检查是否检测到人体"""
        return self.results is not None and self.results.pose_landmarks is not None
    
    def close(self):
        """释放资源"""
        self.pose.close()
    
    def __del__(self):
        """析构函数"""
        self.close()

