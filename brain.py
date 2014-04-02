#!/usr/bin/python2

# Brian's brain cellular automaton. No curses, no masters.

import time, sys, fcntl, termios, struct
from random import randint
from copy import deepcopy

class briansBrain(object):
    o = '\033[94m*\033[0m' # Make living cells blue
    d = '+'
    def __init__(self, maxX, maxY):
        self.maxX = maxX; self.maxY = maxY
        # Draw grid as matrix
        self.g = [ [ ' ' for i in range(self.maxX) ] for j in range(self.maxY) ]

    # Seed random shit
    def seed(self,f):
        for y in range(self.maxY):
            s = ''
            for x in range(self.maxX):
                random = randint(0, f-1) # Determine how random this must be later
                if random == 0:
                    s = self.o
                elif random == 1:
                    s = self.d
                else:
                    s = ' '
                self.g[y][x] = s
        return self.g

    # Given a point, count its on and dying neighbours (* for on, + for dying)
    def counter(self, i, j):
        m = self.g
        # Mod the coordinates to simulate infinite grid
        fx = lambda x: x % self.maxX; fy = lambda x: x % self.maxY
        neighbours = [ m[fy(i-1)][fx(j-1)], m[fy(i-1)][fx(j)], m[fy(i-1)][fx(j+1)], m[fy(i)][fx(j-1)], m[fy(i)][fx(j+1)], m[fy(i+1)][fx(j-1)], m[fy(i+1)][fx(j)], m[fy(i+1)][fx(j+1)] ]
        on = neighbours.count(self.o); dying = neighbours.count(self.d)
        return on, dying

    # Living cells become dying cells; dead cells with two living neighbours resurrect; dying cells die
    def brain(self):
        c = deepcopy(self.g)
        for j in range(len(self.g)):
            for i in range(len(self.g[j])):
                n = self.counter(j,i)
                if self.g[j][i] == self.o: c[j][i] = self.d
                if self.g[j][i] == ' ' and n[0] == 2: c[j][i] = self.o
                if self.g[j][i] == self.d: c[j][i] = ' '
        self.g = c

    # Prepare for pretty printing
    def printIt(self):
        box = '#' * (self.maxX + 2) + '\n'
        for i in self.g:
            box += ( '#' + ''.join(i) + '#\n' )
        box += '#' * (self.maxX + 2)
        return box

    # Count living and dying cells in whole grid
    def live(self):
        on = 0; dying = 0
        for i in self.g:
            on += i.count(self.o)
            dying += i.count(self.d)
        return on, dying

def main():
    # Stolen code to determine terminal height and width
    height, width = struct.unpack('hh',  fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ, '1234'))
    sd = 10 # Randomness seed
    gen = 1
    a = briansBrain(width-2,height-4)
    a.seed(sd)
    while True:
        sys.stdout.write('%s\r' % a.printIt())
        sys.stdout.flush()
        print "\nBRIAN'S BRAIN :: Randomness seed: %d :: Living cells: %d :: Dying cells: %d :: Generation: %d" % (sd, a.live()[0], a.live()[1], gen)
        time.sleep(0.1)
        a.brain()
        gen += 1

if __name__ == '__main__':
    main()
