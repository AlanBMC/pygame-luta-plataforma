import pygame
from globais import *
import random

class Tiro:
    def __init__(self, x, y, direcao, tipo):
        self.rect = pygame.Rect(x, y, 10, 5)  # Define o tamanho do tiro
        self.velocidade = 20  # Velocidade do tiro
        self.tipo = tipo
        if self.tipo == 1:
            self.tiros_sprites = [pygame.transform.scale(pygame.image.load(f'tiro1/{i+1}.png').convert_alpha(), (30,30))for i in range(30)]
        elif self.tipo == 2:
            self.tiros_sprites = [pygame.transform.scale(pygame.image.load(f'tiro2/{i+1}.png').convert_alpha(), (30,30))for i in range(30)]
        self.tiro_rec = self.tiros_sprites[0].get_rect(topleft=(x,y))
        self.tipo = tipo
        self.direcao = direcao
        self.flip = False if direcao == -1 else True
        self.animacao_index = 0
        self.frame_count = len(self.tiros_sprites)
        
    def atualizar(self):
        self.rect.x += self.velocidade * self.direcao
        self.tiro_rec = self.rect
        self.animacao_index += 1
        if self.animacao_index >= self.frame_count:
            self.animacao_index = 0

    def desenha(self, screen, camera):
        tiro_image = self.tiros_sprites[self.animacao_index]
        screen.blit(pygame.transform.flip(tiro_image, self.flip, False), camera.apply_rect(self.tiro_rec).move(0,-10))

class Tiros:
    def __init__(self, intervalo_entre_tiros, cooldown_tiros, numero_de_disparos, tipo):
        self.tiros = []
        self.tipo = tipo
        self.tempo_ultimo_tiro = pygame.time.get_ticks()
        self.intervalo_entre_tiros = intervalo_entre_tiros
        self.numero_de_disparos = numero_de_disparos
        self.em_cooldown = False
        self.cooldown_tiros = cooldown_tiros

    def atualizar(self, camera):
        agora = pygame.time.get_ticks()
        if self.em_cooldown:
            if agora - self.tempo_ultimo_tiro >= self.cooldown_tiros:
                self.numero_de_disparos = 10  # Restaurar disparos após o cooldown
                self.em_cooldown = False
        for tiro in self.tiros:
            tiro.atualizar()
            if tiro.rect.right < -camera.camera.x or tiro.rect.left > -camera.camera.x + 1200:
                self.tiros.remove(tiro)

    def desenha(self, screen, camera):
        for tiro in self.tiros:
            tiro.desenha(screen, camera)

    def atirar(self, x, y, direcao):
        agora = pygame.time.get_ticks()
        if not self.em_cooldown:
            if agora - self.tempo_ultimo_tiro >= self.intervalo_entre_tiros:
                if self.numero_de_disparos > 0:
                    tiro = Tiro(x, y, direcao, self.tipo)
                    self.tiros.append(tiro)
                    self.tempo_ultimo_tiro = agora
                    self.numero_de_disparos -= 1
                else:
                    self.em_cooldown = True
                    self.tempo_ultimo_tiro = agora  # Iniciar cooldown

