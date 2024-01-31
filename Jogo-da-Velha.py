from colorama import Fore, Style
from os import system

def imprimir_tabuleiro(tabuleiro):
    for linha in tabuleiro:
        print("|".join(linha))
        print("-----")

def verificar_vitoria(tabuleiro, jogador):
    for i in range(3):
        if all(tabuleiro[i][j] == jogador for j in range(3)) or \
            all(tabuleiro[j][i] == jogador for j in range(3)):
            return True
    
    if all(tabuleiro[i][i] == jogador for i in range(3)) or \
        all(tabuleiro[i][2-i] == jogador for j in range(3)):
        return True
    
    return False

def jogada_possivel(tabuleiro,linha, coluna):
    return 0<= linha <3 and 0<= coluna <3 and tabuleiro[linha][coluna] == " "

def jogar_jogo_da_velha():
    tabuleiro = [[" " for _ in range (3)] for _ in range(3)]
    jogador_atual = "X"
    jogo_terminado = False

    while not jogo_terminado:
        imprimir_tabuleiro(tabuleiro)
        linha = int(input(f"Jogador {jogador_atual}, escolha a linha (1, 2 ou 3) "))-1
        coluna = int(input(f"Jogador {jogador_atual}, escolha a coluna (1, 2 ou 3) "))-1

        if jogada_possivel(tabuleiro, linha, coluna):
            system("cls")
            cor = Fore.RED if jogador_atual == "X" else Fore.BLUE
            tabuleiro[linha][coluna] = cor + jogador_atual + Style.RESET_ALL

            if verificar_vitoria(tabuleiro, cor + jogador_atual + Style.RESET_ALL):
                imprimir_tabuleiro(tabuleiro)
                print(f"Parabéns, jogador {jogador_atual} Venceu!")
                jogo_terminado = True
            else:
                if jogador_atual == "X":
                    jogador_atual = "O"
                else:
                    jogador_atual = "X"
        else:
            system("cls")
            print("posição ocupada ou inesxistente. Escolha outra.")

        if all(tabuleiro[i][j] != " " for i in range(3) for j in range (3)):
            imprimir_tabuleiro(tabuleiro)
            print("Empate!")
            jogo_terminado = True
        
    return input("Deseja jogar novamente? (s/n): ").lower() == "s"

continuar_jogando = True
while continuar_jogando:
    system("cls")
    continuar_jogando = jogar_jogo_da_velha()
print("Obrigado Por Jogar")

