from game_object import *


class Asteroid(GameObject):
    """
    A class that is Asteroid in the game ship.
    The class inherit GameObject.
    """
    def __init__(self, x_location, y_location, x_speed, y_speed, size):
        """
        Constructor new Asteroid
        :param x_location: number, the position of the object in Axis x
        :param y_location: number, the position of the object in Axis y
        :param x_speed: number, the speed of the object in the x axis
        :param y_speed: number, the speed of the object in the y axis
        :param size: Integer, Size of the asteroid
        """
        # Builds the object-
        super(Asteroid, self).__init__(x_location, y_location, x_speed, y_speed)
        self.__size = size

    def has_intersection(self, obj):
        """
        A function that checks whether an asteroid collides with another object
        :param obj: Any object in the game
        :return: True if they collide and a different False
        """
        distance = ((obj.get_x_location() - self.get_x_location()) ** 2
                    + (obj.get_y_location() -
                       self.get_y_location()) ** 2) ** 0.5

        if distance <= self.get_radios() + obj.get_radios():
            return True
        return False

    """
    The following functions modify and return asteroid size-
    """

    def get_radios(self): return self.__size * 10 - 5

    def get_size(self): return self.__size

