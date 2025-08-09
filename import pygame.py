import pygame
import random
import math
import os
from pygame import mixer

# Inicializar o pygame
pygame.init()

# Criar a tela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))

# Título e ícone
pygame.display.set_caption("Space Shooter - Galaxy Attack")
icone = pygame.Surface((32, 32))
icone.fill((255, 255, 255))
pygame.display.set_icon(icone)

# Cores espaciais e tecnológicas
PRETO = (0, 0, 0)
PRETO_ESPACIAL = (5, 10, 25)  # Azul escuro do espaço
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
CINZA = (100, 100, 100)
ROXO = (128, 0, 128)
LARANJA = (255, 165, 0)

# Cores tecnológicas
AZUL_NEON = (0, 255, 255)  # Ciano brilhante
AZUL_ESCURO = (0, 50, 100)  # Azul escuro
VERDE_NEON = (57, 255, 20)  # Verde lime brilhante
ROXO_NEON = (148, 0, 211)  # Roxo brilhante
ROSA_NEON = (255, 20, 147)  # Rosa brilhante
LARANJA_NEON = (255, 140, 0)  # Laranja brilhante
VERMELHO_NEON = (255, 0, 100)  # Vermelho brilhante
BRANCO_AZULADO = (200, 220, 255)  # Branco com tom azul

