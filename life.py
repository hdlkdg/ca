#!/usr/bin/python2

import time, sys, fcntl, termios, struct
from random import randint
from copy import deepcopy

class gameOfLife(object):
    def __init__(self, maxX, maxY):
        self.maxX = maxX; self.maxY = maxY
        # Draw grid as matrix
        self.g = [ [ ' ' for i in range(self.maxX) ] for j in range(self.maxY) ]

    # Draw grid as matrix and seed random shit
    def seed(self,f):
        for y in range(self.maxY):
            s = ''
            for x in range(self.maxX):
                random = randint(0, f-1) # Determine how random this must be later
                if random == 0:
                    s = '*'
                else:
                    s = ' '
                self.g[y][x] = s
        return self.g

    # Given a point, get a list of its neighbours and count the cells that are alive
    def counter(self, i, j):
        m = self.g
        fx = lambda x: x % self.maxX; fy = lambda x: x% self.maxY
        neighbours = [ m[fy(i-1)][fx(j-1)], m[fy(i-1)][fx(j)], m[fy(i-1)][fx(j+1)], m[fy(i)][fx(j-1)], m[fy(i)][fx(j+1)], m[fy(i+1)][fx(j-1)], m[fy(i+1)][fx(j)], m[fy(i+1)][fx(j+1)] ]
        c = neighbours.count('*')
        return c

    def conway(self):
        c = deepcopy(self.g)
        for j in range(len(self.g)):
            for i in range(len(self.g[j])):
                if self.g[j][i] == '*':
                    if self.counter(j,i) < 2: c[j][i] = ' '
                    if 2 <= self.counter(j,i) <= 3: c[j][i] = '*'
                    if self.counter(j,i) > 3: c[j][i] = ' '
                else:
                    if self.counter(j,i) == 3: c[j][i] = '*'
        self.g = c

    def printIt(self):
        box = '#' * (self.maxX + 2) + '\n'
        for i in self.g:
            box += ( '#' + ''.join(i) + '#\n' )
        box += '#' * (self.maxX + 2)
        return box

    def live(self):
        c = 0
        for i in self.g:
            c += i.count('*')
        return c

def main():
    # Stolen code to determine terminal height and width
    height, width = struct.unpack('hh',  fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ, '1234'))
    sd = 10 # Randomness seed
    gen = 1
    a = gameOfLife(width-2,height-4)
    a.seed(sd)
    while True:
        sys.stdout.write('%s\r' % a.printIt())
        sys.stdout.flush()
        print "\nCONWAY'S GAME OF LIFE :: Randomness seed: %d :: Living cells: %d :: Generation: %d" % (sd, a.live(), gen)
        time.sleep(0.1)
        a.conway()
        gen += 1

if __name__ == '__main__':
    main()
