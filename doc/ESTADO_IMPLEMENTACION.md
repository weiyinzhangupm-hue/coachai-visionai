# Estado de implementación

Referencia de código: `b0696d4522275503751a05d5a7b3320ef42cf461` del [repositorio original](https://gitlab.etsisi.upm.es/bq0073/virtual-trainer).

Estas notas describen el código disponible y las comprobaciones realizadas durante la preparación del portfolio. El documento Word conserva el diseño original; no constituye una lista de funcionalidades verificadas.

## Recorrido por defecto

`python/main.py` abre una cámara, detecta la postura, calcula ángulos, actualiza el contador y presenta resultados en una ventana OpenCV. Crea `HybridClassifier(use_ml=False)` y solicita una evaluación aproximadamente cada dos segundos.

`HybridClassifier` delega en `RuleBasedClassifier`. La carga de un modelo ML y su predicción están pendientes (`TODO`); cambiar únicamente `use_ml=True` no completa esa integración.

## Componentes adicionales

- `java/`: código para clasificación Weka, selección genética de características, entrenamiento y lógica borrosa con jFuzzyLogic.
- `flask_api/`: capa de API y puente para invocar Java. No se inicia desde la aplicación Python principal.
- `models/`: no contiene un modelo entrenado.
- `dataset/`: incluye documentación, pero no un dataset completo de entrenamiento y evaluación.

No se ha verificado el recorrido Java/API de extremo a extremo. Faltan los JAR externos en esta copia; el classpath del puente también requiere revisión para Windows, donde el separador es distinto al de Unix.

## Comprobaciones realizadas · 20 de octubre de 2026

- Análisis sintáctico correcto de los 18 archivos Python.
- Comprobaciones sin cámara: cálculo de un ángulo recto, clasificación de entradas sintéticas de sentadilla y flexión, rango de puntuación y generación de feedback.
- Inspección de fotogramas del vídeo original de unos 14 segundos: muestra seguimiento de postura, conteo de sentadillas y panel de evaluación.
- El script original de pruebas de extracción de características no pudo ejecutarse en el entorno de revisión porque no estaba instalado `scikit-learn`. No se presenta como prueba superada.

No se ha realizado una instalación limpia de todas las dependencias ni una sesión nueva con cámara. Las comprobaciones anteriores no equivalen a una evaluación de precisión o rendimiento del sistema.

## Documentación histórica

Se conserva la documentación original de `doc/` como contexto de la entrega académica. Las cifras estimadas, planes de dataset y objetivos que aparezcan en esos documentos no se presentan en el README como mediciones verificadas.
