import pygame
from globais import *
from classes import *
from mapa import *
import random
pygame.init()
screen = pygame.display.set_mode((1200, 600))
atirador = Atirador(500,500, 4, 50,1,0,100,100,5,10, 10, 15)
soldada = Soldada(100,400, 3.5, 10,1,0,100,100)
soldado = Soldado_dark(300,400, 3.5, 10,1,0,100,100)

######## observações #####
"""

adicionar um personagem implica em: adicionar variaveis na funcao (atualizador_de_acoes), 
gravidade, cria a ia.
e fazer a verificacao de combate e colisao de chao

"""

def gravidade(clock, chao):
    global TEMPO, FORCA,GRAVIDADE, ACELERACAO_Y
    TEMPO =clock.get_time()/ 1000.0
    
    FORCA = GRAVIDADE * TEMPO
    atirador.aceleracao_y += FORCA
    soldada.aceleracao_y += FORCA
    soldado.aceleracao_y += FORCA

    atirador.rect.y += atirador.aceleracao_y
    atirador.rec.y += atirador.aceleracao_y
    if atirador.rect.bottom > chao:
        atirador.rect.bottom = chao
        atirador.aceleracao_y = 0


    soldada.rect.y += soldada.aceleracao_y
    soldada.rec.y += soldada.aceleracao_y
    if soldada.rect.bottom > chao:
        soldada.rect.bottom = chao
        soldada.aceleracao_y = 0
    
    soldado.rect.y += soldado.aceleracao_y
    soldado.rec.y += soldado.aceleracao_y
    if soldado.rect.bottom > chao:
        soldado.rect.bottom = chao
        soldado.aceleracao_y = 0

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
        elif atirador.sofreu_dano:
            atirador.atualiza_acao('sofreu_dano')
            atirador.sofreu_dano = False
        else:
            atirador.atualiza_acao('parado')
        if soldada.corre and not soldada.pulo and not soldada.poder_2 and not soldada.poder_1 and not soldada.poder_3 and not soldada.poder_4:
            soldada.atualiza_acao('corre')
        elif SOLDADA_DIREITA or SOLDADA_ESQUERDA:
            soldada.atualiza_acao('anda')
        elif soldada.pulo:
            soldada.atualiza_acao('pula')
        elif not soldada.pulo and soldada.poder_1 and not soldada.ataques_corpo_a_corpo.em_cooldown:
            soldada.atualiza_acao('poder_1')
        elif not soldada.pulo and soldada.poder_2 and not soldada.poder_1 and not soldada.ataques_corpo_a_corpo.em_cooldown:
            soldada.atualiza_acao('poder_2')
        elif not soldada.pulo and not soldada.poder_2 and not soldada.poder_1 and soldada.poder_3 and not soldada.ataques_corpo_a_corpo.em_cooldown:
            soldada.atualiza_acao('poder_3')
        elif not soldada.pulo and not soldada.poder_2 and not soldada.poder_1 and not soldada.poder_3 and soldada.poder_4 and not soldada.ataques_corpo_a_corpo.em_cooldown:
            soldada.atualiza_acao('poder_4_area')
        elif soldada.sofreu_dano:
            soldada.atualiza_acao('sofreu_dano')
            soldada.sofreu_dano = False
        elif soldada.vida <= 0:
            soldada.atualiza_acao('morte')
        else:
            soldada.atualiza_acao('parado')

