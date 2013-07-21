import calculations as cs

a = [] # inital towers array [tower, x, y, radius]
b = [] # eligilbe towers array [tower, x, y, radius]
c = [] # points of intersection array [point1, point2]

def generateTowers(howmany, whattype):
    global a
    if whattype == 'long&lat':
        for i in range(howmany):
            a.append([i, cs.randomLong(), cs.randomLat(), cs.randomRadius()])
    elif whattype == 'x&y':
        for i in range(howmany):
            a.append([i, cs.randomX(), cs.randomY(), cs.randomR()])
    else:
        print('no type specified')


def manipulateTower(tower, longitude, latitude, radius):
    global a
    a[tower-1][1] = longitude
    a[tower-1][2] = latitude
    a[tower-1][3] = radius


def findEligibleTowers():
    global a
    for i in range(len(a)):
        if a[i][1] != 0 or a[i][2] != 0 or a[i][3]:
            global b
            b.append(a[i])
            print(str(a[i][0]+1)),
    print('')


def convertLongLatToKms():
    import math
    global b
    for i in range(len(b)):
        # convert to UTM
        fractional_min_long = 60 * cs.getFractionalPart(b[i][1])
        fractional_sec_long = 60 * cs.getFractionalPart(fractional_min_long)

        degrees_long = cs.getDecimalPart(b[i][1])
        minutes_long = cs.getDecimalPart(fractional_min_long)
        seconds_long = cs.getDecimalPart(fractional_sec_long)

        fractional_min_lat = 60 * cs.getFractionalPart(b[i][2])
        fractional_sec_lat = 60 * cs.getFractionalPart(fractional_min_lat)

        degrees_lat = cs.getDecimalPart(b[i][2])
        minutes_lat = cs.getDecimalPart(fractional_min_lat)
        seconds_lat = cs.getDecimalPart(fractional_sec_lat)

        """ A degree of longitude at the equator is 111.2 kilometers.
            A minute is 1853 meters.
            A second is 30.9 meters.
            For other latitudes multiply by cos(lat). """

        # convert to meters
        x = degrees_long * 111200 + minutes_long * 1853 + seconds_long * 30.9
        y = degrees_lat * 111200 + minutes_lat * 1853 + seconds_lat * 30.9
        radius = b[i][3] * .55

        # convert to kilometers
        x_km = cs.getDecimalPart(round(x/1000))
        y_km = cs.getDecimalPart(round(y/1000))

        b[i][1] = x_km
        b[i][2] = y_km
        b[i][3] = radius


def findPtsOfIntersection(P1, r1, P2, r2):
    import math

    # P is a point (x,y) stored as a python complex
    # r is radius
    # d is distance between centres
    # h is height of triangle formed between P1 & P2 and Point of Int.
    # a is distance from P1 to P0, where P0 is point of int. between the cross-
    #   section of the two possible pts of int. and line through P1 & P2
        
    d = math.sqrt((P2.real - P1.real)**2 + (P2.imag - P1.imag)**2)

    if d > r1 + r2:
        point1 = None
        point2 = None
        print('no solution, circles are seperate')
    elif d < math.fabs(r1 - r2):
        point1 = None
        point2 = None
        print('no solution, circles contained within each other')
    elif d == 0 and r1 == r2:
        point1 = None
        point2 = None
        print('infinitely many solutions, circles are coincident')
    else:
        a = (r1**2 - r2**2 + d**2)/(2*d)

        h = math.sqrt(r1**2 - a**2)

        P0 = P1 + a * (P2 - P1) / d

        x1 = round(P0.real + h * (P2.imag - P1.imag) / d, 1)
        y1 = round(P0.imag - h * (P2.real - P1.real) / d, 1)

        x2 = round(P0.real - h * (P2.imag - P1.imag) / d, 1)
        y2 = round(P0.imag + h * (P2.real - P1.real) / d, 1)

        point1 = complex(x1, y1)
        point2 = complex(x2, y2)

        print('(' + str(point1.real) + \
              ', ' + str(point1.imag) + ') & (' + str(point2.real) + \
              ', ' + str(point2.imag) + ')')

    if point1 != None and point2 != None:
        return [point1, point2]


def findAllPtsOfIntersectionInArray():
    global b
    for i in range(len(b)):
        j = i + 1
        for j in range(len(b)):
            if b[i][0] == b[j][0]:
                break
            else:
                print('Towers ' + str(b[i][0]+1) + \
                  ' & ' + str(b[j][0]+1) + ':'),

                points = findPtsOfIntersection(complex(b[i][1],b[i][2]), b[i][3], \
                                      complex(b[j][1],b[j][2]), b[j][3])
                if points != None:
                    global c
                    c.append(points[0])
                    c.append(points[1])
                else:
                    pass


