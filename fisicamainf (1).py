from vpython import *
import os
from math import sqrt, pi, sin
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
import threading
import time
#Victor Merker Binda 24.233.086-0
# Paulo Andre de Oliveira Hirata, RA: 24.123.086-1
# Diogo Santos Linna, RA: 24.123.003-6

m = 0
hj = 6.626 * (10 ** -34)  # Constante de Planck em J.s
hev = 4.136 * (10 ** -15)  # Constante de Planck em eV.s

c = 3 * 10 ** 8  # Velocidade da luz no vácuo em m/s
ni = 0
nf = 0
l = 0
a = 0
k = 0
xp = 0
n = 0

def opcao3():
    def simular_niveis_quanticos():
        # Obter os valores dos campos de entrada
        camada_inicial_str = camada_inicial_entry.get()
        camada_salto_str = camada_salto_entry.get()

        # Verificar se os campos de entrada estão vazios
        if camada_inicial_str == '' or camada_salto_str == '':
            messagebox.showerror("Erro", "Por favor, insira valores válidos para a camada inicial e a camada de salto.")
            return

        # Converter os valores para inteiros
        camada_inicial = int(camada_inicial_str)
        camada_salto = int(camada_salto_str)

        energias = [1, 2, 3, 4, 5]  # Níveis de energiahh
        distancias = [2, 3, 4, 5]  # Distâncias entre as linhas

        # Criando cena
        scene = canvas(title="Simulação de Níveis Quânticos", width=800, height=600, center=vector(0, 0, 0), background=color.black)

        # Criando linhas representando os níveis de energia com distâncias diferentes
        linhas = []
        pos_y = 0
        for i, energia in enumerate(energias):
            linha = curve(pos=[vector(-5, pos_y, 0), vector(5, pos_y, 0)], color=color.blue, radius=0.1)
            texto = text(text=f"E{energia}", pos=vector(-6, pos_y, 0), align='center', height=0.3, color=color.white)
            linhas.append(linha)
            if i < len(distancias):
                pos_y += distancias[i]

        # Criando paredes entre as linhas
        parede_esquerda = box(pos=vector(-5, 8, 0), size=vector(0.2, 16, 0.2), color=color.gray(0.5))
        parede_direita = box(pos=vector(5, 8, 0), size=vector(0.2, 16, 0.2), color=color.gray(0.5))

        # Função para criar a partícula representando a bola
        def criar_particula(camada_inicial):
            particula = sphere(pos=vector(-5, sum(distancias[:camada_inicial-1]), 0), radius=0.3, color=color.red)
            particula.velocidade = 4  # Dobrando a velocidade para tornar o movimento mais rápido
            particula.camada = camada_inicial
            return particula


        def mover_particula(particula):
            passou_camada_inicial = False  # Variável para controlar se a partícula passou pela camada inicial
            while True:
                rate(10)
                particula.pos.x += particula.velocidade * 0.1  # Movendo a partícula para a direita

                if particula.pos.x > 5:  # Se a partícula atingir a parede direita
                    particula.pos.x = -5  # Reposicionando a partícula na parede esquerda
                    if particula.camada == camada_inicial:
                        if passou_camada_inicial:
                            particula.camada = camada_salto  # Fazendo a partícula ir para a camada do salto
                            particula.pos.y = sum(distancias[:camada_salto - 1])  # Reposicionando na nova camada
                            particula.pos.x = -5  # Reposicionando a partícula na parede esquerda

                            # Criando o fóton subindo no meio da caixa
                            foton = sphere(pos=vector(0, 8, 0), radius=0.2, color=color.yellow)
                            time.sleep(1.5)  # Tempo de aparição do fóton após o salto
                            foton.visible = False  # Escondendo o fóton

                            time.sleep(1.5)  # Tempo na nova camada antes do retorno
                            for i in range(camada_salto, camada_inicial, -1):  # Descendo nível por nível até o nível inicial
                                particula.camada = i
                                particula.pos.y = sum(distancias[:i - 1])  # Reposicionando na nova camada
                                while particula.pos.x < 5:  # Movendo a partícula até o final do nível
                                    particula.pos.x += particula.velocidade * 0.1
                                    rate(10)
                                time.sleep(0.5)  # Tempo de espera entre os movimentos
                                # Criando o fóton descendo no meio da caixa
                                foton.visible = True  # Mostrando o fóton
                                time.sleep(1.5)  # Tempo de aparição do fóton
                                foton.visible = False  # Escondendo o fóton
                                time.sleep(0.5)  # Tempo de espera antes de descer para o próximo nível
                            particula.camada = camada_inicial  # Retornando para a camada inicial
                            particula.pos.y = sum(distancias[:camada_inicial - 1])  # Reposicionando na camada inicial
                            particula.pos.x = -5  # Reposicionando a partícula na parede esquerda
                            passou_camada_inicial = False  # Resetando a variável para o próximo ciclo
                        else:
                            passou_camada_inicial = True
                    elif particula.camada < camada_salto:
                        for i in range(particula.camada, camada_salto):
                            particula.camada = i
                            particula.pos.y = sum(distancias[:i - 1])  # Reposicionando na nova camada
                            while particula.pos.x < 5:  # Movendo a partícula até o final do nível
                                particula.pos.x += particula.velocidade * 0.1
                                rate(10)
                            time.sleep(0.5)  # Tempo de espera entre os movimentos
                            time.sleep(1.5)  # Tempo em cada nível antes de descer para o próximo

                            # Movendo a partícula por um tempo na camada de salto antes do salto quântico
                        for _ in range(30):
                            particula.pos.x += particula.velocidade * 0.1
                            rate(10)
                            time.sleep(0.1)

                            # Descendo camada por camada antes do salto
                        for i in range(camada_inicial - 1, particula.camada, -1):
                            particula.camada = i
                            particula.pos.y = sum(distancias[:i - 1])  # Reposicionando na nova camada
                            while particula.pos.x < 5:  # Movendo a partícula até o final do nível
                                particula.pos.x += particula.velocidade * 0.1
                                rate(10)
                            time.sleep(0.5)  # Tempo de espera entre os movimentos
                            time.sleep(1.5)  # Tempo em cada nível antes de descer para o próximo

                        else:  # Se a partícula estiver além da camada de salto
                            # Descendo nível por nível até chegar ao nível inicial
                            for i in range(particula.camada, camada_inicial, -1):
                                particula.camada = i
                                particula.pos.y = sum(distancias[:i - 1])  # Reposicionando na nova camada
                                while particula.pos.x < 5:  # Movendo a partícula até o final do nível
                                    particula.pos.x += particula.velocidade * 0.1
                                    rate(10)
                                # Corrigindo a posição x quando a partícula volta aos níveis inferiores
                                if particula.camada == camada_inicial and particula.pos.x > -5:
                                    particula.pos.x = -5
                                time.sleep(0.5)  # Tempo de espera entre os movimentos
                                time.sleep(1.5)  # Tempo em cada nível antes de descer para o próximo

                                # Movendo a partícula por um tempo na camada antes de descer para o próximo nível
                                for _ in range(30):
                                    particula.pos.x += particula.velocidade * 0.1
                                    rate(10)


        particula = criar_particula(camada_inicial)

                        # Criando thread para movimentar a partícula
        thread_mover_particula = threading.Thread(target=mover_particula, args=(particula,))
        thread_mover_particula.start()

    root = tk.Tk()
    root.title("Simulação de Níveis Quânticos - Opção 3")

    # Criando e posicionando os elementos da interface
    camada_inicial_label = tk.Label(root, text="Camada Inicial (1 a 5):")
    camada_inicial_label.grid(row=0, column=0, padx=10, pady=5)
    camada_inicial_entry = tk.Entry(root)
    camada_inicial_entry.grid(row=0, column=1, padx=10, pady=5)

    camada_salto_label = tk.Label(root, text="Camada de Salto (1 a 5):")
    camada_salto_label.grid(row=1, column=0, padx=10, pady=5)
    camada_salto_entry = tk.Entry(root)
    camada_salto_entry.grid(row=1, column=1, padx=10, pady=5)

    simular_button = tk.Button(root, text="Simular", command=simular_niveis_quanticos)
    simular_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    root.mainloop()




