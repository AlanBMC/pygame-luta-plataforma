import pygame
from globais import *
from classes import *
from mapa import *

pygame.init()
screen = pygame.display.set_mode((1200, 600))
atirador = Atirador(500,500, 3)
soldada = Soldada(500,500,3)
def gravidade(clock, chao):
    global TEMPO, FORCA,GRAVIDADE, ACELERACAO_Y
    TEMPO =clock.get_time()/ 1000.0
    
    FORCA = GRAVIDADE * TEMPO
    atirador.aceleracao_y += FORCA
    
    
    atirador.rect.y += atirador.aceleracao_y
    atirador.rec.y += atirador.aceleracao_y
    if atirador.rect.bottom > chao:
        atirador.rect.bottom = chao
        atirador.aceleracao_y = 0
        

def atualizador_de_acoes():
        global SOLDADA_DIREITA, SOLDADA_ESQUERDA, MOVE_DIREITA, MOVE_ESQUERDA
            ######################verifica_colisao_chao(screen, tm)
        if atirador.atira_1 and not atirador.tiros_1.em_cooldown:
            atirador.tiros_1.atirar(atirador.rect.centerx + (40 if atirador.direcao == 1 else -40), atirador.rect.centery - 20, atirador.direcao)
            atirador.atualiza_acao('atira_1')
        elif atirador.atira_2 and not atirador.tiros_2.em_cooldown:
            atirador.tiros_2.atirar(atirador.rect.centerx + (40 if atirador.direcao == 1 else -40), atirador.rect.centery - 20, atirador.direcao)
            atirador.atualiza_acao('atira_2')
        elif atirador.no_ar and not atirador.atira_2:
            atirador.atualiza_acao('pula')
        
        elif atirador.corre and not atirador.no_ar and not atirador.atira_2:
            atirador.atualiza_acao('corre')
        elif atirador.rola and not atirador.corre and not atirador.no_ar and not atirador.atira_2:
            
            atirador.atualiza_acao('rola')
        elif MOVE_DIREITA or MOVE_ESQUERDA:
            atirador.atualiza_acao('anda')
        else:
            atirador.atualiza_acao('parado')



def verifica_colisao_chao(surface, tm, camera_x, camera_y, scale=1):
    global CHAO
    tw = int(tm.tilewidth * scale)
    th = int(tm.tileheight * scale)
    map_width = tm.width * tw
    map_height = tm.height * th

    # Limitar a câmera dentro dos limites do mapa
    camera_x = max(0, min(camera_x, map_width - surface.get_width()))
    camera_y = max(0, min(camera_y, map_height - surface.get_height()))

    start_x = int(camera_x / tw)
    end_x = start_x + int(surface.get_width() / tw) + 1  # +1 para cobrir casos de borda
    start_y = int(camera_y / th)
    end_y = start_y + int(surface.get_height() / th) + 1  # +1 para cobrir casos de borda

    for rect in tm.colisor_pisos_chao:
        scaled_rect = pygame.Rect(
            (rect.x * scale) - camera_x, (rect.y * scale) - camera_y, rect.width * scale, rect.height * scale)
        pygame.draw.rect(surface, (255, 0, 0), scaled_rect, 2)
        if atirador.rec.colliderect(scaled_rect):
            # Ajuste o personagem para que fique em cima do chão
            if atirador.aceleracao_y > 0:  # Verifica se o personagem está caindo
                atirador.rec.bottom = scaled_rect.top
                atirador.rect.bottom = atirador.rec.bottom
                CHAO = scaled_rect.top
                atirador.aceleracao_y = 0
                atirador.no_ar = False
            

def main():
    global RUN, CHAO, MOVE_ESQUERDA, MOVE_DIREITA
    clock = pygame.time.Clock()
    tm = carrega_mapa('terreno1.tmx')
    mapa_largura = tm.width * tm.tilewidth
    mapa_altura = tm.height * tm.tileheight

    while RUN:
        screen.fill((0, 0, 0))
        atirador.desenha(screen)
        camera_x = atirador.rect.centerx - screen.get_width() // 2
        camera_y = atirador.rect.centery - screen.get_height() // 2

        desenha_mapa(screen, tm, camera_x, camera_y)
        gravidade(clock, CHAO)
        atualizador_de_acoes()
        atirador.atualizar_adrenalina()
        atirador.tiros_1.atualizar()
        atirador.tiros_2.atualizar()
        atirador.movimento(MOVE_ESQUERDA, MOVE_DIREITA)
        verifica_colisao_chao(screen, tm, camera_x, camera_y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    MOVE_ESQUERDA = True
                if event.key == pygame.K_RIGHT:
                    MOVE_DIREITA = True
                if event.key == pygame.K_UP:
                    atirador.pulando()
                if event.key == pygame.K_q:
                    if atirador.tiros_1.cooldown_tiros:
                        atirador.atira_1 = True

                if event.key == pygame.K_w and (MOVE_DIREITA or MOVE_ESQUERDA):
                    atirador.atira_2 = True
                    
                if event.key == pygame.K_a and (MOVE_DIREITA or MOVE_ESQUERDA):
                    if atirador.adrenalina > 0 and not atirador.em_cooldown:
                        atirador.corre = True
                if event.key == pygame.K_s and (MOVE_DIREITA or MOVE_ESQUERDA):
                    if atirador.adrenalina > 0 and not atirador.em_cooldown:
                        atirador.rola = True

            elif event.type == pygame.KEYUP:  
                if event.key == pygame.K_LEFT:
                    MOVE_ESQUERDA = False
                elif event.key == pygame.K_RIGHT:
                    MOVE_DIREITA = False
                elif event.key == pygame.K_q:
                    atirador.atira_1 = False
                elif event.key == pygame.K_w:
                    atirador.atira_2 = False
                elif event.key == pygame.K_a:
                    atirador.corre = False
                elif event.key == pygame.K_s:
                    atirador.rola = False
        pygame.display.update()
        clock.tick(60) 
        pass
main()