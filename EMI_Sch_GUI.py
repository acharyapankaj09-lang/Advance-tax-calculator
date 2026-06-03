import pandas as pd
import tkinter as tk
from tkinter import messagebox

def calc_emi(P, R, N):
    R = R / (12 * 100)
    emi = (P * R * (1+R)**N) / ((1+R)**N - 1)
    return emi

def generate_schedule():
    try:
        P = float(entry_principal.get())
        R = float(entry_rate.get())
        N = int(entry_period.get())

        emi = calc_emi(P, R, N)
        balance = P
        monthly_rate = R / (12 * 100)

        schedule = []

        for month in range(1, N+1):
            interest = balance * monthly_rate
            principal = emi - interest
            balance -= principal

            schedule.append([
                month,
                round(emi, 2),
                round(interest, 2),
                round(principal, 2),
                round(balance if balance > 0 else 0, 2)
            ])

        df = pd.DataFrame(schedule, columns=[
            "Month", "EMI", "Interest", "Principal", "Balance"
        ])

        output_file = "EMI_Schedule.xlsx"
        df.to_excel(output_file, index=False)

        messagebox.showinfo("Success", f"EMI Schedule saved as {output_file}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# 🖥️ GUI Window
root = tk.Tk()
root.title("EMI Calculator")
root.geometry("350x250")

# Labels & Inputs
tk.Label(root, text="Loan Amount").pack()
entry_principal = tk.Entry(root)
entry_principal.pack()

tk.Label(root, text="Interest Rate (%)").pack()
entry_rate = tk.Entry(root)
entry_rate.pack()

tk.Label(root, text="Period (months)").pack()
entry_period = tk.Entry(root)
entry_period.pack()

# Button
tk.Button(root, text="Generate EMI Schedule", command=generate_schedule).pack(pady=15)

# Run app
root.mainloop()
