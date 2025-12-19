# 🚗 Detector de Plazas de Aparcamiento

Sistema de visión artificial para monitorizar en tiempo real el estado (Libre/Ocupado) de plazas de aparcamiento usando técnicas de **Computer Vision Clásica**.

## 📋 Descripción del Proyecto

Este proyecto implementa un detector robusto capaz de:
- ✅ Monitorizar ~51 plazas de aparcamiento simultáneamente
- ✅ Funcionar bajo condiciones drásticas de iluminación (sol y sombra)
- ✅ Ejecutarse en tiempo real sin requerir GPU
- ✅ Proporcionar explicaciones matemáticas de cada decisión

### ¿Por qué Computer Vision Clásica y no Deep Learning?

1. **Eficiencia Computacional**: Complejidad O(N) - no requiere entrenamiento ni GPU
2. **Explicabilidad**: Cada decisión es matemáticamente trazable
3. **Robustez**: Adaptive thresholding es inherentemente robusto a cambios de luz
4. **Simplicidad**: No requiere datasets etiquetados ni hyperparameter tuning extensivo

## 🛠️ Instalación

### Requisitos

```bash
pip install opencv-python numpy matplotlib jupyter
```

### Verificación

```python
import cv2
print(f"OpenCV version: {cv2.__version__}")
```

## 🚀 Uso Rápido

### **Paso 1: Configurar las Plazas (Offline)**

Este paso se hace **una sola vez** para definir las 51 ROIs (Regiones de Interés).

```bash
python configurar_plazas.py
```

**Controles**:
- **Click izquierdo + arrastrar**: Dibujar rectángulo para cada plaza
- **'r'**: Eliminar último rectángulo
- **'s'**: Guardar configuración
- **'q'**: Salir sin guardar

**Salida**: Archivo `plazas.pickle` con las coordenadas de las 51 plazas.

---

### **Paso 2: Ejecutar Detección (Online)**

Abre el notebook principal:

```bash
jupyter notebook detector_aparcamiento.ipynb
```

**Flujo de trabajo**:

1. **Ejecutar Celdas 1-5**: Importar librerías y cargar configuración
2. **Ejecutar Celda 6**: Probar con una imagen individual
3. **Ejecutar Celda 8** (Opcional): Calibrar parámetros de forma interactiva
4. **Ejecutar Celda 10** (Opcional): Procesar todo el dataset por lotes

---

## 📊 Pipeline de Procesamiento

```
Imagen BGR → Grayscale → Gaussian Blur → Adaptive Threshold → Median Filter → Classification → Visualization
```

### Explicación Técnica

#### 1️⃣ **Preprocesamiento**
- **Grayscale**: Reduce datos a 1/3 (1 canal vs 3 RGB)
- **Gaussian Blur (5x5)**: Elimina ruido de alta frecuencia

#### 2️⃣ **Segmentación Adaptativa**
```python
cv2.adaptiveThreshold(
    img, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    block_size=21,  # Tamaño de vecindad local
    C=5             # Constante de ajuste
)
```

**¿Por qué Adaptive?**
- Un umbral global fallaría: zonas de sol serían blancas, zonas de sombra negras
- Adaptive calcula el umbral **por vecindad**, ignorando iluminación global
- **Plaza Vacía (Asfalto)**: Textura lisa → Pocos píxeles blancos
- **Plaza Ocupada (Coche)**: Bordes/ventanas → Muchos píxeles blancos

#### 3️⃣ **Post-Procesamiento**
- **Median Blur (5x5)**: Elimina "ruido de sal" del asfalto viejo

#### 4️⃣ **Clasificación**
```python
pixel_count = cv2.countNonZero(roi)
if pixel_count > UMBRAL:
    estado = "OCUPADO"
else:
    estado = "LIBRE"
```

---

## 🎛️ Calibración de Parámetros

El notebook incluye un sistema interactivo con **trackbars** para ajustar:

| Parámetro | Descripción | Rango Típico |
|-----------|-------------|--------------|
| **Umbral de Píxeles** | Cantidad de píxeles blancos para considerar "OCUPADO" | 300-900 |
| **Block Size** | Tamaño de ventana para adaptive threshold | 11-51 (impar) |
| **C Constant** | Ajuste fino de sensibilidad | 3-10 |

**Recomendado**: Calibrar con una imagen que tenga mitad sol / mitad sombra.

---

## 📈 Validación y Métricas

### Selección de Imágenes de Prueba

