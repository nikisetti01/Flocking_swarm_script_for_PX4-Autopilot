import asyncio
from mavsdk import System
from modules.swarm import Swarm
from modules.droneposition import DronePosition
from loguru import logger
import random
import math
import numpy as np
from modules.CONSTANTS import Constants
from Analytics.monitoring import Monitoring
from Analytics.plotting import plot_data

def deg_to_m(deg) -> float:
    # 1 deg = 111319.9 m
    pass
    return deg * 111319.9
    

def m_to_deg(m) -> float:
    pass
    return m / 111319.9
async def fromswarm_to_2Darray(index,swarm:Swarm):
    """
    Return the Droneposition as a 2Darray with 2 dimensions expressed in metres
    """
    temp0= await swarm.positions
    temp=temp0[index]
    position=np.array([deg_to_m(temp.latitude_deg),deg_to_m(temp.longitude_deg)])
    return position
def fromDronePosition_to_2Darray(position:DronePosition):
    new_pos=np.array([deg_to_m(position.latitude_deg),deg_to_m(position.longitude_deg)])
    return new_pos

async def calculate_distance(index,other,swarm:Swarm)->float:
    temp0= await swarm.positions
    temp=temp0[index]
    temp_other=temp0[other]
    distance=temp.distance_2D_m(temp_other)
    #print("Ecco la distanza", distance)
    return  distance
def normalize(array): 
    length=np.linalg.norm(array)

    normalize_arr=array/length
    return normalize_arr
async def set_next_pos(position,index,swarm:Swarm):
    """
    Before set the new position change the position from meteres to deg
    """
    
    
    position_d=DronePosition(m_to_deg(position[0]),m_to_deg(position[1]),Constants.STANDARD_ALTITUDE)
    print("next stop ",position_d)
    await swarm.set_position(index,position_d)


async def set_next_veloc(vl,index,swarm:Swarm):

    await swarm.change_velocity(index,vl[0],vl[1],0.0,0.0)
    


async def flocking(index,future_position:DronePosition,swarm:Swarm, params):

    cohesion_factor=params[0]
    alignement_factor=params[1]
    separation_factor=params[2]
    start_position= await fromswarm_to_2Darray(index,swarm)
    target= fromDronePosition_to_2Darray(future_position)
   
    average_position=np.array([0.0,0.0])
    num_neighbors=0
    average_velocity=np.array([0.0,0.0])
    separation=np.array([0.0,0.0])
    for other, n in enumerate(swarm.get_drones()):
        if other !=index:
           

            distance= await calculate_distance(index,other,swarm)
           # NEIGHBOR RADIUS is the maximum distance that can exist between the drones to affect the algorithm
            if distance <Constants.NEIGHBOR_RADIUS:
                other_position= await fromswarm_to_2Darray(other,swarm)
                # calculing the average_position
                average_position+=other_position
                temp= await swarm.get_velocity(other)
                
                other_velocity=np.array(temp[:2])
               
                average_velocity+=other_velocity
             
                num_neighbors +=1
            # if the distance is less then separation_radius then there is risk of collisions
            if distance < Constants.SEPARATION_RADIUS :
                # if there is risk of collisions than the algorithm calculates the separation value 
                 diff=start_position-other_position
                 diff /=distance **2
                 separation+=diff
               
            if num_neighbors>0:
                average_position /= num_neighbors
                average_velocity /= num_neighbors
                #calculing cohesion value
                cohesion=(average_position-start_position)*cohesion_factor
                #calculing alignement values
                alignement=average_velocity*alignement_factor
                separation*=separation_factor
                #changing the target_position adding cohesion alignment and separation
                target+=cohesion+alignement+separation
            
                new_direction=normalize(target-start_position)
            
                new_velocity=new_direction*Constants.MODULE_SPEED
                
    if num_neighbors>0:
        
        await    set_next_pos(target,index,swarm)
        await   set_next_veloc(new_velocity,index,swarm)

async def start_flocking(next_position:DronePosition,swarm:Swarm, variances_array, params):
   

    data_collector=[]
    counter_move=0
    temp=await swarm.positions
    temp_position=temp[0]
    print(data_collector)

    while (temp_position.latitude_deg< next_position.latitude_deg and temp_position.longitude_deg< next_position.longitude_deg):
        
        for i in range(Constants.NUM_DRONES):
            await flocking(i,temp_position,swarm,params)
          
            temp_latitude=temp_position.latitude_deg+m_to_deg(Constants.DRONE_PROGRESS )if temp_position.latitude_deg<next_position.latitude_deg else temp_position.latitude_deg
            temp_longitude=temp_position.longitude_deg+m_to_deg(Constants.DRONE_PROGRESS )if temp_position.longitude_deg<next_position.longitude_deg else temp_position.longitude_deg

        temp_position=DronePosition( temp_latitude,temp_longitude,Constants.STANDARD_ALTITUDE)
        await asyncio.sleep(2)
        monitor=Monitoring(swarm)
        data=await monitor.collect_index()
        
        variance_array=await monitor.dispersion_variance()
        variances_array.append(variance_array)
        data_collector.append(data)
        logger.info("Monitoring")
        print(data_collector)
        counter_move+=1

        """
        after 6 steps the test stops and 
        the graphs of the various indices collected over time appear
        """
        if counter_move==Constants.MAX_PASSES :
            plot_data(data_collector)
            break
        await asyncio.sleep(2)


                



