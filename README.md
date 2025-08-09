# Galaxy Defender - Operação Estelar

Um jogo espacial desenvolvido em Python com Pygame, agora com código modularizado e design tecnológico avançado.

## 🚀 Estrutura do Projeto

```
space/
├── main.py              # Arquivo principal - coordena todo o jogo
├── constants.py         # Constantes e configurações do jogo
├── game_design.py       # Design visual, sprites e efeitos
├── game_states.py       # Gerenciamento de estados e interfaces
├── game_logic.py        # Lógica principal do jogo
├── import pygame.py     # Arquivo original (pode ser removido)
└── README.md           # Este arquivo
```

## 📁 Descrição dos Módulos

### `main.py`
- **Responsabilidade**: Coordenação geral do jogo
- **Conteúdo**:
  - Loop principal do jogo
  - Gerenciamento de eventos
  - Coordenação entre módulos
  - Renderização principal

### `constants.py`
- **Responsabilidade**: Configurações e constantes
- **Conteúdo**:
  - Dimensões da tela
  - Cores do jogo
  - Estados do jogo
  - Configurações de velocidade
  - Configurações de gameplay

### `game_design.py`
- **Responsabilidade**: Todo o aspecto visual
- **Conteúdo**:
  - Criação de sprites (nave, inimigos, boss, tiros)
  - Sistema de partículas
  - Efeitos visuais
  - Criação do fundo espacial
  - Fontes do jogo

### `game_states.py`
- **Responsabilidade**: Interface e estados
- **Conteúdo**:
  - Tela de menu
  - Tela de instruções
  - Tela de game over
  - Tela de pausa
  - Interface do jogo (pontuação, vida do boss)

### `game_logic.py`
- **Responsabilidade**: Lógica do jogo
- **Conteúdo**:
  - Movimento de objetos
  - Sistema de colisões
  - Gerenciamento de inimigos e boss
  - Sistema de tiros
  - Controle de estado do jogo

## 🎮 Como Executar

```bash
cd space
python main.py
```

## 🎯 Vantagens da Modularização

1. **Organização**: Cada arquivo tem uma responsabilidade específica
2. **Manutenibilidade**: Fácil localizar e modificar funcionalidades
3. **Reutilização**: Funções podem ser reutilizadas em outros projetos
4. **Colaboração**: Diferentes pessoas podem trabalhar em módulos diferentes
5. **Debugging**: Mais fácil encontrar e corrigir bugs
6. **Escalabilidade**: Fácil adicionar novas funcionalidades

## 🛠️ Próximos Passos para Melhorias

### Para adicionar novos recursos:
- **Novos inimigos**: Modificar `game_design.py` (função `criar_inimigo`)
- **Novas armas**: Adicionar em `game_design.py` e `game_logic.py`
- **Novos efeitos**: Expandir sistema de partículas em `game_design.py`
- **Novas telas**: Adicionar funções em `game_states.py`

### Para ajustar jogabilidade:
- **Velocidades**: Modificar `constants.py`
- **Dificuldade**: Ajustar em `game_logic.py`
- **Cores e visual**: Modificar `constants.py` e `game_design.py`

## 📝 Exemplo de Como Adicionar um Novo Inimigo

1. **Em `game_design.py`**: Adicionar novo tipo na função `criar_inimigo()`
2. **Em `game_logic.py`**: Ajustar lógica se necessário
3. **Em `constants.py`**: Adicionar configurações específicas

## 🎨 Personalização Visual

Para mudar o visual do jogo, edite principalmente:
- `constants.py` - Para cores
- `game_design.py` - Para sprites e efeitos
- `game_states.py` - Para interface

## 🔧 Configurações

Todas as configurações principais estão em `constants.py`:
- Tamanho da tela
- Velocidades
- Cores
- Configurações de gameplay

Esta estrutura modular torna o jogo muito mais profissional e fácil de manter!

