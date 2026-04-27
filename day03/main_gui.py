import tkinter as tk
from tkinter import messagebox
import beer_lambert_lib

def run_calculation():
    try:
        a = float(entry_a.get())
        e = float(entry_e.get())
        l = float(entry_l.get())
        
        conc = beer_lambert_lib.calculate_concentration(a, e, l)
        label_result.config(text=f"Result: {conc:.6e} mol/L", fg="blue")
    except ValueError as err:
        messagebox.showerror("Input Error", f"Please check your values: {err}")

# Setting up the main window
root = tk.Tk()
root.title("Beer-Lambert GUI")
root.geometry("300x200")

# Layout
tk.Label(root, text="Absorbance (A):").grid(row=0, column=0, pady=5)
entry_a = tk.Entry(root)
entry_a.grid(row=0, column=1)

tk.Label(root, text="Epsilon (ε):").grid(row=1, column=0, pady=5)
entry_e = tk.Entry(root)
entry_e.grid(row=1, column=1)

tk.Label(root, text="Path Length (l):").grid(row=2, column=0, pady=5)
entry_l = tk.Entry(root)
entry_l.grid(row=2, column=1)

tk.Button(root, text="Calculate", command=run_calculation).grid(row=3, columnspan=2, pady=10)
label_result = tk.Label(root, text="Result: ", font=("Helvetica", 10, "bold"))
label_result.grid(row=4, columnspan=2)

if __name__ == '__main__':
    root.mainloop()