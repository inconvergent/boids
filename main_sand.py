#!/usr/bin/python3
# -*- coding: utf-8 -*-

from numpy import pi as PI
from numpy import zeros
from numpy import ones
TWOPI = 2.0*PI

BACK = [1]*4
FRONT = [0, 0, 0, 0.001]
SIZE = 512
ONE = 1.0/SIZE
INIT_NUM = 1000
STP = ONE

SEPARATION = 0.5
COHESION = 0.7
ALIGNMENT = 1.0

GRAINS = 20

DRAW_ITT = 2


def main():
  from modules.boids import B
  from sand import Sand

  from fn import Fn

  fn = Fn(prefix='./res/', postfix='.png')

  sand = Sand(SIZE)
  sand.set_bg(BACK)
  sand.set_rgba(FRONT)

  b = B(INIT_NUM, SIZE, STP)

  for itt in range(1000000):

    b.step(
        separation=SEPARATION,
        cohesion=COHESION,
        alignment=ALIGNMENT
        )

    xy = b.xy
    for i, nearby in enumerate(b.get_nearby()):
      if not nearby:
        continue
      start = zeros((len(nearby), 2))
      start[:,0] = xy[i,0]
      start[:,1] = xy[i,1]
      stop = xy[nearby,:]
      g = GRAINS*ones(len(nearby), 'int')
      sand.paint_strokes(start, stop, g)

    if not itt%DRAW_ITT:
      name = fn.name()
      print(itt, name)
      sand.write_to_png(name)


if __name__ == '__main__':

  main()

