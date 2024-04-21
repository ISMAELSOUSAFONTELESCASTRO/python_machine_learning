from random import randint, choice
class Formiga:
    def __init__(self):
        self.node = None

    def proximoNo(self,caminho):
        self.node = caminho

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
        self.trilha = []
        self.soma_p = 0
        self.ninho = []
        self.melhor_caminho = None
    
    def gerarNinho(self):
        self.ninho = [ Formiga for _ in range(self.tamanho_ninho)]
    
    def gerarTrilha(self):
        for i in range(-500, 501):
            self.trilha.append(Caminho(0,i/10))

        
    def fitness(self, x):
        return -pow(x,2) + 10*x + 100
    
    def gerarDenominador(self):
        for caminho in self.trilha:
            a = randint(0,2)
            b = randint(0,2)
            T = caminho.T
            N = caminho.N
            self.soma_p = self.soma_p + pow(T, a)*pow(N, b)
    
    def peso(self,caminho):
        a = randint(0,2)
        b = randint(0,2)
        T = caminho.T
        N = caminho.N
        caminho.peso = (pow(T, a)*pow(N, b))
    
    
if __name__ == '__main__':
    aco = ACO(100)
    #inicializando atributos:
    aco.gerarNinho()
    aco.gerarTrilha()
    #aco.gerarDenominador()
    pesos = []

    
    for caminho in aco.trilha:
        caminho.N = aco.fitness(caminho.fim)
        aco.peso(caminho)
        pesos.append(caminho.peso)

    for i in pesos:
        print(i)

    '''
    #primeira exploração
    for formiga in aco.ninho:
        caminho = choice(aco.trilha)
        formiga.proximoNo(caminho)
        formiga.deixarFeromonio(caminho)
'''
    
    
