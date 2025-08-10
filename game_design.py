# Design visual e efeitos do jogo

import pygame
import random
import math
import os
from constants import *

# Variável global para armazenar as imagens
IMAGENS = None

# Carregar imagens
def carregar_imagens():
    """Carregar todas as imagens do jogo"""
    global IMAGENS
    
    if IMAGENS is not None:
        return IMAGENS
    
    imagens = {}
    
    try:
        # Carregar e redimensionar imagens
        imagens['nave'] = pygame.image.load('nave.png').convert_alpha()
        imagens['nave'] = pygame.transform.scale(imagens['nave'], (48, 48))
        
        imagens['enemy'] = pygame.image.load('enemy.png').convert_alpha()
        imagens['enemy'] = pygame.transform.scale(imagens['enemy'], (48, 48))
        
        imagens['tiro'] = pygame.image.load('tiro.png').convert_alpha()
        imagens['tiro'] = pygame.transform.scale(imagens['tiro'], (8, 16))
        
        imagens['fogo'] = pygame.image.load('fogo.png').convert_alpha()
        imagens['fogo'] = pygame.transform.scale(imagens['fogo'], (32, 32))
        
        # Tentar carregar imagem específica do boss, senão usar enemy.png modificado
        if os.path.exists('boss.png'):
            imagens['boss'] = pygame.image.load('boss.png').convert_alpha()
            imagens['boss'] = pygame.transform.scale(imagens['boss'], (96, 96))
        else:
            # Se não houver boss.png, usar enemy.png ampliado
            imagens['boss'] = pygame.transform.scale(imagens['enemy'], (96, 96))
        
        # Carregar imagem de fundo
        if os.path.exists('fundo.jpg'):
            imagens['fundo'] = pygame.image.load('fundo.jpg').convert()
            # Redimensionar para o tamanho da tela
            imagens['fundo'] = pygame.transform.scale(imagens['fundo'], (LARGURA, ALTURA))
        elif os.path.exists('fundo.png'):
            imagens['fundo'] = pygame.image.load('fundo.png').convert()
            imagens['fundo'] = pygame.transform.scale(imagens['fundo'], (LARGURA, ALTURA))
        
        print("Imagens carregadas com sucesso!")
        IMAGENS = imagens
        
    except pygame.error as e:
        print(f"Erro ao carregar imagens: {e}")
        print("Usando sprites programáticos como fallback")
        IMAGENS = {}
    
    return IMAGENS

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
        
        # Reduzir velocidade
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
    """Criar fundo espacial minimalista e elegante"""
    # Tentar carregar imagens se ainda não foram carregadas
    imagens = carregar_imagens()
    
    # Se a imagem de fundo foi carregada, usá-la com overlay sutil
    if imagens and 'fundo' in imagens:
        # Usar a imagem de fundo real
        fundo = imagens['fundo'].copy()
        
        # Aplicar overlay escuro para tornar mais sutil
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((8, 12, 20, 120))  # Escurecer um pouco
        fundo.blit(overlay, (0, 0))
        
        # Adicionar poucas estrelas elegantes
        for i in range(30):  # Muito menos estrelas para look minimalista
            x = random.randint(0, LARGURA)
            y = random.randint(0, ALTURA)
            pygame.draw.circle(fundo, BRANCO_SUAVE, (x, y), 1)
        
        return fundo
    
    # Fallback: fundo minimalista programático
    fundo = pygame.Surface((LARGURA, ALTURA))
    
    # Gradiente suave e elegante
    for y in range(ALTURA):
        intensidade = 20 + int(15 * (1 - y / ALTURA))
        cor = (intensidade // 2, intensidade // 1.5, intensidade)
        pygame.draw.line(fundo, cor, (0, y), (LARGURA, y))
    
    # Poucas estrelas elegantes e bem distribuídas
    estrelas_posicoes = []
    for i in range(80):  # Menos estrelas para visual limpo
        x = random.randint(50, LARGURA-50)
        y = random.randint(50, ALTURA-50)
        
        # Evitar estrelas muito próximas
        muito_proximo = any(abs(x - ex) < 30 and abs(y - ey) < 30 for ex, ey in estrelas_posicoes[-10:])
        if not muito_proximo:
            estrelas_posicoes.append((x, y))
            
            # Estrelas simples e elegantes
            brilho = random.randint(180, 255)
            tamanho = random.choice([1, 1, 1, 2])  # Maioria pequenas
            
            if tamanho == 1:
                pygame.draw.circle(fundo, (brilho, brilho, brilho), (x, y), 1)
            else:
                pygame.draw.circle(fundo, BRANCO_SUAVE, (x, y), 1)
                # Efeito de cruz sutil para estrelas maiores
                pygame.draw.line(fundo, (brilho//2, brilho//2, brilho//2), (x-2, y), (x+2, y), 1)
                pygame.draw.line(fundo, (brilho//2, brilho//2, brilho//2), (x, y-2), (x, y+2), 1)
    
    return fundo

def criar_nave_jogador():
    """Criar sprite da nave do jogador"""
    # Tentar carregar imagens se ainda não foram carregadas
    imagens = carregar_imagens()
    
    # Se as imagens foram carregadas, usar a imagem real
    if imagens and 'nave' in imagens:
        return imagens['nave'].copy()
    
    # Fallback: sprite programático minimalista
    nave = pygame.Surface((48, 48), pygame.SRCALPHA)
    
    # Corpo principal da nave - design limpo
    pontos_corpo = [(24, 4), (6, 38), (15, 34), (24, 26), (33, 34), (42, 38)]
    pygame.draw.polygon(nave, AZUL_SUAVE, pontos_corpo)
    pygame.draw.polygon(nave, BRANCO_SUAVE, pontos_corpo, 2)
    
    # Cockpit elegante
    pygame.draw.circle(nave, AZUL_ESCURO, (24, 19), 6)
    pygame.draw.circle(nave, DESTAQUE_AZUL, (24, 19), 6, 2)
    pygame.draw.circle(nave, DESTAQUE_BRANCO, (24, 17), 2)
    
    # Motores laterais minimalistas
    pygame.draw.rect(nave, CINZA_MEDIO, (11, 30, 6, 11))
    pygame.draw.rect(nave, CINZA_MEDIO, (31, 30, 6, 11))
    pygame.draw.rect(nave, DESTAQUE_AZUL, (11, 30, 6, 11), 1)
    pygame.draw.rect(nave, DESTAQUE_AZUL, (31, 30, 6, 11), 1)
    
    # Propulsores suaves
    pygame.draw.rect(nave, DESTAQUE_AZUL, (13, 41, 3, 6))
    pygame.draw.rect(nave, DESTAQUE_AZUL, (32, 41, 3, 6))
    pygame.draw.rect(nave, BRANCO_SUAVE, (13.5, 42, 2, 4))
    pygame.draw.rect(nave, BRANCO_SUAVE, (32.5, 42, 2, 4))
    
    # Detalhes mínimos e elegantes
    pygame.draw.line(nave, DESTAQUE_VERDE, (24, 6), (24, 24), 1)
    pygame.draw.circle(nave, DESTAQUE_VERDE, (24, 11), 2)
    
    return nave

def criar_boss():
    """Criar sprite do boss"""
    # Tentar carregar imagens se ainda não foram carregadas
    imagens = carregar_imagens()
    
    # Se as imagens foram carregadas, usar a imagem real
    if imagens and 'boss' in imagens:
        boss_img = imagens['boss'].copy()
        
        # Aplicar efeitos especiais ao boss para torná-lo mais intimidador
        # Efeito de brilho dourado/laranja
        overlay = pygame.Surface((96, 96), pygame.SRCALPHA)
        overlay.fill((255, 200, 0, 60))  # Dourado
        boss_img.blit(overlay, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
        
        # Efeito de energia sutil nas bordas
        overlay2 = pygame.Surface((96, 96), pygame.SRCALPHA)
        overlay2.fill((120, 100, 150, 30))  # Roxo suave
        boss_img.blit(overlay2, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
        
        return boss_img
    
    # Fallback: sprite programático minimalista
    boss = pygame.Surface((96, 96), pygame.SRCALPHA)
    
    # Corpo principal hexagonal elegante
    pontos_hex = []
    for i in range(6):
        angulo = i * 60 * math.pi / 180
        x = 48 + 37 * math.cos(angulo)
        y = 48 + 37 * math.sin(angulo)
        pontos_hex.append((x, y))
    
    pygame.draw.polygon(boss, ROXO_SUAVE, pontos_hex)
    pygame.draw.polygon(boss, BRANCO_SUAVE, pontos_hex, 2)
    
    # Núcleo central minimalista
    pygame.draw.circle(boss, CINZA_ESCURO, (48, 48), 19)
    pygame.draw.circle(boss, DESTAQUE_LARANJA, (48, 48), 15)
    pygame.draw.circle(boss, CINZA_CLARO, (48, 48), 11)
    pygame.draw.circle(boss, DESTAQUE_BRANCO, (48, 48), 7)
    
    # Canhões laterais elegantes
    for i in range(4):
        angulo = i * 90 * math.pi / 180
        x = 48 + 26 * math.cos(angulo)
        y = 48 + 26 * math.sin(angulo)
        pygame.draw.circle(boss, CINZA_MEDIO, (int(x), int(y)), 6)
        pygame.draw.circle(boss, DESTAQUE_LARANJA, (int(x), int(y)), 6, 1)
        pygame.draw.circle(boss, BRANCO_SUAVE, (int(x), int(y)), 4)
    
    # Detalhes tecnológicos minimalistas
    for i in range(8):
        angulo = i * 45 * math.pi / 180
        x1 = 48 + 19 * math.cos(angulo)
        y1 = 48 + 19 * math.sin(angulo)
        x2 = 48 + 34 * math.cos(angulo)
        y2 = 48 + 34 * math.sin(angulo)
        pygame.draw.line(boss, DESTAQUE_AZUL, (x1, y1), (x2, y2), 1)
    
    # Borda elegante
    pygame.draw.circle(boss, DESTAQUE_AZUL, (48, 48), 45, 1)
    
    return boss

def criar_inimigo(tipo):
    """Criar sprite de inimigo baseado no tipo"""
    # Tentar carregar imagens se ainda não foram carregadas
    imagens = carregar_imagens()
    
    # Se as imagens foram carregadas, usar a imagem real
    if imagens and 'enemy' in imagens:
        # Criar diferentes variações coloridas da imagem do inimigo
        img = imagens['enemy'].copy()
        
        # Aplicar tint colorido baseado no tipo
        overlay = pygame.Surface((48, 48), pygame.SRCALPHA)
        if tipo == 1:
            overlay.fill((255, 100, 100, 80))  # Vermelho
        elif tipo == 2:
            overlay.fill((100, 100, 255, 80))  # Azul
        else:
            overlay.fill((255, 100, 255, 80))  # Roxo
        
        img.blit(overlay, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
        return img
    
    # Fallback: sprite programático (menor)
    img = pygame.Surface((48, 48), pygame.SRCALPHA)
    
    if tipo == 1:
        # Inimigo triangular (menor)
        pontos = [(24, 8), (8, 38), (40, 38)]
        cor_principal = CINZA_MEDIO
        pygame.draw.polygon(img, cor_principal, pontos)
        pygame.draw.polygon(img, DESTAQUE_VERMELHO, pontos, 2)
        pygame.draw.circle(img, DESTAQUE_AZUL, (24, 26), 3)
        
    elif tipo == 2:
        # Inimigo hexagonal (menor)
        pontos_hex = []
        for j in range(6):
            angulo = j * 60 * math.pi / 180
            x = 24 + 15 * math.cos(angulo)  # Centro em 24, raio 15
            y = 24 + 15 * math.sin(angulo)
            pontos_hex.append((x, y))
        cor_principal = CINZA_MEDIO
        pygame.draw.polygon(img, cor_principal, pontos_hex)
        pygame.draw.polygon(img, DESTAQUE_AZUL, pontos_hex, 2)
        pygame.draw.circle(img, AZUL_SUAVE, (24, 24), 5)
        
    else:
        # Inimigo circular (menor)
        cor_principal = CINZA_MEDIO
        pygame.draw.circle(img, cor_principal, (24, 24), 15)
        pygame.draw.circle(img, DESTAQUE_VERMELHO, (24, 24), 15, 2)
        pygame.draw.circle(img, AZUL_SUAVE, (24, 24), 7)
        pygame.draw.circle(img, BRANCO_SUAVE, (24, 24), 3)
        
        # Detalhes laterais (menores)
        pygame.draw.circle(img, DESTAQUE_AZUL, (11, 24), 2)
        pygame.draw.circle(img, DESTAQUE_AZUL, (37, 24), 2)
    
    return img

def criar_tiro_jogador():
    """Criar sprite do tiro do jogador"""
    # Tentar carregar imagens se ainda não foram carregadas
    imagens = carregar_imagens()
    
    # Se as imagens foram carregadas, usar a imagem real
    if imagens and 'tiro' in imagens:
        return imagens['tiro'].copy()
    
    # Fallback: sprite programático
    tiro = pygame.Surface((8, 16), pygame.SRCALPHA)
    pygame.draw.rect(tiro, DESTAQUE_AZUL, (3, 0, 2, 16))
    pygame.draw.rect(tiro, BRANCO_SUAVE, (3.5, 0, 1, 16))
    pygame.draw.rect(tiro, AZUL_SUAVE, (2, 0, 4, 16))
    pygame.draw.rect(tiro, AZUL_ESCURO, (1, 0, 6, 16))
    return tiro

def criar_tiro_inimigo():
    """Criar sprite do tiro do inimigo"""
    # Tentar carregar imagens se ainda não foram carregadas
    imagens = carregar_imagens()
    
    # Se as imagens foram carregadas, usar versão vermelha do tiro
    if imagens and 'tiro' in imagens:
        tiro = imagens['tiro'].copy()
        # Aplicar tint vermelho
        overlay = pygame.Surface((8, 16), pygame.SRCALPHA)
        overlay.fill((255, 0, 0, 120))
        tiro.blit(overlay, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
        return tiro
    
    # Fallback: sprite programático
    tiro = pygame.Surface((8, 16), pygame.SRCALPHA)
    pygame.draw.rect(tiro, DESTAQUE_VERMELHO, (2, 0, 4, 16))
    pygame.draw.rect(tiro, VERMELHO, (1, 0, 6, 16))
    pygame.draw.rect(tiro, CINZA_MEDIO, (0, 0, 8, 16))
    return tiro

def criar_tiro_boss():
    """Criar sprite do tiro do boss"""
    # Tentar carregar imagens se ainda não foram carregadas
    imagens = carregar_imagens()
    
    # Se as imagens foram carregadas, usar versão especial do tiro
    if imagens and 'tiro' in imagens:
        # Usar tiro maior para o boss
        tiro = pygame.transform.scale(imagens['tiro'], (12, 24))
        
        # Aplicar efeito laranja/dourado para diferenciá-lo
        overlay = pygame.Surface((12, 24), pygame.SRCALPHA)
        overlay.fill((255, 150, 0, 100))  # Laranja dourado
        tiro.blit(overlay, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
        
        return tiro
    
    # Fallback: sprite programático
    tiro = pygame.Surface((12, 24), pygame.SRCALPHA)
    pygame.draw.rect(tiro, DESTAQUE_LARANJA, (3, 0, 6, 24))
    pygame.draw.rect(tiro, AMARELO, (4, 0, 4, 24))
    pygame.draw.rect(tiro, BRANCO_SUAVE, (5, 0, 2, 24))
    pygame.draw.rect(tiro, LARANJA_SUAVE, (2, 0, 8, 24))
    pygame.draw.rect(tiro, CINZA_CLARO, (1, 0, 10, 24))
    return tiro

def criar_sprite_explosao(tamanho=32):
    """Criar sprite de explosão usando imagem do fogo"""
    # Tentar carregar imagens se ainda não foram carregadas
    imagens = carregar_imagens()
    
    # Se as imagens foram carregadas, usar a imagem real
    if imagens and 'fogo' in imagens:
        explosao = imagens['fogo'].copy()
        if tamanho != 32:
            explosao = pygame.transform.scale(explosao, (tamanho, tamanho))
        return explosao
    
    # Fallback: sprite programático de explosão
    explosao = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
    centro = tamanho // 2
    
    # Círculos concêntricos para simular explosão
    pygame.draw.circle(explosao, (255, 0, 0), (centro, centro), centro, 0)
    pygame.draw.circle(explosao, (255, 100, 0), (centro, centro), int(centro * 0.8), 0)
    pygame.draw.circle(explosao, (255, 200, 0), (centro, centro), int(centro * 0.6), 0)
    pygame.draw.circle(explosao, (255, 255, 0), (centro, centro), int(centro * 0.4), 0)
    pygame.draw.circle(explosao, (255, 255, 255), (centro, centro), int(centro * 0.2), 0)
    
    return explosao

def criar_explosao(x, y, cor_base, particulas_list):
    """Criar partículas de explosão"""
    for i in range(PARTICULAS_POR_EXPLOSAO):
        velocidade_x = random.uniform(-5, 5)
        velocidade_y = random.uniform(-5, 5)
        vida = random.randint(VIDA_PARTICULA_MIN, VIDA_PARTICULA_MAX)
        cor = random.choice([cor_base, AMARELO, DESTAQUE_LARANJA, BRANCO_SUAVE])
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
