#  Lógica do jogo

import pygame
import random
import math
from pygame import mixer
from constants import *
from game_design import criar_inimigo, criar_explosao

class GameLogic:
    def __init__(self):
        # Jogador
        self.jogador_x = JOGADOR_X_INICIAL
        self.jogador_y = JOGADOR_Y_INICIAL
        self.jogador_x_mudanca = 0
        
        # Inimigos
        self.inimigo_img = []
        self.inimigo_x = []
        self.inimigo_y = []
        self.inimigo_x_mudanca = []
        self.inimigo_y_mudanca = []
        self.inimigo_vida = []
        self.num_inimigos = NUM_INIMIGOS_BASE
        
        # Boss
        self.boss_x = 336
        self.boss_y = 100
        self.boss_x_mudanca = BOSS_VELOCIDADE
        self.boss_vida = BOSS_VIDA_BASE
        self.boss_ativo = False
        self.boss_tiros_cooldown = 0
        
        # Tiros do jogador
        self.tiro_x = 0
        self.tiro_y = JOGADOR_Y_INICIAL
        self.tiro_estado = "pronto"
        
        # Tiros dos inimigos
        self.tiros_inimigos_x = []
        self.tiros_inimigos_y = []
        self.tiros_inimigos_estado = []
        self.tiros_inimigos_cooldown = []
        
        # Tiros do boss
        self.tiros_boss_x = []
        self.tiros_boss_y = []
        self.tiros_boss_estado = []
        
        # Estado do jogo
        self.pontuacao = 0
        self.nivel = 1
        self.game_over = False
        
        # Partículas
        self.particulas = []
        
        # Inicializar tiros
        self._inicializar_tiros()
        
        # Sons
        self._carregar_sons()
    
    def _inicializar_tiros(self):
        """Inicializar listas de tiros"""
        # Tiros dos inimigos
        for i in range(MAX_TIROS_INIMIGOS):
            self.tiros_inimigos_x.append(0)
            self.tiros_inimigos_y.append(0)
            self.tiros_inimigos_estado.append("pronto")
            self.tiros_inimigos_cooldown.append(random.randint(50, 200))
        
        # Tiros do boss
        for i in range(MAX_TIROS_BOSS):
            self.tiros_boss_x.append(0)
            self.tiros_boss_y.append(0)
            self.tiros_boss_estado.append("pronto")
    
    def _carregar_sons(self):
        """Carregar arquivos de som"""
        try:
            mixer.music.load('background.wav')
            mixer.music.play(-1)
            self.som_tiro = mixer.Sound('laser.wav')
            self.som_explosao = mixer.Sound('explosion.wav')
        except:
            print("Arquivos de som não encontrados. O jogo funcionará sem áudio.")
            self.som_tiro = None
            self.som_explosao = None
    
    def inicializar_inimigos(self, nivel):
        """Inicializar inimigos para um nível"""
        # Verificar se é hora de ativar o boss
        if nivel > 0 and nivel % 3 == 0:
            self.boss_ativo = True
            self.boss_vida = BOSS_VIDA_BASE + (nivel // 3) * 5
            return
        
        # Se não for nível de boss, inicializa inimigos normais
        self.boss_ativo = False
        
        # Limpar listas anteriores
        self.inimigo_img.clear()
        self.inimigo_x.clear()
        self.inimigo_y.clear()
        self.inimigo_x_mudanca.clear()
        self.inimigo_y_mudanca.clear()
        self.inimigo_vida.clear()
        
        # Calcular número de inimigos
        self.num_inimigos = NUM_INIMIGOS_BASE + (nivel - 1) * 2
        if self.num_inimigos > MAX_INIMIGOS:
            self.num_inimigos = MAX_INIMIGOS
        
        # Velocidade aumenta com o nível
        velocidade_base = 2 + (nivel - 1) * 0.5
        if velocidade_base > 5:
            velocidade_base = 5
        
        # Criar inimigos
        for i in range(self.num_inimigos):
            tipo_inimigo = random.randint(1, 3)
            img = criar_inimigo(tipo_inimigo)
            self.inimigo_img.append(img)
            
            # Posicionar inimigos
            x = random.randint(0, 736)
            y = random.randint(50, 150)
            self.inimigo_x.append(x)
            self.inimigo_y.append(y)
            
            # Velocidade
            direcao = 1 if random.random() > 0.5 else -1
            self.inimigo_x_mudanca.append(velocidade_base * direcao)
            self.inimigo_y_mudanca.append(40)
            
            # Vida do inimigo
            self.inimigo_vida.append(1)
        
        # Reinicializar tiros dos inimigos
        self.tiros_inimigos_x.clear()
        self.tiros_inimigos_y.clear()
        self.tiros_inimigos_estado.clear()
        self.tiros_inimigos_cooldown.clear()
        
        for i in range(MAX_TIROS_INIMIGOS):
            self.tiros_inimigos_x.append(0)
            self.tiros_inimigos_y.append(0)
            self.tiros_inimigos_estado.append("pronto")
            self.tiros_inimigos_cooldown.append(random.randint(50, 200))
    
    def atualizar_jogador(self):
        """Atualizar posição do jogador"""
        self.jogador_x += self.jogador_x_mudanca
        
        # Manter jogador dentro dos limites
        if self.jogador_x <= 0:
            self.jogador_x = 0
        elif self.jogador_x >= 736:
            self.jogador_x = 736
    
    def disparar_tiro_jogador(self):
        """Disparar tiro do jogador"""
        if self.tiro_estado == "pronto":
            self.tiro_x = self.jogador_x
            self.tiro_estado = "disparado"
            if self.som_tiro:
                self.som_tiro.play()
    
    def disparar_tiro_inimigo(self, i, x, y):
        """Disparar tiro do inimigo"""
        if self.tiros_inimigos_estado[i] == "pronto":
            self.tiros_inimigos_estado[i] = "disparado"
            self.tiros_inimigos_x[i] = x + 28
            self.tiros_inimigos_y[i] = y + 40
    
    def disparar_tiro_boss(self, i, x, y):
        """Disparar tiro do boss"""
        if self.tiros_boss_estado[i] == "pronto":
            self.tiros_boss_estado[i] = "disparado"
            self.tiros_boss_x[i] = x + 58
            self.tiros_boss_y[i] = y + 80
    
    def colisao(self, obj1_x, obj1_y, obj2_x, obj2_y, distancia_limite=40):
        """Verificar colisão entre dois objetos"""
        distancia = math.sqrt((obj1_x + 32 - obj2_x - 4) ** 2 + (obj1_y + 32 - obj2_y - 8) ** 2)
        return distancia < distancia_limite
    
    def colisao_boss(self, boss_x, boss_y, tiro_x, tiro_y):
        """Verificar colisão com boss"""
        distancia = math.sqrt((boss_x + 64 - tiro_x - 4) ** 2 + (boss_y + 64 - tiro_y - 8) ** 2)
        return distancia < 60
    
    def colisao_jogador(self, jogador_x, jogador_y, tiro_x, tiro_y):
        """Verificar colisão com jogador"""
        distancia = math.sqrt((jogador_x + 32 - tiro_x - 4) ** 2 + (jogador_y + 32 - tiro_y - 8) ** 2)
        return distancia < 30
    
    def atualizar_tiro_jogador(self):
        """Atualizar movimento do tiro do jogador"""
        if self.tiro_y <= 0:
            self.tiro_y = JOGADOR_Y_INICIAL
            self.tiro_estado = "pronto"
        
        if self.tiro_estado == "disparado":
            self.tiro_y -= TIRO_VELOCIDADE
    
    def atualizar_boss(self):
        """Atualizar lógica do boss"""
        if not self.boss_ativo:
            return False
        
        # Movimento do boss
        self.boss_x += self.boss_x_mudanca
        if self.boss_x <= 0:
            self.boss_x_mudanca = abs(self.boss_x_mudanca)
        elif self.boss_x >= LARGURA - 128:
            self.boss_x_mudanca = -abs(self.boss_x_mudanca)
        
        # Tiros do boss
        self.boss_tiros_cooldown += 1
        if self.boss_tiros_cooldown >= BOSS_COOLDOWN_TIROS:
            self.boss_tiros_cooldown = 0
            for i in range(MAX_TIROS_BOSS):
                if self.tiros_boss_estado[i] == "pronto":
                    self.disparar_tiro_boss(i, self.boss_x, self.boss_y)
                    break
        
        return True
    
    def atualizar_inimigos(self):
        """Atualizar movimento dos inimigos"""
        inimigos_restantes = 0
        
        for i in range(self.num_inimigos):
            if self.inimigo_y[i] < 1000:  # Se estiver na tela
                inimigos_restantes += 1
                
                # Game Over se inimigo chegou muito baixo
                if self.inimigo_y[i] > 440 and not self.game_over:
                    for j in range(self.num_inimigos):
                        self.inimigo_y[j] = 2000
                    self.game_over = True
                    return inimigos_restantes
                
                # Movimento dos inimigos
                self.inimigo_x[i] += self.inimigo_x_mudanca[i]
                if self.inimigo_x[i] <= 0:
                    self.inimigo_x_mudanca[i] = abs(self.inimigo_x_mudanca[i])
                    self.inimigo_y[i] += self.inimigo_y_mudanca[i]
                elif self.inimigo_x[i] >= 736:
                    self.inimigo_x_mudanca[i] = -abs(self.inimigo_x_mudanca[i])
                    self.inimigo_y[i] += self.inimigo_y_mudanca[i]
                
                # Tiros dos inimigos
                if random.random() < 0.005 * self.nivel:
                    for j in range(MAX_TIROS_INIMIGOS):
                        if self.tiros_inimigos_estado[j] == "pronto":
                            self.disparar_tiro_inimigo(j, self.inimigo_x[i], self.inimigo_y[i])
                            break
        
        return inimigos_restantes
    
    def verificar_colisoes_inimigos(self):
        """Verificar colisões do tiro do jogador com inimigos"""
        if self.tiro_estado != "disparado":
            return
        
        for i in range(self.num_inimigos):
            if self.inimigo_y[i] < 1000:  # Se estiver na tela
                if self.colisao(self.inimigo_x[i], self.inimigo_y[i], self.tiro_x, self.tiro_y):
                    if self.som_explosao:
                        self.som_explosao.play()
                    
                    # Criar explosão
                    criar_explosao(self.inimigo_x[i] + 32, self.inimigo_y[i] + 32, VERMELHO_NEON, self.particulas)
                    
                    self.tiro_y = JOGADOR_Y_INICIAL
                    self.tiro_estado = "pronto"
                    self.pontuacao += 1
                    self.inimigo_y[i] = 2000  # Remove inimigo
                    break
    
    def verificar_colisoes_boss(self):
        """Verificar colisões do tiro do jogador com o boss"""
        if self.tiro_estado != "disparado" or not self.boss_ativo:
            return False
        
        if self.colisao_boss(self.boss_x, self.boss_y, self.tiro_x, self.tiro_y):
            if self.som_explosao:
                self.som_explosao.play()
            
            # Criar explosão menor no boss
            criar_explosao(self.tiro_x, self.tiro_y, LARANJA_NEON, self.particulas)
            
            self.tiro_y = JOGADOR_Y_INICIAL
            self.tiro_estado = "pronto"
            self.boss_vida -= 1
            self.pontuacao += 2
            
            # Verificar se o boss foi derrotado
            if self.boss_vida <= 0:
                # Explosão maior quando o boss é derrotado
                for j in range(3):
                    criar_explosao(self.boss_x + 64 + random.randint(-30, 30), 
                                 self.boss_y + 64 + random.randint(-30, 30), 
                                 random.choice([ROXO_NEON, LARANJA_NEON, AMARELO]), self.particulas)
                self.pontuacao += 50
                return True  # Boss derrotado
        
        return False
    
    def atualizar_tiros_inimigos(self):
        """Atualizar movimento dos tiros dos inimigos"""
        for i in range(MAX_TIROS_INIMIGOS):
            if self.tiros_inimigos_estado[i] == "disparado":
                self.tiros_inimigos_y[i] += TIROS_INIMIGOS_VELOCIDADE
                
                # Verificar se saiu da tela
                if self.tiros_inimigos_y[i] > ALTURA:
                    self.tiros_inimigos_estado[i] = "pronto"
                
                # Verificar colisão com jogador
                if self.colisao_jogador(self.jogador_x, self.jogador_y, self.tiros_inimigos_x[i], self.tiros_inimigos_y[i]):
                    if self.som_explosao:
                        self.som_explosao.play()
                    self.tiros_inimigos_estado[i] = "pronto"
                    self.game_over = True
    
    def atualizar_tiros_boss(self):
        """Atualizar movimento dos tiros do boss"""
        for i in range(MAX_TIROS_BOSS):
            if self.tiros_boss_estado[i] == "disparado":
                self.tiros_boss_y[i] += TIROS_BOSS_VELOCIDADE
                
                # Verificar se saiu da tela
                if self.tiros_boss_y[i] > ALTURA:
                    self.tiros_boss_estado[i] = "pronto"
                
                # Verificar colisão com jogador
                if self.colisao_jogador(self.jogador_x, self.jogador_y, self.tiros_boss_x[i], self.tiros_boss_y[i]):
                    if self.som_explosao:
                        self.som_explosao.play()
                    self.tiros_boss_estado[i] = "pronto"
                    self.game_over = True
    
    def reiniciar_jogo(self):
        """Reiniciar o jogo"""
        self.game_over = False
        self.pontuacao = 0
        self.nivel = 1
        self.jogador_x = JOGADOR_X_INICIAL
        self.particulas.clear()
        self.inicializar_inimigos(self.nivel)
