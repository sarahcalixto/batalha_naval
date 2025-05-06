import pygame
from config import *

def criar_frota(jogador):
   
    return [
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

def posicao_valida(navio, row, col, grade):

    if row < 1 or col < 1:
        return False
    
    
    if col + navio["tamanho"] - 1 > GRID_PLAYABLE_SIZE:
        return False
    for i in range(navio["tamanho"]):
        if grade[row][col + i] != 0:
            return False
    
    return True

def atualizar_posicoes_navio(navio, row, col, grade):
   
    navio["posicoes"] = [] 
    for i in range(navio["tamanho"]):
        navio["posicoes"].append((row, col + i))
        
    for r, c in navio["posicoes"]:
        if 1 <= r <= GRID_PLAYABLE_SIZE and 1 <= c <= GRID_PLAYABLE_SIZE:
            grade[r][c] = 1



def get_clique_posicionamento(mouse_x, mouse_y):
   
    col = (mouse_x - OFFSET_X) // TAMANHO_CELULA + 1
    row = (mouse_y - OFFSET_Y) // TAMANHO_CELULA + 1
    
    if 1 <= col <= GRID_PLAYABLE_SIZE and 1 <= row <= GRID_PLAYABLE_SIZE:
        return row, col
    return None


def desenhar_navios(screen, frota, navio_selecionado=None, posicao_mouse=None, grade=None):
    
    for navio in frota:
        if navio["posicoes"]:
            for row, col in navio["posicoes"]:
                x = OFFSET_X + (col - 1) * TAMANHO_CELULA
                y = OFFSET_Y + (row - 1) * TAMANHO_CELULA
                pygame.draw.rect(screen, navio["cor"], (x, y, TAMANHO_CELULA, TAMANHO_CELULA))

    if navio_selecionado and posicao_mouse and grade:
        row, col = posicao_mouse
        valido = posicao_valida(navio_selecionado, row, col, grade)
        cor = navio_selecionado["cor"] if valido else COR_NAVIO_INVALIDO

        for i in range(navio_selecionado["tamanho"]):
            c = col + i
            r = row
           
            if 1 <= r <= GRID_PLAYABLE_SIZE and 1 <= c <= GRID_PLAYABLE_SIZE:
                x = OFFSET_X + (c - 1) * TAMANHO_CELULA
                y = OFFSET_Y + (r - 1) * TAMANHO_CELULA
                pygame.draw.rect(screen, cor, (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 2)

def desenhar_tela_batalha(screen, tiros, posicao_mouse, jogador_atual, font, imagens):
    
    screen.blit(imagens['radar_fundo'], (0, 0))
    
    for row in range(1, GRID_PLAYABLE_SIZE + 1):
        for col in range(1, GRID_PLAYABLE_SIZE + 1):
            x = OFFSET_X + (col - 1) * TAMANHO_CELULA
            y = OFFSET_Y + (row - 1) * TAMANHO_CELULA
            
            if tiros[row][col] == 1: 
                screen.blit(imagens['bomba_agua'], (x, y))
            elif tiros[row][col] == 2:  
                screen.blit(imagens['bomba_acerto'], (x, y))
    
    if posicao_mouse:
        row, col = posicao_mouse
        x = OFFSET_X + (col - 1) * TAMANHO_CELULA
        y = OFFSET_Y + (row - 1) * TAMANHO_CELULA
        screen.blit(imagens['bomba_alvo'], (x, y))
    
    texto_jogador = font.render(f"JOGADOR {jogador_atual} ATIRANDO", True, COR_TEXTO)
    screen.blit(texto_jogador, (100, TEXTO_TOPO_Y + 10))
    screen.blit(font.render("Clique: Atirar", True, COR_INSTRUCOES), 
               (30, TEXTO_BAIXO_Y + 10))

def processar_tiro(row, col, jogador_atual, tiros_jogador1, tiros_jogador2, 
                  grade_jogador1, grade_jogador2, frota_jogador1, frota_jogador2, sons):
   
    jogador_acertou = False
    mudar_jogador = False
    vencedor = None
    
    grade_alvo = grade_jogador2 if jogador_atual == 1 else grade_jogador1
    tiros = tiros_jogador1 if jogador_atual == 1 else tiros_jogador2
    
    if tiros[row][col] != 0:
        return jogador_acertou, mudar_jogador, vencedor
    
    if grade_alvo[row][col] == 1:
        tiros[row][col] = 2
        jogador_acertou = True
        sons['explosao'].play()
        
        frota_alvo = frota_jogador2 if jogador_atual == 1 else frota_jogador1
        for navio in frota_alvo:
            if (row, col) in navio["posicoes"]:
                if all(tiros[r][c] == 2 for (r, c) in navio["posicoes"]):
                    print(f"Navio de tamanho {navio['tamanho']} afundado!")
        
        if all(all(tiros[r][c] == 2 for (r, c) in navio["posicoes"]) for navio in frota_alvo):
            vencedor = jogador_atual
    else:
        tiros[row][col] = 1
        jogador_acertou = False
        mudar_jogador = True
        sons['splash'].play()
    
    return jogador_acertou, mudar_jogador, vencedor