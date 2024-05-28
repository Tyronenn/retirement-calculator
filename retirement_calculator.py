import json
import matplotlib.pyplot as plt
import tax_bracket

class RetirementCalculator:
    def __init__(self):
        self.user_data = None

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

    @staticmethod
    def project_savings(data):
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

def main():
    calculator = RetirementCalculator()
    user_data = calculator.get_user_data()
    projected_savings, savings_over_time = calculator.project_savings(user_data)
    print(f"Projected savings at age {user_data['retirement_age']}: ${projected_savings:,.2f}")
    
    retirement_years = user_data['life_expectancy'] - user_data['retirement_age']
    annual_withdrawal = calculator.calculate_annual_withdrawal(projected_savings, retirement_years, user_data['expected_return'] / 100)
    print(f"Annual withdrawal amount to deplete savings by age {user_data['life_expectancy']}: ${annual_withdrawal:,.2f}")
    
    recommendations = calculator.provide_recommendations(user_data, projected_savings)
    for rec in recommendations:
        print(f"- {rec}")
    
    calculator.plot_savings_growth(savings_over_time, user_data['current_age'], user_data['life_expectancy'])

if __name__ == "__main__":
    main()