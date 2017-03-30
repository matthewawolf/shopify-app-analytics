import csv
from pprint import pprint
from decimal import Decimal
from datetime import datetime


# Define Arrays
# store everything
masterFile = []
# all the installs
installs = []
# final list of all uninstalls
uninstalls = []
# list of all stores that have cancelled the charge
chargeCancelled = []
# list of all the stores that have activated
chargeActivated = []
# Stores that are still installed
stillInstalled = []
# Stores that are still active
stillActive = []
# stores that are still installed but not active
notActive = []



#A unique set of stores
storeSet = set()


with open("apphistory.csv", 'rb') as csvfile:
    #open and read the file (downloaded App Export from shopify app page, rename it, and move the the same directory as the py file)
    inputFile = csv.reader(csvfile, delimiter=",",quotechar="|")

    for row in inputFile:
        #remove rows that are shopify employees or are our own test accounts
        masterFile.append(row)

        # Format is 0-date, 1-event, 2-plan, 3-billing date, 4-store name, 5-store country, 6-contact, 7-store web
        if row[1] == 'ApplicationInstalledEvent':
            installs.append(row[4])
        elif row[1] == 'ApplicationUninstalledEvent':
            uninstalls.append(row[4])
        elif row[1] == 'RecurringApplicationChargeActivatedEvent':
            chargeActivated.append(row[4])
        elif row[1] == 'RecurringApplicationChargeCancelledEvent':
            chargeCancelled.append(row[4])
        storeSet.add(row[4])


# ALL STORES THAT ARE CURRENTLY INSTALLED REGARDLESS OF ACTIVATION
def currentlyinstalledstores():
    stillInstalled[:] =[]

    # look for any stores that installed and uninstalled multiple times and if there are more installs than uninstalls
    # keep them. If there are the same number of uninstalls as installs, remove it from the installed list
    for names in storeSet:
        if installs.count(names) > uninstalls.count(names):
            stillInstalled.append(names)



# ALL CURRENTLY INSTALLED STORES THAT ARE CURRENTLY ACTIVATED
def currentactivations():
    stillActive[:] =[]

    # Get the most recent activation price and append that to the string
    # TODO: Figure out which date is the most recent
    for store in stillInstalled:
        #if the store is still installed
        if chargeActivated.count(store) > chargeCancelled.count(store):
            # Find all activations of that store with the date
            datesOfActivation = []
            myStore = store

            #fill in Dates of Activation with the dates that the store was activated on
            for item in masterFile:
                if myStore in item[4] and item[1] == 'RecurringApplicationChargeActivatedEvent':
                    datesOfActivation.append([item[4],item[0], item[7], item[2], item[6]])

            # If there is more than one activation date, send to a function to find the most recent activation date
            if len(datesOfActivation) == 1:
                    stillActive.append(datesOfActivation[0])
            elif len(datesOfActivation) > 1:
                stillActive.append(findnewestactivation(datesOfActivation))

# a function to find the most recent activation date in a list
def findnewestactivation(myList):
    newest = myList[0]
    counter = 0

    for date in myList:
       if counter < len(myList)-1:
           if myList[counter+1][1] > myList[counter][1]:
               newest = myList[counter+1]
               counter += 1
           else:
               counter += 1

    return newest


# ALL CURRENTLY INSTALLED STORES THAT ARE CURRENTLY NOT ACTIVATED
def notactivated():
    notActive[:]= []

    for store in stillInstalled:
        if chargeActivated.count(store) <= chargeCancelled.count(store):
            notActive.append(store)


#Find the MRR for all active companies
def getmrr(activeStores):
    totalMRR = 0

    for store in activeStores:
        thing = Decimal(store[3][17:])
        totalMRR += thing

    return totalMRR

def findstoretype(activeStores):
    planType = ""
    plans =[]

    for store in activeStores:
        planCost = Decimal(store[3][17:])
        if planCost == 9.00:
            planType = "Basic"
        elif planCost >= 9.00 and planCost < 29.00:
            planType = "Basic with Addon"
        elif planCost >= 29.00 and planCost < 499.00:
            planType = "Professional"
        elif planCost >= 499.00:
            planType = "Enterprise"
        plans.append([store[0],planType,str(planCost)])

    return plans

def writecsv(somelist, filename):
        filename = filename+".csv"
        with open(filename, 'a') as outcsv:
        #configure writer to write standard csv file
            writefile = csv.writer(outcsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writefile.writerow(somelist)
            for s in somelist:
                #Write item to outcsv
                writefile.writerow(s)



# A SUMMARY OF THE STORE STATS
def summary():
    print "---------------------------------"
    print 'TOTAL SUMMARY \n\n'
    print "All time installs " + str(len(storeSet))
    print "Currently Installed " + str(len(stillInstalled))
    print "Currently Active " + str(len(stillActive))
    print "Inactive Stores " + str(len(notActive))


# Make sure everything gets populated and then ask the user what they want to do
currentlyinstalledstores()


while True:
    print ""
    print ""
    print "Press 0 to Run the script through"
    print "Press 1 for Currently Installed stores"
    print "Press 2 for Stores that are currently activated"
    print "Press 3 for Installed but not active stores"
    print "Press 4 for a summary"
    print "Press 5 for for total MRR"
    print "Press 6 for Stores by Plan"
    print "Press 7 to Quit"
    userSelection = raw_input("Select an option: ")
    userSelection = int(userSelection)

    if userSelection == 0:
        currentlyinstalledstores()
        pprint (stillInstalled)
        print "Total Stores Installed: " + str(len(stillInstalled))

        saveResult = raw_input("Do you want to save this y/n? ")
        if saveResult == "y":
            writecsv(stillInstalled, "Stores Currently Installed")

    elif userSelection == 2:
        currentactivations()
        pprint (stillActive)
        print "Currently Active Stores: "+ str(len(stillActive))

        saveResult = raw_input("Do you want to save this y/n? ")
        if saveResult == "y":
            writecsv(stillActive, "Stores Still Active")


    elif userSelection == 3:
        notactivated()
        pprint (notActive)
        print "Total Inactive Stores: "+ str(len(notActive))

        saveResult = raw_input("Do you want to save this y/n? ")
        if saveResult == "y":
            writecsv(notActive, "Inactive Stores")


    elif userSelection == 4:
        currentlyinstalledstores()
        currentactivations()
        notactivated()
        print 'TOTAL SUMMARY \n\n'
        print "All time installs " + str(len(storeSet))
        print "Currently Installed " + str(len(stillInstalled))
        print "Currently Active " + str(len(stillActive))
        print "Inactive Stores " + str(len(notActive))
    elif userSelection == 5:
        currentactivations()
        print '$'+ str(getmrr(stillActive))
    elif userSelection == 6:
        currentactivations()
        pprint(findstoretype(stillActive))
    elif userSelection == 7:
        break