Selecciona 3 imágenes representativas:
- **Imagen A**: Sol completo (condición fácil)
- **Imagen B**: Mitad sol / mitad sombra (condición difícil)
- **Imagen C**: Nublado/sombra (condición intermedia)

### Matriz de Confusión

Para cada imagen de prueba, etiqueta manualmente el ground truth y calcula:

| Métrica | Fórmula | Descripción |
|---------|---------|-------------|
| **TP** | True Positive | Plaza ocupada detectada correctamente |
| **TN** | True Negative | Plaza libre detectada correctamente |
| **FP** | False Positive | Sistema dice OCUPADO pero está LIBRE ⚠️ |
| **FN** | False Negative | Sistema dice LIBRE pero hay coche ⚠️ |

### Accuracy

$$\text{Accuracy} = \frac{TP + TN}{\text{Total Plazas}} \times 100$$

**Objetivo**: 
- ≥90% en condiciones uniformes
- ≥80% en condiciones mixtas sol/sombra

---

## 📁 Estructura del Proyecto

```
Vision por Computador/
│
├── data/                          # ~440 imágenes del parking
│   ├── 2012-09-11_15_53_00_...jpg
│   ├── 2012-09-11_16_48_36_...jpg
│   └── ...
│
├── configurar_plazas.py           # Script offline para definir ROIs
├── detector_aparcamiento.ipynb    # Notebook principal con pipeline
├── plazas.pickle                  # Archivo generado con coordenadas
├── resultados/                    # (Opcional) Salida del batch processing
│   └── resultado_*.jpg
│
└── README.md                      # Este archivo
```

---

## 🎓 Justificaciones Técnicas (Para la Memoria)

### 1. **Selección del ROI**
> "Se monitorizaron 51 plazas en la zona central-derecha, descartando las plazas perimetrales para evitar errores por oclusión parcial (árboles) y distorsión de lente en los bordes del frame."

### 2. **Adaptive Threshold vs. Otsu**
> "Frente a métodos globales como Otsu, se eligió umbralización adaptativa para mitigar el fuerte contraste provocado por las sombras de los edificios. Esto permite que cada píxel se compare con su vecindad inmediata, no con el promedio global de la imagen."

### 3. **Complejidad Computacional**
> "El algoritmo propuesto tiene una complejidad O(N) (lineal con el número de píxeles), permitiendo su ejecución en tiempo real en hardware modesto sin requerir aceleración por GPU."

---

## 🔧 Parámetros Recomendados por Condición

| Condición | Umbral Píxeles | Block Size | C |
|-----------|----------------|------------|---|
| **Sol completo** | 400-600 | 15-21 | 4-6 |
| **Mixto sol/sombra** | 500-700 | 21-31 | 5-7 |
| **Nublado/sombra** | 600-900 | 25-35 | 6-8 |

*Nota: Estos son valores iniciales, ajusta según tu dataset específico.*

---

## ⚠️ Limitaciones Conocidas

1. **Vehículos pequeños**: Motos o bicicletas pueden no generar suficiente textura
2. **Oclusiones parciales**: Vehículos mal estacionados pueden afectar plazas adyacentes
3. **Condiciones extremas**: Lluvia, nieve o niebla no fueron probadas en este dataset

---

## 🚀 Posibles Mejoras Futuras

- [ ] Ajuste automático de parámetros basado en hora del día
- [ ] Tracking temporal entre frames consecutivos
- [ ] Detección de líneas de parking para validación geométrica
- [ ] Exportar resultados a formato JSON/CSV para integración con sistemas

---

## 📚 Referencias Técnicas

- **Tema 3**: Filtrado (Gaussian Blur, Median Filter)
- **Tema 5**: Segmentación (Adaptive Thresholding)
- **OpenCV Documentation**: [Adaptive Threshold](https://docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html)

---

## 📝 Checklist de Completación

- [ ] Ejecutar `configurar_plazas.py` y guardar `plazas.pickle`
- [ ] Probar pipeline con imagen individual
- [ ] Calibrar parámetros con trackbars
- [ ] Seleccionar 3 imágenes de validación
- [ ] Etiquetar ground truth manualmente
- [ ] Calcular métricas (Accuracy, Precision, Recall)
- [ ] Documentar resultados en la memoria
- [ ] Preparar visualizaciones para la defensa

---

## 👤 Autor

**Proyecto Individual** - Fundamentos de Visión por Computador

---

## 📄 Licencia

Este proyecto es material académico para uso educativo.