#################################### SOLDADO #################################################
        if soldado.corre and not soldado.pulo and not soldado.poder_2 and not soldado.poder_1 and not soldado.poder_3 and not soldado.poder_4:
            soldado.atualiza_acao('corre')
        elif SOLDADO_DIREITA or SOLDADO_ESQUERDA:
            soldado.atualiza_acao('anda')
        elif soldado.pulo:
            soldado.atualiza_acao('pula')
        elif not soldado.pulo and soldado.poder_1 and not soldado.ataques_corpo_a_corpo.em_cooldown:
            soldado.atualiza_acao('poder_1')
            soldado.poder_1 = False
        elif not soldado.pulo and soldado.poder_2 and not soldado.poder_1 and not soldado.ataques_corpo_a_corpo.em_cooldown:
            soldado.atualiza_acao('poder_2')
            soldado.poder_2 = False
        elif not soldado.pulo and not soldado.poder_2 and not soldado.poder_1 and soldado.poder_3 and not soldado.ataques_corpo_a_corpo.em_cooldown:
            soldado.atualiza_acao('poder_3')
            soldado.poder_3 = False
        elif not soldado.pulo and not soldado.poder_2 and not soldado.poder_1 and not soldado.poder_3 and soldado.poder_4 and not soldado.ataques_corpo_a_corpo.em_cooldown:
            soldado.atualiza_acao('poder_4')
            soldado.poder_4 = False
        elif not soldado.pulo and not soldado.poder_2 and not soldado.poder_1 and not soldado.poder_3 and not soldado.poder_4 and soldado.poder_5 and not soldado.ataques_corpo_a_corpo.em_cooldown:
            soldado.atualiza_acao('poder_5')
            soldado.poder_5 = False
        elif not soldado.pulo and not soldado.poder_2 and not soldado.poder_1 and not soldado.poder_3 and not soldado.poder_4 and not soldado.poder_5 and soldado.poder_6 and not soldado.ataques_corpo_a_corpo.em_cooldown:
            soldado.atualiza_acao('poder_6')
            soldado.poder_6 = False
        elif not soldado.pulo and not soldado.poder_2 and not soldado.poder_1 and not soldado.poder_3 and not soldado.poder_4 and not soldado.poder_5 and not soldado.poder_6 and soldado.poder_7 and not soldado.ataques_corpo_a_corpo.em_cooldown:
            soldado.atualiza_acao('poder_7')
            soldado.poder_7 = False
        elif soldado.sofreu_dano:
            soldado.atualiza_acao('sofreu_dano')
            soldado.sofreu_dano = False
        elif soldado.vida <= 0:
            soldado.atualiza_acao('morte')
        else:
            soldado.atualiza_acao('parado')

def numero_aleatorio_(personagem):
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - personagem.ultimo_poder_usado >= personagem.intervalo_poder:
        personagem.ultimo_poder_usado = tempo_atual
        personagem.ultimo_numero_aleatorio = random.randint(1, 7)
    return personagem.ultimo_numero_aleatorio

def ia_soldado_dark():
    global SOLDADO_ESQUERDA, SOLDADO_DIREITA
    distancia = abs(atirador.rec.centerx - soldado.rec.centerx)
    
    numero_aleatorio = numero_aleatorio_(soldado)
    
    if distancia < 70:
        if not soldado.no_ar:
            if not soldado.ataques_corpo_a_corpo.em_cooldown:
                            SOLDADO_DIREITA = False
                            SOLDADO_ESQUERDA = False
                            if numero_aleatorio == 1:
                                soldado.poder_1 = True
                                soldado.dano = soldado.poder_1_dano
                            elif numero_aleatorio == 2:
                                soldado.poder_2 = True
                                soldado.dano = soldado.poder_2_dano
                            elif numero_aleatorio == 3:
                                soldado.poder_3 = True
                                soldado.dano = soldado.poder_3_dano
                            elif numero_aleatorio == 4:
                                soldado.poder_4 = True
                                soldado.dano = soldado.poder_4_dano
                            elif numero_aleatorio == 5:
                                soldado.poder_5 = True
                                soldado.dano = soldado.poder_5_dano
                            elif numero_aleatorio == 6:
                                soldado.poder_6 = True
                                soldado.dano = soldado.poder_6_dano
                            elif numero_aleatorio == 7:
                                soldado.poder_7 = True
                                soldado.dano = soldado.poder_7_dano
                            
    if soldado.vida < 50:
        #fazer o soldado recuar
        pass
    elif soldado.vida > 60 and soldado.vida < 80:
        #fazer o soldado defender
        pass

    if atirador.atira_1:
        if atirador.direcao != soldado.direcao:
            soldado.pular()
    if soldado.rec.centerx > atirador.rec.centerx and distancia > 200:
        SOLDADO_DIREITA = False
        SOLDADO_ESQUERDA = True
        if distancia > 500:
            soldado.corre = True
    elif soldado.rec.centerx < atirador.rec.centerx and distancia > 200:
        SOLDADO_DIREITA = True
        SOLDADO_ESQUERDA = False
        if distancia > 500:
            soldado.corre = True
    
    

