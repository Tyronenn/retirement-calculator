import json
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import dependencies.tax_bracket as tax_bracket

class RetirementCalculator:
    def __init__(self):
        self.user_data = None
        self.config = self.load_config()

    @staticmethod
    def load_config(filename='config.json'):
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file '{filename}' not found.")

    @staticmethod
    def save_user_data(data, filename='user_data.json'):
        try:
            with open(filename, 'r') as file:
                stored_data = json.load(file)
        except FileNotFoundError:
            stored_data = []

        stored_data.append(data)
        if len(stored_data) > 3:
            stored_data = stored_data[-3:]

        with open(filename, 'w') as file:
            json.dump(stored_data, file, indent=4)

    @staticmethod
    def load_user_data(filename='user_data.json'):
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    @staticmethod
    def get_user_data():
        previous_data = RetirementCalculator.load_user_data()
        if previous_data:
            print("Do you want to use any of the last 3 iterations?")
            for i, data in enumerate(previous_data, 1):
                print(f"{i}: {data}")
            choice = input("Enter the number of the iteration to reuse (or press Enter to enter new data): ")
            if choice.isdigit() and 1 <= int(choice) <= len(previous_data):
                return previous_data[int(choice) - 1]

        data = {}
        try:
            data['current_age'] = int(input("Enter your current age: "))
            data['retirement_age'] = int(input("Enter your desired retirement age: "))
            data['life_expectancy'] = int(input("Enter your life expectancy age: "))  # New input for life expectancy
            data['current_income'] = float(input("Enter your current income: "))
            data['salary_increase_pct'] = float(input("Enter your expected annual salary increase percentage (e.g., 8 for 8%): "))
            data['current_savings'] = float(input("Enter your current retirement savings: "))
            data['annual_contrib_pct'] = float(input("Enter the percentage of your income you plan to contribute annually (e.g., 10 for 10%): "))
            data['employer_match_pct'] = float(input("Enter your employer match percentage (e.g., 5 for 5%): "))
            data['employer_match_limit'] = float(input("Enter your employer match limit: "))
            data['expected_return'] = float(input("Enter the expected annual return on your investments (e.g., 7 for 7%): "))
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter the correct data type.")
            return RetirementCalculator.get_user_data()  # Retry input

        RetirementCalculator.save_user_data(data)
        return data

    def calculate_taxes(self, income):
        tax_rate = tax_bracket.get_tax_bracket(income) / 100
        return income * tax_rate

    def project_savings(self, data):
        current_age = data['current_age']
        retirement_age = data['retirement_age']
        life_expectancy = data['life_expectancy']
        current_income = data['current_income']
        salary_increase_pct = data['salary_increase_pct'] / 100
        current_savings = data['current_savings']
        annual_contrib_pct = data['annual_contrib_pct'] / 100
        employer_match_pct = data['employer_match_pct'] / 100
        employer_match_limit = data['employer_match_limit']
        expected_return = data['expected_return'] / 100

        years_to_retirement = retirement_age - current_age
        savings_over_time = []

        for year in range(years_to_retirement):
            contribution = current_income * annual_contrib_pct
            employer_match = min(contribution, current_income * employer_match_limit / 100) * employer_match_pct
            total_contribution = contribution + employer_match
            current_savings += total_contribution
            current_savings *= (1 + expected_return)
            current_income *= (1 + salary_increase_pct)
            after_tax_income = current_income - self.calculate_taxes(current_income)
            savings_over_time.append(current_savings)

        return current_savings, savings_over_time

    @staticmethod
    def calculate_annual_withdrawal(total_savings, years, return_rate):
        if return_rate == 0:
            return total_savings / years
        return total_savings * return_rate / (1 - (1 + return_rate) ** -years)

    @staticmethod
    def plot_savings_growth(savings_over_time, current_age, life_expectancy):
        years = list(range(current_age, life_expectancy + 1))
        if len(years) > len(savings_over_time):
            years = years[:len(savings_over_time)]
        plt.figure(figsize=(10, 6))
        plt.plot(years, savings_over_time, label='Projected Savings')
        plt.xlabel('Age')
        plt.ylabel('Savings ($)')
        plt.title('Projected Retirement Savings Growth Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()

    @staticmethod
    def provide_recommendations(data, future_savings):
        recommendations = []
        if future_savings < 1_000_000:
            recommendations.append("Increase your annual contributions to retirement accounts.")
            recommendations.append("Consider investing in low-cost index funds to maximize returns.")
        else:
            recommendations.append("Your retirement savings projections look good. Continue with your current strategy.")
            recommendations.append("You might want to diversify your investments to manage risk.")
        
        return recommendations

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
