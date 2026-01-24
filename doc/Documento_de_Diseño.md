Sistema de Entrenador Virtual de Fitness - Documento de Diseño



1. Descripción de la Problemática

1.1 Cada vez más personas eligen hacer ejercicio en casa, pero la falta de orientación profesional de entrenadores conduce a los siguientes problemas:

Movimientos incorrectos: Las posturas erróneas pueden resultar en efectos de entrenamiento deficientes e incluso causar lesiones deportivas

Falta de retroalimentación: Los usuarios no pueden conocer en tiempo real la calidad de sus movimientos y las direcciones de mejora

Falta de personalización: Los videos de fitness tradicionales no pueden proporcionar consejos específicos según las circunstancias individuales

Costo elevado: Contratar un entrenador personal es costoso y no todos pueden permitírselo

1.2 Este proyecto tiene como objetivo desarrollar un sistema inteligente de entrenador virtual de fitness que pueda:

1. Detectar en tiempo real la postura de ejercicio del usuario (flexiones, sentadillas, etc.)

2. Clasificar automáticamente la corrección del movimiento (correcto/incorrecto y tipo de error)

3. Proporcionar retroalimentación personalizada para ayudar a los usuarios a mejorar la calidad del movimiento

4. Evaluar cuantitativamente el rendimiento del ejercicio (velocidad, amplitud, número de repeticiones, etc.)

1.3 Desafíos Técnicos

Cómo identificar con precisión los puntos clave del cuerpo humano en diferentes tipos de cuerpo y ángulos

Cómo distinguir diferencias sutiles de movimiento (postura correcta vs. incorrecta)

Cómo convertir indicadores cuantitativos en retroalimentación en lenguaje natural fácil de entender

Cómo lograr procesamiento en tiempo real para garantizar la experiencia del usuario

2. Descripción de la Solución

Este sistema adopta una arquitectura inteligente multi-módulo que integra las tres tecnologías centrales del curso de sistemas inteligentes:

2.1 Arquitectura del Sistema

[Entrada de Cámara] 
    ↓
[Módulo 1: Visión por Computador - Detección de Postura]
    ↓ (Coordenadas de puntos clave + características de ángulo)
[Módulo 2: Aprendizaje Automático - Clasificación de Movimientos]
    ↓ (Categoría de movimiento + confianza)
[Módulo 3: Lógica Difusa - Generación de Retroalimentación]
    ↓
[Interfaz de Usuario - Visualización de Retroalimentación en Tiempo Real]

2.2 Módulo 1: Visión por Computador (Visión Artificial)

Tecnología: OpenCV + MediaPipe/OpenPose

Funciones:

Captura en tiempo real del flujo de video de la cámara

Detección de puntos clave del esqueleto del cuerpo humano (33 puntos clave, incluyendo hombros, codos, caderas, rodillas, tobillos, etc.)

Cálculo de ángulos clave:

Sentadillas: ángulo de la articulación de la rodilla, ángulo de la articulación de la cadera, ángulo de inclinación del torso

Flexiones: ángulo de la articulación del codo, ángulo de la articulación del hombro, horizontalidad del cuerpo

Extracción de características de series temporales (velocidad, aceleración)

Salida:

Secuencia de coordenadas de puntos clave (x, y, z, visibility)

Datos de ángulos clave

Vector de características de trayectoria de movimiento

2.3 Módulo 2: Computación Evolutiva (Aprendizaje Automático - Computación Evolutiva)

Tecnología: Weka (Java) + Algoritmos Genéticos

Funciones:

Optimización de selección de características: Usar algoritmos genéticos para seleccionar el subconjunto óptimo de características de docenas de características candidatas

Codificación de cromosomas: Cadena binaria que representa si la característica está seleccionada

Función de aptitud: Precisión de clasificación - α×número de características (equilibrio entre precisión y complejidad)

Operaciones genéticas: Cruce de un punto, mutación, selección por ruleta

Optimización de parámetros del clasificador: Optimizar hiperparámetros de árboles de decisión/redes neuronales

Tasa de aprendizaje, número de nodos en capa oculta, umbral de poda

Clasificación de movimientos: Entrenar modelo de clasificación para identificar

Sentadilla correcta vs. rodillas hacia dentro vs. descenso insuficiente vs. centro de gravedad hacia adelante

Flexión correcta vs. espalda hundida vs. glúteos demasiado altos vs. ángulo de brazos incorrecto

Salida:

Etiqueta de categoría de movimiento

Confianza de clasificación

Tipo de error (si se detecta error)

2.4 Módulo 3: Lógica Difusa (Lógica Borrosa)

Tecnología: JFuzzyLogic (Java)

Función: Convertir indicadores cuantitativos en retroalimentación en lenguaje natural

Definición de variables difusas:

1. Velocidad de ejercicio (velocidad):

Entrada: Tiempo de completar cada movimiento (segundos)

Conjuntos difusos: {muy_lento, lento, normal, rápido, muy_rápido}

Función de pertenencia: Trapezoidal/triangular

2. Amplitud del movimiento (amplitud):

Entrada: Ángulo mínimo de articulación (grados)

