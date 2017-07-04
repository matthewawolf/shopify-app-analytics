#!/usr/bin/env python


import csv
import xlsxwriter
import string  # To help with the XLSX filtering
from datetime import *

# Declare global vars
masterList = []
cleanList = []
storeSet = set()


# Function to find the newest record in a list based on the dates passed in
def isnewest(someRows):
    newest = someRows[0]
    counter = 0

    for date in someRows:
        if counter < len(someRows)-1:
            if someRows[counter+1][1] > someRows[counter][1]:
                newest = someRows[counter+1]
                counter += 1
            else:
                counter += 1
    return newest

# Open the CSV file and start processing it into a list of useful content
with open("apphistory.csv", 'rb') as csvfile:
    next(csvfile)
    inputFile = csv.reader(csvfile)

    # Format is 0-date, 1-event, 2-plan, 3-billing date, 4-store name, 5-store country, 6-contact, 7-store web
    for r in inputFile:
        storeSet.add(r[4])
        masterList.append([r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]])

cleanList.append(["Store Name", "Store URL", "Install Date", "Install Status", "Active Status", "MRR", "Contact Info"])


for store in storeSet:
    stillActive = []
    tempList = []
    installs = []
    uninstalls = []
    chargeAccepted = []
    chargeExpired = []
    chargeFrozen = []
    chargeCancelled = []
    activeStatus = ""
    storeStatus = ""
    mrrAmount = 0.00

    # Put all of the instances of each store into a list.
    # loop through the temp list to process it, then output the final result.
    for row in masterList:
        if row[4] == store:
            tempList.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
        else:
            continue

    # For the store make lists for events
    for t in tempList:
        if t[1] == 'Installed':
            installs.append([t[4], t[0]])
        elif t[1] == 'Uninstalled':
            uninstalls.append([t[4], t[0]])
        elif t[1] == "Recurring charge accepted":
            chargeAccepted.append([t[4], t[0]])
        elif t[1] == "Recurring charge expired":
            chargeExpired.append([t[4], t[0]])
        elif t[1] == "Recurring charge cancelled":
            chargeCancelled.append([t[4], t[0]])
        elif t[1] == "Recurring charge frozen":
            chargeFrozen.append([t[4], t[0]])

    # If there are more installs than uninstalls then the store is still installed. If so, determine the most recent install date and if the store is active
    if len(installs) > len(uninstalls):
        # Store is still installed
        storeStatus = "Installed"

        # If the store is installed, determine the most recent events dates
        # Find the most recent install date
        if len(installs) > 1:
            mostRecentInstall = isnewest(installs)[1]
        elif len(installs) == 1:
            mostRecentInstall = installs[0]

        # Find the most recent Charge Accepted date
        if len(chargeAccepted) > 1:
            mostRecentAccepted = isnewest(chargeAccepted)[1]
        elif len(chargeAccepted) == 1:
            mostRecentAccepted = chargeAccepted[0]
        elif len(chargeAccepted) == 0:
            mostRecentAccepted = None

        # Find the most recent Charge Cancelled date
        if len(chargeCancelled) > 1:
            mostRecentCancelled = isnewest(chargeCancelled)[1]
        elif len(chargeCancelled) == 1:
            mostRecentCancelled = chargeCancelled[0]
        elif len(chargeCancelled) == 0:
            mostRecentCancelled = None

        # Find the most recent Charge Frozen date
        if len(chargeFrozen) > 1:
            mostRecentFrozen = isnewest(chargeFrozen)[1]
        elif len(chargeFrozen) == 1:
            mostRecentFrozen = chargeFrozen[0]
        elif len(chargeFrozen) == 0:
            mostRecentFrozen = None

        # Find the most recent Charge Expired date
        if len(chargeExpired) > 1:
            mostRecentExpired = isnewest(chargeExpired)[1]
        elif len(chargeExpired) == 1:
            mostRecentExpired = chargeExpired[0]
        elif len(chargeExpired) == 0:
            mostRecentExpired = None

        # Determine if the most recent event was accepting a charge and if so, how much was it. If not, then the store is not active
        mostRecentEvent = isnewest([["Installed", mostRecentInstall], ["Accepted", mostRecentAccepted], ["Cancelled", mostRecentCancelled], ["Frozen", mostRecentFrozen], ["Expired", mostRecentExpired]])
        if mostRecentEvent[0] == "Accepted":
            activeStatus = "Active"
            mrrAmount = str(t[2])[-6:].strip()
            if mrrAmount.startswith("-"):
                mrrAmount = mrrAmount[1:]

    # If the store is not still installed
    elif len(installs) <= len(uninstalls):
        # The store has been uninstalled
        storeStatus = "Uninstalled"

    # Add the information for this store to the list of stores to output
    cleanList.append([t[4], t[7], datetime.strptime(t[0], '%Y-%m-%d %H:%M:%S %Z'), storeStatus, activeStatus, mrrAmount, t[6]])


