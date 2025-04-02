from datetime import datetime
from time import sleep
# Get the current date and time

# Print the current date and time
while(True):
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    current_time = current_datetime.time()
    print(current_date, current_time)
    sleep(1)

print("Current date:", current_date)
print("Current time:", current_time)