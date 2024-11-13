import cv2 as cv
import cvlib as cv2
from cvlib.object_detection import draw_bbox
import os
import time
import numpy as np
import requests
from pathlib import Path

def download_yolo_tiny():
    """Descarga YOLOv3-tiny que es más ligero y estable"""
    print("Configurando YOLOv3-tiny...")
    
    yolo_dir = Path.home() / '.cvlib' / 'yolo-tiny'
    yolo_dir.mkdir(parents=True, exist_ok=True)
    
    config_url = "https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3-tiny.cfg"
    weights_url = "https://pjreddie.com/media/files/yolov3-tiny.weights"
    
    config_path = yolo_dir / "yolov3-tiny.cfg"
    weights_path = yolo_dir / "yolov3-tiny.weights"
    
    try:
        # Descargar archivo de configuración
        if not config_path.exists():
            print("Descargando archivo de configuración...")
            response = requests.get(config_url)
            with open(config_path, 'wb') as f:
                f.write(response.content)
        
        # Descargar pesos
        if not weights_path.exists():
            print("Descargando pesos del modelo (esto puede tardar unos minutos)...")
            response = requests.get(weights_url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            with open(weights_path, 'wb') as f:
                for data in response.iter_content(chunk_size=8192):
                    if data:
                        f.write(data)
        
        return str(config_path), str(weights_path)
    except Exception as e:
        print(f"Error durante la descarga: {e}")
        return None, None

def ensure_model_downloaded():
    """Asegura que el modelo esté descargado y configurado correctamente"""
    print("Verificando modelo YOLO...")
    try:
        # Crear una imagen de prueba
        test_img = np.zeros((416, 416, 3), dtype=np.uint8)
        
        # Intentar detección con modelo tiny
        cv2.detect_common_objects(
            test_img,
            confidence=0.3,
            model='yolov3-tiny'
        )
        print("Modelo YOLOv3-tiny cargado exitosamente")
        return True
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
        # Intentar descargar el modelo tiny
        config_path, weights_path = download_yolo_tiny()
        if config_path and weights_path:
            try:
                # Cargar el modelo manualmente
                net = cv.dnn.readNet(weights_path, config_path)
                print("Modelo configurado exitosamente")
                return True
            except Exception as e:
                print(f"Error después de la descarga: {e}")
        return False

def initialize_camera():
    """Inicializa y verifica la cámara"""
    for i in range(4):  # Intentar índices 0-3
        print(f"Intentando abrir cámara {i}...")
        cap = cv.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                print(f"Cámara abierta exitosamente en índice {i}")
                return cap
            cap.release()
    return None

def main():
    print("Iniciando sistema de detección de objetos...")
    
    # Asegurar que el modelo esté descargado
    if not ensure_model_downloaded():
        print("No se pudo configurar el modelo. Saliendo...")
        return

    # Inicializar cámara
    cap = initialize_camera()
    if cap is None:
        print("No se pudo abrir ninguna cámara. Saliendo...")
        return

    print("Iniciando detección en tiempo real...")
    
    # Variables para FPS
    fps_start_time = time.time()
    fps_counter = 0
    fps = 0

    while True:
        ret, frame = cap.read()
        
        if not ret or frame is None:
            print("Error al capturar frame")
            break

        try:
            # Actualizar FPS
            fps_counter += 1
            if (time.time() - fps_start_time) > 1:
                fps = fps_counter
                fps_counter = 0
                fps_start_time = time.time()

            # Detección de objetos usando YOLOv3-tiny
            bbox, label, conf = cv2.detect_common_objects(
                frame,
                confidence=0.3,
                model='yolov3-tiny'
            )
            
            # Dibujar resultados
            output_image = draw_bbox(frame, bbox, label, conf)
            
            # Mostrar información
            cv.putText(output_image, f"FPS: {fps}", (10, 30), 
                      cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.putText(output_image, f"Objetos: {len(bbox)}", (10, 60),
                      cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Mostrar imagen
            cv.imshow("Detección de objetos en tiempo real (YOLOv3-tiny)", output_image)
            
            # Salir con 'q'
            if cv.waitKey(1) & 0xFF == ord('q'):
                print("Cerrando aplicación...")
                break

        except Exception as e:
            print(f"Error durante la detección: {e}")
            time.sleep(1)

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()