import curses, random, time
import numpy as np
jogador1 = ''
jogador2 = ''

placar1 = 0
placar2 = 0

valorLevel = 0

menu = ['Play', 'Ranking', 'Exit']
h = 41
w = 154

def print_menu(stdscr, selected_row_idx): #Menu da página inicial
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

def PickLevel(stdscr): #Pergunta ao usuário qual dificuldade deseja
    
    global valorLevel
    stdscr.clear()
    moldura(stdscr)
    selected = 0
    texto = 'ESCOLHA A DIFICULDADE:'
    level = ['Fácil', 'Normal', 'Difícil']

    stdscr.addstr(h//2-5, w//2 - len(texto)//2, texto)
    
    while True:
        for idx, row in enumerate(level): #Muda a cor do texto ao descer com setas up e down
            x = w//2 - len(row)//2
            y = h//2 - len(level)//2 + idx
            if idx == selected:
                stdscr.addstr(y, x, row, curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)

        stdscr.refresh()
        #Avalia resposta do usuário com base nas setas
        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(level) - 1:
            selected += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if(level[selected] == 'Fácil'):
                valorLevel = 30
                Playing(stdscr, valorLevel)
            elif(level[selected] == 'Normal'):
                valorLevel = 25
                Playing(stdscr, valorLevel)
            elif(level[selected] == 'Difícil'):
                valorLevel = 20
                Playing(stdscr, valorLevel)
            
            stdscr.refresh()
            stdscr.getch()
        
        stdscr.refresh()

def KeepPlaying(stdscr): #Após vitória, pergunta aos usuários se eles desejam continuar jogando.
    stdscr.clear()
    moldura(stdscr)
    global valorLevel

    respostas = ['Sim', 'Não']
    texto = 'Você deseja continuar?'
    stdscr.addstr(10, w//2 - len(texto)//2, texto)

    selected = 0

    while True:
        stdscr.refresh()
        for idx, row in enumerate(respostas): #Muda a cor do texto ao descer com setas up e down
            x = w//2 - len(row)//2
            y = h//2 - len(respostas)//2 + idx
            if idx == selected:
                stdscr.addstr(y, x, row, curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)
        stdscr.refresh()

        #Avalia resposta do usuário com base nas setas
        key = stdscr.getch() 
        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(respostas) - 1:
            selected += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if(respostas[selected] == 'Sim'):
                Playing(stdscr, valorLevel) #Gera um novo mapa
            elif(respostas[selected] == 'Não'):
                main(stdscr) #Vai para o menu inicial

            stdscr.getch()
            stdscr.refresh()
    
def Playing(stdscr, level): #Inicia o jogo
    global jogador1
    global jogador2
    global placar1
    global placar2

    stdscr.clear()

    moldura(stdscr)

    pad = curses.newpad(160, 200) #PAD dos prédios
    stdscr.refresh()

    #Pares de cores
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE) #Cor dos prédios
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW) #Cor da banana
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK) #Cor "Você errou."
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK) #Cor "Você acertou!"
    
    hpredios = [] #Armazena alturas geradas aleatoriamente
    for i in range(100):
        for j in range(50):
            pad.addstr('*', curses.color_pair(2))

    for k in range(1):
        h = random.randint(level, 40)
        hpredio1 = h #Armazena altura do 1º prédio
        c = 0
        pad.refresh(0, 0, h, c+1, 40, c+17)
        stdscr.refresh()
        if(k==0): #Posiciona o primeiro macaco
            hmacaco1=h-1
            cmacaco1=int((c+17)/2)
        for m in range(8):
            stdscr.refresh()
            h = random.randint(level, 40)
            hpredios.append(h)

            c = c + 17 #Determina a largura dos prédios como 17
            stdscr.refresh()

            pad.refresh(0, 0, h, c+1, 40, c+17)
            stdscr.refresh()
            if(m==7): #Posiciona o segundo macaco
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
                stdscr.addstr(5, 2, 'Placar: {}'.format(placar1))

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
            tempoTotal = round((((2*vel0) * np.sin(angRAD)) / g), 1)

            #PADs de lançamento:
            bananapad = curses.newpad(160, 200)
            macacopad = curses.newpad(160,200)

            for t in np.arange(0, tempoTotal+5, 0.1): #Lançamento oblíquo para primeiro jogador
                x = int((cmacaco1+3) + abs(vel0) * np.cos(angRAD) * t)
                y = int((hmacaco1-1) - (abs(vel0) * np.sin(angRAD) * t) + ((g*(t**2))/2))
                bananapad.addstr('Z', curses.color_pair(3))
                macacopad.addstr(' ')
                
                try:
                    #Printa e limpa banana segundos depois
                    bananapad.refresh(0, 0, y, x, y, x)
                    time.sleep(0.05)  
                    macacopad.refresh(0, 0, y, x, y, x)
                    stdscr.refresh()

                    #VERIFICAÇÃO DE COLISÃO: JOGADOR 1
                    if((x in range(143, 147) and (y in range(hmacaco2-3, hmacaco2+2)))): 
                        stdscr.addstr(10, 10, "Você acertou!", curses.color_pair(5))
                        placar1 += 1
                        stdscr.refresh()
                        time.sleep(0.7)
                        bananapad.clear()
                        KeepPlaying(stdscr)
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

                except curses.error: #Trata o erro caso a banana ultrapasse a tela do console
                        pass
                        moldura(stdscr)
                        stdscr.addstr(10, 10, "Você errou", curses.color_pair(4))    
            stdscr.refresh()
            time.sleep(0.7)
            #stdscr.getch()
            
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
                stdscr.addstr(5, 125, 'Placar: {}'.format(placar2))

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

            for t in np.arange(0, tempoTotal1+5, 0.1): #Lançamento oblíquo para o segundo jogador
                x1 = int((cmacaco2-1) - abs(vel1) * np.cos(angulo2) * t)
                y1 = int((hmacaco2-1) - (abs(vel1) * np.sin(angulo2) * t) + ((g*(t**2))/2))
                bananapad.addstr('Z', curses.color_pair(3))
                macacopad.addstr(' ')
                
                try:
                    #Printa e limpa banana segundos depois
                    bananapad.refresh(0, 0, y1, x1, y1, x1)
                    time.sleep(0.05)  
                    macacopad.refresh(0, 0, y1, x1, y1, x1)
                    stdscr.refresh()

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
                        placar2 += 1
                        stdscr.refresh()
                        time.sleep(0.7)
                        bananapad.clear()
                        KeepPlaying(stdscr)

                except curses.error: #Trata o erro caso a banana ultrapasse a tela do console
                        pass
                        stdscr.addstr(10, 125, "Você errou", curses.color_pair(4))
                
            stdscr.refresh()
            time.sleep(0.7)
            #stdscr.getch()
        vez+=1

