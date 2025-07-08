import tkinter as tk
from tkinter import messagebox

# Quiz questions
questions = [
    "1. I feel nervous, anxious or on edge.",
    "2. I have trouble relaxing.",
    "3. I worry too much about different things.",
    "4. I get easily annoyed or irritable.",
    "5. I feel afraid as if something awful might happen."
]

options = [
    ("Not at all", 0),
    ("Several days", 1),
    ("More than half the days", 2),
    ("Nearly every day", 3)
]

def start_quiz():
    window = tk.Toplevel()  # Use Toplevel so it doesn't block dashboard
    window.title("Mental Health Self-Assessment Quiz")
    window.geometry("650x600")
    window.configure(bg="#222831")

    tk.Label(window, text="Answer the following questions:",
             bg="#222831", fg="white", font=("Arial", 14)).pack(pady=10)

    responses = []

    for i, question in enumerate(questions):
        frame = tk.Frame(window, bg="#222831")
        frame.pack(pady=10, anchor="w", padx=20, fill="x")

        tk.Label(frame, text=question, bg="#222831", fg="white",
                 anchor="w", justify="left", wraplength=600).pack(anchor="w")

        var = tk.IntVar(value=-1)
        responses.append(var)

        for text, value in options:
            tk.Radiobutton(
                frame, text=text, variable=var, value=value,
                bg="#393E46", fg="white", selectcolor="#00ADB5", anchor="w"
            ).pack(anchor="w", padx=30)

    def submit_quiz():
        for i, var in enumerate(responses):
            if var.get() == -1:
                messagebox.showerror("Incomplete", f"Please answer Question {i+1} before submitting.")
                return

        total_score = sum(var.get() for var in responses)

        if total_score <= 4:
            result = "You seem to be doing well. Keep taking care of yourself!"
        elif total_score <= 9:
            result = "You may be experiencing mild anxiety. Try relaxation techniques."
        elif total_score <= 14:
            result = "Moderate anxiety. Consider speaking to a trusted person or professional."
        else:
            result = "Severe symptoms detected. It's okay to seek help. You're not alone."

        messagebox.showinfo("Quiz Result", f"Your total score: {total_score}\n\n{result}")
        window.destroy()

    tk.Button(window, text="Submit Quiz", command=submit_quiz,
              bg="#00ADB5", fg="white", font=("Arial", 12)).pack(pady=20)


    window.grab_set()    # ✔ Locks focus to quiz window

if __name__ == "__main__":
    start_quiz()
