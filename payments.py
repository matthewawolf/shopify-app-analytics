import csv
from datetime import *
import xlsxwriter


# Global vars
sumTotal = 0.0
sumPayments = 0
storeSet = set()
masterList = [['Payment Duration', 'Payment Date', 'Shop', 'Charge Creation Time', 'Charge Type', 'Partner Share', 'App Title']]
output = [['Store', 'Total Amount', 'Number of Payments', 'First Payment', 'Last Payment']]  # Will be [0] Store Name, [1] Total Amount Paid, [2] Number of payments, [3] First Payment Date, [4] Last payment date


# Import the data from the CSV File
with open("payments.csv", 'rb') as csvfile:
    next(csvfile)
    inputFile = csv.reader(csvfile)

    # Create lists to work wtih
    # Format is [0] Payment Duration, [1] Payment Date, [2] Shop, [3] Charge Creation Time, [4] Charge Type, [5] Amount, [6] App Title
    for r in inputFile:
        storeSet.add(r[2])
        masterList.append([r[0], r[1], r[2], r[3], r[4], float(r[5]), r[6]])

# Go through each store and sum the amount paid, the number of times they paid, then determine the first and last payment date
for s in storeSet:
    totalPaid = 0.0
    numPayments = 0
    payoutDates = []

    for m in masterList:
        if s == m[2]:
            totalPaid += float(m[5])
            numPayments += 1
            payoutDates.append(datetime.strptime(m[1], '%Y-%m-%d %H:%M:%S %Z'))
            continue
    sumTotal += totalPaid
    sumPayments += numPayments
    firstPayout = str(min(payoutDates))[:-9]
    lastPayout = str(max(payoutDates))[:-9]
    output.append([s, round(totalPaid, 2), numPayments, str(firstPayout), str(lastPayout)])


# Create a final row of Totals
output.append(['Totals', round(sumTotal, 2), sumPayments, '', ''])

# Output the list to a csvfile
with open("payments by store.csv", 'wb') as outcsv:
    # Configure writer to write standard csv file
    writefile = csv.writer(outcsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for o in output:
        writefile.writerow(o)




# Output the file to an Excel Spreadsheet
workbook = xlsxwriter.Workbook('Payments by Store.xlsx')
# Set formatting
money = workbook.add_format({'num_format': '$#,##0.00'})
bold = workbook.add_format({'bold': True})
dateFormat = workbook.add_format({'num_format': 'mm/dd/yy'})




#Create a summary sheet
worksheet1 = workbook.add_worksheet('Summary')
row = 0
t = bold
# Write the data.
for o in output:
    col = 0
    for r in o:
        if isinstance(r, str):
            r = r.decode('utf-8').strip()
        elif isinstance(r, datetime):
            t = dateFormat
        elif isinstance(r, float):
            t = money
        worksheet1.write(row, col, r, t)
        col += 1
    row += 1
    t = ''

# Create a raw data sheet
worksheet2 = workbook.add_worksheet('Raw Data')
row = 0
t = bold
# Write the data.
for m in masterList:
    col = 0
    t = ''
    for r in m:
        if isinstance(r, str):
            r = r.decode('utf-8').strip()
        elif isinstance(r, datetime):
            t = dateFormat
        elif isinstance(r, float):
            t = money
        worksheet2.write(row, col, r, t)
        col += 1
    row += 1


# Close the workbook
workbook.close()

