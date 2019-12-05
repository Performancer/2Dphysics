#!/usr/bin/env python3
import lib.vector as vec
import lib.polygon as pol
from matplotlib import pyplot
from matplotlib import animation

polygons = []

polygons.append(pol.Polygon(1, 3, 1, 5))
polygons[0].position = vec.Vector(2,5,0)
polygons[0].velocity = vec.Vector(10,0,0)
polygons[0].angle = 4

polygons.append(pol.Polygon(1, 3, 1, 7))
polygons[1].position = vec.Vector(8,5,0)

fig = pyplot.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = pyplot.axes(xlim=(-4, 14), ylim=(-4, 14))

def handleVertices(vertices):
    handled = []
    for i in range(0, len(vertices)):
        handled.append([vertices[i].x, vertices[i].y])
    return handled

patches = []
patches.append(pyplot.Polygon(handleVertices(polygons[0].getVertices())))
patches.append(pyplot.Polygon(handleVertices(polygons[1].getVertices())))
contact = pyplot.Circle((-1, -1), 0.1, color='r')

def init():
    ax.add_patch(patches[0])
    ax.add_patch(patches[1])
    ax.add_patch(contact)
    return []

def animate(i, contact, square, triangle):
    for pol in polygons:
        pol.update(10 / 1000, 9.81)
        for other in polygons:
            if other is not pol:
                if pol.collides(other) and other.collides(pol):
                    collision = polygons[0].onCollision(polygons[1])
                    contact.center = (collision.x, collision.y)

        if pol.collidesWithFloor(-2):
            pol.onFloorCollision(-2)
        if pol.collidesWithCeiling(12):
            pol.onCeilingCollision(12)
        if pol.collidesWithLeftWall(0):
            pol.onLeftWallCollision(0)
        if pol.collidesWithRightWall(10):
            pol.onRightWallCollision(10)
    for i in range(len(patches)):
        patches[i].set_xy(handleVertices(polygons[i].getVertices()))
    #patches[1].set_xy(handleVertices(polygons[1].getVertices()))
    return []


anim = animation.FuncAnimation(fig, animate, 
                               init_func=init,
                               frames=1,
                               fargs=(contact, patches[0], patches[1],),
                               interval=10,
                               blit=True,
                               repeat=True)

pyplot.show()
