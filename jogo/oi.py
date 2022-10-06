import curses
from curses import textpad
def main(stdscr):
    stdscr.clear()
    SW=100
    SH=20
    win = curses.newwin(SH+1,SW+1,0,0)
    win.border()

    win.keypad(True)
    win.move(4,4)
    win.addstr('''
                   O
                  /|\\
                  / \ 
                  
                  ''') 

    curses.textpad.rectangle(win,4,4,10,10)

    win.getch()



curses.wrapper(main)    