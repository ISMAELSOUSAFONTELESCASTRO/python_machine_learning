from random import randint, choice, uniform
import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split as tt
from sklearn import metrics
import time

class Algoritimo_genetico:
    def __init__(self,num_ind, num_gen, chance_m,arquivo_csv):
        self.num_ind = num_ind
        self.num_gen = num_gen
        self.chance_m = chance_m
        self.arquivo_csv = arquivo_csv
        self.dados = pd.read_csv(str(self.arquivo_csv))
        #"Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigreeFunction","Age","Outcome"
        #"age","sex","chest pain type","resting bp s","cholesterol","fasting blood sugar","resting ecg","max heart rate","exercise angina","oldpeak","ST slope","target"
        self.coluna = ["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigreeFunction","Age","Outcome"]
        self.melhor_ind = None
        self.melhor_fit = 0


    def gerar_ind(self):
        Cc = uniform(0.1,100)
        kernel = randint(0,3)
        
        return list([Cc, kernel])
    
    def gerar_pop(self):
        populacao = []
        for i in range(self.num_ind):
            populacao.append(self.gerar_ind())
        return populacao
    
    def fitness(self, individuo):
        X = self.dados[self.coluna]
        y = self.dados.Outcome
        X_treino, X_teste, y_treino, y_teste = tt(X, y, test_size=0.3, random_state=42)
        kernel = {0: 'linear', 1: 'poly', 2: 'rbf', 3: 'sigmoid'}
        shape = {0: 'ovo', 1: 'ovr'}
        if individuo[1]== 0:
            clf = svm.LinearSVC(C = float(individuo[0]),max_iter= 10000,dual=False, random_state= 42)
        else:
            clf = svm.SVC(C = float(individuo[0]), kernel= kernel[int(individuo[1])], decision_function_shape= shape[int(1)], random_state= 42)
        clf.fit(X_treino, y_treino)
        previsao = clf.predict(X_teste)
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
        sorteio = 0
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
                p[0] = uniform(0.1,100)
            chance = randint(1,100)
            if chance <= 10:
                p[1] = randint(0,3)
            pop_mutada.append(p)
        return pop_mutada
            




    def finalizar(self):
        with open("evolucaosvm.txt","w") as file:

            #geracao1
            geracao = 1
            geracao_melhor_ind = 1
            inicio = time.time()
            pop = self.gerar_pop()
            
            pop_mutada = pop
            fit = []
            for j in range(self.num_ind):
                fit.append(self.fitness(pop_mutada[j]))
                file.write(str(pop_mutada[j]) + " " + str(fit[j]) + '\n')
            self.melhor_ind = pop_mutada[0]
            self.melhor_fit = fit[0]

            for i in range(self.num_ind):
                if self.melhor_fit < fit[i]:
                    self.melhor_ind = pop_mutada[i]
                    self.melhor_fit = fit[i]

            file.write("\n" + "MELHOR INDIVIDUO:  "+ str(self.melhor_ind) + '\n')
            file.write("SUA GERAÇÃO:  " + str(geracao_melhor_ind) + '\n')
            file.write("SEU FITNESS:  " + str(self.melhor_fit) + '\n')
            file.write("FITNESS MEDIO:" + str(sum(fit)/10) + '\n')
            geracao += 1
            file.write("\n")
            file.write("\n")

            #geracao_seguinte
            for i in range(self.num_gen - 1):
                pop = list(pop_mutada)
                nova_pop = self.gerar_nova(pop)
                pop_mutada = self.mutar(nova_pop)
                fit = []
                for j in range(self.num_ind):
                    fit.append(self.fitness(pop_mutada[j]))
                    file.write(str(pop_mutada[j]) + " " + str(fit[j]) + '\n')

                for i in range(self.num_ind):
                    if self.melhor_fit < fit[i]:
                        self.melhor_ind = pop_mutada[i]
                        self.melhor_fit = fit[i]
                        geracao_melhor_ind = geracao
                file.write("\n" + "MELHOR INDIVIDUO:  "+ str(self.melhor_ind) + '\n')
                file.write("SUA GERAÇÃO:  " + str(geracao_melhor_ind) + '\n')
                file.write("SEU FITNESS:  " + str(self.melhor_fit) + '\n')
                file.write("FITNESS MEDIO:" + str(sum(fit)/10) + '\n')
                geracao += 1
                file.write("\n")
            fim = time.time()
            print('\n')
            print(fim - inicio)






if __name__ == '__main__':
        
    ag = Algoritimo_genetico(10, 10, 10, "diabetes.csv")
    ag.finalizar()
