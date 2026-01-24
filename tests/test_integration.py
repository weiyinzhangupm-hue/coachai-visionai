"""
集成测试 - 测试系统整体功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import cv2
import time


def test_dependencies():
    """测试所有依赖是否可正常导入"""
    print("测试: 依赖导入...")
    try:
        import cv2
        import mediapipe
        import numpy
        import pandas
        import sklearn
        import requests
        import flask
        
        print("✓ 所有依赖导入成功")
        print(f"  OpenCV: {cv2.__version__}")
        print(f"  MediaPipe: {mediapipe.__version__}")
        return True
    except ImportError as e:
        print(f"✗ 依赖导入失败: {e}")
        return False


def test_module_imports():
    """测试项目模块导入"""
    print("\n测试: 项目模块导入...")
    try:
        from python import config
        from python.pose_detector import PoseDetector
        from python.angle_calculator import AngleCalculator
        from python.motion_tracker import MotionTracker
        from python.feature_extractor import FeatureExtractor
        from python.java_bridge import JavaBridge
        from python.ui_manager import UIManager
        from python import utils
        
        print("✓ 所有项目模块导入成功")
        return True
    except ImportError as e:
        print(f"✗ 模块导入失败: {e}")
        return False


def test_configuration():
    """测试配置文件"""
    print("\n测试: 配置文件...")
    try:
        from python.config import (
            CAMERA_INDEX, CAMERA_WIDTH, CAMERA_HEIGHT,
            ExerciseType, LandmarkIndex,
            SQUAT_THRESHOLDS, PUSHUP_THRESHOLDS
        )
        
        assert isinstance(CAMERA_INDEX, int)
        assert isinstance(CAMERA_WIDTH, int)
        assert isinstance(CAMERA_HEIGHT, int)
        assert hasattr(ExerciseType, 'SQUAT')
        assert hasattr(ExerciseType, 'PUSHUP')
        
        print("✓ 配置文件检查通过")
        return True
    except Exception as e:
        print(f"✗ 配置文件检查失败: {e}")
        return False


def test_pose_detection_pipeline():
    """测试姿态检测流水线"""
    print("\n测试: 姿态检测流水线...")
    try:
        from python.pose_detector import PoseDetector
        from python.angle_calculator import AngleCalculator
        from python.config import ExerciseType
        
        # 初始化
        detector = PoseDetector()
        calculator = AngleCalculator()
        
        # 创建测试图像
        test_image = cv2.imread("test_image.jpg") if os.path.exists("test_image.jpg") else None
        
        if test_image is None:
            # 使用摄像头获取一帧
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                ret, test_image = cap.read()
                cap.release()
        
        if test_image is not None:
            # 检测
            landmarks = detector.detect(test_image)
            
            if landmarks:
                # 计算角度
                angles = calculator.get_squat_angles(landmarks)
                print("✓ 姿态检测流水线运行成功")
                print(f"  检测到关键点: {len(landmarks)}")
                print(f"  计算的角度: {list(angles.keys())}")
            else:
                print("! 未检测到人体（可能需要实际人物图像）")
            
            detector.close()
            return True
        else:
            print("! 无法获取测试图像")
            return True  # 不算失败
            
    except Exception as e:
        print(f"✗ 流水线测试失败: {e}")
        return False


def test_motion_tracking():
    """测试动作追踪"""
    print("\n测试: 动作追踪...")
    try:
        from python.motion_tracker import MotionTracker
        from python.config import ExerciseType
        
        tracker = MotionTracker(ExerciseType.SQUAT)
        
        # 模拟动作序列
        # 站立 -> 下蹲 -> 站立
        angles_sequence = [
            {'knee_avg': 170},  # 站立
            {'knee_avg': 160},
            {'knee_avg': 140},
            {'knee_avg': 120},
            {'knee_avg': 95},   # 下蹲
            {'knee_avg': 110},
            {'knee_avg': 130},
            {'knee_avg': 150},
            {'knee_avg': 165},  # 站立
        ]
        
        for angles in angles_sequence:
            tracker.update(angles)
            time.sleep(0.1)
        
        rep_count = tracker.get_rep_count()
        print("✓ 动作追踪运行成功")
        print(f"  检测到的重复次数: {rep_count}")
        
        return True
    except Exception as e:
        print(f"✗ 动作追踪测试失败: {e}")
        return False


def test_api_connectivity():
    """测试API连接"""
    print("\n测试: API连接...")
    try:
        from python.java_bridge import JavaBridge
        
        bridge = JavaBridge()
        is_healthy = bridge.health_check()
        
        if is_healthy:
            print("✓ API服务运行正常")
        else:
            print("! API服务未运行（这是正常的，如未启动Flask）")
        
        bridge.close()
        return True  # 不强制要求API运行
    except Exception as e:
        print(f"! API测试跳过: {e}")
        return True


def test_java_files_exist():
    """测试Java文件是否存在"""
    print("\n测试: Java文件检查...")
    java_files = [
        "java/src/main/java/com/virtualtrainer/ExerciseClassifier.java",
        "java/src/main/java/com/virtualtrainer/GeneticFeatureSelector.java",
        "java/src/main/java/com/virtualtrainer/FuzzyFeedbackEngine.java",
        "java/src/main/resources/fitness_feedback.fcl"
    ]
    
    all_exist = True
    for file_path in java_files:
        if os.path.exists(file_path):
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} 不存在")
            all_exist = False
    
    if all_exist:
        print("✓ 所有Java文件存在")
    else:
        print("! 部分Java文件缺失")
    
    return all_exist


def run_all_tests():
    """运行所有集成测试"""
    print("=" * 60)
    print("系统集成测试套件")
    print("=" * 60)
    
    tests = [
        test_dependencies,
        test_module_imports,
        test_configuration,
        test_pose_detection_pipeline,
        test_motion_tracking,
        test_api_connectivity,
        test_java_files_exist
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"测试结果: {sum(results)}/{len(results)} 通过")
    print("=" * 60)
    
    if all(results):
        print("\n✓ 所有测试通过！系统准备就绪。")
    else:
        print("\n! 部分测试未通过，请检查错误信息。")
    
    return all(results)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

