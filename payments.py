import csv
from datetime import *


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

# Output the list to a file
with open("payments by store.csv", 'wb') as outcsv:
    # Configure writer to write standard csv file
    writefile = csv.writer(outcsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writefile.writerow(['Store', 'Total Amount', 'Number of Payments', 'First Payment', 'Last Payment'])
    for o in output:
        writefile.writerow(o)




