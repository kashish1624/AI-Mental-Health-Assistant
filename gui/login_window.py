# --------- Import Required Libraries ----------
import tkinter as tk  # GUI framework
from tkinter import messagebox  # For alert popups
from PIL import Image, ImageTk  # To show logo image
import dashboard  # To launch the main dashboard after login
import sqlite3  # For local database operations
import hashlib  # To encrypt password securely
import os  # For handling file paths

# --------- Function to Encrypt Password Using SHA-256 ----------
def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()  # Converts password to secure hash

# --------- Define Path to SQLite Database File ----------
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database", "user_auth.db"))
# db_path = path like /project_root/database/user_auth.db

# --------- Create Table If Not Exists ----------
def create_user_table():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)  # Table with username (unique) and encrypted password
    conn.commit()
    conn.close()

# --------- Register New User ----------
def register_user():
    username = entry_username.get()
    password = entry_password.get()

    # Check if fields are filled
    if not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    encrypted_pw = encrypt_password(password)  # Encrypt password before saving

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, encrypted_pw))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")  # Prevent duplicate usernames
    conn.close()

# --------- Login Existing User ----------
def login_user():
    username = entry_username.get()
    password = entry_password.get()
    encrypted_pw = encrypt_password(password)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, encrypted_pw))
    result = c.fetchone()
    conn.close()

    if result:
        messagebox.showinfo("Login Success", f"Welcome, {username}!")
        root.destroy()  # Close login window
        dashboard.launch_dashboard(username)  # Open dashboard.py for logged-in user
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# --------- Forgot Password Handler ----------
def forgot_password():
    def reset():
        uname = entry_forgot_username.get()
        new_pw = entry_new_password.get()

        if not uname or not new_pw:
            messagebox.showerror("Error", "All fields are required.")
            return

        encrypted_pw = encrypt_password(new_pw)

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (uname,))
        if c.fetchone():
            c.execute("UPDATE users SET password=? WHERE username=?", (encrypted_pw, uname))
            conn.commit()
            messagebox.showinfo("Success", "Password reset!")
            top.destroy()  # Close forgot password popup
        else:
            messagebox.showerror("Error", "Username not found.")
        conn.close()

    # --------- Popup Window for Password Reset ----------
    top = tk.Toplevel(root)
    top.title("Reset Password")
    top.geometry("300x200")
    top.configure(bg="#393E46")

    tk.Label(top, text="Enter Username:", fg="white", bg="#393E46").pack(pady=5)
    entry_forgot_username = tk.Entry(top, width=25)
    entry_forgot_username.pack(pady=5)

    tk.Label(top, text="New Password:", fg="white", bg="#393E46").pack(pady=5)
    entry_new_password = tk.Entry(top, show="*", width=25)
    entry_new_password.pack(pady=5)

    tk.Button(top, text="Reset", command=reset, bg="#00ADB5", fg="white").pack(pady=10)

# --------- GUI Design Starts Here ----------
root = tk.Tk()
root.title("AI Mental Health Assistant")
root.geometry("900x600")
root.configure(bg="#222831")  # Dark background theme

# ✅ Set Icon in Title Bar
icon_path = os.path.abspath("assets/logo.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# --------- Title Label ---------
tk.Label(
    root,
    text="🌿 AI Mental Health Assistant",
    font=("Arial", 32, "bold"),
    fg="#00ADB5",
    bg="#222831"
).pack(pady=(0, 20))

# ✅ Display Logo Image Under Title
logo_path = os.path.abspath("assets/logo.png")
if os.path.exists(logo_path):
    logo_img = Image.open(logo_path)
    logo_img = logo_img.resize((200, 200))  # Resize logo
    logo_tk = ImageTk.PhotoImage(logo_img)
    tk.Label(root, image=logo_tk, bg="#222831").pack(pady=10)

# --------- Form Container for Login/Register ---------
container = tk.Frame(root, bg="#393E46", padx=30, pady=30)
container.place(relx=0.5, rely=0.5, anchor="center")  # Center of the window

# Username Field
tk.Label(container, text="Username:", fg="white", bg="#393E46", font=("Arial", 12)).pack(pady=5)
entry_username = tk.Entry(container, font=("Arial", 12), width=30)
entry_username.pack(pady=5)

# Password Field
tk.Label(container, text="Password:", fg="white", bg="#393E46", font=("Arial", 12)).pack(pady=5)
entry_password = tk.Entry(container, show="*", font=("Arial", 12), width=30)
entry_password.pack(pady=5)

# Buttons with Common Style
btn_style = {"font": ("Arial", 12), "width": 20}

# Login Button
tk.Button(container, text="Login", command=login_user, bg="#00ADB5", fg="white", **btn_style).pack(pady=10)

# Sign Up Button
tk.Button(container, text="Sign Up", command=register_user, bg="#393E46", fg="white", **btn_style).pack(pady=5)

# Forgot Password Button (Flat Style)
tk.Button(container, text="Forgot Password?", command=forgot_password,
          bg="#222831", fg="skyblue", relief="flat", font=("Arial", 10)).pack(pady=5)

# --------- Call Create Table Once on Start ---------
create_user_table()

# --------- Start GUI Event Loop ---------
root.mainloop()
