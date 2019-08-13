from torpedo import *
import math


class SpecialTorpedo(Torpedo):
    """
    A class that is special torpedo in the game.
    The class inherit Torpedo.
    """
    MAX_SPEED = 4.5

    def __init__(self,  x_location, y_location, x_speed, y_speed, direction):
        """
        Constructor new special torpedo
        :param x_location: number, the position of the object in Axis x
        :param y_location: number, the position of the object in Axis y
        :param x_speed: number, the speed of the object in the x axis
        :param y_speed: number, the speed of the object in the y axis
        :param direction: number, direction of the torpedo
        """
        # Builds A normal torpedo -
        super(SpecialTorpedo, self)\
            .__init__(x_location, y_location, x_speed, y_speed, direction)
        # variable containing the asteroid followed by the torpedo now,
        # Begins to empty, because in the construction not yet "chooses"
        # after whom to follow
        self.asteroid_trace = None

    def update_speed(self, new_asdro=None):
        """
        A function that updates the direction and speed of the torpedo,
        corresponding to the tracked asteroid.
        :param new_asdro: A new asteroid to track.
                None if there is no update.
        """
        # Check for an update for asteroid-
        if new_asdro:
            self.asteroid_trace = new_asdro

        # Calculation of distances to asteroid-
        x_distance = \
            self.get_x_location() - self.asteroid_trace.get_x_location()
        y_distance = \
            self.get_y_location() - self.asteroid_trace.get_y_location()

        # Speed ​​limit on speed size-
        tot_speed = (self.get_x_speed()**2 + self.get_y_speed()**2)**0.5
        tot_speed = max(min(tot_speed, self.MAX_SPEED), - self.MAX_SPEED)

        # Calculation of angle to an asteroid-
        tan_result = math.atan(y_distance / x_distance)
        if x_distance > 0:
            tan_result += math.pi

        # The speed distribution according to the axes -
        new_x_speed = tot_speed * math.cos(tan_result)
        new_y_speed = tot_speed * math.sin(tan_result)

        # Updating the parameters of the trapeze-
        self.set_direction(math.degrees(tan_result))
        self.set_x_speed(new_x_speed)
        self.set_y_speed(new_y_speed)
