package java;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;
import java.util.Stack;

// Funções de exemplo

public class Main {

    public static void exemploVariaveis() {
        // Variáveis e Tipos de Dados
        int inteiro = 10;
        float flutuante = 5.5f;
        char caractere = 'A';
        String texto = "Olá, mundo!";

        System.out.println("Inteiro: " + inteiro);
        System.out.println("Flutuante: " + flutuante);
        System.out.println("Caractere: " + caractere);
        System.out.println("Texto: " + texto);
    }

    public static void exemploEstruturasControle() {
        // Estruturas de Controle
        int x = 10;

        if (x > 5) {
            System.out.println("x é maior que 5");
        } else {
            System.out.println("x é menor ou igual a 5");
        }

        for (int i = 0; i < 5; i++) {
            System.out.println("i: " + i);
        }
    }

    public static void saudacao() {
        System.out.println("Olá, mundo!");
    }

    public static int soma(int a, int b) {
        return a + b;
    }

    public static void exemploFuncoes() {
        // Funções
        saudacao();
        int resultado = soma(5, 3);
        System.out.println("Soma: " + resultado);
    }

    public static void exemploPOO() {
        // Programação Orientada a Objetos
        class Pessoa {
            String nome;
            int idade;

            Pessoa(String nome, int idade) {
                this.nome = nome;
                this.idade = idade;
            }

            void saudacao() {
                System.out.println("Olá, meu nome é " + nome + " e eu tenho " + idade + " anos.");
            }
        }

        Pessoa pessoa = new Pessoa("João", 30);
        pessoa.saudacao();
    }
    interface Veiculo {
        void mover();
    }
    public static void exemploHerancaInterfacePolimorfismo() {
        // Herança, Interface e Polimorfismo
        abstract class Animal {
            String nome;

            Animal(String nome) {
                this.nome = nome;
            }

            abstract void fazerSom();
        }

        class Cachorro extends Animal {
            Cachorro(String nome) {
                super(nome);
            }

            @Override
            void fazerSom() {
                System.out.println(nome + " late.");
            }
        }

        class Gato extends Animal {
            Gato(String nome) {
                super(nome);
            }

            @Override
            void fazerSom() {
                System.out.println(nome + " mia.");
            }
        }

        class Carro implements Veiculo {
            @Override
            public void mover() {
                System.out.println("O carro está se movendo.");
            }
        }

        class Bicicleta implements Veiculo {
            @Override
            public void mover() {
                System.out.println("A bicicleta está se movendo.");
            }
        }

        Animal[] animais = {new Cachorro("Rex"), new Gato("Mimi")};
        for (Animal animal : animais) {
            animal.fazerSom();
        }

        Veiculo[] veiculos = {new Carro(), new Bicicleta()};
        for (Veiculo veiculo : veiculos) {
            veiculo.mover();
        }
    }

    // Estruturas de Dados

    public static void exemploVetores() {
        // Vetores
        ArrayList<Integer> vetor = new ArrayList<>();
        vetor.add(1);
        vetor.add(2);
        vetor.add(3);
        vetor.add(4);
        vetor.add(5);

        for (int i : vetor) {
            System.out.print(i + " ");
        }
        System.out.println();
    }

    public static void exemploMatrizes() {
        // Matrizes
        int[][] matriz = {{1, 2, 3}, {4, 5, 6}};
        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 3; j++) {
                System.out.print(matriz[i][j] + " ");
            }
            System.out.println();
        }
    }

    static class Node {
        int data;
        Node next;

        Node(int data) {
            this.data = data;
            this.next = null;
        }
    }

    public static void exemploListasEncadeadas() {
        // Listas Encadeadas
        Node head = new Node(1);
        Node second = new Node(2);
        Node third = new Node(3);

        head.next = second;
        second.next = third;

        Node temp = head;
        while (temp != null) {
            System.out.print(temp.data + " ");
            temp = temp.next;
        }
        System.out.println();
    }

    public static class TreeNode {
        int data;
        TreeNode left, right;

        TreeNode(int data) {
            this.data = data;
            left = right = null;
        }
    }

    public static void preOrder(TreeNode node) {
        if (node == null) return;
        System.out.print(node.data + " ");
        preOrder(node.left);
        preOrder(node.right);
    }

    public static void exemploArvoreBinaria() {
        // Árvore Binária
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);

        preOrder(root);
        System.out.println();
    }

    public static void exemploFilas() {
        // Filas
        Queue<Integer> fila = new LinkedList<>();
        fila.add(1);
        fila.add(2);
        fila.add(3);

        while (!fila.isEmpty()) {
            System.out.print(fila.poll() + " ");
        }
        System.out.println();
    }

    public static void exemploPilhas() {
        // Pilhas
        Stack<Integer> pilha = new Stack<>();
        pilha.push(1);
        pilha.push(2);
        pilha.push(3);

        while (!pilha.isEmpty()) {
            System.out.print(pilha.pop() + " ");
        }
        System.out.println();
    }

    // Função para exibir o menu
    public static void exibirMenu() {
        System.out.println("Selecione um exemplo para executar:");
        System.out.println("1. Variáveis e Tipos de Dados");
        System.out.println("2. Estruturas de Controle");
        System.out.println("3. Funções");
        System.out.println("4. Programação Orientada a Objetos");
        System.out.println("5. Herança, Interface e Polimorfismo");
        System.out.println("6. Vetores");
        System.out.println("7. Matrizes");
        System.out.println("8. Listas Encadeadas");
        System.out.println("9. Árvore Binária");
        System.out.println("10. Filas");
        System.out.println("11. Pilhas");
        System.out.println("Escreva ESC para sair.");
    }

    public static void main (String[] args) {
        try (Scanner scanner = new Scanner(System.in)) {
            while (true) {
                exibirMenu();
                String escolha = scanner.nextLine();
                
                if (escolha.equalsIgnoreCase("ESC")) {
                    break;
                }
                
                switch (escolha) {
                    case "1" -> exemploVariaveis();
                    case "2" -> exemploEstruturasControle();
                    case "3" -> exemploFuncoes();
                    case "4" -> exemploPOO();
                    case "5" -> exemploHerancaInterfacePolimorfismo();
                    case "6" -> exemploVetores();
                    case "7" -> exemploMatrizes();
                    case "8" -> exemploListasEncadeadas();
                    case "9" -> exemploArvoreBinaria();
                    case "10" -> exemploFilas();
                    case "11" -> exemploPilhas();
                    default -> System.out.println("Opção inválida. Tente novamente.");
                }
                
                System.out.println("Pressione Enter para voltar ao menu...");
                scanner.nextLine();
            }
        }
    }
}
