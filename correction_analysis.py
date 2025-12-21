import cv2
import numpy as np
import pickle
import json
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report

# Configuración
DATA_DIR = Path("data")
GT_FILE = "ground_truth.json"
PLAZAS_FILE = "plazas.pickle"
MODEL_FILE = "model.pkl"

def cargar_datos():
    # 1. Cargar Plazas (ROIs)
    if not Path(PLAZAS_FILE).exists():
        raise FileNotFoundError(f"Falta {PLAZAS_FILE}")
    with open(PLAZAS_FILE, 'rb') as f:
        plazas = pickle.load(f)
        
    # 2. Cargar Etiquetas
    if not Path(GT_FILE).exists():
        raise FileNotFoundError(f"Falta {GT_FILE}")
    with open(GT_FILE, 'r') as f:
        ground_truth = json.load(f)
        
    return plazas, ground_truth

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    return blur

def extract_features(roi_gray, roi_binary, roi_color):
    pixels = cv2.countNonZero(roi_binary)
    match_mean, match_std = cv2.meanStdDev(roi_gray)
    texture = match_std[0][0]
    hsv = cv2.cvtColor(roi_color, cv2.COLOR_BGR2HSV)
    s_mean, s_std = cv2.meanStdDev(hsv[:,:,1])
    saturation = s_mean[0][0]
    return [pixels, texture, saturation]

def main():
    print("🚀 Iniciando análisis de corrección de Data Leakage (y generación de modelo)...")
    
    plazas, ground_truth = cargar_datos()
    
    # Ordenar cronológicamente las imágenes
    sorted_image_names = sorted(ground_truth.keys())
    print(f"✅ Total imágenes etiquetadas: {len(sorted_image_names)}")
    
    X = []
    y = []

    print("⏳ Extrayendo características (orden cronológico)...")
    for img_name in sorted_image_names:
        img_path = DATA_DIR / img_name
        labels = ground_truth[img_name]
        if not img_path.exists(): continue
        
        image = cv2.imread(str(img_path))
        processed = preprocess_image(image)
        binary = cv2.adaptiveThreshold(processed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY_INV, 25, 15)
        binary = cv2.medianBlur(binary, 5)

        for idx, rect in enumerate(plazas):
            if idx >= len(labels): break
            x, y_pos, w, h = rect
            
            roi_gray = processed[y_pos:y_pos+h, x:x+w]
            roi_binary = binary[y_pos:y_pos+h, x:x+w]
            roi_color = image[y_pos:y_pos+h, x:x+w]
            
            features = extract_features(roi_gray, roi_binary, roi_color)
            label = labels[idx]
            
            X.append(features)
            y.append(label)

    X = np.array(X)
    y = np.array(y)
    
    print(f"✅ Extracción completada. Total muestras: {len(X)}")

    # 4. Preparar Datos (Escalar)
    print("⚖️ Escalando datos...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 5. Split Cronológico 80/20
    split_idx = int(len(X) * 0.8)
    X_train = X_scaled[:split_idx]
    X_test = X_scaled[split_idx:]
    y_train = y[:split_idx]
    y_test = y[split_idx:]
    
    print(f"📊 División Cronológica:")
    print(f"   - Train: {len(X_train)} muestras (80%)")
    print(f"   - Test:  {len(X_test)} muestras (20%)")

    # 6. Entrenar SVM
    print("🧠 Entrenando SVM...")
    model = SVC(kernel='rbf', C=1.0, gamma='scale', probability=True, random_state=42)
    model.fit(X_train, y_train)
    print("✅ Entrenamiento finalizado.")

    # 7. Evaluar
    print("-" * 30)
    print("📝 Resultados de Evaluación (Test Set):")
    y_pred = model.predict(X_test)
    
    print(classification_report(y_test, y_pred, target_names=['Libre', 'Ocupado']))
    
    cm = confusion_matrix(y_test, y_pred)
    print(f"Confusion Matrix:\n{cm}")

    # 8. Guardar Modelo
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump({'model': model, 'scaler': scaler}, f)
    print(f"\n💾 Modelo y Scaler guardados en {MODEL_FILE}")

if __name__ == "__main__":
    main()
