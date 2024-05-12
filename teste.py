from MLP import *

mlp = MLP(input= np.array([[2,3], [4,5]]), output= np.array([[1] , [0]]), perceptron_per_hidden_layer= 4, n_hidden_layers= 2)
mlp.initLayers()
mlp.startSinapses(mlp.X[0])
for p in mlp.layers[-1]:
    print(p.weights)

mlp.startBackPropagation()
for p in mlp.layers[-1]:
    print(p.weights)


