import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import os

# ✅ Create DB and table with journal field
def init_gratitude_db():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect("database/gratitude_log.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS gratitude (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            entry1 TEXT,
            entry2 TEXT,
            entry3 TEXT,
            journal_entry TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

# ✅ Main Gratitude Log Window
def open_gratitude_log(user):
    init_gratitude_db()

    def save_entries():
        e1, e2, e3 = entry1.get(), entry2.get(), entry3.get()
        journal = journal_box.get("1.0", tk.END).strip()

        if not e1 and not e2 and not e3 and not journal:
            messagebox.showerror("Empty", "Please write at least one gratitude or journal entry.")
            return

        conn = sqlite3.connect("database/gratitude_log.db")
        c = conn.cursor()
        c.execute("INSERT INTO gratitude (user, entry1, entry2, entry3, journal_entry, date) VALUES (?, ?, ?, ?, ?, ?)",
                  (user, e1, e2, e3, journal, datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        conn.close()

        messagebox.showinfo("Saved", "Your gratitude and journal have been saved!")
        entry1.delete(0, tk.END)
        entry2.delete(0, tk.END)
        entry3.delete(0, tk.END)
        journal_box.delete("1.0", tk.END)

    def delete_entry(entry_id, window_to_refresh):
        confirm = messagebox.askyesno("Delete", "Are you sure you want to delete this entry?")
        if confirm:
            conn = sqlite3.connect("database/gratitude_log.db")
            c = conn.cursor()
            c.execute("DELETE FROM gratitude WHERE id = ?", (entry_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Entry deleted successfully!")
            window_to_refresh.destroy()
            view_logs()

    def view_logs():
        conn = sqlite3.connect("database/gratitude_log.db")
        c = conn.cursor()
        c.execute("SELECT id, date, entry1, entry2, entry3, journal_entry FROM gratitude WHERE user = ? ORDER BY date DESC", (user,))
        logs = c.fetchall()
        conn.close()

        popup = tk.Toplevel(window)
        popup.title("Past Gratitude Entries")
        popup.geometry("600x500")
        popup.configure(bg="#222831")

        container = tk.Frame(popup, bg="#eeeeee")
        canvas = tk.Canvas(container, bg="#eeeeee", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#eeeeee")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        container.pack(fill="both", expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for entry in logs:
            eid, date, e1, e2, e3, journal = entry

            frame = tk.Frame(scrollable_frame, bg="#eeeeee", pady=5, padx=5, relief=tk.GROOVE, bd=1)
            tk.Label(frame, text=f"📅 {date}", bg="#eeeeee", font=("Arial", 10, "bold")).pack(anchor="w")
            if e1: tk.Label(frame, text=f"1. {e1}", bg="#eeeeee").pack(anchor="w")
            if e2: tk.Label(frame, text=f"2. {e2}", bg="#eeeeee").pack(anchor="w")
            if e3: tk.Label(frame, text=f"3. {e3}", bg="#eeeeee").pack(anchor="w")
            if journal:
                tk.Label(frame, text="📝 Journal:", bg="#eeeeee", font=("Arial", 10, "italic")).pack(anchor="w")
                tk.Label(frame, text=journal, wraplength=500, justify="left",
                         bg="#eeeeee", font=("Arial", 10)).pack(anchor="w", padx=5)

            tk.Button(frame, text="🗑️ Delete", bg="#FF3E4D", fg="white", font=("Arial", 10),
                      command=lambda id=eid: delete_entry(id, popup)).pack(anchor="e", pady=5)

            frame.pack(fill="x", padx=5, pady=5)

    # ---------- GUI ----------
    window = tk.Toplevel()
    window.title("Gratitude Journal")
    window.attributes('-fullscreen', True)  # ✅ Fullscreen
    window.configure(bg="#222831")

    wrapper = tk.Frame(window, bg="#222831")
    wrapper.pack(expand=True)

    tk.Label(wrapper, text="🙏 Write 3 things you're grateful for", bg="#222831", fg="white",
             font=("Arial", 18)).pack(pady=(30, 10))

    entry1 = tk.Entry(wrapper, width=70, font=("Arial", 12))
    entry2 = tk.Entry(wrapper, width=70, font=("Arial", 12))
    entry3 = tk.Entry(wrapper, width=70, font=("Arial", 12))
    entry1.pack(pady=5)
    entry2.pack(pady=5)
    entry3.pack(pady=5)

    tk.Label(wrapper, text="📝 Daily Reflection (Free Writing):", bg="#222831", fg="white", font=("Arial", 14)).pack(pady=10)
    journal_box = tk.Text(wrapper, width=80, height=6, font=("Arial", 11))
    journal_box.pack(pady=5)

    tk.Button(wrapper, text="💾 Save Entry", command=save_entries,
              bg="#00ADB5", fg="white", font=("Arial", 13), width=25).pack(pady=20)

    tk.Button(wrapper, text="📂 View Past Entries", command=view_logs,
              bg="#393E46", fg="white", font=("Arial", 12), width=25).pack(pady=5)

    tk.Button(wrapper, text="🔙 Back", command=window.destroy,
              bg="#FF3E4D", fg="white", font=("Arial", 12), width=15).pack(pady=40)

    window.grab_set()


