# 🚗 Detector de Plazas de Aparcamiento (Smart ML)

Sistema inteligente de Visión por Computador para la detección de plazas de aparcamiento libres y ocupadas, utilizando **Machine Learning (SVM)** para adaptarse a condiciones de iluminación cambiantes.

## 📋 Descripción del Proyecto

A diferencia de los sistemas tradicionales basados en sustracción de fondo o umbrales fijos, este proyecto utiliza un clasificador **Support Vector Machine (SVM)** entrenado con características robustas (Textura, Bordes y Color) para distinguir vehículos del asfalto.

### Características Principales
- **Precisión Realista**: ~98% de acierto global (evaluado cronológicamente).
- **Robustez**: Validación mediante *Chronological Split* para evitar "fugas de datos" y asegurar generalización real.
- **Eficiencia**: Procesamiento rápido.
- **Escalabilidad**: Fácil de re-entrenar con nuevas imágenes.

## 🛠️ Tecnologías Utilizadas

- **OpenCV**: Procesamiento de imágenes y extracción de ROIs.
- **Scikit-Learn**: Implementación del clasificador SVM (Kernel RBF).
- **Python**: Lenguaje base.
- **Jupyter Notebook**: Entorno de desarrollo interactivo.

## 🧠 Cómo funciona (El Algoritmo)

El sistema no "mira" la imagen como un humano, sino que extrae 3 descriptores clave de cada plaza:

1.  **Densidad de Bordes (Canny)**: Los coches tienen muchas líneas y formas; el asfalto vacío es plano.
2.  **Varianza de Textura**: Mide qué tan "rugosa" o variada es la imagen en esa zona.
3.  **Saturación de Color (HSV)**: El asfalto es gris (baja saturación); los coches suelen tener colores más vivos.

Estos 3 números forman un vector que el SVM clasifica como `0` (Libre) o `1` (Ocupado).

## 📊 Resultados (Evaluación Realista)

Se ha corregido la validación para usar una **División Cronológica** (80% pasado / 20% futuro), obteniendo métricas más honestas que evitan el *Data Leakage*:

| Métrica | Valor Realista | Antes (Inflado) |
|---------|----------------|-----------------|
| **Accuracy** | **~98%** | ~99.5% |
| Precision (Libres) | ~95% | 100% |
| Recall (Ocupados) | ~99% | 100% |

> *Datos obtenidos en `05_Correccion_DataLeakage.ipynb` simulando un entorno de producción real.*
