###############################################################################
# per a mathematician - just an algebraic simplification:  3 ops vs 4
# [i * (360.0 / range)] * (pi / 180)
# [i * (360.0 / range) * pi] / 180
# [i * (2 / range) * pi]
# [(i / range) * 2 * pi]
# also: swapped cos and sin
# 
# >Oh, I didn't check direction.  In fact if you care about the order and the
# >origin, mine is probably wrong.
# >x=cos, y=sin starts at the rightmost point and moves counterclockwise.  If
# >you want it to be clockwise from the top, you need
# >x=cos(pi/2-angle), y=sin(pi/2-angle)
#############################################################################


from math import cos, sin, pi

def circle(numpoints, radius, centerX, centerY):
  print '-' * 10
  for i in range(numpoints):
     angle = i / float(numpoints) * 2 * pi  # in radians
     x = int(round(radius * cos(angle)))
     y = int(round(radius * sin(angle)))
     print i+1, ':', angle, '=', (x,y)
     # draw from centerX, centerY to centerX+x, centerY-y

Width = Height = 400
originX = Width / 2
originY = Height / 2

circle(4,   200, originX, originY)
circle(12,  200, originX, originY)
circle(60,  200, originX, originY)
circle(360, 200, originX, originY)
