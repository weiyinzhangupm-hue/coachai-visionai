"""
Java桥接模块
通过REST API与Java后端通信
"""

import requests
import json
from typing import Dict, Optional, List
from config import API_CONFIG


class JavaBridge:
    """Python-Java REST API客户端"""
    
    def __init__(self, api_url: str = None):
        """
        初始化桥接器
        
        Args:
            api_url: API基础URL，默认从配置读取
        """
        self.api_url = api_url or API_CONFIG['base_url']
        self.timeout = API_CONFIG['timeout']
        self.session = requests.Session()
        
    def classify_exercise(self, features: Dict[str, float]) -> Optional[Dict]:
        """
        调用分类服务
        
        Args:
            features: 特征字典
            
        Returns:
            分类结果: {
                'exercise_type': str,
                'correctness': str,
                'confidence': float,
                'error_type': str (可选)
            }
        """
        try:
            url = f"{self.api_url}{API_CONFIG['classify_endpoint']}"
            response = self.session.post(
                url,
                json={'features': features},
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"分类请求失败: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print("分类请求超时")
            return None
        except requests.exceptions.ConnectionError:
            print("无法连接到Java服务，请确保Flask API正在运行")
            return None
        except Exception as e:
            print(f"分类请求出错: {e}")
            return None
    
    def get_fuzzy_feedback(self, motion_data: Dict) -> Optional[Dict]:
        """
        获取模糊逻辑反馈
        
        Args:
            motion_data: 运动数据 {
                'velocidad': float,  # 速度（秒/次）
                'amplitud': float,   # 幅度（角度）
                'estabilidad': float,  # 稳定性（0-100）
                'fatiga': float      # 疲劳度（0-100）
            }
            
        Returns:
            反馈结果: {
                'score': float,
                'feedback_text': str,
                'suggestions': List[str]
            }
        """
        try:
            url = f"{self.api_url}{API_CONFIG['feedback_endpoint']}"
            response = self.session.post(
                url,
                json=motion_data,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"反馈请求失败: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print("反馈请求超时")
            return None
        except requests.exceptions.ConnectionError:
            print("无法连接到Java服务，请确保Flask API正在运行")
            return None
        except Exception as e:
            print(f"反馈请求出错: {e}")
            return None
    
    def health_check(self) -> bool:
        """
        检查Java服务是否正常运行
        
        Returns:
            服务是否可用
        """
        try:
            url = f"{self.api_url}/health"
            response = self.session.get(url, timeout=2.0)
            return response.status_code == 200
        except:
            return False
    
    def close(self):
        """关闭会话"""
        self.session.close()

