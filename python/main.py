"""
Programa principal - Entrenador Virtual
Integra todos los módulos, implementa detección de movimiento en tiempo real y retroalimentación
"""

import cv2
import sys
import time
from collections import deque

from config import (
    CAMERA_INDEX, CAMERA_WIDTH, CAMERA_HEIGHT,
    ExerciseType, FEATURE_CONFIG
)
from pose_detector import PoseDetector
from angle_calculator import AngleCalculator
from motion_tracker import MotionTracker
from feature_extractor import FeatureExtractor
from hybrid_classifier import HybridClassifier
from ui_manager import UIManager
from utils import setup_logger, print_system_info, check_dependencies


class VirtualTrainer:
    """Clase principal del Entrenador Virtual"""
    
    def __init__(self, exercise_type: ExerciseType):
        """
        Inicializar entrenador virtual
        
        Args:
            exercise_type: Tipo de ejercicio
        """
        self.exercise_type = exercise_type
        self.logger = setup_logger()
        
        # Inicializar módulos
        self.logger.info("Inicializando módulos...")
        self.pose_detector = PoseDetector()
        self.angle_calculator = AngleCalculator()
        self.motion_tracker = MotionTracker(exercise_type)
        self.feature_extractor = FeatureExtractor()
        
        # Usar clasificador híbrido en lugar de puente Java
        self.classifier = HybridClassifier(use_ml=False)
        self.logger.info("Usando clasificador híbrido (basado en reglas)")
        
        self.ui_manager = UIManager()
        
        # Caché de datos históricos
        self.feature_history = deque(maxlen=FEATURE_CONFIG['history_length'])
        self.angle_history = deque(maxlen=30)
        
        # Monitoreo de rendimiento
        self.frame_times = deque(maxlen=30)
        
        # Caché de retroalimentación
        self.last_feedback = None
        self.last_feedback_time = 0
        self.feedback_interval = 2.0
        
        # Caché de resultados de clasificación
        self.last_classification = None
        
    def run(self):
        """Ejecutar programa principal"""
        print_system_info()
        
        # Información sobre el clasificador
        self.logger.info("Sistema de clasificación híbrida activo")
        self.logger.info("Modo: Basado en reglas (sin necesidad de datos de entrenamiento)")
        
        # Abrir cámara
        self.logger.info("Abriendo cámara...")
        cap = cv2.VideoCapture(CAMERA_INDEX)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        
        if not cap.isOpened():
            self.logger.error("No se puede abrir la cámara")
            return
        
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.logger.info(f"Resolución de cámara: {frame_width}x{frame_height}")
        
        # Crear ventana UI
        self.ui_manager.create_window()
        
        self.logger.info("=" * 60)
        self.logger.info(f"Entrenador Virtual iniciado - Tipo de ejercicio: {self.exercise_type.value}")
        self.logger.info("Presiona 'q' para salir, 'r' para reiniciar contador")
        self.logger.info("=" * 60)
        
        # Bucle principal
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            frame = self.process_frame(frame, frame_height, frame_width)
            self.ui_manager.show_frame(frame)
            self.frame_times.append(time.time())
            
            key = self.ui_manager.wait_key(1)
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.motion_tracker.reset()
                self.feature_history.clear()
                self.angle_history.clear()
        
        self.cleanup(cap)
        self.show_statistics()
    
    def process_frame(self, frame, frame_height, frame_width):
        """Procesar un solo frame"""
        landmarks = self.pose_detector.detect(frame)
        
        if landmarks is None:
            frame = self.ui_manager.draw_status_message(frame, "No person detected", "warning")
            return frame
        
        frame = self.pose_detector.draw_landmarks(frame)
        
        if self.exercise_type == ExerciseType.SQUAT:
            angles = self.angle_calculator.get_squat_angles(landmarks)
        else:
            angles = self.angle_calculator.get_pushup_angles(landmarks)
        
        self.motion_tracker.update(angles)
        self.angle_history.append(angles)
        
        # Clasificar cada 2 segundos (evitar demasiada frecuencia)
        current_time = time.time()
        if current_time - self.last_feedback_time > self.feedback_interval:
            self.last_classification = self.classifier.classify(
                self.exercise_type,
                angles,
                list(self.angle_history)
            )
            self.last_feedback = self.last_classification.get('feedback', '')
            self.last_feedback_time = current_time
        
        frame = self.draw_ui_elements(frame, angles)
        
        return frame
    
    def draw_ui_elements(self, frame, angles):
        """Dibujar elementos de UI"""
        frame = self.ui_manager.draw_rep_counter(
            frame,
            self.motion_tracker.get_rep_count(),
            self.motion_tracker.get_current_state()
        )
        
        info = {
            'Exercise': self.exercise_type.value.capitalize(),
            'FPS': f"{self.calculate_fps():.1f}",
        }
        
        if self.exercise_type == ExerciseType.SQUAT:
            info['Knee Angle'] = f"{angles.get('knee_avg', 0):.0f}°"
        else:
            info['Elbow Angle'] = f"{angles.get('elbow_avg', 0):.0f}°"
        
        # Añadir resultados de clasificación
        if self.last_classification:
            correctness = self.last_classification.get('correctness', 'unknown')
            info['Quality'] = 'CORRECT' if correctness == 'correct' else 'INCORRECT'
            info['Score'] = f"{self.last_classification.get('score', 0):.1f}/10"
        
        frame = self.ui_manager.draw_info_panel(frame, info)
        
        # Mostrar retroalimentación
        if self.last_feedback:
            cv2.putText(
                frame, self.last_feedback, 
                (10, frame.shape[0] - 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2
            )
        
        return frame
    
    def calculate_fps(self) -> float:
        """Calcular FPS"""
        if len(self.frame_times) < 2:
            return 0.0
        time_diff = self.frame_times[-1] - self.frame_times[0]
        return len(self.frame_times) / time_diff if time_diff > 0 else 0.0
    
    def cleanup(self, cap):
        """Limpiar recursos"""
        cap.release()
        self.pose_detector.close()
        self.ui_manager.close()
        cv2.destroyAllWindows()
    
    def show_statistics(self):
        """Mostrar estadísticas"""
        print("=" * 60)
        print(f"Repeticiones totales: {self.motion_tracker.get_rep_count()}")
        if self.last_classification:
            print(f"Última puntuación: {self.last_classification.get('score', 0):.1f}/10")
        print("=" * 60)


def main():
    """Función principal"""
    if not check_dependencies():
        sys.exit(1)
    
    print("=" * 60)
    print("Sistema de Entrenador Virtual")
    print("=" * 60)
    print("\nSeleccione tipo de ejercicio:")
    print("1. Sentadilla (Squat)")
    print("2. Flexión (Pushup)")
    
    choice = input("\nIngrese (1/2): ").strip()
    
    if choice == "1":
        exercise_type = ExerciseType.SQUAT
    elif choice == "2":
        exercise_type = ExerciseType.PUSHUP
    else:
        exercise_type = ExerciseType.SQUAT
    
    trainer = VirtualTrainer(exercise_type)
    trainer.run()


if __name__ == "__main__":
    main()