def ia_soldada():
    global SOLDADA_DIREITA, SOLDADA_ESQUERDA
    
    distancia = abs(atirador.rec.centerx - soldada.rec.centerx)
    if distancia < 70:
        if not soldada.no_ar:
            if not soldada.ataques_corpo_a_corpo.em_cooldown:
                        soldada.poder_1 = True
                        SOLDADA_DIREITA = False
                        SOLDADA_ESQUERDA = False
    if atirador.atira_1:
        if atirador.direcao != soldada.direcao:
            soldada.pular()
    if soldada.rec.centerx > atirador.rec.centerx and distancia > 200:
        SOLDADA_DIREITA = False
        SOLDADA_ESQUERDA = True
        if distancia > 500:
            soldada.corre = True
    elif soldada.rec.centerx < atirador.rec.centerx and distancia > 200:
        SOLDADA_DIREITA = True
        SOLDADA_ESQUERDA = False
        if distancia > 500:
            soldada.corre = True
        
def desenha_status_atirador(screen):
    fonte = pygame.font.SysFont(None, 24)
    xp_rect = pygame.Rect(10, 10, atirador.xp * 2, 20)  # Largura baseada no XP
    nivel_rect = pygame.Rect(10, 40, 100, 20)
    dano_rect = pygame.Rect(10, 70, atirador.dano * 2, 20)  # Largura baseada no dano
    vida_rect = pygame.Rect(10, 100, atirador.vida * 2, 20)  # Largura baseada na vida

    pygame.draw.rect(screen, (0, 255, 0), xp_rect)
    pygame.draw.rect(screen, (0, 0, 255), nivel_rect)
    pygame.draw.rect(screen, (255, 0, 0), dano_rect)
    pygame.draw.rect(screen, (255, 255, 0), vida_rect)

    screen.blit(fonte.render(f'XP: {atirador.xp}', True, (255, 255, 255)), (xp_rect.x + 5, xp_rect.y + 5))
    screen.blit(fonte.render(f'Nível: {atirador.nivel}', True, (255, 255, 255)), (nivel_rect.x + 5, nivel_rect.y + 5))
    screen.blit(fonte.render(f'Dano: {atirador.dano}', True, (255, 255, 255)), (dano_rect.x + 5, dano_rect.y + 5))
    screen.blit(fonte.render(f'Vida: {atirador.vida}', True, (255, 255, 255)), (vida_rect.x + 5, vida_rect.y + 5))

def desenha_status_soldada(screen):
    fonte = pygame.font.SysFont(None, 24)
    xp_rect = pygame.Rect(10, 110, soldada.xp * 2, 20)  # Largura baseada no XP
    nivel_rect = pygame.Rect(10, 140, 100, 20)
    dano_rect = pygame.Rect(10, 170, soldada.dano * 2, 20)  # Largura baseada no dano
    vida_rect = pygame.Rect(10, 200, soldada.vida * 2, 20)  # Largura baseada na vida

    pygame.draw.rect(screen, (0, 255, 0), xp_rect)
    pygame.draw.rect(screen, (0, 0, 255), nivel_rect)
    pygame.draw.rect(screen, (255, 0, 0), dano_rect)
    pygame.draw.rect(screen, (255, 255, 0), vida_rect)

    screen.blit(fonte.render(f'XP: {soldada.xp}', True, (255, 255, 255)), (xp_rect.x + 5, xp_rect.y + 5))
    screen.blit(fonte.render(f'Nível: {soldada.nivel}', True, (255, 255, 255)), (nivel_rect.x + 5, nivel_rect.y + 5))
    screen.blit(fonte.render(f'Dano: {soldada.dano}', True, (255, 255, 255)), (dano_rect.x + 5, dano_rect.y + 5))
    screen.blit(fonte.render(f'Vida: {soldada.vida}', True, (255, 255, 255)), (vida_rect.x + 5, vida_rect.y + 5))