def locateCellPhone():
    # looks through all points of intersection and selects those which are
    # furthest away and discards them when calcuating an average
    all_x = 0
    all_y = 0
    j = 0
    deletepoint = []
    
    global c
    for i in range(len(c)):
        pointcounter = 0
        for j in range(len(c)):
            precision_x = 1
            precision_y = 1
            if (c[i].real > c[j].real - precision_x and c[i].real < c[j].real + precision_y) \
               and (c[i].imag > c[j].imag - precision_x and c[i].imag < c[j].imag + precision_y):
                pointcounter += 1
        if pointcounter < 2:
            deletepoint.append(c[i])

    for i in range(len(deletepoint)):
        for j in range(len(c)):
            if deletepoint[i] == c[j]:
                c.pop(j)
                c.append(None)

    howmanyNoneEntries = 0
    for i in range(len(c)):
        if c[i] != None:
            all_x += c[i].real
            all_y += c[i].imag
        else:
            howmanyNoneEntries += 1

    empties = howmanyNoneEntries

    if empties != len(c):    
        avg_x = round(all_x / (len(c) - empties), 1)
        avg_y = round(all_y / (len(c) - empties), 1)
        return (avg_x, avg_y)


def locateCellPhoneViaAverage():
    # takes all points and finds the average
    all_x = 0
    all_y = 0
    global c
    for i in range(len(c)):
        all_x += c[i].real
        all_y += c[i].imag

    avg_x = round(all_x / (len(c)), 1)
    avg_y = round(all_y / (len(c)), 1)
    
    return (avg_x, avg_y)


def convertBack(coords):
    # converts kms to back to Lat&Long
    import math

    x_km = coords[0]
    y_km = coords[1]

    x = x_km * 1000
    y = y_km * 1000

    degrees_x = x / 111200
    degrees_y = y / 111200

    location_deg = complex(degrees_x, degrees_y)

    return location_deg


def printTowersInA():
    global a
    for i in range(len(a)):
        print('Tower ' + str(a[i][0]+1) + ': ' + str(a[i][1]) + \
              ', ' + str(a[i][2]) + ', ' + str(a[i][3]))


def printTowersInB():
    global b
    for i in range(len(b)):
        print('Tower ' + str(b[i][0]+1) + ': ' + str(b[i][1]) + \
              ', ' + str(b[i][2]) + ', ' + str(b[i][3]))


if __name__ == '__main__':
    # if working with x&y coords then comment out: algorithm = lat&long
    algorithm = 'x&y'
    algorithm = 'lat&long'
    
    if algorithm == 'lat&long':        
        print('Cell phone location: UNKNOWN')
        print('\n***RANDOM TOWERS FOUND***')
        generateTowers(7, 'long&lat')    
        #manipulateTower(1,0,0,0)
        #manipulateTower(4,0,0,0)        
        printTowersInA()        
        print('\n***TOWERS SELECTED FOR ALGORITHM***')
        findEligibleTowers()        
        print("\n***CONVERTING TOWER PARAMETERS TO kms***")
        convertLongLatToKms()
        printTowersInB()
        print('\n***FINDING POINTS OF INTERSECTION***')
        findAllPtsOfIntersectionInArray()        
        print('\n***LOCATING CELL PHONE***')
        print('Cell phone location: ' + str(locateCellPhone()))
        print('Cell phone location: ' + str(convertBack(locateCellPhone())))
    else:
        print('Cell phone location: UNKNOWN')
        print('\n***RANDOM TOWERS FOUND***')
        generateTowers(7, 'x&y')
        
        manipulateTower(1,21,28,35)
        manipulateTower(2,28,70,29)
        manipulateTower(3,63,84,37)
        manipulateTower(4,63,77,32)
        manipulateTower(5,84,49,35)
        manipulateTower(6,91,21,52)
        manipulateTower(7,49,28,21)
        
        printTowersInA()        
        print('\n***TOWERS SELECTED FOR ALGORITHM***')
        findEligibleTowers()        
        print('\n***FINDING POINTS OF INTERSECTION***')
        findAllPtsOfIntersectionInArray()
        print('\n***LOCATING CELL PHONE***')
        print('Cell phone location: ' + str(locateCellPhone()))
        #print('Cell phone location: ' + str(locateCellPhoneViaAverage()))
