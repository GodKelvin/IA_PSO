import random
import numpy as np 

#function that models the problem
def fitness_function(position):
    return position[0]**2 + position[1]**2 + 1

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
n_particles = 30

#2 - Inicializar aleatoriamente a posicao inicial(x) de cada particula
#MELHORAR ISSO AQUI
particle_position_vector = np.array([np.array([(-1) ** (bool(random.getrandbits(1))) * random.random()*50, (-1)**(bool(random.getrandbits(1))) * random.random()*50]) for _ in range(n_particles)])

pbest_position = particle_position_vector
pbest_fitness_value = np.array([float('inf') for _ in range(n_particles)])
gbest_fitness_value = float('inf')
gbest_position = np.array([float('inf'), float('inf')])

#3 - Velocidade inicial(v) para todas as particulas
velocity_vector = ([np.array([0, 0]) for _ in range(n_particles)])
iteration = 0


while iteration < n_iterations:
    for i in range(n_particles):
        #4 a) - Calculando aptidao de 'p'
        fitness_cadidate = fitness_function(particle_position_vector[i])
        #print(fitness_cadidate, ' ', particle_position_vector[i])
        
        #4 b) - Verificando a melhor posicao de 'p'
        if(pbest_fitness_value[i] > fitness_cadidate):
            pbest_fitness_value[i] = fitness_cadidate
            pbest_position[i] = particle_position_vector[i]

        #5 - Verificando a melhor aptdao da populacao
        if(gbest_fitness_value > fitness_cadidate):
            gbest_fitness_value = fitness_cadidate
            gbest_position = particle_position_vector[i]
    
    for i in range(n_particles):
        #6 a) - Atualizando velocidade
        new_velocity = (W*velocity_vector[i]) + (c1*random.random()) * (pbest_position[i] - particle_position_vector[i]) + (c2*random.random()) * (gbest_position-particle_position_vector[i])
        new_position = new_velocity + particle_position_vector[i]
        particle_position_vector[i] = new_position

    iteration = iteration + 1
    
print("The best position is ", gbest_position, "in iteration number ", iteration)