def reseta(morto):
    personagem = None
    if morto == 'atirador':
        personagem = Atirador(500,500, 4, 10,1,0,100,100)
    elif morto == 'soldada':
        personagem = Soldada(100,400, 3.5, 10,1,0,100,100)
    return personagem


def verificar_colisoes_combate():
    if soldada.vivo:
        for tiro in atirador.tiros_1.tiros + atirador.tiros_2.tiros:
            if tiro.rect.colliderect(soldada.rec):
                soldada.vida -= atirador.dano
                soldada.sofreu_dano = True
                
                if soldada.vida <= 0:
                    atirador.matou_inimigo = True
                    #soldada.vida = 100
                    soldada.vivo = False
                    atirador.xp += soldada.xp_de_morte
                    
                    soldada.xp = 0
    if atirador.vivo:
        for ataque in soldada.ataques_corpo_a_corpo.ataques:
            if ataque.rect.colliderect(atirador.rec):
                atirador.vida -= soldada.dano
                atirador.sofreu_dano = True
                if atirador.vida <= 0:
                    soldada.matou_inimigo = True
                    atirador.vida = 100
                    #atirador.vivo = False
                    soldada.xp += atirador.xp_de_morte
                    atirador.xp = 0
    if soldado.vivo:
        for ataque in soldado.ataques_corpo_a_corpo.ataques:
            if ataque.rect.colliderect(atirador.rec):
                atirador.vida -= soldado.dano
                
                atirador.sofreu_dano = True
                if atirador.vida <= 0:
                    soldado.matou_inimigo = True
                    atirador.vida = 100
                    #atirador.vivo = False
                    soldado.xp += atirador.xp_de_morte
                    atirador.xp = 0


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
        if soldada.rec.colliderect(scaled_rect):
            if soldada.aceleracao_y > 0:
                soldada.rec.bottom = scaled_rect.top
                soldada.rect.bottom = soldada.rec.bottom
                CHAO = scaled_rect.top
                soldada.aceleracao_y = 0
                soldada.no_ar = False

        if soldado.rec.colliderect(scaled_rect):
            if soldado.aceleracao_y > 0:
                soldado.rec.bottom = scaled_rect.top
                soldado.rect.bottom = soldado.rec.bottom
                CHAO = scaled_rect.top
                soldado.aceleracao_y = 0
                soldado.no_ar = False

