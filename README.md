# \# Deserto Assombrado

# 

# Este é um simples jogo de sobrevivência 2D de arena, desenvolvido em Python utilizando a biblioteca \*\*Pygame Zero\*\* (`pgzero`).

# 

# A ideia central do jogo é controlar um herói em um mapa fixo, sobreviver o máximo de tempo possível e derrotar ondas de fantasmas que patrulham a área. O jogador ganha pontos por cada fantasma derrotado. O jogo termina se um fantasma conseguir tocar no herói.

# 

# ---

# 

# \## 🎮 Como Jogar

# 

# O jogo é controlado de forma simples:

# 

# \* \*\*Movimentação:\*\* Use as \*\*Setas Direcionais\*\* (Cima, Baixo, Esquerda, Direita) para mover o herói pelo mapa.

# \* \*\*Ataque:\*\* Pressione a \*\*Barra de Espaço\*\* para desferir um ataque. O ataque é uma pequena área à frente do personagem que destrói os fantasmas ao contato.

# \* \*\*Objetivo:\*\* Sobreviva! Derrote o máximo de fantasmas que puder para aumentar sua pontuação (`PONTOS`).

# \* \*\*Game Over:\*\* Se qualquer fantasma tocar no seu herói, o jogo acaba.

# 

# ---

# 

# \## ✨ Funcionalidades

# 

# \* \*\*Menu Principal:\*\* O jogo inicia com um menu que inclui opções para "Jogar", "Ligar/Desligar Música" e "Sair".

# \* \*\*Sistema de Pontuação:\*\* Você ganha +1 ponto por cada fantasma derrotado.

# \* \*\*Cronômetro de Sobrevivência:\*\* Um contador de tempo (`TEMPO`) mostra quantos segundos você sobreviveu.

# \* \*\*Animações de Sprite:\*\*

# &nbsp;   \* O \*\*Herói\*\* possui animações para ficar parado (idle), andar (em 4 direções) e atacar (em 4 direções).

# &nbsp;   \* Os \*\*Inimigos\*\* (fantasmas) têm uma animação sutil de "flutuação".

# \* \*\*Tela de Game Over:\*\* Ao perder, uma tela de "FIM DE JOGO" é exibida, mostrando sua pontuação final. Você pode pressionar `ENTER` para retornar ao menu principal.

# \* \*\*Controle de Som:\*\* A música do jogo pode ser ligada ou desligada através do menu.

# 

# ---

# 

# \## 🛠️ Estrutura do Código

# 

# A lógica do jogo é dividida em algumas partes principais:

# 

# \### Classes Principais

# 

# 1\.  \*\*`Hero`\*\*:

# &nbsp;   \* Controla toda a lógica do jogador.

# &nbsp;   \* Gerencia a entrada do teclado para movimento (`update`).

# &nbsp;   \* Controla a animação do sprite (parado, andando, atacando) com base nas ações do jogador (`animate`).

# &nbsp;   \* Gerencia os \*cooldowns\* (tempos de espera) do ataque.

# 

# 2\.  \*\*`Enemy`\*\*:

# &nbsp;   \* Define o comportamento dos fantasmas.

# &nbsp;   \* Cada fantasma patrulha uma área aleatória (`pick\_target`) em uma velocidade variável.

# &nbsp;   \* Possui uma lógica de animação simples para fazê-lo flutuar.

# 

# 3\.  \*\*`Attack`\*\*:

# &nbsp;   \* Esta classe representa o "ataque" do jogador.

# &nbsp;   \* Quando o jogador ataca, um objeto `Attack` é criado.

# &nbsp;   \* Ele existe por um curto período (`lifetime`) e é invisível (no código, ele é desenhado como um quadrado amarelo para debug, mas a intenção é ser a "hitbox" da espada).

# &nbsp;   \* Se colidir com um `Enemy`, o inimigo é removido.

# 

# \### Gerenciamento de Estado

# 

# O fluxo do jogo é controlado por três variáveis booleanas principais:

# \* `menu`: Se `True`, mostra o menu principal.

# \* `running`: Se `True`, o jogo está em andamento.

# \* `game\_over`: Se `True`, mostra a tela de fim de jogo.

# 

# \### Funções Principais (Pygame Zero)

# 

# \* \*\*`update()`\*\*: O loop principal do jogo. É chamado 60 vezes por segundo. Ele atualiza o herói, todos os inimigos, e os ataques. Também verifica as colisões:

# &nbsp;   \* Colisão entre `Attack` e `Enemy` (resulta em ponto).

# &nbsp;   \* Colisão entre `Hero` e `Enemy` (resulta em \*Game Over\*).

# \* \*\*`draw()`\*\*: Responsável por desenhar tudo na tela. Ele verifica o estado do jogo e desenha o menu, a tela de jogo (mapa, personagens, UI) ou a tela de game over.

# \* \*\*`on\_key\_down(key)`\*\*: Captura os eventos de teclado (Espaço para atacar, Enter para reiniciar).

# \* \*\*`on\_mouse\_down(pos)`\*\*: Captura os cliques do mouse, usados exclusivamente para os botões do menu principal.