class Atirador:
    def __init__(self, x, y, velocidade, dano, nivel, xp, dinheiro, vida, velocidade_ataque, adrenalina, quantidade_disparos_skil1, quantidade_disparos_skil2):
        self.rec = pygame.Rect((x,y, 20, 80))
        self.flip = True # de frente
        self.velocidade = velocidade
        self.frame_index = 0
        self.aceleracao_y = 0
        self.direcao = 1 # esquerda
        self.acao_atual = 'parado'
        self.no_ar = False
        # variaveis de animacao
        #variaveis de controle de sprites
        self.tempo_ultima_animacao = pygame.time.get_ticks()
        self.tempo_entre_frames = 100
        self.sofreu_dano = False
        # variaveis de recarga
        self.corre = False
        self.rola = False
        self.atira_1 = False
        self.atira_2 = False
        self.tempo_ultima_adrenalina = pygame.time.get_ticks()
        self.intervalo_adrenalina = 500
        self.em_cooldown = False
        self.cooldown_adrenalina = 5000
        self.velocidade_base = velocidade

        # sistema de recompensa -  status do personagem.
        self.xp_de_morte = 50 
        self.adrenalina = adrenalina
        self.adrenalina_base = adrenalina
        self.velocidade_ataque = velocidade_ataque
        self.dano = dano
        self.nivel = nivel
        self.xp = xp
        self.dinheiro = dinheiro
        self.vida = vida
        self.vivo = True
        self.matou_inimigo = False
        self.xp_anterior = self.xp
        self.quantidade_disparos_skil1 = quantidade_disparos_skil1
        self.quantidade_disparos_skil2 = quantidade_disparos_skil2
        self.ultimo_nivel_checado = 0
        self.xp_necessario = 200

        self.sprite_skill_1= pygame.transform.scale(pygame.image.load(f'skillsatirador/skill_1.png').convert_alpha(), (30,30))
        self.sprite_skill_2 = pygame.transform.scale(pygame.image.load(f'skillsatirador/skill_2.png').convert_alpha(), (30,30))

        self.sprites = [pygame.transform.scale(pygame.image.load(f'atirador/({i+1}).png').convert_alpha(), (120, 90)) for i in range(202)]
        self.acoes = {
            'parado': self.sprites[1:18],
            'anda': self.sprites[56:63],
            'pula': self.sprites[64:65],
            'atira_1': self.sprites[19:55],
            'atira_2': self.sprites[71:103],
            'corre': self.sprites[104:111],
            'rola': self.sprites[112:121],
            'morte': self.sprites[122:128],
            'sofreu_dano': self.sprites[122:125]
        }
        self.img = self.acoes[self.acao_atual][0]
        self.rect = self.sprites[0].get_rect()
        self.rect.center = (x, y+20)
        self.rec.center = (x+10,y-50)
        self.tiros_1 = Tiros(intervalo_entre_tiros=400, cooldown_tiros=5000, numero_de_disparos=quantidade_disparos_skil1, tipo =1)
        self.tiros_2 = Tiros(intervalo_entre_tiros=300, cooldown_tiros=5000, numero_de_disparos=quantidade_disparos_skil2, tipo =2)


    def movimento(self, esquerda, direita, map_width, map_height):
        dx= 0
       
        if self.corre:
            self.velocidade = self.velocidade_base + 0.5
        elif self.rola:
            self.velocidade = self.velocidade_base + 1.5
        else:
            self.velocidade = self.velocidade_base

        if esquerda:
            dx = -self.velocidade
            self.flip = True
            self.direcao = -1
        if direita:
            dx = +self.velocidade
            self.flip = False
            self.direcao = 1

   
        self.rec.x += dx
        self.rect.x += dx
        self.rec.centerx = self.rect.centerx - (10 if self.direcao == 1 else - 10)
       
    def progresso_de_status(self):
        subiu_de_nivel = self.proximo_nivel()
        if subiu_de_nivel:
            if self.nivel < 10:
                self.dano += 3
                self.vida += 20
                self.dinheiro += 50
                self.adrenalina += 1
            elif self.nivel % 10 == 0 and self.nivel != self.ultimo_nivel_checado:
                self.dano += 5
                self.vida += 30
                self.adrenalina += 3
                self.dinheiro += 70
                self.adrenalina_base = self.adrenalina
                self.velocidade_ataque += 0.5
                self.quantidade_disparos_skil1 += 2
                self.quantidade_disparos_skil2 += 2
            elif self.nivel % 20 == 0 and self.nivel != self.ultimo_nivel_checado:
                self.dano += 5
                self.vida += 30
                self.adrenalina += 3
                self.dinheiro += 70
                self.adrenalina_base = self.adrenalina
                self.velocidade_ataque += 0.5
                self.quantidade_disparos_skil1 += 2
                self.quantidade_disparos_skil2 += 2
            elif self.nivel % 30 == 0 and self.nivel != self.ultimo_nivel_checado:
                self.dano += 5
                self.vida += 30
                self.adrenalina += 3
                self.dinheiro += 70
                self.adrenalina_base = self.adrenalina
                self.velocidade_ataque += 0.5
                self.quantidade_disparos_skil1 += 2
                self.quantidade_disparos_skil2 += 2

    def proximo_nivel(self):
        if self.xp >= self.xp_necessario:
            self.xp = 0
            self.nivel += 1
            if self.nivel < 10:
                self.xp_necessario += 100
            elif self.nivel % 10 == 0 and self.nivel != self.ultimo_nivel_checado:
                self.xp_necessario += 1000
            elif self.nivel % 20 == 0 and self.nivel != self.ultimo_nivel_checado:
                self.xp_necessario += 5000
            elif self.nivel % 30 == 0 and self.nivel != self.ultimo_nivel_checado:
                self.xp_necessario += 10000
            self.ultimo_nivel_checado = self.nivel
            return True
        return False


    def atualizar_adrenalina(self):
        agora = pygame.time.get_ticks()
        if self.corre or self.rola:
            if agora - self.tempo_ultima_adrenalina >= self.intervalo_adrenalina:
                if self.adrenalina > 0:
                    self.adrenalina -= 1
                    self.tempo_ultima_adrenalina = agora
                else:
                    self.corre = False
                    self.rola = False
                    self.em_cooldown = True
                    self.tempo_ultima_adrenalina = agora  # Iniciar cooldown
        elif self.em_cooldown:
            if agora - self.tempo_ultima_adrenalina >= self.cooldown_adrenalina:
                self.adrenalina = self.adrenalina_base  # Restaurar adrenalina após o cooldown
                self.em_cooldown = False
        else:
            if self.adrenalina < 10 and agora - self.tempo_ultima_adrenalina >= self.intervalo_adrenalina:
                self.adrenalina += 1
                self.tempo_ultima_adrenalina = agora

    def atualiza_animacao(self):
        agora = pygame.time.get_ticks()
        if self.atira_1:
            self.tempo_entre_frames = 40
        elif self.atira_2:
            self.tempo_entre_frames = 40
        elif self.sofreu_dano:
            self.tempo_entre_frames = 100
        else:
            self.tempo_entre_frames = 60

        if agora - self.tempo_ultima_animacao > self.tempo_entre_frames:
            self.tempo_ultima_animacao = agora  # Atualiza o tempo da última animação
            self.frame_index += 1
            if self.frame_index >= len(self.acoes[self.acao_atual]):
                self.frame_index = 0
            self.img = self.acoes[self.acao_atual][self.frame_index]
    
    def atualiza_acao(self, nova_acao):
        global MOVE_DIREITA, MOVE_ESQUERDA

        if self.tiros_1.em_cooldown  and nova_acao == 'atira_1':
            nova_acao = 'parado' 
        if self.tiros_2.em_cooldown and nova_acao == 'atira_2':
            nova_acao = 'parado'

        if nova_acao != self.acao_atual:
            self.acao_atual = nova_acao
            self.frame_index = 0
        if self.no_ar and self.acao_atual != 'pula':  
            self.acao_atual = 'pula'
            self.frame_index = 0
        if self.atira_2 and (MOVE_DIREITA or MOVE_ESQUERDA):
            self.acao_atual = 'atira_2'
            self.frame_index = 0

    def pulando(self):
        if not self.no_ar:
            self.aceleracao_y = -7  # Impulso inicial do pulo (ajuste este valor)
            self.no_ar = True


       
    def desenha(self, screen, camera):
        self.atualiza_animacao()

        pygame.draw.rect(screen, (255, 0, 0), camera.apply_rect(self.rec))
        screen.blit(pygame.transform.flip(self.img, self.flip, False), camera.apply_rect(self.rect).move(0,10))

        self.tiros_1.desenha(screen, camera)
        self.tiros_2.desenha(screen, camera)
    
    def desenha_morte(self, screen):
        agora = pygame.time.get_ticks()
        
        if not hasattr(self, 'tempo_morte'):
            self.tempo_morte = agora  # Marca o tempo de morte inicial

        if agora - self.tempo_ultima_animacao > self.tempo_entre_frames:
            self.tempo_ultima_animacao = agora
            self.frame_index += 1
            if self.frame_index >= len(self.acoes['morte']):
                self.frame_index = len(self.acoes['morte']) - 1  # Fixa no último frame de morte
            self.img = self.acoes['morte'][self.frame_index]
        
        if agora - self.tempo_morte < 5000:  # Exibe o corpo por 5 segundos
            screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect.move(0, -30))
        else:
            self.img = None  # Remove o corpo após 5 segundos

