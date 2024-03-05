import tkinter as tk
from tkinter import messagebox

def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        bmi = weight / (height * height)
        category = classify_bmi(bmi)
        result_label.config(text=f'BMI: {bmi:.2f} | Category: {category}', fg=get_category_color(category))
        show_category_info(category)
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter numeric values.")

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def get_category_color(category):
    colors = {
        "Underweight": "blue",
        "Normal": "green",
        "Overweight": "orange",
        "Obese": "red"
    }
    return colors.get(category, "black")

def show_category_info(category):
    category_info = {
        "Underweight": "You may need to gain some weight.",
        "Normal": "You have a healthy weight.",
        "Overweight": "Consider maintaining a healthy diet and exercise routine.",
        "Obese": "Consult with a healthcare professional for weight management."
    }
    messagebox.showinfo("BMI Category Info", category_info.get(category, ""))

def clear_fields(entries):
    for entry in entries:
        entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("BMI Calculator")

# Add labels, entry widgets, buttons, and a result label
weight_label = tk.Label(root, text="Weight (kg):")
weight_label.grid(row=0, column=0, padx=10, pady=10)

weight_entry = tk.Entry(root)
weight_entry.grid(row=0, column=1, padx=10, pady=10)

height_label = tk.Label(root, text="Height (m):")
height_label.grid(row=1, column=0, padx=10, pady=10)

height_entry = tk.Entry(root)
height_entry.grid(row=1, column=1, padx=10, pady=10)

calculate_button = tk.Button(root, text="Calculate BMI", command=calculate_bmi)
calculate_button.grid(row=2, column=0, padx=5, pady=10)

clear_button = tk.Button(root, text="Clear", command=lambda: clear_fields([weight_entry, height_entry]))
clear_button.grid(row=2, column=1, padx=5, pady=10)

result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=2, pady=10)

# Start the main loop
root.mainloop()
