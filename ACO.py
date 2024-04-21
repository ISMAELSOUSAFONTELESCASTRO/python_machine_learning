from random import randint, uniform
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
        self.pesos = []
    
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
            x = pow(T, a)*pow(N, b)
            caminho.peso = x
            self.pesos.append(x)
            self.soma_p = self.soma_p + x
    
    
if __name__ == '__main__':
    aco = ACO(100)
    #inicializando atributos:
    aco.gerarNinho()
    aco.gerarTrilha()
    for i in aco.trilha:
        i.N = aco.fitness(i.fim)/10
    aco.gerarDenominador()
    print(aco.soma_p)
    print("\n\n")

    dado = uniform(0, aco.soma_p)
    #print(dado)

    pesos = []
    for caminho in aco.trilha:
        pesos.append(caminho.peso)
        #print(caminho.peso)
    
    pesos_nivelados = []
    pesos_nivelados.append(pesos[0])
    
    for i in range(1,len(pesos)):
        pesos_nivelados.append(pesos[i] + pesos_nivelados[i - 1])
        print(pesos_nivelados[i])
    

    

'''
    
    #primeira exploração
    for formiga in aco.ninho:
        caminho = choice(aco.trilha)
        formiga.proximoNo(caminho)
        formiga.deixarFeromonio(caminho)
'''
    
    
