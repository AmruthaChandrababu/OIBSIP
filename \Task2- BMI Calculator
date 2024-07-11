import tkinter as tk
from tkinter import messagebox


app = tk.Tk()
app.title('BMI Calculator')
app.geometry('400x450')


app.configure(bg='#000')  

def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        
        if weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Please enter valid weight and height values.")
            return
        
        bmi = weight / (height ** 2)
        bmi_label.config(text=f"Your BMI: {bmi:.2f}", fg='#fff', font=('Helvetica', 18, 'bold'))
        
        if bmi < 18.5:
            category = "Underweight"
            category_color = '#e74c3c'  
        elif bmi < 25:
            category = "Normal weight"
            category_color = '#2ecc71'  
        elif bmi < 30:
            category = "Overweight"
            category_color = '#f39c12'  
        else:
            category = "Obese"
            category_color = '#e74c3c' 
        
        category_label.config(text=f"BMI Category: {category}", fg=category_color, font=('Helvetica', 14, 'italic'))
        
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter numeric values for weight and height.")


title_label = tk.Label(app, text="BMI Calculator", font=("Arial", 24, "bold"), fg='#3498db', bg='#000')
title_label.pack(pady=10)

weight_label = tk.Label(app, text="Enter your weight (kg):", fg='#fff', bg='#000', font=('Helvetica', 12))
weight_label.pack()

weight_entry = tk.Entry(app, width=10, font=('Helvetica', 12))
weight_entry.pack()

height_label = tk.Label(app, text="Enter your height (m):", fg='#fff', bg='#000', font=('Helvetica', 12))
height_label.pack()

height_entry = tk.Entry(app, width=10, font=('Helvetica', 12))
height_entry.pack()

calculate_button = tk.Button(app, text="Calculate BMI", command=calculate_bmi, bg='#3498db', fg='#fff', font=('Helvetica', 14, 'bold'), relief='raised', bd=3)
calculate_button.pack(pady=10)

bmi_label = tk.Label(app, text="", fg='#fff', bg='#000', font=('Helvetica', 18, 'bold'))
bmi_label.pack()

category_label = tk.Label(app, text="", fg='#fff', bg='#000', font=('Helvetica', 14, 'italic'))
category_label.pack()

app.mainloop()