def calcEij():
    ei = ni ** 2 * (hj ** 2) / (8 * m * l ** 2)
    return ei


def calcEfj():
    ef = nf ** 2 * (hj ** 2) / (8 * m * l ** 2)
    return ef


def calcEfoton():
    efoton = abs(calcEfev() - calcEiev())
    return efoton


def calcEiev():
    eij = calcEij() / (1.602 * (10 ** -19))
    return eij


def calcEfev():
    efj = calcEfj() / (1.602 * (10 ** -19))
    return efj


def calcLamb():
    lamb = (hev * 3 * (10 ** 8)) / calcEfoton()
    return lamb


def calcFrequencia():
    f = calcEfoton() / hev
    return f


def calcVi():
    vi = sqrt((2 * calcEij()) / m)
    return vi


def calcVf():
    vf = sqrt((2 * calcEfj()) / m)
    return vf


def calcCi():
    ci = 2 * l / ni
    return ci


def calcCf():
    cf = 2 * l / nf
    return cf


def calcKi():
    ki = ni * pi / l
    return ki


def calcKf():
    kf = nf * pi / l
    return kf


def probabilidade(a, b, ni, l):
    integrand = lambda x: 2 / l * sin((ni * pi * x) / l) ** 2
    result, _ = quad(integrand, a, b)
    return result



