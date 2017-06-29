import csv

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
        mostRecentEvent = isnewest([["Installed",mostRecentInstall], ["Accepted", mostRecentAccepted], ["Cancelled", mostRecentCancelled], ["Frozen", mostRecentFrozen], ["Expired", mostRecentExpired]])
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
    cleanList.append([t[4], t[7], t[0], storeStatus, activeStatus, mrrAmount, t[6]])


# Output the list to a file
with open("Store List.csv", 'wb') as outcsv:
    # Configure writer to write standard csv file
    writefile = csv.writer(outcsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for s in cleanList:
        writefile.writerow(s)


