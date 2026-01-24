"""
UI管理模块
管理用户界面显示
"""

import cv2
import numpy as np
from typing import Dict, Optional, Tuple
from config import UI_CONFIG


class UIManager:
    """UI管理器类"""
    
    def __init__(self, window_name: str = None):
        """
        初始化UI管理器
        
        Args:
            window_name: 窗口名称
        """
        self.window_name = window_name or UI_CONFIG['window_name']
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = UI_CONFIG['font_scale']
        self.font_thickness = UI_CONFIG['font_thickness']
        
    def create_window(self):
        """创建显示窗口"""
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
    
    def draw_info_panel(self, frame: np.ndarray, info: Dict) -> np.ndarray:
        """
        在图像上绘制信息面板
        
        Args:
            frame: 输入图像
            info: 信息字典，包含要显示的内容
            
        Returns:
            绘制了信息的图像
        """
        height, width = frame.shape[:2]
        
        # 创建半透明背景
        overlay = frame.copy()
        panel_height = 150
        cv2.rectangle(overlay, (0, 0), (width, panel_height), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)
        
        # 绘制文本信息
        y_offset = 30
        line_height = 30
        
        for key, value in info.items():
            text = f"{key}: {value}"
            cv2.putText(
                frame,
                text,
                (10, y_offset),
                self.font,
                self.font_scale,
                UI_CONFIG['text_color'],
                self.font_thickness,
                cv2.LINE_AA
            )
            y_offset += line_height
        
        return frame
    
    def draw_rep_counter(self, frame: np.ndarray, count: int, state: str) -> np.ndarray:
        """
        绘制重复次数计数器
        
        Args:
            frame: 输入图像
            count: 当前计数
            state: 当前状态
            
        Returns:
            绘制了计数器的图像
        """
        height, width = frame.shape[:2]
        
        # 绘制计数
        count_text = f"Reps: {count}"
        text_size = cv2.getTextSize(count_text, self.font, 1.5, 3)[0]
        text_x = width - text_size[0] - 20
        text_y = 50
        
        cv2.putText(
            frame,
            count_text,
            (text_x, text_y),
            self.font,
            1.5,
            UI_CONFIG['text_color'],
            3,
            cv2.LINE_AA
        )
        
        # 绘制状态
        state_text = f"State: {state}"
        cv2.putText(
            frame,
            state_text,
            (text_x, text_y + 40),
            self.font,
            0.8,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )
        
        return frame
    
    def draw_feedback(self, frame: np.ndarray, feedback: Dict) -> np.ndarray:
        """
        绘制反馈信息
        
        Args:
            frame: 输入图像
            feedback: 反馈字典 {'score': float, 'feedback_text': str}
            
        Returns:
            绘制了反馈的图像
        """
        if not feedback:
            return frame
        
        height, width = frame.shape[:2]
        
        # 创建底部反馈区域
        overlay = frame.copy()
        panel_y = height - 100
        cv2.rectangle(overlay, (0, panel_y), (width, height), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)
        
        # 绘制评分
        score = feedback.get('score', 0)
        score_text = f"Score: {score:.1f}/10"
        score_color = self._get_score_color(score)
        
        cv2.putText(
            frame,
            score_text,
            (10, panel_y + 30),
            self.font,
            1.0,
            score_color,
            2,
            cv2.LINE_AA
        )
        
        # 绘制反馈文本
        feedback_text = feedback.get('feedback_text', '')
        if feedback_text:
            # 自动换行处理
            max_width = width - 20
            words = feedback_text.split()
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                text_size = cv2.getTextSize(test_line, self.font, 0.6, 2)[0]
                
                if text_size[0] < max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # 绘制每一行
            y_pos = panel_y + 60
            for line in lines[:2]:  # 最多显示2行
                cv2.putText(
                    frame,
                    line,
                    (10, y_pos),
                    self.font,
                    0.6,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA
                )
                y_pos += 25
        
        return frame
    
    def draw_angle_labels(self, frame: np.ndarray, angles: Dict, 
                          landmark_coords: Dict[str, Tuple[int, int]]) -> np.ndarray:
        """
        在关节位置绘制角度标签
        
        Args:
            frame: 输入图像
            angles: 角度字典
            landmark_coords: 关节坐标字典
            
        Returns:
            绘制了角度标签的图像
        """
        color = UI_CONFIG['angle_color']
        
        for angle_name, angle_value in angles.items():
            # 根据角度名称确定显示位置
            coord_key = self._get_coord_key_for_angle(angle_name)
            
            if coord_key in landmark_coords:
                coord = landmark_coords[coord_key]
                text = f"{int(angle_value)}"
                
                cv2.putText(
                    frame,
                    text,
                    coord,
                    self.font,
                    0.5,
                    color,
                    2,
                    cv2.LINE_AA
                )
        
        return frame
    
    def draw_status_message(self, frame: np.ndarray, message: str, 
                           message_type: str = "info") -> np.ndarray:
        """
        绘制状态消息
        
        Args:
            frame: 输入图像
            message: 消息文本
            message_type: 消息类型 ('info', 'error', 'warning')
            
        Returns:
            绘制了消息的图像
        """
        height, width = frame.shape[:2]
        
        # 选择颜色
        if message_type == "error":
            color = UI_CONFIG['error_color']
        elif message_type == "warning":
            color = (0, 165, 255)  # 橙色
        else:
            color = UI_CONFIG['text_color']
        
        # 计算文本位置（居中）
        text_size = cv2.getTextSize(message, self.font, 0.8, 2)[0]
        text_x = (width - text_size[0]) // 2
        text_y = height // 2
        
        # 绘制背景
        padding = 10
        cv2.rectangle(
            frame,
            (text_x - padding, text_y - text_size[1] - padding),
            (text_x + text_size[0] + padding, text_y + padding),
            (0, 0, 0),
            -1
        )
        
        # 绘制文本
        cv2.putText(
            frame,
            message,
            (text_x, text_y),
            self.font,
            0.8,
            color,
            2,
            cv2.LINE_AA
        )
        
        return frame
    
    def show_frame(self, frame: np.ndarray):
        """显示帧"""
        cv2.imshow(self.window_name, frame)
    
    def wait_key(self, delay: int = 1) -> int:
        """等待按键"""
        return cv2.waitKey(delay) & 0xFF
    
    def close(self):
        """关闭窗口"""
        cv2.destroyWindow(self.window_name)
    
    @staticmethod
    def _get_score_color(score: float) -> Tuple[int, int, int]:
        """根据评分获取颜色"""
        if score >= 8:
            return (0, 255, 0)  # 绿色
        elif score >= 6:
            return (0, 255, 255)  # 黄色
        elif score >= 4:
            return (0, 165, 255)  # 橙色
        else:
            return (0, 0, 255)  # 红色
    
    @staticmethod
    def _get_coord_key_for_angle(angle_name: str) -> str:
        """根据角度名称获取对应的坐标键"""
        mapping = {
            'left_knee': 'left_knee',
            'right_knee': 'right_knee',
            'left_hip': 'left_hip',
            'right_hip': 'right_hip',
            'left_elbow': 'left_elbow',
            'right_elbow': 'right_elbow',
            'left_shoulder': 'left_shoulder',
            'right_shoulder': 'right_shoulder'
        }
        return mapping.get(angle_name, '')