def calcL():
    l = 2 / a ** 2
    return l


def calcN():
    n = round((k * l) / pi)
    return n


def calcprobop2():
    prob = 2 / l * (sin(n * pi * xp) ** 2)
    return prob


def plot_wave_functions(a, b, ni, nf, l):
    x = np.linspace(a, b, 1000)  # Array de pontos para o eixo x
    ki = ni * pi / l
    kf = nf * pi / l
    psi_i = sqrt(2 / l) * np.sin(ki * x)
    psi_f = sqrt(2 / l) * np.sin(kf * x)

    plt.figure(figsize=(10, 6))

    plt.plot(x, psi_i, label=f'ni{ni}(x)', color='blue')
    plt.plot(x, psi_f, label=f'nf{nf}(x)', color='red')

    plt.title('Funções de Onda')
    plt.xlabel('x (Å)')
    plt.ylabel('ψ')
    plt.legend()
    plt.grid(True)
    plt.savefig('wave_functions.png')
    plt.close()


def plot_probability_distribution(a, b, ni, nf, l):
    x = np.linspace(a, b, 1000)  # Array de pontos para o eixo x
    ki = ni * pi / l
    kf = nf * pi / l
    psi_i = sqrt(2 / l) * np.sin(ki * x)
    psi_f = sqrt(2 / l) * np.sin(kf * x)

    prob_i = (psi_i ** 2) / quad(lambda x: (sqrt(2 / l) * np.sin(ki * x)) ** 2, a, b)[0]
    prob_f = (psi_f ** 2) / quad(lambda x: (sqrt(2 / l) * np.sin(kf * x)) ** 2, a, b)[0]

    plt.figure(figsize=(10, 6))

    plt.plot(x, prob_i, label=f'Probabilidade ni{ni}(x)', color='blue')
    plt.plot(x, prob_f, label=f'Probabilidade nf{nf}(x)', color='red')

    plt.title('Distribuição de Probabilidade')
    plt.xlabel('x (Å)')
    plt.ylabel('|ψ|²')
    plt.legend()
    plt.grid(True)
    plt.savefig('probability_distribution.png')
    plt.close()


def menu():
    print("\nEscolha uma opção:")
    print("1 - Caixa 1D: Determinação da função de onda quântica e outros parâmetros")
    print("2 - Caixa 1D: Cálculo dos parâmetros da caixa e partícula, dada a função da onda")
    print("3 - Sair")




