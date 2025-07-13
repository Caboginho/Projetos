# App DW Moodle - Visualizador de Dados Educacionais
# Autor: George Silva ALves, 201620032
# Descrição: Aplicação de visualização de dados conectada ao banco de dados 'educacional' (MySQL),
# com suporte a análises estatísticas, gráficos e exploração de variáveis diretamente da base.
# Bibliotecas: tkinter, matplotlib, numpy, mysql-connector-python

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np

# --- CONEXÃO COM O BANCO DE DADOS ---
db = mysql.connector.connect(host="localhost", user="root", password="", database="educacional")
cursor = db.cursor()

# --- UTILITÁRIOS DE DADOS ---
def resetar_texto():
    """Limpa o conteúdo da área de texto."""
    texto.delete("1.0", tk.END)

def executar_query(sql):
    """Executa uma query SQL e retorna os resultados."""
    cursor.execute(sql)
    return cursor.fetchall()

def carregar_tabelas():
    """Retorna a lista de tabelas disponíveis no banco de dados."""
    cursor.execute("SHOW TABLES")
    return [linha[0] for linha in cursor.fetchall()]

def colunas_numericas(tabela):
    """Retorna colunas com dados numéricos para análise estatística/gráfica."""
    cursor.execute(f"SHOW COLUMNS FROM {tabela}")
    colunas = [col[0] for col in cursor.fetchall()]
    numericas = []
    for coluna in colunas:
        cursor.execute(f"SELECT `{coluna}` FROM {tabela}")
        valores = [row[0] for row in cursor.fetchall() if isinstance(row[0], (int, float))]
        if valores:
            numericas.append((coluna, valores))
    return numericas

def colunas_categoricas(tabela):
    """Retorna colunas do tipo texto ou categóricas."""
    cursor.execute(f"SHOW COLUMNS FROM {tabela}")
    return [col[0] for col in cursor.fetchall() if 'char' in col[1] or 'text' in col[1]]

# --- EXIBIÇÃO DE TABELA ---
def mostrar_tabela():
    """Mostra as primeiras linhas da tabela selecionada no painel de texto."""
    tabela = combo_tabelas.get()
    resetar_texto()
    resultado = executar_query(f"SELECT * FROM {tabela}")
    for linha in resultado:
        texto.insert(tk.END, str(linha) + "\n")

# --- ESTATÍSTICAS BÁSICAS ---
def mostrar_estatisticas():
    """Mostra média, mediana, desvio padrão, mínimo e máximo para cada coluna numérica."""
    tabela = combo_tabelas.get()
    resetar_texto()
    stats = colunas_numericas(tabela)
    if not stats:
        texto.insert(tk.END, "Nenhuma coluna numérica encontrada na tabela.")
        return
    for coluna, valores in stats:
        arr = np.array(valores)
        texto.insert(tk.END, f"\n📌 Coluna: {coluna}\n")
        texto.insert(tk.END, f"  - Média: {np.mean(arr):.2f}\n")
        texto.insert(tk.END, f"  - Mediana: {np.median(arr):.2f}\n")
        texto.insert(tk.END, f"  - Desvio Padrão: {np.std(arr):.2f}\n")
        texto.insert(tk.END, f"  - Mínimo: {np.min(arr)}\n")
        texto.insert(tk.END, f"  - Máximo: {np.max(arr)}\n")

