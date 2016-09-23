# -*- coding: utf-8 -*-

from numpy import cos
from numpy import pi as PI
TWOPI = 2.0*PI
from numpy import zeros
from numpy import sin
from numpy import mean
from numpy.linalg import norm
from numpy import column_stack
from numpy.random import random
from scipy.spatial import cKDTree as kdtree

class B(object):
  def __init__(self, init_num, size, stp):
    self.num = init_num
    self.size = size
    self.stp = stp
    self.one = 1.0/size

    self.rad = 0.04

    edge = 0.2
    self.xy = edge + random((init_num, 2))*(1.0-2*edge)

    self.v = zeros((init_num, 2), 'float')
    self.dx = zeros((init_num, 2), 'float')
    self.random_velocity(self.stp)
    self.tree = kdtree(self.xy)

    self.slowdown = 0.99999

  def random_velocity(self, s):
    theta = random(self.num)*TWOPI
    a = column_stack((cos(theta), sin(theta)))
    self.v += a*s

  def separation(self, i, near, s):
    dx = mean(self.xy[i, :] - self.xy[near, :], axis=0)
    dx = dx/norm(dx)
    self.dx[i, :] += dx*s

  def alignment(self, i, near, s):
    vv = mean(self.v[near, :], axis=0)
    dv = vv - self.v[i, :]
    dv = dv/norm(dv)
    self.dx[i, :] += vv*s

  def cohesion(self, i, near, s):
    mx = mean(self.xy[near, :], axis=0)
    dx = mx - self.xy[i, :]
    dx = dx/norm(dx)
    self.dx[i, :] += dx*s

  def get_nearby(self):
    return self.tree.query_ball_point(self.xy, self.rad)

  def step(
      self,
      separation,
      cohesion,
      alignment
      ):
    self.xy += self.v

    nearby = self.get_nearby()

    separation = self.stp*separation
    alignment = self.stp*alignment
    cohesion = self.stp*cohesion

    self.dx[:, :] = 0
    for i, near in enumerate(nearby):
      near = list(set(near).difference(set([i])))

      if not near:
        continue

      self.separation(i, near, separation)
      self.alignment(i, near, alignment)
      self.cohesion(i, near, cohesion)

    self.v += self.dx/3.0
    self.v *= self.slowdown

    self.tree = kdtree(self.xy)


