import numpy as np

class Perceptron:
    def __init__(self,alpha = 0.1, n_iters = 1000) -> None:
        self.pesos = None
        self.bias = None
        self.alpha = alpha
        self.n_iters = n_iters


    def fit(self, X, y):
        n_samples, n_features = np.array(X).shape

        #init parameters
        self.pesos = np.random.randint(0,5,n_features)
        self.bias = 0
        Y = np.where(y > 0, 1, 0)

        #learn weights
        for _ in range(self.n_iters):
            for i in range(n_samples):
                linear = 0
                for j in range(n_features):
                    linear += self.pesos[j]*np.array(X)[i][j]
                linear += self.bias
                y_estimado = 1 if linear > 0 else 0
                alpha = 1 if self.alpha >= 1 else self.alpha if self.alpha < 1 and self.alpha > 0 else 0
                for j in range(n_features):
                    self.pesos[j] += (Y[i] - y_estimado)*alpha*np.array(X)[i][j]
                
                self.bias += (Y[i] - y_estimado)*self.alpha
    
    def predict(self, X):
        n_samples, n_features = np.array(X).shape
        output = []
        for i in range(n_samples):
            linear = 0
            for j in range(n_features):
                linear += self.pesos[j]*np.array(X)[i][j]
            linear += self.bias
            y_previsto = 1 if linear > 0 else 0
            output.append(y_previsto)
        return output

            
