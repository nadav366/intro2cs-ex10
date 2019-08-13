class GameObject:
    """
    A class that is an object in the game.
    The class contains the most basic attributes each object has.
    """
    def __init__(self, x_location, y_location, x_speed=0, y_speed=0):
        """
        Constructor object in game
        :param x_location: number, the position of the object in Axis x
        :param y_location: number, the position of the object in Axis y
        :param x_speed: number, the speed of the object in the x axis
        :param y_speed: number, the speed of the object in the y axis
        """
        self.__x_location = x_location
        self.__x_speed =x_speed
        self.__y_location = y_location
        self.__y_speed = y_speed

    """
    The following functions modify and return object properties-
    """

    def get_x_speed(self): return self.__x_speed

    def get_y_speed(self): return self.__y_speed

    def get_x_location(self): return self.__x_location

    def get_y_location(self): return self.__y_location

    def set_x_speed(self, new_speed): self.__x_speed = new_speed

    def set_y_speed(self, new_speed): self.__y_speed = new_speed

    def set_x_location(self, new_loc): self.__x_location = new_loc

    def set_y_location(self, new_loc): self.__y_location = new_loc
