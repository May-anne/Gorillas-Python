import curses, random
# import time

menu = ['Play', 'Ranking', 'Exit']

def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    stdscr.addstr(10, w//2 - len('GORILLAS')//2, 'GORILLAS')
    
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)

    stdscr.refresh()

def Playing(stdscr):
    pad = curses.newpad(160, 200)
    stdscr.refresh()
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)

    for i in range(100):
        for j in range(50):
            pad.addstr('*', curses.color_pair(2))
    for k in range(1):
        h = random.randint(10, 26)
        c = 0
        pad.refresh(0, 0, h, c, 26, c+17)
        for m in range(8):
            h = random.randint(10, 26)
            c = c + 17
            pad.refresh(0, 0, h, c, 26, c+17)
        
        stdscr.refresh()
    stdscr.getch()

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_row_idx = 0
    

    print_menu(stdscr, current_row_idx)

    while True:
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if(menu[current_row_idx] == 'Play'):
                Playing(stdscr)
            elif(menu[current_row_idx] == 'Ranking'):
                stdscr.addstr('hey')
            elif(menu[current_row_idx] == 'Exit'):
                stdscr.endwin()

            stdscr.refresh()
            stdscr.getch()

        print_menu(stdscr, current_row_idx)
        stdscr.refresh()

curses.wrapper(main)