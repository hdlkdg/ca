#!/usr/bin/python2

import time, fcntl, termios, struct, re
from random import randint
from copy import deepcopy
from sys import stdout, argv

script, pattern = argv

class gameOfLife(object):
    def __init__(self, maxX, maxY):
        self.maxX = maxX; self.maxY = maxY
        # Draw grid as matrix
        self.g = [ [ ' ' for i in range(self.maxX) ] for j in range(self.maxY) ]

    # Draw grid as matrix and seed random shit
    # ptn = [ (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2) ]
    def seed(self,lif):
        ptn = []
        lst = [ line.strip() for line in open(lif, 'r') ]
        del lst[0]
        lst  = [ re.findall(r'[-+]?\d+', i) for i in lst ]
        ptn = [ (int(i), int(j)) for i, j in lst ]
        cX = self.maxX / 2; cY = self.maxY / 2
        for i,j in ptn:
            self.g[cY+j][cX+i] = '*'
        return self.g

    def clear(self):
        self.g = [ [ ' ' for i in range(self.maxX) ] for j in range(self.maxY) ]

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
    height, width = struct.unpack('hh',  fcntl.ioctl(stdout, termios.TIOCGWINSZ, '1234'))
    gen = 1
    a = gameOfLife(width-2,height-4)
    a.seed(pattern) # Reads a pattern indicated as an argument
    while True:
        stdout.write('%s\r' % a.printIt())
        stdout.flush()
        print "\nCONWAY'S GAME OF LIFE :: Living cells: %d :: Generation: %d" % (a.live(), gen)
        time.sleep(0.1)
        a.conway()
        gen += 1

if __name__ == '__main__':
    main()
