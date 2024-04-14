from random import randint, choice
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier as KNC
from sklearn.model_selection import train_test_split as tt
from sklearn import metrics

class Algoritimo_genetico:
    def __init__(self,num_ind, num_gen, chance_m,arquivo_csv):
        self.num_ind = num_ind
        self.num_gen = num_gen
        self.chance_m = chance_m
        self.arquivo_csv = arquivo_csv
        self.dados = pd.read_csv(str(self.arquivo_csv))
        self.coluna = ['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age']
        self.melhor_ind = None
        self.melhor_fit = 0


    def gerar_ind(self):
        n_neighbors = randint(1,20)
        weight = randint(0,1)
        
        return list([n_neighbors, weight])
    
    def gerar_pop(self):
        populacao = []
        for i in range(self.num_ind):
            populacao.append(self.gerar_ind())
        return populacao
    
    def fitness(self, individuo):
        X = self.dados[self.coluna]
        y = self.dados.Outcome
        X_treino, X_teste, y_treino, y_teste = tt(X, y, test_size=0.3, random_state=1)
        weight_dic = {0:'uniform', 1:'distance'}
        valor = individuo[1]
        knn = KNC(n_neighbors= individuo[0], weights= weight_dic[int(valor)])
        knn.fit(X_treino, y_treino)
        previsao = knn.predict(X_teste)
        return metrics.accuracy_score(y_teste,previsao)
    
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
        filho1 = []
        filho2 = []
        
        filho1.append(selecao[0][0])
        filho2.append(selecao[1][0])

    
        filho2.append(selecao[0][1])
        filho1.append(selecao[1][1])

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
        pop_mutada= []
        chance = 0
        for p in nova_populacao:
            chance = randint(1,100)
            if chance <= 10:
                p[0] = randint(1,20)
            if chance <= 10:
                p[1] = randint(0,1)
            pop_mutada.append(p)
        return pop_mutada
            




    def finalizar(self):
        with open("evolucaoknn.txt","w") as file:

            #geracao1
            geracao = 1
            geracao_melhor_ind = 1
            pop = self.gerar_pop()
            nova_pop = self.gerar_nova(pop)
            pop_mutada = self.mutar(nova_pop)

            for j in range(self.num_ind):
                file.write(str(pop_mutada[j]) + " " + str(self.fitness(pop_mutada[j])) + '\n')
            self.melhor_ind = pop_mutada[0]
            for i in range(self.num_ind):
                if self.fitness(self.melhor_ind) <= self.fitness(pop_mutada[i]):
                    self.melhor_ind = pop_mutada[i]
            file.write("\n" + "MELHOR INDIVIDUO:  "+ str(self.melhor_ind) + '\n')
            file.write("SUA GERAÇÃO:  " + str(geracao_melhor_ind) + '\n')
            file.write("SEU FITNESS:  " + str(self.melhor_fit) + '\n')
            geracao += 1
            file.write("\n")
            file.write("\n")

            #geracao_seguinte
            for i in range(self.num_gen - 1):
                pop = list(pop_mutada)
                nova_pop = self.gerar_nova(pop)
                pop_mutada = self.mutar(nova_pop)
                for j in range(10):
                    file.write(str(pop_mutada[j]) + " " + str(self.fitness(pop_mutada[j])) + '\n')

                for i in range(self.num_ind):
                    if self.fitness(self.melhor_ind) <= self.fitness(pop_mutada[i]):
                        self.melhor_ind = pop_mutada[i]
                        self.melhor_fit = self.fitness(self.melhor_ind)
                        geracao_melhor_ind = geracao
                file.write("\n" + "MELHOR INDIVIDUO:  "+ str(self.melhor_ind) + '\n')
                file.write("SUA GERAÇÃO:  " + str(geracao_melhor_ind) + '\n')
                file.write("SEU FITNESS:  " + str(self.melhor_fit) + '\n')
                geracao += 1
                file.write("\n")






if __name__ == '__main__':
        
    ag = Algoritimo_genetico(10, 10, 10, "diabetes.csv")
    ag.finalizar()
