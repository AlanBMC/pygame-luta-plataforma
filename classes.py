import pygame
from globais import *

class Tiro:
    def __init__(self, x, y, direcao):
        self.rect = pygame.Rect(x, y, 10, 5)  # Define o tamanho do tiro
        self.velocidade = 10  # Velocidade do tiro
        self.direcao = direcao

    def atualizar(self):
        self.rect.x += self.velocidade * self.direcao

    def desenha(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)


class Tiros:
    def __init__(self, intervalo_entre_tiros, cooldown_tiros, numero_de_disparos):
        self.tiros = []
        self.tempo_ultimo_tiro = pygame.time.get_ticks()
        self.intervalo_entre_tiros = intervalo_entre_tiros
        self.numero_de_disparos = numero_de_disparos
        self.em_cooldown = False
        self.cooldown_tiros = cooldown_tiros

    def atualizar(self):
        agora = pygame.time.get_ticks()

        if self.em_cooldown:
            if agora - self.tempo_ultimo_tiro >= self.cooldown_tiros:
                self.numero_de_disparos = 10  # Restaurar disparos após o cooldown
                self.em_cooldown = False

        for tiro in self.tiros:
            tiro.atualizar()
            if tiro.rect.x > 1200 or tiro.rect.x < 0:
                self.tiros.remove(tiro)

    def desenha(self, screen):
        for tiro in self.tiros:
            tiro.desenha(screen)

    def atirar(self, x, y, direcao):
        agora = pygame.time.get_ticks()
        if not self.em_cooldown:
            if agora - self.tempo_ultimo_tiro >= self.intervalo_entre_tiros:
                if self.numero_de_disparos > 0:
                    tiro = Tiro(x, y, direcao)
                    self.tiros.append(tiro)
                    self.tempo_ultimo_tiro = agora
                    self.numero_de_disparos -= 1
                else:
                    self.em_cooldown = True
                    self.tempo_ultimo_tiro = agora  # Iniciar cooldown

class Atirador:
    def __init__(self, x, y, velocidade):
        self.rec = pygame.Rect((x,y, 20, 80))
        self.flip = True # de frente
        self.velocidade = velocidade
        self.frame_index = 0
        self.aceleracao_y = 0
        self.direcao = 1 # esquerda
        self.acao_atual = 'parado'
        self.no_ar = False
        # variaveis de animacao
        self.tempo_ultima_animacao = pygame.time.get_ticks()
        self.tempo_entre_frames = 100

        # variaveis de recarga
        self.corre = False
        self.rola = False
        self.atira_1 = False
        self.atira_2 = False
        self.tempo_ultima_adrenalina = pygame.time.get_ticks()
        self.intervalo_adrenalina = 500
        self.adrenalina = 10
        self.em_cooldown = False
        self.cooldown_adrenalina = 5000
        self.velocidade_base = velocidade
        self.velocidade_ataque = 5

        self.sprites = [pygame.transform.scale(pygame.image.load(f'atirador/({i+1}).png').convert_alpha(), (120, 90)) for i in range(202)]
        self.acoes = {
            'parado': self.sprites[1:18],
            'anda': self.sprites[56:63],
            'pula': self.sprites[64:70],
            'atira_1': self.sprites[19:55],
            'atira_2': self.sprites[71:103],
            'corre': self.sprites[104:111],
            'rola': self.sprites[112:121]
        }
        self.img = self.acoes[self.acao_atual][0]
        self.rect = self.sprites[0].get_rect()
        self.rect.center = (x, y+20)
        self.rec.center = (x+10,y-50)
        self.tiros_1 = Tiros(intervalo_entre_tiros=400, cooldown_tiros=5000, numero_de_disparos=10)
        self.tiros_2 = Tiros(intervalo_entre_tiros=300, cooldown_tiros=5000, numero_de_disparos=20)


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
                self.adrenalina = 10  # Restaurar adrenalina após o cooldown
                self.em_cooldown = False
        else:
            if self.adrenalina < 10 and agora - self.tempo_ultima_adrenalina >= self.intervalo_adrenalina:
                self.adrenalina += 1
                self.tempo_ultima_adrenalina = agora


    def atualiza_animacao(self):
        agora = pygame.time.get_ticks()
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

    def movimento(self, esquerda, direita):
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
       
    def desenha(self, screen):
        self.atualiza_animacao()
        pygame.draw.rect(screen, (255,0,0), self.rec)
        screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect.move(0, 10))
        self.tiros_1.desenha(screen)
        self.tiros_2.desenha(screen)


