# game_states.py - Gerenciamento de estados e interfaces do jogo

import pygame
import random
from constants import *

def mostrar_pontuacao(tela, fonte, pontuacao, x, y):
    """Mostrar pontuação com efeito tecnológico"""
    texto_sombra = fonte.render(f"PONTUAÇÃO: {pontuacao}", True, AZUL_ESCURO)
    tela.blit(texto_sombra, (x + 2, y + 2))
    texto = fonte.render(f"PONTUAÇÃO: {pontuacao}", True, AZUL_NEON)
    tela.blit(texto, (x, y))

def mostrar_nivel(tela, fonte, nivel, x, y):
    """Mostrar nível com efeito tecnológico"""
    texto_sombra = fonte.render(f"NÍVEL: {nivel}", True, AZUL_ESCURO)
    tela.blit(texto_sombra, (x + 2, y + 2))
    texto = fonte.render(f"NÍVEL: {nivel}", True, VERDE_NEON)
    tela.blit(texto, (x, y))

def mostrar_vida_boss(tela, fonte, fonte_pequena, boss_vida, nivel, x, y):
    """Mostrar vida do boss com barra de energia"""
    texto_sombra = fonte.render("ENERGIA DO BOSS:", True, (100, 0, 0))
    tela.blit(texto_sombra, (x + 2, y + 2))
    texto = fonte.render("ENERGIA DO BOSS:", True, VERMELHO_NEON)
    tela.blit(texto, (x, y))
    
    # Barra de energia
    barra_largura = 200
    barra_altura = 20
    vida_maxima = BOSS_VIDA_BASE + (nivel // 3) * 5
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

def mostrar_menu(tela, fundo, fonte_go, fonte_media, fonte_pequena):
    """Mostrar tela de menu futurista"""
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
    tela.blit(versao, (10, ALTURA - 30))

def mostrar_instrucoes(tela, fundo, fonte_media, fonte_pequena):
    """Mostrar instruções futuristas"""
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
                texto_sombra = fonte_pequena.render(texto, True, AZUL_ESCURO)
                tela.blit(texto_sombra, (102, y_pos + 2))
            rendered_text = fonte_pequena.render(texto, True, cor)
            tela.blit(rendered_text, (100, y_pos))
        y_pos += 25

def mostrar_game_over(tela, fundo, fonte_go, fonte, pontuacao, nivel):
    """Mostrar tela de game over futurista"""
    tela.blit(fundo, (0, 0))
    
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

def mostrar_proximo_nivel(tela, fundo, fonte_media, fonte_pequena, nivel):
    """Mostrar tela de próximo nível"""
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

def mostrar_boss_derrotado(tela, fundo, fonte_go, fonte_media, fonte_pequena, boss_vida):
    """Mostrar tela de boss derrotado"""
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

def mostrar_pausa(tela, fonte_go, fonte_media, fonte_pequena):
    """Mostrar tela de pausa"""
    # Criar superfície semi-transparente
    pausa_overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    pausa_overlay.fill((0, 0, 0, 128))
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

def mostrar_dica_pausa(tela, fonte_pequena):
    """Mostrar dica de pausa"""
    dica_pausa_sombra = fonte_pequena.render("[ P ] - PAUSA", True, AZUL_ESCURO)
    tela.blit(dica_pausa_sombra, (LARGURA - 118, 12))
    dica_pausa = fonte_pequena.render("[ P ] - PAUSA", True, VERDE_NEON)
    tela.blit(dica_pausa, (LARGURA - 120, 10))
