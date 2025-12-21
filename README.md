# 🚗 Detector de Plazas de Aparcamiento (Smart ML)

Sistema inteligente de Visión por Computador para la detección de plazas de aparcamiento libres y ocupadas, utilizando **Machine Learning (SVM)** para adaptarse a condiciones de iluminación cambiantes.

## 📋 Descripción del Proyecto

A diferencia de los sistemas tradicionales basados en sustracción de fondo o umbrales fijos, este proyecto utiliza un clasificador **Support Vector Machine (SVM)** entrenado con características robustas (Textura, Bordes y Color) para distinguir vehículos del asfalto.

### Características Principales
- **Precisión**: 99.51% de acierto global en el conjunto de prueba.
- **Robustez**: Funciona en días soleados, nublados y con sombras proyectadas.
- **Eficiencia**: Procesamiento rápido.
- **Escalabilidad**: Fácil de re-entrenar con nuevas imágenes.

## 🛠️ Tecnologías Utilizadas

- **OpenCV**: Procesamiento de imágenes y extracción de ROIs.
- **Scikit-Learn**: Implementación del clasificador SVM (Kernel RBF).
- **Python**: Lenguaje base.
- **Jupyter Notebook**: Entorno de desarrollo interactivo.

## 🚀 Guía de Uso

### 1. Configuración Inicial (Si cambio de cámara/parking)
Para redefinir dónde están las plazas:
```bash
python configurar_plazas.py
```
*Dibujar rectángulos sobre las plazas. Presionar 's' para guardar.*

### 2. Entrenamiento del Modelo
Para mejorar el sistema con más datos o ver cómo aprende:
Ejecutar `03_ML.ipynb`.
*Esto generará un nuevo archivo `model.pkl`.*

### 3. Ejecutar el Detector (Demo)
Para ver el sistema en acción y las métricas de rendimiento:
Ejecutar `04_Resultados.ipynb`.

## 🧠 Cómo funciona (El Algoritmo)

El sistema no "mira" la imagen como un humano, sino que extrae 3 descriptores clave de cada plaza:

1.  **Densidad de Bordes (Canny)**: Los coches tienen muchas líneas y formas; el asfalto vacío es plano.
2.  **Varianza de Textura**: Mide qué tan "rugosa" o variada es la imagen en esa zona.
3.  **Saturación de Color (HSV)**: El asfalto es gris (baja saturación); los coches suelen tener colores más vivos.

Estos 3 números forman un vector que el SVM clasifica como `0` (Libre) o `1` (Ocupado).

## 📊 Resultados

| Métrica | Valor |
|---------|-------|
| **Accuracy** | **99.51%** |
| Precision (Libres) | 100% |
| Recall (Ocupados) | 100% |

> *Datos obtenidos sobre el conjunto de validación del proyecto (ver `04_Resultados.ipynb`).*
