from random import randint, choice
class Formiga:
    def __init__(self):
        self.node = None

    def proximoNo(self,caminho):
        self.node = caminho

    def deixarFeromonio(self,Caminho):
        Caminho.T = Caminho.T + 10 


class Caminho:
    def __init__(self, inicio, fim):
        self.inicio = inicio
        self.fim = fim
        self.T = 10
        self.N = 1
 

    def evaporar(self):
        self.T = self.T*0.9



    

class ACO:
    def __init__(self,tamanho_ninho):
        self.tamanho_ninho = tamanho_ninho
        self.trilha = None
        self.soma_p = 0
        self.ninho = None
        self.melhor_caminho = None
    
    def gerarNinho(self):
        self.ninho = [ Formiga for _ in range(self.tamanho_ninho)]
    
    def gerarTrilha(self):
        trilha = []
        for i in range(-5000, 5001):
            trilha.append(Caminho(0,i/100))
        self.trilha = trilha

        
        

    def fitness(x):
        return pow(x,2) - 100
    
    def gerarDenominador(self):
        for caminho in self.trilha:
            a = randint(0,2)
            b = randint(0,2)
            T = caminho.T
            N = caminho.N
            self.soma_p = self.soma_p + pow(T, a)*pow(N, b)
    
    def probalidade(self,caminho):
        a = randint(0,2)
        b = randint(0,2)
        T = caminho.T
        N = caminho.N
        return (pow(T, a)*pow(N, b))/(self.soma_p)
    
    
if __name__ == '__main__':
    aco = ACO(100)
    #inicializando atributos:
    aco.gerarNinho
    aco.gerarTrilha
    aco.gerarDenominador

    #primeira exploração
    for formiga in aco.ninho:
        caminho = choice(aco.trilha)
        formiga.proximoNo(caminho)
        formiga.deixarFeromonio(caminho)
    
