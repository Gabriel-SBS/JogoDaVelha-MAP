import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.uic import loadUi

class JogoDaVelhaUI(QMainWindow):
    def __init__(self):
        super(JogoDaVelhaUI, self).__init__()
        loadUi("JogoDaVelha.ui", self)  # Substitua "JogoDaVelha.ui" pelo caminho real do seu arquivo UI
        
        # Conecta os botões a um slot comum (por exemplo, botaoClicado)
        for linha in range(3):
            for coluna in range(3):
                nome_botao = f"pushButton_{linha * 3 + coluna + 1}"
                botao = self.findChild(QPushButton, nome_botao)
                if botao is not None:
                    botao.clicked.connect(self.botaoClicado) # Conecta o sinal 'clicked' ao método 'botaoClicado'
                else:
                    print(f"Aviso: Botão {nome_botao} não encontrado!")

        # Conecta o botão "Recomeçar" ao método reiniciar
        botao_reiniciar = self.findChild(QPushButton, "pushButton_10")
        if botao_reiniciar is not None:
            botao_reiniciar.clicked.connect(self.reiniciar) # Conecta o sinal 'clicked' ao método 'reiniciar'
        else:
            print("Aviso: Botão de reiniciar não encontrado!")
        self.rotulo_vencedor = self.findChild(QLabel, "label")
        self.reiniciar()

    # Método chamado quando um botão é clicado pelo jogador humano
    def botaoClicado(self):
        botao = self.sender()
        if botao is not None and botao.text() == "":
            botao.setText("X")
            botao.setEnabled(False)
            if self.verificar_vitoria():
                trio_vencedor = self.obter_trio_vencedor()
                self.vitoria(*trio_vencedor)
            elif self.verificar_empate():
                self.empate()
            else:
                self.jogador_atual = 2
                if self.jogador_atual == 2:
                    self.jogada_ia()


    # Método para reiniciar o jogo, resetando os botões e redefinindo o estado inicial
    def reiniciar(self):
        for linha in range(3):
            for coluna in range(3):
                nome_botao = f"pushButton_{linha * 3 + coluna + 1}"
                botao = self.findChild(QPushButton, nome_botao)
                if botao is not None:
                    botao.setText("")
                    botao.setEnabled(True)
                    botao.setStyleSheet("QPushButton {color: 797979;}")
                else:
                    print(f"Aviso: Botão {nome_botao} não encontrado!")
        self.jogador_atual = 1
        self.rotulo_vencedor.setText("X começa")

    # Verifica se há uma vitória em linhas, colunas ou diagonais
    def verificar_vitoria(self):
        # Verificar linhas
        for linha in range(3):
            if self.verificar_trio(self.findChild(QPushButton, f"pushButton_{linha * 3 + 1}"),
                                    self.findChild(QPushButton, f"pushButton_{linha * 3 + 2}"),
                                    self.findChild(QPushButton, f"pushButton_{linha * 3 + 3}")):
                return True

        # Verificar colunas
        for coluna in range(3):
            if self.verificar_trio(self.findChild(QPushButton, f"pushButton_{coluna + 1}"),
                                    self.findChild(QPushButton, f"pushButton_{coluna + 4}"),
                                    self.findChild(QPushButton, f"pushButton_{coluna + 7}")):
                return True

        # Verificar diagonais
        if self.verificar_trio(self.findChild(QPushButton, "pushButton_1"),
                                self.findChild(QPushButton, "pushButton_5"),
                                self.findChild(QPushButton, "pushButton_9")) or \
           self.verificar_trio(self.findChild(QPushButton, "pushButton_3"),
                                self.findChild(QPushButton, "pushButton_5"),
                                self.findChild(QPushButton, "pushButton_7")):
            return True

        return False

    # Retorna os botões que compõem o trio vencedor
    def obter_trio_vencedor(self):
        # Retorna os botões que compõem o trio vencedor
        for linha in range(3):
            if self.verificar_trio(self.findChild(QPushButton, f"pushButton_{linha * 3 + 1}"),
                                    self.findChild(QPushButton, f"pushButton_{linha * 3 + 2}"),
                                    self.findChild(QPushButton, f"pushButton_{linha * 3 + 3}")):
                return (
                    self.findChild(QPushButton, f"pushButton_{linha * 3 + 1}"),
                    self.findChild(QPushButton, f"pushButton_{linha * 3 + 2}"),
                    self.findChild(QPushButton, f"pushButton_{linha * 3 + 3}")
                )

        # Verificar colunas
        for coluna in range(3):
            if self.verificar_trio(self.findChild(QPushButton, f"pushButton_{coluna + 1}"),
                                    self.findChild(QPushButton, f"pushButton_{coluna + 4}"),
                                    self.findChild(QPushButton, f"pushButton_{coluna + 7}")):
                return (
                    self.findChild(QPushButton, f"pushButton_{coluna + 1}"),
                    self.findChild(QPushButton, f"pushButton_{coluna + 4}"),
                    self.findChild(QPushButton, f"pushButton_{coluna + 7}")
                )

        # Verificar diagonais
        if self.verificar_trio(self.findChild(QPushButton, "pushButton_1"),
                                self.findChild(QPushButton, "pushButton_5"),
                                self.findChild(QPushButton, "pushButton_9")):
            return (
                self.findChild(QPushButton, "pushButton_1"),
                self.findChild(QPushButton, "pushButton_5"),
                self.findChild(QPushButton, "pushButton_9")
            )
        elif self.verificar_trio(self.findChild(QPushButton, "pushButton_3"),
                                  self.findChild(QPushButton, "pushButton_5"),
                                  self.findChild(QPushButton, "pushButton_7")):
            return (
                self.findChild(QPushButton, "pushButton_3"),
                self.findChild(QPushButton, "pushButton_5"),
                self.findChild(QPushButton, "pushButton_7")
            )

    # Destaca visualmente os botões que levaram à vitória e exibe a mensagem de vitória
    def vitoria(self, botao1, botao2, botao3):
        botao1.setStyleSheet("QPushButton {color: red;}")
        botao2.setStyleSheet("QPushButton {color: red;}")
        botao3.setStyleSheet("QPushButton {color: red;}")
        self.rotulo_vencedor.setText(f"{botao1.text()} ganhou!")
        self.desativar()

    # Verifica se três botões formam um trio vencedor
    def verificar_trio(self, botao1, botao2, botao3):
        return botao1.text() == botao2.text() == botao3.text() != ""

    # Desativa todos os botões após uma vitória
    def desativar(self):
        for linha in range(3):
            for coluna in range(3):
                nome_botao = f"pushButton_{linha * 3 + coluna + 1}"
                botao = self.findChild(QPushButton, nome_botao)
                if botao is not None:
                    botao.setEnabled(False)

    # Verifica se houve empate (todos os botões preenchidos e sem vitória)
    def verificar_empate(self):
        for linha in range(3):
            for coluna in range(3):
                nome_botao = f"pushButton_{linha * 3 + coluna + 1}"
                botao = self.findChild(QPushButton, nome_botao)
                if botao.text() == "":
                    return False  # Ainda há pelo menos um botão não preenchido
        return True  # Todos os botões estão preenchidos e não houve vitória

    # Exibe a mensagem de empate
    def empate(self):
        self.rotulo_vencedor.setText("Empate!")

    # Função para a jogada da inteligência artificial (IA) usando o algoritmo minimax
    def jogada_ia(self):
        melhor_pontuacao = float('-inf')
        melhor_jogada = None
        alfa = float('-inf')
        beta = float('inf')
        for linha in range(3):
            for coluna in range(3):
                nome_botao = f"pushButton_{linha * 3 + coluna + 1}"
                botao = self.findChild(QPushButton, nome_botao)
                if botao is not None and botao.text() == "":
                    botao.setText("O")
                    pontuacao = self.minimax(0, False, alfa, beta)
                    botao.setText("")
                    if pontuacao > melhor_pontuacao:
                        melhor_pontuacao = pontuacao
                        melhor_jogada = botao
                    alfa = max(alfa, melhor_pontuacao)

        if melhor_jogada is not None:
            melhor_jogada.setText("O")
            melhor_jogada.setEnabled(False)
            if self.verificar_vitoria():
                trio_vencedor = self.obter_trio_vencedor()
                self.vitoria(*trio_vencedor)
            elif self.verificar_empate():
                self.empate()
            else:
                self.jogador_atual = 1  # Alterna o jogador

    # Algoritmo minimax com poda alfa-beta para otimizar a busca
    def minimax(self, profundidade, maximizando, alfa, beta):
        if self.verificar_vitoria():
            return -1 if maximizando else 1
        elif self.verificar_empate():
            return 0

        if maximizando:
            melhor_pontuacao = float('-inf')
            for linha in range(3):
                for coluna in range(3):
                    nome_botao = f"pushButton_{linha * 3 + coluna + 1}"
                    botao = self.findChild(QPushButton, nome_botao)
                    if botao is not None and botao.text() == "":
                        botao.setText("O")
                        pontuacao = self.minimax(profundidade + 1, False, alfa, beta)
                        botao.setText("")
                        melhor_pontuacao = max(melhor_pontuacao, pontuacao)
                        alfa = max(alfa, melhor_pontuacao)
                        if beta <= alfa:
                            break  # Poda beta
            return melhor_pontuacao
        else:
            melhor_pontuacao = float('inf')
            for linha in range(3):
                for coluna in range(3):
                    nome_botao = f"pushButton_{linha * 3 + coluna + 1}"
                    botao = self.findChild(QPushButton, nome_botao)
                    if botao is not None and botao.text() == "":
                        botao.setText("X")
                        pontuacao = self.minimax(profundidade + 1, True, alfa, beta)
                        botao.setText("")
                        melhor_pontuacao = min(melhor_pontuacao, pontuacao)
                        beta = min(beta, melhor_pontuacao)
                        if beta <= alfa:
                            break  # Poda alfa
            return melhor_pontuacao
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela_principal = JogoDaVelhaUI()
    janela_principal.show()
    sys.exit(app.exec_())