import numpy as np
import pandas as pd

def SimplificarProdutos(A, p):
    # Criar conjuntos para materiais e receitas
    materiais = set(p)
    receitas = set(range(A.shape[0]))

    # Iterar até não haver mais adições aos vértices conectados
    while True:
        num_materiais_anterior = len(materiais)
        num_receitas_anterior = len(receitas)

        # Iterar sobre todas as linhas (receitas) da matriz A
        for i in range(A.shape[0]):
            # Se a receita i tem um caminho para um material conectado, adicionar i às receitas conectadas
            if i not in receitas and any(A[i, j] < 0 for j in materiais):
                receitas.add(i)

        # Iterar sobre todas as colunas (materiais) da matriz A
        for j in range(A.shape[1]):
            # Se o material j tem um caminho para uma receita conectada, adicionar j aos materiais conectados
            if j not in materiais and any(A[i, j] > 0 for i in receitas):
                materiais.add(j)

        # Se não houver adições, sair do loop
        if len(materiais) == num_materiais_anterior and len(receitas) == num_receitas_anterior:
            break

    # Filtrar as linhas e colunas da matriz original com base nos vértices conectados
    linhas_conectadas = list(receitas)
    colunas_conectadas = list(materiais)

    A_simplificado = A[linhas_conectadas, :][:, colunas_conectadas]

    return A_simplificado

# Matriz A
receitas = pd.read_json('receitas.json')
items = pd.read_json('items.json')

A = np.zeros((197, 116))

linha = 0
for i in receitas:
    for j in receitas[i]["ingredients"]:
        A[linha][items[j["item"]]["id"]] = -j["amount"]
    for j in receitas[i]["products"]:
        A[linha][items[j["item"]]["id"]] = j["amount"]
    linha += 1

# Lista de materiais a serem produzidos
materiais_a_produzir = [items[j["item"]]["id"] for i in receitas for j in receitas[i]["products"]]

# Chamando a função SimplificarProdutos
A_simplificado = SimplificarProdutos(A, materiais_a_produzir)

# Imprimindo a matriz simplificada
print(A_simplificado)

# Salvando a matriz simplificada em um arquivo
np.savetxt("MatrizSimplificada.txt", A_simplificado)
