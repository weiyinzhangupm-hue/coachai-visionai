"""
Java调用桥接模块
用于从Flask调用Java程序
"""

import subprocess
import json
import os


class JavaCaller:
    """Java程序调用器"""
    
    def __init__(self, java_dir: str):
        """
        初始化Java调用器
        
        Args:
            java_dir: Java项目目录
        """
        self.java_dir = java_dir
        self.classpath = self._build_classpath()
    
    def _build_classpath(self) -> str:
        """构建Java classpath"""
        lib_dir = os.path.join(self.java_dir, 'lib')
        jars = [
            os.path.join(lib_dir, 'weka.jar'),
            os.path.join(lib_dir, 'jFuzzyLogic.jar')
        ]
        
        # 添加编译后的class文件路径
        classes_dir = os.path.join(self.java_dir, 'bin')
        
        classpath_parts = jars + [classes_dir]
        return ':'.join(classpath_parts)
    
    def call_classifier(self, features: dict) -> dict:
        """
        调用Java分类器
        
        Args:
            features: 特征字典
            
        Returns:
            分类结果
        """
        try:
            # 将特征转换为JSON字符串
            features_json = json.dumps(features)
            
            # 调用Java程序
            cmd = [
                'java',
                '-cp', self.classpath,
                'com.virtualtrainer.ExerciseClassifier',
                features_json
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                print(f"Java分类器错误: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"调用Java分类器失败: {e}")
            return None
    
    def call_fuzzy_engine(self, motion_data: dict) -> dict:
        """
        调用Java模糊推理引擎
        
        Args:
            motion_data: 运动数据
            
        Returns:
            反馈结果
        """
        try:
            motion_json = json.dumps(motion_data)
            
            cmd = [
                'java',
                '-cp', self.classpath,
                'com.virtualtrainer.FuzzyFeedbackEngine',
                motion_json
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                print(f"Java模糊引擎错误: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"调用Java模糊引擎失败: {e}")
            return None