# Função para lidar com o cálculo e exibição dos resultados
def opcao1():
    def calcular_e_exibir_resultados():
        global m, ni, nf, l

        particula = int(particula_entry.get())
        if particula == 1:
            m = 1.67 * (10**-27)
        elif particula == 2:
            m = 9.11 * (10**-31)
        else:
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Opção inválida")
            result_text.config(state=tk.DISABLED)
            return

        ni = int(ni_entry.get())
        nf = int(nf_entry.get())
        l = float(l_entry.get())
        a = float(a_entry.get())
        b = float(b_entry.get())

        eij = calcEij()
        eiev = calcEiev()
        efj = calcEfj()
        efev = calcEfev()
        efoton = calcEfoton()
        lamb = calcLamb()
        f = calcFrequencia()
        vi = calcVi()
        vf = calcVf()
        ci = calcCi()
        cf = calcCf()
        ki = calcKi()
        kf = calcKf()
        area = sqrt(2/l)
        resulti = probabilidade(a, b, ni, l)
        resultf = probabilidade(a, b, nf, l)

        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"ψ{ni} (x) = {area:.4e} . sen({(ki):.4e}.x)\n"
                                    f"ψ{nf} (x) = {area:.4e} . sen({(kf):.4e}.x)\n"
                                    f"E{ni} = {eij:.4e} J ou {eiev:.4e} eV\n"
                                    f"E{nf} = {efj:.4e} J ou {efev:.4e} eV\n"
                                    f"Efoton = {efoton:.4e} eV\n"
                                    f"Comprimento de onda do fóton = {lamb:.4e} m\n"
                                    f"Frequência do fóton = {f:.4e} Hz\n"
                                    f"Velocidade da partícula:\nn = {ni}: v = {vi:.4e} m/s\tn = {nf}: v = {vf:.4e} m/s\n"
                                    f"Comprimento de onda de De Broglie:\nn = {ni}: ƛ = {ci:.4e} m\tn = {nf}: ƛ = {cf:.4e} m\n"
                                    f"A probabilidade da partícula estar entre {a:.4e} e {b:.4e} no nível {ni} é de {resulti*100:.3f} %\n"
                                    f"A probabilidade da partícula estar entre {a:.4e} e {b:.4e} no nível {nf} é de {resultf*100:.3f} %")
        result_text.config(state=tk.DISABLED)

        plot_wave_functions(a, b, ni, nf, l)
        plot_probability_distribution(a, b, ni, nf, l)

    # Criando a janela principal
    root = tk.Tk()
    root.title("Calculadora de Física Quântica")

    # Criando e posicionando os elementos da interface
    particula_label = tk.Label(root, text="Informe qual partícula está pedindo (1 para Próton, 2 para Elétron):")
    particula_label.grid(row=0, column=0, padx=10, pady=5)
    particula_entry = tk.Entry(root)
    particula_entry.grid(row=0, column=1, padx=10, pady=5)

    ni_label = tk.Label(root, text="Digite o n inicial:")
    ni_label.grid(row=1, column=0, padx=10, pady=5)
    ni_entry = tk.Entry(root)
    ni_entry.grid(row=1, column=1, padx=10, pady=5)

    nf_label = tk.Label(root, text="Digite o n final:")
    nf_label.grid(row=2, column=0, padx=10, pady=5)
    nf_entry = tk.Entry(root)
    nf_entry.grid(row=2, column=1, padx=10, pady=5)

    l_label = tk.Label(root, text="Digite a largura do poço potencial infinito em metros:")
    l_label.grid(row=3, column=0, padx=10, pady=5)
    l_entry = tk.Entry(root)
    l_entry.grid(row=3, column=1, padx=10, pady=5)

    a_label = tk.Label(root, text="Informe o valor do início do intervalo:")
    a_label.grid(row=4, column=0, padx=10, pady=5)
    a_entry = tk.Entry(root)
    a_entry.grid(row=4, column=1, padx=10, pady=5)

    b_label = tk.Label(root, text="Informe o valor do final do intervalo:")
    b_label.grid(row=5, column=0, padx=10, pady=5)
    b_entry = tk.Entry(root)
    b_entry.grid(row=5, column=1, padx=10, pady=5)

    calculate_button = tk.Button(root, text="Calcular", command=calcular_e_exibir_resultados)
    calculate_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

    # Criando o widget Text para exibir os resultados
    result_text = tk.Text(root, wrap="word", relief="sunken", state=tk.DISABLED, bg="#f0f0f0", fg="#333333", font=("Helvetica", 10))
    result_text.grid(row=7, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="nsew")

    root.mainloop()

