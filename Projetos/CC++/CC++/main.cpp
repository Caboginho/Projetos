#include <iostream>
#include <string>
#include <cstdlib>
#include <conio.h> // Para _getch()
#include <vector>
#include <queue>
#include <stack>

// Funções de exemplo

void exemploVariaveisC() {
    // C
    #include <stdio.h>
    int inteiro = 10;
    float flutuante = 5.5;
    char caractere = 'A';

    printf("Inteiro: %d\n", inteiro);
    printf("Flutuante: %.2f\n", flutuante);
    printf("Caractere: %c\n", caractere);
}

void exemploVariaveisCPP() {
    // C++
    int inteiro = 10;
    float flutuante = 5.5;
    char caractere = 'A';

    std::cout << "Inteiro: " << inteiro << std::endl;
    std::cout << "Flutuante: " << flutuante << std::endl;
    std::cout << "Caractere: " << caractere << std::endl;
}

void exemploEstruturasControleC() {
    // C
    int x = 10;

    if (x > 5) {
        printf("x é maior que 5\n");
    } else {
        printf("x é menor ou igual a 5\n");
    }

    for (int i = 0; i < 5; i++) {
        printf("i: %d\n", i);
    }
}

void exemploEstruturasControleCPP() {
    // C++

    int x = 10;

    if (x > 5) {
        std::cout << "x é maior que 5" << std::endl;
    } else {
        std::cout << "x é menor ou igual a 5" << std::endl;
    }

    for (int i = 0; i < 5; i++) {
        std::cout << "i: " << i << std::endl;
    }
}

void saudacao() {
    printf("Olá, mundo!\n");
}

int soma(int a, int b) {
    return a + b;
}
void exemploFuncoesC() {
    // C
    saudacao();
    int resultado = soma(5, 3);
    printf("Soma: %d\n", resultado);
}

void saudacaocpp() {
    std::cout << "Olá, mundo!" << std::endl;
}
int somacpp(int a, int b) {
    return a + b;
}

void exemploFuncoesCPP() {
    // C++
    saudacaocpp();
    int resultado = somacpp(5, 3);
    std::cout << "Soma: " << resultado << std::endl;
}

void exemploPOO() {
    // Programação Orientada a Objetos (C++)
   
    class Pessoa {
    public:
        std::string nome;
        int idade;

        void saudacao() {
            std::cout << "Olá, meu nome é " << nome << " e eu tenho " << idade << " anos." << std::endl;
        }
    };

    Pessoa pessoa;
    pessoa.nome = "João";
    pessoa.idade = 30;
    pessoa.saudacao();
}

void exemploHerancaInterfacePolimorfismo() {
    // Herança, Interface e Polimorfismo
    
    // Classe base
    class Animal {
    public:
        std::string nome;

        Animal(std::string n) : nome(n) {}

        virtual void fazerSom() {
            std::cout << nome << " faz um som." << std::endl;
        }
    };

    // Classe derivada (herança)
    class Cachorro : public Animal {
    public:
        Cachorro(std::string n) : Animal(n) {}

        void fazerSom() override {
            std::cout << nome << " late." << std::endl;
        }
    };

    // Outra classe derivada (herança)
    class Gato : public Animal {
    public:
        Gato(std::string n) : Animal(n) {}

        void fazerSom() override {
            std::cout << nome << " mia." << std::endl;
        }
    };

    // Interface (classe abstrata)
    class Veiculo {
    public:
        virtual void mover() = 0; // Método puramente virtual
    };

    // Classe que implementa a interface
    class Carro : public Veiculo {
    public:
        void mover() override {
            std::cout << "O carro está se movendo." << std::endl;
        }
    };

    // Classe que implementa a interface
    class Bicicleta : public Veiculo {
    public:
        void mover() override {
            std::cout << "A bicicleta está se movendo." << std::endl;
        }
    };
    int i = 0;
    // Polimorfismo com classes derivadas
    Animal* animais[2];
    animais[0] = new Cachorro("Rex");
    animais[1] = new Gato("Mimi");

    for ( i = 0; i < 2; i++) {
        animais[i]->fazerSom();
    }

    // Polimorfismo com interfaces
    Veiculo* veiculos[2];
    veiculos[0] = new Carro();
    veiculos[1] = new Bicicleta();

    for (i = 0; i < 2; i++) {
        veiculos[i]->mover();
    }

    // Limpeza de memória
    for (i = 0; i < 2; i++) {
        delete animais[i];
        delete veiculos[i];
    }
}

// Estruturas de Dados

void exemploVetores() {
    // Vetores
    std::vector<int> vetor = {1, 2, 3, 4, 5};
    for (int i : vetor) {
        std::cout << i << " ";
    }
    std::cout << std::endl;
}

