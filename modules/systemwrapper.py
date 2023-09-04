from loguru import logger
from mavsdk import System
import random

class SystemWrapper:
    """
    Nasconde parte della complessità della classe System di MavSDK.

    Permette di istanziare un elemento della classe System e di
    connetervicisi. 
    """

    @logger.catch
    def __init__(self,
                 system_addr:int) -> None:
        """
        Crea un System all'indirizzo specificato

        Args:
            system_addr (int): Indirizzo del System (il drone)
        """
        self.system_addr = system_addr
        # la porta casuale è copiata da uno script, ancora devo capirne il motivo
        self.server_port = random.randint(1000, 65535)

        logger.debug(f"Creating System: system_addr={self.system_addr}, server_port={self.server_port}")
        self.system = System(port=self.server_port)
    
    @logger.catch
    async def connect(self) -> System:
        """
        Effettua la connessione a un System (il drone).

        Per ridurre la complessità, dall'esterno è accessibile solo un drone già
        connesso.

        Returns:
            L'istanza di System già connessa.
        """
        logger.debug(f"Connecting to system@{self.system_addr}")
        await self.system.connect(f"udp://:{self.system_addr}")
        async for state in self.system.core.connection_state():
            if state.is_connected:
                logger.debug("Connection completed")
                break

        logger.debug("Waiting for drone to have a global position estimate...")
        async for health in self.system.telemetry.health():
            if health.is_global_position_ok and health.is_home_position_ok:
                logger.debug("Global position estimate OK")
                break
        return self.system
    