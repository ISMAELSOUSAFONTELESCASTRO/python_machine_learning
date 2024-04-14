from random import uniform, randint
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split as tt
from sklearn import metrics
import time


class Particula:
    def __init__(self, pos, vel, per):
        self.melhor_pos = None
        self.melhor_per = 0
        self.pos = np.array(pos)
        
        self.vel = np.array(vel)
        
        self.per = per
        self.c1 = uniform(0,2)
        self.c2 = uniform(0,2)


    def __str__(self):
        return "pos: {}, per: {:.5f}, \n--------melhor pos: {}, melhor per: {:.5f}".format(list(self.pos), self.per, list(self.melhor_pos), self.melhor_per)
    

    def prox_velocidade(self, melhor_pos_g):
        
        c1 = self.c1
        c2 = self.c2
        inercia = self.vel
        c_comp = c1*(self.melhor_pos - self.pos)
       
        
        s_comp = c2*(melhor_pos_g - self.pos)
        

        prox_vel = inercia + c_comp + s_comp
        prox_vel = prox_vel.astype('int32')
        self.vel = prox_vel


class PSO:
    def __init__(self, tam_enxame, num_interacao, arquivo_csv):
        
        self.tam_enxame = tam_enxame
        self.num_interacao = int(num_interacao)
        self.melhor_pos_geral = None
        self.melhor_per_geral = 0
        self.parametro_max = np.array([99.9999,3])
        self. paramentro_min = np.array([0.00001,0])
        self.arquivo_csv = arquivo_csv
        self.dados = pd.read_csv(str(self.arquivo_csv))
        self.coluna = ['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age']
    
    def gerar_pos_zero(self):
        zero = np.array([0.00001,0])

        return zero

    def gerar_pos_rand(self):
        return np.array([uniform(0.00001,100), randint(0,3)])

    def performace(self, pos):
        X = self.dados[self.coluna]
        y = self.dados.Outcome
        X_treino, X_teste, y_treino, y_teste = tt(X, y, test_size=0.3, random_state=42)
        kernel = {0: 'linear', 1: 'poly', 2: 'rbf', 3: 'sigmoid', 4: 'precomputed'}
        shape = {0: 'ovo', 1: 'ovr'}
        if pos[1]== 0:
            clf = svm.LinearSVC(C = float(pos[0]),max_iter= 10000,dual= True, random_state= 42)
        else:
            clf = svm.SVC(C = float(pos[0]), kernel= kernel[int(pos[1])], decision_function_shape= shape[int(1)], random_state= 42)
        clf.fit(X_treino, y_treino)
        previsao = clf.predict(X_teste)
        return metrics.accuracy_score(y_teste,previsao)
    
    def gerar_part(self):
        zero = self.gerar_pos_zero()
        pos = self.gerar_pos_rand()
        vel = pos - zero
        per = self.performace(pos)
        p = Particula(pos, vel,per)
        p.melhor_pos = pos
        p.melhor_per = per
        return p
    
    
    
    def gerar_enxame(self):
        enxame = []
        for _ in range(self.tam_enxame):
            p = self.gerar_part()
            if p.per > self.melhor_per_geral:
                self.melhor_pos_geral = np.array(list(p.melhor_pos))
                self.melhor_per_geral = p.per
            enxame.append(p)
        return enxame
    
    def andar(self, p):
        p.prox_velocidade(self.melhor_pos_geral)
        
        p.pos += p.vel
        for i in range(len(list(p.pos))):
            if p.pos[i] > self.parametro_max[i]:
                p.pos[i] = self.parametro_max[i]
            if p.pos[i] < self.paramentro_min[i]:
                p.pos[i] = self.paramentro_min[i]
        p.per = self.performace(p.pos)
        if p.per > p.melhor_per:
            p.melhor_per = p.per
            p.melhor_pos = np.array(list(p.pos))
        if p.per > self.melhor_per_geral:
            self.melhor_pos_geral = np.array(list(p.melhor_pos))
            self.melhor_per_geral = p.per
    
    def executar(self):
        inicio = time.time()
        enxame = self.gerar_enxame()
        with open ('/home/ismael/Documentos/PYTHON LEARNING PROJECTS/PYTHON_MACHINE_LEARNING/SVM/PSO_RESsvm.txt', 'w') as file:
            for i in range(self.tam_enxame):
                p = enxame[i]
                file.write(str(p) + '\n')
            file.write("\n\n")
            
        
        with open ('/home/ismael/Documentos/PYTHON LEARNING PROJECTS/PYTHON_MACHINE_LEARNING/SVM/PSO_RESsvm.txt', 'a') as file:
            for _ in range(self.num_interacao):
                for i in range(self.tam_enxame):
                    p = enxame[i]
                    self.andar(p)
                    file.write(str(p) + '\n')
                file.write("\n\n")
            file.write("melhor pos geral: "+ str(list(self.melhor_pos_geral)) +"  "+ "melhor per geral: "+str(self.melhor_per_geral))
            fim = time.time()
            print(fim - inicio)

        
if __name__ == '__main__':

    pso = PSO(10,10,"/home/ismael/Documentos/PYTHON LEARNING PROJECTS/PYTHON_MACHINE_LEARNING/knn/diabetes.csv")
    pso.executar()