Conjuntos difusos: {insuficiente, parcial, adecuada, completa}

3. Estabilidad del movimiento (estabilidad):

Entrada: Varianza de temblor de puntos clave

Conjuntos difusos: {inestable, moderada, estable}

4. Nivel de fatiga (fatiga):

Entrada: Tasa de disminución de velocidad, tasa de disminución de calidad del movimiento

Conjuntos difusos: {fresco, ligera, moderada, alta}

Salida:

Retroalimentación textual

Puntuación (0-10 puntos)

Sugerencias de mejora

2.5 Integración e Interfaz de Usuario

Pipeline de procesamiento en tiempo real: Usar procesamiento multi-hilo para garantizar fluidez de 30fps

Visualización: Superponer esqueleto, anotaciones de ángulos y texto de retroalimentación en la imagen de video

Panel de estadísticas: Mostrar número de repeticiones, velocidad promedio, curvas de rendimiento histórico

3. Descripción de los Datos de Entrada

3.1 Recopilación de Datos

Dataset Propio:

Captura de video: Usar cámara web ordinaria (720p, 30fps)

Escenario de captura: Ambiente interior con buena iluminación, distancia de 2-3 metros de la cámara

Sujetos de captura: Miembros del grupo (diferentes géneros, tipos de cuerpo, edades)

Tipos de movimientos:

Sentadillas: 200 muestras

Flexiones: 200 muestras

Estrategia de anotación:

Cada muestra de video se anota con:

Categoría de movimiento: Sentadilla/Flexión

Corrección: Correcto/Incorrecto

Tipo de error: (si aplica) rodillas hacia dentro, espalda hundida, amplitud insuficiente, etc.

Fotogramas clave: Anotar fotogramas de inicio, punto más bajo y final del movimiento

3.2 Complemento con Datasets Públicos

Considerar el uso de los siguientes datasets públicos para pre-entrenamiento o aumento de datos:

MPII Human Pose Dataset: Datos de anotación de postura humana

Fitness Activity Recognition Dataset: Datos de reconocimiento de movimientos de fitness

Videos de fitness de YouTube: Videos públicos filtrados y anotados

3.3 Ingeniería de Características

Características extraídas de los puntos clave originales (aproximadamente 50 dimensiones):

Características geométricas:

Ángulos de articulaciones (codo, rodilla, cadera, hombro, etc.)

Proporciones de longitud de partes del cuerpo

Distancias entre puntos clave

Características de movimiento:

Velocidad angular, velocidad lineal

Aceleración

Suavidad de la trayectoria de movimiento

Características temporales:

Ciclo de movimiento

Proporción de tiempo de cada fase

Tasa de cambio de velocidad

3.4 Preprocesamiento de Datos

Normalización: Ajustar coordenadas según la altura para eliminar diferencias de tipo de cuerpo

Suavizado: Usar filtro de Kalman para reducir el temblor de puntos clave

Aumento de datos: Volteo de espejo, rotación ligera, cambio de velocidad

4. Estado del Arte / Bibliografía

4.1 Estimación de Postura Humana

Tecnologías relacionadas:

OpenPose (CMU, 2017): Estimación de postura 2D multi-persona en tiempo real, usando campos de afinidad de partes (PAF)

MediaPipe Pose (Google, 2020): Detección de postura ligera, adecuada para dispositivos móviles y aplicaciones en tiempo real

AlphaPose (2018): Estimación de postura multi-persona de alta precisión

Elección de este proyecto: MediaPipe Pose

Ventajas: Buena capacidad en tiempo real, alta precisión, fácil integración con OpenCV

Desventajas: Detección de una sola persona (se ajusta a nuestro escenario de aplicación)

4.2 Reconocimiento y Clasificación de Movimientos

Investigaciones relacionadas:

ST-GCN (Spatial Temporal Graph CNN): Reconocimiento de movimientos basado en esqueleto

Enfoques basados en LSTM: Usar redes neuronales recurrentes para procesar datos temporales

Aprendizaje automático tradicional: SVM, Random Forest, Decision Trees

Elección de este proyecto:

Usar Weka para implementar métodos de aprendizaje automático tradicionales (árboles de decisión, Naive Bayes)

Optimizar selección de características y parámetros del modelo mediante algoritmos genéticos

Razón: Cumple con los requisitos del curso (computación evolutiva) y tiene buenos resultados en datasets de pequeña escala

4.3 Referencias Bibliográficas

1. Cao, Z., et al. (2017). "Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields". CVPR.

2. Bazarevsky, V., et al. (2020). "BlazePose: On-device Real-time Body Pose tracking". arXiv:2006.10204.

3. Goldberg, D. E. (1989). "Genetic Algorithms in Search, Optimization, and Machine Learning". Addison-Wesley.

4. Zadeh, L. A. (1965). "Fuzzy Sets". Information and Control, 8(3), 338-353.

5. Cilla, R., et al. (2013). "JFuzzyLogic: a Java Library to Design Fuzzy Logic Controllers". IEEE International Conference on Fuzzy Systems.

6. Weka Documentation: https://www.cs.waikato.ac.nz/ml/weka/

7. OpenCV Documentation: https://docs.opencv.org/