# Fundo espacial avançado
def criar_fundo_espacial():
    fundo = pygame.Surface((largura, altura))
    
    # Gradiente espacial (do azul escuro para preto)
    for y in range(altura):
        intensidade = int(25 * (1 - y / altura))  # Gradiente vertical
        cor = (intensidade // 3, intensidade // 2, intensidade)
        pygame.draw.line(fundo, cor, (0, y), (largura, y))
    
    # Estrelas de diferentes tamanhos e brilhos
    for i in range(150):
        x = random.randint(0, largura)
        y = random.randint(0, altura)
        tamanho = random.randint(1, 4)
        brilho = random.randint(150, 255)
        
        if tamanho == 1:
            pygame.draw.circle(fundo, (brilho, brilho, brilho), (x, y), 1)
        elif tamanho == 2:
            pygame.draw.circle(fundo, (brilho, brilho, brilho), (x, y), 1)
            pygame.draw.circle(fundo, (brilho//2, brilho//2, brilho//2), (x, y), 2)
        elif tamanho == 3:
            # Estrela brilhante com halo
            pygame.draw.circle(fundo, (brilho, brilho, brilho), (x, y), 2)
            pygame.draw.circle(fundo, (brilho//3, brilho//3, brilho//3), (x, y), 4)
        else:
            # Estrela muito brilhante com cruz
            pygame.draw.circle(fundo, BRANCO, (x, y), 2)
            pygame.draw.line(fundo, BRANCO, (x-4, y), (x+4, y), 1)
            pygame.draw.line(fundo, BRANCO, (x, y-4), (x, y+4), 1)
    
    # Nebulosas distantes (círculos semi-transparentes)
    nebulosa_surface = pygame.Surface((largura, altura), pygame.SRCALPHA)
    for i in range(8):
        x = random.randint(50, largura-50)
        y = random.randint(50, altura-50)
        raio = random.randint(30, 80)
        cor_nebulosa = random.choice([
            (50, 0, 100, 30),   # Roxo
            (0, 50, 100, 30),   # Azul
            (100, 0, 50, 30),   # Rosa
            (0, 100, 50, 30)    # Verde
        ])
        pygame.draw.circle(nebulosa_surface, cor_nebulosa, (x, y), raio)
    
    fundo.blit(nebulosa_surface, (0, 0))
    return fundo

# Criar fundo
fundo = criar_fundo_espacial()

# Sons
try:
    mixer.music.load('background.wav')
    mixer.music.play(-1)
    som_tiro = mixer.Sound('laser.wav')
    som_explosao = mixer.Sound('explosion.wav')
except:
    print("Arquivos de som não encontrados. O jogo funcionará sem áudio.")

# Nave do jogador com design tecnológico
def criar_nave_jogador():
    nave = pygame.Surface((64, 64), pygame.SRCALPHA)
    
    # Corpo principal da nave (triangular futurista)
    pontos_corpo = [(32, 5), (8, 50), (20, 45), (32, 35), (44, 45), (56, 50)]
    pygame.draw.polygon(nave, AZUL_NEON, pontos_corpo)
    pygame.draw.polygon(nave, BRANCO_AZULADO, pontos_corpo, 2)
    
    # Cockpit (cabine do piloto)
    pygame.draw.circle(nave, AZUL_ESCURO, (32, 25), 8)
    pygame.draw.circle(nave, AZUL_NEON, (32, 25), 8, 2)
    pygame.draw.circle(nave, BRANCO, (32, 23), 3)
    
    # Motores laterais
    pygame.draw.rect(nave, CINZA, (15, 40, 8, 15))
    pygame.draw.rect(nave, CINZA, (41, 40, 8, 15))
    pygame.draw.rect(nave, AZUL_NEON, (15, 40, 8, 15), 2)
    pygame.draw.rect(nave, AZUL_NEON, (41, 40, 8, 15), 2)
    
    # Propulsores (efeito de fogo azul)
    pygame.draw.rect(nave, AZUL_NEON, (17, 55, 4, 8))
    pygame.draw.rect(nave, AZUL_NEON, (43, 55, 4, 8))
    pygame.draw.rect(nave, BRANCO, (18, 56, 2, 6))
    pygame.draw.rect(nave, BRANCO, (44, 56, 2, 6))
    
    # Detalhes tecnológicos (luzes e linhas)
    pygame.draw.line(nave, VERDE_NEON, (32, 8), (32, 32), 2)
    pygame.draw.circle(nave, VERDE_NEON, (20, 20), 2)
    pygame.draw.circle(nave, VERDE_NEON, (44, 20), 2)
    pygame.draw.circle(nave, VERMELHO_NEON, (32, 15), 2)
    
    return nave

jogador_img = criar_nave_jogador()
jogador_x = 370
jogador_y = 480
jogador_x_mudanca = 0
jogador_velocidade = 5

# Inimigo
inimigo_img = []
inimigo_x = []
inimigo_y = []
inimigo_x_mudanca = []
inimigo_y_mudanca = []
inimigo_vida = []  # Vida dos inimigos normais (1 hit para destruir)
num_inimigos = 6

# Boss tecnológico avançado
def criar_boss():
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
    
    # Núcleo central pulsante
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
    
    # Escudo energético (borda externa)
    pygame.draw.circle(boss, AZUL_NEON, (64, 64), 60, 2)
    
    return boss

boss_img = criar_boss()
boss_x = 336  # Centralizado (800 - 128) / 2
boss_y = 100
boss_x_mudanca = 3
boss_vida = 20  # Boss precisa de vários tiros para ser destruído
boss_ativo = False
boss_tiros_cooldown = 0

# Tiros dos inimigos com efeito plasma
def criar_tiro_inimigo():
    tiro = pygame.Surface((8, 16), pygame.SRCALPHA)
    # Núcleo do tiro
    pygame.draw.rect(tiro, VERMELHO_NEON, (2, 0, 4, 16))
    # Brilho externo
    pygame.draw.rect(tiro, VERMELHO, (1, 0, 6, 16))
    pygame.draw.rect(tiro, (255, 100, 100), (0, 0, 8, 16))
    return tiro

tiros_inimigos_img = criar_tiro_inimigo()
tiros_inimigos_x = []
tiros_inimigos_y = []
tiros_inimigos_velocidade = 5
tiros_inimigos_estado = []
tiros_inimigos_cooldown = []
max_tiros_inimigos = 3

# Tiros do boss com efeito de energia
def criar_tiro_boss():
    tiro = pygame.Surface((12, 24), pygame.SRCALPHA)
    # Núcleo energético
    pygame.draw.rect(tiro, LARANJA_NEON, (3, 0, 6, 24))
    pygame.draw.rect(tiro, AMARELO, (4, 0, 4, 24))
    pygame.draw.rect(tiro, BRANCO, (5, 0, 2, 24))
    # Brilho externo
    pygame.draw.rect(tiro, LARANJA, (2, 0, 8, 24))
    pygame.draw.rect(tiro, (255, 200, 100), (1, 0, 10, 24))
    pygame.draw.rect(tiro, (255, 255, 200), (0, 0, 12, 24))
    return tiro

tiros_boss_img = criar_tiro_boss()
tiros_boss_x = []
tiros_boss_y = []
tiros_boss_velocidade = 7
tiros_boss_estado = []
max_tiros_boss = 5

# Inicializar tiros do boss
for i in range(max_tiros_boss):
    tiros_boss_x.append(0)
    tiros_boss_y.append(0)
    tiros_boss_estado.append("pronto")

# Inicializar inimigos
def inicializar_inimigos(nivel):
    global inimigo_img, inimigo_x, inimigo_y, inimigo_x_mudanca, inimigo_y_mudanca, num_inimigos, inimigo_vida
    global boss_ativo, boss_vida
    
    # Verificar se é hora de ativar o boss (a cada 3 níveis)
    if nivel > 0 and nivel % 3 == 0:
        boss_ativo = True
        boss_vida = 20 + (nivel // 3) * 5  # Aumenta a vida do boss conforme avança
        return
    
    # Se não for nível de boss, inicializa inimigos normais
    boss_ativo = False
    
    # Limpar listas anteriores
    inimigo_img.clear()
    inimigo_x.clear()
    inimigo_y.clear()
    inimigo_x_mudanca.clear()
    inimigo_y_mudanca.clear()
    inimigo_vida.clear()
    
    # Aumentar número de inimigos com o nível
    num_inimigos = 6 + (nivel - 1) * 2
    if num_inimigos > 15:
        num_inimigos = 15
    
    # Velocidade aumenta com o nível
    velocidade_base = 2 + (nivel - 1) * 0.5
    if velocidade_base > 5:
        velocidade_base = 5
    
    for i in range(num_inimigos):
        # Criar imagem do inimigo com design tecnológico
        img = pygame.Surface((64, 64), pygame.SRCALPHA)
        
        # Escolher um tipo de inimigo aleatório
        tipo_inimigo = random.randint(1, 3)
        
        if tipo_inimigo == 1:
            # Inimigo triangular
            pontos = [(32, 10), (10, 50), (54, 50)]
            cor_principal = (random.randint(150, 255), random.randint(0, 100), random.randint(0, 100))
            pygame.draw.polygon(img, cor_principal, pontos)
            pygame.draw.polygon(img, VERMELHO_NEON, pontos, 2)
            pygame.draw.circle(img, LARANJA_NEON, (32, 35), 5)
            
        elif tipo_inimigo == 2:
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
            # Inimigo circular com detalhes
            cor_principal = (random.randint(100, 255), random.randint(50, 150), random.randint(50, 200))
            pygame.draw.circle(img, cor_principal, (32, 32), 20)
            pygame.draw.circle(img, ROXO_NEON, (32, 32), 20, 2)
            pygame.draw.circle(img, LARANJA_NEON, (32, 32), 10)
            pygame.draw.circle(img, BRANCO, (32, 32), 5)
            
            # Detalhes laterais
            pygame.draw.circle(img, VERDE_NEON, (15, 32), 3)
            pygame.draw.circle(img, VERDE_NEON, (49, 32), 3)
        
        inimigo_img.append(img)
        
        # Posicionar inimigos com distância da nave
        x = random.randint(0, 736)
        y = random.randint(50, 150)
        inimigo_x.append(x)
        inimigo_y.append(y)
        
        # Velocidade aumenta com o nível
        direcao = 1 if random.random() > 0.5 else -1
        inimigo_x_mudanca.append(velocidade_base * direcao)
        inimigo_y_mudanca.append(40)
        
        # Vida do inimigo (sempre 1 para inimigos normais)
        inimigo_vida.append(1)
    
    # Inicializar tiros dos inimigos
    tiros_inimigos_x.clear()
    tiros_inimigos_y.clear()
    tiros_inimigos_estado.clear()
    tiros_inimigos_cooldown.clear()
    
    for i in range(max_tiros_inimigos):
        tiros_inimigos_x.append(0)
        tiros_inimigos_y.append(0)
        tiros_inimigos_estado.append("pronto")
        tiros_inimigos_cooldown.append(random.randint(50, 200))

# Tiro do jogador com efeito laser
def criar_tiro_jogador():
    tiro = pygame.Surface((8, 16), pygame.SRCALPHA)
    # Núcleo do laser
    pygame.draw.rect(tiro, VERDE_NEON, (3, 0, 2, 16))
    pygame.draw.rect(tiro, BRANCO, (3.5, 0, 1, 16))
    # Brilho externo
    pygame.draw.rect(tiro, VERDE, (2, 0, 4, 16))
    pygame.draw.rect(tiro, (100, 255, 100), (1, 0, 6, 16))
    pygame.draw.rect(tiro, (150, 255, 150), (0, 0, 8, 16))
    return tiro

tiro_img = criar_tiro_jogador()
tiro_x = 0
tiro_y = 480
tiro_y_mudanca = 15  # Aumentado para tiros mais rápidos
tiro_estado = "pronto"  # pronto - não visível, disparado - visível

# Pontuação
pontuacao = 0
fonte = pygame.font.SysFont('arial', 32)
texto_x = 10
texto_y = 10

# Nível
nivel = 1
inimigos_restantes = num_inimigos

# Fontes tecnológicas
try:
    # Tentar usar fontes mais tecnológicas
    fonte = pygame.font.Font(None, 32)
    fonte_go = pygame.font.Font(None, 64)
    fonte_media = pygame.font.Font(None, 36)
    fonte_pequena = pygame.font.Font(None, 24)
    fonte_titulo = pygame.font.Font(None, 48)
except:
    # Fallback para fontes do sistema
    fonte = pygame.font.SysFont('consolas', 32)  # Fonte monoespaçada
    fonte_go = pygame.font.SysFont('consolas', 64)
    fonte_media = pygame.font.SysFont('consolas', 36)
    fonte_pequena = pygame.font.SysFont('consolas', 24)
    fonte_titulo = pygame.font.SysFont('consolas', 48)

# Estados do jogo
ESTADO_MENU = 0
ESTADO_INSTRUCOES = 1
ESTADO_JOGO = 2
ESTADO_GAME_OVER = 3
ESTADO_PROXIMO_NIVEL = 4
ESTADO_PAUSA = 5  # Estado para pausa
ESTADO_BOSS_DERROTADO = 6  # Novo estado para quando o boss é derrotado
estado_atual = ESTADO_MENU

# Sistema de partículas para explosões
particulas = []

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

def criar_explosao(x, y, cor_base):
    """Criar partículas de explosão"""
    for i in range(15):
        velocidade_x = random.uniform(-5, 5)
        velocidade_y = random.uniform(-5, 5)
        vida = random.randint(20, 40)
        cor = random.choice([cor_base, AMARELO, LARANJA_NEON, BRANCO])
        particula = Particula(x, y, cor, velocidade_x, velocidade_y, vida)
        particulas.append(particula)

def atualizar_particulas():
    """Atualizar e desenhar todas as partículas"""
    global particulas
    particulas_ativas = []
    
    for particula in particulas:
        particula.atualizar()
        if particula.vida > 0:
            particula.desenhar(tela)
            particulas_ativas.append(particula)
    
    particulas = particulas_ativas

# Função para mostrar pontuação com efeito tecnológico
def mostrar_pontuacao(x, y):
    # Sombra/brilho
    texto_sombra = fonte.render(f"PONTUAÇÃO: {pontuacao}", True, AZUL_ESCURO)
    tela.blit(texto_sombra, (x + 2, y + 2))
    # Texto principal
    texto = fonte.render(f"PONTUAÇÃO: {pontuacao}", True, AZUL_NEON)
    tela.blit(texto, (x, y))

# Função para mostrar nível com efeito tecnológico
def mostrar_nivel(x, y):
    # Sombra/brilho
    texto_sombra = fonte.render(f"NÍVEL: {nivel}", True, AZUL_ESCURO)
    tela.blit(texto_sombra, (x + 2, y + 2))
    # Texto principal
    texto = fonte.render(f"NÍVEL: {nivel}", True, VERDE_NEON)
    tela.blit(texto, (x, y))

# Função para mostrar vida do boss com barra de energia
def mostrar_vida_boss(x, y):
    # Título
    texto_sombra = fonte.render("ENERGIA DO BOSS:", True, (100, 0, 0))
    tela.blit(texto_sombra, (x + 2, y + 2))
    texto = fonte.render("ENERGIA DO BOSS:", True, VERMELHO_NEON)
    tela.blit(texto, (x, y))
    
    # Barra de energia
    barra_largura = 200
    barra_altura = 20
    vida_maxima = 20 + (nivel // 3) * 5  # Vida máxima do boss atual
    vida_percentual = boss_vida / vida_maxima
    
    # Fundo da barra
    pygame.draw.rect(tela, CINZA, (x, y + 30, barra_largura, barra_altura))
    pygame.draw.rect(tela, BRANCO, (x, y + 30, barra_largura, barra_altura), 2)
    
    # Barra de vida
    cor_vida = VERMELHO_NEON if vida_percentual < 0.3 else LARANJA_NEON if vida_percentual < 0.6 else VERDE_NEON
    largura_vida = int(barra_largura * vida_percentual)
    if largura_vida > 0:
        pygame.draw.rect(tela, cor_vida, (x, y + 30, largura_vida, barra_altura))
    
    # Texto da vida
    texto_vida = fonte_pequena.render(f"{boss_vida}/{vida_maxima}", True, BRANCO)
    tela.blit(texto_vida, (x + barra_largura + 10, y + 32))

# Função para desenhar o jogador
def jogador(x, y):
    tela.blit(jogador_img, (x, y))

# Função para desenhar o inimigo
def inimigo(x, y, i):
    tela.blit(inimigo_img[i], (x, y))

# Função para desenhar o boss
def desenhar_boss(x, y):
    tela.blit(boss_img, (x, y))

# Função para disparar o tiro do jogador
def disparar_tiro(x, y):
    global tiro_estado
    tiro_estado = "disparado"
    tela.blit(tiro_img, (x + 28, y + 10))
    try:
        som_tiro.play()
    except:
        pass

# Função para disparar tiro do inimigo
def disparar_tiro_inimigo(i, x, y):
    global tiros_inimigos_estado
    if tiros_inimigos_estado[i] == "pronto":
        tiros_inimigos_estado[i] = "disparado"
        tiros_inimigos_x[i] = x + 28
        tiros_inimigos_y[i] = y + 40

# Função para disparar tiro do boss
def disparar_tiro_boss(i, x, y):
    global tiros_boss_estado
    if tiros_boss_estado[i] == "pronto":
        tiros_boss_estado[i] = "disparado"
        tiros_boss_x[i] = x + 58  # Centralizado no boss
        tiros_boss_y[i] = y + 80

# Função para verificar colisão com inimigos (aumentada sensibilidade)
def colisao(inimigo_x, inimigo_y, tiro_x, tiro_y):
    distancia = math.sqrt((inimigo_x + 32 - tiro_x - 4) ** 2 + (inimigo_y + 32 - tiro_y - 8) ** 2)
    if distancia < 40:  # Aumentado de 27 para 40 para maior sensibilidade
        return True
    return False

# Função para verificar colisão com boss
def colisao_boss(boss_x, boss_y, tiro_x, tiro_y):
    distancia = math.sqrt((boss_x + 64 - tiro_x - 4) ** 2 + (boss_y + 64 - tiro_y - 8) ** 2)
    if distancia < 60:  # Área de colisão grande para o boss
        return True
    return False

# Função para verificar colisão com jogador
def colisao_jogador(jogador_x, jogador_y, tiro_x, tiro_y):
    distancia = math.sqrt((jogador_x + 32 - tiro_x - 4) ** 2 + (jogador_y + 32 - tiro_y - 8) ** 2)
    if distancia < 30:
        return True
    return False

# Função para mostrar game over futurista
def game_over_texto():
    # Efeito de glitch no texto
    for i in range(3):
        offset_x = random.randint(-2, 2)
        offset_y = random.randint(-2, 2)
        cor_glitch = random.choice([VERMELHO_NEON, AZUL_NEON, VERDE_NEON])
        texto_glitch = fonte_go.render("MISSÃO FALHOU", True, cor_glitch)
        tela.blit(texto_glitch, (200 + offset_x, 250 + offset_y))
    
    # Texto principal
    texto_go = fonte_go.render("MISSÃO FALHOU", True, VERMELHO_NEON)
    tela.blit(texto_go, (200, 250))

# Função para mostrar tela de menu futurista
def mostrar_menu():
    tela.blit(fundo, (0, 0))
    
    # Título com efeito neon
    titulo_sombra = fonte_go.render("GALAXY DEFENDER", True, AZUL_ESCURO)
    tela.blit(titulo_sombra, (152, 152))
    titulo = fonte_go.render("GALAXY DEFENDER", True, AZUL_NEON)
    tela.blit(titulo, (150, 150))
    
    # Subtítulo
    subtitulo = fonte_media.render("- OPERAÇÃO ESTELAR -", True, VERDE_NEON)
    tela.blit(subtitulo, (220, 200))
    
    # Botão de início futurista
    botao_rect = pygame.Rect(300, 280, 200, 60)
    
    # Efeito de brilho no botão
    pygame.draw.rect(tela, AZUL_ESCURO, (botao_rect.x + 3, botao_rect.y + 3, botao_rect.width, botao_rect.height))
    pygame.draw.rect(tela, AZUL_NEON, botao_rect)
    pygame.draw.rect(tela, BRANCO_AZULADO, botao_rect, 3)
    
    # Detalhes tecnológicos no botão
    pygame.draw.line(tela, VERDE_NEON, (botao_rect.x + 10, botao_rect.y + 10), (botao_rect.x + 30, botao_rect.y + 10), 2)
    pygame.draw.line(tela, VERDE_NEON, (botao_rect.x + botao_rect.width - 30, botao_rect.y + 10), (botao_rect.x + botao_rect.width - 10, botao_rect.y + 10), 2)
    pygame.draw.line(tela, VERDE_NEON, (botao_rect.x + 10, botao_rect.y + botao_rect.height - 10), (botao_rect.x + 30, botao_rect.y + botao_rect.height - 10), 2)
    pygame.draw.line(tela, VERDE_NEON, (botao_rect.x + botao_rect.width - 30, botao_rect.y + botao_rect.height - 10), (botao_rect.x + botao_rect.width - 10, botao_rect.y + botao_rect.height - 10), 2)
    
    texto_botao = fonte_media.render("INICIAR MISSÃO", True, BRANCO)
    texto_rect = texto_botao.get_rect(center=botao_rect.center)
    tela.blit(texto_botao, texto_rect)
    
    # Informações adicionais
    info1 = fonte_pequena.render(">> SISTEMA DE DEFESA PLANETÁRIA ATIVO <<", True, VERDE_NEON)
    tela.blit(info1, (200, 380))
    
    info2 = fonte_pequena.render("STATUS: AGUARDANDO COMANDOS DO PILOTO", True, AMARELO)
    tela.blit(info2, (220, 400))
    
    # Versão tecnológica
    versao = fonte_pequena.render("VERSÃO 4.0 - QUANTUM EDITION", True, ROXO_NEON)
    tela.blit(versao, (10, altura - 30))

# Função para mostrar instruções futuristas
def mostrar_instrucoes():
    tela.blit(fundo, (0, 0))
    
    # Título
    titulo_sombra = fonte_media.render("BRIEFING DA MISSÃO", True, AZUL_ESCURO)
    tela.blit(titulo_sombra, (302, 102))
    titulo = fonte_media.render("BRIEFING DA MISSÃO", True, AMARELO)
    tela.blit(titulo, (300, 100))
    
    # Linha decorativa
    pygame.draw.line(tela, AZUL_NEON, (100, 130), (700, 130), 2)
    
    # Instruções com cores tecnológicas
    instrucoes = [
        (">> CONTROLES DA NAVE:", VERDE_NEON),
        ("   ← → : Movimentação lateral", BRANCO_AZULADO),
        ("   ESPAÇO : Disparar lasers", BRANCO_AZULADO),
        ("", BRANCO),
        (">> OBJETIVOS DA MISSÃO:", LARANJA_NEON),
        ("   • Eliminar todas as ameaças hostis", BRANCO_AZULADO),
        ("   • Avançar através dos setores galácticos", BRANCO_AZULADO),
        ("   • Enfrentar comandantes inimigos a cada 3 setores", VERMELHO_NEON),
        ("", BRANCO),
        (">> SISTEMAS AUXILIARES:", ROXO_NEON),
        ("   P : Ativar modo de pausa de emergência", BRANCO_AZULADO),
        ("", BRANCO),
        ("⚠ CUIDADO: Evite projéteis hostis!", VERMELHO_NEON),
        ("", BRANCO),
        ("[ R ] - INICIAR OPERAÇÃO", VERDE_NEON)
    ]
    
    y_pos = 160
    for texto, cor in instrucoes:
        if texto:
            if texto.startswith(">>"):
                # Cabeçalhos com efeito
                texto_sombra = fonte_pequena.render(texto, True, AZUL_ESCURO)
                tela.blit(texto_sombra, (102, y_pos + 2))
            rendered_text = fonte_pequena.render(texto, True, cor)
            tela.blit(rendered_text, (100, y_pos))
        y_pos += 25

# Função para mostrar tela de próximo nível
def mostrar_proximo_nivel():
    tela.blit(fundo, (0, 0))
    
    # Mensagem de nível concluído
    texto_nivel = fonte_media.render(f"NÍVEL {nivel-1} CONCLUÍDO!", True, VERDE)
    tela.blit(texto_nivel, (250, 200))
    
    # Próximo nível
    if nivel % 3 == 0:
        texto_proximo = fonte_media.render(f"PREPARANDO NÍVEL {nivel}... BOSS CHEGANDO!", True, VERMELHO)
    else:
        texto_proximo = fonte_media.render(f"PREPARANDO NÍVEL {nivel}...", True, AMARELO)
    
    tela.blit(texto_proximo, (180, 300))
    
    # Instruções
    texto_continuar = fonte_pequena.render("Pressione ESPAÇO para continuar", True, BRANCO)
    tela.blit(texto_continuar, (250, 400))

# Função para mostrar tela de boss derrotado
def mostrar_boss_derrotado():
    tela.blit(fundo, (0, 0))
    
    # Mensagem de boss derrotado
    texto_boss = fonte_go.render("BOSS DERROTADO!", True, VERDE)
    tela.blit(texto_boss, (180, 200))
    
    # Pontuação bônus
    texto_bonus = fonte_media.render(f"BÔNUS: +{boss_vida * 5} PONTOS!", True, AMARELO)
    tela.blit(texto_bonus, (250, 300))
    
    # Instruções
    texto_continuar = fonte_pequena.render("Pressione ESPAÇO para continuar", True, BRANCO)
    tela.blit(texto_continuar, (250, 400))

# Função para mostrar tela de pausa
def mostrar_pausa():
    # Criar superfície semi-transparente
    pausa_overlay = pygame.Surface((largura, altura), pygame.SRCALPHA)
    pausa_overlay.fill((0, 0, 0, 128))  # Preto com 50% de transparência
    tela.blit(pausa_overlay, (0, 0))
    
    # Título de pausa
    titulo_pausa = fonte_go.render("JOGO PAUSADO", True, BRANCO)
    tela.blit(titulo_pausa, (200, 200))
    
    # Instruções
    continuar = fonte_media.render("Pressione P para continuar", True, BRANCO)
    tela.blit(continuar, (250, 300))
    
    # Botão de menu principal
    pygame.draw.rect(tela, AZUL, (300, 350, 200, 50))
    pygame.draw.rect(tela, BRANCO, (300, 350, 200, 50), 2)
    texto_menu = fonte_pequena.render("Menu Principal", True, BRANCO)
    tela.blit(texto_menu, (330, 365))

# Inicializar inimigos para o primeiro nível
inicializar_inimigos(nivel)

# Loop do jogo
executando = True
game_over = False
clock = pygame.time.Clock()
tempo_proximo_nivel = 0
tempo_cooldown = 0

while executando:
    # Limitar a 60 FPS
    clock.tick(60)
    
    # Eventos comuns a todos os estados
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
            
        # Verificar se uma tecla foi pressionada
        if evento.type == pygame.KEYDOWN:
            # Tecla de pausa (funciona em qualquer estado do jogo)
            if evento.key == pygame.K_p:
                if estado_atual == ESTADO_JOGO:
                    estado_atual = ESTADO_PAUSA
                elif estado_atual == ESTADO_PAUSA:
                    estado_atual = ESTADO_JOGO
            
            # Controles do menu
            if estado_atual == ESTADO_MENU:
                if evento.key == pygame.K_RETURN:
                    estado_atual = ESTADO_INSTRUCOES
            
            # Controles das instruções
            elif estado_atual == ESTADO_INSTRUCOES:
                if evento.key == pygame.K_r:
                    estado_atual = ESTADO_JOGO
            
            # Controles do jogo
            elif estado_atual == ESTADO_JOGO:
                if evento.key == pygame.K_LEFT:
                    jogador_x_mudanca = -jogador_velocidade
                if evento.key == pygame.K_RIGHT:
                    jogador_x_mudanca = jogador_velocidade
                if evento.key == pygame.K_SPACE and tiro_estado == "pronto":
                    tiro_x = jogador_x
                    disparar_tiro(tiro_x, tiro_y)
            
            # Controles de game over
            elif estado_atual == ESTADO_GAME_OVER:
                if evento.key == pygame.K_r:
                    # Reiniciar jogo
                    estado_atual = ESTADO_JOGO
                    game_over = False
                    pontuacao = 0
                    nivel = 1
                    jogador_x = 370
                    inicializar_inimigos(nivel)
            
            # Controles de próximo nível
            elif estado_atual == ESTADO_PROXIMO_NIVEL:
                if evento.key == pygame.K_SPACE:
                    estado_atual = ESTADO_JOGO
                    inicializar_inimigos(nivel)
            
            # Controles de boss derrotado
            elif estado_atual == ESTADO_BOSS_DERROTADO:
                if evento.key == pygame.K_SPACE:
                    nivel += 1
                    estado_atual = ESTADO_PROXIMO_NIVEL
                
        # Verificar se uma tecla foi solta
        if evento.type == pygame.KEYUP:
            if estado_atual == ESTADO_JOGO:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                    jogador_x_mudanca = 0
    
    # Verificar clique do mouse no menu
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if estado_atual == ESTADO_MENU:
        # Verificar se clicou no botão de início (ajustado para o novo botão)
        if 300 <= mouse[0] <= 500 and 280 <= mouse[1] <= 340:
            if click[0] == 1:
                estado_atual = ESTADO_INSTRUCOES
    
    elif estado_atual == ESTADO_PAUSA:
        # Verificar se clicou no botão de menu principal
        if 300 <= mouse[0] <= 500 and 350 <= mouse[1] <= 400:
            if click[0] == 1:
                estado_atual = ESTADO_MENU
                # Reiniciar jogo ao voltar para o menu
                game_over = False
                pontuacao = 0
                nivel = 1
                jogador_x = 370
                inicializar_inimigos(nivel)
    
    # Lógica específica para cada estado
    if estado_atual == ESTADO_MENU:
        mostrar_menu()
    
    elif estado_atual == ESTADO_INSTRUCOES:
        mostrar_instrucoes()
    
    elif estado_atual == ESTADO_JOGO:
        # Cor de fundo
        tela.blit(fundo, (0, 0))
        
        # Atualizar posição do jogador
        jogador_x += jogador_x_mudanca
        
        # Manter jogador dentro dos limites
        if jogador_x <= 0:
            jogador_x = 0
        elif jogador_x >= 736:
            jogador_x = 736
        
        # Lógica do boss
        if boss_ativo:
            # Movimento do boss
            boss_x += boss_x_mudanca
            if boss_x <= 0:
                boss_x_mudanca = abs(boss_x_mudanca)
            elif boss_x >= largura - 128:
                boss_x_mudanca = -abs(boss_x_mudanca)
            
            # Tiros do boss
            boss_tiros_cooldown += 1
            if boss_tiros_cooldown >= 30:  # Atirar a cada meio segundo
                boss_tiros_cooldown = 0
                for i in range(max_tiros_boss):
                    if tiros_boss_estado[i] == "pronto":
                        disparar_tiro_boss(i, boss_x, boss_y)
                        break
            
            # Movimento dos tiros do boss
            for i in range(max_tiros_boss):
                if tiros_boss_estado[i] == "disparado":
                    tiros_boss_y[i] += tiros_boss_velocidade
                    tela.blit(tiros_boss_img, (tiros_boss_x[i], tiros_boss_y[i]))
                    
                    # Verificar se saiu da tela
                    if tiros_boss_y[i] > altura:
                        tiros_boss_estado[i] = "pronto"
                    
                    # Verificar colisão com jogador
                    if colisao_jogador(jogador_x, jogador_y, tiros_boss_x[i], tiros_boss_y[i]):
                        try:
                            som_explosao.play()
                        except:
                            pass
                        tiros_boss_estado[i] = "pronto"
                        game_over = True
                        estado_atual = ESTADO_GAME_OVER
            
            # Colisão do tiro do jogador com o boss
            if tiro_estado == "disparado":
                colisao_detectada = colisao_boss(boss_x, boss_y, tiro_x, tiro_y)
                if colisao_detectada:
                    try:
                        som_explosao.play()
                    except:
                        pass
                    # Criar explosão menor no boss
                    criar_explosao(tiro_x, tiro_y, LARANJA_NEON)
                    tiro_y = 480
                    tiro_estado = "pronto"
                    boss_vida -= 1
                    pontuacao += 2
                    
                    # Verificar se o boss foi derrotado
                    if boss_vida <= 0:
                        # Explosão maior quando o boss é derrotado
                        for j in range(3):
                            criar_explosao(boss_x + 64 + random.randint(-30, 30), 
                                         boss_y + 64 + random.randint(-30, 30), 
                                         random.choice([ROXO_NEON, LARANJA_NEON, AMARELO]))
                        pontuacao += 50  # Bônus por derrotar o boss
                        estado_atual = ESTADO_BOSS_DERROTADO
            
            # Desenhar boss e sua vida
            desenhar_boss(boss_x, boss_y)
            mostrar_vida_boss(texto_x, texto_y + 80)
            
        else:
            # Movimento dos inimigos normais
            inimigos_restantes = 0
            for i in range(num_inimigos):
                # Verificar se o inimigo está ativo
                if inimigo_y[i] < 1000:  # Se estiver na tela
                    inimigos_restantes += 1
                    
                    # Game Over
                    if inimigo_y[i] > 440 and not game_over:
                        for j in range(num_inimigos):
                            inimigo_y[j] = 2000  # Move todos os inimigos para fora da tela
                        game_over = True
                        estado_atual = ESTADO_GAME_OVER
                        break
                        
                    inimigo_x[i] += inimigo_x_mudanca[i]
                    if inimigo_x[i] <= 0:
                        inimigo_x_mudanca[i] = abs(inimigo_x_mudanca[i])
                        inimigo_y[i] += inimigo_y_mudanca[i]
                    elif inimigo_x[i] >= 736:
                        inimigo_x_mudanca[i] = -abs(inimigo_x_mudanca[i])
                        inimigo_y[i] += inimigo_y_mudanca[i]
                    
                    # Tiros dos inimigos
                    # Cada inimigo tem chance de atirar a cada frame
                    if random.random() < 0.005 * nivel:  # Aumenta a chance com o nível
                        for j in range(max_tiros_inimigos):
                            if tiros_inimigos_estado[j] == "pronto":
                                disparar_tiro_inimigo(j, inimigo_x[i], inimigo_y[i])
                                break
                        
                    # Colisão com tiro do jogador
                    colisao_detectada = colisao(inimigo_x[i], inimigo_y[i], tiro_x, tiro_y)
                    if colisao_detectada and tiro_estado == "disparado":
                        try:
                            som_explosao.play()
                        except:
                            pass
                        # Criar explosão de partículas
                        criar_explosao(inimigo_x[i] + 32, inimigo_y[i] + 32, VERMELHO_NEON)
                        tiro_y = 480
                        tiro_estado = "pronto"
                        pontuacao += 1
                        inimigo_y[i] = 2000  # Remove o inimigo (move para fora da tela)
                        
                    # Desenhar inimigo
                    inimigo(inimigo_x[i], inimigo_y[i], i)
            
            # Verificar se todos os inimigos foram eliminados
            if inimigos_restantes == 0 and not game_over:
                nivel += 1
                estado_atual = ESTADO_PROXIMO_NIVEL
                tempo_proximo_nivel = pygame.time.get_ticks()
                
            # Movimento dos tiros dos inimigos
            for i in range(max_tiros_inimigos):
                if tiros_inimigos_estado[i] == "disparado":
                    tiros_inimigos_y[i] += tiros_inimigos_velocidade
                    tela.blit(tiros_inimigos_img, (tiros_inimigos_x[i], tiros_inimigos_y[i]))
                    
                    # Verificar se saiu da tela
                    if tiros_inimigos_y[i] > altura:
                        tiros_inimigos_estado[i] = "pronto"
                    
                    # Verificar colisão com jogador
                    if colisao_jogador(jogador_x, jogador_y, tiros_inimigos_x[i], tiros_inimigos_y[i]):
                        try:
                            som_explosao.play()
                        except:
                            pass
                        tiros_inimigos_estado[i] = "pronto"
                        game_over = True
                        estado_atual = ESTADO_GAME_OVER
        
        # Movimento do tiro do jogador
        if tiro_y <= 0:
            tiro_y = 480
            tiro_estado = "pronto"
            
        if tiro_estado == "disparado":
            disparar_tiro(tiro_x, tiro_y)
            tiro_y -= tiro_y_mudanca
            
        # Desenhar jogador
        jogador(jogador_x, jogador_y)
        
        # Atualizar e desenhar partículas
        atualizar_particulas()
        
        # Mostrar pontuação e nível
        mostrar_pontuacao(texto_x, texto_y)
        mostrar_nivel(texto_x, texto_y + 40)
        
        # Mostrar dica de pausa futurista
        dica_pausa_sombra = fonte_pequena.render("[ P ] - PAUSA", True, AZUL_ESCURO)
        tela.blit(dica_pausa_sombra, (largura - 118, 12))
        dica_pausa = fonte_pequena.render("[ P ] - PAUSA", True, VERDE_NEON)
        tela.blit(dica_pausa, (largura - 120, 10))
    
    elif estado_atual == ESTADO_GAME_OVER:
        # Cor de fundo
        tela.blit(fundo, (0, 0))
        
        # Mostrar game over
        game_over_texto()
        
        # Informações com estilo tecnológico
        reiniciar_sombra = fonte.render("[ R ] - REINICIAR OPERAÇÃO", True, AZUL_ESCURO)
        tela.blit(reiniciar_sombra, (252, 352))
        reiniciar = fonte.render("[ R ] - REINICIAR OPERAÇÃO", True, VERDE_NEON)
        tela.blit(reiniciar, (250, 350))
        
        pontuacao_final_sombra = fonte.render(f"PONTUAÇÃO FINAL: {pontuacao}", True, AZUL_ESCURO)
        tela.blit(pontuacao_final_sombra, (252, 402))
        pontuacao_final = fonte.render(f"PONTUAÇÃO FINAL: {pontuacao}", True, AZUL_NEON)
        tela.blit(pontuacao_final, (250, 400))
        
        nivel_final_sombra = fonte.render(f"SETOR ALCANÇADO: {nivel}", True, AZUL_ESCURO)
        tela.blit(nivel_final_sombra, (252, 452))
        nivel_final = fonte.render(f"SETOR ALCANÇADO: {nivel}", True, AMARELO)
        tela.blit(nivel_final, (250, 450))
    
    elif estado_atual == ESTADO_PROXIMO_NIVEL:
        mostrar_proximo_nivel()
    
    elif estado_atual == ESTADO_PAUSA:
        # Mostrar tela de pausa sobre o jogo atual
        mostrar_pausa()
    
    elif estado_atual == ESTADO_BOSS_DERROTADO:
        mostrar_boss_derrotado()
    
    # Atualizar a tela
    pygame.display.update()

# Encerrar o pygame
pygame.quit()