class Soldada:
    def __init__(self, x, y, velocidade, dano, nivel, xp, dinheiro, vida):
        self.rec = pygame.Rect((x,y, 20, 80))
        self.velocidade = velocidade

        self.ultimo_poder_usado = 0
        self.intervalo_poder = 5000
        self.ultimo_numero_aleatorio = random.randint(1, 7)
        #variaveis de controle de sprites
        self.frame_index = 0
        self.direcao = 1 # esquerda
        self.flip = True # de frente
        self.acao_atual = 'parado'
        self.tempo_ultima_animacao = pygame.time.get_ticks()
        self.tempo_entre_frames = 60
        self.pulo = False
        self.no_ar = False
        self.corre = False
        self.sofreu_dano = False
        #sistema de status e recompensa
        self.dano = dano
        self.nivel = nivel
        self.xp = xp
        self.dinheiro = dinheiro
        self.vida = vida
        self.vivo = True
        self.matou_inimigo = False
        self.xp_anterior = self.xp
        self.xp_de_morte = 50

        self.aceleracao_y = 0
      
        self.velocidade_base = velocidade
        self.poder_1 = False
        self.poder_2 = False
        self.poder_3 = False
        self.poder_4 = False
        self.tempo_ultima_adrenalina = pygame.time.get_ticks()
        self.intervalo_adrenalina = 500
        self.adrenalina = 10
        self.em_cooldown = False
        self.cooldown_adrenalina = 5000
        self.sprites = [pygame.transform.scale(pygame.image.load(f'soldada/({i+1}).png').convert_alpha(), (160, 140)) for i in range(246)]
       
        self.acoes = {
            'parado': self.sprites[1:13],
            'anda': self.sprites[14:23],
            'corre': self.sprites[152:159],
            'pula': self.sprites[36:42],
            'poder_1': self.sprites[50:65],
            'poder_2': self.sprites[66:74],
            'poder_3': self.sprites[83:98],
            'poder_4_area': self.sprites[175:186],
            'poder_5': self.sprites[161:167],
            'poder_6': self.sprites[169:174],
            'vitoria': self.sprites[244:246],
            'morte': self.sprites[140:144],
            'sofreu_dano': self.sprites[139:141]
        }
        self.img = self.acoes[self.acao_atual][0]
        self.rect = self.sprites[0].get_rect()
        self.rect.center = (x, y)
        
        self.rec.center = (self.rect.centerx -5, self.rect.top)
        self.ataques_corpo_a_corpo = AtaquesCorpoACorpo(intervalo_entre_ataques=500, cooldown_ataques=2000, numero_de_ataques=3)

        
    def sistama_de_recompensa(self):
        if self.vivo and self.matou_inimigo:
            self.xp_anterior = self.xp
            self.xp += 10
            self.dinheiro += 10
            self.matou_inimigo = False
        if self.xp > 100:
            self.xp = 0
            self.nivel += 1
            self.dano += 10
            self.vida += 50
            
        
     
    def atualizar_adrenalina(self):
        agora = pygame.time.get_ticks()
        
        if self.corre:
            if agora - self.tempo_ultima_adrenalina >= self.intervalo_adrenalina:
                if self.adrenalina > 0:
                    self.adrenalina -= 1
                    self.tempo_ultima_adrenalina = agora
                else:
                    self.corre = False
                    self.em_cooldown = True
                    self.tempo_ultima_adrenalina = agora  # Iniciar cooldown
        elif self.em_cooldown:
            if agora - self.tempo_ultima_adrenalina >= self.cooldown_adrenalina:
                self.adrenalina = 10  # Restaurar adrenalina após o cooldown
                self.em_cooldown = False
        else:
            if self.adrenalina < 10 and agora - self.tempo_ultima_adrenalina >= self.intervalo_adrenalina:
                self.adrenalina += 1
                self.tempo_ultima_adrenalina = agora
       
       
    def movimento(self, move_esquerda, move_direita):
       
        dx = 0
        
        if self.corre:
            self.velocidade = self.velocidade_base + 1.5
        else:
            self.velocidade = self.velocidade_base
       
        if move_direita:
            dx = +self.velocidade
            self.flip = False
            self.direcao = 1
            

        if move_esquerda:
            dx = -self.velocidade
            self.flip = True
            self.direcao = -1
            
            
        self.rect.x += dx
        self.rec.x += dx
        self.rec.centerx = self.rect.centerx - (15 if self.direcao == 1 else - 15)
       
        

    def pular(self):
        if not self.no_ar:  # Só pode pular se não estiver no ar
            self.aceleracao_y = -7  # Impulso inicial do pulo (ajuste este valor)
            self.no_ar = True

    def atualiza_acao(self, nova_acao):
        global SOLDADA_ESQUERDA, SOLDADA_DIREITA
        
        if nova_acao != self.acao_atual:
            self.acao_atual = nova_acao
            self.frame_index = 0
            
        if self.no_ar and self.acao_atual != 'pula':  
            self.acao_atual = 'pula'
            self.frame_index = 0

    def atualiza_animacao(self):
        agora = pygame.time.get_ticks()
        if self.poder_1:
            self.tempo_entre_frames = 50
        elif self.poder_2:
            self.tempo_entre_frames = 50
        elif self.poder_3:
            self.tempo_entre_frames = 50
        elif self.poder_4:
            self.tempo_entre_frames = 50
        elif self.sofreu_dano:
            self.tempo_entre_frames = 200
        elif not self.vivo:
            self.tempo_entre_frames = 200
        else:
            self.tempo_entre_frames = 60

        if agora - self.tempo_ultima_animacao > self.tempo_entre_frames:
            self.tempo_ultima_animacao = agora  # Atualiza o tempo da última animação
            self.frame_index += 1
            if self.frame_index >= len(self.acoes[self.acao_atual]):
                self.frame_index = 0
            self.img = self.acoes[self.acao_atual][self.frame_index]
    
    def atualizar(self):
        self.atualiza_animacao()

    def desenha(self, screen, camera):
        self.atualiza_animacao()
        #pygame.draw.rect(screen, (255,0,0), self.rec)
        #screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect.move(0, 25))
        pygame.draw.rect(screen, (255, 0, 0), camera.apply_rect(self.rec))
        screen.blit(pygame.transform.flip(self.img, self.flip, False), camera.apply_rect(self.rect).move(0, 30))
        self.ataques_corpo_a_corpo.desenha(screen, camera)

    def atacar(self, tipo):
        
        x = self.rect.centerx + (40 if self.direcao == 1 else -60)
        y = self.rect.centery - 20

        self.ataques_corpo_a_corpo.atacar(x, y, self.direcao, tipo)

    def desenha_morte(self, screen):
        agora = pygame.time.get_ticks()
        
        if not hasattr(self, 'tempo_morte'):
            self.tempo_morte = agora  # Marca o tempo de morte inicial

        if agora - self.tempo_ultima_animacao > self.tempo_entre_frames:
            self.tempo_ultima_animacao = agora
            self.frame_index += 1
            if self.frame_index >= len(self.acoes['morte']):
                self.frame_index = len(self.acoes['morte']) - 1  # Fixa no último frame de morte
            self.img = self.acoes['morte'][self.frame_index]
        
        if agora - self.tempo_morte < 5000:  # Exibe o corpo por 5 segundos
            screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect.move(0, 25))
        else:
            self.img = None  # Remove o corpo após 5 segundos

