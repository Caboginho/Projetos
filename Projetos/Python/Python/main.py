import os

# Funções de exemplo

def exemplo_variaveis():
    # Variáveis e Tipos de Dados
    inteiro = 10
    flutuante = 5.5
    caractere = 'A'
    texto = "Olá, mundo!"

    print(f"Inteiro: {inteiro}")
    print(f"Flutuante: {flutuante}")
    print(f"Caractere: {caractere}")
    print(f"Texto: {texto}")

def exemplo_estruturas_controle():
    # Estruturas de Controle
    x = 10

    if x > 5:
        print("x é maior que 5")
    else:
        print("x é menor ou igual a 5")

    for i in range(5):
        print(f"i: {i}")

def saudacao():
    print("Olá, mundo!")

def soma(a, b):
    return a + b

def exemplo_funcoes():
    # Funções
    saudacao()
    resultado = soma(5, 3)
    print(f"Soma: {resultado}")

class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def saudacao(self):
        print(f"Olá, meu nome é {self.nome} e eu tenho {self.idade} anos.")

def exemplo_poo():
    # Programação Orientada a Objetos
    pessoa = Pessoa("João", 30)
    pessoa.saudacao()

class Animal:
    def __init__(self, nome):
        self.nome = nome

    def fazer_som(self):
        pass

class Cachorro(Animal):
    def fazer_som(self):
        print(f"{self.nome} late.")

class Gato(Animal):
    def fazer_som(self):
        print(f"{self.nome} mia.")

class Veiculo:
    def mover(self):
        pass

class Carro(Veiculo):
    def mover(self):
        print("O carro está se movendo.")

class Bicicleta(Veiculo):
    def mover(self):
        print("A bicicleta está se movendo.")

def exemplo_heranca_interface_polimorfismo():
    # Herança, Interface e Polimorfismo
    animais = [Cachorro("Rex"), Gato("Mimi")]
    for animal in animais:
        animal.fazer_som()

    veiculos = [Carro(), Bicicleta()]
    for veiculo in veiculos:
        veiculo.mover()

# Estruturas de Dados

def exemplo_vetores():
    # Vetores
    vetor = [1, 2, 3, 4, 5]
    while True:
        print(f"Vetor atual: {vetor}")
        print("1. Adicionar elemento")
        print("2. Remover elemento")
        print("3. Buscar elemento")
        print("4. Editar elemento")
        print("5. Voltar ao menu principal")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            elemento = int(input("Digite o elemento a ser adicionado: "))
            vetor.append(elemento)
        elif escolha == '2':
            elemento = int(input("Digite o elemento a ser removido: "))
            if elemento in vetor:
                vetor.remove(elemento)
            else:
                print("Elemento não encontrado.")
        elif escolha == '3':
            elemento = int(input("Digite o elemento a ser buscado: "))
            if elemento in vetor:
                print(f"Elemento {elemento} encontrado na posição {vetor.index(elemento)}.")
            else:
                print("Elemento não encontrado.")
        elif escolha == '4':
            posicao = int(input("Digite a posição do elemento a ser editado: "))
            if 0 <= posicao < len(vetor):
                novo_valor = int(input("Digite o novo valor: "))
                vetor[posicao] = novo_valor
            else:
                print("Posição inválida.")
        elif escolha == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

