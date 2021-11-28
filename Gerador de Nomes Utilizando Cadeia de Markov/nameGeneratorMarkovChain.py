import pandas as pd
import copy
import time


def MLGC(m, a, seed):
    return (a * seed) % m


# Função que imprime um nome gerado aleatoriamente
def printName(l, n, A, translatorLN, translatorNL):
    # Variáveis que serão usadas para gerar números aleatórios
    m = 549755813881
    a = 30508823
    seed = 41574574571 + time.gmtime().tm_sec + \
        (time.gmtime().tm_min*60) + (time.gmtime().tm_hour*3600)

    randomNumber = seed

    # Índice da primeira letra
    index = translatorLN[l]

    print(l, end="")
    # Laço de repetição que imprimirá n - 1 letras
    for i in range(n - 1):
        if i != 0:
            index = translatorLN[l]

        pre, cur = 0, 0
        randomNumber = abs(MLGC(m, a, randomNumber)) % 100

        for j in range(26):
            cur += A[index][j]
            # Verifica se o número gerado aleatoriamente está dentro de uma faixa
            if pre <= randomNumber <= cur:
                l = translatorNL[j]
                print(l, end="")
                break
            pre = cur
    print()


def multMatrix(A):
    aux = [[0 for x in range(len(A))] for y in range(len(A))]
    for i in range(len(A)):
        for j in range(len(A)):
            aux[i][j] = 0
            for k in range(len(A)):
                aux[i][j] += A[i][k]*A[k][j]
                aux[i][j] = round(aux[i][j], 6)
    return aux


def probability(D, names):
    # Criação do dicionário que irá guardar as frequências de cada letra que segue outra
    for i in range(26):
        D[chr(i + 65)] = {chr(x): 0 for x in range(65, 65 + 26)}

    # Contagem das frequências
    for name in names:
        for i in range(len(name) - 1):
            D[name[i]][name[i + 1]] += 1

    markovMatrix = [[0 for x in range(26)] for y in range(26)]

    # Criação da matriz que contará com as probabilidades
    for i in range(65, 65 + 26):
        lineTotal = sum([D[chr(i)][chr(x + 65)] for x in range(26)])
        for j in range(65, 65 + 26):
            markovMatrix[i - 65][j - 65] = D[chr(i)][chr(j)]/lineTotal

    return markovMatrix


def toPercentage(A):
    # Transformação para porcentagem
    for i in range(26):
        for j in range(26):
            A[i][j] = A[i][j]*100

    return A


def main():

    # Leitura do csv contendo os nomes de pessoas
    df = pd.read_csv("./grupos.csv")

    # Transformação do dataframe em lista
    names = list(df["name"])

    D = {}
    # Tradutores de índice para letra e letra para índice
    translatorLN = {chr(x + 65): x for x in range(26)}
    translatorNL = {x: chr(x + 65) for x in range(26)}

    markovMatrix = probability(D, names)

    A = copy.deepcopy(markovMatrix)

    A = toPercentage(A)

    print("Digite a letra inicial do nome: ")
    l = input().upper()

    print("Digite o tamanho do nome: ")
    n = int(input())

    print("Nome:", end=" ")
    printName(l, n, A, translatorLN, translatorNL)
    print()

    time.sleep(2)

    A = copy.deepcopy(markovMatrix)

    # Multiplicação da matriz com as probabilidades por ela mesma
    for i in range(10):
        A = multMatrix(A)

    print("As probabilidades individuais de cada letra são as seguintes: ")

    for i in range(26):
        print(chr(i + 65) + ": " + str(A[0][i]))
    print("Probabilidade total: " + str(round(sum(A[0]), 6)))


if __name__ == '__main__':
    main()
