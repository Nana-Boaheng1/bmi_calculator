# Rebuilding with gamified style, dark mode toggle, animations, progress bar, and input validation
import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib.pyplot as plt
from fpdf import FPDF
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global state
user_data = {
    "name": "",
    "gender": "",
    "age": 0,
    "height": 0.0,
    "weight": 0.0
}
questions = ["name", "gender", "age", "height", "weight"]
question_labels = {
    "name": "👤 What's your name?",
    "gender": "⚧ What's your gender? (Male/Female)",
    "age": "🎂 What's your age?",
    "height": "📏 Your height in meters (e.g., 1.75):",
    "weight": "⚖️ Your weight in kg:"
}
current_question_index = 0
entries = {}
frames = []
dark_mode = False


def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()


def apply_theme():
    bg = "#121212" if dark_mode else "#f0f0f0"
    fg = "#f0f0f0" if dark_mode else "#000000"
    for widget in root.winfo_children():
        widget.configure()
        for sub in widget.winfo_children():
            try:
                sub.configure()
            except:
                pass
    root.configure(bg=bg)


def next_question():
    global current_question_index
    key = questions[current_question_index]
    val = entries[key].get().strip()
    if not val or (key == "age" and not val.isdigit()) or (key in ["height", "weight"] and not is_float(val)):
        messagebox.showerror("Invalid Input", f"Please enter a valid {key}.")
        return
    current_question_index += 1
    if current_question_index < len(questions):
        show_question()
    else:
        show_result()


def back_question():
    global current_question_index
    if current_question_index > 0:
        current_question_index -= 1
        show_question()


def show_question():
    for frame in frames:
        frame.pack_forget()
    frame = frames[current_question_index]
    frame.pack(pady=40, fill='x')
    progress_var.set((current_question_index + 1) / len(questions) * 100)
    entries[questions[current_question_index]].focus_set()


def show_result():
    for frame in frames:
        frame.pack_forget()

    user_data["name"] = entries["name"].get().strip()
    user_data["gender"] = entries["gender"].get().strip().capitalize()
    user_data["age"] = int(entries["age"].get().strip())
    user_data["height"] = float(entries["height"].get().strip())
    user_data["weight"] = float(entries["weight"].get().strip())

    bmi = user_data["weight"] / (user_data["height"] ** 2)
    category = classify_bmi(bmi)
    ideal = ideal_weight_range(user_data["height"], user_data["gender"])
    tips = category_info[category]

    result_text = f"🎉 Hello {user_data['name']}!\n\n📊 Your BMI is {bmi:.2f}.\n💬 Category: {category}\n💡 Tips: {tips}\n🏁 Ideal Weight Range: {ideal[0]}kg - {ideal[1]}kg"
    result_label.config(text=result_text)
    result_frame.pack(pady=20)
    draw_chart(bmi, category)


def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def ideal_weight_range(height, gender):
    base = 50 if gender.lower() == "male" else 45.5
    ideal = base + 2.3 * ((height * 100 - 152.4) / 2.54)
    return round(ideal * 0.9, 1), round(ideal * 1.1, 1)


def draw_chart(bmi, category):
    fig, ax = plt.subplots(figsize=(6, 1.5))
    categories = ["Underweight", "Normal", "Overweight", "Obese"]
    colors = ["blue", "green", "orange", "red"]
    bounds = [0, 18.5, 25, 30, 40]

    for i in range(4):
        ax.barh([0], [bounds[i + 1] - bounds[i]], left=bounds[i], color=colors[i], label=categories[i])

    ax.axvline(bmi, color="black", linestyle="--", linewidth=2)
    ax.set_xlim(0, 40)
    ax.axis('off')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3), ncol=4)

    for widget in chart_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


def export_to_pdf():
    bmi = user_data["weight"] / (user_data["height"] ** 2)
    category = classify_bmi(bmi)
    ideal = ideal_weight_range(user_data["height"], user_data["gender"])
    tips = category_info[category]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"BMI Report for {user_data['name']}", ln=True, align="C")
    pdf.ln(10)
    pdf.multi_cell(0, 10,
                   f"BMI: {bmi:.2f}\nCategory: {category}\nTips: {tips}\nIdeal Weight Range: {ideal[0]}kg - {ideal[1]}kg")
    pdf.output("BMI_Report.pdf")
    messagebox.showinfo("PDF Exported", "BMI_Report.pdf has been saved.")


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


# Category info tips
category_info = {
    "Underweight": "Eat more frequently and choose nutrient-rich foods.",
    "Normal": "Maintain your healthy lifestyle!",
    "Overweight": "Try to include daily walking and reduce sugary snacks.",
    "Obese": "Adopt a structured weight loss plan with professional support."
}

# App UI
root = tk.Tk()
root.title("Gamified BMI Assistant")
root.geometry("700x600")
root.configure(bg="#f0f0f0")

# Top bar with dark mode toggle
top_frame = tk.Frame(root, bg="#f0f0f0")
top_frame.pack(fill='x', pady=5)
tk.Button(top_frame, text="🌙 Toggle Dark Mode", command=toggle_dark_mode).pack(side="right", padx=10)

# Progress bar
progress_var = tk.DoubleVar()
progress = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress.pack(fill="x", padx=20, pady=10)


# Question frames
def make_question_frame(key):
    frame = tk.Frame(root, bg="#f0f0f0")
    label = tk.Label(frame, text=question_labels[key], font=("Poppins", 18), bg="#f0f0f0")
    label.pack(pady=10)
    entry = tk.Entry(frame, font=("Montserrat", 16), width=30, justify="center")
    entries[key] = entry
    entry.pack(pady=10)
    nav_frame = tk.Frame(frame, bg="#f0f0f0")
    tk.Button(nav_frame, text="⬅ Back", command=back_question).pack(side="left", padx=10)
    tk.Button(nav_frame, text="➡ Next", command=next_question).pack(side="left", padx=10)
    nav_frame.pack(pady=20)
    return frame


for key in questions:
    frames.append(make_question_frame(key))

# Result frame
result_frame = tk.Frame(root, bg="#f0f0f0")
result_label = tk.Label(result_frame, text="", font=("Poppins", 14), bg="#f0f0f0", wraplength=600, justify="left")
result_label.pack(pady=10)
tk.Button(result_frame, text="📄 Export PDF", command=export_to_pdf).pack(pady=5)
chart_frame = tk.Frame(result_frame, bg="#f0f0f0")
chart_frame.pack(pady=10)

# Start app
show_question()
apply_theme()
root.mainloop()