class AtaquesCorpoACorpo:
    def __init__(self, intervalo_entre_ataques, cooldown_ataques, numero_de_ataques):
        self.ataques = []
        self.tempo_ultimo_ataque = pygame.time.get_ticks()
        self.intervalo_entre_ataques = intervalo_entre_ataques
        self.numero_de_ataques = numero_de_ataques
        self.em_cooldown = False
        self.cooldown_ataques = cooldown_ataques

    def atualizar(self):
        agora = pygame.time.get_ticks()

        if self.em_cooldown:
            if agora - self.tempo_ultimo_ataque >= self.cooldown_ataques:
                self.numero_de_ataques = 5  # Restaurar ataques após o cooldown
                self.em_cooldown = False

        for ataque in self.ataques:
            if not ataque.atualizar():
                self.ataques.remove(ataque)

    def desenha(self, screen, camera):
        for ataque in self.ataques:
            ataque.desenha(screen, camera)

    def atacar(self, x, y, direcao, tipo):
        agora = pygame.time.get_ticks()
        if not self.em_cooldown:
            if agora - self.tempo_ultimo_ataque >= self.intervalo_entre_ataques:
                if self.numero_de_ataques > 0:
                    
                    ataque = AtaqueCorpoACorpo(x, y, direcao, tipo)
                    self.ataques.append(ataque)
                    self.tempo_ultimo_ataque = agora
                    self.numero_de_ataques -= 1
                else:
                    self.em_cooldown = True
                    self.tempo_ultimo_ataque = agora  # Iniciar cooldown


