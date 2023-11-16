import numpy as np
import pandas as pd

def SimplificarProdutos(A, p):
    # Criar uma cópia da matriz original
    A_simplificado = np.copy(A)

    # Encontrar os vértices que não têm caminho até os materiais em p
    vertices_a_remover = []
    for coluna in range(A.shape[1]):
        if coluna not in p and not any(A[:, coluna]):
            vertices_a_remover.append(coluna)

    # Remover os vértices da matriz
    A_simplificado = np.delete(A_simplificado, vertices_a_remover, axis=1)

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
