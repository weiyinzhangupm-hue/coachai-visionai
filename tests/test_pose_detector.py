"""
测试姿态检测模块
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import cv2
import numpy as np
from python.pose_detector import PoseDetector
from python.config import LandmarkIndex


def test_pose_detector_initialization():
    """测试姿态检测器初始化"""
    print("测试: 姿态检测器初始化...")
    try:
        detector = PoseDetector()
        assert detector is not None
        assert detector.pose is not None
        print("✓ 初始化成功")
        return True
    except Exception as e:
        print(f"✗ 初始化失败: {e}")
        return False


def test_pose_detection_with_image():
    """测试图像姿态检测"""
    print("\n测试: 图像姿态检测...")
    try:
        detector = PoseDetector()
        
        # 创建测试图像（黑色背景）
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # 检测（应该返回None因为没有人）
        landmarks = detector.detect(test_image)
        
        print("✓ 检测方法可以运行")
        print(f"  检测结果: {'无人体' if landmarks is None else '检测到人体'}")
        
        detector.close()
        return True
    except Exception as e:
        print(f"✗ 检测失败: {e}")
        return False


def test_landmark_count():
    """测试关键点数量"""
    print("\n测试: 关键点数量...")
    try:
        # MediaPipe Pose应该有33个关键点
        expected_count = 33
        
        # 通过LandmarkIndex验证
        landmark_indices = [
            getattr(LandmarkIndex, attr) 
            for attr in dir(LandmarkIndex) 
            if not attr.startswith('_')
        ]
        
        print(f"  定义的关键点索引数: {len(landmark_indices)}")
        print(f"  预期关键点数: {expected_count}")
        
        if max(landmark_indices) < expected_count:
            print("✓ 关键点索引在有效范围内")
            return True
        else:
            print("✗ 关键点索引超出范围")
            return False
            
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False


def test_camera_access():
    """测试摄像头访问"""
    print("\n测试: 摄像头访问...")
    try:
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("✗ 无法打开摄像头")
            print("  提示: 请检查摄像头权限和连接")
            return False
        
        # 尝试读取一帧
        ret, frame = cap.read()
        cap.release()
        
        if ret and frame is not None:
            print("✓ 摄像头可正常访问")
            print(f"  分辨率: {frame.shape[1]}x{frame.shape[0]}")
            return True
        else:
            print("✗ 无法读取摄像头帧")
            return False
            
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("姿态检测模块测试套件")
    print("=" * 60)
    
    tests = [
        test_pose_detector_initialization,
        test_pose_detection_with_image,
        test_landmark_count,
        test_camera_access
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

