# Arquivo principal do jogo Galaxy Defender

import pygame
import sys
from constants import *
from game_design import *
from game_states import *
from game_logic import GameLogic

class Game:
    def __init__(self):
        # Inicializar pygame
        pygame.init()
        
        # Criar tela
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Galaxy Defender - Operação Estelar")
        
        # Criar ícone
        icone = pygame.Surface((32, 32))
        icone.fill(BRANCO)
        pygame.display.set_icon(icone)
        
        # Clock para FPS
        self.clock = pygame.time.Clock()
        
        # Estado do jogo
        self.estado_atual = ESTADO_MENU
        self.executando = True
        
        # Inicializar componentes
        self.game_logic = GameLogic()
        
        # Criar recursos visuais
        self.fundo = criar_fundo_espacial()
        self.jogador_img = criar_nave_jogador()
        self.boss_img = criar_boss()
        self.tiro_img = criar_tiro_jogador()
        self.tiros_inimigos_img = criar_tiro_inimigo()
        self.tiros_boss_img = criar_tiro_boss()
        
        # Inicializar fontes
        self.fonte, self.fonte_go, self.fonte_media, self.fonte_pequena, self.fonte_titulo = inicializar_fontes()
        
        # Variáveis de controle
        self.tempo_proximo_nivel = 0
        
        # Inicializar primeiro nível
        self.game_logic.inicializar_inimigos(self.game_logic.nivel)
    
    def processar_eventos(self):
        """Processar eventos do pygame"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.executando = False
            
            if evento.type == pygame.KEYDOWN:
                self._processar_tecla_pressionada(evento.key)
            
            if evento.type == pygame.KEYUP:
                self._processar_tecla_solta(evento.key)
        
        # Processar cliques do mouse
        self._processar_mouse()
    
    def _processar_tecla_pressionada(self, tecla):
        """Processar tecla pressionada"""
        # Tecla de pausa (funciona em qualquer estado do jogo)
        if tecla == pygame.K_p:
            if self.estado_atual == ESTADO_JOGO:
                self.estado_atual = ESTADO_PAUSA
            elif self.estado_atual == ESTADO_PAUSA:
                self.estado_atual = ESTADO_JOGO
        
        # Controles específicos por estado
        if self.estado_atual == ESTADO_MENU:
            if tecla == pygame.K_RETURN:
                self.estado_atual = ESTADO_INSTRUCOES
        
        elif self.estado_atual == ESTADO_INSTRUCOES:
            if tecla == pygame.K_r:
                self.estado_atual = ESTADO_JOGO
        
        elif self.estado_atual == ESTADO_JOGO:
            if tecla == pygame.K_LEFT:
                self.game_logic.jogador_x_mudanca = -JOGADOR_VELOCIDADE
            elif tecla == pygame.K_RIGHT:
                self.game_logic.jogador_x_mudanca = JOGADOR_VELOCIDADE
            elif tecla == pygame.K_SPACE:
                self.game_logic.disparar_tiro_jogador()
        
        elif self.estado_atual == ESTADO_GAME_OVER:
            if tecla == pygame.K_r:
                self.game_logic.reiniciar_jogo()
                self.estado_atual = ESTADO_JOGO
        
        elif self.estado_atual == ESTADO_PROXIMO_NIVEL:
            if tecla == pygame.K_SPACE:
                self.estado_atual = ESTADO_JOGO
                self.game_logic.inicializar_inimigos(self.game_logic.nivel)
        
        elif self.estado_atual == ESTADO_BOSS_DERROTADO:
            if tecla == pygame.K_SPACE:
                self.game_logic.nivel += 1
                self.estado_atual = ESTADO_PROXIMO_NIVEL
    
    def _processar_tecla_solta(self, tecla):
        """Processar tecla solta"""
        if self.estado_atual == ESTADO_JOGO:
            if tecla in [pygame.K_LEFT, pygame.K_RIGHT]:
                self.game_logic.jogador_x_mudanca = 0
    
    def _processar_mouse(self):
        """Processar cliques do mouse"""
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if self.estado_atual == ESTADO_MENU:
            # Botão de início
            if 300 <= mouse[0] <= 500 and 280 <= mouse[1] <= 340:
                if click[0] == 1:
                    self.estado_atual = ESTADO_INSTRUCOES
        
        elif self.estado_atual == ESTADO_PAUSA:
            # Botão de menu principal
            if 300 <= mouse[0] <= 500 and 350 <= mouse[1] <= 400:
                if click[0] == 1:
                    self.estado_atual = ESTADO_MENU
                    self.game_logic.reiniciar_jogo()
    
    def atualizar_jogo(self):
        """Atualizar lógica do jogo"""
        if self.estado_atual != ESTADO_JOGO:
            return
        
        # Atualizar jogador
        self.game_logic.atualizar_jogador()
        
        # Atualizar tiro do jogador
        self.game_logic.atualizar_tiro_jogador()
        
        if self.game_logic.boss_ativo:
            self._atualizar_boss()
        else:
            self._atualizar_inimigos()
        
        # Verificar game over
        if self.game_logic.game_over:
            self.estado_atual = ESTADO_GAME_OVER
    
    def _atualizar_boss(self):
        """Atualizar lógica do boss"""
        self.game_logic.atualizar_boss()
        self.game_logic.atualizar_tiros_boss()
        
        # Verificar colisões
        if self.game_logic.verificar_colisoes_boss():
            self.estado_atual = ESTADO_BOSS_DERROTADO
    
    def _atualizar_inimigos(self):
        """Atualizar lógica dos inimigos"""
        inimigos_restantes = self.game_logic.atualizar_inimigos()
        self.game_logic.atualizar_tiros_inimigos()
        
        # Verificar colisões
        self.game_logic.verificar_colisoes_inimigos()
        
        # Verificar se todos os inimigos foram eliminados
        if inimigos_restantes == 0 and not self.game_logic.game_over:
            self.game_logic.nivel += 1
            self.estado_atual = ESTADO_PROXIMO_NIVEL
    
    def renderizar(self):
        """Renderizar o jogo"""
        if self.estado_atual == ESTADO_MENU:
            mostrar_menu(self.tela, self.fundo, self.fonte_go, self.fonte_media, self.fonte_pequena)
        
        elif self.estado_atual == ESTADO_INSTRUCOES:
            mostrar_instrucoes(self.tela, self.fundo, self.fonte_media, self.fonte_pequena)
        
        elif self.estado_atual == ESTADO_JOGO:
            self._renderizar_jogo()
        
        elif self.estado_atual == ESTADO_GAME_OVER:
            mostrar_game_over(self.tela, self.fundo, self.fonte_go, self.fonte, 
                            self.game_logic.pontuacao, self.game_logic.nivel)
        
        elif self.estado_atual == ESTADO_PROXIMO_NIVEL:
            mostrar_proximo_nivel(self.tela, self.fundo, self.fonte_media, 
                                self.fonte_pequena, self.game_logic.nivel)
        
        elif self.estado_atual == ESTADO_PAUSA:
            mostrar_pausa(self.tela, self.fonte_go, self.fonte_media, self.fonte_pequena)
        
        elif self.estado_atual == ESTADO_BOSS_DERROTADO:
            mostrar_boss_derrotado(self.tela, self.fundo, self.fonte_go, self.fonte_media, 
                                 self.fonte_pequena, self.game_logic.boss_vida)
        
        pygame.display.update()
    
    def _renderizar_jogo(self):
        """Renderizar a tela de jogo"""
        # Fundo
        self.tela.blit(self.fundo, (0, 0))
        
        # Desenhar jogador
        self.tela.blit(self.jogador_img, (self.game_logic.jogador_x, self.game_logic.jogador_y))
        
        # Desenhar tiro do jogador
        if self.game_logic.tiro_estado == "disparado":
            self.tela.blit(self.tiro_img, (self.game_logic.tiro_x + 28, self.game_logic.tiro_y + 10))
        
        if self.game_logic.boss_ativo:
            self._desenhar_boss()
        else:
            self._desenhar_inimigos()
        
        # Desenhar tiros dos inimigos
        self._desenhar_tiros_inimigos()
        
        # Desenhar tiros do boss
        self._desenhar_tiros_boss()
        
        # Atualizar e desenhar partículas
        atualizar_particulas(self.game_logic.particulas, self.tela)
        
        # Interface
        mostrar_pontuacao(self.tela, self.fonte, self.game_logic.pontuacao, 10, 10)
        mostrar_nivel(self.tela, self.fonte, self.game_logic.nivel, 10, 50)
        mostrar_dica_pausa(self.tela, self.fonte_pequena)
    
    def _desenhar_boss(self):
        """Desenhar o boss"""
        self.tela.blit(self.boss_img, (self.game_logic.boss_x, self.game_logic.boss_y))
        mostrar_vida_boss(self.tela, self.fonte, self.fonte_pequena, 
                         self.game_logic.boss_vida, self.game_logic.nivel, 10, 90)
    
    def _desenhar_inimigos(self):
        """Desenhar os inimigos"""
        for i in range(self.game_logic.num_inimigos):
            if self.game_logic.inimigo_y[i] < 1000:  # Se estiver na tela
                self.tela.blit(self.game_logic.inimigo_img[i], 
                             (self.game_logic.inimigo_x[i], self.game_logic.inimigo_y[i]))
    
    def _desenhar_tiros_inimigos(self):
        """Desenhar tiros dos inimigos"""
        for i in range(MAX_TIROS_INIMIGOS):
            if self.game_logic.tiros_inimigos_estado[i] == "disparado":
                self.tela.blit(self.tiros_inimigos_img, 
                             (self.game_logic.tiros_inimigos_x[i], self.game_logic.tiros_inimigos_y[i]))
    
    def _desenhar_tiros_boss(self):
        """Desenhar tiros do boss"""
        for i in range(MAX_TIROS_BOSS):
            if self.game_logic.tiros_boss_estado[i] == "disparado":
                self.tela.blit(self.tiros_boss_img, 
                             (self.game_logic.tiros_boss_x[i], self.game_logic.tiros_boss_y[i]))
    
    def executar(self):
        """Loop principal do jogo"""
        while self.executando:
            self.clock.tick(FPS)
            
            self.processar_eventos()
            self.atualizar_jogo()
            self.renderizar()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    jogo = Game()
    jogo.executar()
