import gym
from gym import spaces
import numpy as np
import pygame
from classes import Atirador, Soldada

class CustomEnv(gym.Env):
    def __init__(self):
        super(CustomEnv, self).__init__()
        self.screen = pygame.display.set_mode((600, 300))  # Reduzir a resolução da tela para treinamento
        self.atirador = Atirador(250, 150, 4, dano=10, nivel=1, xp=0, dinheiro=0, vida=100)
        self.soldada = Soldada(50, 150, 3.5, dano=10, nivel=1, xp=0, dinheiro=0, vida=100)
        self.action_space = spaces.Discrete(6)  # Exemplo de 6 ações: [parado, esquerda, direita, pular, poder_1, poder_2]
        self.observation_space = spaces.Box(low=0, high=255, shape=(300, 600, 3), dtype=np.uint8)
    
    def reset(self):
        self.atirador = Atirador(250, 150, 4, dano=10, nivel=1, xp=0, dinheiro=0, vida=100)
        self.soldada = Soldada(50, 150, 3.5, dano=10, nivel=1, xp=0, dinheiro=0, vida=100)
        return self._get_obs()
    
    def step(self, action):
        if action == 0:
            self.soldada.movimento(False, False)  # Parado
        elif action == 1:
            self.soldada.movimento(True, False)  # Esquerda
        elif action == 2:
            self.soldada.movimento(False, True)  # Direita
        elif action == 3:
            self.soldada.pular()  # Pular
        elif action == 4:
            self.soldada.poder_1 = True  # Poder 1
        elif action == 5:
            self.soldada.poder_2 = True  # Poder 2
        
        self._update_game_state()
        
        obs = self._get_obs()
        reward = self._calculate_reward()
        done = self._check_done()
        info = {}
        
        self.render()  # Renderizar a tela para visualização
        
        return obs, reward, done, info
    
    def render(self, mode='human'):
        self.screen.fill((0, 0, 0))
        self.atirador.desenha(self.screen)
        self.soldada.desenha(self.screen)
        pygame.display.flip()
    
    def _get_obs(self):
        obs = pygame.surfarray.array3d(self.screen)
        obs = np.transpose(obs, (1, 0, 2))
        return obs
    
    def _update_game_state(self):
        self.atirador.movimento(False, False)  # Exemplo: Atirador parado
        self.soldada.movimento(False, False)  # Exemplo: Soldada parada
        self._apply_gravity(self.atirador)
        self._apply_gravity(self.soldada)
        self.soldada.ataques_corpo_a_corpo.atualizar()
        self.verificar_colisoes()
    
    def _apply_gravity(self, personagem):
        personagem.aceleracao_y += 1  # Aceleracao da gravidade (exemplo)
        personagem.rect.y += personagem.aceleracao_y
        if personagem.rect.bottom > 300:  # Supomos que 300 é o chão
            personagem.rect.bottom = 300
            personagem.aceleracao_y = 0
            personagem.no_ar = False
    
    def verificar_colisoes(self):
        for tiro in self.atirador.tiros_1.tiros + self.atirador.tiros_2.tiros:
            if tiro.rect.colliderect(self.soldada.rec):
                self.soldada.vida -= self.atirador.dano
                if self.soldada.vida <= 0:
                    self.atirador.matou_inimigo = True
                    self.soldada.vida = 100
        for ataque in self.soldada.ataques_corpo_a_corpo.ataques:
            if ataque.rect.colliderect(self.atirador.rec):
                self.atirador.vida -= self.soldada.dano
                if self.atirador.vida <= 0:
                    self.soldada.matou_inimigo = True
                    self.atirador.vida = 100
    
    def _calculate_reward(self):
        reward = 0
        if self.soldada.matou_inimigo:
            reward += 10
            self.soldada_xp += 10
            self.soldada.matou_inimigo = False
            if self.soldada_xp >= 100:
                self.soldada_xp -= 100
                self.soldada.nivel += 1
                self._level_up()
        return reward
    
    def _level_up(self):
        self.soldada.dano += 10  # Exemplo: aumentar o dano ao subir de nível
    
    def _check_done(self):
        return self.atirador.vida <= 0 or self.soldada.vida <= 0

env = CustomEnv()
