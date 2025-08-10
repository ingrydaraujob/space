# interfaces do jogo

import pygame
import random
from constants import *

def mostrar_pontuacao(tela, fonte, pontuacao, x, y):
    """Mostrar pontuação"""
    texto_sombra = fonte.render(f"PONTUAÇÃO: {pontuacao}", True, AZUL_ESCURO)
    tela.blit(texto_sombra, (x + 2, y + 2))
    texto = fonte.render(f"PONTUAÇÃO: {pontuacao}", True, DESTAQUE_AZUL)
    tela.blit(texto, (x, y))

def mostrar_nivel(tela, fonte, nivel, x, y):
    """Mostrar nível"""
    texto_sombra = fonte.render(f"NÍVEL: {nivel}", True, AZUL_ESCURO)
    tela.blit(texto_sombra, (x + 2, y + 2))
    texto = fonte.render(f"NÍVEL: {nivel}", True, DESTAQUE_VERDE)
    tela.blit(texto, (x, y))

def mostrar_vida_boss(tela, fonte, fonte_pequena, boss_vida, nivel, x, y):
    """Mostrar vida do boss """
    texto_sombra = fonte.render("ENERGIA DO BOSS:", True, (100, 0, 0))
    tela.blit(texto_sombra, (x + 2, y + 2))
    texto = fonte.render("ENERGIA DO BOSS:", True, DESTAQUE_VERMELHO)
    tela.blit(texto, (x, y))
    
    # Barra de energia
    barra_largura = 200
    barra_altura = 20
    vida_maxima = BOSS_VIDA_BASE + (nivel // 3) * 5
    vida_percentual = boss_vida / vida_maxima
    
    # Fundo da barra
    pygame.draw.rect(tela, CINZA_ESCURO, (x, y + 30, barra_largura, barra_altura))
    pygame.draw.rect(tela, BRANCO_SUAVE, (x, y + 30, barra_largura, barra_altura), 2)
    
    # Barra de vida
    cor_vida = DESTAQUE_VERMELHO if vida_percentual < 0.3 else DESTAQUE_LARANJA if vida_percentual < 0.6 else DESTAQUE_VERDE
    largura_vida = int(barra_largura * vida_percentual)
    if largura_vida > 0:
        pygame.draw.rect(tela, cor_vida, (x, y + 30, largura_vida, barra_altura))
    
    # Texto da vida
    texto_vida = fonte_pequena.render(f"{boss_vida}/{vida_maxima}", True, BRANCO_SUAVE)
    tela.blit(texto_vida, (x + barra_largura + 10, y + 32))

def mostrar_menu(tela, fundo, fonte_go, fonte_media, fonte_pequena):
    """Mostrar tela de menu """
    tela.blit(fundo, (0, 0))
    
    centro_x = LARGURA // 2
    
    # Título centralizado
    titulo = fonte_go.render("GALAXY DEFENDER", True, DESTAQUE_AZUL)
    rect_titulo = titulo.get_rect(center=(centro_x, 150))
    tela.blit(titulo, rect_titulo)
    
    # Subtítulo centralizado
    subtitulo = fonte_media.render("- OPERAÇÃO ESTELAR -", True, DESTAQUE_VERDE)
    rect_subtitulo = subtitulo.get_rect(center=(centro_x, 200))
    tela.blit(subtitulo, rect_subtitulo)
    
    # Botão de início centralizado
    botao_rect = pygame.Rect(centro_x - 100, 280, 200, 60)
    
    # Efeito de brilho no botão
    pygame.draw.rect(tela, AZUL_ESCURO, (botao_rect.x + 3, botao_rect.y + 3, botao_rect.width, botao_rect.height))
    pygame.draw.rect(tela, AZUL_SUAVE, botao_rect)
    pygame.draw.rect(tela, BRANCO_SUAVE, botao_rect, 3)
    
    # Detalhes no botão
    pygame.draw.line(tela, DESTAQUE_AZUL, (botao_rect.x + 10, botao_rect.y + 10), (botao_rect.x + 30, botao_rect.y + 10), 2)
    pygame.draw.line(tela, DESTAQUE_AZUL, (botao_rect.x + botao_rect.width - 30, botao_rect.y + 10), (botao_rect.x + botao_rect.width - 10, botao_rect.y + 10), 2)
    pygame.draw.line(tela, DESTAQUE_AZUL, (botao_rect.x + 10, botao_rect.y + botao_rect.height - 10), (botao_rect.x + 30, botao_rect.y + botao_rect.height - 10), 2)
    pygame.draw.line(tela, DESTAQUE_AZUL, (botao_rect.x + botao_rect.width - 30, botao_rect.y + botao_rect.height - 10), (botao_rect.x + botao_rect.width - 10, botao_rect.y + botao_rect.height - 10), 2)
    
    texto_botao = fonte_media.render("INICIAR MISSÃO", True, BRANCO_SUAVE)
    texto_rect = texto_botao.get_rect(center=botao_rect.center)
    tela.blit(texto_botao, texto_rect)
    
    # Informações adicionais centralizadas
    info1 = fonte_pequena.render(">> SISTEMA DE DEFESA PLANETÁRIA ATIVO <<", True, DESTAQUE_VERDE)
    rect_info1 = info1.get_rect(center=(centro_x, 380))
    tela.blit(info1, rect_info1)
    
    info2 = fonte_pequena.render("STATUS: AGUARDANDO COMANDOS DO PILOTO", True, DESTAQUE_LARANJA)
    rect_info2 = info2.get_rect(center=(centro_x, 400))
    tela.blit(info2, rect_info2)
    
    # Versão no canto
    versao = fonte_pequena.render("VERSÃO 4.0 - QUANTUM EDITION", True, ROXO_SUAVE)
    tela.blit(versao, (10, ALTURA - 30))

def mostrar_instrucoes(tela, fundo, fonte_media, fonte_pequena):
    """Mostrar instruções"""
    tela.blit(fundo, (0, 0))
    
    # Título
    titulo_sombra = fonte_media.render("BRIEFING DA MISSÃO", True, AZUL_ESCURO)
    tela.blit(titulo_sombra, (302, 102))
    titulo = fonte_media.render("BRIEFING DA MISSÃO", True, AMARELO)
    tela.blit(titulo, (300, 100))
    
    # Linha decorativa
    pygame.draw.line(tela, DESTAQUE_AZUL, (100, 130), (700, 130), 2)
    
    # Instruções com cores 
    instrucoes = [
        (">> CONTROLES DA NAVE:", DESTAQUE_VERDE),
        ("   ← → : Movimentação lateral", BRANCO_SUAVE),
        ("   ESPAÇO : Disparar lasers", BRANCO_SUAVE),
        ("", BRANCO_SUAVE),
        (">> OBJETIVOS DA MISSÃO:", DESTAQUE_LARANJA),
        ("   • Eliminar todas as ameaças hostis", BRANCO_SUAVE),
        ("   • Avançar através dos setores galácticos", BRANCO_SUAVE),
        ("   • Enfrentar comandantes inimigos a cada 3 setores", DESTAQUE_VERMELHO),
        ("", BRANCO_SUAVE),
        (">> SISTEMAS AUXILIARES:", ROXO_SUAVE),
        ("   P : Ativar modo de pausa de emergência", BRANCO_SUAVE),
        ("", BRANCO_SUAVE),
        ("⚠ CUIDADO: Evite projéteis hostis!", DESTAQUE_VERMELHO),
        ("", BRANCO_SUAVE),
        ("[ R ] - INICIAR OPERAÇÃO", DESTAQUE_VERDE)
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
    """Mostrar tela de game over """
    tela.blit(fundo, (0, 0))
    
    centro_x = LARGURA // 2
    
    # Efeito de glitch no texto
    for i in range(3):
        offset_x = random.randint(-2, 2)
        offset_y = random.randint(-2, 2)
        cor_glitch = random.choice([DESTAQUE_VERMELHO, DESTAQUE_AZUL, DESTAQUE_VERDE])
        texto_glitch = fonte_go.render("MISSÃO FALHOU", True, cor_glitch)
        rect_glitch = texto_glitch.get_rect(center=(centro_x + offset_x, 250 + offset_y))
        tela.blit(texto_glitch, rect_glitch)
    
    # Texto principal
    texto_go = fonte_go.render("MISSÃO FALHOU", True, DESTAQUE_VERMELHO)
    rect_go = texto_go.get_rect(center=(centro_x, 250))
    tela.blit(texto_go, rect_go)
    
    # Informações centralizadas
    pontuacao_final = fonte.render(f"PONTUAÇÃO FINAL: {pontuacao}", True, DESTAQUE_AZUL)
    rect_pontuacao = pontuacao_final.get_rect(center=(centro_x, 320))
    tela.blit(pontuacao_final, rect_pontuacao)
    
    nivel_final = fonte.render(f"SETOR ALCANÇADO: {nivel}", True, DESTAQUE_LARANJA)
    rect_nivel = nivel_final.get_rect(center=(centro_x, 360))
    tela.blit(nivel_final, rect_nivel)
    
    reiniciar = fonte.render("[ R ] - REINICIAR OPERAÇÃO", True, DESTAQUE_VERDE)
    rect_reiniciar = reiniciar.get_rect(center=(centro_x, 420))
    tela.blit(reiniciar, rect_reiniciar)

def mostrar_proximo_nivel(tela, fundo, fonte_media, fonte_pequena, nivel):
    """Mostrar tela de próximo nível"""
    tela.blit(fundo, (0, 0))
    
    # Centralizar os textos
    centro_x = LARGURA // 2
    
    # Mensagem de nível concluído
    texto_nivel = fonte_media.render(f"NÍVEL {nivel-1} CONCLUÍDO!", True, DESTAQUE_VERDE)
    rect_nivel = texto_nivel.get_rect(center=(centro_x, 200))
    tela.blit(texto_nivel, rect_nivel)
    
    # Próximo nível
    if nivel % 3 == 0:
        texto_proximo = fonte_media.render(f"PREPARANDO NÍVEL {nivel}...", True, DESTAQUE_LARANJA)
        texto_boss = fonte_pequena.render("BOSS CHEGANDO!", True, DESTAQUE_VERMELHO)
        
        rect_proximo = texto_proximo.get_rect(center=(centro_x, 280))
        tela.blit(texto_proximo, rect_proximo)
        
        rect_boss = texto_boss.get_rect(center=(centro_x, 320))
        tela.blit(texto_boss, rect_boss)
    else:
        texto_proximo = fonte_media.render(f"PREPARANDO NÍVEL {nivel}...", True, DESTAQUE_LARANJA)
        rect_proximo = texto_proximo.get_rect(center=(centro_x, 300))
        tela.blit(texto_proximo, rect_proximo)
    
    # Instrução para continuar
    texto_continuar = fonte_pequena.render("Pressione ESPAÇO para continuar", True, BRANCO_SUAVE)
    rect_continuar = texto_continuar.get_rect(center=(centro_x, 400))
    tela.blit(texto_continuar, rect_continuar)
    
    

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
    dica_pausa = fonte_pequena.render("[ P ] - PAUSA", True, DESTAQUE_VERDE)
    tela.blit(dica_pausa, (LARGURA - 120, 10))
