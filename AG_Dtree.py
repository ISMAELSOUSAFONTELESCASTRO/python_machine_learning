from random import randint, choice, uniform
import pandas as pd
from sklearn.tree import DecisionTreeClassifier 
from sklearn.model_selection import train_test_split 
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
        max_depth = randint(1,1000)
        criterion = randint(0,2)
        min_sample_splits = round(uniform(0,1),4)
        return [max_depth, criterion, min_sample_splits]
    
    def gerar_pop(self):
        populacao = []
        for i in range(self.num_ind):
            populacao.append(self.gerar_ind())
        return populacao
    
    def fitness(self, individuo):
        X = self.dados[self.coluna]
        y = self.dados.Outcome
        criterion_dic = {0:'gini', 1:'entropy', 2:'log_loss'}
        X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.3, random_state=1)
        valor = individuo[1]
        arvore = DecisionTreeClassifier(max_depth= int(individuo[0]), criterion= criterion_dic[int(valor)], min_samples_split=individuo[2])
        arvore.fit(X_treino, y_treino)

        previsao = arvore.predict(X_teste)
        acuracia = metrics.accuracy_score(y_teste, previsao)
        return acuracia
    
    
    
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
        sorteio = randint(0,1)
        filho1 = []
        filho2 = []
        if sorteio != 0:
            for i in range(sorteio + 1):
                filho1.append(selecao[0][i])
                filho2.append(selecao[1][i])
        else:
            filho1.append(selecao[0][0])
            filho2.append(selecao[1][0])

        if sorteio != 1:
            for i in range(sorteio + 1 ,len(selecao[0])):
                filho1.append(selecao[0][i])
                filho2.append(selecao[1][i])
        else:
            filho2.append(selecao[0][2])
            filho1.append(selecao[1][2])

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
        populacao_mutada = []
        for i in range(len(nova_populacao)):
            chance = randint(1,100)
            if chance <= self.chance_m:
                    nova_populacao[i][0] = randint(1, 1000)
            populacao_mutada.append(nova_populacao[i])
            chance = randint(1,100)
            if chance <= self.chance_m:
                    nova_populacao[i][1] = randint(0,2)
            populacao_mutada.append(nova_populacao[i])
            chance = randint(1,100)
            if chance <= self.chance_m:
                    nova_populacao[i][2] = round(uniform(0,1),4)
            populacao_mutada.append(nova_populacao[i])
        return populacao_mutada

    def finalizar(self):
        with open("/home/ismael/Documentos/PYTHON LEARNING PROJECTS/PYTHON_MACHINE_LEARNING/knn/evolucaodtree.txt","w") as file:

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
        
    ag = Algoritimo_genetico(10, 10, 10, "/home/ismael/Documentos/PYTHON LEARNING PROJECTS/PYTHON_MACHINE_LEARNING/knn/diabetes.csv")
    ag.finalizar()
    