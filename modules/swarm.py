from loguru import logger
from pprint import pprint
from mavsdk import System
from mavsdk import telemetry
from mavsdk.offboard import  VelocityNedYaw
import asyncio
from typing import List, Callable
from modules.systemwrapper import SystemWrapper
from modules.droneposition import DronePosition

class Swarm:
    """
    Creates a drones swarm composed by `drones_number` vehicles at the given addresses or incremental addresses

    Args:
        drones_number (int): number of drones composing the swarm
        drones_addrs (List[int], optional): drone addresses
            Defaults to None.
    Attributes:

    Raises:
        ValueError: drones_number must coincide with the number of drone addresses
    """

    next_drone_address = 14540 
    def __init__(self,
                drones_number:int,
                drones_addrs:List[int]=None) -> None:
        self.__drones_number = drones_number
        self.__positions = []
        self.__drones:List[System] = []

        if drones_addrs == None:
            self.drones_addrs = []
            for i in range(drones_number):
                self.drones_addrs.append(Swarm.next_drone_address)
                Swarm.next_drone_address += 1
        elif drones_number != len(drones_addrs):
            raise ValueError
        else:
            self.drones_addrs = drones_addrs
        logger.info(f"Creating swarm with {self.__drones_number} drones at {self.drones_addrs}")
        """
    the flocking algorithm works by changing the direction and speed module of the drones in a certain time interval
    besides modifying the target position, for this I added methods to the swarm class


        """
    async def set_drone_speed(self, drone, speed_m_s):
        """
        Set the  module velocity of the drone
        """
        await drone.action.set_current_speed(speed_m_s)
        await drone.action.set_maximum_speed(speed_m_s+1.0)
    async def set_swarm_speed(self, speed_m_s):
        """
        Set the module velocity of the swarm
        """
        for drone in self.__drones:
            await self.set_drone_speed(drone,speed_m_s)
            
        logger.info("modifico velocità")
            



   
    async def connect(self):
        """
        Connects to every drone of the swarm simultaneously
        """
        logger.info("Connecting to drones...")
        for a in self.drones_addrs:
            logger.info(f"Connecting to drone@{a}...")
            sysW = SystemWrapper(a)
            drone = await sysW.connect()
            logger.info(f"Connection to drone@{a} completed")
            self.__drones.append(drone)


    async def check_system_connections(self) -> bool:
        """
        Check if all the drones [System] are connected to the base station
        """
        for system in self.__drones:
            async for state in system.core.connection_state():
                if state.is_connected:
                    logger.debug("Drone is connected.")
                    break
                else:
                    logger.debug("Drone is not connected.")
                    return False
        return True

    async def takeoff(self):
        """
        Sends `takeoff` command to each drone of the swarm.
        """

        # assert that all the drones are connected
        ready_for_takeoff = 0
        while not ready_for_takeoff:
            ready_for_takeoff = await self.check_system_connections()

        logger.info("Taking off...")
        for d in self.__drones:
            await d.action.arm()
            await d.action.takeoff()
            await d.action.set_maximum_speed(10)
        logger.info("Takeoff completed")

    async def land(self):
        """
        Sends `land` command to each drone of the swarm.
        """
        logger.info("Landing...")
        for d in self.__drones:
            await d.action.land()
        logger.info("Landing completed")

    @property
    async def positions(self) -> List[DronePosition]:
        """
        Retrieves drones positions

        Returns:
            List[DronePosition]: Current position of each drone
        """
        self.__positions = []
        for d in self.__drones:
            p = await anext(d.telemetry.position())
            pos = DronePosition.from_mavsdk_position(p)
            self.__positions.append(pos)

        return self.__positions
       
    def get_leader(self) -> System:
        """
        Get the first drone of the swarm, which will be called "Leader"
        """
        return self.__drones[0]
    
    def get_drones(self) -> List[System]:
        """
        Get the list of all the drones of the swarm
        """
   

        return self.__drones
    def get_drones_number(self)-> int:
        """
        Get the number of drones
        """
        return self.__drones_number

    async def get_velocity(self, index) :
      """"
      Using the mavdsk telemetry library this function returns the speed of the drone in the three NED components
      """
      drone=self.__drones[index]
      async for velocity_ned in drone.telemetry.velocity_ned():
            return velocity_ned.north_m_s, velocity_ned.east_m_s, velocity_ned.down_m_s
    async def get_single_max_speed(self, index:int)->float:

        try:
            drone = self.__drones[index]
            
            return await drone.action.get_maximum_speed()
        except IndexError:
            logger.error(f"Drone at index {index} not found.")
            return 0.0 
    async def get_swarm_max_speed(self)->float:
        max_speeds = []
        for drone in self.__drones:
            max_speed = await drone.action.get_maximum_speed()
            max_speeds.append(max_speed)
        return max(max_speeds, default=0.0)
    
    async def set_position(self, index, target_position:DronePosition):
        """
        Sets a new position (`target_position`) for the drone identified by its index
        """
        try:
            prev_pos = self.__positions[index]
            drone = self.__drones[index]
        except IndexError:
            return
        
        logger.info(f"Moving drone@{self.drones_addrs[index]}")
        await drone.action.goto_location(*target_position.to_goto_location(prev_pos))
    
    async def set_positions(self, target_positions:List[DronePosition]):
        """
        Sets a new position (`target_position`) for each drone

        Args:
            target_positions (List[DronePosition]): List of target position 
        """
        prev_pos = await self.positions
        print(prev_pos)
        for n, d in enumerate(self.__drones):
            pos = target_positions[n]
            logger.info(f"Moving drone@{self.drones_addrs[n]} to {pos}")
            await d.action.goto_location(*pos.to_goto_location(prev_pos[n]))
    async def get_velocities(self):
        "get the three velocities NED of all the swarm"
        velocities=[]
        for index, drone in enumerate(self.__drones):
            velocity= await self.get_velocity(index)
            velocities.append(velocity)
        return velocities

    async def change_velocity(self, index, velocity_north_m_s, velocity_east_m_s, velocity_down_m_s, yaw_deg):
     """
     Through the offboard library this function modifies the NED components of the speed of the drone
     """
     drone = self.__drones[index]
     offboard = drone.offboard
     velo=await  self.get_velocity(index)
     current_velocity_north=velo[0]
     current_velocity_east=velo[1]
     current_velocity_down=velo[2]     
     await offboard.set_velocity_ned(VelocityNedYaw(current_velocity_north,current_velocity_east,current_velocity_down, 0.0))
 
     await offboard.start()

    # Set the new velocity
     await offboard.set_velocity_ned(VelocityNedYaw(velocity_north_m_s, velocity_east_m_s, velocity_down_m_s, yaw_deg))
     await asyncio.sleep(2) 

    # Turn off Offboard mode

     await offboard.stop()




    


 
    