# Author: R.D.S Mihiran
# Date: 27/11/2024
# Student ID: 20230043 / W2120344

from datetime import datetime


# Task A: 
# Date validation functions
def validate_day():
    while True:
        try:
            day = int(input("Please enter the day of the survey in the format DD: "))
            if not (1 <= day <= 31):
                print("Out of range - Values must be in the range 1 and 31.")
            else:
                return day
        except ValueError:
            print("Invalid input - Please enter numeric values only.")

def validate_month():
    while True:
        try:
            month = int(input("Please enter the month of the survey in the format MM: "))
            if not (1 <= month <= 12):
                print("Out of range - Values must be in the range 1 and 12.")
            else:
                return month
        except ValueError:
            print("Invalid input - Please enter numeric values only.")

def validate_year():
    while True:
        try:
            year = int(input("Please enter the year of the survey in the format YYYY: "))
            if not (2000 <= year <= 2024):
                print("Out of range - Values must be in the range 2000 and 2024.")
            else:
                return year
        except ValueError:
            print("Invalid input - Please enter numeric values only.")

def validate_date_input():
    while True:
        day = validate_day()
        month = validate_month()
        year = validate_year()

        # Validate leap years
        if month == 2:  # February
            if day > 29:
                print("February has at most 29 days.")
                continue
            elif day == 29:
                if not ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)):
                    print(f"{year} is not a leap year. February has only 28 days in this year.")
                    continue

        # Ensure the date is valid
        try:
            datetime(year, month, day)
        except ValueError:
            print("Invalid date - Please ensure the day is valid for the given month and year.")
            continue

        # Return the day, month, year, and formatted file name
        filedate = f"traffic_data{day:02d}{month:02d}{year}.csv"
        return day, month, year, filedate

# Task B: 
import csv
# Process the CSV file based on user input
def process_csv_data(filedate):
    # Initialize variables
    total_vehicles = 0
    total_trucks = 0
    total_ev = 0
    two_wheeled_vehicles = 0
    total_buses_elm_rab_N = 0
    total_Twojun_vehicles = 0
    total_over_speed = 0  # Initialize total_over_speed
    hr_traffic_hanley = [0] * 24
    total_rain_hr = [0] * 24
    all_bicycle = 0
    #all_elm_scooters = 0

    try:
        with open(filedate, 'r') as file:
            csv_read = csv.DictReader(file)

            # Process rows
            for row in csv_read:
                try:
                    total_vehicles += 1

                    # Increment counts based on vehicle type and conditions
                    if row['VehicleType'] == "Truck":
                        total_trucks += 1
                    if row['elctricHybrid'].strip().upper() == "TRUE":
                        total_ev += 1
                    if row['VehicleType'] in ["Bicycle", "Scooter", "motorcycle"]:
                        two_wheeled_vehicles += 1
                    if (row['JunctionName'] == "Elm Avenue/Rabbit Road" and
                        row['travel_Direction_out'] == "N" and
                        row['VehicleType'] == "Buss"):
                        total_buses_elm_rab_N += 1
                    if row['travel_Direction_in'] == row['travel_Direction_out']:
                                                total_Twojun_vehicles += 1
                    if row['VehicleType'] == "Bicycle":
                        all_bicycle += 1
                    if int(row['JunctionSpeedLimit']) < int(row['VehicleSpeed']):
                        total_over_speed += 1

                    # Calculate hour-wise data
                    hour = int(row['timeOfDay'].split(":")[0])
                    if row['JunctionName'] == "Hanley Highway/Westway":
                        hr_traffic_hanley[hour] += 1

                    # Check for rain conditions
                    if row['Weather_Conditions'] in ["Heavy Rain", "Light Rain"]:
                        total_rain_hr[hour] = True
                except (IndexError, ValueError):
                    print(f"Invalid data encountered in row: {row}")
                    continue

            # Post-processing calculations
            perc_all_trucks = round((total_trucks / total_vehicles) * 100) if total_vehicles > 0 else 0
            avg_bike_hr = all_bicycle // 24 if all_bicycle > 0 else 0
            peak_hr_vehicles = max(hr_traffic_hanley, default=0)
            total_rain = sum(1 for hr in total_rain_hr if hr)

            # Identify peak traffic hours
            peak_traffic_count = max(hr_traffic_hanley, default=0)
            peak_hours = [
                f"{hour:02d}:00-{hour+1:02d}:00"
                for hour in range(24) if hr_traffic_hanley[hour] == peak_traffic_count
            ]

            outcomes = [
                f"======================================================",
                f"---[ The opening file is {filedate} ]---",
                f"======================================================",
                f"The total number of vehicles recorded for this date is {total_vehicles}.",
                f"The total number of trucks recorded for this date is {total_trucks}.",
                f"The total number of electric vehicles for this date is {total_ev}.",
                f"The total number of two-wheeled vehicles for this date is {two_wheeled_vehicles}.",
                f"The total number of buses leaving Elm Avenue/Rabbit Road heading North is {total_buses_elm_rab_N}.",
                f"The total number of vehicles through both junctions not turning left or right is {total_Twojun_vehicles}.",
                f"The percentage of trucks among total vehicles is {perc_all_trucks}%.",
                f"The average number of bikes per hour is {avg_bike_hr}.",
                f"The total number of vehicles recorded as over the speed limit for this date is {total_over_speed}.",
                f"The highest number of vehicles in an hour on Hanley Highway/Westway is {peak_hr_vehicles}.",
                f"Most traffic was recorded during: {', '.join(peak_hours)}",
                f"The number of hours of rain for this date is {total_rain} hours.",
            ]
            return outcomes, {
                "Elm Avenue/Rabbit Road": hr_traffic_hanley,
                "Hanley Highway/Westway": hr_traffic_hanley,
            }

    except FileNotFoundError:
        print(f"Error: File {filedate} not found.")
        return [], {}

