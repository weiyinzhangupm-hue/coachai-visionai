"""
Clasificador híbrido
Combina juicio basado en reglas y modelo de aprendizaje automático opcional
"""

from typing import Dict, List, Optional
from config import ExerciseType
from rule_based_classifier import RuleBasedClassifier


class HybridClassifier:
    """Sistema de clasificación híbrida"""
    
    def __init__(self, use_ml: bool = False):
        """
        Inicializar clasificador híbrido
        
        Args:
            use_ml: Si usar modelo de aprendizaje automático (requiere modelo entrenado)
        """
        self.rule_classifier = RuleBasedClassifier()
        self.ml_classifier = None
        self.use_ml = use_ml
        
        if use_ml:
            self._load_ml_model()
    
    def _load_ml_model(self):
        """Cargar modelo ML (si existe)"""
        try:
            # TODO: Si hay un modelo entrenado, cargarlo aquí
            # import pickle
            # with open('../models/classifier.pkl', 'rb') as f:
            #     self.ml_classifier = pickle.load(f)
            pass
        except Exception as e:
            print(f"Advertencia: No se puede cargar el modelo ML: {e}")
            self.ml_classifier = None
    
    def classify(
        self, 
        exercise_type: ExerciseType, 
        angles: Dict, 
        history: List = None,
        features: Optional[Dict] = None
    ) -> Dict:
        """
        Clasificación híbrida
        
        Args:
            exercise_type: Tipo de ejercicio
            angles: Datos de ángulos
            history: Datos históricos
            features: Características extraídas (para modelo ML)
        
        Returns:
            Resultado de clasificación
        """
        # Paso 1: Clasificación basada en reglas
        rule_result = self.rule_classifier.classify(exercise_type, angles, history)
        
        # Paso 2: Si hay modelo ML, combinar resultados ML
        if self.ml_classifier and features:
            try:
                ml_result = self._classify_with_ml(features)
                # Combinar dos resultados
                final_result = self._merge_results(rule_result, ml_result)
            except Exception as e:
                print(f"Clasificación ML falló: {e}, usando resultado de reglas")
                final_result = rule_result
        else:
            final_result = rule_result
        
        # Paso 3: Generar texto de retroalimentación
        final_result['feedback'] = self._generate_feedback(final_result)
        
        return final_result
    
    def _classify_with_ml(self, features: Dict) -> Dict:
        """Clasificación usando modelo ML"""
        # TODO: Implementar clasificación ML
        # prediction = self.ml_classifier.predict([features])
        # confidence = self.ml_classifier.predict_proba([features]).max()
        
        return {
            'correctness': 'correct',
            'confidence': 0.8
        }
    
    def _merge_results(self, rule_result: Dict, ml_result: Dict) -> Dict:
        """Fusionar resultados de reglas y ML"""
        # Promedio ponderado simple
        rule_weight = 0.6
        ml_weight = 0.4
        
        # Fusionar confianza
        combined_confidence = (
            rule_result['confidence'] * rule_weight +
            ml_result['confidence'] * ml_weight
        )
        
        # Si los resultados no coinciden, usar el de mayor confianza
        if rule_result['correctness'] != ml_result['correctness']:
            if rule_result['confidence'] > ml_result['confidence']:
                correctness = rule_result['correctness']
            else:
                correctness = ml_result['correctness']
        else:
            correctness = rule_result['correctness']
        
        return {
            **rule_result,
            'correctness': correctness,
            'confidence': combined_confidence,
            'method': 'hybrid'
        }
    
    def _generate_feedback(self, result: Dict) -> str:
        """Generar retroalimentación en lenguaje natural"""
        feedback_parts = []
        
        # Evaluación básica
        score = result.get('score', 0)
        if score >= 9:
            feedback_parts.append("✓ ¡Calidad de movimiento excelente!")
        elif score >= 7:
            feedback_parts.append("Calidad de movimiento buena")
        elif score >= 5:
            feedback_parts.append("Movimiento básicamente correcto, pero hay espacio para mejorar")
        else:
            feedback_parts.append("⚠ El movimiento necesita ajustes")
        
        # Indicaciones de error
        errors = result.get('errors', [])
        if errors:
            feedback_parts.append("Problemas: " + "; ".join(errors[:2]))  # Mostrar máximo 2
        
        # Indicaciones de advertencia
        warnings = result.get('warnings', [])
        if warnings and not errors:
            feedback_parts.append("Sugerencia: " + warnings[0])  # Mostrar la más importante
        
        return " | ".join(feedback_parts)
