#!/usr/bin/env python3
import curses
from curses import wrapper
from subprocess import call, DEVNULL
import itertools

w, h, cc = 0, 0, 0
sq = 0


fvars = {}
where = {}
cl = []


def ask(stdscr):
    global w, h, err, sq
    err.write("ask\n")

    ch = ''
    x = 0
    y = 0
    field = [[0 for i in range(w)] for j in range(h)]
    while ch != '\n':
        stdscr.clear()
        for i in range(h):
            for j in range(w):
                if y == i and x == j:
                    stdscr.addch('o' if field[i][j] else '.', curses.color_pair(10))
                else:
                    stdscr.addch('o' if field[i][j] else '.')
            stdscr.addch('\n')
        ch = stdscr.getkey()
        if ch == ' ':
            field[y][x] ^= 1
        elif ch == 'd':
            x = (x + 1) % w
        elif ch == 'a':
            x = (x - 1 + w) % w
        elif ch == 'w':
            y = (y - 1 + h) % h
        elif ch == 's':
            y = (y + 1) % h
    fieldc = []
    mn = (w, h)
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == 1 and i < mn[0]:
                mn = (i, mn[1])
            if field[i][j] == 1 and j < mn[1]:
                mn = (mn[0], j)

    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == 1:
                sq += 1
                fieldc.append((i-mn[0], j-mn[1]))

    stdscr.refresh()
    return fieldc

intro = """
Imagine you have a rectangle WxH and your friend decided to split in C parts
Then your friend gives you splitted parts and asks you to combine them into a rectangle, like a puzzle
This program solves that problem for you
Enter W, H, C: """

intro2 = """
Now you need to enter the pieces, using the board.
Type WASD to move, SPACE to select/unselect, ENTER to confirm

Press Enter to begin 
"""

def premain():
    global w, h, cc
    w, h, cc = map(int, input(intro).split())
    input(intro2)
    res = wrapper(main)
    if res == 0:
        print("No solutions")

def main(stdscr):
    global w, h, cc, var, where
    global err
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    figs = []
    for i in range(cc):
        figs.append(ask(stdscr))
    err.write(str(len(figs))) 
    if sq != w*h:
        stdscr.clear()
        if sq < w*h:
            stdscr.addstr("error: field is undercovered")
        else:
            stdscr.addstr("error: field is overcovered")
        stdscr.getch()
        return
    fig_a = [addfig(i) for i in figs]
    for i in fig_a:
        exoneof(i[0])
    for i in fvars.values():
        exoneof(i)
    with open('puzzle.cnf','w') as o:
        o.write('p cnf {} {}\n'.format(var, len(cl)))
        for i in cl:
            for j in i:
                o.write('{} '.format(j))
            o.write('0\n')
    call(['minisat', 'puzzle.cnf', 'puzzle.ans'], stdout=DEVNULL)
    stdscr.clear()
    with open('puzzle.ans', 'r') as r:
        res = r.readline()
        if res == "UNSAT\n":
            stdscr.addstr('No solution')
        else:
            ans = list(map(int, r.readline().split()))[:-1]
            fia = [[0 for j in range(w)] for i in range(h)]
            num = 0
            for var in ans:
                if var > 0:
                    num += 1
                    for mark in where[var]:
                        err.write(str(mark)+'\n')
                        err.write(str(len(fia))+'\n')
                        err.write(str(len(fia[mark[0]]))+'\n')
                        fia[mark[0]][mark[1]] = num
            for i in range(h):
                for j in range(w):
                    stdscr.addch('o', curses.color_pair(fia[i][j] + 1))
                stdscr.addch('\n')
        stdscr.getch()

var = 0


def addvar():
    global var
    var += 1
    return var


def exoneof(lst):
    global cl
    cl.append([i for i in lst])

    for i in itertools.combinations(lst, 2):
        cl.append([-j for j in i])


err = open("err.txt","a")


def addfig(fieldc):
    global w, h, fvars, where
    global err
    err.write("add!\n")
    dct = {}
    lst = []
    for i in range(-h, h):
        for j in range(-w, w):
            bad = 0
            for c in fieldc:
                if c[0] + i >= h or c[1] + j >= w or c[0] + i < 0 or c[1] + j < 0:
                    bad = 1
            if not bad:
                err.write("not bad!\n")
                vr = addvar()
                lst.append(vr)
                dct[(i, j)] = vr
                where[vr] = [(c[0] + i, c[1] + j) for c in fieldc]
                err.write('where[%i]' % vr + str(where[vr])+'\n')

                for c in fieldc:
                    fvars.setdefault((c[0] + i, c[1] + j), []).append(vr)
    return (lst, dct)


if __name__ == "__main__":
    premain()


# curses.nocbreak()
# stdscr.keypad(False)
# curses.echo()
#
# curses.endwin()
