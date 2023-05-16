import math

radius = 160
g=9.8

def toRadian(theta):
    return theta * math.pi / 180


def toDegrees(theta):
    return theta * 180 / math.pi


def getGradient(p1, p2):
    if p1[0] == p2[0]:
        m = toRadian(90)
    else:
        m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    return m


def getAngleFromGradient(gradient):
    return math.atan(gradient)


def getAngle(pos, origin):
    m = getGradient(pos, origin)
    thetaRad = getAngleFromGradient(m)
    theta = round(toDegrees(thetaRad), 2)
    return theta


def getPosOnCircumeference(theta, origin):
    theta = toRadian(theta)
    x = origin[0] + radius * math.cos(theta)
    y = origin[1] + radius * math.sin(theta)
    return (x, y)

def timeOfFlight(u, theta):
    return round((2 * u * math.sin(theta)) / g, 2)


def getRange(u, theta):
    range_ = ((u ** 2) * 2 * math.sin(theta) * math.cos(theta)) / g
    return round(range_, 2)


def getMaxHeight(u, theta):
    h = ((u ** 2) * (math.sin(theta)) ** 2) / (2 * g)
    return round(h, 2)
