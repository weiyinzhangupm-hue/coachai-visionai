"""
Clasificador basado en reglas
No requiere datos de entrenamiento, utiliza reglas para juzgar la calidad del movimiento
"""

from typing import Dict, List
from config import SQUAT_THRESHOLDS, PUSHUP_THRESHOLDS, ExerciseType


class RuleBasedClassifier:
    """Clasificador basado en reglas"""
    
    def __init__(self):
        self.squat_thresholds = SQUAT_THRESHOLDS
        self.pushup_thresholds = PUSHUP_THRESHOLDS
    
    def classify_squat(self, angles: Dict, history: List = None) -> Dict:
        """
        Juicio de calidad de movimiento de sentadilla
        
        Args:
            angles: Diccionario de ángulos actuales
            history: Datos históricos de ángulos (opcional)
        
        Returns:
            Diccionario de resultados de clasificación
        """
        errors = []
        warnings = []
        score = 10.0
        
        # Obtener ángulos clave
        knee_angle = angles.get('knee_avg', 180)
        hip_angle = angles.get('hip_avg', 180)
        back_angle = angles.get('back_angle', 90)
        left_knee = angles.get('left_knee', 180)
        right_knee = angles.get('right_knee', 180)
        
        # Regla 1: Verificación de ángulo de rodilla (más importante)
        if knee_angle < 70:
            errors.append('Sentadilla demasiado profunda, puede causar presión en las rodillas')
            score -= 2.0
        elif knee_angle > 120 and knee_angle < 160:
            warnings.append('Profundidad insuficiente, se recomienda bajar hasta que los muslos estén paralelos al suelo')
            score -= 1.5
        
        # Regla 2: Ángulo de cadera
        if hip_angle < 60:
            errors.append('Ángulo de cadera demasiado pequeño')
            score -= 1.5
        
        # Regla 3: Ángulo de espalda (detectar inclinación hacia adelante)
        if back_angle < 45:
            errors.append('Inclinación excesiva hacia adelante, mantener la espalda recta')
            score -= 2.0
        elif back_angle > 90:
            warnings.append('Torso demasiado vertical')
            score -= 0.5
        
        # Regla 4: Simetría de rodillas izquierda y derecha (detectar valgo de rodilla)
        knee_diff = abs(left_knee - right_knee)
        if knee_diff > 20:
            errors.append('Rodillas asimétricas, cuidado con el valgo de rodilla')
            score -= 2.0
        elif knee_diff > 10:
            warnings.append('Ligera asimetría en las rodillas')
            score -= 1.0
        
        # Regla 5: Verificación de velocidad (basada en datos históricos)
        if history and len(history) > 5:
            speed_score, speed_msg = self._check_speed(history)
            score += speed_score
            if speed_msg:
                warnings.append(speed_msg)
        
        # Determinar corrección
        correctness = 'correct' if len(errors) == 0 else 'incorrect'
        confidence = 0.9 if len(errors) == 0 else 0.7
        
        # Determinar tipo de error
        error_type = 'none'
        if 'valgo de rodilla' in str(errors):
            error_type = 'knee_valgus'
        elif 'Profundidad insuficiente' in str(errors) or 'Profundidad insuficiente' in str(warnings):
            error_type = 'insufficient_depth'
        elif 'adelante' in str(errors):
            error_type = 'forward_lean'
        
        return {
            'correctness': correctness,
            'confidence': confidence,
            'error_type': error_type,
            'errors': errors,
            'warnings': warnings,
            'score': max(0, min(10, score)),
            'angles': {
                'knee': knee_angle,
                'hip': hip_angle,
                'back': back_angle
            }
        }
    
    def classify_pushup(self, angles: Dict, history: List = None) -> Dict:
        """
        Juicio de calidad de movimiento de flexión
        
        Args:
            angles: Diccionario de ángulos actuales
            history: Datos históricos de ángulos (opcional)
        
        Returns:
            Diccionario de resultados de clasificación
        """
        errors = []
        warnings = []
        score = 10.0
        
        # Obtener ángulos clave
        elbow_angle = angles.get('elbow_avg', 180)
        shoulder_angle = angles.get('shoulder_avg', 90)
        body_angle = angles.get('body_line_angle', 180)
        left_elbow = angles.get('left_elbow', 180)
        right_elbow = angles.get('right_elbow', 180)
        
        # Regla 1: Ángulo del codo
        if elbow_angle < 70:
            errors.append('Descenso excesivo')
            score -= 1.5
        elif elbow_angle > 110 and elbow_angle < 160:
            warnings.append('Amplitud insuficiente, los brazos deben doblarse a 90 grados')
            score -= 2.0
        
        # Regla 2: Alineación del cuerpo (detectar espalda hundida y caderas altas)
        if body_angle < 160:
            errors.append('Espalda hundida, mantener el core apretado')
            score -= 2.5
        elif body_angle > 200:
            errors.append('Caderas demasiado altas, el cuerpo debe mantenerse en línea recta')
            score -= 2.0
        
        # Regla 3: Ángulo del hombro
        if shoulder_angle < 30:
            errors.append('Brazos demasiado cerca del cuerpo')
            score -= 1.0
        elif shoulder_angle > 100:
            errors.append('Brazos demasiado abiertos')
            score -= 1.0
        
        # Regla 4: Simetría izquierda-derecha
        elbow_diff = abs(left_elbow - right_elbow)
        if elbow_diff > 15:
            errors.append('Brazos asimétricos')
            score -= 1.5
        elif elbow_diff > 8:
            warnings.append('Ligera asimetría en los brazos')
            score -= 0.5
        
        # Regla 5: Verificación de velocidad
        if history and len(history) > 5:
            speed_score, speed_msg = self._check_speed(history)
            score += speed_score
            if speed_msg:
                warnings.append(speed_msg)
        
        # Determinar corrección
        correctness = 'correct' if len(errors) == 0 else 'incorrect'
        confidence = 0.9 if len(errors) == 0 else 0.7
        
        # Determinar tipo de error
        error_type = 'none'
        if 'hundida' in str(errors):
            error_type = 'sagging_back'
        elif 'Caderas demasiado altas' in str(errors):
            error_type = 'high_hips'
        elif 'Brazos' in str(errors):
            error_type = 'wrong_arm_angle'
        
        return {
            'correctness': correctness,
            'confidence': confidence,
            'error_type': error_type,
            'errors': errors,
            'warnings': warnings,
            'score': max(0, min(10, score)),
            'angles': {
                'elbow': elbow_angle,
                'shoulder': shoulder_angle,
                'body': body_angle
            }
        }
    
    def _check_speed(self, history: List) -> tuple:
        """
        Verificar velocidad del movimiento
        
        Returns:
            (ajuste_puntuación, mensaje)
        """
        if len(history) < 10:
            return (0, None)
        
        # Cálculo simple: comparar cambios de ángulo en los últimos 10 frames
        recent = history[-10:]
        angle_changes = []
        
        for i in range(1, len(recent)):
            if 'knee_avg' in recent[i] and 'knee_avg' in recent[i-1]:
                change = abs(recent[i]['knee_avg'] - recent[i-1]['knee_avg'])
                angle_changes.append(change)
            elif 'elbow_avg' in recent[i] and 'elbow_avg' in recent[i-1]:
                change = abs(recent[i]['elbow_avg'] - recent[i-1]['elbow_avg'])
                angle_changes.append(change)
        
        if not angle_changes:
            return (0, None)
        
        avg_change = sum(angle_changes) / len(angle_changes)
        
        # Juzgar velocidad
        if avg_change > 15:  # Cambio demasiado rápido
            return (-1.0, 'Movimiento demasiado rápido, se recomienda reducir la velocidad para mantener el control')
        elif avg_change < 3:  # Cambio demasiado lento
            return (-0.5, 'Movimiento demasiado lento, se puede acelerar el ritmo adecuadamente')
        else:
            return (0, None)
    
    def classify(self, exercise_type: ExerciseType, angles: Dict, history: List = None) -> Dict:
        """
        Interfaz de clasificación unificada
        
        Args:
            exercise_type: Tipo de ejercicio
            angles: Datos de ángulos
            history: Datos históricos
        
        Returns:
            Resultado de clasificación
        """
        if exercise_type == ExerciseType.SQUAT:
            return self.classify_squat(angles, history)
        elif exercise_type == ExerciseType.PUSHUP:
            return self.classify_pushup(angles, history)
        else:
            return {
                'correctness': 'unknown',
                'confidence': 0.0,
                'error_type': 'unknown',
                'errors': ['Tipo de ejercicio desconocido'],
                'warnings': [],
                'score': 0.0
            }
