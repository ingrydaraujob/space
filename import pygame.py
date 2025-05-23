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

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
CINZA = (100, 100, 100)
ROXO = (128, 0, 128)
LARANJA = (255, 165, 0)

# Fundo
fundo = pygame.Surface((largura, altura))
fundo.fill(PRETO)
for i in range(100):
    x = random.randint(0, largura)
    y = random.randint(0, altura)
    tamanho = random.randint(1, 3)
    pygame.draw.circle(fundo, BRANCO, (x, y), tamanho)

# Sons
try:
    mixer.music.load('background.wav')
    mixer.music.play(-1)
    som_tiro = mixer.Sound('laser.wav')
    som_explosao = mixer.Sound('explosion.wav')
except:
    print("Arquivos de som não encontrados. O jogo funcionará sem áudio.")

# Jogador
jogador_img = pygame.Surface((64, 64), pygame.SRCALPHA)
pygame.draw.polygon(jogador_img, AZUL, [(32, 0), (0, 64), (64, 64)])
pygame.draw.polygon(jogador_img, BRANCO, [(32, 10), (10, 54), (54, 54)], 2)
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

# Boss
boss_img = pygame.Surface((128, 128), pygame.SRCALPHA)
pygame.draw.circle(boss_img, ROXO, (64, 64), 50)
pygame.draw.circle(boss_img, VERMELHO, (64, 64), 55, 3)
pygame.draw.circle(boss_img, LARANJA, (64, 64), 60, 2)
boss_x = 336  # Centralizado (800 - 128) / 2
boss_y = 100
boss_x_mudanca = 3
boss_vida = 20  # Boss precisa de vários tiros para ser destruído
boss_ativo = False
boss_tiros_cooldown = 0

# Tiros dos inimigos
tiros_inimigos_img = pygame.Surface((8, 16), pygame.SRCALPHA)
pygame.draw.rect(tiros_inimigos_img, VERMELHO, (0, 0, 8, 16))
tiros_inimigos_x = []
tiros_inimigos_y = []
tiros_inimigos_velocidade = 5
tiros_inimigos_estado = []
tiros_inimigos_cooldown = []
max_tiros_inimigos = 3

# Tiros do boss
tiros_boss_img = pygame.Surface((12, 24), pygame.SRCALPHA)
pygame.draw.rect(tiros_boss_img, LARANJA, (0, 0, 12, 24))
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
        # Criar imagem do inimigo
        img = pygame.Surface((64, 64), pygame.SRCALPHA)
        cor = (random.randint(150, 255), random.randint(0, 100), random.randint(0, 100))
        pygame.draw.circle(img, cor, (32, 32), 20)
        pygame.draw.circle(img, VERMELHO, (32, 32), 25, 2)
        
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

# Tiro do jogador
tiro_img = pygame.Surface((8, 16), pygame.SRCALPHA)
pygame.draw.rect(tiro_img, VERDE, (0, 0, 8, 16))
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

# Texto de Game Over
fonte_go = pygame.font.SysFont('arial', 64)
fonte_media = pygame.font.SysFont('arial', 36)
fonte_pequena = pygame.font.SysFont('arial', 24)

# Estados do jogo
ESTADO_MENU = 0
ESTADO_INSTRUCOES = 1
ESTADO_JOGO = 2
ESTADO_GAME_OVER = 3
ESTADO_PROXIMO_NIVEL = 4
ESTADO_PAUSA = 5  # Estado para pausa
ESTADO_BOSS_DERROTADO = 6  # Novo estado para quando o boss é derrotado
estado_atual = ESTADO_MENU

# Função para mostrar pontuação
def mostrar_pontuacao(x, y):
    texto = fonte.render(f"Pontuação: {pontuacao}", True, BRANCO)
    tela.blit(texto, (x, y))

# Função para mostrar nível
def mostrar_nivel(x, y):
    texto = fonte.render(f"Nível: {nivel}", True, BRANCO)
    tela.blit(texto, (x, y))

