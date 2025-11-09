"""
GradeBook Analyzer
Author: Subhranil Dutta
Date: November 2025
Description: A CLI-based GradeBook Analyzer for analyzing and reporting student grades.
"""

import csv


# Task 1: Project Setup

def print_welcome():
    print("\n===============================")
    print("   Welcome to GradeBook Analyzer")
    print("===============================\n")
    print("1. Enter student data manually")
    print("2. Load data from CSV file")
    print("3. Exit\n")



# Task 2: Data Entry or CSV Import

def get_data_manual():
    marks = {}
    n = int(input("Enter number of students: "))
    for _ in range(n):
        name = input("Enter student name: ")
        score = float(input(f"Enter marks for {name}: "))
        marks[name] = score
    return marks


def get_data_from_csv():
    marks = {}
    file_path = input("Enter CSV file path (e.g. data.csv): ")
    try:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header if present
            for row in reader:
                if len(row) >= 2:
                    name, score = row[0], float(row[1])
                    marks[name] = score
        print("CSV file loaded successfully!\n")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return marks



# Task 3: Statistical Analysis

def calculate_average(marks_dict):
    return sum(marks_dict.values()) / len(marks_dict) if marks_dict else 0


def calculate_median(marks_dict):
    scores = sorted(marks_dict.values())
    n = len(scores)
    if n == 0:
        return 0
    if n % 2 == 1:
        return scores[n // 2]
    else:
        return (scores[n // 2 - 1] + scores[n // 2]) / 2


def find_max_score(marks_dict):
    return max(marks_dict.values()) if marks_dict else None


def find_min_score(marks_dict):
    return min(marks_dict.values()) if marks_dict else None


# Task 4: Grade Assignment

def assign_grades(marks_dict):
    grades = {}
    for name, score in marks_dict.items():
        if score >= 90:
            grades[name] = 'A'
        elif score >= 80:
            grades[name] = 'B'
        elif score >= 70:
            grades[name] = 'C'
        elif score >= 60:
            grades[name] = 'D'
        else:
            grades[name] = 'F'
    return grades


def grade_distribution(grades):
    dist = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for grade in grades.values():
        if grade in dist:
            dist[grade] += 1
    return dist


# Task 5: Pass/Fail Filter

def pass_fail_lists(marks_dict):
    passed = [name for name, score in marks_dict.items() if score >= 40]
    failed = [name for name, score in marks_dict.items() if score < 40]
    return passed, failed


# Task 6: Results Table & Loop

def print_results_table(marks_dict, grades):
    print("\nName\t\tMarks\tGrade")
    print("----------------------------------")
    for name in marks_dict:
        print(f"{name:<15}\t{marks_dict[name]:<5}\t{grades[name]}")
    print("----------------------------------")


def main():
    while True:
        print_welcome()
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            marks = get_data_manual()
        elif choice == '2':
            marks = get_data_from_csv()
        elif choice == '3':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.\n")
            continue

        if not marks:
            print("No data found. Please try again.\n")
            continue

        # Perform analysis
        avg = calculate_average(marks)
        median = calculate_median(marks)
        max_score = find_max_score(marks)
        min_score = find_min_score(marks)

        print(f"\nAverage Marks: {avg:.2f}")
        print(f"Median Marks: {median:.2f}")
        print(f"Highest Marks: {max_score}")
        print(f"Lowest Marks: {min_score}")

        grades = assign_grades(marks)
        dist = grade_distribution(grades)
        passed, failed = pass_fail_lists(marks)

        # Display tables
        print_results_table(marks, grades)

        print("\nGrade Distribution:")
        for g, count in dist.items():
            print(f"{g}: {count} students")

        print(f"\nPassed Students ({len(passed)}): {', '.join(passed)}")
        print(f"Failed Students ({len(failed)}): {', '.join(failed)}")

        again = input("\nDo you want to run another analysis? (y/n): ")
        if again.lower() != 'y':
            print("Thank you for using GradeBook Analyzer!")
            break


if __name__ == "__main__":
    main()