import pygame
from sys import exit



pygame.init()
screen= pygame.display.set_mode((300,300))
pygame.display.set_caption("Batalha Naval")

imagem = pygame.image.load("Naval Battle Assets/intro.png").convert()
imagem = pygame.transform.scale(imagem, (300, 300))  

grid_fundo = pygame.image.load("Naval Battle Assets/Naval Battle Assets/oceangrid_final.png").convert_alpha()
grid_fundo = pygame.transform.scale(grid_fundo, (300, 300))

font = pygame.font.Font("font/Pixeltype.ttf",20)


clock = pygame.time.Clock()
tela = "menu"
botao_comecar = pygame.Rect(101, 253, 96, 19)


GRID_SIZE = 11  # 11x11 para incluir rótulos
TAMANHO_CELULA = 27 # Cada célula agora tem 27px
OFFSET_X = 30
OFFSET_Y = 30

grade_jogador1 = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
grade_jogador2 = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

vez_do_jogador = 1
posicionando_navios = True

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

navio_selecionado = None
navio_atual_idx = 0
modo_posicionamento = "selecionar"

# Posições dos textos
TEXTO_TOPO_Y = 10
TEXTO_BAIXO_Y = 270  # Ajuste este valor conforme necessário

def desenhar_navios(frota):
    for navio in frota:
        if not navio["posicoes"]:
            continue
            
        # Desenha o navio completo
        for row, col in navio["posicoes"]:
            x = OFFSET_X + col * TAMANHO_CELULA
            y = OFFSET_Y + row * TAMANHO_CELULA
            pygame.draw.rect(screen, navio["cor"], (x, y, TAMANHO_CELULA, TAMANHO_CELULA))
            
        # Destaca a primeira posição do navio
        if navio == navio_selecionado:
            first_row, first_col = navio["posicoes"][0]
            x = OFFSET_X + first_col * TAMANHO_CELULA
            y = OFFSET_Y + first_row * TAMANHO_CELULA
            pygame.draw.rect(screen, (255, 255, 255), (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 2)

def posicao_valida(navio, row, col, grade):
    if navio["horizontal"]:
        if col + navio["tamanho"] > GRID_SIZE:
            return False
        for i in range(navio["tamanho"]):
            if grade[row][col + i] != 0:
                return False
    else:
        if row + navio["tamanho"] > GRID_SIZE:
            return False
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


def get_clique_posicionamento(mouse_x, mouse_y):
    col = (mouse_x - OFFSET_X) // TAMANHO_CELULA
    row = (mouse_y - OFFSET_Y) // TAMANHO_CELULA
    if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
        return row, col
    return None




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if tela == "menu" and botao_comecar.collidepoint(event.pos):
                tela = "jogo"
                # Começa com o primeiro navio do jogador 1
                navio_selecionado = frota_jogador1[navio_atual_idx]

            elif tela == "jogo" and posicionando_navios:
                mouse_x, mouse_y = event.pos
                posicao = get_clique_posicionamento(mouse_x, mouse_y)
                
                if posicao:
                    row, col = posicao
                    grade_atual = grade_jogador1 if vez_do_jogador == 1 else grade_jogador2
                    frota_atual = frota_jogador1 if vez_do_jogador == 1 else frota_jogador2
                    
                    if posicao_valida(navio_selecionado, row, col, grade_atual):
                        atualizar_posicoes_navio(navio_selecionado, row, col)
                        
                        # Marca as posições na grade
                        for r, c in navio_selecionado["posicoes"]:
                            grade_atual[r][c] = 1
                            
                        # Passa para o próximo navio
                        navio_atual_idx += 1
                        if navio_atual_idx < len(frota_atual):
                            navio_selecionado = frota_atual[navio_atual_idx]
                        else:
                            # Todos os navios foram posicionados
                            if vez_do_jogador == 1:
                                vez_do_jogador = 2
                                navio_atual_idx = 0
                                navio_selecionado = frota_jogador2[navio_atual_idx]
                            else:
                                posicionando_navios = False
                                tela = "batalha"

        if event.type == pygame.KEYDOWN and tela == "jogo" and posicionando_navios:
            if event.key == pygame.K_RETURN:
                if vez_do_jogador == 1:
            # Verifica se todos os navios do jogador 1 foram posicionados
                    if all(navio["posicoes"] for navio in frota_jogador1):
                        vez_do_jogador = 2
                        navio_atual_idx = 0
                        navio_selecionado = frota_jogador2[navio_atual_idx]
                    else:
                        print("Posicione todos os navios primeiro!")
                else:
            # Verifica se todos os navios do jogador 2 foram posicionados
                    if all(navio["posicoes"] for navio in frota_jogador2):
                        posicionando_navios = False
                        tela = "batalha"
                    else:
                        print("Posicione todos os navios primeiro!")
    # ----- TELA DO MENU -----
    if tela == "menu":
        screen.blit(imagem, (0, 0))

    # ----- TELA DE POSICIONAMENTO -----
    
    elif tela == "jogo":
        screen.blit(grid_fundo, (0, 0))
    
    # Desenha os navios
        desenhar_navios(frota_jogador1 if vez_do_jogador == 1 else frota_jogador2)
    
    # Texto no TOPO - apenas indicação do jogador (amarelo)
        texto_jogador = font.render(f"JOGADOR {vez_do_jogador}", True, (255, 255, 0))
        screen.blit(texto_jogador, (100, TEXTO_TOPO_Y))  # Centralizado
    
    # Texto na BASE - instruções (cinza claro)
        cor_instrucoes = (200, 200, 200)
        screen.blit(font.render("◉ Clique: Posicionar navio", True, cor_instrucoes), 
               (10, TEXTO_BAIXO_Y))
        screen.blit(font.render("◉ Tecla R: Girar navio", True, cor_instrucoes), 
               (10, TEXTO_BAIXO_Y + 20))
        screen.blit(font.render("◉ Enter: Confirmar posições", True, cor_instrucoes), 
               (10, TEXTO_BAIXO_Y + 40))
    
    
    pygame.display.update()
    clock.tick(60)