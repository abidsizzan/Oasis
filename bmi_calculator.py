import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
conn = sqlite3.connect('bmi_data.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS bmi_data (
    id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL,
    weight REAL NOT NULL,
    height REAL NOT NULL,
    bmi REAL NOT NULL,
    category TEXT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()
def cal_bmi(weight, height):
    height_in_mts = height / 100
    bmi = weight / (height_in_mts ** 2)
    return round(bmi, 2)

def get_bmi_cat(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"
root = tk.Tk()
root.title("BMI Calculator")
user_name_var = tk.StringVar()
weight_var = tk.DoubleVar()
height_var = tk.DoubleVar()

def cal_and_save_bmi():
    try:
        user_name = user_name_var.get()
        weight = weight_var.get()
        height = height_var.get()

        if not user_name or weight <= 0 or height <= 0:
            messagebox.showerror("Input Error", "Please provide valid inputs.")
            return

        bmi = cal_bmi(weight, height)
        category = get_bmi_cat(bmi)
        result_label.config(text=f"BMI: {bmi} ({category})")
        cursor.execute('''
        INSERT INTO bmi_data (user_name, weight, height, bmi, category)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_name, weight, height, bmi, category))
        conn.commit()
        messagebox.showinfo("Success", "BMI calculated and saved Successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_bmi_history():
    user_name = user_name_var.get()    
    if not user_name:
        messagebox.showerror("Input Error", "Please enter a user name to view history.")
        return
    cursor.execute('SELECT date, bmi FROM bmi_data WHERE user_name = ?', (user_name,))
    data = cursor.fetchall()
    if not data:
        messagebox.showinfo("No Data", "No historical data found for this user.")
        return
    dates = [datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S') for row in data]
    bmi_values = [row[1] for row in data]
    plt.figure(figsize=(10, 6))
    plt.plot(dates, bmi_values, marker='o')
    plt.title(f"BMI Trend for {user_name}")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.grid(True)
    plt.show()
tk.Label(root, text="User Name").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=user_name_var).grid(row=0, column=1, padx=10, pady=10)
tk.Label(root, text="Weight (kg)").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=weight_var).grid(row=1, column=1, padx=10, pady=10)
tk.Label(root, text="Height (cm)").grid(row=2, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=height_var).grid(row=2, column=1, padx=10, pady=10)
tk.Button(root, text="Calculate BMI", command=cal_and_save_bmi).grid(row=3, column=0, padx=10, pady=20)
tk.Button(root, text="View History", command=view_bmi_history).grid(row=3, column=1, padx=10, pady=20)
result_label = tk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=2)
root.mainloop()
conn.close()
