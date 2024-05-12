import numpy as np


def unit_step_func(x):
    return 1/(1+pow(2.71828182845904523536, -x))

class Perceptron:

    def __init__(self, learning_rate=1):
        self.lr = learning_rate
        self.activation_func = unit_step_func
        self.weights = None
        self.em = None
        self.bias = None
        self.output = None

    

    def initP(self, x):
        n_features = len(x)

        # init parameters
        self.weights = np.random.uniform(0.1,1, n_features)
        self.bias = 0

        # learn weights
        linear_output = np.dot(x, self.weights) + self.bias
        y_predicted = self.activation_func(linear_output)

        self.output = y_predicted

    def Forward(self, x):

        linear_output = np.dot(x, self.weights) + self.bias
        y_predicted = self.activation_func(linear_output)

        self.output = y_predicted



    def predict(self, X):
        linear_output = np.dot(X, self.weights) + self.bias
        y_predicted = self.activation_func(linear_output)
        return y_predicted
    

            
            



