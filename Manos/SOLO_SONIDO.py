import tkinter as tk
from ultralytics import YOLO
import cv2
import pygame
import threading

def start_detection_thread():
    detection_thread = threading.Thread(target=run_detection)
    detection_thread.start()

def button_1():
    print("Hola, soy el boton 1")

def button_2():
    print("Hola, soy el boton 2")

def run_detection():
    cap = cv2.VideoCapture(0)
    model = YOLO('V8.pt')
    sound_paths = [
        'C:\\Manos\\latido.mp3',
        'C:\\Manos\\peace.mp3',
        'C:\\Manos\\punio.mp3',
        'C:\\Manos\\riff.mp3',
        'C:\\Manos\\Hi.mp3'
    ]
    pygame.mixer.init()
    
    while True:
        try:
            class_num = 0
            ret, frame = cap.read()
            if not ret:
                break
            img_name = "webcam_image.png"
            cv2.imwrite(img_name, frame)
            s = 'C:\\Manos\\webcam_image.png'
            results = model.predict(source=s, conf=0.33, imgsz=640)
            if results and results[0].boxes:  # Verifica si hay detecciones
                for result in results:
                    for box in result.boxes:
                        class_num = int(box.cls[0].item())  # Convierte el número de clase a entero
                        if class_num <= 5:
                            print(f"Reproduciendo sonido para clase {class_num}")
                            pygame.mixer.music.load(sound_paths[class_num])  # Carga el sonido correspondiente
                            pygame.mixer.music.play()
                        else:
                            print(f"Clase fuera de rango: {class_num}")
            else:
                pygame.mixer.music.stop()  # Detén cualquier sonido si no hay detecciones

            cv2.waitKey(3000)  # Espera un tiempo corto para continuar con la siguiente iteración

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            pygame.mixer.music.stop()  # Asegura que se detenga la música en caso de error
    
    cap.release()

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Detección con YOLO")

start_button = tk.Button(root, text="Button 1", command=button_1)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Button 2", command=button_2)
stop_button.pack(pady=10)

# Iniciar la detección en un hilo separado
start_detection_thread()

root.mainloop()
