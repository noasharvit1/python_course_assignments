import tkinter as tk
from tkinter import messagebox
import beer_lambert_lib

def run_calculation():
    try:
        # שליפת הנתונים מהתיבות
        a = float(entry_a.get())
        e = float(entry_e.get())
        l = float(entry_l.get())
        
        # ביצוע החישובים באמצעות הספרייה
        conc = beer_lambert_lib.calculate_concentration(a, e, l)
        trans = beer_lambert_lib.calculate_transmittance(a)
        
        # עדכון תווית התוצאה עם שני הערכים
        result_text = f"Concentration: {conc:.6e} mol/L\nTransmittance: {trans:.2f}%"
        label_result.config(text=result_text, fg="blue")
        
    except ValueError as err:
        messagebox.showerror("Input Error", f"Please check your values: {err}")

# הגדרת החלון הראשי
root = tk.Tk()
root.title("Beer-Lambert Calculator")
root.geometry("350x250") # הגדלנו מעט את החלון כדי שיהיה מקום לתוצאה הכפולה

# סידור האלמנטים בחלון
tk.Label(root, text="Absorbance (A):").grid(row=0, column=0, pady=5, padx=5)
entry_a = tk.Entry(root)
entry_a.grid(row=0, column=1)

tk.Label(root, text="Epsilon (ε):").grid(row=1, column=0, pady=5, padx=5)
entry_e = tk.Entry(root)
entry_e.grid(row=1, column=1)

tk.Label(root, text="Path Length (l):").grid(row=2, column=0, pady=5, padx=5)
entry_l = tk.Entry(root)
entry_l.grid(row=2, column=1)

tk.Button(root, text="Calculate", command=run_calculation, bg="lightgray").grid(row=3, columnspan=2, pady=10)

# תווית להצגת התוצאות
label_result = tk.Label(root, text="Results will appear here", font=("Helvetica", 10, "bold"), justify="left")
label_result.grid(row=4, columnspan=2, pady=10)

if __name__ == '__main__':
    root.mainloop()