def exemplo_matrizes():
    # Matrizes
    matriz = [[1, 2, 3], [4, 5, 6]]
    while True:
        print("Matriz atual:")
        for linha in matriz:
            print(linha)
        print("1. Adicionar elemento")
        print("2. Remover elemento")
        print("3. Buscar elemento")
        print("4. Editar elemento")
        print("5. Voltar ao menu principal")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            linha = int(input("Digite a linha do elemento a ser adicionado: "))
            coluna = int(input("Digite a coluna do elemento a ser adicionado: "))
            elemento = int(input("Digite o elemento a ser adicionado: "))
            if 0 <= linha < len(matriz) and 0 <= coluna < len(matriz[0]):
                matriz[linha][coluna] = elemento
            else:
                print("Posição inválida.")
        elif escolha == '2':
            linha = int(input("Digite a linha do elemento a ser removido: "))
            coluna = int(input("Digite a coluna do elemento a ser removido: "))
            if 0 <= linha < len(matriz) and 0 <= coluna < len(matriz[0]):
                matriz[linha][coluna] = 0
            else:
                print("Posição inválida.")
        elif escolha == '3':
            elemento = int(input("Digite o elemento a ser buscado: "))
            encontrado = False
            for i in range(len(matriz)):
                for j in range(len(matriz[0])):
                    if matriz[i][j] == elemento:
                        print(f"Elemento {elemento} encontrado na posição ({i}, {j}).")
                        encontrado = True
            if not encontrado:
                print("Elemento não encontrado.")
        elif escolha == '4':
            linha = int(input("Digite a linha do elemento a ser editado: "))
            coluna = int(input("Digite a coluna do elemento a ser editado: "))
            if 0 <= linha < len(matriz) and 0 <= coluna < len(matriz[0]):
                novo_valor = int(input("Digite o novo valor: "))
                matriz[linha][coluna] = novo_valor
            else:
                print("Posição inválida.")
        elif escolha == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def exemplo_listas_encadeadas():
    # Listas Encadeadas
    head = Node(1)
    second = Node(2)
    third = Node(3)

    head.next = second
    second.next = third

    while True:
        temp = head
        print("Lista Encadeada atual: ", end="")
        while temp:
            print(temp.data, end=" -> ")
            temp = temp.next
        print("None")
        print("1. Adicionar elemento")
        print("2. Remover elemento")
        print("3. Buscar elemento")
        print("4. Editar elemento")
        print("5. Voltar ao menu principal")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            elemento = int(input("Digite o elemento a ser adicionado: "))
            novo_node = Node(elemento)
            temp = head
            while temp.next:
                temp = temp.next
            temp.next = novo_node
        elif escolha == '2':
            elemento = int(input("Digite o elemento a ser removido: "))
            temp = head
            prev = None
            while temp and temp.data != elemento:
                prev = temp
                temp = temp.next
            if temp:
                if prev:
                    prev.next = temp.next
                else:
                    head = temp.next
            else:
                print("Elemento não encontrado.")
        elif escolha == '3':
            elemento = int(input("Digite o elemento a ser buscado: "))
            temp = head
            posicao = 0
            encontrado = False
            while temp:
                if temp.data == elemento:
                    print(f"Elemento {elemento} encontrado na posição {posicao}.")
                    encontrado = True
                    break
                temp = temp.next
                posicao += 1
            if not encontrado:
                print("Elemento não encontrado.")
        elif escolha == '4':
            elemento = int(input("Digite o elemento a ser editado: "))
            temp = head
            encontrado = False
            while temp:
                if temp.data == elemento:
                    novo_valor = int(input("Digite o novo valor: "))
                    temp.data = novo_valor
                    encontrado = True
                    break
                temp = temp.next
            if not encontrado:
                print("Elemento não encontrado.")
        elif escolha == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def pre_order(node):
    if not node:
        return
    print(node.data, end=" ")
    pre_order(node.left)
    pre_order(node.right)

def min_value_node(node):
    current = node
    while current.left is not None:
        current = current.left
    return current

def delete_node(root, key):
    if root is None:
        return root

    if key < root.data:
        root.left = delete_node(root.left, key)
    elif key > root.data:
        root.right = delete_node(root.right, key)
    else:
        if root.left is None:
            temp = root.right
            root = None
            return temp
        elif root.right is None:
            temp = root.left
            root = None
            return temp

        temp = min_value_node(root.right)
        root.data = temp.data
        root.right = delete_node(root.right, temp.data)

    return root

def exemplo_arvore_binaria():
    # Árvore Binária
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)

    while True:
        print("Árvore Binária atual (pre-order): ", end="")
        pre_order(root)
        print()
        print("1. Adicionar elemento")
        print("2. Remover elemento")
        print("3. Buscar elemento")
        print("4. Editar elemento")
        print("5. Voltar ao menu principal")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            elemento = int(input("Digite o elemento a ser adicionado: "))
            novo_node = TreeNode(elemento)
            temp = root
            while temp:
                if elemento < temp.data:
                    if temp.left:
                        temp = temp.left
                    else:
                        temp.left = novo_node
                        break
                else:
                    if temp.right:
                        temp = temp.right
                    else:
                        temp.right = novo_node
                        break
        elif escolha == '2':
            elemento = int(input("Digite o elemento a ser removido: "))
            root = delete_node(root, elemento)
        elif escolha == '3':
            elemento = int(input("Digite o elemento a ser buscado: "))
            temp = root
            encontrado = False
            while temp:
                if temp.data == elemento:
                    print(f"Elemento {elemento} encontrado.")
                    encontrado = True
                    break
                elif elemento < temp.data:
                    temp = temp.left
                else:
                    temp = temp.right
            if not encontrado:
                print("Elemento não encontrado.")
        elif escolha == '4':
            elemento = int(input("Digite o elemento a ser editado: "))
            temp = root
            encontrado = False
            while temp:
                if temp.data == elemento:
                    novo_valor = int(input("Digite o novo valor: "))
                    temp.data = novo_valor
                    encontrado = True
                    break
                elif elemento < temp.data:
                    temp = temp.left
                else:
                    temp = temp.right
            if not encontrado:
                print("Elemento não encontrado.")
        elif escolha == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

