import random
import numpy as np 

#function that models the problem
def fitness_function(position):
    return position[0]**2 + position[1]**2 + 1


def random_position():
    #Intervalos designados na especificacao
    return [random.uniform(-512, 512),random.uniform(-512, 512)] 
    
#Some variables to calculate the velocity
W = 0.5
c1 = 0.5
c2 = 0.9
target = 1

#Quantidade de iteracoes vai variar conforme testes
n_iterations = 100

#Taxa de erro
# target_error = float(input("Inform the target error: "))

#1 - Determinar o numero de particulas P da populacao
qtd_particulas = 30

#2 - Inicializar aleatoriamente a posicao inicial(x) de cada particula
#MELHORAR ISSO AQUI
particulas = np.array([np.array(random_position()) for _ in range(qtd_particulas)])

pbest_position = particulas
pbest_fitness_value = np.array([float('inf') for _ in range(qtd_particulas)])
gbest_fitness_value = float('inf')
gbest_position = np.array([float('inf'), float('inf')])

#3 - Velocidade inicial(v) para todas as particulas
#Atribuir numero aleatorio
velocity_vector = ([np.array([0, 0]) for _ in range(qtd_particulas)])
iteration = 0


while iteration < n_iterations:
    for i in range(qtd_particulas):
        #4 a) - Calculando aptidao de 'p'
        fitness_cadidate = fitness_function(particulas[i])
        #print(fitness_cadidate, ' ', particulas[i])
        
        #4 b) - Verificando a melhor posicao de 'p'
        if(pbest_fitness_value[i] > fitness_cadidate):
            pbest_fitness_value[i] = fitness_cadidate
            pbest_position[i] = particulas[i]

        #5 - Verificando a melhor aptdao da populacao
        if(gbest_fitness_value > fitness_cadidate):
            gbest_fitness_value = fitness_cadidate
            gbest_position = particulas[i]
    
    for i in range(qtd_particulas):
        #6 a) - Atualizando velocidade
        new_velocity = (W*velocity_vector[i]) + (c1*random.random()) * (pbest_position[i] - particulas[i]) + (c2*random.random()) * (gbest_position-particulas[i])
        new_position = new_velocity + particulas[i]
        particulas[i] = new_position

    iteration = iteration + 1
    
print("The best position is ", gbest_position, "in iteration number ", iteration)