def opcao2():
    def calcular_e_exibir_resultados():
        global a, k, xp, l, m, n

        particula = int(particula_entry.get())
        if particula == 1:
            m = 1.67 * (10 ** -27)
        elif particula == 2:
            m = 9.11 * (10 ** -31)
        else:
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Opção inválida")
            result_text.config(state=tk.DISABLED)
            return

        a = float(a_entry.get())
        k = float(k_entry.get())
        xp = float(xp_entry.get())

        l = calcL()
        n = calcN()
        prob = calcprobop2()

        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"L = {l:.4e} m\n"
                                   f"n = {n}\n"
                                   f"P ({xp}.L) = {prob:.3} dx")
        result_text.config(state=tk.DISABLED)

    # Criando a janela principal
    root = tk.Tk()
    root.title("Calculadora de Física Quântica - Opção 2")

    # Criando e posicionando os elementos da interface
    particula_label = tk.Label(root, text="Informe qual partícula está pedindo (1 para Próton, 2 para Elétron):")
    particula_label.grid(row=0, column=0, padx=10, pady=5)
    particula_entry = tk.Entry(root)
    particula_entry.grid(row=0, column=1, padx=10, pady=5)

    a_label = tk.Label(root, text="Digite o valor de A em metros:")
    a_label.grid(row=1, column=0, padx=10, pady=5)
    a_entry = tk.Entry(root)
    a_entry.grid(row=1, column=1, padx=10, pady=5)

    k_label = tk.Label(root, text="Digite o valor de k em metros:")
    k_label.grid(row=2, column=0, padx=10, pady=5)
    k_entry = tk.Entry(root)
    k_entry.grid(row=2, column=1, padx=10, pady=5)

    xp_label = tk.Label(root, text="Digite a posição x na qual será calculada a probabilidade (informe apenas o número que multiplica L, ex: 0.75L -> informe apenas 0.75):")
    xp_label.grid(row=3, column=0, padx=10, pady=5)
    xp_entry = tk.Entry(root)
    xp_entry.grid(row=3, column=1, padx=10, pady=5)

    calculate_button = tk.Button(root, text="Calcular", command=calcular_e_exibir_resultados)
    calculate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    # Criando o widget Text para exibir os resultados
    result_text = tk.Text(root, wrap="word", relief="sunken", state=tk.DISABLED)
    result_text.grid(row=5, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="nsew")

    root.mainloop()

def main():
    def selecionar_opcao(opcao):
        if opcao == "1":
            opcao1()
        elif opcao == "2":
            opcao2()
        elif opcao == "3":
            opcao3()


        elif opcao == "4":
            print("Saindo...")
            root.quit()
        else:
            print("Opção inválida. Tente novamente.")

    def on_click():
        opcao = opcao_var.get()
        selecionar_opcao(opcao)

    root = tk.Tk()
    root.title("Menu")

    opcao_var = tk.StringVar(root)
    opcao_var.set("1")  # Valor padrão

    opcoes = [("Opção 1 - Caixa 1D: Determinação da função de onda quântica e outros parâmetro Entradas: L, ni, nf, a, b", "1"),
              ("Opção 2 - Caixa 1D:  Cálculo dos parâmetros da caixa e partícula, dada a função da onda\nEntradas: A, k, xp", "2"),
              ("Opção 3 - Simular Níveis Quânticos", "3"),
              ("Sair", "4")]

    for texto, valor in opcoes:
        radio_button = tk.Radiobutton(root, text=texto, variable=opcao_var, value=valor)
        radio_button.pack(anchor=tk.W)

    button = tk.Button(root, text="Selecionar", command=on_click)
    button.pack()

    root.mainloop()

# Chamar a função main() para iniciar o programa

if os.path.exists('wave_functions.png'):
    os.remove('wave_functions.png')
if os.path.exists('probability_distribution.png'):
    os.remove('probability_distribution.png')
main()
