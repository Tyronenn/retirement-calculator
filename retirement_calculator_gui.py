import tkinter as tk
from tkinter import messagebox
from retirement_calculator import RetirementCalculator  # Importing the class from retirement_calculator.py

class RetirementCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Retirement Calculator")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Current Age:").grid(row=0, column=0)
        self.current_age_entry = tk.Entry(self.root)
        self.current_age_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Retirement Age:").grid(row=1, column=0)
        self.retirement_age_entry = tk.Entry(self.root)
        self.retirement_age_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Life Expectancy:").grid(row=2, column=0)
        self.life_expectancy_entry = tk.Entry(self.root)
        self.life_expectancy_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Current Income:").grid(row=3, column=0)
        self.current_income_entry = tk.Entry(self.root)
        self.current_income_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Salary Increase (%):").grid(row=4, column=0)
        self.salary_increase_entry = tk.Entry(self.root)
        self.salary_increase_entry.grid(row=4, column=1)

        tk.Label(self.root, text="Current Savings:").grid(row=5, column=0)
        self.current_savings_entry = tk.Entry(self.root)
        self.current_savings_entry.grid(row=5, column=1)

        tk.Label(self.root, text="Annual Contribution (%):").grid(row=6, column=0)
        self.annual_contrib_entry = tk.Entry(self.root)
        self.annual_contrib_entry.grid(row=6, column=1)

        tk.Label(self.root, text="Employer Match (%):").grid(row=7, column=0)
        self.employer_match_entry = tk.Entry(self.root)
        self.employer_match_entry.grid(row=7, column=1)

        tk.Label(self.root, text="Employer Match Limit (%):").grid(row=8, column=0)
        self.employer_match_limit_entry = tk.Entry(self.root)
        self.employer_match_limit_entry.grid(row=8, column=1)

        tk.Label(self.root, text="Expected Return (%):").grid(row=9, column=0)
        self.expected_return_entry = tk.Entry(self.root)
        self.expected_return_entry.grid(row=9, column=1)

        self.calculate_button = tk.Button(self.root, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=10, column=0, columnspan=2)

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