def exemplo_filas():
    # Filas
    from collections import deque
    fila = deque([1, 2, 3])
    while True:
        print(f"Fila atual: {list(fila)}")
        print("1. Adicionar elemento")
        print("2. Remover elemento")
        print("3. Buscar elemento")
        print("4. Editar elemento")
        print("5. Voltar ao menu principal")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            elemento = int(input("Digite o elemento a ser adicionado: "))
            fila.append(elemento)
        elif escolha == '2':
            if fila:
                fila.popleft()
            else:
                print("Fila vazia.")
        elif escolha == '3':
            elemento = int(input("Digite o elemento a ser buscado: "))
            if elemento in fila:
                print(f"Elemento {elemento} encontrado na posição {list(fila).index(elemento)}.")
            else:
                print("Elemento não encontrado.")
        elif escolha == '4':
            posicao = int(input("Digite a posição do elemento a ser editado: "))
            if 0 <= posicao < len(fila):
                novo_valor = int(input("Digite o novo valor: "))
                fila[posicao] = novo_valor
            else:
                print("Posição inválida.")
        elif escolha == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

def exemplo_pilhas():
    # Pilhas
    pilha = [1, 2, 3]
    while True:
        print(f"Pilha atual: {pilha}")
        print("1. Adicionar elemento")
        print("2. Remover elemento")
        print("3. Buscar elemento")
        print("4. Editar elemento")
        print("5. Voltar ao menu principal")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            elemento = int(input("Digite o elemento a ser adicionado: "))
            pilha.append(elemento)
        elif escolha == '2':
            if pilha:
                pilha.pop()
            else:
                print("Pilha vazia.")
        elif escolha == '3':
            elemento = int(input("Digite o elemento a ser buscado: "))
            if elemento in pilha:
                print(f"Elemento {elemento} encontrado na posição {pilha.index(elemento)}.")
            else:
                print("Elemento não encontrado.")
        elif escolha == '4':
            posicao = int(input("Digite a posição do elemento a ser editado: "))
            if 0 <= posicao < len(pilha):
                novo_valor = int(input("Digite o novo valor: "))
                pilha[posicao] = novo_valor
            else:
                print("Posição inválida.")
        elif escolha == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

# Função para exibir o menu
def exibir_menu():
    print("Selecione um exemplo para executar:")
    print("1. Variáveis e Tipos de Dados")
    print("2. Estruturas de Controle")
    print("3. Funções")
    print("4. Programação Orientada a Objetos")
    print("5. Herança, Interface e Polimorfismo")
    print("6. Vetores")
    print("7. Matrizes")
    print("8. Listas Encadeadas")
    print("9. Árvore Binária")
    print("10. Filas")
    print("11. Pilhas")
    print("Digite 'ESC' para sair.")

def main():
    while True:
        exibir_menu()
        escolha = input("Escolha uma opção: ")

        if escolha.lower() == 'esc':
            break

        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela

        if escolha == '1':
            exemplo_variaveis()
        elif escolha == '2':
            exemplo_estruturas_controle()
        elif escolha == '3':
            exemplo_funcoes()
        elif escolha == '4':
            exemplo_poo()
        elif escolha == '5':
            exemplo_heranca_interface_polimorfismo()
        elif escolha == '6':
            exemplo_vetores()
        elif escolha == '7':
            exemplo_matrizes()
        elif escolha == '8':
            exemplo_listas_encadeadas()
        elif escolha == '9':
            exemplo_arvore_binaria()
        elif escolha == '10':
            exemplo_filas()
        elif escolha == '11':
            exemplo_pilhas()
        else:
            print("Opção inválida. Tente novamente.")

        input("Pressione Enter para voltar ao menu...")
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela

if __name__ == "__main__":
    main()
