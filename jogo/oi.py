import curses, random
# import time

menu = ['Play', 'Ranking', 'Exit']
h = 27
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

def Playing(stdscr):
    stdscr.clear()

    '''stdscr.addstr('Informe seu nome: ')
    curses.curs_set(1)
    nome = stdscr.getstr(0,19, 30)
    
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()'''

    moldura(stdscr)

    pad = curses.newpad(160, 200)
    stdscr.refresh()
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)

    for i in range(100):
        for j in range(50):
            pad.addstr('*', curses.color_pair(2))
    for k in range(1):
        h = random.randint(10, 26)
        c = 0
        pad.refresh(0, 0, h, c+1, 26, c+17)
        if(k==0):
            hmacaco1=h-1
            cmacaco1=int((c+17)/2)
        for m in range(8):
            h = random.randint(10, 26)
            c = c + 17
            pad.refresh(0, 0, h, c+1, 26, c+17)
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
        
        if(vez%2==0): #vez do macaco 1
            curses.echo()

            stdscr.addstr(1,1,'Angulo:')
            curses.curs_set(1)

            stdscr.refresh()
            
            ang=stdscr.getstr()

            stdscr.addstr(2,1,'Velocidade: ')
            vel = stdscr.getstr()

            curses.noecho()
            curses.curs_set(0)

            

            stdscr.refresh()
            stdscr.getch()
            # while(True):
            #     key=stdscr.getkey()
            #     if(key=='KEY_ENTER'):
            #         break
            #     resp+=key
                
            
            stdscr.refresh()
            #stdscr.addstr(1,10,resp)
            #stdscr.refresh()

    
        
        else:         #vez do macaco 2
            pass



        vez+=1
    #stdscr.getch()

#Borda do jogo
def moldura(stdscr):
    stdscr.refresh()
    for i in range(27):
        stdscr.addstr(i, 0, '#')
        stdscr.addstr(i, w, '#')
    for i in range(155):
        stdscr.addstr(0, i, '#')
        stdscr.addstr(h, i, '#')
    stdscr.refresh()

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
