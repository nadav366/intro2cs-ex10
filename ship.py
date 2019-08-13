from game_object import *


LIFE_QUANTITY = 3
START_DIRECTION = 0


class Ship(GameObject):
    """
    A class that is the game ship.
    The class inherit GameObject.
    """
    SHIP_RADIOS = 1

    def __init__(self,  x_location, y_location):
        """
        Constructor ship
        :param x_location: number, the position of the object in Axis x
        :param y_location: number, the position of the object in Axis y
        """
        super(Ship, self).__init__(x_location, y_location)  # Builds the object
        self.__direction = START_DIRECTION
        self.__life = LIFE_QUANTITY

    """
    The following functions modify and return ship properties-
    """

    def rotate(self, deg_to_rotate): self.__direction += deg_to_rotate

    def get_direction(self): return self.__direction

    def get_radios(self): return self.SHIP_RADIOS

    def remove_life(self): self.__life -= 1

    def get_life(self): return self.__life

