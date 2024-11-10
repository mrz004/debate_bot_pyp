import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from gemini_connect import generate_response


class DebateBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Debate Bot")

        # Configure the root window to expand with resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create a main frame with padding
        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame.grid_rowconfigure(3, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)

        self.topic_label = tk.Label(self.main_frame, text="Enter Topic:")
        self.topic_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.topic_entry = tk.Entry(self.main_frame, width=50)
        self.topic_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.side_label = tk.Label(self.main_frame, text="Select Side (for/against):")
        self.side_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.side_combobox = ttk.Combobox(
            self.main_frame, values=["for", "against"], state="readonly"
        )
        self.side_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.user_message_label = tk.Label(self.main_frame, text="Enter Your Points:")
        self.user_message_label.grid(row=2, column=0, padx=10, pady=10, sticky="nw")

        self.user_message_text = tk.Text(self.main_frame, height=10, width=50)
        self.user_message_text.grid(
            row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew"
        )

        self.response_label = tk.Label(self.main_frame, text="Bot Response:")
        self.response_label.grid(row=2, column=2, padx=10, pady=10, sticky="nw")

        self.response_text = tk.Text(
            self.main_frame, height=10, width=50, state=tk.DISABLED
        )
        self.response_text.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

        self.send_button = tk.Button(
            self.main_frame, text="Send Message", command=self.handle_message
        )
        self.send_button.grid(row=4, column=0, columnspan=3, pady=10, sticky="ew")

        self.topic = None
        self.side = None
        self.first_message = True

    def set_response(self, response):
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete("1.0", tk.END)
        self.response_text.insert(tk.END, response + "\n")
        self.response_text.config(state=tk.DISABLED)
        self.user_message_text.delete("1.0", tk.END)

    def start_debate(self):
        self.topic = self.topic_entry.get()
        self.side = self.side_combobox.get()
        user_message = self.user_message_text.get("1.0", tk.END).strip()
        if not self.topic or not self.side:
            messagebox.showerror("Error", "Please enter both topic and side.")
            return
        response = generate_response(user_message, self.topic, self.side)
        self.set_response(response)

    def send_message(self):
        user_message = self.user_message_text.get("1.0", tk.END).strip()
        if not user_message:
            messagebox.showerror("Error", "Please enter a message.")
            return
        response = generate_response(user_message)
        self.set_response(response)

    def handle_message(self):
        user_message = self.user_message_text.get("1.0", tk.END).strip()
        if not user_message:
            messagebox.showerror("Error", "Please enter a message.")
            return
        if self.first_message:
            self.start_debate()
            self.first_message = False
        else:
            self.send_message()


if __name__ == "__main__":
    root = tk.Tk()
    app = DebateBotGUI(root)
    root.mainloop()
