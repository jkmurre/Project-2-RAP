import csv
import datetime

one_month_dict = {
  "KAN": 2,
  "KAE": 1,
  "EAN": 2,
  "EAE": 1,
  "PAE": 2,
  "PAN": 3,
  "CAE": 2,
  "CAN": 3,
  "NAE": 2,
  "NAN": 3,
  "EBE": 1,
  "PBE": 1,
  "KBE": 1,
  "ISS": 10, #Folks missing their crew codes should stand out...
  "PIN": 0
}

three_month_dict = {
  "KAN": 5,
  "KAE": 3,
  "EAN": 5,
  "EAE": 3,
  "PAE": 5,
  "PAN": 8,
  "CAE": 5,
  "CAN": 8,
  "NAE": 5,
  "NAN": 8,
  "EBE": 3,
  "PBE": 2,
  "KBE": 2,
  "ISS": 30, #Folks missing their crew codes should stand out...
  "PIN": 0,
}

month_nums = {
  "October":1,
  "November":2,
  "December":3,
  "January":4,
  "February":5,
  "March":6,
  "April":7,
  "May":8,
  "June":9,
  "July":10,
  "August":11,
  "September":12
}

today = datetime.date.today()
first_day_of_this_month = datetime.date(today.year, today.month, 1)
last_day_of_previous_month = first_day_of_this_month - datetime.timedelta(days=1)
previous_month = last_day_of_previous_month.strftime('%B')

# NOTE: Someone is on probation if they have failed their one and three month. If the member fails again, then they are on regression.
# TODO: Sort outputs by pass/fail, yes/no. Oooh, use radio buttons to apply filters! 

# TODO: Use recurssion to clean things up...
# TODO: Either clean things up by putting all the functions into another file, or using OOP in another file. 

def one_month_lookback(flight_counts, crew_code):
  if crew_code in one_month_dict:
    flights_required = one_month_dict[crew_code]
    month_number = month_nums[previous_month] - 1 #Element numbers start with 0, so set the month # back 1...
    flights_flown = int(flight_counts[month_number]) #Process row list with the flight counts using the month #.
    if flights_flown < flights_required: #If the flights flown is less than the flights required...
      return "FAIL"
    elif flights_flown >= flights_required:
      return "PASS"
    else:
      return "ERROR"

def three_month_lookback(flight_counts, crew_code):
  if crew_code in three_month_dict:
    flights_required = three_month_dict[crew_code]
    month1 = month_nums[previous_month] - 1
    month2 = month_nums[previous_month] - 2
    month3 = month_nums[previous_month] - 3
    flights_flown_month1 = int(flight_counts[month1])
    flights_flown_month2 = int(flight_counts[month2])
    flights_flown_month3 = int(flight_counts[month3])
    flights_flown_sum = flights_flown_month1 + flights_flown_month2 + flights_flown_month3
    if flights_flown_sum < flights_required:
      return "FAIL"
    elif flights_flown_sum >= flights_required:
      return "PASS"
    else:
      return "ERROR"

def probation(flight_counts, crew_code):
  if one_month_lookback(flight_counts, crew_code) == "PASS":
    one_month_status = "PASS"
  elif one_month_lookback(flight_counts, crew_code) == "FAIL":
    one_month_status = "FAIL"
  else:
    one_month_status = "ERROR"
  if three_month_lookback(flight_counts, crew_code) == "PASS":
    three_month_status = "PASS"
  elif three_month_lookback(flight_counts, crew_code) == "FAIL":
    three_month_status = "FAIL"
  else:
    three_month_status = "ERROR"
  if one_month_status and three_month_status == "FAIL":
    probation_status = "YES"
    return probation_status
  else:
    probation_status = "NO"
    return probation_status

def regression(flight_counts,crew_code):
  if one_month_lookback(flight_counts,crew_code) and three_month_lookback(flight_counts,crew_code) == "FAIL":
    flights_required = three_month_dict[crew_code]
    prev_month1 = month_nums[previous_month] - 2 
    prev_month2 = month_nums[previous_month] - 3
    prev_month3 = month_nums[previous_month] - 4
    month1_flights = int(flight_counts[prev_month1])
    month2_flights = int(flight_counts[prev_month2])
    month3_flights = int(flight_counts[prev_month3])
    sum = month1_flights + month2_flights + month3_flights
    if sum < flights_required:
      return "YES"
    else:
      return "NO"
  else:
    return "NO"    

def main():
  print("1: Run EOM RAP Report")
  selection = int(input("Select an operation: "))
  while selection in [1, 2, 3, 4]:
    if selection == 1:
      print(f"Running EOM RAP Report for {previous_month}")
      try:
        input_file = input("Enter input file name (.csv): ")
        with open(input_file, 'r') as csvfile: #Open input file.Open inp
          reader = csv.reader(csvfile) #Generate csv read file.
          i = 0
          for row in reader:
            i += 1
            if i >= 3: #Skip the headers in the CSV file.
              name = row[0]
              # Extract crew code from the first element of the row
              crew_code = row[1][1:4]
              full_crew_code = row[1]
              # Extract flight counts for each month starting from October
              flight_counts = row[2:14]
              print(f"{i - 2} Name: {name}, Code: {full_crew_code}, 1-Month: {one_month_lookback(flight_counts,crew_code)}, 3-Month: {three_month_lookback(flight_counts, crew_code)}, Probation: {probation(flight_counts, crew_code)}, Regression: {regression(flight_counts, crew_code)}")
      except FileNotFoundError:
        print("File not found. Please check the file name and try again...")
      except Exception as e:
        print(f"An error occurred: {e}. Please check the file format and try again...")
      break
    else:
      print("Please enter a valid selection: [1,2,3,4]")
      break

if __name__ == "__main__":
  main()