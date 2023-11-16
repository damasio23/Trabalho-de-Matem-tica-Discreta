import numpy as np
import pandas as pd

def SimplificarProdutos(A, p):
    # Encontrar os vértices que têm um caminho até algum material em p
    vertices_conectados = set()

    # Adicionar os materiais em p
    vertices_conectados.update(p)

    # Iterar até não haver mais adições aos vértices conectados
    while True:
        num_vertices_anterior = len(vertices_conectados)

        # Iterar sobre todas as linhas da matriz A
        for i in range(A.shape[0]):
            # Se a linha i tem um caminho para um vértice conectado, adicionar i aos vértices conectados
            if i not in vertices_conectados and any(A[i, j] != 0 for j in vertices_conectados):
                vertices_conectados.add(i)

        # Se não houver adições, sair do loop
        if len(vertices_conectados) == num_vertices_anterior:
            break

    # Filtrar as linhas da matriz original com base nos vértices conectados
    linhas_conectadas = list(vertices_conectados)

    # Criar a matriz simplificada
    A_simplificado = A[linhas_conectadas, :]

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
