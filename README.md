# Galaxy Defender - Operação Estelar

Um jogo espacial desenvolvido em Python com Pygame.

## Estrutura do Projeto

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

## Descrição dos Módulos

### `main.py`
- **Responsabilidade**: Coordenação geral do jogo
- **Conteúdo**:
  - Loop principal do jogo
  - Gerenciamento de eventos
  - Coordenação entre módulos
  - Renderização principal

### `constants.py`
- **Responsabilidade**: Configurações
- **Conteúdo**:
  - Dimensões da tela
  - Cores do jogo
  - Estados do jogo
  - Configurações de velocidade
  - Configurações de gameplay

### `game_design.py`
- **Responsabilidade**: Aspecto visual
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

##  Como Executar:

```bash
cd space
python main.py
```

##  Vantagens da Modularização

1. **Organização**: Cada arquivo tem uma responsabilidade específica
2. **Manutenibilidade**: Fácil localizar e modificar funcionalidades
3. **Reutilização**: Funções podem ser reutilizadas em outros projetos
4. **Colaboração**: Diferentes pessoas podem trabalhar em módulos diferentes
5. **Debugging**: Mais fácil encontrar e corrigir bugs
6. **Escalabilidade**: Fácil adicionar novas funcionalidades



