# modules/chatbot_module.py

import tkinter as tk
from tkinter import messagebox
import random

# ----- Improved AI Response Generator -----
def generate_response(user_input):
    user_input = user_input.lower()

    if any(word in user_input for word in ["sad", "depressed", "down", "crying"]):
        responses = [
            "I'm really sorry you're feeling this way. You're not alone.",
            "It’s okay to cry. It shows strength in feeling deeply.",
            "Take your time. Would you like a calming activity suggestion?",
        ]
        return random.choice(responses)

    elif any(word in user_input for word in ["anxious", "panic", "worried", "scared"]):
        responses = [
            "Anxiety can be tough. Let's pause and breathe slowly together.",
            "You’re safe here. Let’s take a moment to calm your thoughts.",
            "Would you like to try a grounding exercise right now?",
        ]
        return random.choice(responses)

    elif any(word in user_input for word in ["angry", "frustrated", "furious"]):
        responses = [
            "Anger is a valid emotion. Let’s explore what triggered it.",
            "Would a breathing exercise help you cool down?",
            "Take a moment to breathe. You're in control.",
        ]
        return random.choice(responses)

    elif any(word in user_input for word in ["happy", "good", "excited", "grateful"]):
        responses = [
            "That’s wonderful! I'm so glad you're feeling that way.",
            "Let’s capture this moment. Want to log this in your mood tracker?",
            "Awesome! You deserve to feel great. 🎉",
        ]
        return random.choice(responses)

    elif any(word in user_input for word in ["lonely", "alone", "isolated"]):
        responses = [
            "I may be a bot, but I'm here for you. You’re not alone in this.",
            "Try reaching out to someone you trust, even if just to say hi.",
            "Would you like to write a gratitude note? It sometimes helps.",
        ]
        return random.choice(responses)

    else:
        fallback_responses = [
            "I'm listening. Tell me more.",
            "Want to talk about what happened today?",
            "Would a motivational video or breathing exercise help?",
            "Take your time. I'm here when you're ready.",
        ]
        return random.choice(fallback_responses)


# ----- Chatbot GUI -----
def open_chatbot():
    def send_message():
        user_msg = entry.get()
        if user_msg.strip() == "":
            return
        chat_display.insert(tk.END, f"You: {user_msg}\n")

        ai_reply = generate_response(user_msg)
        chat_display.insert(tk.END, f"AI: {ai_reply}\n\n")
        entry.delete(0, tk.END)

    # Main window
    window = tk.Toplevel()
    window.title("AI Mental Health Assistant")
    window.attributes("-fullscreen", True)  # ✅ Fullscreen
    window.configure(bg="#222831")

    wrapper = tk.Frame(window, bg="#222831")
    wrapper.pack(expand=True, fill="both", padx=50, pady=30)

    # Title
    tk.Label(wrapper, text="🤖 AI Mental Health Assistant",
             font=("Arial", 20, "bold"), bg="#222831", fg="#00FFF0").pack(pady=10)

    # Chat display
    chat_display = tk.Text(wrapper, height=22, width=100, wrap=tk.WORD,
                           font=("Arial", 12), bg="white", fg="black")
    chat_display.pack(pady=10)

    # Entry field
    entry = tk.Entry(wrapper, width=80, font=("Arial", 12))
    entry.pack(pady=5)

    # Send button
    tk.Button(wrapper, text="Send", command=send_message,
              bg="#00ADB5", fg="white", font=("Arial", 12), width=15).pack(pady=5)

    # Back button
    tk.Button(wrapper, text="🔙 Back", command=window.destroy,
              bg="#FF3E4D", fg="white", font=("Arial", 12), width=15).pack(pady=20)

    # Intro message
    chat_display.insert(tk.END, "AI: Hello! How are you feeling today?\n")

    window.grab_set()
