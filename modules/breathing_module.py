import tkinter as tk
from tkinter import messagebox
import os
import cv2
import subprocess
import platform

# Mapping of breathing types to descriptions and video files
breathing_exercises = {
    "Alternate Nostril": {
        "desc": "Balances both hemispheres of the brain. Great for anxiety and calming the nervous system.",
        "file": "exercise_videos/alternate_nostril.mp4"
    },
    "Box Breathing": {
        "desc": "Inhale, hold, exhale, hold – all for 4 seconds. Builds focus and reduces stress.",
        "file": "exercise_videos/box_breathing.mp4"
    },
    "4-7-8 Breathing": {
        "desc": "Inhale 4s, hold 7s, exhale 8s. Helps sleep and deep relaxation.",
        "file": "exercise_videos/four_seven_eight.mp4"
    },
    "Inhale–Hold–Exhale": {
        "desc": "Basic guided breathing. Perfect for quick stress relief.",
        "file": "exercise_videos/inhale_exhale_hold.mp4"
    },
    "Balloon Breathing": {
        "desc": "Visualize blowing a balloon. Great for kids and light anxiety.",
        "file": "exercise_videos/balloon_breathing.mp4"
    },
    "Mountain Flow": {
        "desc": "Visualize climbing and descending a mountain with breath. Increases calm.",
        "file": "exercise_videos/mountain_flow.mp4"
    },
    "Yoga Movement": {
        "desc": "Gentle yoga poses synchronized with breath. Ideal for mild tension.",
        "file": "exercise_videos/yoga_movement.mp4"
    },
    "Wave Breathing": {
        "desc": "Breathe with ocean wave rhythms. Good for mindfulness.",
        "file": "exercise_videos/wave_breathing.mp4"
    }
}

def open_breathing_exercise():
    def play_selected_video():
        selected = selected_type.get()
        if selected not in breathing_exercises:
            messagebox.showerror("Error", "Please select a breathing type.")
            return

        filename = breathing_exercises[selected]["file"]
        video_path = os.path.abspath(os.path.join("assets", filename))

        if not os.path.exists(video_path):
           messagebox.showerror("File Missing", f"Could not find {video_path}")
           return

        # Detect OS and open video with system default media player
        try:
            if platform.system() == "Windows":
               os.startfile(video_path)
            elif platform.system() == "Darwin":  # macOS
               subprocess.call(["open", video_path])
            else:  # Linux
               subprocess.call(["xdg-open", video_path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not play video: {e}")


    # --- GUI Window ---
    window = tk.Toplevel()
    window.title("Breathing Exercise Selector")
    window.geometry("600x450")
    window.configure(bg="#222831")

    tk.Label(window, text="🧘 Select a Breathing Exercise", bg="#222831", fg="white",
             font=("Arial", 16)).pack(pady=10)

    selected_type = tk.StringVar(value="")

    for name, data in breathing_exercises.items():
        frame = tk.Frame(window, bg="#393E46", padx=10, pady=5)
        tk.Radiobutton(frame, text=name, variable=selected_type, value=name,
                       font=("Arial", 12), bg="#393E46", fg="white", selectcolor="#00ADB5").pack(anchor="w")
        tk.Label(frame, text=data["desc"], font=("Arial", 10), wraplength=500,
                 bg="#393E46", fg="#eeeeee", justify="left").pack(anchor="w")
        frame.pack(fill="x", pady=5, padx=15)

    tk.Button(window, text="▶️ Start Exercise", command=play_selected_video,
              bg="#00ADB5", fg="white", font=("Arial", 12)).pack(pady=20)

    

    window.grab_set()
