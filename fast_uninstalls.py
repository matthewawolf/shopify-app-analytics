#!/usr/bin/env python

import csv
from datetime import *

# Declare global vars
masterList = [['Date', 'Event',	'Details', 'Billing on', 'Shop name', 'Shop country', 'Shop email',	'Shop domain']]
storeSet = set()

tempList = []
storeOutput = [["Store Name", "Store URL", "Install Date", "Uninstall Date", "Delta"]]


# Open the CSV file and start processing it into a list of useful content
with open("apphistory.csv", 'rb') as csvfile:
    next(csvfile)
    inputFile = csv.reader(csvfile)

    # Create a master list of all the events from the imported CSV
    for r in inputFile:
        storeSet.add(r[4])
        masterList.append([r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]])


for s in storeSet:
    for m in masterList:
        if m[4] == s:
            tempList.append(m)

    # Go through the list to get install and uninstall dates
    installDate = ''
    uninstallDate = ''
    countInstall = 0
    countUninstall = 0
    for t in tempList:
        if t[1] == 'Installed':
            if isinstance(installDate, str):
                installDate = datetime.strptime(t[0], "%Y-%m-%d %H:%M:%S %Z")
                countInstall += 1
            else:
                if installDate < datetime.strptime(t[0], "%Y-%m-%d %H:%M:%S %Z"):
                    installDate = datetime.strptime(t[0], "%Y-%m-%d %H:%M:%S %Z")
                    countInstall += 1

        elif t[1] == 'Uninstalled':
            if isinstance(uninstallDate, str):
                uninstallDate = datetime.strptime(t[0], "%Y-%m-%d %H:%M:%S %Z")
                countUninstall += 1
            else:
                if uninstallDate < datetime.strptime(t[0], "%Y-%m-%d %H:%M:%S %Z"):
                    uninstallDate = datetime.strptime(t[0], "%Y-%m-%d %H:%M:%S %Z")
                    countUninstall +=1

    if (countInstall > 0) and (countUninstall > 0) and (countInstall == countUninstall):
        storeOutput.append([t[4], t[7], installDate, uninstallDate, (uninstallDate - installDate).days])

    # Clear the list for the next store
    tempList[:] = []


# Save the file
with open("Uninstalls.csv", 'wb') as outcsv:
    # Configure writer to write standard csv file
    writefile = csv.writer(outcsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for s in storeOutput:
        writefile.writerow(s)

