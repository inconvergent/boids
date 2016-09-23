# Boids

![ani](/img/ani.gif?raw=true "ani")
![ani](/img/ani2.gif?raw=true "ani")

More or less an implementation of Boids flocking algorithm.

Note that this implementation stores a velocity vector. Some of the other
implementations I have seen do not do this

## Running it

The easiest is to run:

    python3 main.py

The other main file is experimental and relies on
https://github.com/inconvergent/fast-sand-paint

## Requires

 * cairo or cairocffi
 * gi
 * numpy
 * scipy