# Função para mostrar vida do boss
def mostrar_vida_boss(x, y):
    texto = fonte.render(f"Vida do Boss: {boss_vida}", True, VERMELHO)
    tela.blit(texto, (x, y))

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

# Função para mostrar game over
def game_over_texto():
    texto_go = fonte_go.render("GAME OVER", True, VERMELHO)
    tela.blit(texto_go, (200, 250))

# Função para mostrar tela de menu
def mostrar_menu():
    tela.blit(fundo, (0, 0))
    
    # Título
    titulo = fonte_go.render("SPACE SHOOTER", True, AZUL)
    tela.blit(titulo, (150, 150))
    
    # Botão de início
    pygame.draw.rect(tela, AZUL, (300, 300, 200, 50))
    pygame.draw.rect(tela, BRANCO, (300, 300, 200, 50), 2)
    texto_botao = fonte_media.render("Começar Jogo", True, BRANCO)
    tela.blit(texto_botao, (310, 310))
    
    # Versão
    versao = fonte_pequena.render("Versão 3.0", True, BRANCO)
    tela.blit(versao, (10, altura - 30))

# Função para mostrar instruções
def mostrar_instrucoes():
    tela.blit(fundo, (0, 0))
    
    # Título
    titulo = fonte_media.render("INSTRUÇÕES", True, AMARELO)
    tela.blit(titulo, (300, 100))
    
    # Instruções
    instrucao1 = fonte_pequena.render("Use as setas ESQUERDA e DIREITA para mover a nave espacial.", True, BRANCO)
    instrucao2 = fonte_pequena.render("Pressione ESPAÇO para atirar contra os inimigos.", True, BRANCO)
    instrucao3 = fonte_pequena.render("Destrua todos os inimigos para avançar para o próximo nível.", True, BRANCO)
    instrucao4 = fonte_pequena.render("A cada 3 níveis, você enfrentará um poderoso BOSS!", True, VERMELHO)
    instrucao5 = fonte_pequena.render("Cuidado com os tiros dos inimigos!", True, BRANCO)
    instrucao6 = fonte_pequena.render("Pressione P para pausar o jogo a qualquer momento.", True, BRANCO)
    instrucao7 = fonte_pequena.render("Pressione R para começar o jogo", True, AMARELO)
    
    tela.blit(instrucao1, (100, 180))
    tela.blit(instrucao2, (100, 220))
    tela.blit(instrucao3, (100, 260))
    tela.blit(instrucao4, (100, 300))
    tela.blit(instrucao5, (100, 340))
    tela.blit(instrucao6, (100, 380))
    tela.blit(instrucao7, (100, 450))

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
        # Verificar se clicou no botão de início
        if 300 <= mouse[0] <= 500 and 300 <= mouse[1] <= 350:
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
                    tiro_y = 480
                    tiro_estado = "pronto"
                    boss_vida -= 1
                    pontuacao += 2
                    
                    # Verificar se o boss foi derrotado
                    if boss_vida <= 0:
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
        
        # Mostrar pontuação e nível
        mostrar_pontuacao(texto_x, texto_y)
        mostrar_nivel(texto_x, texto_y + 40)
        
        # Mostrar dica de pausa
        dica_pausa = fonte_pequena.render("P = Pausar", True, BRANCO)
        tela.blit(dica_pausa, (largura - 120, 10))
    
    elif estado_atual == ESTADO_GAME_OVER:
        # Cor de fundo
        tela.blit(fundo, (0, 0))
        
        # Mostrar game over
        game_over_texto()
        reiniciar = fonte.render("Pressione R para reiniciar", True, BRANCO)
        pontuacao_final = fonte.render(f"Pontuação final: {pontuacao}", True, BRANCO)
        nivel_final = fonte.render(f"Nível alcançado: {nivel}", True, BRANCO)
        
        tela.blit(reiniciar, (250, 350))
        tela.blit(pontuacao_final, (250, 400))
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
