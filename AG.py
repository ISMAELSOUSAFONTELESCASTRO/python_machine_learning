from random import randint, choice

class Algoritimo_genetico:
    def __init__(self,num_ind, num_gen, chance_m):
        self.num_ind = num_ind
        self.num_gen = num_gen
        self.chance_m = chance_m
        self.melhor_ind = None
        self.atributo = [5,10,15,20,25]

    def gerar_ind(self):
        individuo = []
        for i in range(len(self.atributo)):
            individuo.append(randint(1,self.atributo[i]))
        return individuo
    
    def gerar_pop(self):
        populacao = []
        for i in range(self.num_ind):
            populacao.append(self.gerar_ind())
        return populacao
    
    def fitness(self, individuo):
        soma = 0
        maior = 0
        for i in range(len(self.atributo)):
            soma += individuo[i]
            maior += self.atributo[i]
        return soma/maior
    
    def selecao(self, populacao):
        selecaoH = [choice(populacao), choice(populacao)]
        selecaoM = [choice(populacao), choice(populacao)]

        pai = []
        if self.fitness(selecaoH[0]) > self.fitness(selecaoH[1]):
            pai = selecaoH[0]
        else:
            pai = selecaoH[1]
        
        mae = []
        if self.fitness(selecaoM[0]) > self.fitness(selecaoM[1]):
            mae = selecaoM[0]
        else:
            mae = selecaoM[1]

        return pai, mae
    
    def crossover(self, selecao):
        sorteio = randint(0,3)
        filho1 = []
        filho2 = []
        if sorteio != 0:
            for i in range(sorteio + 1):
                filho1.append(selecao[0][i])
                filho2.append(selecao[1][i])
        else:
            filho1.append(selecao[0][0])
            filho2.append(selecao[1][0])

        if sorteio != 3:
            for i in range(sorteio + 1 ,len(selecao[0])):
                filho1.append(selecao[0][i])
                filho2.append(selecao[1][i])
        else:
            filho2.append(selecao[0][4])
            filho1.append(selecao[1][4])

        return list(filho1), list(filho2)

    def gerar_nova(self, populacao):
        nova_populacao = []
        for i in range(5):
            pai, mae = self.selecao(populacao)
            filho1, filho2 = self.crossover((pai, mae))
            nova_populacao.append(filho1)
            nova_populacao.append(filho2)
        return nova_populacao

    def mutar(self, nova_populacao):
        chance = 0
        a = list(nova_populacao)
        populacao_mutada = []
        for i in range(len(nova_populacao)):
            for j in range(len(self.atributo)):
                chance = randint(1,100)
                if chance <= self.chance_m:
                    nova_populacao[i][j] = randint(1, self.atributo[j])
            populacao_mutada.append(nova_populacao[i])
        return populacao_mutada



    def fitness_populacao(self, populacao):
        soma = 0
        for i in range(self.num_ind):
            soma += self.fitness(populacao[i])
        return soma/self.num_ind
    def finalizar(self):


        #geracao1
        algoritimo = ""
        geracao = 1
        geracao_melhor_ind = 1
        geracao_melhor = 1
        pop = self.gerar_pop()
        nova_pop = self.gerar_nova(pop)
        pop_mutada = self.mutar(nova_pop)
        fitness_pop = self.fitness_populacao(pop_mutada)

        for j in range(10):
            algoritimo += str(pop_mutada[j]) + '\n'
        self.melhor_ind = pop_mutada[0]
        for i in range(self.num_ind):
            if self.fitness(self.melhor_ind) < self.fitness(pop_mutada[i]):
                self.melhor_ind = pop_mutada[i]


        algoritimo += "\nmelhor geracao: " + str(geracao_melhor) + '\n' + str(fitness_pop) + '\n' + "melhor ind: " + '\n' + str(self.melhor_ind) + '\n' +  "geracao: " + str(geracao_melhor_ind) + '\n' + str(self.fitness(self.melhor_ind)) + 2*'\n'


        geracao += 1
        #geracao_seguinte
        for i in range(self.num_gen - 1):
            pop = list(pop_mutada)
            nova_pop = self.gerar_nova(pop)
            pop_mutada = self.mutar(nova_pop)
            for k in range(10):
                algoritimo += str(pop_mutada[k]) + '\n'
            if fitness_pop < self.fitness_populacao(pop_mutada):
                fitness_pop = self.fitness_populacao(pop_mutada)
                geracao_melhor = geracao

            for i in range(self.num_ind):
                if self.fitness(self.melhor_ind) < self.fitness(pop_mutada[i]):
                    self.melhor_ind = pop_mutada[i]
                    geracao_melhor_ind = geracao
            algoritimo += "\nfit atual: " + str(self.fitness_populacao(pop_mutada))
            algoritimo += "\nmelhor geracao: " + str(geracao_melhor) + '\n' + str(fitness_pop) + '\n' + "melhor ind: " + '\n' + str(self.melhor_ind) + '\n' +  "geracao: " + str(geracao_melhor_ind) + '\n' + str(self.fitness(self.melhor_ind)) + 2*'\n'

            geracao += 1

        return algoritimo







if __name__ == '__main__':
        
    ag = Algoritimo_genetico(10, 10, 10)
    with open("/home/ismael/Documentos/PYTHON LEARNING PROJECTS/PYTHON_MACHINE_LEARNING/algoritmo genetico/evolucao.txt","w") as file:
        file.write(ag.finalizar())