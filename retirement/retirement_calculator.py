import json
import matplotlib.pyplot as plt
import tax_bracket

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

def load_user_data(filename='user_data.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def get_user_data():
    previous_data = load_user_data()
    if previous_data:
        print("Do you want to use any of the last 3 iterations?")
        for i, data in enumerate(previous_data, 1):
            print(f"{i}: {data}")
        choice = input("Enter the number of the iteration to reuse (or press Enter to enter new data): ")
        if choice.isdigit() and 1 <= int(choice) <= len(previous_data):
            return previous_data[int(choice) - 1]

    data = {}
    data['current_age'] = int(input("Enter your current age: "))
    data['retirement_age'] = int(input("Enter your desired retirement age: "))
    data['life_expectancy'] = int(input("Enter your life expectancy age: "))  # New input for life expectancy
    data['current_income'] = float(input("Enter your current income: "))
    data['salary_increase_pct'] = float(input("Enter your expected annual salary increase percentage (e.g., 8 for 8%): "))
    data['current_savings'] = float(input("Enter your current retirement savings: "))
    data['annual_contrib_pct'] = float(input("Enter the percentage of your income you plan to contribute annually (e.g., 10 for 10%): "))
    data['employer_match_pct'] = float(input("Enter your employer match percentage (e.g., 5 for 5%): "))
    data['employer_match_limit'] = float(input("Enter your employer match limit as a percentage of your salary (e.g., 5 for 5%): "))
    data['tax_bracket'] = tax_bracket.get_tax_bracket(data['current_income'])
    data['expected_return'] = float(input("Enter your expected annual return on investments (e.g., 7 for 7%): "))

    save_user_data(data)
    return data

def calculate_future_value(pv, rate, nper):
    return pv * ((1 + rate) ** nper)

def calculate_annual_contribution(income, contrib_pct, employer_match_pct, employer_match_limit):
    employee_contrib = income * (contrib_pct / 100)
    employer_contrib = min(income * (employer_match_limit / 100), employee_contrib) * (employer_match_pct / 100)
    return employee_contrib + employer_contrib

def project_savings(data):
    years_to_retirement = data['retirement_age'] - data['current_age']
    future_income = data['current_income']
    future_savings = data['current_savings']
    savings_over_time = []

    print(f"Initial Savings: {future_savings}")
    
    # Project savings until retirement
    for year in range(years_to_retirement):
        annual_contribution = calculate_annual_contribution(
            future_income,
            data['annual_contrib_pct'],
            data['employer_match_pct'],
            data['employer_match_limit']
        )
        future_savings = (future_savings + annual_contribution) * (1 + data['expected_return'] / 100)
        savings_over_time.append(future_savings)
        future_income *= (1 + data['salary_increase_pct'] / 100)
        print(f"Year {year + 1}: Savings {future_savings}")

    # Project withdrawals until life expectancy
    years_in_retirement = data['life_expectancy'] - data['retirement_age']
    annual_withdrawal = calculate_annual_withdrawal(future_savings, years_in_retirement, data['expected_return'] / 100)
    print(f"Annual Withdrawal Amount: {annual_withdrawal}")

    for year in range(years_in_retirement):
        future_savings = (future_savings - annual_withdrawal) * (1 + data['expected_return'] / 100)
        if future_savings < 0:
            future_savings = 0
        savings_over_time.append(future_savings)
        print(f"Year {year + 1 + years_to_retirement}: Savings {future_savings}")

    return future_savings, savings_over_time

def calculate_annual_withdrawal(future_savings, years, rate):
    if rate == 0:
        return future_savings / years
    annuity_factor = (1 - (1 + rate) ** -years) / rate
    annual_withdrawal = future_savings / annuity_factor
    print(f"Annuity Factor: {annuity_factor}, Annual Withdrawal: {annual_withdrawal}")
    return annual_withdrawal

def plot_savings_growth(savings_over_time, current_age, life_expectancy):
    years = list(range(current_age, life_expectancy + 1))  # Include the life expectancy year
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
    user_data = get_user_data()
    projected_savings, savings_over_time = project_savings(user_data)
    print(f"Projected savings at age {user_data['retirement_age']}: ${projected_savings:,.2f}")
    
    # Calculate the annual withdrawal amount
    retirement_years = user_data['life_expectancy'] - user_data['retirement_age']
    annual_withdrawal = calculate_annual_withdrawal(projected_savings, retirement_years, user_data['expected_return'] / 100)
    print(f"Annual withdrawal amount to deplete savings by age {user_data['life_expectancy']}: ${annual_withdrawal:,.2f}")
    
    recommendations = provide_recommendations(user_data, projected_savings)
    for rec in recommendations:
        print(f"- {rec}")
    
    plot_savings_growth(savings_over_time, user_data['current_age'], user_data['life_expectancy'])

if __name__ == "__main__":
    main()