# Output the list to a csv file
with open("Store List.csv", 'wb') as outcsv:
    # Configure writer to write standard csv file
    writefile = csv.writer(outcsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for s in cleanList:
        writefile.writerow(s)



# Output the file to an Excel Spreadsheet
workbook = xlsxwriter.Workbook('Store List.xlsx', {'strings_to_numbers': True})
worksheet1 = workbook.add_worksheet('Summary')
thing = 'A1:' + string.uppercase[len(cleanList[0])-1] + '1'
worksheet1.autofilter('A1:' + string.uppercase[len(cleanList[0])-1] + '1')

# Create formatting
money = workbook.add_format({'num_format': '$#,##0.00'})
bold = workbook.add_format({'bold': True})
dateFormat = workbook.add_format({'num_format': 'mm/dd/yy'})


# Create a sheet for the summarized data
row = 0
col = 0

worksheet1.write(row, col, 'Store Name', bold)
worksheet1.write(row, col + 1, 'Store URL', bold)
worksheet1.write(row, col + 2, 'Install Date', bold)
worksheet1.write(row, col + 3, 'Install Status', bold)
worksheet1.write(row, col + 4, 'Active Status', bold)
worksheet1.write(row, col + 5, 'Current MRR', bold)
worksheet1.write(row, col + 6, 'Contact Info', bold)
row += 1


# Iterate over the data and write it out row by row.
for c in cleanList[1:]:
    worksheet1.write(row, col, c[0].decode('utf-8').strip())
    worksheet1.write(row, col + 1, c[1].decode('utf-8').strip())
    worksheet1.write(row, col + 2, c[2], dateFormat)
    worksheet1.write(row, col + 3, c[3].decode('utf-8').strip())
    worksheet1.write(row, col + 4, c[4].decode('utf-8').strip())
    worksheet1.write(row, col + 5, c[5], money)
    worksheet1.write(row, col + 6, c[6].decode('utf-8').strip())
    row += 1

# Create a sheet for the raw data
worksheet2 = workbook.add_worksheet('Raw Data')
worksheet2.autofilter('A1:' + string.uppercase[len(masterList[0])-1] + '1')


row = 0
col = 0

worksheet2.write(row, col, 'Date', bold)
worksheet2.write(row, col + 1, 'Event', bold)
worksheet2.write(row, col + 2, 'Details', bold)
worksheet2.write(row, col + 3, 'Billing on', bold)
worksheet2.write(row, col + 4, 'Shop name', bold)
worksheet2.write(row, col + 5, 'Shop country', bold)
worksheet2.write(row, col + 6, 'Shop email', bold)
worksheet2.write(row, col + 7, 'Shop domain', bold)
row += 1

for m in masterList:
    worksheet2.write(row, col, m[0], dateFormat)
    worksheet2.write(row, col + 1, m[1].decode('utf-8').strip())
    worksheet2.write(row, col + 2, m[2].decode('utf-8').strip())
    worksheet2.write(row, col + 3, m[3], dateFormat)
    worksheet2.write(row, col + 4, m[4].decode('utf-8').strip())
    worksheet2.write(row, col + 5, m[5].decode('utf-8').strip())
    worksheet2.write(row, col + 6, m[6].decode('utf-8').strip())
    worksheet2.write(row, col + 7, m[7].decode('utf-8').strip())
    row += 1


#Close the workbook
workbook.close()


