import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect("database/mood_logs.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS mood_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            mood TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# ---------- Add Mood Entry ----------
def log_mood(user, mood):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("database/mood_logs.db")
    c = conn.cursor()
    c.execute("INSERT INTO mood_log (user, mood, timestamp) VALUES (?, ?, ?)", (user, mood, timestamp))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", f"Mood '{mood}' logged at {timestamp}")

# ---------- Show Mood Chart with Date Filter ----------
def view_mood_chart(user):
    def show_chart_for_range(range_type):
        conn = sqlite3.connect("database/mood_logs.db")
        c = conn.cursor()

        query = "SELECT mood, COUNT(*) FROM mood_log WHERE user = ?"
        params = [user]

        if range_type == "Today":
            today = datetime.now().strftime("%Y-%m-%d")
            query += " AND DATE(timestamp) = ?"
            params.append(today)

        elif range_type == "Last 7 Days":
            seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            query += " AND DATE(timestamp) >= ?"
            params.append(seven_days_ago)

        elif range_type == "This Month":
            first_day = datetime.now().replace(day=1).strftime("%Y-%m-%d")
            query += " AND DATE(timestamp) >= ?"
            params.append(first_day)

        c.execute(query + " GROUP BY mood", params)
        data = c.fetchall()
        conn.close()

        if not data:
            messagebox.showinfo("No Data", f"No mood logs for '{range_type}'.")
            return

        moods, counts = zip(*data)

        plt.figure(figsize=(12, 5))

        # Bar Chart
        plt.subplot(1, 2, 1)
        plt.bar(moods, counts, color=["green", "red", "blue", "orange", "gray"])
        plt.title(f"Mood Bar Chart ({range_type})")
        plt.xlabel("Mood")
        plt.ylabel("Count")

        # Pie Chart
        plt.subplot(1, 2, 2)
        plt.pie(counts, labels=moods, autopct='%1.1f%%', startangle=90,
                colors=["green", "red", "blue", "orange", "gray"])
        plt.title(f"Mood Distribution ({range_type})")
        plt.axis("equal")

        plt.tight_layout()
        plt.show()

    # Popup for filter options
    filter_window = tk.Toplevel()
    filter_window.title("Select Mood Chart Time Range")
    filter_window.geometry("300x250")
    filter_window.configure(bg="#222831")

    tk.Label(filter_window, text="Select Time Range", bg="#222831", fg="white", font=("Arial", 14)).pack(pady=20)

    for label in ["Today", "Last 7 Days", "This Month", "All Time"]:
        tk.Button(filter_window, text=label, bg="#00ADB5", fg="white", font=("Arial", 12),
                  width=20, command=lambda r=label: [filter_window.destroy(), show_chart_for_range(r)]).pack(pady=10)

    filter_window.grab_set()

# ---------- Mood Timeline Graph ----------
def show_mood_timeline(user):
    mood_scores = {
        "Happy": 5,
        "Neutral": 3,
        "Sad": 2,
        "Anxious": 1,
        "Angry": 0
    }

    def fetch_and_plot(range_type):
        conn = sqlite3.connect("database/mood_logs.db")
        c = conn.cursor()

        query = "SELECT timestamp, mood FROM mood_log WHERE user = ?"
        params = [user]

        if range_type == "Last 7 Days":
            date_limit = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            query += " AND DATE(timestamp) >= ?"
            params.append(date_limit)
        elif range_type == "This Month":
            first_day = datetime.now().replace(day=1).strftime("%Y-%m-%d")
            query += " AND DATE(timestamp) >= ?"
            params.append(first_day)

        query += " ORDER BY timestamp"

        c.execute(query, params)
        data = c.fetchall()
        conn.close()

        if not data:
            messagebox.showinfo("No Data", f"No mood timeline data for {range_type}.")
            return

        dates = [datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").date() for row in data]
        scores = [mood_scores.get(row[1], 0) for row in data]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, scores, marker='o', linestyle='-', color='#00ADB5')
        plt.title(f"Mood Timeline ({range_type})")
        plt.xlabel("Date")
        plt.ylabel("Mood Level (0–5)")
        plt.yticks([0, 1, 2, 3, 4, 5],
                   ['Angry', 'Anxious', 'Sad', 'Neutral', '', 'Happy'])
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # GUI for range selection
    popup = tk.Toplevel()
    popup.title("Mood Timeline Filter")
    popup.geometry("300x200")
    popup.configure(bg="#222831")

    tk.Label(popup, text="Select Time Range", bg="#222831", fg="white", font=("Arial", 14)).pack(pady=10)

    for label in ["Last 7 Days", "This Month", "All Time"]:
        tk.Button(popup, text=label, bg="#00ADB5", fg="white", font=("Arial", 12),
                  command=lambda r=label: [popup.destroy(), fetch_and_plot(r)]).pack(pady=10)

    popup.grab_set()

# ---------- Mood Tracker Window ----------
def open_mood_tracker(user):
    init_db()

    window = tk.Toplevel()
    window.title("Mood Tracker")
    window.geometry("400x500")
    window.configure(bg="#222831")

    tk.Label(window, text="How are you feeling today?", bg="#222831", fg="white", font=("Arial", 14)).pack(pady=20)

    moods = ["Happy", "Sad", "Anxious", "Angry", "Neutral"]
    for mood in moods:
        tk.Button(window, text=mood, bg="#00ADB5", fg="white", font=("Arial", 12),
                  width=20, command=lambda m=mood: log_mood(user, m)).pack(pady=5)

    tk.Button(window, text="📊 View Mood Chart", bg="#393E46", fg="white", font=("Arial", 12),
              command=lambda: view_mood_chart(user)).pack(pady=10)

    tk.Button(window, text="📈 View Mood Timeline", bg="#00ADB5", fg="white", font=("Arial", 12),
              command=lambda: show_mood_timeline(user)).pack(pady=10)

    

    window.grab_set()
