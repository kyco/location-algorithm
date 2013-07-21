from main import *
import random, decimal


def randomLong(): # generate random longitude(x)
    decimal.getcontext().prec = 15
    a = 18
    b = decimal.Decimal(random.random())/40
    longitude = a + b
    return longitude

def randomLat(): # generate random latitude (y)
    decimal.getcontext().prec = 15
    a = 33
    b = decimal.Decimal(random.random())/40
    latitude = -(a + b)
    return latitude

def randomRadius(): # generate random radius (r)
    radius = random.randint(1,3)
    return radius


def randomX(): # generate random x value
    x = random.randint(0,10)
    return x

def randomY(): # generate random y value
    y = random.randint(0,10)
    return y

def randomR(): # generate random radius r
    r = random.randint(1,7)
    return r


def getFractionalPart(n):
    return n - int(n)

def getDecimalPart(n):
    return int(n)
