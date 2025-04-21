import pygame
from sys import exit

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Batalha Naval")

imagem = pygame.image.load("Naval Battle Assets/intro.png").convert()
imagem = pygame.transform.scale(imagem, (300, 300))  
grid_fundo = pygame.image.load("Naval Battle Assets/Naval Battle Assets/oceangrid_final.png").convert_alpha()
grid_fundo = pygame.transform.scale(grid_fundo, (300, 300))
font = pygame.font.Font("font/Pixeltype.ttf", 20)

explosion_sound = pygame.mixer.Sound("sons_batalha/explosion-47163.mp3")
splash_sound = pygame.mixer.Sound("sons_batalha/splash-by-blaukreuz-6261.mp3")
start_sound = pygame.mixer.Sound("sons_batalha/game-start-6104.mp3") 
win_sound = pygame.mixer.Sound("sons_batalha/goodresult-82807.mp3")
win_sound.set_volume(0.1)
select_barco = pygame.mixer.Sound("sons_batalha/Metal-Click.mp3")
fundo_sound = pygame.mixer.Sound("sons_batalha/som_intro.mp3")
fundo_sound.set_volume(0.1)
fundo_sound.play(loops=-1)

win_sound_played = False

clock = pygame.time.Clock()
tela = "menu"
botao_comecar = pygame.Rect(101, 253, 96, 19)

GRID_PLAYABLE_SIZE = 10
GRID_SIZE = 11  # 11x11 para incluir rótulos
TAMANHO_CELULA = 27  # Cada célula agora tem 27px
OFFSET_X = 30
OFFSET_Y = 30


# Adicione após as outras imagens carregadas
radar_fundo = pygame.image.load("Naval Battle Assets/Naval Battle Assets/radargrid_final.png").convert_alpha()
radar_fundo = pygame.transform.scale(radar_fundo, (300, 300))

# Imagens para os estados das bombas (DESTAQUE PARA AS IMAGENS QUE VOCÊ MENCIONOU)
bomba_agua_img = pygame.image.load("Naval Battle Assets/alvo_agua.png").convert_alpha()
bomba_agua_img = pygame.transform.scale(bomba_agua_img, (TAMANHO_CELULA, TAMANHO_CELULA))

bomba_acerto_img = pygame.image.load("Naval Battle Assets/barco_explodido.png").convert_alpha()
bomba_acerto_img = pygame.transform.scale(bomba_acerto_img, (TAMANHO_CELULA, TAMANHO_CELULA))

bomba_alvo_img = pygame.image.load("Naval Battle Assets/alvo.png").convert_alpha()
bomba_alvo_img = pygame.transform.scale(bomba_alvo_img, (TAMANHO_CELULA, TAMANHO_CELULA))

# Variáveis para controle da fase de batalha
tiros_jogador1 = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # 0=não atirado, 1=água, 2=acerto
tiros_jogador2 = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
jogador_acertou = False  # Controla se o jogador acertou e deve continuar jogando


grade_jogador1 = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
grade_jogador2 = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

vez_do_jogador = 1
posicionando_navios = True
posicao_mouse_grid = None
navio_selecionado = None
navio_atual_idx = 0
posicao_mouse_batalha = None

frota_jogador1 = [
    {"tamanho": 4, "horizontal": True, "posicoes": [], "cor": (0, 100, 200)},
    {"tamanho": 3, "horizontal": True, "posicoes": [], "cor": (0, 120, 180)},
    {"tamanho": 3, "horizontal": True, "posicoes": [], "cor": (0, 140, 160)},
    {"tamanho": 2, "horizontal": True, "posicoes": [], "cor": (0, 160, 140)},
    {"tamanho": 2, "horizontal": True, "posicoes": [], "cor": (0, 180, 120)},
    {"tamanho": 2, "horizontal": True, "posicoes": [], "cor": (0, 200, 100)},
    {"tamanho": 1, "horizontal": True, "posicoes": [], "cor": (0, 220, 80)},
    {"tamanho": 1, "horizontal": True, "posicoes": [], "cor": (0, 240, 60)},
    {"tamanho": 1, "horizontal": True, "posicoes": [], "cor": (0, 255, 40)},
    {"tamanho": 1, "horizontal": True, "posicoes": [], "cor": (0, 255, 20)}
]

