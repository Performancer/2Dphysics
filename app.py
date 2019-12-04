#!/usr/bin/env python3
import lib.vector as vec
import lib.polygon as pol
from matplotlib import pyplot
from matplotlib import animation

pola = pol.Polygon(1, 0, 4, 1)
polb = pol.Polygon(3, 1, 4, 1)
polb.position = vec.Vector(-4,-4,0)
pola.position = vec.Vector(5,5,0)
print('Collision?: ' + str(pola.CollidesWithOtherPolygon(polb)))
fig = pyplot.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = pyplot.axes(xlim=(0, 10), ylim=(0, 10))

points = pola.getVertices()
patch = pyplot.Polygon(pola.getVertices())

def init():
    ax.add_patch(patch)
    return patch,

def animate(i):
    pola.update(20 / 1000, 9.81)
    pola.angular += 0.1
    patch.set_xy(pola.getVertices())
    return patch,



anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               interval=20,
                               blit=True)

pyplot.show()
