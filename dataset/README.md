# descripción del conjunto de datos

Este directorio se utiliza para almacenar los datos de entrenamiento y de prueba.


## estructura de directorios

```
dataset/
├── raw/                   # datos de vídeo originales

│   ├── squat/             # acción Squat
│   │   ├── correct/       # ejecución correcta
│   │   └── incorrect/     # ejecución incorrecta
│   └── pushup/            # acción Pushup
│       ├── correct/       # ejecución correcta
│       └── incorrect/     # ejecución incorrecta
├── processed/             # datos de características procesadas
├── train.csv              # conjunto de entrenamiento
├── test.csv               # conjunto de prueba
└── README.md              # este archivo
```

## Guía de recopilación de datos

### 1. Uso de la herramienta de recopilación de datos

```bash
cd python
python data_collector.py
```

### 2. Requisitos de recopilación

#### Squat (Squat)
**Ejecución correcta:**:
- Pies separados al ancho de los hombros
- Las rodillas no sobrepasan la punta de los pies
- Espalda recta
- Descenso hasta que los muslos queden paralelos al suelo

**Errores comunes:**:
- Rodillas hacia dentro (knee_valgus)
- Profundidad insuficiente (insufficient_depth)
- Inclinación excesiva del tronco hacia delante (forward_lean)

#### Pushup (Pushup)
**Ejecución correcta:**:
- El cuerpo mantiene una línea recta
- Brazos ligeramente más abiertos que el ancho de los hombros
- Descenso hasta que los codos alcancen 90 grados
- Core activado durante todo el movimiento

**Errores comunes:**:
- Hundimiento de la zona lumbar (sagging_back) (sagging_back)
- Caderas demasiado elevadas(high_hips)
- Ángulo incorrecto de los brazos (wrong_arm_angle)

### 3. Recomendaciones de recopilación

**Cantidad mínima:**:
- Al menos 30 muestras correctas por cada tipo de ejercicio
- Al menos 20 muestras por cada tipo de error
- Objetivo total: 400 muestras

**Requisitos de calidad:**:
- Todo el cuerpo debe aparecer dentro del campo de visión de la cámara
- Iluminación adecuada, evitando contraluces
- Fondo sencillo para reducir interferencias
- Grabación desde múltiples ángulos (frontal y lateral)
- Participación de varias personas (diferentes complexiones físicas)

**Normas de etiquetado:**:
- Etiquetar correctamente el tipo de ejercicio
- Indicar claramente si la ejecución es correcta o incorrecta
- Especificar el tipo de error cuando corresponda
- Conservar tanto los vídeos originales como los datos de características

## Formato de los datos

### Datos originales
Cada sesión de recopilación genera:
- `.mp4` - archivo de vídeo original
- `_features.json` - datos de características extraídas

### Datos procesados
Formato de los archivos CSV:
```csv
angle_knee_avg,angle_hip_avg,shoulder_width,trunk_length,...,label
120.5,85.3,0.15,0.25,...,squat_correct
95.2,110.5,0.16,0.24,...,squat_knee_valgus
...
```

## Descripción de las características

### Características geométricas
- Ángulos articulares (rodilla, cadera, codo, hombro)
- Proporciones corporales (ancho de hombros, ancho de caderas, longitud del tronco)
- Relaciones de longitud entre extremidades

### Características de movimiento
- Velocidad angular y aceleración
- Ciclo del movimiento
- Suavidad del movimiento
### Características temporales
- Rango de variación de los ángulos
- Media y desviación estándar de la velocidad
- Características derivadas de la aceleración

## Preprocesamiento de datos

Ejecutar el script de extracción de características:

```bash
python python/feature_extractor.py \
    --input dataset/raw \
    --output dataset/processed \
    --normalize
```

## Aumento de datos

Métodos opcionales de data augmentation:
1. Volteo horizontal (simetría izquierda-derecha)
2. Variación de velocidad (0.8x – 1.2x)
3. Rotación ligera (±5 grados)

## Consideraciones importantes

- ⚠️ Los vídeos originales son archivos grandes y no deben subirse a Git
- ✅ Subir únicamente los archivos CSV con las características procesadas
- ✅ Mantener la coherencia en el etiquetado
- ✅ Realizar copias de seguridad de los datos periódicamente

## Estado actual del conjunto de datos

- [ ] Squat correcto: 0/30
- [ ] Squat knee_valgus: 0/20
- [ ] Squat insufficient_depth: 0/20
- [ ] Squat forward_lean: 0/20
- [ ] Pushup correcto: 0/30
- [ ] Pushup sagging_back: 0/20
- [ ] Pushup high_hips: 0/20
- [ ] Pushup wrong_arm_angle: 0/20

**Progreso total:**: 0/180 (0%)

---

Fecha de actualización: 2026-1-25

