"""
Configurador de Plazas de Aparcamiento
======================================
Script offline para definir manualmente las 51 ROIs (Regiones de Interés)
del parking que se van a monitorizar.

Uso:
    python configurar_plazas.py

Controles:
    - Click izquierdo y arrastrar: Dibujar rectángulo
    - 'r': Eliminar último rectángulo
    - 's': Guardar y salir
    - 'q': Salir sin guardar
"""

import cv2
import pickle
from pathlib import Path
import numpy as np


class PlazaConfigurator:
    def __init__(self, image_path, output_file="plazas.pickle"):
        self.image_path = image_path
        self.output_file = output_file
        
        # Load image
        self.original_image = cv2.imread(str(image_path))
        if self.original_image is None:
            raise FileNotFoundError(f"No se pudo cargar la imagen: {image_path}")
        
        self.image = self.original_image.copy()
        self.plazas = []  # Lista de (x, y, w, h)
        
        # Drawing state
        self.drawing = False
        self.start_point = None
        self.current_rect = None
        
        # Window setup
        self.window_name = "Configurador de Plazas - {} plazas definidas"
        cv2.namedWindow(self.get_window_title())
        cv2.setMouseCallback(self.get_window_title(), self.mouse_callback)
    
    def get_window_title(self):
        return self.window_name.format(len(self.plazas))
    
    def mouse_callback(self, event, x, y, flags, param):
        """Callback para eventos del ratón"""
        if event == cv2.EVENT_LBUTTONDOWN:
            # Inicio de dibujo
            self.drawing = True
            self.start_point = (x, y)
            self.current_rect = None
        
        elif event == cv2.EVENT_MOUSEMOVE:
            # Dibujar rectángulo temporal mientras se arrastra
            if self.drawing:
                self.current_rect = (x, y)
        
        elif event == cv2.EVENT_LBUTTONUP:
            # Finalizar rectángulo
            if self.drawing and self.start_point:
                end_point = (x, y)
                
                # Calcular coordenadas normalizadas
                x1, y1 = self.start_point
                x2, y2 = end_point
                
                # Asegurar que x1,y1 sea la esquina superior izquierda
                x_min = min(x1, x2)
                y_min = min(y1, y2)
                width = abs(x2 - x1)
                height = abs(y2 - y1)
                
                # Agregar plaza si tiene área válida
                if width > 10 and height > 10:
                    self.plazas.append((x_min, y_min, width, height))
                    print(f"Plaza {len(self.plazas)} añadida: ({x_min}, {y_min}, {width}, {height})")
                
                self.drawing = False
                self.start_point = None
                self.current_rect = None
                
                # Actualizar ventana
                cv2.setWindowTitle(self.get_window_title(), self.get_window_title())
    
    def draw_plazas(self):
        """Dibuja todas las plazas definidas en la imagen"""
        display_image = self.original_image.copy()
        
        # Dibujar plazas guardadas
        for idx, (x, y, w, h) in enumerate(self.plazas):
            cv2.rectangle(display_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Número de plaza
            cv2.putText(display_image, str(idx + 1), (x + 5, y + 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Dibujar rectángulo temporal si se está dibujando
        if self.drawing and self.start_point and self.current_rect:
            x1, y1 = self.start_point
            x2, y2 = self.current_rect
            cv2.rectangle(display_image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        
        return display_image
    
    def remove_last_plaza(self):
        """Elimina la última plaza definida"""
        if self.plazas:
            removed = self.plazas.pop()
            print(f"Plaza {len(self.plazas) + 1} eliminada: {removed}")
            cv2.setWindowTitle(self.get_window_title(), self.get_window_title())
        else:
            print("No hay plazas para eliminar")
    
    def save_plazas(self):
        """Guarda las plazas en un archivo pickle"""
        if not self.plazas:
            print("⚠️ No hay plazas definidas. No se guardará nada.")
            return False
        
        with open(self.output_file, 'wb') as f:
            pickle.dump(self.plazas, f)
        
        print(f"✅ {len(self.plazas)} plazas guardadas en '{self.output_file}'")
        return True
    
    def run(self):
        """Ejecuta el configurador interactivo"""
        print("\n" + "="*60)
        print("CONFIGURADOR DE PLAZAS DE APARCAMIENTO")
        print("="*60)
        print("\nControles:")
        print("  - Click izquierdo y arrastrar: Dibujar rectángulo")
        print("  - 'r': Eliminar último rectángulo")
        print("  - 's': Guardar y salir")
        print("  - 'q': Salir sin guardar")
        print("\nObjetivo: Definir 51 plazas en la zona central-derecha")
        print("="*60 + "\n")
        
        while True:
            # Dibujar imagen actualizada
            display = self.draw_plazas()
            
            # Mostrar contador en la imagen
            counter_text = f"Plazas: {len(self.plazas)} / 51"
            cv2.putText(display, counter_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            
            # Mostrar instrucciones
            cv2.putText(display, "r: Eliminar | s: Guardar | q: Salir", (10, display.shape[0] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            cv2.imshow(self.get_window_title(), display)
            
            # Procesar teclas
            key = cv2.waitKey(30) & 0xFF
            
            if key == ord('r'):
                self.remove_last_plaza()
            
            elif key == ord('s'):
                if self.save_plazas():
                    break
            
            elif key == ord('q'):
                print("❌ Saliendo sin guardar...")
                break
        
        cv2.destroyAllWindows()


def main():
    # Buscar la primera imagen en la carpeta data
    data_dir = Path("data")
    
    if not data_dir.exists():
        print(f"❌ Error: La carpeta '{data_dir}' no existe")
        print("   Asegúrate de ejecutar el script desde el directorio del proyecto")
        return
    
    # Obtener todas las imágenes
    image_files = sorted(list(data_dir.glob("*.jpg")) + list(data_dir.glob("*.png")))
    
    if not image_files:
        print(f"❌ Error: No se encontraron imágenes en '{data_dir}'")
        return
    
    # Usar la primera imagen
    first_image = image_files[0]
    print(f"📸 Usando imagen: {first_image.name}")
    
    # Iniciar configurador
    configurator = PlazaConfigurator(first_image)
    configurator.run()


if __name__ == "__main__":
    main()