frota_jogador2 = [
    {"tamanho": 4, "horizontal": True, "posicoes": [], "cor": (0, 100, 200)},
    {"tamanho": 3, "horizontal": True, "posicoes": [], "cor": (0, 120, 180)},
    {"tamanho": 3, "horizontal": True, "posicoes": [], "cor": (0, 140, 160)},
    {"tamanho": 2, "horizontal": True, "posicoes": [], "cor": (0, 160, 140)},
    {"tamanho": 2, "horizontal": True, "posicoes": [], "cor": (0, 180, 120)},
    {"tamanho": 2, "horizontal": True, "posicoes": [], "cor": (0, 200, 100)},
    {"tamanho": 1, "horizontal": True, "posicoes": [], "cor": (0, 220, 80)},
    {"tamanho": 1, "horizontal": True, "posicoes": [], "cor": (0, 240, 60)},
    {"tamanho": 1, "horizontal": True, "posicoes": [], "cor": (0, 255, 40)},
    {"tamanho": 1, "horizontal": True, "posicoes": [], "cor": (0, 255, 20)}
]

# Posições dos textos
TEXTO_TOPO_Y = 10
TEXTO_BAIXO_Y = 270  # Ajuste este valor conforme necessário




def desenhar_navios(frota):
    
    for navio in frota:
        if navio["posicoes"]:
            for row, col in navio["posicoes"]:
                x = OFFSET_X + (col - 1) * TAMANHO_CELULA  # Ajuste para coordenadas de tela
                y = OFFSET_Y + (row - 1) * TAMANHO_CELULA
                pygame.draw.rect(screen, navio["cor"], (x, y, TAMANHO_CELULA, TAMANHO_CELULA))

    if navio_selecionado and posicao_mouse_grid:
        row, col = posicao_mouse_grid
        grade_atual = grade_jogador1 if vez_do_jogador == 1 else grade_jogador2
        valido = posicao_valida(navio_selecionado, row, col, grade_atual)
        cor = navio_selecionado["cor"] if valido else (255, 0, 0)

        for i in range(navio_selecionado["tamanho"]):
            if navio_selecionado["horizontal"]:
                c = col + i
                r = row
            else:
                r = row + i
                c = col
            
            if 1 <= r <= GRID_PLAYABLE_SIZE and 1 <= c <= GRID_PLAYABLE_SIZE:
                x = OFFSET_X + (c - 1) * TAMANHO_CELULA
                y = OFFSET_Y + (r - 1) * TAMANHO_CELULA
                pygame.draw.rect(screen, cor, (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 2)
        



def posicao_valida(navio, row, col, grade):
    # Verifica se está dentro dos limites jogáveis (1-10)
    if row < 1 or col < 1:
        return False
    
    if navio["horizontal"]:
        # Verifica se o navio cabe na horizontal
        if col + navio["tamanho"] - 1 > GRID_PLAYABLE_SIZE:
            return False
        # Verifica se todas as células estão livres
        for i in range(navio["tamanho"]):
            if grade[row][col + i] != 0:
                return False
    else:
        # Verifica se o navio cabe na vertical
        if row + navio["tamanho"] - 1 > GRID_PLAYABLE_SIZE:
            return False
        # Verifica se todas as células estão livres
        for i in range(navio["tamanho"]):
            if grade[row + i][col] != 0:
                return False
    return True


def atualizar_posicoes_navio(navio, row, col):
    navio["posicoes"] = []
    for i in range(navio["tamanho"]):
        if navio["horizontal"]:
            navio["posicoes"].append((row, col + i))
        else:
            navio["posicoes"].append((row + i, col))
    
    # Atualiza a grade
    for r, c in navio["posicoes"]:
        if 1 <= r <= GRID_PLAYABLE_SIZE and 1 <= c <= GRID_PLAYABLE_SIZE:
            grade_atual = grade_jogador1 if vez_do_jogador == 1 else grade_jogador2
            grade_atual[r][c] = 1

def get_clique_posicionamento(mouse_x, mouse_y):
    col = (mouse_x - OFFSET_X) // TAMANHO_CELULA+1
    row = (mouse_y - OFFSET_Y) // TAMANHO_CELULA+1
    # Verifica se está dentro da área jogável (1-10)
    if 1 <= col <= GRID_PLAYABLE_SIZE and 1 <= row <= GRID_PLAYABLE_SIZE:
        return row, col
    return None

def desenhar_tela_batalha(jogador_atual):
    # Desenha o fundo do radar
    screen.blit(radar_fundo, (0, 0))
    
    # Desenha os tiros já realizados
    tiros = tiros_jogador1 if jogador_atual == 1 else tiros_jogador2
    for row in range(1, GRID_PLAYABLE_SIZE + 1):
        for col in range(1, GRID_PLAYABLE_SIZE + 1):
            x = OFFSET_X + (col - 1) * TAMANHO_CELULA
            y = OFFSET_Y + (row - 1) * TAMANHO_CELULA
            
            if tiros[row][col] == 1:  # Água
                screen.blit(bomba_agua_img, (x, y))
            elif tiros[row][col] == 2:  # Acerto
                screen.blit(bomba_acerto_img, (x, y))
    
    # Desenha o alvo seguindo o mouse
    if posicao_mouse_batalha:
        row, col = posicao_mouse_batalha
        x = OFFSET_X + (col - 1) * TAMANHO_CELULA
        y = OFFSET_Y + (row - 1) * TAMANHO_CELULA
        screen.blit(bomba_alvo_img, (x, y))
    
    # Desenha instruções
    texto_jogador = font.render(f"JOGADOR {jogador_atual} ATIRANDO", True, (255, 0, 0))
    screen.blit(texto_jogador, (100, TEXTO_TOPO_Y + 20))
    
    screen.blit(font.render("Clique: Atirar", True, (200, 200, 200)), 
               (30, TEXTO_BAIXO_Y + 10))


def processar_tiro(row, col, jogador_atual):
    global jogador_acertou, vez_do_jogador, tela, vencedor
    
    # Determina qual grade verificar e qual matriz de tiros atualizar
    grade_alvo = grade_jogador2 if jogador_atual == 1 else grade_jogador1
    tiros = tiros_jogador1 if jogador_atual == 1 else tiros_jogador2
    
    # Verifica se já foi atirado nesta posição
    if tiros[row][col] != 0:
        return
    
    # Verifica se acertou um navio
    if grade_alvo[row][col] == 1:
        tiros[row][col] = 2  # Acerto
        jogador_acertou = True
        explosion_sound.play()
        # Verifica se afundou um navio completo
        frota_alvo = frota_jogador2 if jogador_atual == 1 else frota_jogador1
        for navio in frota_alvo:
            if (row, col) in navio["posicoes"]:
                # Verifica se todas as posições do navio foram atingidas
                if all(tiros[r][c] == 2 for (r, c) in navio["posicoes"]):
                    print(f"Navio de tamanho {navio['tamanho']} afundado!")
        
        # Verifica se todos os navios foram afundados
        if all(all(tiros[r][c] == 2 for (r, c) in navio["posicoes"]) for navio in frota_alvo):
            tela = "fim"
            vencedor = jogador_atual
    else:
        tiros[row][col] = 1  # Água
        jogador_acertou = False
        vez_do_jogador = 2 if jogador_atual == 1 else 1  # Alterna jogador
        splash_sound.play()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if tela == "menu" and botao_comecar.collidepoint(event.pos):
                start_sound.play()
                tela = "jogo"
                navio_selecionado = frota_jogador1[navio_atual_idx]
            elif tela == "jogo" and posicionando_navios:
                select_barco.play()
                if event.button == 1:  # Clique esquerdo
                    posicao = get_clique_posicionamento(event.pos[0], event.pos[1])
                    if posicao and navio_selecionado:
                        row, col = posicao
                        grade_atual = grade_jogador1 if vez_do_jogador == 1 else grade_jogador2

                        if posicao_valida(navio_selecionado, row, col, grade_atual):
                            atualizar_posicoes_navio(navio_selecionado, row, col)

                            navio_atual_idx += 1
                            if navio_atual_idx < len(frota_jogador1 if vez_do_jogador == 1 else frota_jogador2):
                                navio_selecionado = frota_jogador1[navio_atual_idx] if vez_do_jogador == 1 else frota_jogador2[navio_atual_idx]
                            else:
                                if vez_do_jogador == 1:
                                    vez_do_jogador = 2
                                    navio_atual_idx = 0
                                    navio_selecionado = frota_jogador2[navio_atual_idx]
                                else:
                                    posicionando_navios = False
                                    tela = "batalha"
                                    jogador_acertou = False

                elif event.button == 3:  # Clique direito
                    if navio_selecionado:
                        navio_selecionado["horizontal"] = not navio_selecionado["horizontal"]
            
            elif tela == "batalha":
                if event.button == 1 and posicao_mouse_batalha:  # Clique esquerdo para atirar
                    row, col = posicao_mouse_batalha
                    processar_tiro(row, col, vez_do_jogador)

        # Atualizado para rastrear mouse tanto no posicionamento quanto na batalha
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            pos = get_clique_posicionamento(mouse_x, mouse_y)
            
            if tela == "jogo" and posicionando_navios:
                if pos:
                    posicao_mouse_grid = pos
                else:
                    posicao_mouse_grid = None
            elif tela == "batalha":
                if pos:
                    posicao_mouse_batalha = pos
                else:
                    posicao_mouse_batalha = None

    # Renderização
    if tela == "menu":
        screen.blit(imagem, (0, 0))
    elif tela == "jogo":
        screen.blit(grid_fundo, (0, 0))
        desenhar_navios(frota_jogador1 if vez_do_jogador == 1 else frota_jogador2)

        if navio_selecionado and posicao_mouse_grid:
            row, col = posicao_mouse_grid
            grade_atual = grade_jogador1 if vez_do_jogador == 1 else grade_jogador2
    
            valido = posicao_valida(navio_selecionado, row, col, grade_atual)
            cor = navio_selecionado["cor"] if valido else (255, 0, 0)
    
            for i in range(navio_selecionado["tamanho"]):
                if navio_selecionado["horizontal"]:
                    c = col + i
                    r = row
                else:
                    r = row + i
                    c = col
        
                if 1 <= r <= GRID_PLAYABLE_SIZE and 1 <= c <= GRID_PLAYABLE_SIZE:
                    x = OFFSET_X + (c - 1) * TAMANHO_CELULA
                    y = OFFSET_Y + (r - 1) * TAMANHO_CELULA
                    pygame.draw.rect(screen, cor, (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 2)

    # Texto no topo - indicação do jogador (amarelo)
        texto_jogador = font.render(f"JOGADOR {vez_do_jogador}", True, (255, 255, 0))
        screen.blit(texto_jogador, (120, TEXTO_TOPO_Y + 10))

    # Texto na base - instruções (cinza claro)
        cor_instrucoes = (200, 200, 200)
        screen.blit(font.render("Clique: Selecionar", True, cor_instrucoes), 
               (30, TEXTO_BAIXO_Y + 10))
        
    
    elif tela == "batalha":
        # Desenha o fundo e os tiros já realizados
        screen.blit(radar_fundo, (0, 0))
    
        # Desenha os tiros já realizados
        tiros = tiros_jogador1 if vez_do_jogador == 1 else tiros_jogador2
        for row in range(1, GRID_PLAYABLE_SIZE + 1):
            for col in range(1, GRID_PLAYABLE_SIZE + 1):
                x = OFFSET_X + (col - 1) * TAMANHO_CELULA
                y = OFFSET_Y + (row - 1) * TAMANHO_CELULA
            
                if tiros[row][col] == 1:  # Água
                    screen.blit(bomba_agua_img, (x, y))
                elif tiros[row][col] == 2:  # Acerto
                    screen.blit(bomba_acerto_img, (x, y))
    
        # Desenha o alvo seguindo o mouse
        if posicao_mouse_batalha:
            row, col = posicao_mouse_batalha
            x = OFFSET_X + (col - 1) * TAMANHO_CELULA
            y = OFFSET_Y + (row - 1) * TAMANHO_CELULA
            screen.blit(bomba_alvo_img, (x, y))
    
        # Texto no topo - indicação do jogador (amarelo)
        texto_jogador = font.render(f"JOGADOR {vez_do_jogador} ATIRANDO", True, (255, 255, 0))
        screen.blit(texto_jogador, (90, TEXTO_TOPO_Y + 10))
    
        # Texto na base - instruções (cinza claro)
        cor_instrucoes = (200, 200, 200)
        screen.blit(font.render("Clique: Selecionar", True, cor_instrucoes), 
                   (30, TEXTO_BAIXO_Y + 10))
    
    elif tela == "fim":
        if not win_sound_played:
            fundo_sound.stop()  # opcional: para parar o som de fundo
            win_sound.play()
            win_sound_played = True
        
        screen.fill((0, 0, 0))
        texto = font.render(f"JOGADOR {vencedor} VENCEU!", True, (255, 255, 0))
        screen.blit(texto, (100, 150))
    
    pygame.display.update()
    clock.tick(60)