"""
数据采集模块
用于录制和标注训练数据
"""

import cv2
import os
import time
import json
from datetime import datetime
from typing import Optional
from pose_detector import PoseDetector
from angle_calculator import AngleCalculator
from feature_extractor import FeatureExtractor
from config import ExerciseType, DATA_COLLECTION_CONFIG


class DataCollector:
    """数据采集器类"""
    
    def __init__(self, exercise_type: ExerciseType, correctness: str, error_type: str = "none"):
        """
        初始化数据采集器
        
        Args:
            exercise_type: 运动类型
            correctness: 正确性 ('correct' 或 'incorrect')
            error_type: 错误类型（如果incorrect）
        """
        self.exercise_type = exercise_type
        self.correctness = correctness
        self.error_type = error_type
        
        # 初始化模块
        self.pose_detector = PoseDetector()
        self.angle_calculator = AngleCalculator()
        self.feature_extractor = FeatureExtractor()
        
        # 数据存储
        self.frames_data = []
        self.video_writer = None
        
        # 生成保存路径
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_id = f"{exercise_type.value}_{correctness}_{timestamp}"
        
        # 创建保存目录
        self.base_dir = f"dataset/raw/{exercise_type.value}/{correctness}"
        os.makedirs(self.base_dir, exist_ok=True)
        
    def start_recording(self, frame_width: int, frame_height: int):
        """
        开始录制
        
        Args:
            frame_width: 视频宽度
            frame_height: 视频高度
        """
        if DATA_COLLECTION_CONFIG['save_video']:
            video_path = os.path.join(self.base_dir, f"{self.session_id}.mp4")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_writer = cv2.VideoWriter(
                video_path,
                fourcc,
                DATA_COLLECTION_CONFIG['fps'],
                (frame_width, frame_height)
            )
            print(f"开始录制视频: {video_path}")
    
    def process_frame(self, frame):
        """
        处理并保存单帧数据
        
        Args:
            frame: 输入图像帧
        """
        # 检测姿态
        landmarks = self.pose_detector.detect(frame)
        
        if landmarks:
            # 计算角度
            if self.exercise_type == ExerciseType.SQUAT:
                angles = self.angle_calculator.get_squat_angles(landmarks)
            else:
                angles = self.angle_calculator.get_pushup_angles(landmarks)
            
            # 提取特征
            features = self.feature_extractor.extract_frame_features(landmarks, angles)
            
            # 保存帧数据
            frame_data = {
                'timestamp': time.time(),
                'landmarks': landmarks,
                'angles': angles,
                'features': features
            }
            self.frames_data.append(frame_data)
            
            # 绘制骨架
            frame = self.pose_detector.draw_landmarks(frame)
        
        # 保存视频帧
        if self.video_writer:
            self.video_writer.write(frame)
        
        return frame
    
    def stop_recording(self):
        """停止录制并保存数据"""
        # 释放视频写入器
        if self.video_writer:
            self.video_writer.release()
            print(f"视频保存完成")
        
        # 保存特征数据
        if DATA_COLLECTION_CONFIG['save_features'] and self.frames_data:
            features_path = os.path.join(self.base_dir, f"{self.session_id}_features.json")
            
            # 创建元数据
            metadata = {
                'session_id': self.session_id,
                'exercise_type': self.exercise_type.value,
                'correctness': self.correctness,
                'error_type': self.error_type,
                'num_frames': len(self.frames_data),
                'timestamp': datetime.now().isoformat()
            }
            
            # 保存
            output_data = {
                'metadata': metadata,
                'frames': self.frames_data
            }
            
            with open(features_path, 'w') as f:
                json.dump(output_data, f, indent=2)
            
            print(f"特征数据保存完成: {features_path}")
            print(f"共采集 {len(self.frames_data)} 帧数据")
    
    def close(self):
        """清理资源"""
        self.pose_detector.close()
        if self.video_writer:
            self.video_writer.release()


def run_data_collection():
    """运行数据采集程序（交互式）"""
    print("=" * 50)
    print("虚拟健身教练 - 数据采集工具")
    print("=" * 50)
    
    # 选择运动类型
    print("\n选择运动类型:")
    print("1. 深蹲 (Squat)")
    print("2. 俯卧撑 (Pushup)")
    exercise_choice = input("请输入 (1/2): ").strip()
    
    if exercise_choice == "1":
        exercise_type = ExerciseType.SQUAT
    elif exercise_choice == "2":
        exercise_type = ExerciseType.PUSHUP
    else:
        print("无效选择")
        return
    
    # 选择正确性
    print("\n选择动作质量:")
    print("1. 正确 (Correct)")
    print("2. 错误 (Incorrect)")
    correctness_choice = input("请输入 (1/2): ").strip()
    
    if correctness_choice == "1":
        correctness = "correct"
        error_type = "none"
    elif correctness_choice == "2":
        correctness = "incorrect"
        print("\n选择错误类型:")
        if exercise_type == ExerciseType.SQUAT:
            print("1. 膝盖内扣")
            print("2. 下蹲不足")
            print("3. 重心前倾")
        else:
            print("1. 塌腰")
            print("2. 臀部过高")
            print("3. 手臂角度错误")
        error_choice = input("请输入错误类型编号: ").strip()
        error_types = {
            "1": "knee_valgus" if exercise_type == ExerciseType.SQUAT else "sagging_back",
            "2": "insufficient_depth" if exercise_type == ExerciseType.SQUAT else "high_hips",
            "3": "forward_lean" if exercise_type == ExerciseType.SQUAT else "wrong_arm_angle"
        }
        error_type = error_types.get(error_choice, "unknown")
    else:
        print("无效选择")
        return
    
    # 初始化采集器
    collector = DataCollector(exercise_type, correctness, error_type)
    
    # 打开摄像头
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    if not cap.isOpened():
        print("无法打开摄像头")
        return
    
    # 获取视频尺寸
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print("\n准备就绪!")
    print("按 'r' 开始录制")
    print("按 's' 停止录制")
    print("按 'q' 退出")
    
    recording = False
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 处理帧
        if recording:
            frame = collector.process_frame(frame)
            cv2.putText(frame, "RECORDING", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # 显示状态信息
        status_text = f"Exercise: {exercise_type.value} | Status: {'RECORDING' if recording else 'READY'}"
        cv2.putText(frame, status_text, (10, frame_height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow('Data Collection', frame)
        
        # 键盘控制
        key = cv2.waitKey(1) & 0xFF
        if key == ord('r') and not recording:
            collector.start_recording(frame_width, frame_height)
            recording = True
        elif key == ord('s') and recording:
            collector.stop_recording()
            recording = False
            print("\n继续录制请按 'r'，退出请按 'q'")
        elif key == ord('q'):
            break
    
    # 清理
    if recording:
        collector.stop_recording()
    collector.close()
    cap.release()
    cv2.destroyAllWindows()
    
    print("\n数据采集完成!")


if __name__ == "__main__":
    run_data_collection()

