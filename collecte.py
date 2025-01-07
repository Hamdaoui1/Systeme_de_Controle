import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import csv  # Pour enregistrer les données

# Initialisation Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialisation OpenCV
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erreur : Impossible d'accéder à la webcam")
    exit()

# Nom du fichier CSV
CSV_FILE = "gesture_data.csv"

# Fonction pour enregistrer les données dans un fichier CSV
def save_data_to_csv(gesture_name, distances):
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([gesture_name] + distances)

# Fonction pour calculer la distance entre deux points
def calculate_distance(point1, point2):
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5

# Fonction principale pour enregistrer les distances
def record_gesture_data(hand_landmarks, gesture_name):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

    # Calculer les distances
    distances = [
        calculate_distance(thumb_tip, wrist),
        calculate_distance(index_tip, wrist),
        calculate_distance(middle_tip, wrist),
        calculate_distance(ring_tip, wrist),
        calculate_distance(pinky_tip, wrist),
    ]

    # Enregistrer dans le CSV
    save_data_to_csv(gesture_name, distances)

# Fonction pour mettre à jour la vidéo et enregistrer les gestes
def update_video():
    ret, frame = cap.read()
    if not ret:
        print("Erreur lors de la capture vidéo")
        return

    # Convertir en RGB pour l'affichage
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Processer avec Mediapipe
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(rgb_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Enregistrer les données
            record_gesture_data(hand_landmarks, gesture_name.get())

    # Convertir l'image pour Tkinter
    img = Image.fromarray(rgb_frame)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    # Relancer la fonction
    video_label.after(10, update_video)

# Fonction pour fermer l'application proprement
def close_app():
    cap.release()
    root.destroy()

# Création de la fenêtre Tkinter
root = tk.Tk()
root.title("Collecte de Données Gestuelles")
root.geometry("800x600")

# Widget pour afficher la vidéo
video_label = Label(root)
video_label.pack()

# Champ pour entrer le nom du geste
gesture_name_label = tk.Label(root, text="Nom du Geste :", font=("Arial", 14))
gesture_name_label.pack(pady=10)
gesture_name = tk.StringVar()
gesture_name_entry = tk.Entry(root, textvariable=gesture_name, font=("Arial", 14))
gesture_name_entry.pack(pady=10)

# Bouton pour quitter l'application
quit_button = tk.Button(root, text="Quitter", command=close_app, font=("Arial", 14), bg="red", fg="white")
quit_button.pack(pady=20)

# Lancer la mise à jour vidéo
update_video()

# Boucle principale Tkinter
root.protocol("WM_DELETE_WINDOW", close_app)
root.mainloop()
