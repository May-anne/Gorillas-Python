import curses, random, time
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

def KeepPlaying(stdscr):
    stdscr.clear()
    moldura(stdscr)

    respostas =['sim', 'não']
    texto = 'Você deseja continuar?'
    stdscr.addstr(10, w//2 - len(texto)//2, texto)

    selected = 0

    while True:
        stdscr.refresh()
        
        for idx, row in enumerate(respostas):
            x = w//2 - len(row)//2
            y = h//2 - len(respostas)//2 + idx
            if idx == selected:
                stdscr.addstr(y, x, row, curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(respostas) - 1:
            selected += 1

        elif key == curses.KEY_ENTER or key in [10, 13]:
            if(respostas[selected] == 'sim'):
                Playing(stdscr)
            elif(respostas[selected] == 'não'):
                main(stdscr)

        stdscr.refresh()
        stdscr.getch()
    
def Playing(stdscr): #Função Jogando
    jogador1 = ''
    jogador2 = ''

    stdscr.clear()

    moldura(stdscr)

    pad = curses.newpad(160, 200)
    stdscr.refresh()

    #Pares de cores
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE) #Cor dos prédios
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW) #Cor da banana
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK) #Cor "Você errou."
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK) #Cor "Você acertou!"
    
    hpredios = []

    for i in range(100):
        for j in range(50):
            pad.addstr('*', curses.color_pair(2))
    for k in range(1):
        h = random.randint(30, 40)
        hpredio1 = h
        c = 0
        pad.refresh(0, 0, h, c+1, 40, c+17)
        stdscr.refresh()
        if(k==0):
            hmacaco1=h-1
            cmacaco1=int((c+17)/2)
        for m in range(8):
            stdscr.refresh()
            h = random.randint(30, 40)
            hpredios.append(h)

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
    
    while True: #Gera partidas consecutivas até que alguém acerte

        if(vez%2==0): #Jogador 1
            stdscr.refresh()
            curses.echo()
            curses.curs_set(1)

            stdscr.addstr(3, 125, '            ')
            stdscr.addstr(4, 125, '                  ')
            stdscr.addstr(10, 125, '                ')

            if(jogador1 == ''):
                stdscr.addstr(2, 2, "Nome Jogador 1: ")
                jogador1 = stdscr.getstr()
                moldura(stdscr)
                stdscr.refresh()
            else:
                stdscr.addstr(2, 2, 'Nome Jogador 1: {}'.format(jogador1))

            stdscr.addstr(3, 2,'Angulo: ')
            angulo = int(stdscr.getstr())
            moldura(stdscr)
            stdscr.refresh()

            stdscr.addstr(4, 2,'Velocidade: ')
            vel0= int(stdscr.getstr())
            moldura(stdscr)
            stdscr.refresh()

            curses.noecho()
            curses.curs_set(0)

            #Dados gerais para lançamento:
            angRAD = np.deg2rad(angulo)
            g = 10
            alcanceMax = round(((vel0**2) * np.sin(2*angRAD)) / g, 1)
            alturaMax = round((vel0*2) * (np.sin(angRAD))*2 / (2*g), 1)
            tempoTotal = round((((2*vel0) * np.sin(angRAD)) / g), 1)

            #PADs de lançamento:
            bananapad = curses.newpad(160, 200)
            macacopad = curses.newpad(160,200)

            for t in np.arange(0, tempoTotal+5, 0.1):

                x = int((cmacaco1+3) + abs(vel0) * np.cos(angRAD) * t)
                y = int((hmacaco1-1) - (abs(vel0) * np.sin(angRAD) * t) + ((g*(t**2))/2))
        
                bananapad.addstr('Z', curses.color_pair(3))
                macacopad.addstr(' ')
                
                try:
                    
                    bananapad.refresh(0, 0, y, x, y, x)
                    time.sleep(0.05)  
                    macacopad.refresh(0, 0, y, x, y, x)
                    
                    stdscr.refresh()

                    #stdscr.addstr(5, 10, 'y = {}'.format(str(y))) #Informa os valores de x e y conforme o sleep
                    #stdscr.addstr(7, 10, 'x = {}'.format(str(x)))
                    #stdscr.addstr(8, 10, str(hpredios))

                    #VERIFICAÇÃO DE COLISÃO: JOGADOR 1
                    if((x in range(143, 147) and (y in range(hmacaco2-3, hmacaco2+1)))): 
                        stdscr.addstr(10, 10, "Você acertou!", curses.color_pair(5))
                        stdscr.refresh()
                        bananapad.clear
                        KeepPlaying(stdscr)
                        break
                    elif(y in range(hpredio1, 40) and x in range(0, 17)):
                        stdscr.addstr(10, 10, "Você errou", curses.color_pair(4))
                        bananapad.clear()
                        break
                    elif(y in range(hpredios[0], 40) and x in range(17, 35)):
                        stdscr.addstr(10, 10, "Você errou", curses.color_pair(4))
                        bananapad.clear()
                        break
                    elif(y in range(hpredios[1], 40) and x in range(35, 52)):
                        stdscr.addstr(10, 10, "Você errou", curses.color_pair(4))
                        bananapad.clear()
                        break
                    elif(y in range(hpredios[2], 40) and x in range(52, 69)):
                        stdscr.addstr(10, 10, "Você errou", curses.color_pair(4))
                        bananapad.clear()
                        break
                    elif(y in range(hpredios[3], 40) and x in range(69, 86)):
                        stdscr.addstr(10, 10, "Você errou", curses.color_pair(4))
                        bananapad.clear()
                        break
                    elif(y in range(hpredios[4], 40) and x in range(86, 103)):
                        stdscr.addstr(10, 10, "Você errou", curses.color_pair(4))
                        bananapad.clear()
                        break
                    elif(y in range(hpredios[5], 40) and x in range(103, 120)):
                        stdscr.addstr(10, 10, "Você errou", curses.color_pair(4))
                        bananapad.clear()
                        break
                    elif(y in range(hpredios[6], 40) and x in range(120, 137)):
                        stdscr.addstr(10, 10, "Você errou", curses.color_pair(4))
                        bananapad.clear()
                        break
                    elif(y in range(hpredios[7], 40) and x in range(137, 154)):
                        stdscr.addstr(10, 10, "Você errou", curses.color_pair(4))
                        bananapad.clear()
                        break
                    elif(x > 154):
                        stdscr.addstr(10, 10, "Você errou", curses.color_pair(4))
                        break

                except curses.error:
                        pass
                        moldura(stdscr)
                        stdscr.addstr(10, 10, "Você errou", curses.color_pair(4))
                
                
            stdscr.refresh()
            stdscr.getch()
            
        else: #Jogador 2
            pass
            stdscr.addstr(3, 2, '            ')
            stdscr.addstr(4, 2, '                  ')
            stdscr.addstr(10, 10, '                ')

            curses.echo()
            curses.curs_set(1)

            if(jogador2 == ''):
                stdscr.addstr(2, 125, "Nome Jogador 2: ")
                jogador2 = stdscr.getstr()
                moldura(stdscr)
                stdscr.refresh()
            else:
                stdscr.refresh()
                stdscr.addstr(2, 125, 'Nome Jogador 2: {}'.format(jogador2))

            stdscr.addstr(3, 125,'Angulo: ')
            angulo2 = np.deg2rad(int(stdscr.getstr()))
            moldura(stdscr)
            stdscr.refresh()

            stdscr.addstr(4,125,'Velocidade: ')
            vel1= int(stdscr.getstr())
            moldura(stdscr)
            stdscr.refresh()

            curses.noecho()
            curses.curs_set(0)

            tempoTotal1 = round((((2*vel1) * np.sin(angulo2)) / g), 1)

            for t in np.arange(0, tempoTotal1+5, 0.1):

                x1 = int((cmacaco2-1) - abs(vel1) * np.cos(angulo2) * t)
                y1 = int((hmacaco2-1) - (abs(vel1) * np.sin(angulo2) * t) + ((g*(t**2))/2))
        
                bananapad.addstr('Z', curses.color_pair(3))
                macacopad.addstr(' ')
                
                try:
                    
                    bananapad.refresh(0, 0, y1, x1, y1, x1)
                    time.sleep(0.05)  
                    macacopad.refresh(0, 0, y1, x1, y1, x1)
                    
                    stdscr.refresh()

                    stdscr.addstr(5, 10, 'y = {}'.format(str(y1))) #Informa os valores de x e y conforme o sleep
                    stdscr.addstr(7, 10, 'x = {}'.format(str(x1)))

                    #VERIFICAÇÃO DE COLISÃO: JOGADOR 2
                    if(y1 in range(hpredios[7], 40) and x1 in range(137, 154)):
                        stdscr.addstr(10, 125, "Você errou", curses.color_pair(4))
                        bananapad.clear()
                        break
                    elif(y1 in range(hpredios[6], 40) and x1 in range(120, 137)):
                        stdscr.addstr(10, 125, "Você errou", curses.color_pair(4))
                        bananapad.clear()
                        break
                    elif(y1 in range(hpredios[5], 40) and x1 in range(103, 120)):
                        stdscr.addstr(10, 125, "Você errou", curses.color_pair(4))
                        bananapad.clear()
                        break
                    elif(y1 in range(hpredios[4], 40) and x1 in range(86, 103)):
                        stdscr.addstr(10, 125, "Você errou", curses.color_pair(4))
                        bananapad.clear()
                        break
                    elif(y1 in range(hpredios[3], 40) and x1 in range(69, 86)):
                        stdscr.addstr(10, 125, "Você errou", curses.color_pair(4))
                        bananapad.clear()
                        break
                    elif(y1 in range(hpredios[2], 40) and x1 in range(52, 69)):
                        stdscr.addstr(10, 125, "Você errou", curses.color_pair(4))
                        bananapad.clear()
                        break
                    elif(y1 in range(hpredios[1], 40) and x1 in range(35, 52)):
                        stdscr.addstr(10, 125, "Você errou", curses.color_pair(4))
                        bananapad.clear()
                        break
                    elif(y1 in range(hpredios[0], 40) and x1 in range(17, 35)):
                        stdscr.addstr(10, 125, "Você errou", curses.color_pair(4))
                        bananapad.clear()
                        break
                    elif(y1 in range(hpredio1, 40) and x1 in range(0, 17)):
                        stdscr.addstr(10, 125, "Você errou", curses.color_pair(4))
                        bananapad.clear()
                        break
                    elif(y1 in range(hmacaco1-3, hmacaco1+1) and x1 in range(6, 11)):
                        stdscr.addstr(10, 125, "Você acertou!", curses.color_pair(5))
                        bananapad.clear()
                        KeepPlaying(stdscr)
                        break

                except curses.error:
                        pass
                        stdscr.addstr(10, 125, "Você errou", curses.color_pair(4))
                
            stdscr.refresh()
            stdscr.getch()

        vez+=1

#Borda do jogo
def moldura(stdscr):
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_CYAN)
    for i in range(h+1):
        stdscr.addstr(i, 0, '#', curses.color_pair(6))
        stdscr.addstr(i, w, '#', curses.color_pair(6))
    for i in range(w):
        stdscr.addstr(0, i, '#', curses.color_pair(6))
        stdscr.addstr(h, i, '#', curses.color_pair(6))

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
