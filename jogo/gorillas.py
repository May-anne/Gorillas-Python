import curses, random, math, time
import numpy as np

menu = ['Play', 'Ranking', 'Exit']
h = 41
w = 154

#Menu da página inicial
def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    
    moldura(stdscr)

    stdscr.addstr(10, w//2 - len('GORILLAS')//2, 'GORILLAS')
    
    #Muda a cor do texto ao descer com setas up e down
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

def Playing(stdscr): #Função Jogandot

    stdscr.clear()

    moldura(stdscr)

    pad = curses.newpad(160, 200)
    stdscr.refresh()
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)

    for i in range(100):
        for j in range(50):
            pad.addstr('*', curses.color_pair(2))
    for k in range(1):
        h = random.randint(30, 40)
        c = 0
        pad.refresh(0, 0, h, c+1, 40, c+17)
        stdscr.refresh()
        if(k==0):
            hmacaco1=h-1
            cmacaco1=int((c+17)/2)
        for m in range(8):
            h = random.randint(30, 40)
            c = c + 17
            stdscr.refresh()

            pad.refresh(0, 0, h, c+1, 40, c+17)
            stdscr.refresh()
            if(m==7): 
                hmacaco2=h-1
                cmacaco2=int(c+17/2)

        #Primeiro Jogador:
        stdscr.addstr(hmacaco1-2,cmacaco1+1,'o')
        stdscr.addstr(hmacaco1-1,cmacaco1,'/|\\')
        stdscr.addstr(hmacaco1,cmacaco1,'/ \\')
        
        stdscr.refresh()
        
        #Segundo Jogador:
        stdscr.addstr(hmacaco2-2,cmacaco2+1,'o')
        stdscr.addstr(hmacaco2-1,cmacaco2,'/|\\')
        stdscr.addstr(hmacaco2,cmacaco2,'/ \\')

        stdscr.refresh()

    vez=0
    
    while(True):

        if(vez%2==0): #Jogador 1
            curses.echo()
            curses.curs_set(1)

            stdscr.addstr(1, 2, "Nome Jogador 1: ")
            jogador1 = (stdscr.getstr())
            stdscr.refresh()

            stdscr.addstr(2,2,'Angulo:')
            angulo = int(stdscr.getstr())
            stdscr.refresh()

            stdscr.addstr(3,2,'Velocidade: ')
            vel0= int(stdscr.getstr())
            stdscr.refresh()

            curses.noecho()
            curses.curs_set(0)

            #Dados gerais para lançamento:
            angRAD = np.deg2rad(angulo)
            g = 10
            alcanceMax = round(((vel0**2) * np.sin(2*angRAD)) / g, 1)
            alturaMax = round((vel0**2) * (np.sin(angRAD))**2 / (2*g), 1)
            tempoTotal = round((((2*vel0) * np.sin(angRAD)) / g), 1)

            #PAD de lançamento:
            bananapad = curses.newpad(160, 200)
            for i in range(100):
                for j in range(50):
                    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)
                    bananapad.addstr('Z', curses.color_pair(3))

            for t in np.arange(0, tempoTotal+5, 0.1):
                x = int((cmacaco1+3) + abs(vel0) * np.cos(angRAD) * t)
                y = int((hmacaco1-1) - (abs(vel0) * np.sin(angRAD) * t) + ((g*(t**2))/2))

                try:
                    bananapad.refresh(0, 0, y, x, y, x)
                    time.sleep(0.3)
                    stdscr.refresh()
                    stdscr.addstr(5, 10, 'y = {}'.format(str(y))) #Informa o valor final de x e y
                    stdscr.addstr(7, 12, 'x = {}'.format(str(x)))
                    #stdscr.addstr(8, 10, 'c = {}'.format(c))
                    #stdscr.addstr(9, 10, 'h = {}'.format(h))

                    if(c % x == 0):
                        stdscr.addstr(10, 10, "Bateu em algo")
                        stdscr.refresh()

                except curses.error:
                    #vez = vez + 1
                    pass
                
            stdscr.refresh()
            stdscr.getch()
    
        else: #Jogador 2
            pass
            '''
            curses.echo()
            curses.curs_set(1)

            stdscr.addstr(1, 2, "Nome Jogador 2: ")
            jogador1 = (stdscr.getstr())
            stdscr.refresh()

            stdscr.addstr(2,2,'Angulo:')
            angulo = int(stdscr.getstr())
            stdscr.refresh()

            stdscr.addstr(3,2,'Velocidade: ')
            vel0= int(stdscr.getstr())
            stdscr.refresh()

            curses.noecho()
            curses.curs_set(0)'''

        vez+=1

#Borda do jogo
def moldura(stdscr):
    for i in range(h+1):
        stdscr.addstr(i, 0, '#')
        stdscr.addstr(i, w, '#')
    for i in range(w):
        stdscr.addstr(0, i, '#')
        stdscr.addstr(h, i, '#')

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_row_idx = 0
    
    print_menu(stdscr, current_row_idx)

    #Loop do Menu: espera resposta do usuário pelo teclado
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