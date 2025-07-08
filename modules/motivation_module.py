import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import os
import subprocess

# ✅ Create DB for favorites if not exists
def init_fav_db():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect("database/motivational_quotes.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feeling TEXT,
            quote TEXT,
            tip TEXT,
            challenge TEXT,
            video TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

# ✅ Actual Motivation Data
motivation_data = {
    "I am feeling low and unproductive": {
        "quote": "You don't have to be great to start, but you have to start to be great. - Zig Ziglar",
        "tip": "Break down tasks into small chunks. Celebrate each win!",
        "challenge": "Write 3 things you're grateful for and 3 small tasks for today.",
        "video": "assets/motivation_videos/productivity_boost.mp4"
    },
    "I am feeling anxious about the future": {
        "quote": "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "tip": "Focus on the present, breathe deeply, break worries into steps.",
        "challenge": "Write 3 things you're excited about in the near future.",
        "video": "assets/motivation_videos/overcoming_anxiety.mp4"
    },
    "I need peace and clarity": {
        "quote": "Peace is the only battle worth waging. - Albert Camus",
        "tip": "Practice mindfulness for a few minutes daily.",
        "challenge": "Sit silently for 10 mins and release stress with deep breathing.",
        "video": "assets/motivation_videos/healing_thoughts.mp4"
    },
    "I need a boost of confidence": {
        "quote": "Believe you can and you're halfway there. - Theodore Roosevelt",
        "tip": "Focus on wins, practice affirmations, take small bold steps.",
        "challenge": "List 3 things you're proud of this week and share it!",
        "video": "assets/motivation_videos/confidence_boost.mp4"
    },
    "I need self-love reminders": {
        "quote": "You are stronger than you seem, braver than you believe, and smarter than you think. - Christopher Robin",
        "tip": "Use phone reminders, sticky notes, and show self-compassion.",
        "challenge": "Write 5 things you love about yourself and revisit daily.",
        "video": "assets/motivation_videos/love_yourself.mp4"
    },
}

def open_motivational_corner():
    init_fav_db()

    window = tk.Toplevel()
    window.title("Motivational Corner")
    window.geometry("1000x700")
    window.configure(bg="#222831")

    quote = tk.StringVar()
    tip = tk.StringVar()
    challenge = tk.StringVar()
    current_video = tk.StringVar()
    selected_feeling = tk.StringVar(value="I am feeling low and unproductive")

    def show_content():
        feeling = selected_feeling.get()
        data = motivation_data.get(feeling, {})
        quote.set(data.get("quote", "No quote found."))
        tip.set(data.get("tip", ""))
        challenge.set(data.get("challenge", ""))
        current_video.set(data.get("video", ""))

    def play_video():
        video_path = current_video.get()
        if os.path.exists(video_path):
            subprocess.Popen(["start", video_path], shell=True)
        else:
            messagebox.showerror("Error", f"Video not found: {video_path}")

    def save_to_favorites():
        feeling = selected_feeling.get()
        conn = sqlite3.connect("database/motivational_quotes.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO favorites (feeling, quote, tip, challenge, video, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            feeling, quote.get(), tip.get(), challenge.get(), current_video.get(),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()
        messagebox.showinfo("Saved", "This motivation is saved to your favorites!")

    def view_favorites():
        fav_win = tk.Toplevel(window)
        fav_win.title("❤️ Your Saved Favorites")
        fav_win.geometry("850x500")
        fav_win.configure(bg="#222831")

        container = tk.Frame(fav_win, bg="#393E46")
        container.pack(padx=20, pady=20, fill="both", expand=True)

        canvas = tk.Canvas(container, bg="#393E46", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#393E46")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        conn = sqlite3.connect("database/motivational_quotes.db")
        c = conn.cursor()
        c.execute("SELECT id, feeling, quote, tip, challenge, video, date FROM favorites ORDER BY date DESC")
        entries = c.fetchall()
        conn.close()

        def delete_entry(entry_id, frame):
            confirm = messagebox.askyesno("Delete", "Are you sure you want to delete this entry?")
            if confirm:
                conn = sqlite3.connect("database/motivational_quotes.db")
                c = conn.cursor()
                c.execute("DELETE FROM favorites WHERE id=?", (entry_id,))
                conn.commit()
                conn.close()
                frame.destroy()
                messagebox.showinfo("Deleted", "Favorite removed.")

        for entry in entries:
            entry_id, feeling, q, t, ch, video, date = entry
            frame = tk.Frame(scrollable_frame, bg="#eeeeee", padx=10, pady=8, bd=1, relief=tk.GROOVE)

            tk.Label(frame, text=f"🕒 {date}", bg="#eeeeee", font=("Arial", 9, "italic")).pack(anchor="w")
            tk.Label(frame, text=f"💬 {q}", wraplength=780, justify="left", bg="#eeeeee", fg="#00ADB5").pack(anchor="w")
            tk.Label(frame, text=f"📝 Tip: {t}", wraplength=780, justify="left", bg="#eeeeee").pack(anchor="w")
            tk.Label(frame, text=f"🎯 Challenge: {ch}", wraplength=780, justify="left", bg="#eeeeee").pack(anchor="w")

            tk.Button(frame, text="🗑 Delete", bg="#FF3E4D", fg="white", command=lambda eid=entry_id, f=frame: delete_entry(eid, f)).pack(anchor="e", pady=5)

            frame.pack(fill="x", pady=8)

        fav_win.grab_set()

    # ---------- Layout ----------
    tk.Label(window, text="🧠 Motivational Corner", font=("Arial", 22, "bold"), fg="#00FFF0", bg="#222831").pack(pady=(30, 10))

    tk.Label(window, text="🙋‍♀️ How are you feeling right now?", font=("Arial", 14), bg="#222831", fg="white").pack()
    tk.OptionMenu(window, selected_feeling, *motivation_data.keys()).pack(pady=10)

    tk.Button(window, text="🔁 Show Motivation", command=show_content,
              font=("Arial", 12), bg="#00ADB5", fg="white").pack(pady=5)

    content_frame = tk.Frame(window, bg="#393E46", bd=2, relief="flat")
    content_frame.pack(padx=30, pady=30, fill="both", expand=True)

    tk.Label(content_frame, text="💬 Quote", font=("Arial", 13, "bold"),
             bg="#393E46", fg="white").pack(anchor="w", padx=20, pady=(10, 2))
    tk.Label(content_frame, textvariable=quote, font=("Arial", 12),
             wraplength=920, bg="#393E46", fg="#00FFAA", justify="left").pack(padx=20)

    tk.Label(content_frame, text="📝 Tip", font=("Arial", 13, "bold"),
             bg="#393E46", fg="white").pack(anchor="w", padx=20, pady=(15, 2))
    tk.Label(content_frame, textvariable=tip, font=("Arial", 12),
             wraplength=920, bg="#393E46", fg="#FFD369", justify="left").pack(padx=20)

    tk.Label(content_frame, text="🎯 Challenge", font=("Arial", 13, "bold"),
             bg="#393E46", fg="white").pack(anchor="w", padx=20, pady=(15, 2))
    tk.Label(content_frame, textvariable=challenge, font=("Arial", 12),
             wraplength=920, bg="#393E46", fg="#FF6F61", justify="left").pack(padx=20)

    # Buttons
    btn_frame = tk.Frame(window, bg="#222831")
    btn_frame.pack(pady=20)

    tk.Button(btn_frame, text="▶️ Watch Suggested Video", command=play_video,
              font=("Arial", 12), bg="#393E46", fg="white", width=25).grid(row=0, column=0, padx=10)

    tk.Button(btn_frame, text="❤️ Save to Favorites", command=save_to_favorites,
              font=("Arial", 12), bg="#FF416C", fg="white", width=25).grid(row=0, column=1, padx=10)

    tk.Button(window, text="📂 View Saved Favorites", command=view_favorites,
              font=("Arial", 11), bg="#00ADB5", fg="white", width=30).pack(pady=5)

    tk.Label(window, text="🌟 I hope this helped you today.", font=("Arial", 12),
             bg="#222831", fg="#BBBBBB").pack(pady=10)

    

    window.grab_set()

