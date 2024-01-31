from colorama import Fore, Style
from os import system
import copy

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
        all(tabuleiro[i][2-i] == jogador for i in range(3)):
        return True
    
    return False

def jogada_possivel(tabuleiro,linha, coluna):
    return 0<= linha <3 and 0<= coluna <3 and tabuleiro[linha][coluna] == " "

def verificar_empate(tabuleiro):
    return all(tabuleiro[i][j] != " " for i in range(3) for j in range(3))

def minimax(tabuleiro, maximizing):
    if verificar_empate(tabuleiro):
        return 0
    elif verificar_vitoria(tabuleiro, "O"):
        return 1
    elif verificar_vitoria(tabuleiro, "X"):
        return -1

    if maximizing:
        melhorJogada = -float('inf')
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == " ":
                    tab = copy.deepcopy(tabuleiro)
                    tab[i][j] = "O"
                    jogada = minimax(tab, False)
                    melhorJogada = max(jogada, melhorJogada)
        return melhorJogada

    else: 
        melhorJogada = float('inf')
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == " ":
                    tab = copy.deepcopy(tabuleiro)
                    tab[i][j] = "X"
                    jogada = minimax(tab, True)
                    melhorJogada = min(jogada, melhorJogada)
        return melhorJogada
    
def get_movimento(tabuleiro):
    melhorJogada = -float('inf')
    melhorMovimento = None
    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] == " ":
                tab = copy.deepcopy(tabuleiro)
                tab[i][j] = "O"
                jogada = minimax(tab, False)
                if jogada > melhorJogada:
                    melhorJogada = jogada
                    melhorMovimento = (i,j)
    return melhorMovimento    

def jogar_jogo_da_velha():
    tabuleiro = [[" " for _ in range(3)] for _ in range(3)]
    troca = 1
    jogo_terminado = False

    while not jogo_terminado:
        imprimir_tabuleiro(tabuleiro)
        if troca == 1:
            linha = int(input(f"Vez do Jogador (X), escolha a linha (1, 2 ou 3) ")) - 1
            coluna = int(input(f"Vez do Jogador (X), escolha a coluna (1, 2 ou 3) ")) - 1
            if jogada_possivel(tabuleiro, linha, coluna):
                tabuleiro[linha][coluna] = Fore.RED + "X" + Style.RESET_ALL
                if verificar_vitoria(tabuleiro, Fore.RED + "X" + Style.RESET_ALL):
                    imprimir_tabuleiro(tabuleiro)
                    print(f"Parabéns, jogador X venceu!")
                    jogo_terminado = True
                elif verificar_empate(tabuleiro):
                    imprimir_tabuleiro(tabuleiro)
                    print("Empate!")
                    jogo_terminado = True
                else:
                    troca = 2
            else:
                system("cls")
                print("Posição ocupada ou inexistente. Escolha outra.")
                continue
        else:
            system("cls")
            print("Vez da IA (O):")
            linha, coluna = get_movimento(tabuleiro)
            tabuleiro[linha][coluna] = Fore.BLUE + "O" + Style.RESET_ALL
            if verificar_vitoria(tabuleiro, Fore.BLUE + "O" + Style.RESET_ALL):
                imprimir_tabuleiro(tabuleiro)
                print("IA venceu!")
                jogo_terminado = True
            elif verificar_empate(tabuleiro):
                imprimir_tabuleiro(tabuleiro)
                print("Empate!")
                jogo_terminado = True
            else:
                troca = 1

    return input("Deseja jogar novamente? (s/n): ").lower() == "s"

continuar_jogando = True
while continuar_jogando:
    system("cls")
    continuar_jogando = jogar_jogo_da_velha()
print("Obrigado por jogar!")