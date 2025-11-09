# Name:Subhranil Dutta
# Date: 29/10/2025
# Project Title: Daily Calorie Tracker CLI

print(
      "This mini project aims to help them build a Python-based CLI (Command Line Interface) tool "
      "where they can log their meals and keep track of total calories consumed, "
      "compare against a personal daily limit, and save session logs for future tracking.")

# Input total number of meals
total_meals = int(input("Enter the total number of meals you want to enter: "))

# Lists for meals and calories
M = []
C = []

for i in range(total_meals):
    meal = input(f"Enter the name of meal {i+1}: ")
    calorie_amount = int(input(f"Enter the total number of calories in {meal}: "))
    M.append(meal)
    C.append(calorie_amount)

# Calculate total and average of calories
total_calories = sum(C)
avg_calories = total_calories / total_meals

# Get daily calorie limit
daily_limit = int(input("Enter your daily total calorie limit: "))

# Compare
if daily_limit < total_calories:
    print(" WARNING! Your total calorie intake is more than your daily limit!")
else:
    print("SUCCESS! Your total calorie intake is within your daily limit!")

# Display summary
print("\nMeal Name\tCalories")
print("-------------------------")
for i in range(total_meals):
    print(f"{M[i]}\t\t{C[i]}")
print("-------------------------")
print(f"Total:\t\t{total_calories}")
print(f"Average:\t{avg_calories:.2f}")

# Save report option
report = input("\nDo you want to save the report? (yes/no): ").strip().lower()
date = input("Enter today's date (DD/MM/YYYY): ")

if report == "yes":
    with open("calorie_log.txt", "w") as f:
        f.write(f"Date: {date}\n")
        f.write("Meal Name\tCalories\n")
        f.write("-------------------------\n")
        for i in range(total_meals):
            f.write(f"{M[i]}\t\t{C[i]}\n")
        f.write("-------------------------\n")
        f.write(f"Total:\t\t{total_calories}\n")
        f.write(f"Average:\t{avg_calories:.2f}\n")
        if daily_limit < total_calories:
            f.write("STATUS: WARNING! You exceeded your daily calorie limit.\n")
        else:
            f.write("STATUS: SUCCESS! You are within your daily calorie limit.\n")
    print("UPLOAD COMPLETED! Report saved as 'calorie_log.txt'.")
else:
    print("Report not saved.")