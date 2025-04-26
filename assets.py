import pygame
from config import *

def carregar_imagens():
   
    imagens = {
        'intro': pygame.image.load("Naval Battle Assets/intro.png").convert(),
        'grid_fundo': pygame.image.load("Naval Battle Assets/Naval Battle Assets/oceangrid_final.png").convert_alpha(),
        'radar_fundo': pygame.image.load("Naval Battle Assets/Naval Battle Assets/radargrid_final.png").convert_alpha(),
        'bomba_agua': pygame.image.load("Naval Battle Assets/alvo_agua.png").convert_alpha(),
        'bomba_acerto': pygame.image.load("Naval Battle Assets/barco_explodido.png").convert_alpha(),
        'bomba_alvo': pygame.image.load("Naval Battle Assets/alvo.png").convert_alpha()
    }
    

    imagens['intro'] = pygame.transform.scale(imagens['intro'], (SCREEN_WIDTH, SCREEN_HEIGHT))
    imagens['grid_fundo'] = pygame.transform.scale(imagens['grid_fundo'], (SCREEN_WIDTH, SCREEN_HEIGHT))
    imagens['radar_fundo'] = pygame.transform.scale(imagens['radar_fundo'], (SCREEN_WIDTH, SCREEN_HEIGHT))
    imagens['bomba_agua'] = pygame.transform.scale(imagens['bomba_agua'], (TAMANHO_CELULA, TAMANHO_CELULA))
    imagens['bomba_acerto'] = pygame.transform.scale(imagens['bomba_acerto'], (TAMANHO_CELULA, TAMANHO_CELULA))
    imagens['bomba_alvo'] = pygame.transform.scale(imagens['bomba_alvo'], (TAMANHO_CELULA, TAMANHO_CELULA))
    
    return imagens

def carregar_sons():
   
    sons = {
        'explosao': pygame.mixer.Sound("sons_batalha/explosion-47163.mp3"),
        'splash': pygame.mixer.Sound("sons_batalha/splash-by-blaukreuz-6261.mp3"),
        'start': pygame.mixer.Sound("sons_batalha/game-start-6104.mp3"),
        'win': pygame.mixer.Sound("sons_batalha/goodresult-82807.mp3"),
        'select_barco': pygame.mixer.Sound("sons_batalha/Metal-Click.mp3"),
        'fundo': pygame.mixer.Sound("sons_batalha/som_intro.mp3")
    }
    
    sons['win'].set_volume(VOLUME_WIN_SOUND)
    sons['fundo'].set_volume(VOLUME_FUNDO_SOUND)
    
    return sons

def carregar_fonte():
    
    return pygame.font.Font("font/Pixeltype.ttf", 20)