class AtaqueCorpoACorpo:
    def __init__(self, x, y, direcao, tipo):
        self.tipo = tipo
        self.direcao = direcao
        self.tempo_ativo = pygame.time.get_ticks()
        self.rect = self.definir_tamanho(x, y)
        self.piscar = False
        self.piscar_intervalo = 50  # Intervalo de piscada em milissegundos
        self.ultima_piscada = pygame.time.get_ticks()
        self.piscar_contador = 0
        self.piscar_limite = self.definir_piscar_limite(tipo)


    def definir_piscar_limite(self, tipo):
        if tipo == 1:
            return 1
        elif tipo == 2:
            return 1
        elif tipo == 3:
            return 1
        elif tipo == 4:
            return 1
        else:
            return 1  # Limite padrão
        
    def definir_tamanho(self, x, y):
        if self.tipo == 1:
            largura, altura = 20, 100
        elif self.tipo == 2:
            largura, altura = 10, 70
        elif self.tipo == 3:
            largura, altura = 50, 50
        elif self.tipo == 4:
            largura, altura = 140, 30
        else:
            largura, altura = 30, 30  # Tamanho padrão
        
        if self.tipo == 4:
            if self.direcao == -1:
                return pygame.Rect(x, y+30, largura, altura)
            elif self.direcao == 1:
                return pygame.Rect(x-100, y+30, largura, altura)
        elif self.tipo == 1:
            if self.direcao == -1:
                return pygame.Rect(x, y, largura, altura)
            elif self.direcao == 1:
                return pygame.Rect(x-10, y, largura, altura)
        elif self.tipo == 2:
            return pygame.Rect(x, y, largura, altura)
        elif self.tipo == 3:
            return pygame.Rect(x, y, largura, altura)
        return pygame.Rect(x, y, largura, altura)

    def atualizar(self):
        agora = pygame.time.get_ticks()
        
        # Lógica de piscar
        if agora - self.ultima_piscada >= self.piscar_intervalo:
            self.piscar = not self.piscar
            self.ultima_piscada = agora
            self.piscar_contador += 1
            if self.piscar_contador >= self.piscar_limite * 2:  # Cada piscada conta como duas trocas
                self.piscar_contador = 0  # Resetar o contador para continuar piscando
                return False
        return True

    def desenha(self, screen, camera):
        if not self.piscar:
            pygame.draw.rect(screen, (0, 255, 0), camera.apply_rect(self.rect))