# --- GRÁFICOS DINÂMICOS COM BASE NA TABELA SELECIONADA ---
def grafico_bar_avg_contextual():
    """Gráfico de barras: média de uma variável numérica agrupada por uma categórica."""
    tabela = combo_tabelas.get()
    cat_cols = colunas_categoricas(tabela)
    num_cols = colunas_numericas(tabela)
    if not cat_cols or not num_cols:
        texto.insert(tk.END, "É necessário ao menos uma coluna categórica e uma numérica.")
        return
    cat_col = cat_cols[0]
    num_col = num_cols[0][0]
    sql = f"SELECT `{cat_col}`, AVG(`{num_col}`) FROM `{tabela}` GROUP BY `{cat_col}`"
    dados = executar_query(sql)
    labels = [linha[0] if linha[0] else "Indefinido" for linha in dados]
    valores = [linha[1] for linha in dados]
    plt.bar(labels, valores, color='steelblue')
    plt.title(f"Média de {num_col} por {cat_col} - {tabela}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def grafico_linha_avg_contextual():
    """Gráfico de linha da média de uma variável numérica por categoria."""
    tabela = combo_tabelas.get()
    cat_cols = colunas_categoricas(tabela)
    num_cols = colunas_numericas(tabela)
    if not cat_cols or not num_cols:
        texto.insert(tk.END, "É necessário ao menos uma coluna categórica e uma numérica.")
        return
    cat_col = cat_cols[0]
    num_col = num_cols[0][0]
    sql = f"SELECT `{cat_col}`, AVG(`{num_col}`) FROM `{tabela}` GROUP BY `{cat_col}`"
    dados = executar_query(sql)
    labels = [linha[0] if linha[0] else "Indefinido" for linha in dados]
    valores = [linha[1] for linha in dados]
    plt.plot(labels, valores, marker='o')
    plt.title(f"Média de {num_col} por {cat_col} - {tabela}")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def grafico_rollup_contextual():
    """Gráfico de barras com agrupamento + total (ROLLUP) para média de valores."""
    tabela = combo_tabelas.get()
    cat_cols = colunas_categoricas(tabela)
    num_cols = colunas_numericas(tabela)
    if not cat_cols or not num_cols:
        texto.insert(tk.END, "É necessário ao menos uma coluna categórica e uma numérica.")
        return
    cat_col = cat_cols[0]
    num_col = num_cols[0][0]
    sql = f"""
        SELECT COALESCE(`{cat_col}`, 'Total'), AVG(`{num_col}`), COUNT(*)
        FROM `{tabela}`
        GROUP BY `{cat_col}` WITH ROLLUP
    """
    dados = executar_query(sql)
    labels = [linha[0] for linha in dados]
    valores = [linha[1] for linha in dados]
    plt.bar(labels, valores, color='purple')
    plt.title(f"Média com ROLLUP: {num_col} por {cat_col} - {tabela}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def grafico_having_contextual():
    """Gráfico de barras com HAVING (quantidade mínima de registros por grupo)."""
    tabela = combo_tabelas.get()
    cat_cols = colunas_categoricas(tabela)
    num_cols = colunas_numericas(tabela)
    if not cat_cols or not num_cols:
        texto.insert(tk.END, "É necessário ao menos uma coluna categórica e uma numérica.")
        return
    cat_col = cat_cols[0]
    num_col = num_cols[0][0]
    sql = f"""
        SELECT `{cat_col}`, AVG(`{num_col}`), COUNT(*) as qtd
        FROM `{tabela}`
        GROUP BY `{cat_col}`
        HAVING qtd > 5
    """
    dados = executar_query(sql)
    labels = [linha[0] for linha in dados]
    valores = [linha[1] for linha in dados]
    plt.bar(labels, valores, color='darkorange')
    plt.title(f"Média de {num_col} (HAVING qtd > 5) por {cat_col} - {tabela}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# --- OUTROS GRÁFICOS ---
def mostrar_boxplot():
    """Boxplot de todas as colunas numéricas."""
    tabela = combo_tabelas.get()
    stats = colunas_numericas(tabela)
    if not stats:
        resetar_texto()
        texto.insert(tk.END, "Nenhuma coluna numérica encontrada para gerar o boxplot.")
        return
    nomes = [col[0] for col in stats]
    valores = [col[1] for col in stats]
    plt.boxplot(valores, labels=nomes, patch_artist=True)
    plt.title(f"Boxplot - {tabela}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

def mostrar_histograma():
    """Histograma para cada variável numérica."""
    tabela = combo_tabelas.get()
    resetar_texto()
    stats = colunas_numericas(tabela)
    if not stats:
        texto.insert(tk.END, "Nenhuma coluna numérica encontrada.")
        return
    for coluna, valores in stats:
        plt.hist(valores, bins=10, alpha=0.7)
        plt.title(f"Histograma - {coluna}")
        plt.xlabel(coluna)
        plt.ylabel("Frequência")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

def grafico_pie_dinamico():
    """Gráfico de pizza com base na primeira coluna categórica."""
    tabela = combo_tabelas.get()
    resetar_texto()
    cursor.execute(f"SHOW COLUMNS FROM {tabela}")
    colunas = cursor.fetchall()
    cat_col = next((col[0] for col in colunas if 'char' in col[1] or 'text' in col[1]), None)
    if not cat_col:
        texto.insert(tk.END, "Nenhuma coluna categórica para gráfico de pizza.")
        return
    sql = f'''
        SELECT `{cat_col}`, COUNT(*) as qtd
        FROM `{tabela}`
        GROUP BY `{cat_col}`
        HAVING qtd > 1
    '''
    dados = executar_query(sql)
    labels = [linha[0] if linha[0] else "Indefinido" for linha in dados]
    quantidades = [linha[1] for linha in dados]
    plt.pie(quantidades, labels=labels, autopct='%1.1f%%')
    plt.title(f"Distribuição por {cat_col} na tabela {tabela}")
    plt.tight_layout()
    plt.show()

def abrir_regressao():
    """Abre janela para regressão linear entre duas colunas numéricas."""
    tabela = combo_tabelas.get()
    stats = colunas_numericas(tabela)
    colnames = [col[0] for col in stats]
    janela_reg = tk.Toplevel(janela)
    janela_reg.title("Regressão Linear")
    janela_reg.geometry("300x150")

    def calcular():
        x_col = combo_x.get()
        y_col = combo_y.get()
        if x_col == y_col:
            messagebox.showerror("Erro", "Colunas devem ser diferentes.")
            return
        x = next(v for c, v in stats if c == x_col)
        y = next(v for c, v in stats if c == y_col)
        if len(x) != len(y):
            messagebox.showerror("Erro", "Tamanhos diferentes.")
            return
        x_arr = np.array(x)
        y_arr = np.array(y)
        m, b = np.polyfit(x_arr, y_arr, 1)
        plt.scatter(x_arr, y_arr)
        plt.plot(x_arr, m*x_arr + b, color='red')
        plt.title(f"Regressão Linear: {y_col} ~ {x_col}")
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    tk.Label(janela_reg, text="X:").grid(row=0, column=0)
    combo_x = ttk.Combobox(janela_reg, values=colnames)
    combo_x.grid(row=0, column=1)
    tk.Label(janela_reg, text="Y:").grid(row=1, column=0)
    combo_y = ttk.Combobox(janela_reg, values=colnames)
    combo_y.grid(row=1, column=1)
    tk.Button(janela_reg, text="Calcular", command=calcular).grid(row=2, columnspan=2, pady=10)

# --- INTERFACE TKINTER ---
janela = tk.Tk()
janela.title("App DW Moodle - Visualizações")
janela.geometry("700x500")

frame_top = tk.Frame(janela)
frame_top.pack(pady=10)

combo_tabelas = ttk.Combobox(frame_top, values=carregar_tabelas())
combo_tabelas.set("Selecione uma tabela")
combo_tabelas.grid(row=0, column=0, padx=5)
btn_tabela = tk.Button(frame_top, text="Mostrar Tabela", command=mostrar_tabela)
btn_tabela.grid(row=0, column=1, padx=5)

frame_text = tk.Frame(janela)
frame_text.pack()
texto = tk.Text(frame_text, width=80, height=10)
texto.pack()

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=20)

# Botões
btn1 = tk.Button(frame_botoes, text="Bar AVG", command=grafico_bar_avg_contextual)
btn1.grid(row=0, column=0, padx=5)
btn2 = tk.Button(frame_botoes, text="Pie", command=grafico_pie_dinamico)
btn2.grid(row=0, column=1, padx=5)
btn3 = tk.Button(frame_botoes, text="Linha Média", command=grafico_linha_avg_contextual)
btn3.grid(row=0, column=2, padx=5)
btn4 = tk.Button(frame_botoes, text="Rollup", command=grafico_rollup_contextual)
btn4.grid(row=1, column=0, padx=5)
btn5 = tk.Button(frame_botoes, text="HAVING > 5", command=grafico_having_contextual)
btn5.grid(row=1, column=1, padx=5)
btn6 = tk.Button(frame_botoes, text="Estatísticas", command=mostrar_estatisticas)
btn6.grid(row=1, column=2, padx=5)
btn7 = tk.Button(frame_botoes, text="Boxplot", command=mostrar_boxplot)
btn7.grid(row=2, column=0, padx=5)
btn8 = tk.Button(frame_botoes, text="Histograma", command=mostrar_histograma)
btn8.grid(row=2, column=1, padx=5)
btn9 = tk.Button(frame_botoes, text="Regressão", command=abrir_regressao)
btn9.grid(row=2, column=2, padx=5)

janela.mainloop()
