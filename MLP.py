from Perceptronnn import *

class MLP:
    def __init__(self, n_interactions = 1000, n_hidden_layers = 1,perceptron_per_hidden_layer = 1, input = None, output = None, lr = 1) -> None:
        self.n_itr = n_interactions
        self.n_hl = n_hidden_layers
        self.pphl = perceptron_per_hidden_layer
        self.layers = []
        self.X = np.array(input)
        self.y = output
        self.lr = lr

    
    def initLayers(self):

        #Hidden layers
        for _ in range(self.n_hl):
            layer = []
            for _ in range(self.pphl):
                p = Perceptron(learning_rate= self.lr)
                layer.append(p)
            self.layers.append(layer)

        #output layer
        layer = []
        for _ in range(len(self.y[0])):
            p = Perceptron(learning_rate= self.lr)
            layer.append(p)
        self.layers.append(layer)


    def startSinapses(self, x_sample):
        #hidden layer 1
        sinapses = []
        for  p in self.layers[0]:
            p.initP(x_sample)
            sinapses.append(p.output)

        #hidden layers
    
        for layer in self.layers[1:-1]:
            sinapses_ph = []
            for  p in layer:
                p.initP(sinapses)
                sinapses_ph.append(p.output)
            sinapses = sinapses_ph

        #output layer
        sinapses_ph = []
        for p in self.layers[-1]:
            p.initP(sinapses)
            sinapses_ph.append(p.output)
        
    
    def startBackPropagation(self):

        #output layer

        for i in range(len(self.layers[-1])):
            y_ = self.y[i]
            self.layers[-1][i].em = self.layers[-1][i].output*(1-self.layers[-1][i].output)*(y_ -self.layers[-1][i].output)
            for j in range(len(self.layers[-1][i].weights)):
                self.layers[-1][i].weights[j] += self.lr*self.layers[-1][i].em*self.layers[-1][i].output


        


        
