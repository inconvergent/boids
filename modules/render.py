#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
  import cairo as cairo
except Exception:
  import cairocffi as cairo

from numpy import pi as PI
TWOPI = PI*2


class Render(object):

  def __init__(self,n, back, front):
    self.n = n
    self.front = front
    self.back = back
    self.pix = 1./float(n)

    self.colors = []
    self.ncolors = 0
    self.num_img = 0
    self.__init_cairo()

  def __init_cairo(self):
    sur = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.n, self.n)
    ctx = cairo.Context(sur)
    ctx.scale(self.n, self.n)
    self.sur = sur
    self.ctx = ctx

    self.clear_canvas()

  def clear_canvas(self):
    ctx = self.ctx

    ctx.set_source_rgba(*self.back)
    ctx.rectangle(0, 0, 1, 1)
    ctx.fill()
    ctx.set_source_rgba(*self.front)

  def write_to_png(self, fn):
    self.sur.write_to_png(fn)
    self.num_img += 1

  def set_front(self, c):
    self.front = c
    self.ctx.set_source_rgba(*c)

  def set_back(self, c):
    self.back = c

  def set_line_width(self, w):
    self.ctx.set_line_width(w)

  def line(self, x1, y1, x2, y2):
    ctx = self.ctx

    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

  def circle(self, x, y, r, fill=False):
    ctx = self.ctx

    ctx.arc(x, y, r, 0, TWOPI)
    if fill:
      ctx.fill()
    else:
      ctx.stroke()

class Animate(Render):

  def __init__(self, n, front, back, step):
    from gi.repository import Gtk
    from gi.repository import GObject

    Render.__init__(self, n, front, back)

    window = Gtk.Window()
    self.window = window
    window.resize(self.n, self.n)

    self.step = step

    window.connect("destroy", self.__destroy)
    darea = Gtk.DrawingArea()
    # darea.connect("expose-event", self.expose)
    self.darea = darea

    window.add(darea)
    window.show_all()

    #self.cr = self.darea.window.cairo_create()
    self.steps = 0
    GObject.idle_add(self.step_wrap)

  def __destroy(self,*args):
    from gi.repository import Gtk
    Gtk.main_quit(*args)

  def start(self):
    from gi.repository import Gtk
    Gtk.main()

  def expose(self, *args):
    #cr = self.cr
    # cr = self.darea.window.cairo_create()
    cr = self.darea.get_property('window').cairo_create()
    cr.set_source_surface(self.sur, 0, 0)
    cr.paint()

  def step_wrap(self):
    res = self.step(self)
    self.steps += 1
    self.expose()
    return res