class Soldado_dark:
    def __init__(self, x, y, velocidade, dano, nivel, xp, dinheiro, vida):
        self.rec = pygame.Rect((x,y, 20, 80))
        self.velocidade = velocidade


        #variaveis de controle de sprites
        self.frame_index = 0
        self.direcao = 1 # esquerda
        self.flip = True # de frente
        self.acao_atual = 'parado'
        self.tempo_ultima_animacao = pygame.time.get_ticks()
        self.tempo_entre_frames = 60
        self.pulo = False
        self.no_ar = False
        self.corre = False
        self.sofreu_dano = False
        #sistema de status e recompensa
        self.dano = dano
        self.nivel = nivel
        self.xp = xp
        self.dinheiro = dinheiro
        self.vida = vida
        self.vivo = True
        self.matou_inimigo = False
        self.xp_anterior = self.xp
        self.xp_de_morte = 50
        self.ultimo_poder_usado = 0
        self.intervalo_poder = 5000
        self.ultimo_numero_aleatorio = random.randint(1, 7)
        self.aceleracao_y = 0
        self.velocidade_base = velocidade
        self.poder_1 = False
        self.poder_2 = False
        self.poder_3 = False
        self.poder_4 = False
        self.poder_5 = False
        self.poder_6 = False
        self.poder_7 = False

        self.ultimo_poder_usado = 0
        self.intervalo_poder = 5000
        self.ultimo_numero_aleatorio = random.randint(1, 7)

        self.tempo_ultima_adrenalina = pygame.time.get_ticks()
        self.intervalo_adrenalina = 500
        self.adrenalina = 10
        self.em_cooldown = False
        self.cooldown_adrenalina = 5000
        self.sprites = [pygame.transform.scale(pygame.image.load(f'soldado/({i+1}).png').convert_alpha(), (160, 140)) for i in range(240)]
        self.acoes = {
            'parado': self.sprites[175:178],
            'anda': self.sprites[179:186],
            'corre': self.sprites[105:112],
            'pula': self.sprites[126:132],
            'poder_1': self.sprites[187:193],
            'poder_2': self.sprites[1:20],
            'poder_3': self.sprites[35:42],
            'poder_4': self.sprites[61:65],
            'poder_5': self.sprites[66:75],
            'poder_6': self.sprites[194:198],
            'poder_7': self.sprites[198:209],
            'vitoria': self.sprites[76:91],
            'morte': self.sprites[97:104],
            'sofreu_dano': self.sprites[97:99],
            'defende': self.sprites[123:124]
        }

        self.img = self.acoes[self.acao_atual][0]
        self.rect = self.sprites[0].get_rect()
        self.rect.center = (x, y)
        self.rec.center = (self.rect.centerx -5, self.rect.top)
        self.ataques_corpo_a_corpo = AtaquesCorpoACorpo_2(intervalo_entre_ataques=500, cooldown_ataques=2000, numero_de_ataques=3)
        self.poder_1_dano = 10
        self.poder_2_dano = 20
        self.poder_3_dano = 30
        self.poder_4_dano = 40
        self.poder_5_dano = 50
        self.poder_6_dano = 60
        self.poder_7_dano = 70
        
    def sistema_de_recompensa(self):
        if self.vivo and self.matou_inimigo:
            self.xp_anterior = self.xp
            self.xp += 10
            self.dinheiro += 10
            self.matou_inimigo = False
        if self.xp > 100:
            self.xp = 0
            self.nivel += 1
            self.dano += 10
            self.vida += 50
            
        
     
    def atualizar_adrenalina(self):
        agora = pygame.time.get_ticks()
        
        if self.corre:
            if agora - self.tempo_ultima_adrenalina >= self.intervalo_adrenalina:
                if self.adrenalina > 0:
                    self.adrenalina -= 1
                    self.tempo_ultima_adrenalina = agora
                else:
                    self.corre = False
                    self.em_cooldown = True
                    self.tempo_ultima_adrenalina = agora  # Iniciar cooldown
        elif self.em_cooldown:
            if agora - self.tempo_ultima_adrenalina >= self.cooldown_adrenalina:
                self.adrenalina = 10  # Restaurar adrenalina após o cooldown
                self.em_cooldown = False
        else:
            if self.adrenalina < 10 and agora - self.tempo_ultima_adrenalina >= self.intervalo_adrenalina:
                self.adrenalina += 1
                self.tempo_ultima_adrenalina = agora
       
       
    def movimento(self, move_esquerda, move_direita):
       
        dx = 0
        
        if self.corre:
            self.velocidade = self.velocidade_base + 1.5
        else:
            self.velocidade = self.velocidade_base
       
        if move_direita:
            dx = +self.velocidade
            self.flip = False
            self.direcao = 1
            

        if move_esquerda:
            dx = -self.velocidade
            self.flip = True
            self.direcao = -1
            
            
        self.rect.x += dx
        self.rec.x += dx
        self.rec.centerx = self.rect.centerx - (15 if self.direcao == 1 else - 15)
       
    def pular(self):
        if not self.no_ar:  # Só pode pular se não estiver no ar
            self.aceleracao_y = -7  # Impulso inicial do pulo (ajuste este valor)
            self.no_ar = True

    def atualiza_acao(self, nova_acao):
        if nova_acao != self.acao_atual:
            self.acao_atual = nova_acao
            self.frame_index = 0
            
        if self.no_ar and self.acao_atual != 'pula':  
            self.acao_atual = 'pula'
            self.frame_index = 0

    def atualiza_animacao(self):
        agora = pygame.time.get_ticks()
        if self.poder_1 and self.poder_2 and self.poder_3 and self.poder_4 and self.poder_5 and self.poder_6 and self.poder_7:
            self.tempo_entre_frames = 50
        elif self.sofreu_dano:
            self.tempo_entre_frames = 200
        elif not self.vivo:
            self.tempo_entre_frames = 200
        else:
            self.tempo_entre_frames = 60

        if agora - self.tempo_ultima_animacao > self.tempo_entre_frames:
            self.tempo_ultima_animacao = agora  # Atualiza o tempo da última animação
            self.frame_index += 1
            if self.frame_index >= len(self.acoes[self.acao_atual]):
                self.frame_index = 0
            self.img = self.acoes[self.acao_atual][self.frame_index]

    def atualizar(self):
        self.atualiza_animacao()

    def desenha(self, screen, camera):
        self.atualiza_animacao()
        
        #pygame.draw.rect(screen, (255,0,0), self.rec)
        #screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect.move(0, 25))
        pygame.draw.rect(screen, (255, 0, 0), camera.apply_rect(self.rec))
        screen.blit(pygame.transform.flip(self.img, self.flip, False), camera.apply_rect(self.rect).move(0, 30))
        self.ataques_corpo_a_corpo.desenha(screen, camera)

    def atacar(self, tipo):
        
        x = self.rect.centerx + (40 if self.direcao == 1 else -60)
        y = self.rect.centery - 20

        self.ataques_corpo_a_corpo.atacar(x, y, self.direcao, tipo)

    def desenha_morte(self, screen):
        agora = pygame.time.get_ticks()
        
        if not hasattr(self, 'tempo_morte'):
            self.tempo_morte = agora  # Marca o tempo de morte inicial

        if agora - self.tempo_ultima_animacao > self.tempo_entre_frames:
            self.tempo_ultima_animacao = agora
            self.frame_index += 1
            if self.frame_index >= len(self.acoes['morte']):
                self.frame_index = len(self.acoes['morte']) - 1  # Fixa no último frame de morte
            self.img = self.acoes['morte'][self.frame_index]
        
        if agora - self.tempo_morte < 5000:  # Exibe o corpo por 5 segundos
            screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect.move(0, 25))
        else:
            self.img = None  # Remove o corpo após 5 segundos

class AtaquesCorpoACorpo_2:
    def __init__(self, intervalo_entre_ataques, cooldown_ataques, numero_de_ataques):
        self.ataques = []
        self.tempo_ultimo_ataque = pygame.time.get_ticks()
        self.intervalo_entre_ataques = intervalo_entre_ataques
        self.numero_de_ataques = numero_de_ataques
        self.em_cooldown = False
        self.cooldown_ataques = cooldown_ataques

    def atualizar(self):
        agora = pygame.time.get_ticks()

        if self.em_cooldown:
            if agora - self.tempo_ultimo_ataque >= self.cooldown_ataques:
                self.numero_de_ataques = 5  # Restaurar ataques após o cooldown
                self.em_cooldown = False

        for ataque in self.ataques:
            if not ataque.atualizar():
                self.ataques.remove(ataque)

    def desenha(self, screen, camera):
        for ataque in self.ataques:
            ataque.desenha(screen, camera)

    def atacar(self, x, y, direcao, tipo):
        agora = pygame.time.get_ticks()
        if not self.em_cooldown:
            if agora - self.tempo_ultimo_ataque >= self.intervalo_entre_ataques:
                if self.numero_de_ataques > 0:
                    
                    ataque = AtaqueCorpoACorpo_2(x, y, direcao, tipo)
                    self.ataques.append(ataque)
                    self.tempo_ultimo_ataque = agora
                    self.numero_de_ataques -= 1
                else:
                    self.em_cooldown = True
                    self.tempo_ultimo_ataque = agora  # Iniciar cooldown


