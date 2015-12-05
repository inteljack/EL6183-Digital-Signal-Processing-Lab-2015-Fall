import math

def point(tick, range, radius):           # identical to plotterGui's
    angle = tick * (360.0 / range)        # but prints points and angle
    radiansPerDegree = math.pi / 180
    pointX = int( round( radius * math.sin(angle * radiansPerDegree) )) 
    pointY = int( round( radius * math.cos(angle * radiansPerDegree) ))
    print tick, ':', angle, '=', (pointX, pointY) 
    return (pointX, pointY)

def circle(points, radius, centerX, centerY):
    print '-' * 10
    for i in range(points):
        x, y = point(i+1, points, radius)
        # draw from centerX, centerY to centerX+x, centerY-y

Width = Height = 400
originX = Width / 2
originY = Height / 2

circle(4,   200, originX, originY)
circle(12,  200, originX, originY)
circle(60,  200, originX, originY)
circle(360, 200, originX, originY)
