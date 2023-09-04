import asyncio
from mavsdk import System
from modules.swarm import Swarm
from modules.droneposition import DronePosition
from loguru import logger
import random
import math
import numpy as np
from itertools import combinations
class Monitoring:
    def __init__(self,swarm:Swarm) -> None:

        """
        the class calculates movement indices of the drone swarm like variance dispersion
        """
        self.__swarm=swarm
        

        pass
    async def average_dispersion(self)-> int:
        """
        Return average_dispersion of the drone swarm as the average of the distances of all pairs of drones
        """
        positions= await  self.__swarm.positions
        distances=[]
        for drone1,drone2 in combinations(positions,2):
            distance=drone1.distance_2D_m(drone2)
            distances.append(distance)
        if distances:
         average_dispersion=sum(distances)/len(distances)
         
         return average_dispersion
        else: 
           return 0.0
        


    async def dispersion_variance(self)-> int: 
       """
       Likiwise this method return the dispersion variance
       """
       positions= await self.__swarm.positions
       distances=[]
       average_dispersion = await self.average_dispersion()
       for drone1, drone2 in combinations(positions,2):
           distance = drone1.distance_2D_m(drone2)  #
           difference_squared = (distance - average_dispersion) ** 2
           distances.append(difference_squared)
       if distances:
          variance= sum(distances)/len(distances)
          return variance
       else :
          return 0.0
       
    async def average_velocity(self):
       """
       Return the average velocity considering only north velocities and east velocities 
       """
       velocities= await self.__swarm.get_velocities()
       if velocities:
       
        average_velocity = (
            sum(v[0] for v in velocities) / len(velocities),
            sum(v[1] for v in velocities) / len(velocities)
        )
        return average_velocity
    
       else:
         return (0.0, 0.0)  
       
    async def velocity_variance(self):
     velocities= await self.__swarm.get_velocities()
     average_velocity=await self.average_velocity()
     if velocities:
        
        variance = (
            sum((v[0] - average_velocity[0]) ** 2 for v in velocities) / len(velocities),
            sum((v[1] - average_velocity[1]) ** 2 for v in velocities) / len(velocities)
        )
        return variance
     else:
        return (0.0, 0.0)  
    async def collect_index(self):
          """
          This function return a dictionary with all the indexes calculated by the functions before
          """
       
      
          average_dispersion= await self.average_dispersion()
          dispersion_variance=await self.dispersion_variance()
          average_velocity= await self.average_velocity()
          velocity_variance= await self.velocity_variance()
      
          return {
        "average_dispersion": average_dispersion,
        "dispersion_variance": dispersion_variance,
        "average_velocity": average_velocity,
        "velocity_variance": velocity_variance
    }

 

       
     
        

          
       


       
       

    