# Task C: 
# Display outcomes
def display_outcomes(outcomes):
    for outcome in outcomes:
        print(outcome)

# Create txt file
def save_outcomes_to_file(outcomes, filedate):
    try:
        filename = "results.txt"
        with open(filename, "a") as file:
            file.write(f"Analysis Results for {filedate}:\n")
            for outcome in outcomes:
                file.write(f"{outcome}\n")
            file.write("\n")
        print(f"!!! Results have been successfully saved to {filename} !!!")
    except IOError as e:
        print(f"Error saving results to file: {e}")


#Task D: 
import tkinter as tk
# Configuration for the histogram
canvas_width = 850
canvas_height = 350
bar_width = 10
spacing = 5
padding = 45

class HistogramApp:
    def __init__(self, histogram_data, date):
        self.histogram_data = histogram_data
        self.date = date

    def draw_histogram(self):
        # Create the tkinter window
        root = tk.Tk()
        root.title("Histogram")

        # Create a canvas
        canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
        canvas.pack()

        # Draw the axes
        canvas.create_line(padding, canvas_height - padding, canvas_width - padding, canvas_height - padding, width=2)
        canvas.create_line(padding, canvas_height - padding, padding, padding, width=2)
        
        # Draw hours range lable
        canvas.create_text(
        canvas_width // 3,
        canvas_height - padding // 3,  # Replace margin with padding
        text="Hours (00:00 to 24:00)",
        font=("Helvetica", 10),
        fill="black"
        )

        # Combine the data for scaling
        combined_data = self.histogram_data["Elm Avenue/Rabbit Road"] + self.histogram_data["Hanley Highway/Westway"]
        max_value = max(combined_data, default=1)  # Use default=1 to avoid division by zero
        scale = (canvas_height - 2 * padding) / max_value  # Scale factor for the bars

        # Draw the bars and labels
        for i in range(24):
            # Calculate positions
            x_green = padding + i * (bar_width * 2 + spacing)
            x_red = x_green + bar_width
            y_green = canvas_height - padding - self.histogram_data["Elm Avenue/Rabbit Road"][i] * scale
            y_red = canvas_height - padding - self.histogram_data["Hanley Highway/Westway"][i] * scale

            # Draw green bar
            canvas.create_rectangle(x_green, y_green, x_green + bar_width, canvas_height - padding, fill="lightgreen", outline="green")
            canvas.create_text(x_green + bar_width / 2, y_green - 10, text=str(self.histogram_data["Elm Avenue/Rabbit Road"][i]), font=("Arial", 8), fill="green")

            # Draw red bar
            canvas.create_rectangle(x_red, y_red, x_red + bar_width, canvas_height - padding, fill="salmon", outline="red")
            canvas.create_text(x_red + bar_width / 2, y_red - 10, text=str(self.histogram_data["Hanley Highway/Westway"][i]), font=("Arial", 8), fill="red")

            # Draw hour label
            canvas.create_text(x_green + bar_width, canvas_height - padding + 15, text=str(i), font=("Arial", 8), fill="black")

        # Add legend
        canvas.create_rectangle(canvas_width - 210, 30, canvas_width - 190, 50, fill="lightgreen", outline="green")
        canvas.create_text(canvas_width - 180, 40, text="Elm Avenue/Rabbit Road", anchor="w", font=("Arial", 10), fill="black")
        canvas.create_rectangle(canvas_width - 210, 50, canvas_width - 190, 70, fill="salmon", outline="red")
        canvas.create_text(canvas_width - 180, 60, text="Hanley Highway/Westway", anchor="w", font=("Arial", 10), fill="black")

        # Add title
        canvas.create_text(canvas_width / 2, 20, text=f"Histogram of Vehicle Frequency per Hour ({self.date})", font=("Arial", 14, "bold"), fill="black")

        # Run the tkinter loop
        root.mainloop()

#Task E:
# Main function
def main():
    while True:
        # Getting user input
        day, month, year, filedate = validate_date_input()

        # Process data
        outcomes, histogram_data = process_csv_data(filedate)
        if not outcomes:
            print("No valid data to display.")
            return

        # Displaying text outcomes
        display_outcomes(outcomes)
        save_outcomes_to_file(outcomes,filedate)

        # Generating and displaying the histogram
        app = HistogramApp(histogram_data, f"{day:02d}/{month:02d}/{year}")
        app.draw_histogram()

        # Prompt to load another dataset
        cont = input("Do you want to load another dataset? (Y/N): ").strip().upper()
        if cont != 'Y':
            print("---------------------------")
            print("|-- Exiting the program --|")
            print("---------------------------")
            break

if __name__ == "__main__":
    main()