import csv
import os

course_code = "CSE101"
batch = "2022"

attendance = [['amogh', 11, 28], ['umang', 14, 26], ['test', 0, 7]]
download_path = os.path.join(os.path.join(os.path.expanduser('~'), 'Downloads'), f'Attendance_Report_{course_code}_{batch}.csv')

for row in attendance:
    percentage = (row[1] / row[2]) * 100 if row[2] != 0 else 0
    row.append(round(percentage, 2)) 

with open(download_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Present', 'Total', 'Percentage'])
    writer.writerows(attendance)