def moldura(stdscr): #Borda do jogo
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_CYAN)
    for i in range(h+1):
        stdscr.addstr(i, 0, '#', curses.color_pair(6))
        stdscr.addstr(i, w, '#', curses.color_pair(6))
    for i in range(w):
        stdscr.addstr(0, i, '#', curses.color_pair(6))
        stdscr.addstr(h, i, '#', curses.color_pair(6))

def Ranking(stdscr): #Exibe o ranking dos jogadores
    stdscr.clear()
    moldura(stdscr)
    texto = 'RANKING DE JOGADORES'

    global jogador1
    global jogador2
    global placar1
    global placar2

    texto1 = '{}: {}'.format(jogador1, placar1)
    texto2 = '{}: {}'.format(jogador2, placar2)

    stdscr.addstr(h//2, w//2 - len(texto)//2, texto)
    stdscr.addstr(h//2 + 1, w//2 - len(texto1)//2, texto1)
    stdscr.addstr(h//2 + 2, w//2 - len(texto2)//2, texto2)

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_row_idx = 0
    print_menu(stdscr, current_row_idx)

    #Loop do Menu: espera resposta do usuário pelo teclado por meio das setas
    while True:
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if(menu[current_row_idx] == 'Play'):
                PickLevel(stdscr)
            elif(menu[current_row_idx] == 'Ranking'):
                Ranking(stdscr)
            elif(menu[current_row_idx] == 'Exit'):
                stdscr.endwin()

            stdscr.refresh()
            stdscr.getch()

        print_menu(stdscr, current_row_idx)
        stdscr.refresh()

curses.wrapper(main)
