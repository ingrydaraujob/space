# game_design.py - Design visual e efeitos do jogo

import pygame
import random
import math
from constants import *

class Particula:
    def __init__(self, x, y, cor, velocidade_x, velocidade_y, vida):
        self.x = x
        self.y = y
        self.cor = cor
        self.velocidade_x = velocidade_x
        self.velocidade_y = velocidade_y
        self.vida = vida
        self.vida_max = vida
    
    def atualizar(self):
        self.x += self.velocidade_x
        self.y += self.velocidade_y
        self.vida -= 1
        
        # Reduzir velocidade gradualmente
        self.velocidade_x *= 0.98
        self.velocidade_y *= 0.98
    
    def desenhar(self, tela):
        if self.vida > 0:
            alpha = int(255 * (self.vida / self.vida_max))
            cor_com_alpha = (*self.cor, alpha)
            particula_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(particula_surface, cor_com_alpha, (2, 2), 2)
            tela.blit(particula_surface, (self.x, self.y))

def criar_fundo_espacial():
    """Criar fundo espacial com estrelas e nebulosas"""
    fundo = pygame.Surface((LARGURA, ALTURA))
    
    # Gradiente espacial (do azul escuro para preto)
    for y in range(ALTURA):
        intensidade = int(25 * (1 - y / ALTURA))
        cor = (intensidade // 3, intensidade // 2, intensidade)
        pygame.draw.line(fundo, cor, (0, y), (LARGURA, y))
    
    # Estrelas de diferentes tamanhos e brilhos
    for i in range(150):
        x = random.randint(0, LARGURA)
        y = random.randint(0, ALTURA)
        tamanho = random.randint(1, 4)
        brilho = random.randint(150, 255)
        
        if tamanho == 1:
            pygame.draw.circle(fundo, (brilho, brilho, brilho), (x, y), 1)
        elif tamanho == 2:
            pygame.draw.circle(fundo, (brilho, brilho, brilho), (x, y), 1)
            pygame.draw.circle(fundo, (brilho//2, brilho//2, brilho//2), (x, y), 2)
        elif tamanho == 3:
            pygame.draw.circle(fundo, (brilho, brilho, brilho), (x, y), 2)
            pygame.draw.circle(fundo, (brilho//3, brilho//3, brilho//3), (x, y), 4)
        else:
            pygame.draw.circle(fundo, BRANCO, (x, y), 2)
            pygame.draw.line(fundo, BRANCO, (x-4, y), (x+4, y), 1)
            pygame.draw.line(fundo, BRANCO, (x, y-4), (x, y+4), 1)
    
    # Nebulosas distantes
    nebulosa_surface = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    for i in range(8):
        x = random.randint(50, LARGURA-50)
        y = random.randint(50, ALTURA-50)
        raio = random.randint(30, 80)
        cor_nebulosa = random.choice([
            (50, 0, 100, 30), (0, 50, 100, 30),
            (100, 0, 50, 30), (0, 100, 50, 30)
        ])
        pygame.draw.circle(nebulosa_surface, cor_nebulosa, (x, y), raio)
    
    fundo.blit(nebulosa_surface, (0, 0))
    return fundo

def criar_nave_jogador():
    """Criar sprite da nave do jogador"""
    nave = pygame.Surface((64, 64), pygame.SRCALPHA)
    
    # Corpo principal da nave
    pontos_corpo = [(32, 5), (8, 50), (20, 45), (32, 35), (44, 45), (56, 50)]
    pygame.draw.polygon(nave, AZUL_NEON, pontos_corpo)
    pygame.draw.polygon(nave, BRANCO_AZULADO, pontos_corpo, 2)
    
    # Cockpit
    pygame.draw.circle(nave, AZUL_ESCURO, (32, 25), 8)
    pygame.draw.circle(nave, AZUL_NEON, (32, 25), 8, 2)
    pygame.draw.circle(nave, BRANCO, (32, 23), 3)
    
    # Motores laterais
    pygame.draw.rect(nave, CINZA, (15, 40, 8, 15))
    pygame.draw.rect(nave, CINZA, (41, 40, 8, 15))
    pygame.draw.rect(nave, AZUL_NEON, (15, 40, 8, 15), 2)
    pygame.draw.rect(nave, AZUL_NEON, (41, 40, 8, 15), 2)
    
    # Propulsores
    pygame.draw.rect(nave, AZUL_NEON, (17, 55, 4, 8))
    pygame.draw.rect(nave, AZUL_NEON, (43, 55, 4, 8))
    pygame.draw.rect(nave, BRANCO, (18, 56, 2, 6))
    pygame.draw.rect(nave, BRANCO, (44, 56, 2, 6))
    
    # Detalhes tecnológicos
    pygame.draw.line(nave, VERDE_NEON, (32, 8), (32, 32), 2)
    pygame.draw.circle(nave, VERDE_NEON, (20, 20), 2)
    pygame.draw.circle(nave, VERDE_NEON, (44, 20), 2)
    pygame.draw.circle(nave, VERMELHO_NEON, (32, 15), 2)
    
    return nave

def criar_boss():
    """Criar sprite do boss"""
    boss = pygame.Surface((128, 128), pygame.SRCALPHA)
    
    # Corpo principal hexagonal
    pontos_hex = []
    for i in range(6):
        angulo = i * 60 * math.pi / 180
        x = 64 + 50 * math.cos(angulo)
        y = 64 + 50 * math.sin(angulo)
        pontos_hex.append((x, y))
    
    pygame.draw.polygon(boss, ROXO_NEON, pontos_hex)
    pygame.draw.polygon(boss, ROSA_NEON, pontos_hex, 3)
    
    # Núcleo central
    pygame.draw.circle(boss, VERMELHO_NEON, (64, 64), 25)
    pygame.draw.circle(boss, LARANJA_NEON, (64, 64), 20)
    pygame.draw.circle(boss, AMARELO, (64, 64), 15)
    pygame.draw.circle(boss, BRANCO, (64, 64), 10)
    
    # Canhões laterais
    for i in range(4):
        angulo = i * 90 * math.pi / 180
        x = 64 + 35 * math.cos(angulo)
        y = 64 + 35 * math.sin(angulo)
        pygame.draw.circle(boss, CINZA, (int(x), int(y)), 8)
        pygame.draw.circle(boss, VERMELHO_NEON, (int(x), int(y)), 8, 2)
        pygame.draw.circle(boss, LARANJA_NEON, (int(x), int(y)), 5)
    
    # Detalhes tecnológicos
    for i in range(8):
        angulo = i * 45 * math.pi / 180
        x1 = 64 + 25 * math.cos(angulo)
        y1 = 64 + 25 * math.sin(angulo)
        x2 = 64 + 45 * math.cos(angulo)
        y2 = 64 + 45 * math.sin(angulo)
        pygame.draw.line(boss, AZUL_NEON, (x1, y1), (x2, y2), 2)
    
    # Escudo energético
    pygame.draw.circle(boss, AZUL_NEON, (64, 64), 60, 2)
    
    return boss

def criar_inimigo(tipo):
    """Criar sprite de inimigo baseado no tipo"""
    img = pygame.Surface((64, 64), pygame.SRCALPHA)
    
    if tipo == 1:
        # Inimigo triangular
        pontos = [(32, 10), (10, 50), (54, 50)]
        cor_principal = (random.randint(150, 255), random.randint(0, 100), random.randint(0, 100))
        pygame.draw.polygon(img, cor_principal, pontos)
        pygame.draw.polygon(img, VERMELHO_NEON, pontos, 2)
        pygame.draw.circle(img, LARANJA_NEON, (32, 35), 5)
        
    elif tipo == 2:
        # Inimigo hexagonal
        pontos_hex = []
        for j in range(6):
            angulo = j * 60 * math.pi / 180
            x = 32 + 20 * math.cos(angulo)
            y = 32 + 20 * math.sin(angulo)
            pontos_hex.append((x, y))
        cor_principal = (random.randint(100, 200), random.randint(0, 150), random.randint(100, 255))
        pygame.draw.polygon(img, cor_principal, pontos_hex)
        pygame.draw.polygon(img, AZUL_NEON, pontos_hex, 2)
        pygame.draw.circle(img, ROSA_NEON, (32, 32), 8)
        
    else:
        # Inimigo circular
        cor_principal = (random.randint(100, 255), random.randint(50, 150), random.randint(50, 200))
        pygame.draw.circle(img, cor_principal, (32, 32), 20)
        pygame.draw.circle(img, ROXO_NEON, (32, 32), 20, 2)
        pygame.draw.circle(img, LARANJA_NEON, (32, 32), 10)
        pygame.draw.circle(img, BRANCO, (32, 32), 5)
        
        # Detalhes laterais
        pygame.draw.circle(img, VERDE_NEON, (15, 32), 3)
        pygame.draw.circle(img, VERDE_NEON, (49, 32), 3)
    
    return img

def criar_tiro_jogador():
    """Criar sprite do tiro do jogador"""
    tiro = pygame.Surface((8, 16), pygame.SRCALPHA)
    pygame.draw.rect(tiro, VERDE_NEON, (3, 0, 2, 16))
    pygame.draw.rect(tiro, BRANCO, (3.5, 0, 1, 16))
    pygame.draw.rect(tiro, VERDE, (2, 0, 4, 16))
    pygame.draw.rect(tiro, (100, 255, 100), (1, 0, 6, 16))
    pygame.draw.rect(tiro, (150, 255, 150), (0, 0, 8, 16))
    return tiro

def criar_tiro_inimigo():
    """Criar sprite do tiro do inimigo"""
    tiro = pygame.Surface((8, 16), pygame.SRCALPHA)
    pygame.draw.rect(tiro, VERMELHO_NEON, (2, 0, 4, 16))
    pygame.draw.rect(tiro, VERMELHO, (1, 0, 6, 16))
    pygame.draw.rect(tiro, (255, 100, 100), (0, 0, 8, 16))
    return tiro

def criar_tiro_boss():
    """Criar sprite do tiro do boss"""
    tiro = pygame.Surface((12, 24), pygame.SRCALPHA)
    pygame.draw.rect(tiro, LARANJA_NEON, (3, 0, 6, 24))
    pygame.draw.rect(tiro, AMARELO, (4, 0, 4, 24))
    pygame.draw.rect(tiro, BRANCO, (5, 0, 2, 24))
    pygame.draw.rect(tiro, LARANJA, (2, 0, 8, 24))
    pygame.draw.rect(tiro, (255, 200, 100), (1, 0, 10, 24))
    pygame.draw.rect(tiro, (255, 255, 200), (0, 0, 12, 24))
    return tiro

def criar_explosao(x, y, cor_base, particulas_list):
    """Criar partículas de explosão"""
    for i in range(PARTICULAS_POR_EXPLOSAO):
        velocidade_x = random.uniform(-5, 5)
        velocidade_y = random.uniform(-5, 5)
        vida = random.randint(VIDA_PARTICULA_MIN, VIDA_PARTICULA_MAX)
        cor = random.choice([cor_base, AMARELO, LARANJA_NEON, BRANCO])
        particula = Particula(x, y, cor, velocidade_x, velocidade_y, vida)
        particulas_list.append(particula)

def atualizar_particulas(particulas_list, tela):
    """Atualizar e desenhar todas as partículas"""
    particulas_ativas = []
    
    for particula in particulas_list:
        particula.atualizar()
        if particula.vida > 0:
            particula.desenhar(tela)
            particulas_ativas.append(particula)
    
    particulas_list[:] = particulas_ativas

def inicializar_fontes():
    """Inicializar fontes do jogo"""
    try:
        fonte = pygame.font.Font(None, 32)
        fonte_go = pygame.font.Font(None, 64)
        fonte_media = pygame.font.Font(None, 36)
        fonte_pequena = pygame.font.Font(None, 24)
        fonte_titulo = pygame.font.Font(None, 48)
    except:
        fonte = pygame.font.SysFont('consolas', 32)
        fonte_go = pygame.font.SysFont('consolas', 64)
        fonte_media = pygame.font.SysFont('consolas', 36)
        fonte_pequena = pygame.font.SysFont('consolas', 24)
        fonte_titulo = pygame.font.SysFont('consolas', 48)
    
    return fonte, fonte_go, fonte_media, fonte_pequena, fonte_titulo