void exemploMatrizes() {
    // Matrizes
    int matriz[2][3] = {{1, 2, 3}, {4, 5, 6}};
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 3; j++) {
            std::cout << matriz[i][j] << " ";
        }
        std::cout << std::endl;
    }
}

struct Node {
    int data;
    Node* next;
};

void exemploListasEncadeadas() {
    // Listas Encadeadas
    Node* head = new Node();
    Node* second = new Node();
    Node* third = new Node();

    head->data = 1;
    head->next = second;

    second->data = 2;
    second->next = third;

    third->data = 3;
    third->next = nullptr;

    Node* temp = head;
    while (temp != nullptr) {
        std::cout << temp->data << " ";
        temp = temp->next;
    }
    std::cout << std::endl;

    delete head;
    delete second;
    delete third;
}

struct TreeNode {
    int data;
    TreeNode* left;
    TreeNode* right;
};

TreeNode* newNode(int data) {
    TreeNode* node = new TreeNode();
    node->data = data;
    node->left = nullptr;
    node->right = nullptr;
    return node;
}

void preOrder(TreeNode* node) {
    if (node == nullptr) return;
    std::cout << node->data << " ";
    preOrder(node->left);
    preOrder(node->right);
}

void exemploArvoreBinaria() {
    // Árvore Binária
    TreeNode* root = newNode(1);
    root->left = newNode(2);
    root->right = newNode(3);
    root->left->left = newNode(4);
    root->left->right = newNode(5);

    preOrder(root);
    std::cout << std::endl;

    // Limpeza de memória
    delete root->left->left;
    delete root->left->right;
    delete root->left;
    delete root->right;
    delete root;
}

void exemploFilas() {
    // Filas
    std::queue<int> fila;
    fila.push(1);
    fila.push(2);
    fila.push(3);

    while (!fila.empty()) {
        std::cout << fila.front() << " ";
        fila.pop();
    }
    std::cout << std::endl;
}

void exemploPilhas() {
    // Pilhas
    std::stack<int> pilha;
    pilha.push(1);
    pilha.push(2);
    pilha.push(3);

    while (!pilha.empty()) {
        std::cout << pilha.top() << " ";
        pilha.pop();
    }
    std::cout << std::endl;
}

// Função para exibir o menu
void exibirMenu() {
    std::cout << "Selecione um exemplo para executar:" << std::endl;
    std::cout << "1. Variáveis e Tipos de Dados (C)" << std::endl;
    std::cout << "2. Variáveis e Tipos de Dados (C++)" << std::endl;
    std::cout << "3. Estruturas de Controle (C)" << std::endl;
    std::cout << "4. Estruturas de Controle (C++)" << std::endl;
    std::cout << "5. Funções (C)" << std::endl;
    std::cout << "6. Funções (C++)" << std::endl;
    std::cout << "7. Programação Orientada a Objetos (C++)" << std::endl;
    std::cout << "8. Herança, Interface e Polimorfismo (C++)" << std::endl;
    std::cout << "9. Vetores" << std::endl;
    std::cout << "10. Matrizes" << std::endl;
    std::cout << "11. Listas Encadeadas" << std::endl;
    std::cout << "12. Árvore Binária" << std::endl;
    std::cout << "13. Filas" << std::endl;
    std::cout << "14. Pilhas" << std::endl;
    std::cout << "Escreva '15' para sair." << std::endl;
}

int main() {
    // Configura a localidade para português do Brasil
    std::setlocale(LC_ALL, "pt_BR");
    while (true) {
        exibirMenu();
        int escolha = 0;

        scanf("%d", &escolha);
        if (escolha == 15) { // ESC key
            break;
        }
        system("cls"); // Limpa a tela

        switch (escolha) {
            case 1:
                exemploVariaveisC();
                break;
            case 2:
                exemploVariaveisCPP();
                break;
            case 3:
                exemploEstruturasControleC();
                break;
            case 4:
                exemploEstruturasControleCPP();
                break;
            case 5:
                exemploFuncoesC();
                break;
            case 6:
                exemploFuncoesCPP();
                break;
            case 7:
                exemploPOO();
                break;
            case 8:
                exemploHerancaInterfacePolimorfismo();
                break;
            case 9:
                exemploVetores();
                break;
            case 10:
                exemploMatrizes();
                break;
            case 11:
                exemploListasEncadeadas();
                break;
            case 12:
                exemploArvoreBinaria();
                break;
            case 13:
                exemploFilas();
                break;
            case 14:
                exemploPilhas();
                break;
            default:
                std::cout << "Opção inválida. Tente novamente." << std::endl;
                break;
        }

        std::cout << "Pressione qualquer tecla para voltar ao menu..." << std::endl;
        system("cls"); // Limpa a tela
    }

    return 0;
}
