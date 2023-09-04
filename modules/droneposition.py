from mavsdk import telemetry
from typing import List
import math
from geopy import distance as geo_distance
# http://mavsdk-python-docs.s3-website.eu-central-1.amazonaws.com/plugins/telemetry.html#mavsdk.telemetry.Position
# http://mavsdk-python-docs.s3-website.eu-central-1.amazonaws.com/plugins/telemetry.html#mavsdk.telemetry.PositionBody
# http://mavsdk-python-docs.s3-website.eu-central-1.amazonaws.com/plugins/action.html#mavsdk.action.Action.goto_location

def deg_to_m(deg) -> float:
    # 1 deg = 111319.9 m
    pass
    return deg * 111319.9
    

def m_to_deg(m) -> float:
    pass
    return m / 111319.9

# goto_location(latitude_deg, longitude_deg, absolute_altitude_m, yaw_deg)
# mavsdk.telemetry.PositionBody(x_m, y_m, z_m)
# mavsdk.telemetry.Position(latitude_deg, longitude_deg, absolute_altitude_m, relative_altitude_m)
class DronePosition:
    """
    Rappresentazione della posizione del drone indipendente da quella di MavSDK.

    Implementa i metodi per convertire le posizioni nei vari formati necessari
    (da Telemetry.position a lista di float, da lista di float al
    formato richiesto da action.goto_location, ecc.)
    """
    def __init__(self,
                 latitude_deg:float,
                 longitude_deg:float,
                 absolute_altitude_m:float) -> None:
        self.latitude_deg = latitude_deg
        self.longitude_deg = longitude_deg
        self.absolute_altitude_m = absolute_altitude_m

    @classmethod
    def from_mavsdk_position(cls, pos:telemetry.Position) -> None:
        """
        Istanzia la classe a partire da un elemento Position di MAVSDK.

        Args:
            pos (telemetry.Position): La posizione da cui istanzare la classe
        """
        return cls(pos.latitude_deg, pos.longitude_deg, pos.absolute_altitude_m)

    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    
    # goto_location(latitude_deg, longitude_deg, absolute_altitude_m, yaw_deg)
    def to_goto_location(self, prev_pos:'DronePosition'=None) -> List[float]:
        """
        Converte la posizione nel formato necessario per action.goto_location.

        Args:
            prev_pos (DronePosition, optional): La posizione di partenza.
                Viene utilizzata per calcolare l'angolo di yaw.
                Se non specificata `yaw` = 0. Defaults to None.

        Returns:
            List[float]: Lista di coordinate in formato
                (lat_deg, long_deg, abs_alt_m, yaw)
        """
        if prev_pos == None:
            yaw = 0
        else:
            # ATTENZIONE: i calcoli fatti qui sono solo un'approssimazione
            d_lat = self.latitude_deg - prev_pos.latitude_deg
            d_lon = self.longitude_deg - prev_pos.longitude_deg
        if d_lat !=0:
            tan_angle = 90 + d_lon/d_lat
            yaw = math.atan(tan_angle)
        else : 
           yaw=0
        return (self.latitude_deg, self.longitude_deg, self.absolute_altitude_m, yaw)

    def increment_m(self, lat_increment_m, long_increment_m, alt_increment_m) -> 'DronePosition':
        """
        Incrementa la posizione di un valore specificato in metri.

        Args:
            lat_increment_m (_type_): Incremento di latitudine in metri
            long_increment_m (_type_): Incremento di longitudine in metri 
            alt_increment_m (_type_): Incremento di altezza in metri 

        Returns:
            DronePosition: La nuova DronePosition con i valori incrementati
        """
        # TODO: questo metodo non è molto accurato
        new_lat = self.latitude_deg + m_to_deg(lat_increment_m)
        new_lon = self.longitude_deg + m_to_deg(long_increment_m)
        new_alt = self.absolute_altitude_m + alt_increment_m
        return DronePosition(new_lat, new_lon, new_alt)

    def distance_3D_m(self, point:'DronePosition') -> float:
        # TODO: questo metodo non è molto accurato
        dx_m = deg_to_m(self.longitude_deg - point.longitude_deg)
        dy_m = deg_to_m(self.latitude_deg - point.latitude_deg)
        dz_m = deg_to_m(self.absolute_altitude_m - point.absolute_altitude_m)
        distance = math.sqrt(dx_m**2 + dy_m**2 + dz_m**2)
        return distance

    def distance_2D_m(self, point:'DronePosition') -> float:
        """
        Calcola la distanza tra due punti considerandoli entrambi sulla superficie.

        Args:
            point (DronePosition): Punto da cui calcolare la distanza.

        Returns:
            float: Distanza dal punto `point`
        """
        point1 = (self.latitude_deg, self.longitude_deg)
        point2 = (point.latitude_deg, point.longitude_deg)

        distance = geo_distance.distance(point1, point2).meters
        return distance