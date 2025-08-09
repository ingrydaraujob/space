# Configurações do jogo

# Configurações da tela
LARGURA = 800
ALTURA = 600
FPS = 60

# Cores básicas
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
CINZA = (100, 100, 100)
ROXO = (128, 0, 128)
LARANJA = (255, 165, 0)

# Cores espaciais
PRETO_ESPACIAL = (5, 10, 25)
AZUL_NEON = (0, 255, 255)
AZUL_ESCURO = (0, 50, 100)
VERDE_NEON = (57, 255, 20)
ROXO_NEON = (148, 0, 211)
ROSA_NEON = (255, 20, 147)
LARANJA_NEON = (255, 140, 0)
VERMELHO_NEON = (255, 0, 100)
BRANCO_AZULADO = (200, 220, 255)

# Estados do jogo
ESTADO_MENU = 0
ESTADO_INSTRUCOES = 1
ESTADO_JOGO = 2
ESTADO_GAME_OVER = 3
ESTADO_PROXIMO_NIVEL = 4
ESTADO_PAUSA = 5
ESTADO_BOSS_DERROTADO = 6

# Configurações do jogador
JOGADOR_VELOCIDADE = 5
JOGADOR_X_INICIAL = 370
JOGADOR_Y_INICIAL = 480

# Configurações dos tiros
TIRO_VELOCIDADE = 25          # Tiro do jogador mais rápido (era 15)
MAX_TIROS_INIMIGOS = 8        # Mais tiros dos inimigos (era 3)
MAX_TIROS_BOSS = 10           # Mais tiros do boss (era 5)
TIROS_INIMIGOS_VELOCIDADE = 12  # Tiros dos inimigos mais rápidos (era 5)
TIROS_BOSS_VELOCIDADE = 15      # Tiros do boss mais rápidos (era 7)

# Configurações dos inimigos
NUM_INIMIGOS_BASE = 6
MAX_INIMIGOS = 15

# Configurações do boss
BOSS_VIDA_BASE = 20
BOSS_VELOCIDADE = 3
BOSS_COOLDOWN_TIROS = 15       # Boss atira mais frequentemente (era 30)

# Configurações de partículas
PARTICULAS_POR_EXPLOSAO = 15
VIDA_PARTICULA_MIN = 20
VIDA_PARTICULA_MAX = 40
