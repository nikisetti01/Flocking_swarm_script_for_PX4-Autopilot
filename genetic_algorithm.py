from Flocking import start_flocking
import random
import numpy as np
import asyncio 
from modules.swarm import Swarm
from modules.CONSTANTS import Constants
from loguru import logger 


async def fitness_function(swarm: Swarm,params):
    variances_array=[]
    await start_flocking(Constants.EXAMPLE_DESTINATION ,swarm, variances_array,params)
    for i in range(1, len(variances_array)):
        differences=[]
        differences.append(variances_array[i]- variances_array[i-1])
    print("le differenze",differences)
    max_variation=max(differences)
    
    temporal_growth=sum(differences)
    fitness= 1.0/(temporal_growth+ max_variation)
    
    return fitness
def initialize_population(population_size):
    population=[]
    for _ in range(population_size):
       params= generate_params()
       population.append(params)
    return population
def generate_params():
   cohesion=Constants.COHESION_FACTOR+random.uniform(-Constants.COHESION_FACTOR,+Constants.COHESION_FACTOR)
   alignement=Constants.ALIGNEMENT_FACTOR+ random.uniform(-Constants.ALIGNEMENT_FACTOR,Constants.ALIGNEMENT_FACTOR)
   separation=Constants.SEPARATION_FACTOR+ (random.uniform(-Constants.SEPARATION_FACTOR,+Constants.SEPARATION_FACTOR))/2
   params= [
       cohesion,
       alignement,
       separation
   ]
   return params
def crossover(parent1,parent2) :
   child=[]
   crossover_point= random.randint(0, len(parent1))
   child.extend(parent1[:crossover_point])
   child.extend(parent2[crossover_point:]) 
   return child 


def mutate(individual):
   for i in range(len(individual)):
      if random.random()< Constants.MUTATION_RATE:
         individual[0]+=random.uniform(-Constants.COHESION_FACTOR,Constants.COHESION_FACTOR)/5
         individual[1]+=random.uniform(-Constants.ALIGNEMENT_FACTOR,Constants.ALIGNEMENT_FACTOR)/5
         individual[2]+= random.uniform(-Constants.SEPARATION_FACTOR,Constants.SEPARATION_FACTOR)/10
   return individual


async def genetic_algorithm(swarm:Swarm):
   population= initialize_population(Constants.POPULATION_SIZE)
   for generation in range(Constants.GENERATION):
      fitness_scores=[ await fitness_function(swarm,params) for params in population]
     
      num_parents= int(Constants.PROMOTION_RATE*Constants.POPULATION_SIZE)
      parents=np.argsort(fitness_scores)[: num_parents]
      parents_population=[population[i] for i in parents]
      new_population=[]
      for _ in range(Constants.POPULATION_SIZE-num_parents):
         parent1=random.choice(parents)
         parent2=random.choice(parents)
         child= crossover(population[parent1], population[parent2])
         child=mutate(child)
         new_population.append(child)
      population= parents_population+ new_population

   best_individual=population[np.argmax(fitness_scores)]
   logger.info("FINE ESPERIMENTO")
   print("miglior individuo", best_individual)
   return best_individual
   
     
    