class AtaqueCorpoACorpo_2:
    def __init__(self, x, y, direcao, tipo):
        self.tipo = tipo
        self.direcao = direcao
        self.tempo_ativo = pygame.time.get_ticks()
        self.rect = self.definir_tamanho(x, y)
        self.piscar = False
        self.piscar_intervalo = 50  # Intervalo de piscada em milissegundos
        self.ultima_piscada = pygame.time.get_ticks()
        self.piscar_contador = 0
        self.piscar_limite = self.definir_piscar_limite(tipo)


    def definir_piscar_limite(self, tipo):
        if tipo < 3:
            return 1
        elif tipo > 3:
            return 3
        else:
            return 1  # Limite padrão
        
    def definir_tamanho(self, x, y):
        if self.tipo == 1:
            largura, altura = 20, 100
        elif self.tipo == 2:
            largura, altura = 50, 10
        elif self.tipo == 3:
            largura, altura = 50, 50
        elif self.tipo == 4:
            largura, altura = 100, 30
        elif self.tipo == 5:
            largura, altura = 90, 10
        elif self.tipo == 6:
            largura, altura = 50, 20
        elif self.tipo == 7:
            largura, altura = 20, 100
        else:
            largura, altura = 30, 30  # Tamanho padrão
        
        if self.tipo == 4:
            if self.direcao == -1:
                return pygame.Rect(x, y+30, largura, altura)
            elif self.direcao == 1:
                return pygame.Rect(x-100, y+30, largura, altura)
        elif self.tipo == 1 or self.tipo == 7:
            if self.direcao == -1:
                return pygame.Rect(x, y, largura, altura)
            elif self.direcao == 1:
                return pygame.Rect(x-10, y, largura, altura)
        elif self.tipo == 2:
            return pygame.Rect(x-30, y+30, largura, altura)
        elif self.tipo == 3:
            return pygame.Rect(x, y, largura, altura)
        elif self.tipo == 5:
            return pygame.Rect(x-30, y+40, largura, altura)
        elif self.tipo == 6:
            return pygame.Rect(x-40, y+60, largura, altura)
        
        return pygame.Rect(x, y, largura, altura)

    def atualizar(self):
        agora = pygame.time.get_ticks()
        
        # Lógica de piscar
        if agora - self.ultima_piscada >= self.piscar_intervalo:
            self.piscar = not self.piscar
            self.ultima_piscada = agora
            self.piscar_contador += 1
            if self.piscar_contador >= self.piscar_limite * 2:  # Cada piscada conta como duas trocas
                self.piscar_contador = 0  # Resetar o contador para continuar piscando
                return False
        return True

    def desenha(self, screen, camera):
        if not self.piscar:
            pygame.draw.rect(screen, (0, 255, 0), camera.apply_rect(self.rect))



class Soldado_humano:
    def __init__(self, x, y, velocidade, dano, nivel, xp, dinheiro, vida):
        self.rec = pygame.Rect((x,y, 20, 80))
        self.velocidade = velocidade
        #variaveis de controle de sprites
        self.frame_index = 0
        self.direcao = 1 # esquerda
        self.flip = True # de frente
        self.acao_atual = 'parado'
        self.tempo_ultima_animacao = pygame.time.get_ticks()
        self.tempo_entre_frames = 60
        self.pulo = False
        self.no_ar = False
        self.corre = False
        self.sofreu_dano = False
        #sistema de status e recompensa
        self.dano = dano
        self.nivel = nivel
        self.xp = xp
        self.dinheiro = dinheiro
        self.vida = vida
        self.vivo = True
        self.matou_inimigo = False
        self.xp_anterior = self.xp
        self.xp_de_morte = 50

        self.aceleracao_y = 0
        self.velocidade_base = velocidade
        self.poder_1 = False
        self.poder_2 = False
        self.poder_3 = False
        self.poder_4 = False
        self.poder_5 = False
        self.poder_6 = False
        self.poder_7 = False

        self.tempo_ultima_adrenalina = pygame.time.get_ticks()
        self.intervalo_adrenalina = 500
        self.adrenalina = 10
        self.em_cooldown = False
        self.cooldown_adrenalina = 5000
        self.sprites = [pygame.transform.scale(pygame.image.load(f'soldada/({i+1}).png').convert_alpha(), (160, 140)) for i in range(246)]
       
        self.acoes = {
            'parado': self.sprites[1:4],
            'anda': self.sprites[63:70],
            'corre': self.sprites[71:76],
            'poder_1': self.sprites[23:31],
            'pula': self.sprites[86:92],
            'poder_2': self.sprites[174:182],
            'vitoria': self.sprites[76:91],
            'morte': self.sprites[120:124],
            'sofreu_dano': self.sprites[120:121],
            'defende': self.sprites[133:136]
        }

        self.img = self.acoes[self.acao_atual][0]
        self.rect = self.sprites[0].get_rect()
        self.rect.center = (x, y)
        
        self.rec.center = (self.rect.centerx -5, self.rect.top)
        self.ataques_corpo_a_corpo = AtaquesCorpoACorpo_3(intervalo_entre_ataques=500, cooldown_ataques=2000, numero_de_ataques=3)

