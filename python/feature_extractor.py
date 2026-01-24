"""
特征提取模块
从关键点和角度数据中提取机器学习特征
"""

import numpy as np
from typing import Dict, List, Optional
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from config import LandmarkIndex, FEATURE_CONFIG


class FeatureExtractor:
    """特征提取器类"""
    
    def __init__(self):
        """初始化特征提取器"""
        self.normalization_method = FEATURE_CONFIG['normalization_method']
        self.scaler = None
        self.feature_names = []
        
    def extract_frame_features(self, landmarks: List, angles: Dict[str, float]) -> Dict[str, float]:
        """
        提取单帧特征
        
        Args:
            landmarks: 关键点列表
            angles: 角度字典
            
        Returns:
            特征字典
        """
        features = {}
        
        # 1. 角度特征（直接使用计算好的角度）
        for angle_name, angle_value in angles.items():
            features[f'angle_{angle_name}'] = angle_value
        
        # 2. 几何特征 - 关键距离
        if landmarks and len(landmarks) >= 33:
            # 肩宽（归一化特征）
            shoulder_width = self._calculate_distance(
                landmarks[LandmarkIndex.LEFT_SHOULDER],
                landmarks[LandmarkIndex.RIGHT_SHOULDER]
            )
            features['shoulder_width'] = shoulder_width
            
            # 髋宽
            hip_width = self._calculate_distance(
                landmarks[LandmarkIndex.LEFT_HIP],
                landmarks[LandmarkIndex.RIGHT_HIP]
            )
            features['hip_width'] = hip_width
            
            # 躯干长度（肩膀中点到髋部中点）
            shoulder_mid = self._get_midpoint(
                landmarks[LandmarkIndex.LEFT_SHOULDER],
                landmarks[LandmarkIndex.RIGHT_SHOULDER]
            )
            hip_mid = self._get_midpoint(
                landmarks[LandmarkIndex.LEFT_HIP],
                landmarks[LandmarkIndex.RIGHT_HIP]
            )
            trunk_length = self._calculate_distance(shoulder_mid, hip_mid)
            features['trunk_length'] = trunk_length
            
            # 大腿长度（左侧）
            left_thigh_length = self._calculate_distance(
                landmarks[LandmarkIndex.LEFT_HIP],
                landmarks[LandmarkIndex.LEFT_KNEE]
            )
            features['left_thigh_length'] = left_thigh_length
            
            # 小腿长度（左侧）
            left_calf_length = self._calculate_distance(
                landmarks[LandmarkIndex.LEFT_KNEE],
                landmarks[LandmarkIndex.LEFT_ANKLE]
            )
            features['left_calf_length'] = left_calf_length
            
            # 上臂长度（左侧）
            left_upper_arm_length = self._calculate_distance(
                landmarks[LandmarkIndex.LEFT_SHOULDER],
                landmarks[LandmarkIndex.LEFT_ELBOW]
            )
            features['left_upper_arm_length'] = left_upper_arm_length
            
            # 前臂长度（左侧）
            left_forearm_length = self._calculate_distance(
                landmarks[LandmarkIndex.LEFT_ELBOW],
                landmarks[LandmarkIndex.LEFT_WRIST]
            )
            features['left_forearm_length'] = left_forearm_length
            
            # 3. 身体比例特征（归一化，消除身高差异）
            if trunk_length > 0:
                features['hip_shoulder_ratio'] = hip_width / shoulder_width if shoulder_width > 0 else 1.0
                features['thigh_trunk_ratio'] = left_thigh_length / trunk_length
                features['calf_trunk_ratio'] = left_calf_length / trunk_length
            
            # 4. 关键点可见性特征
            visibility_scores = [lm['visibility'] for lm in landmarks]
            features['avg_visibility'] = np.mean(visibility_scores)
            features['min_visibility'] = np.min(visibility_scores)
        
        return features
    
    def extract_temporal_features(self, history: List[Dict]) -> Dict[str, float]:
        """
        提取时序特征（从历史帧中）
        
        Args:
            history: 历史帧的特征列表
            
        Returns:
            时序特征字典
        """
        temporal_features = {}
        
        if len(history) < 2:
            return temporal_features
        
        # 提取关键角度的时间序列
        angle_names = ['knee_avg', 'hip_avg', 'elbow_avg', 'shoulder_avg']
        
        for angle_name in angle_names:
            angle_key = f'angle_{angle_name}'
            if angle_key in history[0]:
                angle_series = [frame.get(angle_key, 0) for frame in history]
                
                # 统计特征
                temporal_features[f'{angle_name}_mean'] = np.mean(angle_series)
                temporal_features[f'{angle_name}_std'] = np.std(angle_series)
                temporal_features[f'{angle_name}_min'] = np.min(angle_series)
                temporal_features[f'{angle_name}_max'] = np.max(angle_series)
                temporal_features[f'{angle_name}_range'] = np.max(angle_series) - np.min(angle_series)
                
                # 运动特征
                if len(angle_series) > 1:
                    # 速度（角度变化率）
                    velocities = np.diff(angle_series)
                    temporal_features[f'{angle_name}_velocity_mean'] = np.mean(np.abs(velocities))
                    temporal_features[f'{angle_name}_velocity_max'] = np.max(np.abs(velocities))
                    
                    # 加速度
                    if len(velocities) > 1:
                        accelerations = np.diff(velocities)
                        temporal_features[f'{angle_name}_acceleration_mean'] = np.mean(np.abs(accelerations))
                
                # 平滑度（标准差越小越平滑）
                temporal_features[f'{angle_name}_smoothness'] = 1.0 / (1.0 + temporal_features[f'{angle_name}_std'])
        
        return temporal_features
    
    def normalize_features(self, features: Dict[str, float], fit: bool = False) -> np.ndarray:
        """
        特征归一化
        
        Args:
            features: 特征字典
            fit: 是否拟合归一化器（训练时使用）
            
        Returns:
            归一化后的特征数组
        """
        # 转换为数组
        feature_values = np.array(list(features.values())).reshape(1, -1)
        
        # 保存特征名称
        if not self.feature_names:
            self.feature_names = list(features.keys())
        
        # 初始化或使用已有的归一化器
        if fit or self.scaler is None:
            if self.normalization_method == 'minmax':
                self.scaler = MinMaxScaler()
            else:
                self.scaler = StandardScaler()
            
            normalized = self.scaler.fit_transform(feature_values)
        else:
            normalized = self.scaler.transform(feature_values)
        
        return normalized.flatten()
    
    def create_feature_vector(self, landmarks: List, angles: Dict, history: List[Dict] = None) -> np.ndarray:
        """
        创建完整的特征向量
        
        Args:
            landmarks: 当前帧的关键点
            angles: 当前帧的角度
            history: 历史帧特征（可选）
            
        Returns:
            特征向量
        """
        # 提取单帧特征
        frame_features = self.extract_frame_features(landmarks, angles)
        
        # 如果有历史数据，提取时序特征
        if history and len(history) > 0:
            temporal_features = self.extract_temporal_features(history)
            frame_features.update(temporal_features)
        
        return frame_features
    
    @staticmethod
    def _calculate_distance(p1: Dict, p2: Dict) -> float:
        """计算两点之间的欧氏距离"""
        dx = p2['x'] - p1['x']
        dy = p2['y'] - p1['y']
        dz = p2['z'] - p1['z']
        return np.sqrt(dx**2 + dy**2 + dz**2)
    
    @staticmethod
    def _get_midpoint(p1: Dict, p2: Dict) -> Dict:
        """计算两点的中点"""
        return {
            'x': (p1['x'] + p2['x']) / 2,
            'y': (p1['y'] + p2['y']) / 2,
            'z': (p1['z'] + p2['z']) / 2,
            'visibility': min(p1['visibility'], p2['visibility'])
        }
    
    def get_feature_names(self) -> List[str]:
        """获取特征名称列表"""
        return self.feature_names
    
    def save_features_to_csv(self, features_list: List[Dict], labels: List, filepath: str):
        """
        保存特征到CSV文件
        
        Args:
            features_list: 特征字典列表
            labels: 标签列表
            filepath: 输出文件路径
        """
        import pandas as pd
        
        # 转换为DataFrame
        df = pd.DataFrame(features_list)
        df['label'] = labels
        
        # 保存
        df.to_csv(filepath, index=False)
        print(f"特征已保存到: {filepath}")

