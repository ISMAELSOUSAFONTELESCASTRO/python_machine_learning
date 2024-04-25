import numpy as np

class ACO:
    def __init__(self, q_formigas, uniT, a, b) -> None:
        self.q_formigas = q_formigas
        self.uniT = uniT
        self.a = a
        self.b = b
        self.pontos = {
            0:np.array((0,0)),
            1:np.array((2,3)),
            2:np.array((3,6)),
            3:np.array((1,4)),
            4:np.array((7,3))
        }
        self.caminhos = []

    def distancia(self, ponto1, ponto2):
        return np.linalg.norm(ponto1 - ponto2)
    
    def gerarCaminhos(self):
        for i in range(len(self.pontos)):
            for j in range(i + 1 ,len(self.pontos)):
                self.caminhos.append([i,j])
