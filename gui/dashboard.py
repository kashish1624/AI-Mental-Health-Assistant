# ---------- Import Required Libraries ----------
import tkinter as tk  # GUI framework
from tkinter import messagebox  # For popup dialogs
from PIL import Image, ImageTk  # For loading and displaying images
import os  # For file path handling
import sys  # For system path configuration

# ---------- Add Parent Directory to Import Custom Modules ----------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ---------- Import Custom Modules ----------
from modules.chatbot_module import open_chatbot  # AI chatbot module
from modules.quiz_module import start_quiz  # Mental health quiz module
from modules.mood_tracker import open_mood_tracker  # Mood tracking & graph
from modules.breathing_module import open_breathing_exercise  # Breathing activity
from modules.motivation_module import open_motivational_corner  # Motivation quotes/video
from modules.gratitude_module import open_gratitude_log  # Gratitude journaling

# ---------- Launch Dashboard Function ----------
def launch_dashboard(user):
    window = tk.Tk()  # Main window
    window.title("AI Mental Health Assistant")
    window.state("zoomed")  # ✅ Opens in full screen mode

    # ---------- Set Icon in Title Bar ----------
    icon_path = os.path.abspath("assets/logo.ico")
    if os.path.exists(icon_path):
        window.iconbitmap(icon_path)

    # ---------- Set Fullscreen Background Image ----------
    bg_path = os.path.abspath("assets/bg_dashboard.png")
    if os.path.exists(bg_path):
        screen_w = window.winfo_screenwidth()  # Get screen width
        screen_h = window.winfo_screenheight()  # Get screen height
        bg_img = Image.open(bg_path).resize((screen_w, screen_h))  # Resize image
        bg_photo = ImageTk.PhotoImage(bg_img)

        bg_label = tk.Label(window, image=bg_photo)
        bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fullscreen

    # ---------- Overlay Frame (Black Transparent Box) ----------
    overlay = tk.Frame(window, bg="#000000", bd=0)  # Overlay panel for content
    overlay.place(relx=0.5, rely=0.5, anchor="center")  # Centered

    # ---------- Welcome Text ----------
    tk.Label(
        overlay,
        text=f"Welcome, {user}",
        font=("Arial", 20, "bold"),
        bg="#000000", fg="#00FFF5"
    ).pack(pady=(20, 5))

    tk.Label(
        overlay,
        text="✽ Take a step today toward your mental wellness ✽",
        font=("Arial", 12),
        bg="#000000", fg="white"
    ).pack()

    # ---------- Buttons Frame (Grid Layout) ----------
    grid_frame = tk.Frame(overlay, bg="#000000")
    grid_frame.pack(pady=30)

    # ---------- Function to Create Styled Buttons ----------
    def styled_button(text, cmd, icon="💡"):
        return tk.Button(
            grid_frame,
            text=f"{icon}  {text}",
            font=("Arial", 12, "bold"),
            width=30,
            height=2,
            bg="#00ADB5",
            fg="white",
            bd=0,
            activebackground="#008C8C",
            command=cmd
        )

    # ---------- Feature Buttons in Grid (2 columns) ----------
    styled_button("Talk to AI Assistant", open_chatbot, "🤖").grid(row=0, column=0, padx=20, pady=10)
    styled_button("Take Mental Health Quiz", start_quiz, "📝").grid(row=0, column=1, padx=20, pady=10)
    styled_button("View Mood Tracker", lambda: open_mood_tracker(user), "📈").grid(row=1, column=0, padx=20, pady=10)
    styled_button("Breathing Exercise", open_breathing_exercise, "🌬️").grid(row=1, column=1, padx=20, pady=10)
    styled_button("Motivational Corner", open_motivational_corner, "💬").grid(row=2, column=0, padx=20, pady=10)
    styled_button("Gratitude Journal", lambda: open_gratitude_log(user), "🙏").grid(row=2, column=1, padx=20, pady=10)

    # ---------- Logout Button ----------
    tk.Button(
        overlay,
        text="🔐 Logout",
        font=("Arial", 11, "bold"),
        bg="#FF3E4D",
        fg="white",
        width=20,
        command=lambda: logout(window)
    ).pack(pady=20)

    # ---------- Start Main GUI Loop ----------
    window.mainloop()

# ---------- Logout Handler ----------
def logout(window):
    if messagebox.askyesno("Logout", "Do you really want to logout?"):
        window.destroy()  # Close the dashboard window

# ---------- Run Directly for Testing ----------
if __name__ == "__main__":
    launch_dashboard("test_user@example.com")  # Launch dashboard with test user
