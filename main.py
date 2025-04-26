# main.py
import pygame
from sys import exit
from config import *
from assets import carregar_imagens, carregar_sons, carregar_fonte
from game_functions import (criar_frota, desenhar_navios, posicao_valida, 
                          atualizar_posicoes_navio, get_clique_posicionamento,
                          desenhar_tela_batalha, processar_tiro)

def inicializar_jogo():
    
    pygame.init()
    pygame.mixer.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(SCREEN_TITLE)
    
    imagens = carregar_imagens()
    sons = carregar_sons()
    font = carregar_fonte()
    
    
    frota_jogador1 = criar_frota(1)
    frota_jogador2 = criar_frota(2)
    
    grade_jogador1 = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    grade_jogador2 = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    tiros_jogador1 = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    tiros_jogador2 = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    botao_comecar = pygame.Rect(101, 253, 96, 19)
    
    return {
        'screen': screen,
        'imagens': imagens,
        'sons': sons,
        'font': font,
        'frota_jogador1': frota_jogador1,
        'frota_jogador2': frota_jogador2,
        'grade_jogador1': grade_jogador1,
        'grade_jogador2': grade_jogador2,
        'tiros_jogador1': tiros_jogador1,
        'tiros_jogador2': tiros_jogador2,
        'botao_comecar': botao_comecar,
        'clock': pygame.time.Clock(),
        'tela': MENU,
        'vez_do_jogador': 1,
        'posicionando_navios': True,
        'posicao_mouse_grid': None,
        'navio_selecionado': None,
        'navio_atual_idx': 0,
        'posicao_mouse_batalha': None,
        'jogador_acertou': False,
        'vencedor': None,
        'win_sound_played': False
    }

def main():
    
    jogo = inicializar_jogo()
    jogo['sons']['fundo'].play(loops=-1)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if jogo['tela'] == MENU and jogo['botao_comecar'].collidepoint(event.pos):
                    jogo['sons']['start'].play()
                    jogo['tela'] = JOGO
                    jogo['navio_selecionado'] = jogo['frota_jogador1'][jogo['navio_atual_idx']]
                
                elif jogo['tela'] == JOGO and jogo['posicionando_navios']:
                    jogo['sons']['select_barco'].play()
                    
                    if event.button == 1:  
                        posicao = get_clique_posicionamento(event.pos[0], event.pos[1])
                        if posicao and jogo['navio_selecionado']:
                            row, col = posicao
                            grade_atual = jogo['grade_jogador1'] if jogo['vez_do_jogador'] == 1 else jogo['grade_jogador2']

                            if posicao_valida(jogo['navio_selecionado'], row, col, grade_atual):
                                atualizar_posicoes_navio(jogo['navio_selecionado'], row, col, grade_atual)

                                jogo['navio_atual_idx'] += 1
                                if jogo['navio_atual_idx'] < len(jogo['frota_jogador1'] if jogo['vez_do_jogador'] == 1 else jogo['frota_jogador2']):
                                    jogo['navio_selecionado'] = jogo['frota_jogador1'][jogo['navio_atual_idx']] if jogo['vez_do_jogador'] == 1 else jogo['frota_jogador2'][jogo['navio_atual_idx']]
                                else:
                                    if jogo['vez_do_jogador'] == 1:
                                        jogo['vez_do_jogador'] = 2
                                        jogo['navio_atual_idx'] = 0
                                        jogo['navio_selecionado'] = jogo['frota_jogador2'][jogo['navio_atual_idx']]
                                    else:
                                        jogo['posicionando_navios'] = False
                                        jogo['tela'] = BATALHA
                                        jogo['jogador_acertou'] = False

                    elif event.button == 3:  
                        if jogo['navio_selecionado']:
                            jogo['navio_selecionado']['horizontal'] = not jogo['navio_selecionado']['horizontal']
                
                elif jogo['tela'] == BATALHA:
                    if event.button == 1 and jogo['posicao_mouse_batalha']:  
                        row, col = jogo['posicao_mouse_batalha']
                        jogador_acertou, mudar_jogador, vencedor = processar_tiro(
                            row, col, jogo['vez_do_jogador'], 
                            jogo['tiros_jogador1'], jogo['tiros_jogador2'],
                            jogo['grade_jogador1'], jogo['grade_jogador2'],
                            jogo['frota_jogador1'], jogo['frota_jogador2'],
                            jogo['sons']
                        )
                        
                        jogo['jogador_acertou'] = jogador_acertou
                        if mudar_jogador:
                            jogo['vez_do_jogador'] = 2 if jogo['vez_do_jogador'] == 1 else 1
                        if vencedor:
                            jogo['tela'] = FIM
                            jogo['vencedor'] = vencedor

            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                pos = get_clique_posicionamento(mouse_x, mouse_y)
                
                if jogo['tela'] == JOGO and jogo['posicionando_navios']:
                    jogo['posicao_mouse_grid'] = pos if pos else None
                elif jogo['tela'] == BATALHA:
                    jogo['posicao_mouse_batalha'] = pos if pos else None

        
        if jogo['tela'] == MENU:
            jogo['screen'].blit(jogo['imagens']['intro'], (0, 0))
        
        elif jogo['tela'] == JOGO:
            jogo['screen'].blit(jogo['imagens']['grid_fundo'], (0, 0))
            
            frota = jogo['frota_jogador1'] if jogo['vez_do_jogador'] == 1 else jogo['frota_jogador2']
            desenhar_navios(
                jogo['screen'], frota, 
                jogo['navio_selecionado'], 
                jogo['posicao_mouse_grid'],
                jogo['grade_jogador1'] if jogo['vez_do_jogador'] == 1 else jogo['grade_jogador2']
            )

            texto_jogador = jogo['font'].render(f"JOGADOR {jogo['vez_do_jogador']}", True, COR_TEXTO)
            jogo['screen'].blit(texto_jogador, (120, TEXTO_TOPO_Y + 15))
            jogo['screen'].blit(jogo['font'].render("Clique: Selecionar", True, COR_INSTRUCOES), 
                              (30, TEXTO_BAIXO_Y + 10))
        
        elif jogo['tela'] == BATALHA:
            tiros = jogo['tiros_jogador1'] if jogo['vez_do_jogador'] == 1 else jogo['tiros_jogador2']
            desenhar_tela_batalha(
                jogo['screen'], tiros, jogo['posicao_mouse_batalha'], 
                jogo['vez_do_jogador'], jogo['font'], jogo['imagens']
            )
        
        elif jogo['tela'] == FIM:
            if not jogo['win_sound_played']:
                jogo['sons']['fundo'].stop()
                jogo['sons']['win'].play()
                jogo['win_sound_played'] = True
            
            jogo['screen'].fill((0, 0, 0))
            texto = jogo['font'].render(f"JOGADOR {jogo['vencedor']} VENCEU!", True, COR_TEXTO)
            jogo['screen'].blit(texto, (100, 150))

        pygame.display.update()
        jogo['clock'].tick(60)

if __name__ == "__main__":
    main()