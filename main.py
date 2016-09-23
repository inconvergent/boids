#!/usr/bin/python3
# -*- coding: utf-8 -*-

from numpy import pi as PI
TWOPI = 2.0*PI

BACK = [1]*4
FRONT = [0, 0, 0, 0.5]
SIZE = 512
ONE = 1.0/SIZE
INIT_NUM = 1000
STP = ONE

SEPARATION = 0.5
COHESION = 0.7
ALIGNMENT = 1.0


def main():
  from modules.boids import B
  from modules.render import Animate

  b = B(INIT_NUM, SIZE, STP)

  def wrap(render):
    render.clear_canvas()
    b.step(
        separation=SEPARATION,
        cohesion=COHESION,
        alignment=ALIGNMENT
        )
    for xy in b.xy:
      render.circle(xy[0], xy[1], 2.*ONE, fill=True)

    return True

  render = Animate(SIZE, BACK, FRONT, wrap)

  render.set_line_width(ONE)
  render.start()


if __name__ == '__main__':

  main()

