from modules.droneposition import DronePosition
class Constants:
    #General constants
    NUM_DRONES=5
    STANDARD_ALTITUDE=30
    MODULE_SPEED=5

    #Flocking Algorithm constants
    COHESION_FACTOR=0.025
    ALIGNEMENT_FACTOR=0.2
    SEPARATION_FACTOR=0.5
    SEPARATION_RADIUS=1
    NEIGHBOR_RADIUS=16
    DRONE_PROGRESS=10
    STARTING_RADIUS=8
    MAX_PASSES=6
    EXAMPLE_DESTINATION=DronePosition(47.6,8.6,25)

    # Genetic_algorithm constants
    POPULATION_SIZE=35
    GENERATION=50
    PROMOTION_RATE=0.2
    MUTATION_RATE=0.1


   