class Soldada:
    def __init__(self, x, y, velocidade):
        self.rec = pygame.Rect((x,y, 20, 80))
        self.flip = True # de frente
        self.direcao = 1 # esquerda
        self.velocidade = velocidade
        self.frame_index = 0
        self.aceleracao_y = 0
        self.acao_atual = 'parado'
        self.tempo_ultima_animacao = pygame.time.get_ticks()
        self.tempo_entre_frames = 60
        self.pulo = False
        self.no_ar = False
        self.corre = False
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
            'morte': self.sprites[140:144]
        }
        self.img = self.acoes[self.acao_atual][0]
        self.rect = self.sprites[0].get_rect()
        self.rect.center = (x, y)
        
        self.rec.center = (self.rect.centerx -5, self.rect.top)
        self.ataques_corpo_a_corpo = AtaquesCorpoACorpo(intervalo_entre_ataques=500, cooldown_ataques=2000, numero_de_ataques=3)

        
      
     
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
            self.tempo_entre_frames = 15
        elif self.poder_2:
            self.tempo_entre_frames = 15
        elif self.poder_3:
            self.tempo_entre_frames = 15
        elif self.poder_4:
            self.tempo_entre_frames = 15
        else:
            self.tempo_entre_frames = 60
        if agora - self.tempo_ultima_animacao > self.tempo_entre_frames:
            self.tempo_ultima_animacao = agora  # Atualiza o tempo da última animação
            self.frame_index += 1
            if self.frame_index >= len(self.acoes[self.acao_atual]):
                self.frame_index = 0
            self.img = self.acoes[self.acao_atual][self.frame_index]
    
    
    def desenha(self, screen):
        self.atualiza_animacao()
        
        pygame.draw.rect(screen, (255,0,0), self.rec)
        screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect.move(0, 25))
        self.ataques_corpo_a_corpo.desenha(screen)

    def atacar(self, tipo):
       
        x = self.rect.centerx + (40 if self.direcao == 1 else -60)
        y = self.rect.centery - 20
        self.ataques_corpo_a_corpo.atacar(x, y, self.direcao, tipo)


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

    def desenha(self, screen):
        for ataque in self.ataques:
            ataque.desenha(screen)

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
        self.piscar_intervalo = 100  # Intervalo de piscada em milissegundos
        self.ultima_piscada = pygame.time.get_ticks()
        self.piscar_contador = 0
        self.piscar_limite = self.definir_piscar_limite(tipo)


    def definir_piscar_limite(self, tipo):
        if tipo == 1:
            return 3
        elif tipo == 2:
            return 3
        elif tipo == 3:
            return 3
        elif tipo == 4:
            return 3
        else:
            return 3  # Limite padrão
        
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
                rect = pygame.Rect(x, y+30, largura, altura)
            elif self.direcao == 1:
                rect = pygame.Rect(x-100, y+30, largura, altura)
        elif self.tipo == 1:
            if self.direcao == -1:
                rect = pygame.Rect(x, y, largura, altura)
            elif self.direcao == 1:
                rect = pygame.Rect(x-10, y, largura, altura)
        elif self.tipo == 2:
            rect = pygame.Rect(x, y, largura, altura)
        elif self.tipo == 3:
            rect = pygame.Rect(x, y, largura, altura)
        return rect

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

