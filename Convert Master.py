import csv

# Declare global vars
masterList = []
tempList = []
cleanList = []
stillActive = []
installs = []
uninstalls = []
activations = []
storeSet = set()


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


with open("apphistory.csv", 'rb') as csvfile:
    inputFile = csv.reader(csvfile, delimiter=",",quotechar="|")

    # Format is 0-date, 1-event, 2-plan, 3-billing date, 4-store name, 5-store country, 6-contact, 7-store web
    for r in inputFile:
        storeSet.add(r[4])
        masterList.append([r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7]])

    # for each row, see if that row is an install, uninstall, or activations
    # compare install to uninstall if install count is higher, than check to see if it is active to set status

cleanList.append(["Store Name","Store URL", "Install Date", "Install Status", "Active Status", "MRR", "Contact Info"])


for store in storeSet:
    stillActive[:] = []
    tempList [:] = []
    installs[:] = []
    uninstalls[:] = []
    activations[:] = []
    activeStatus = ""
    storeStatus = ""
    mrrAmount = 0.00

# TODO Logic error in the loop; its not finding all, THEN adding recent, its adding each one as it goes through.

    # Make a counter for the length of the file, put all of the instances of that store into a temp file.
    # loop through the temp file to process it, then output the final result.

    for row in masterList:
        if row[4] == store:
            tempList.append([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]])
        else:
            continue

    for t in tempList:
        if t[1] == 'ApplicationInstalledEvent':
            installs.append([t[4], t[0]])
        elif t[1] == 'ApplicationUninstalledEvent':
            uninstalls.append([t[4], t[0]])

    # Determine if the store is still installed
    if len(installs) > len(uninstalls):
        #Store is still installed
        storeStatus = "Installed"

        # Find the most recent installation date
        if len(installs) > 1:
            mostRecentInstall = isnewest(installs)[1]
        elif len(installs) == 1:
            mostRecentInstall = installs[0]

        # Determine if the store is still active
        # TODO If there are frozen or cancelled or expired charges, get the date and if any of the dates are after the newest activation then the store is not active.
        if row[1] == 'RecurringApplicationChargeActivatedEvent':
            activations.append([t[4],t[0]])
            mrrAmount = str(t[2][16:])
            activeStatus = "Active"

        # If there is more than one activation date, send to a function to find the most recent activation date
        if len(activations) == 1:
            stillActive.append(activations[0])
        elif len(activations) > 1:
            stillActive.append(isnewest(activations))

    # If the store is not still installed
    elif len(installs) <= len(uninstalls):
        # The store has been uninstalled
        storeStatus = "Uninstalled"

    #Add the information for this store to the list of stores to output
    cleanList.append([t[4],t[7],t[0],storeStatus, activeStatus, mrrAmount, t[6]])

# Output the list to a file
with open("Store List1.csv", 'a') as outcsv:
    #configure writer to write standard csv file
    writefile = csv.writer(outcsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for s in cleanList:
        writefile.writerow(s)


