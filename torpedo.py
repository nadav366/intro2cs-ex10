from game_object import *


class Torpedo(GameObject):
    """
    A class that is torpedo in the game.
    The class inherit GameObject.
    """
    RADIOS = 4

    def __init__(self,  x_location, y_location, x_speed, y_speed, direction):
        """
        Constructor new torpedo
        :param x_location: number, the position of the object in Axis x
        :param y_location: number, the position of the object in Axis y
        :param x_speed: number, the speed of the object in the x axis
        :param y_speed: number, the speed of the object in the y axis
        :param direction: number, direction of the torpedo
        """
        # Builds the object -
        super(Torpedo, self).__init__(x_location, y_location, x_speed, y_speed)
        self.__direction = direction

    """
    The following functions modify and return torpedo properties-
    """

    def set_direction(self, new_dirc): self.__direction = new_dirc

    def get_direction(self): return self.__direction

    def get_radios(self): return self.RADIOS

