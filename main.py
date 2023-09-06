import asyncio
from mavsdk import System
from modules.swarm import Swarm
from modules.droneposition import DronePosition
from loguru import logger
import random
import math
from Flocking import start_flocking
from modules.CONSTANTS import Constants
from genetic_algorithm import genetic_algorithm





def deg_to_m(deg) -> float:
    # 1 deg = 111319.9 m
    pass
    return deg * 111319.9
    

def m_to_deg(m) -> float:
    pass
    return m / 111319.9


async def main():
    """
    Before starting the flocking algorithm, 
    the drones are randomly moved in an 8m circular area
    """
    
    swarm=Swarm(Constants.NUM_DRONES)
    await swarm.connect()
    await swarm.takeoff()
    positions=[]
    posizioni = await swarm.positions
    
    start=posizioni[0]
    for i in range(Constants.NUM_DRONES):
        random_deviation_north=random.uniform(-Constants.STARTING_RADIUS,Constants.STARTING_RADIUS)
        random_deviation_east=random.uniform(-Constants.STARTING_RADIUS,Constants.STARTING_RADIUS)

        new_latitude=start.latitude_deg+m_to_deg(random_deviation_north)
        new_longitudine=start.longitude_deg+m_to_deg(random_deviation_east)
        new_position=DronePosition(new_latitude,new_longitudine,start.absolute_altitude_m)
        positions.append(new_position)
        
   
    await swarm.set_positions(positions)
    
    params=[Constants.COHESION_FACTOR,Constants.ALIGNEMENT_FACTOR,Constants.SEPARATION_FACTOR]


    variances_array=[]
    await start_flocking(Constants.EXAMPLE_DESTINATION,swarm,
    variances_array,  params   )
    await genetic_algorithm(swarm)
      
        
        




if __name__=="__main__":
   asyncio.get_event_loop().run_until_complete(main())
    


    
    
