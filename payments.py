import csv
from datetime import *
import xlsxwriter


# Global vars
sumTotal = 0.0
sumPayments = 0
storeSet = set()
masterList = []
output = []  # Will be [0] Store Name, [1] Total Amount Paid, [2] Number of payments, [3] First Payment Date, [4] Last payment date


# Import the data from the CSV File
with open("payments.csv", 'rb') as csvfile:
    next(csvfile)
    inputFile = csv.reader(csvfile)

    # Create lists to work wtih
    # Format is [0] Payment Duration, [1] Payment Date, [2] Shop, [3] Charge Creation Time, [4] Charge Type, [5] Amount, [6] App Title
    for r in inputFile:
        storeSet.add(r[2])
        masterList.append([r[0], r[1], r[2], r[3], r[4], r[5], r[6]])

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
    writefile.writerow(['Store', 'Total Amount', 'Number of Payments', 'First Payment', 'Last Payment'])
    for o in output:
        writefile.writerow(o)

# Output the file to an Excel Spreadsheet
workbook = xlsxwriter.Workbook('Payments from Stores2.xlsx')
worksheet1 = workbook.add_worksheet('summary')

# Create formatting
money = workbook.add_format({'num_format': '$#,##0.00'})
bold = workbook.add_format({'bold': True})


# Create a sheet for the summarized data
del o
row = 0
col = 0
worksheet1.write(row, col, 'Store', bold)
worksheet1.write(row, col + 1, 'Total Amount', bold)
worksheet1.write(row, col + 2, 'Number of Payments', bold)
worksheet1.write(row, col + 3, 'First Payment Date', bold)
worksheet1.write(row, col + 4, 'Last Payment Date', bold)
row += 1

# Iterate over the data and write it out row by row.
for o in (output):
    for c in o:
        worksheet1.write(row, col, o[0])
        worksheet1.write(row, col + 1, o[1], money)
        worksheet1.write(row, col + 2, o[2])
        worksheet1.write(row, col + 3, o[3])
        worksheet1.write(row, col + 4, o[4])
    row += 1


# Create a sheet for the raw data
worksheet2 = workbook.add_worksheet('Raw Data')
row = 0
col = 0
del m
worksheet2.write(row, col, 'Payment Duration', bold)
worksheet2.write(row, col + 1, 'Payment Date', bold)
worksheet2.write(row, col + 2, 'Store', bold)
worksheet2.write(row, col + 3, 'Charge Creation Time', bold)
worksheet2.write(row, col + 4, 'Charge Type', bold)
worksheet2.write(row, col + 5, 'Amount', bold)
worksheet2.write(row, col + 4, 'App Title', bold)
row += 1

for m in masterList:
    worksheet2.write(row, col, m[0])
    worksheet2.write(row, col + 1, m[1])
    worksheet2.write(row, col + 2, m[2])
    worksheet2.write(row, col + 3, m[3])
    worksheet2.write(row, col + 4, m[4])
    worksheet2.write(row, col + 5, float(m[5]), money)
    worksheet2.write(row, col + 6, m[6])
    row += 1


#Close the workbook
workbook.close()

