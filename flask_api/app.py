"""
Flask REST API服务
提供分类和模糊反馈的API端点
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json
import os

app = Flask(__name__)
CORS(app)

# Java程序路径配置
JAVA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'java')
JAVA_CLASSPATH = f"{JAVA_DIR}/lib/weka.jar:{JAVA_DIR}/lib/jFuzzyLogic.jar:."


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'ok',
        'service': 'Virtual Trainer API',
        'version': '1.0'
    }), 200


@app.route('/classify', methods=['POST'])
def classify():
    """
    运动分类端点
    
    请求体: {
        "features": {
            "feature1": value1,
            "feature2": value2,
            ...
        }
    }
    
    返回: {
        "exercise_type": "squat" | "pushup",
        "correctness": "correct" | "incorrect",
        "confidence": 0.95,
        "error_type": "knee_valgus" (如果incorrect)
    }
    """
    try:
        data = request.get_json()
        features = data.get('features', {})
        
        # TODO: 实际调用Java分类器
        # 当前返回模拟数据
        response = {
            'exercise_type': 'squat',
            'correctness': 'correct',
            'confidence': 0.85,
            'error_type': None
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': '分类请求处理失败'
        }), 500


@app.route('/feedback', methods=['POST'])
def feedback():
    """
    模糊反馈端点
    
    请求体: {
        "velocidad": 2.5,    // 速度（秒/次）
        "amplitud": 120,      // 幅度（角度）
        "estabilidad": 80,    // 稳定性（0-100）
        "fatiga": 20          // 疲劳度（0-100）
    }
    
    返回: {
        "score": 8.5,
        "feedback_text": "动作质量良好，保持当前节奏",
        "suggestions": ["保持膝盖稳定", "注意呼吸节奏"]
    }
    """
    try:
        data = request.get_json()
        
        velocidad = data.get('velocidad', 2.0)
        amplitud = data.get('amplitud', 90)
        estabilidad = data.get('estabilidad', 70)
        fatiga = data.get('fatiga', 20)
        
        # TODO: 实际调用Java模糊推理引擎
        # 当前返回基于简单规则的模拟反馈
        score = calculate_simple_score(velocidad, amplitud, estabilidad, fatiga)
        feedback_text = generate_simple_feedback(velocidad, amplitud, estabilidad, fatiga)
        suggestions = generate_suggestions(velocidad, amplitud, estabilidad, fatiga)
        
        response = {
            'score': score,
            'feedback_text': feedback_text,
            'suggestions': suggestions
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': '反馈请求处理失败'
        }), 500


def calculate_simple_score(velocidad, amplitud, estabilidad, fatiga):
    """简单的评分计算（临时实现）"""
    score = 10.0
    
    # 速度评分（理想范围: 1.5-3.0秒）
    if velocidad < 1.0:
        score -= 2.0
    elif velocidad > 4.0:
        score -= 1.5
    
    # 幅度评分（理想范围: 90-120度）
    if amplitud < 70:
        score -= 2.0
    elif amplitud < 90:
        score -= 1.0
    
    # 稳定性评分
    if estabilidad < 60:
        score -= 1.5
    elif estabilidad < 75:
        score -= 0.5
    
    # 疲劳影响
    if fatiga > 70:
        score -= 1.0
    elif fatiga > 50:
        score -= 0.5
    
    return max(0, min(10, score))


def generate_simple_feedback(velocidad, amplitud, estabilidad, fatiga):
    """生成简单反馈文本（临时实现）"""
    feedback_parts = []
    
    if velocidad < 1.0:
        feedback_parts.append("速度过快")
    elif velocidad > 4.0:
        feedback_parts.append("速度较慢")
    else:
        feedback_parts.append("速度合适")
    
    if amplitud < 90:
        feedback_parts.append("幅度不足")
    else:
        feedback_parts.append("幅度良好")
    
    if estabilidad < 70:
        feedback_parts.append("注意保持稳定")
    
    if fatiga > 60:
        feedback_parts.append("建议适当休息")
    
    return "，".join(feedback_parts) if feedback_parts else "动作质量良好"


def generate_suggestions(velocidad, amplitud, estabilidad, fatiga):
    """生成建议列表（临时实现）"""
    suggestions = []
    
    if amplitud < 90:
        suggestions.append("增加下蹲深度")
    
    if estabilidad < 70:
        suggestions.append("保持核心收紧")
    
    if velocidad < 1.5:
        suggestions.append("放慢动作速度")
    
    if fatiga > 60:
        suggestions.append("考虑休息片刻")
    
    return suggestions


@app.route('/train', methods=['POST'])
def train_model():
    """
    训练模型端点（用于后续阶段）
    
    请求体: {
        "dataset_path": "path/to/dataset.csv",
        "model_type": "decision_tree",
        "use_genetic_algorithm": true
    }
    """
    try:
        data = request.get_json()
        
        # TODO: 实际调用Java模型训练程序
        
        response = {
            'status': 'training_started',
            'message': '模型训练已开始',
            'estimated_time': '5-10分钟'
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': '训练请求处理失败'
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("虚拟健身教练 - Flask REST API服务")
    print("=" * 60)
    print("服务地址: http://localhost:5000")
    print("端点:")
    print("  GET  /health      - 健康检查")
    print("  POST /classify    - 运动分类")
    print("  POST /feedback    - 模糊反馈")
    print("  POST /train       - 模型训练")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)

