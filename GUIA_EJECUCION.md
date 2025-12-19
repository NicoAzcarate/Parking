# 🚀 Guía de Ejecución Paso a Paso - Detector de Plazas

## ✅ Requisitos Previos

- Python 3.8 o superior instalado
- Acceso a terminal/PowerShell
- Dataset de imágenes en la carpeta `data/`

---

## 📋 PASO 1: Crear Entorno Virtual (venv)

### Abrir PowerShell en el directorio del proyecto

```powershell
cd "C:\Users\nico.azcarate\Desktop\Vision por Computador"
```

### Crear el entorno virtual

```powershell
python -m venv venv
```

Esto creará una carpeta `venv/` con el entorno aislado.

### Activar el entorno virtual

```powershell
.\venv\Scripts\Activate
```

**Indicador de éxito**: Verás `(venv)` al principio de tu línea de comandos:
```
(venv) PS C:\Users\nico.azcarate\Desktop\Vision por Computador>
```

---

## 📦 PASO 2: Instalar Dependencias

Con el venv activado, instala las librerías necesarias:

```powershell
pip install opencv-python numpy matplotlib jupyter
```

**Tiempo estimado**: 1-2 minutos

### Verificar instalación

```powershell
python verificar_proyecto.py
```

**Salida esperada**:
```
✅ OpenCV: 4.x.x
✅ NumPy: 1.x.x
✅ Matplotlib: 3.x.x
✅ Pickle: built-in module
✅ Pathlib: built-in module
...
🎉 ¡Todo listo! El proyecto está correctamente configurado.
```

---

## 🎯 PASO 3: Configurar Plazas (OFFLINE - Una sola vez)

Este paso define las 51 plazas de aparcamiento que se van a monitorizar.

```powershell
python configurar_plazas.py
```

### Instrucciones Interactivas:

1. **Se abre una ventana** con la primera imagen del parking
2. **Dibuja los rectángulos**:
   - **Click izquierdo + arrastrar**: Dibujar cada plaza
   - **'r'**: Eliminar último rectángulo (si te equivocas)
   - Repite hasta tener **51 rectángulos**
3. **Guardar configuración**:
   - Presiona **'s'** cuando termines
   - Se creará el archivo `plazas.pickle`

**🎯 Consejos**:
- Dibuja plazas en la zona **central-derecha** del parking
- Evita zonas con árboles o bordes del frame
- Los rectángulos deben cubrir completamente cada plaza

**Resultado**: Archivo `plazas.pickle` creado ✅

---

## 📓 PASO 4: Ejecutar el Notebook Principal

### Iniciar Jupyter Notebook

```powershell
jupyter notebook
```

Esto abrirá tu navegador web con Jupyter.

### En el navegador:

1. **Abre el archivo**: `detector_aparcamiento.ipynb`
2. **Ejecuta las celdas en orden**:

---

### 📊 Celdas a Ejecutar (En orden)

#### **Celdas 1-2: Setup inicial**
- Click en la primera celda
- Presiona **Shift + Enter** para ejecutar
- Repite con la segunda celda
- **Resultado**: Carga de librerías y configuración

#### **Celdas 3-5: Definición de funciones**
- Ejecuta cada celda con **Shift + Enter**
- **Resultado**: Funciones del pipeline listas

#### **Celda 6: Prueba con imagen individual** ⭐ IMPORTANTE
- Ejecuta esta celda
- **Resultado**: Verás 3 imágenes:
  1. **Imagen original**
  2. **Imagen binaria procesada** (blanco y negro)
  3. **Detección con rectángulos verdes/rojos**
  
**✅ Si ves las detecciones, el sistema funciona correctamente!**

---

### 🎛️ PASO 5 (OPCIONAL): Calibración Interactiva

Si quieres ajustar los parámetros para mejor precisión:

#### **Celda 8: Sistema de calibración**

1. **Descomenta** las líneas de la celda 8:
   ```python
   # parametros_optimizados = calibrar_parametros(test_image_path, plazas)
   # print(f"\nParámetros guardados: {parametros_optimizados}")
   ```
   
   Cambiar a:
   ```python
   parametros_optimizados = calibrar_parametros(test_image_path, plazas)
   print(f"\nParámetros guardados: {parametros_optimizados}")
   ```

2. **Ejecuta la celda** (Shift + Enter)

3. **Se abrirán 3 ventanas de OpenCV**:
   - **Controles**: Con 3 barras deslizantes
   - **Calibración - Resultado**: Vista con detecciones
   - **Calibración - Binaria**: Vista procesada

4. **Ajusta las barras** hasta que las detecciones sean correctas:
   - **Umbral Píxeles**: 300-900 (más alto = más restrictivo)
   - **Block Size**: 11-51 (impar, ventana de análisis)
   - **C Constant**: 3-10 (ajuste fino)

5. **Presiona 'q'** para salir y guardar parámetros

**🎯 Recomendación**: Calibra con una imagen que tenga **sol Y sombra** juntos (la más difícil).

---

### 📦 PASO 6 (OPCIONAL): Procesamiento por Lotes