class AtaquesCorpoACorpo_3:
    def __init__(self, intervalo_entre_ataques, cooldown_ataques, numero_de_ataques):
        self.ataques = []
        self.tempo_ultimo_ataque = pygame.time.get_ticks()
        self.intervalo_entre_ataques = intervalo_entre_ataques
        self.numero_de_ataques = numero_de_ataques
        self.em_cooldown = False
        self.cooldown_ataques = cooldown_ataques

    def atualizar(self):
        agora = pygame.time.get_ticks()

        if self.em_cooldown:
            if agora - self.tempo_ultimo_ataque >= self.cooldown_ataques:
                self.numero_de_ataques = 5  # Restaurar ataques após o cooldown
                self.em_cooldown = False

        for ataque in self.ataques:
            if not ataque.atualizar():
                self.ataques.remove(ataque)

    def desenha(self, screen):
        for ataque in self.ataques:
            ataque.desenha(screen)

    def atacar(self, x, y, direcao, tipo):
        agora = pygame.time.get_ticks()
        if not self.em_cooldown:
            if agora - self.tempo_ultimo_ataque >= self.intervalo_entre_ataques:
                if self.numero_de_ataques > 0:
                    
                    ataque = AtaqueCorpoACorpo_3(x, y, direcao, tipo)
                    self.ataques.append(ataque)
                    self.tempo_ultimo_ataque = agora
                    self.numero_de_ataques -= 1
                else:
                    self.em_cooldown = True
                    self.tempo_ultimo_ataque = agora  # Iniciar cooldown


class AtaqueCorpoACorpo_3:
    def __init__(self, x, y, direcao, tipo):
        self.tipo = tipo
        self.direcao = direcao
        self.tempo_ativo = pygame.time.get_ticks()
        self.rect = self.definir_tamanho(x, y)
        self.piscar = False
        self.piscar_intervalo = 50  # Intervalo de piscada em milissegundos
        self.ultima_piscada = pygame.time.get_ticks()
        self.piscar_contador = 0
        self.piscar_limite = self.definir_piscar_limite(tipo)


    def definir_piscar_limite(self, tipo):
        if tipo == 1:
            return 1
        elif tipo == 2:
            return 1
        elif tipo == 3:
            return 1
        elif tipo == 4:
            return 1
        else:
            return 1  # Limite padrão
        
    def definir_tamanho(self, x, y):
        if self.tipo == 1:
            largura, altura = 20, 100
        elif self.tipo == 2:
            largura, altura = 10, 70
        elif self.tipo == 3:
            largura, altura = 50, 50
        elif self.tipo == 4:
            largura, altura = 140, 30
        else:
            largura, altura = 30, 30  # Tamanho padrão
        
        if self.tipo == 4:
            if self.direcao == -1:
                return pygame.Rect(x, y+30, largura, altura)
            elif self.direcao == 1:
                return pygame.Rect(x-100, y+30, largura, altura)
        elif self.tipo == 1:
            if self.direcao == -1:
                return pygame.Rect(x, y, largura, altura)
            elif self.direcao == 1:
                return pygame.Rect(x-10, y, largura, altura)
        elif self.tipo == 2:
            return pygame.Rect(x, y, largura, altura)
        elif self.tipo == 3:
            return pygame.Rect(x, y, largura, altura)
        return pygame.Rect(x, y, largura, altura)

    def atualizar(self):
        agora = pygame.time.get_ticks()
        
        # Lógica de piscar
        if agora - self.ultima_piscada >= self.piscar_intervalo:
            self.piscar = not self.piscar
            self.ultima_piscada = agora
            self.piscar_contador += 1
            if self.piscar_contador >= self.piscar_limite * 2:  # Cada piscada conta como duas trocas
                self.piscar_contador = 0  # Resetar o contador para continuar piscando
                return False
        return True

    def desenha(self, screen):
        if not self.piscar:
            pygame.draw.rect(screen, (0, 255, 0), self.rect)


class BackgroundLayer:
    def __init__(self, image_path, speed, screen_height):
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.scale_image(self.original_image, screen_height)
        self.speed = speed
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = 0
        self.y = 0

    def scale_image(self, image, screen_height):
        # Redimensionar a imagem mantendo a proporção da largura/altura
        aspect_ratio = image.get_width() / image.get_height()
        new_height = screen_height
        new_width = int(aspect_ratio * new_height)
        return pygame.transform.scale(image, (new_width, new_height))

    def update(self, player_x):
        self.x = -(player_x * self.speed) % self.width

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        # Se a imagem não cobre toda a tela, desenhe uma segunda imagem
        if self.x > 0:
            screen.blit(self.image, (self.x - self.width, self.y))
        elif self.x < screen.get_width() - self.width:
            screen.blit(self.image, (self.x + self.width, self.y))

class ParallaxBackground:
    def __init__(self, screen_height):
        self.layers = []
        self.screen_height = screen_height

    def add_layer(self, image_path, speed):
        layer = BackgroundLayer(image_path, speed, self.screen_height)
        self.layers.append(layer)

    def update(self, player_x):
        for layer in self.layers:
            layer.update(player_x)

    def draw(self, screen):
        for layer in self.layers:
            layer.draw(screen)


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        global WIDTH, HEIGHT
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # Limitar a câmera dentro dos limites do mapa
        x = min(0, x)  # Não passar do lado esquerdo
        y = min(0, y)  # Não passar do topo
        x = max(-(self.width - WIDTH), x)  # Não passar do lado direito
        y = max(-(self.height - HEIGHT), y)  # Não passar do fundo

        self.camera = pygame.Rect(x, y, self.width, self.height)

    def draw(self, surface, group):
        for sprite in group:
            surface.blit(sprite.image, self.apply(sprite))