#!/usr/bin/env python3
import lib.vector as vec
import lib.polygon as pol
from matplotlib import pyplot
from matplotlib import animation

#creating polygons
polygons = []

polygons.append(pol.Polygon(1, 2, 1, 5))
polygons[0].position = vec.Vector(2,5,0)
polygons[0].velocity = vec.Vector(20,0,0)
polygons[0].angle = 4

polygons.append(pol.Polygon(1, 2, 1, 4))
polygons[1].position = vec.Vector(8,5,0)

polygons.append(pol.Polygon(1, 2, 1, 6))
polygons[2].position = vec.Vector(4,2,0)
polygons[2].velocity = vec.Vector(20,20,0)

polygons.append(pol.Polygon(1, 2, 1, 4))
polygons[3].position = vec.Vector(2,2,0)
polygons[3].velocity = vec.Vector(20,20,0)

polygons.append(pol.Polygon(1, 2, 1, 7))
polygons[4].position = vec.Vector(1,2,0)
polygons[4].velocity = vec.Vector(20,20,0)

#figure settings
fig = pyplot.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)
ax = pyplot.axes(xlim=(0, 10), ylim=(0, 10))

#handles Vector vertices to suitable form for matplotlib
def handleVertices(vertices):
    handled = []
    for i in range(0, len(vertices)):
        handled.append([vertices[i].x, vertices[i].y])
    return handled

#create patches acording polygons
patches = []
for i in range(len(polygons)):
    patches.append(pyplot.Polygon(handleVertices(polygons[i].getVertices())))

contact = pyplot.Circle((-1, -1), 0.1, color='r')

def init():
    for i in range(len(patches)):
        ax.add_patch(patches[i])
        
    ax.add_patch(contact)
    return []

def animate(i, contact, patches):
    collisions = []

    #handle updating polygons and handling collisions
    for polygon in polygons:
        polygon.update(20 / 1000, 9.81)

        if polygon.collidesWithBorder(0, 10, 0, 10):
            polygon.onBorderCollision(0, 10, 0, 10)

        for other in polygons:
            if other is not polygon:
                if polygon.collides(other) and other.collides(polygon):
                    #we dont want to process the same collision again
                    alreadyCollided = False 
                    for i in range(len(collisions)):
                        if collisions[i][0] is other and collisions[i][1] is polygon:
                            alreadyCollided = True
                    if alreadyCollided:
                        continue

                    collisions.append((polygon, other))
                    collision = polygon.onCollision(other)
                    contact.center = (collision.x, collision.y)

    #update all the patches
    for i in range(len(patches)):
        patches[i].set_xy(handleVertices(polygons[i].getVertices()))
    return []

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=30, fargs=(contact, patches,), interval=20)
pyplot.show()
