import tkinter as tk
from tkinter import messagebox
from retirement_calculator import RetirementCalculator

class RetirementCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Retirement Calculator")

        self.create_widgets()

    def create_widgets(self):
        self.entries = {}
        tooltips = {
            "Current Age": "Enter your current age in years.",
            "Retirement Age": "Enter the age at which you plan to retire.",
            "Life Expectancy": "Enter your expected age of living.",
            "Current Income": "Enter your current annual income in dollars.",
            "Salary Increase (%)": "Enter your expected annual salary increase percentage.",
            "Current Savings": "Enter your current retirement savings in dollars.",
            "Annual Contribution (%)": "Enter the percentage of your income you plan to contribute annually.",
            "Employer Match (%)": "Enter the percentage of your income that your employer matches.",
            "Employer Match Limit (%)": "Enter the maximum percentage of your income that your employer matches.",
            "Expected Return (%)": "Enter the expected annual return rate on your investments."
        }

        self.add_label_entry("Current Age", 0, tooltips["Current Age"])
        self.add_label_entry("Retirement Age", 1, tooltips["Retirement Age"])
        self.add_label_entry("Life Expectancy", 2, tooltips["Life Expectancy"])
        self.add_label_entry("Current Income", 3, tooltips["Current Income"])
        self.add_label_entry("Salary Increase (%)", 4, tooltips["Salary Increase (%)"])
        self.add_label_entry("Current Savings", 5, tooltips["Current Savings"])
        self.add_label_entry("Annual Contribution (%)", 6, tooltips["Annual Contribution (%)"])
        self.add_label_entry("Employer Match (%)", 7, tooltips["Employer Match (%)"])
        self.add_label_entry("Employer Match Limit (%)", 8, tooltips["Employer Match Limit (%)"])
        self.add_label_entry("Expected Return (%)", 9, tooltips["Expected Return (%)"])

        self.calculate_button = tk.Button(self.root, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=10, column=0, columnspan=2, pady=10)

    def add_label_entry(self, text, row, tooltip_text):
        label = tk.Label(self.root, text=text)
        label.grid(row=row, column=0, padx=5, pady=5, sticky='e')
        entry = tk.Entry(self.root)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky='w')
        self.add_tooltip(entry, tooltip_text)
        self.entries[text] = entry

    def add_tooltip(self, widget, text):
        tooltip = tk.Label(self.root, text=text, bg='yellow', relief='solid', borderwidth=1, wraplength=150)
        tooltip.place_forget()

        def enter(event):
            x, y, width, height = widget.bbox("insert")
            x = x + widget.winfo_rootx() + width
            y = y + widget.winfo_rooty() + height // 2
            tooltip.place(x=x, y=y)

        def leave(event):
            tooltip.place_forget()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def calculate(self):
        try:
            data = {
                'current_age': int(self.entries['Current Age'].get()),
                'retirement_age': int(self.entries['Retirement Age'].get()),
                'life_expectancy': int(self.entries['Life Expectancy'].get()),
                'current_income': float(self.entries['Current Income'].get()),
                'salary_increase_pct': float(self.entries['Salary Increase (%)'].get()),
                'current_savings': float(self.entries['Current Savings'].get()),
                'annual_contrib_pct': float(self.entries['Annual Contribution (%)'].get()),
                'employer_match_pct': float(self.entries['Employer Match (%)'].get()),
                'employer_match_limit': float(self.entries['Employer Match Limit (%)'].get()),
                'expected_return': float(self.entries['Expected Return (%)'].get())
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
