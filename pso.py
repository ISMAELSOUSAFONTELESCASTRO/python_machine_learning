from random import uniform, randint
import numpy as np

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
        return "pos: {}, per: {:.2f}, melhor pos: {}, melhor per: {:.2f}".format(self.pos, (self.per), self.melhor_pos, self.melhor_per)
    

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
    def __init__(self, tam_enxame, num_interacao):
        
        self.tam_enxame = tam_enxame
        self.num_interacao = int(num_interacao)
        self.melhor_pos_geral = None
        self.melhor_per_geral = 0
        self.parametro_max = np.array([25,25,25])
        self. paramentro_min = np.array([0,0,0])
    
    def gerar_pos_zero(self):
        zero = np.array([12,12,12])

        return zero

    def gerar_pos_rand(self):
        return np.array([randint(0,25), randint(0,25), randint(0,25)])

    def performace(self, pos):
        return sum(list(pos))/75

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
        enxame = self.gerar_enxame()
        with open ('PSO_RES.txt', 'w') as file:
            for i in range(self.tam_enxame):
                p = enxame[i]
                file.write(str(p) + '\n')
            file.write("\n\n")
            
        print("\n\n")
        with open ('PSO_RES.txt', 'a') as file:
            for _ in range(self.num_interacao):
                for i in range(self.tam_enxame):
                    p = enxame[i]
                    self.andar(p)
                    file.write(str(p) + '\n')
                file.write("\n\n")
            file.write("melhor pos geral: "+ str(self.melhor_pos_geral) +"  "+ "melhor per geral: "+str(self.melhor_per_geral)) 

        
if __name__ == '__main__':

    pso = PSO(10,10)
    pso.executar()
