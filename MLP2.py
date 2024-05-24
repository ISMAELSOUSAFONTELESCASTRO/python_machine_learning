import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split as tt
import pandas as pd


class Layer:
    def __init__(self, n_per, func_activation = 0):
        self.lr = None
        self.n_per = n_per
        self.p_weights = []
        self.dw = []
        self.bias = None
        self.db = None
        self.chose = func_activation
        self.func_act = None
        self.input = []
        self.outputs = []
        self.linear_out = []

    def sigmoid(self, z):
        return 1/(1 + np.exp(-z)) if z >= -700 else 0
    
    
    def reLU(self, z):
        return np.maximum(0, z)
    
    
        

    def initLayer(self):
        
        for _ in range(self.n_per):
            self.p_weights.append(np.random.uniform(-0.01,0.01, len(self.input)))
            
        self.bias = 0
        

    def layerFoward(self):

        if self.chose == 0:
            self.func_act = self.sigmoid
        elif self.chose == 1:
            self.func_act = self.reLU


        
        self.linear_out = [np.dot(self.p_weights[i], self.input) + self.bias for i in range(self.n_per)]
        self.outputs = np.array(self.func_act(np.array(self.linear_out)))
        



class MLP:
    def __init__(self, X, y, learning_rate = 0.1, n_hiden_layers = 1, perceptron_per_hiden_layer = 16, n_iters = 3, ):
        self.X = X
        self.y = y
        self.lr = learning_rate
        self.n_iters = n_iters
        self.n_hl = n_hiden_layers
        self.pphl = perceptron_per_hiden_layer
        self.layers = []


    def initLayers(self, X_sample):
        self.layers = [Layer(self.pphl, func_activation= 1) for _ in range(self.n_hl)]
        self.layers.append(Layer(len([self.y.iloc[0]]),func_activation= 0))
        
        #X_sample
        self.layers[0].input = X_sample
        self.layers[0].initLayer()
        self.layers[0].layerFoward()

        for i in range(1, len(self.layers)):
            self.layers[i].input = self.layers[i -1].outputs
            self.layers[i].initLayer()
            self.layers[i].layerFoward()

    def derivRELU(self, z):
        return 0 if z <= 0 else 1
    
    def derivSigmoid(self, l):
        return np.exp(-l)/pow((1+ np.exp(-l)),2)

        
    def startBack(self, y_sample):
#dw e db da output layer
        l = np.array(self.layers[-1].linear_out)
        ŷ = np.array(self.layers[-1].outputs)
        derro = self.lr*2*(ŷ - y_sample)*self.derivSigmoid(l)

        



#dw e db das hl
        for i in range(2, self.layers + 1):
            l = np.array(self.layers[-i].linear_out)
            ŷ = np.array(self.layers[-i].outputs)
            derro = self.layers[-i + 1].dw*np.array(self.derivRELU(l)).T

            



    def Update(self):
        for layer in self.layers:
            layer.p_weights += self.lr * layer.dw
            layer.bias += self.lr * layer.db

    def startFoward(self, X_sample):

        #X_sample
        self.layer[0].input = X_sample
        self.layer[0].layerFoward()

        for i in range(1, self.layer):
            self.layer[i].input = self.layer[i -1].p_output
            self.layer[i].layerFoward()


    def fit(self, X_test):

        #train
        self.initLayers(X_sample= X.iloc[0])
        self.startBack(y_sample= y.iloc[0])
        self.Update()
        for i in range(1,len(X)):
            self.startFoward(X_sample = X.iloc[i])
            self.startBack(y_sample= y.iloc[i])
            self.Update()

        for _ in range(self.n_iters):
            for i in range(len(X)):
                self.startFoward(X_sample = X.iloc[i])
                self.startBack(y_sample= y.iloc[i])
                self.Update()
            

        #test
        predicts = []
        for i in range(len(X_test)):
            self.startFoward(X_sample= X_test.iloc[i])
            predict.append(self.layers[-1].outputs)

        return predicts
    
    def accuracy(self,y,y_test):
        return np.sum(y == y_test.iloc)/len(y_test)
    

if __name__ == '__main__':
    
    dados = pd.read_csv('/home/ismael/Documentos/GitHub/python_machine_learning/diabetes.csv')
    coluna = ['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age']

    X = dados[coluna]
    y = dados.Outcome
    X_treino, X_teste, y_treino, y_teste = tt(X, y, test_size=0.3, random_state=1)
    
    
    mlp =MLP(X_treino, y_treino,learning_rate= 0.1, n_iters= 10)

    predicts = mlp.fit(X_teste)
    acurracy = mlp.accuracy(predicts, y_teste)

    print(acurracy)

