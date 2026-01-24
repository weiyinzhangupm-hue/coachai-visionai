"""
测试特征提取模块
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
from python.feature_extractor import FeatureExtractor
from python.config import LandmarkIndex


def create_mock_landmarks():
    """创建模拟的关键点数据"""
    landmarks = []
    for i in range(33):
        landmarks.append({
            'x': np.random.rand(),
            'y': np.random.rand(),
            'z': np.random.rand(),
            'visibility': 0.9
        })
    return landmarks


def create_mock_angles():
    """创建模拟的角度数据"""
    return {
        'knee_avg': 120.0,
        'hip_avg': 90.0,
        'elbow_avg': 160.0,
        'shoulder_avg': 85.0,
        'trunk_tilt': 10.0
    }


def test_feature_extractor_initialization():
    """测试特征提取器初始化"""
    print("测试: 特征提取器初始化...")
    try:
        extractor = FeatureExtractor()
        assert extractor is not None
        print("✓ 初始化成功")
        return True
    except Exception as e:
        print(f"✗ 初始化失败: {e}")
        return False


def test_frame_feature_extraction():
    """测试单帧特征提取"""
    print("\n测试: 单帧特征提取...")
    try:
        extractor = FeatureExtractor()
        landmarks = create_mock_landmarks()
        angles = create_mock_angles()
        
        features = extractor.extract_frame_features(landmarks, angles)
        
        assert isinstance(features, dict)
        assert len(features) > 0
        
        print("✓ 特征提取成功")
        print(f"  提取的特征数: {len(features)}")
        print(f"  特征示例: {list(features.keys())[:5]}")
        return True
    except Exception as e:
        print(f"✗ 特征提取失败: {e}")
        return False


def test_temporal_feature_extraction():
    """测试时序特征提取"""
    print("\n测试: 时序特征提取...")
    try:
        extractor = FeatureExtractor()
        
        # 创建历史帧数据
        history = []
        for _ in range(10):
            landmarks = create_mock_landmarks()
            angles = create_mock_angles()
            features = extractor.extract_frame_features(landmarks, angles)
            history.append(features)
        
        temporal_features = extractor.extract_temporal_features(history)
        
        assert isinstance(temporal_features, dict)
        
        print("✓ 时序特征提取成功")
        print(f"  提取的时序特征数: {len(temporal_features)}")
        return True
    except Exception as e:
        print(f"✗ 时序特征提取失败: {e}")
        return False


def test_feature_normalization():
    """测试特征归一化"""
    print("\n测试: 特征归一化...")
    try:
        extractor = FeatureExtractor()
        landmarks = create_mock_landmarks()
        angles = create_mock_angles()
        
        features = extractor.extract_frame_features(landmarks, angles)
        normalized = extractor.normalize_features(features, fit=True)
        
        assert isinstance(normalized, np.ndarray)
        assert len(normalized) > 0
        
        print("✓ 特征归一化成功")
        print(f"  归一化后维度: {normalized.shape}")
        return True
    except Exception as e:
        print(f"✗ 特征归一化失败: {e}")
        return False


def test_feature_vector_creation():
    """测试完整特征向量创建"""
    print("\n测试: 完整特征向量创建...")
    try:
        extractor = FeatureExtractor()
        landmarks = create_mock_landmarks()
        angles = create_mock_angles()
        
        # 创建历史数据
        history = []
        for _ in range(5):
            lm = create_mock_landmarks()
            ag = create_mock_angles()
            feat = extractor.extract_frame_features(lm, ag)
            history.append(feat)
        
        feature_vector = extractor.create_feature_vector(landmarks, angles, history)
        
        assert isinstance(feature_vector, dict)
        assert len(feature_vector) > 0
        
        print("✓ 特征向量创建成功")
        print(f"  总特征数: {len(feature_vector)}")
        return True
    except Exception as e:
        print(f"✗ 特征向量创建失败: {e}")
        return False


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("特征提取模块测试套件")
    print("=" * 60)
    
    tests = [
        test_feature_extractor_initialization,
        test_frame_feature_extraction,
        test_temporal_feature_extraction,
        test_feature_normalization,
        test_feature_vector_creation
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"测试结果: {sum(results)}/{len(results)} 通过")
    print("=" * 60)
    
    return all(results)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

