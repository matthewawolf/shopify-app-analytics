
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
