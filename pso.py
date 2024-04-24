from random import randint, uniform
import numpy as np
class Formiga:
    def __init__(self):
        self.node = None

    def caminhar(self,caminho):
        self.node.append(caminho)

    def deixarFeromonio(self,caminho):
        caminho.T = caminho.T + 20 



class Caminho:
    def __init__(self, inicio, fim):
        self.inicio = inicio
        self.fim = fim
        self.T = 20
        self.N = None
        self.peso = None
 

    def evaporar(self):
        self.T = self.T*0.9



class ACO:
    def __init__(self,tamanho_ninho):
        self.tamanho_ninho = tamanho_ninho
        self.pontos = {
            0:np.array([0,0]),
            1:np.array([2,3]),
            2:np.array([3,7]),
            3:np.array([2,6]),
            4:np.array([1,3])
        }
        self.trilha = []
        self.soma_p = 0
        self.ninho = []
        self.melhor_caminho = None
    
    def gerarNinho(self):
        self.ninho = [ Formiga for _ in range(self.tamanho_ninho)]
    
    def gerarTrilha(self):
        for i in range(5):
            for f in range(i + 1, 5):
                self.trilha.append(Caminho(i,f))

        
    def fitness(self, caminho):
        caminho.N = 10*np.linalg.norm(self.pontos[caminho.inicio] - self.pontos[caminho.fim])
    
    def gerarDenominador(self):
        for caminho in self.trilha:
            a = randint(1,2)
            b = randint(1,2)
            T = caminho.T
            N = caminho.N
            x = pow(T, a)*pow(N, b)
            caminho.peso = x

            self.soma_p = self.soma_p + x
        
        for caminho in self.trilha:
            caminho.peso = 100*caminho.peso/self.soma_p
    
    
if __name__ == '__main__':
    aco = ACO(100)
    #inicializando atributos:
    aco.gerarNinho()
    aco.gerarTrilha()
    for caminho in aco.trilha:
        aco.fitness(caminho)
    aco.gerarDenominador()

    #Primeiras Formigas

    for formiga in aco.ninho:
        possiveis_caminhos = []
        for i in range (len(aco.trilha)):
            if aco.trilha[i].inicio == 0:
                possiveis_caminhos.append(aco.trilha[i])
