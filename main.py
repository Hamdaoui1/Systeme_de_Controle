import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import pyautogui
from tensorflow.keras.models import load_model
import numpy as np
import sys
import time

# Gestionnaire d'exception global
def global_exception_handler(exc_type, exc_value, exc_traceback):
    if not issubclass(exc_type, KeyboardInterrupt):
        print(f"Exception détectée : {exc_value}")
sys.excepthook = global_exception_handler

# Charger le modèle pré-entraîné
model = load_model("gesture_recognition_model.h5")

label_mapping = {0: 'augmenter le volume', 1: 'diminuer le volume', 2: "j'aime", 3: "j'aime pas", 4: 'play/pause'}

# Initialisation Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialisation OpenCV
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erreur : Impossible d'accéder à la webcam")
    exit()

# Variables pour les gestes et le mouvement
frame_counter = 0
GESTURE_DELAY = 15
previous_wrist_x = None
last_gesture = None

def calculate_distance(point1, point2):
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5

def add_directional_feature(data):
    direction = np.sign(data[0] - data[1])
    return np.append(data, direction)

def predict_gesture(distances):
    try:
        distances = add_directional_feature(distances)
        distances = np.array(distances).reshape(1, -1)
        distances = distances / np.max(distances, axis=1)
        prediction = model.predict(distances, verbose=0)
        predicted_label = np.argmax(prediction, axis=1)[0]
        return label_mapping[predicted_label]
    except Exception as e:
        print(f"Erreur dans predict_gesture : {e}")
        return "Aucun geste détecté"

def detect_gesture(hand_landmarks):
    global previous_wrist_x
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

    distances = [
        calculate_distance(thumb_tip, wrist),
        calculate_distance(index_tip, wrist),
        calculate_distance(middle_tip, wrist),
        calculate_distance(ring_tip, wrist),
        calculate_distance(pinky_tip, wrist),
    ]

    if previous_wrist_x is not None:
        movement = wrist.x - previous_wrist_x
        if movement > 0.1:
            previous_wrist_x = wrist.x
            return "Vidéo suivante"
        elif movement < -0.1:
            previous_wrist_x = wrist.x
            return "Vidéo précédente"
    previous_wrist_x = wrist.x

    gesture = predict_gesture(distances)
    return gesture

def execute_action(gesture):
    global frame_counter
    if frame_counter % GESTURE_DELAY == 0:
        if gesture == "play/pause":
            pyautogui.press("space")
        elif gesture == "augmenter le volume":
            pyautogui.press("volumeup")
        elif gesture == "diminuer le volume":
            pyautogui.press("volumedown")
        elif gesture == "Vidéo suivante":
            pyautogui.hotkey("ctrl", "right")
        elif gesture == "Vidéo précédente":
            pyautogui.hotkey("ctrl", "left")
    frame_counter += 1

def update_video():
    global last_gesture
    try:
        ret, frame = cap.read()
        if not ret:
            return

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        gesture = "Aucun geste détecté"
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                try:
                    gesture = detect_gesture(hand_landmarks)
                    if gesture != last_gesture:
                        last_gesture = gesture
                        gesture_label.config(text=f"Geste détecté : {gesture}")
                    execute_action(gesture)
                except Exception as e:
                    print(f"Erreur lors de la détection du geste : {e}")

        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

        video_label.after(10, update_video)

    except Exception as e:
        print(f"Erreur dans update_video : {e}")

def close_app():
    cap.release()
    root.destroy()

root = tk.Tk()
root.title("Contrôle Vidéo par Gestes")
root.geometry("800x600")

video_label = Label(root)
video_label.pack()

gesture_label = tk.Label(root, text="Aucun geste détecté", font=("Arial", 16))
gesture_label.pack(pady=20)

quit_button = tk.Button(root, text="Quitter", command=close_app, font=("Arial", 14), bg="red", fg="white")
quit_button.pack(pady=20)

update_video()
root.mainloop()
