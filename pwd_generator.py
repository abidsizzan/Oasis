import tkinter as tk
from tkinter import messagebox
import random
import string

class PwdGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        self.create_widgets()
        
    def create_widgets(self):
        tk.Label(self.root, text="Password Length:").grid(row=0, column=0, padx=10, pady=10)
        self.length_var = tk.IntVar(value=12)
        tk.Entry(self.root, textvariable=self.length_var).grid(row=0, column=1, padx=10, pady=10)

        self.include_lower = tk.BooleanVar(value=True)
        self.include_upper = tk.BooleanVar(value=True)
        self.include_digits = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)

        tk.Checkbutton(self.root, text="Include Lowercase Letters", variable=self.include_lower).grid(row=1, column=0, padx=10, pady=5, columnspan=2, sticky='w')
        tk.Checkbutton(self.root, text="Include Uppercase Letters", variable=self.include_upper).grid(row=2, column=0, padx=10, pady=5, columnspan=2, sticky='w')
        tk.Checkbutton(self.root, text="Include Digits", variable=self.include_digits).grid(row=3, column=0, padx=10, pady=5, columnspan=2, sticky='w')
        tk.Checkbutton(self.root, text="Include Symbols", variable=self.include_symbols).grid(row=4, column=0, padx=10, pady=5, columnspan=2, sticky='w')

        tk.Button(self.root, text="Generate Password", command=self.generate_pwd).grid(row=5, column=0, padx=10, pady=10, columnspan=2)
        self.pwd_output = tk.Entry(self.root, width=50)
        self.pwd_output.grid(row=6, column=0, padx=10, pady=10, columnspan=2)
        tk.Button(self.root, text="Copy to Clipboard", command=self.copy_to_clipboard).grid(row=7, column=0, padx=10, pady=10, columnspan=2)
        
    def generate_pwd(self):
        length = self.length_var.get()
        if length <= 0:
            messagebox.showerror("Input Error", "Password length must be a positive integer.")
            return

        char_sets = {
            'lower': string.ascii_lowercase,
            'upper': string.ascii_uppercase,
            'digits': string.digits,
            'symbols': string.punctuation
        }

        chars = ""
        if self.include_lower.get():
            chars += char_sets['lower']
        if self.include_upper.get():
            chars += char_sets['upper']
        if self.include_digits.get():
            chars += char_sets['digits']
        if self.include_symbols.get():
            chars += char_sets['symbols']

        if not chars:
            messagebox.showerror("Input Error", "At least one character type must be selected.")
            return

        pwd = ''.join(random.choice(chars) for _ in range(length))
        self.pwd_output.delete(0, tk.END)
        self.pwd_output.insert(0, pwd)

    def copy_to_clipboard(self):
        pwd = self.pwd_output.get()
        if not pwd:
            messagebox.showwarning("Clipboard Error", "No password to copy.")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.root.update()
        messagebox.showinfo("Clipboard", "Password copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PwdGeneratorApp(root)
    root.mainloop()
