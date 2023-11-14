import pandas as pd
import numpy as np

receitas = pd.read_json('receitas.json')
items = pd.read_json('items.json')

A = np.zeros((197,116))

linha = 0
for i in receitas:
    for j in receitas[i]["ingredients"]:
        A[linha][items[j["item"]]["id"]] = -j["amount"]
    for j in receitas[i]["products"]:
        A[linha][items[j["item"]]["id"]] = j["amount"]
    linha += 1

print(A)

np.savetxt("Matriz.txt", A)