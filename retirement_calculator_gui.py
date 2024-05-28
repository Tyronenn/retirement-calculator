import tkinter as tk
from tkinter import messagebox
from retirement_calculator import RetirementCalculator

class RetirementCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Retirement Calculator")

        self.create_widgets()

    def create_widgets(self):
        self.add_label_entry("Current Age:", 0)
        self.add_label_entry("Retirement Age:", 1)
        self.add_label_entry("Life Expectancy:", 2)
        self.add_label_entry("Current Income:", 3)
        self.add_label_entry("Salary Increase (%):", 4)
        self.add_label_entry("Current Savings:", 5)
        self.add_label_entry("Annual Contribution (%):", 6)
        self.add_label_entry("Employer Match (%):", 7)
        self.add_label_entry("Employer Match Limit (%):", 8)
        self.add_label_entry("Expected Return (%):", 9)

        self.calculate_button = tk.Button(self.root, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=10, column=0, columnspan=2, pady=10)

    def add_label_entry(self, text, row):
        label = tk.Label(self.root, text=text)
        label.grid(row=row, column=0, padx=5, pady=5, sticky='e')
        entry = tk.Entry(self.root)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky='w')
        self.add_tooltip(label, text)
        setattr(self, f"{text.lower().replace(' ', '_').replace('(%):', '_entry').replace(':', '')}_entry", entry)

    def add_tooltip(self, widget, text):
        tooltip = tk.Label(self.root, text=text, bg='yellow', relief='solid', borderwidth=1, wraplength=150)
        tooltip.place_forget()

        def enter(event):
            x, y, _, _ = widget.bbox()
            tooltip.place(x=x, y=y+20)

        def leave(event):
            tooltip.place_forget()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def calculate(self):
        try:
            data = {
                'current_age': int(self.current_age_entry.get()),
                'retirement_age': int(self.retirement_age_entry.get()),
                'life_expectancy': int(self.life_expectancy_entry.get()),
                'current_income': float(self.current_income_entry.get()),
                'salary_increase_pct': float(self.salary_increase_entry.get()),
                'current_savings': float(self.current_savings_entry.get()),
                'annual_contrib_pct': float(self.annual_contrib_entry.get()),
                'employer_match_pct': float(self.employer_match_entry.get()),
                'employer_match_limit': float(self.employer_match_limit_entry.get()),
                'expected_return': float(self.expected_return_entry.get())
            }
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}. Please enter the correct data type.")
            return

        calculator = RetirementCalculator()
        projected_savings, savings_over_time = calculator.project_savings(data)
        retirement_years = data['life_expectancy'] - data['retirement_age']
        annual_withdrawal = calculator.calculate_annual_withdrawal(projected_savings, retirement_years, data['expected_return'] / 100)

        result_message = (
            f"Projected savings at age {data['retirement_age']}: ${projected_savings:,.2f}\n"
            f"Annual withdrawal amount to deplete savings by age {data['life_expectancy']}: ${annual_withdrawal:,.2f}\n"
        )
        recommendations = calculator.provide_recommendations(data, projected_savings)
        for rec in recommendations:
            result_message += f"- {rec}\n"

        messagebox.showinfo("Results", result_message)
        calculator.plot_savings_growth(savings_over_time, data['current_age'], data['life_expectancy'])

if __name__ == "__main__":
    root = tk.Tk()
    app = RetirementCalculatorGUI(root)
    root.mainloop()