Para procesar todas las ~438 imágenes:

#### **Celda 10: Batch processing**

1. **Descomenta** el código:
   ```python
   stats, libres_por_imagen = procesar_dataset(
       "data",
       plazas,
       output_dir="resultados",
       umbral_pixeles=500,  # Usa los valores de calibración si los tienes
       block_size=21,
       C=5,
       show_counts=False
   )
   ```

2. **Ejecuta la celda**

3. **Espera** (puede tardar 2-5 minutos para 438 imágenes)

4. **Resultado**: Carpeta `resultados/` con todas las imágenes procesadas

---

### 📊 PASO 7 (OPCIONAL): Validación con Métricas

Para obtener métricas académicas rigurosas:

#### A. Seleccionar 3 imágenes representativas (Celda 11)

**Ejecuta la celda** para ver las imágenes seleccionadas automáticamente.

**Mejor opción**: Revisa manualmente las imágenes y selecciona:
- **Imagen A**: Parking completamente al sol
- **Imagen B**: Mitad sol / mitad sombra (la más desafiante)
- **Imagen C**: Parking en sombra o nublado

#### B. Etiquetar Ground Truth (Celda 12)

Necesitas **etiquetar manualmente** el estado real de cada plaza:

1. Abre cada imagen de validación
2. Para cada una de las 51 plazas, anota:
   - `"OCUPADO"` si hay vehículo
   - `"LIBRE"` si está vacía

**Ejemplo de formato**:
```python
ground_truth['A_Sol'] = [
    "OCUPADO", "LIBRE", "OCUPADO", "LIBRE", "OCUPADO",
    "OCUPADO", "LIBRE", "LIBRE", "OCUPADO", "LIBRE",
    # ... (hasta 51 valores)
]
```

#### C. Calcular métricas (Celda 13)

1. **Descomenta** el código de validación
2. **Ejecuta la celda**
3. **Resultado**: Matriz de confusión y Accuracy para cada imagen

**Métricas generadas**:
- TP (True Positives)
- TN (True Negatives)
- FP (False Positives)
- FN (False Negatives)
- **Accuracy** (%)

---

## 🎯 RESUMEN DE COMANDOS (Flujo Completo)

```powershell
# 1. Navegar al proyecto
cd "C:\Users\nico.azcarate\Desktop\Vision por Computador"

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
.\venv\Scripts\Activate

# 4. Instalar dependencias
pip install opencv-python numpy matplotlib jupyter

# 5. Verificar instalación
python verificar_proyecto.py

# 6. Configurar plazas (interactivo)
python configurar_plazas.py

# 7. Iniciar Jupyter
jupyter notebook

# Luego en el navegador: Abrir detector_aparcamiento.ipynb y ejecutar celdas
```

---

## ⚠️ Solución de Problemas

### Problema: "python no se reconoce como comando"

**Solución**: Asegúrate de que Python está en el PATH o usa:
```powershell
py -m venv venv
py -m pip install opencv-python numpy matplotlib jupyter
```

### Problema: Error al activar venv

**Solución**: Si PowerShell no permite ejecutar scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Luego intenta activar de nuevo.

### Problema: OpenCV no muestra ventanas

**Solución**: Asegúrate de que `opencv-python` está instalado (no `opencv-python-headless`):
```powershell
pip uninstall opencv-python-headless
pip install opencv-python
```

### Problema: Jupyter no abre navegador

**Solución**: Copia la URL que aparece en el terminal y pégala manualmente en tu navegador.

---

## 📝 Checklist de Ejecución

- [ ] ✅ Venv creado y activado
- [ ] ✅ Dependencias instaladas
- [ ] ✅ `verificar_proyecto.py` ejecutado exitosamente
- [ ] ✅ `configurar_plazas.py` ejecutado → `plazas.pickle` creado
- [ ] ✅ Jupyter notebook iniciado
- [ ] ✅ Celdas 1-6 ejecutadas → Vista de detección funcionando
- [ ] ⚙️ (Opcional) Calibración realizada
- [ ] 📦 (Opcional) Batch processing completado
- [ ] 📊 (Opcional) Validación con métricas

---

## 💡 Consejos Finales

1. **Siempre activa el venv** antes de trabajar:
   ```powershell
   .\venv\Scripts\Activate
   ```

2. **Desactivar venv** cuando termines:
   ```powershell
   deactivate
   ```

3. **Guardar parámetros óptimos**: Anota los valores que funcionen mejor después de calibrar.

4. **Para la memoria académica**: Toma screenshots de:
   - Resultado de detección (celda 6)
   - Imagen binaria procesada
   - Métricas de validación

---

## 🎓 Para la Defensa del Proyecto

Prepara explicaciones de:
- ¿Por qué adaptive threshold y no Otsu? → Robustez a sombras
- ¿Por qué grayscale? → Reduce datos, color no es determinante
- ¿Complejidad computacional? → O(N) lineal
- ¿Métricas obtenidas? → Accuracy en diferentes condiciones

---

**¡Éxito con tu proyecto!** 🚀