def main():
    global RUN, CHAO, MOVE_ESQUERDA, MOVE_DIREITA, SOLDADA_DIREITA, SOLDADA_ESQUERDA, SOLDADO_ESQUERDA, SOLDADO_DIREITA
    clock = pygame.time.Clock()
    tm = carrega_mapa('terreno1.tmx')
    #mapa_largura = tm.width * tm.tilewidth
    #mapa_altura = tm.height * tm.tileheight

    while RUN:
        screen.fill((0, 0, 0))
       
        desenha_status_atirador(screen)
        camera_x = atirador.rect.centerx - screen.get_width() // 2
        camera_y = atirador.rect.centery - screen.get_height() // 2
        desenha_mapa(screen, tm, camera_x, camera_y)
        gravidade(clock, CHAO)
        
        atualizador_de_acoes()

        if atirador.vivo:
            atirador.desenha(screen)
            desenha_status_atirador(screen)
            atirador.atualizar_adrenalina()
            atirador.tiros_1.atualizar()
            atirador.tiros_2.atualizar()
            atirador.movimento(MOVE_ESQUERDA, MOVE_DIREITA)
            atirador.progresso_de_status()
        else:
            atirador.desenha_morte(screen)

        if soldada.vivo:
            desenha_status_soldada(screen)
            #ia_soldada()
            soldada.movimento(SOLDADA_ESQUERDA, SOLDADA_DIREITA)
            soldada.atualizar_adrenalina()
            soldada.desenha(screen)
            soldada.ataques_corpo_a_corpo.atualizar()
            soldada.sistama_de_recompensa()
            if soldada.poder_1:
                soldada.atacar(1)
            elif soldada.poder_2:
                soldada.atacar(2)
            elif soldada.poder_3:
                soldada.atacar(3)
            elif soldada.poder_4:
                soldada.atacar(4)
        else:
            soldada.desenha_morte(screen)

        if soldado.vivo:
            
            ia_soldado_dark()
            soldado.movimento(SOLDADO_ESQUERDA, SOLDADO_DIREITA)
            soldado.atualizar_adrenalina()
            soldado.desenha(screen)
            soldado.ataques_corpo_a_corpo.atualizar()
            soldado.sistema_de_recompensa()
            if soldado.poder_1:
                soldado.atacar(1)
            elif soldado.poder_2:
                soldado.atacar(2)
            elif soldado.poder_3:
                soldado.atacar(3)
            elif soldado.poder_4:
                soldado.atacar(4)
            elif soldado.poder_5:
                soldado.atacar(5)
            elif soldado.poder_6:
                soldado.atacar(6)
            elif soldado.poder_7:
                soldado.atacar(7)
        else:
            soldado.desenha_morte(screen)

        
        verifica_colisao_chao(screen, tm, camera_x, camera_y)
        verificar_colisoes_combate()
        
  

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
                if event.key == pygame.K_q and not MOVE_DIREITA and not MOVE_ESQUERDA:
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

                if event.key == pygame.K_l:
                    SOLDADA_DIREITA = True
                if event.key == pygame.K_j:
                    SOLDADA_ESQUERDA = True
                if event.key == pygame.K_i:
                    soldada.pular()
                if event.key == pygame.K_n:
                    SOLDADO_DIREITA = True
                if event.key == pygame.K_u and not soldada.no_ar:
                    if not soldada.ataques_corpo_a_corpo.em_cooldown:
                        soldada.poder_1 = True
                if event.key == pygame.K_y and not soldada.no_ar:
                    if not soldada.ataques_corpo_a_corpo.em_cooldown:
                        soldada.poder_2 = True
                if event.key == pygame.K_h and not soldada.no_ar:
                    if not soldada.ataques_corpo_a_corpo.em_cooldown:    
                        soldada.poder_3 = True
                if event.key == pygame.K_o and not soldada.no_ar:
                    if not soldada.ataques_corpo_a_corpo.em_cooldown:
                        soldada.poder_4 = True
                if event.key == pygame.K_p and (SOLDADA_DIREITA or SOLDADA_ESQUERDA):
                    if soldada.adrenalina > 0 and not soldada.em_cooldown:
                        soldada.corre = True



            elif event.type == pygame.KEYUP:  
                if event.key == pygame.K_LEFT:
                    MOVE_ESQUERDA = False
                elif event.key == pygame.K_RIGHT:
                    MOVE_DIREITA = False
                elif event.key == pygame.K_q  and not (MOVE_DIREITA or MOVE_ESQUERDA):
                    atirador.atira_1 = False
                elif event.key == pygame.K_w:
                    atirador.atira_2 = False
                elif event.key == pygame.K_a:
                    atirador.corre = False
                elif event.key == pygame.K_s:
                    atirador.rola = False

                if event.key == pygame.K_l:
                    SOLDADA_DIREITA = False
                elif event.key == pygame.K_j:
                    SOLDADA_ESQUERDA = False
                elif event.key == pygame.K_u:
                    soldada.poder_1 = False
                elif event.key == pygame.K_y:
                    soldada.poder_2 = False
                elif event.key == pygame.K_h:
                    soldada.poder_3 = False
                elif event.key == pygame.K_o:
                    soldada.poder_4 = False
                if event.key == pygame.K_p:
                    soldada.corre = False
       
        pygame.display.update()
        clock.tick(60)
        pass
main()