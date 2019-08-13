from screen import Screen
import sys
import random
import math

from ship import *
from asteroid import *
from torpedo import *
from special_torpedo import *

DEFAULT_ASTEROIDS_NUM = 5
DEG_ROTATE_FER_PRESS = 7
MAX_SPEED = 4
MIN_SPEED = 1
REGULAR_TORP_AMOUNT = 10
SPECIAL_TORP_AMOUNT = 5
REGULAR_TORP_LIFE = 200
SPECIAL_TORP_LIFE = 150
NEW_LIFE_TIME = 0
NEW_SCORE = 0
SIZE_OF_NEW_ASTRO = 3
VERY_LARGE_NUM = 100000

SCORING = {
    3: 20,
    2: 50,
    1: 100
}

CRASH_TITLE = "CRASH!!"
CRASH_MSG = "You hit an asteroid. Try to be more careful."

END_TITLE = "game over!!"
END_OF_ASTRO_MSG = "You won!!\nAll asteroids destroyed!"
END_OF_LIFE_MSG = "You lose!!\nYou're out of life!"
QUIT_MSG = "You left.\nCome back again!"


class GameRunner:
    """
    An object that runs the game
    """
    X_DELTA = Screen.SCREEN_MAX_X - Screen.SCREEN_MIN_X
    Y_DELTA = Screen.SCREEN_MAX_Y - Screen.SCREEN_MIN_Y

    def __init__(self, asteroids_amount):
        """
        Constructor for the game
        :param asteroids_amount: An integer, the number of asteroids in game
        """
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

        x_loc, y_loc = self.__get_random_loc()
        self.__ship = Ship(x_loc, y_loc)

        # Collections that will contain all objects in the game-
        self.__torpedo_dict = dict()
        self.__special_torpedo_dict = dict()
        self.__asteroids_set = set()
        self.__score = NEW_SCORE  # Game Score

        # Add the asteroids to the game-
        for i in range(asteroids_amount):
            new_asteroid = self.__get_asteroid_loc()
            self.__asteroids_set.add(new_asteroid)

    # General Help Functions-

    def __get_random_loc(self):
        """
        A function that returns random coordinates in a game
        """
        x_loc = random.randint(Screen.SCREEN_MIN_X, Screen.SCREEN_MAX_X)
        y_loc = random.randint(Screen.SCREEN_MIN_Y, Screen.SCREEN_MAX_Y)
        return x_loc, y_loc

    def __get_distance(self, obj1, obj2):
        """
        A function that calculates and returns the distance between two objects
        :param obj1: object in the game
        :param obj2: object in the game
        :return: Distance between objects
        """
        distance = ((obj1.get_x_location() - obj2.get_x_location()) ** 2
                    + (obj1.get_y_location() - obj2.get_y_location()) ** 2) \
                   ** 0.5
        return distance

    # Functions location and speed update -

    def __move_object(self, game_obj):
        """
        A function that updates the body position in the game,
        depending on its speed
        The function follows the given formula.
        :param game_obj: Any object in the game
        """
        # Calculate x axis-
        x_min = Screen.SCREEN_MIN_X
        new_x_cor = (game_obj.get_x_speed() + game_obj.get_x_location() -
                     x_min) % self.X_DELTA + x_min
        game_obj.set_x_location(new_x_cor)

        # Calculate y axis
        y_min = Screen.SCREEN_MIN_Y
        new_y_cor = (game_obj.get_y_speed() + game_obj.get_y_location() -
                     y_min) % self.Y_DELTA + y_min
        game_obj.set_y_location(new_y_cor)

    def __move_all_object(self):
        """
        A function that updates the location of all the objects in the game
        """
        self.__move_object(self.__ship)

        for astero in self.__asteroids_set:
            self.__move_object(astero)

        self.__move_all_torp()
        self.__move_all_s_torp()

    def __move_all_torp(self):
        """
        A function that updates the location of all the regular torpedoes
        The function updates the running time of each torpedo, and remove
        the torpedo constitution runs out of time
        """
        bad_torp = None
        for torp in self.__torpedo_dict:
            if self.__torpedo_dict[torp] < REGULAR_TORP_LIFE:
                self.__move_object(torp)
                self.__torpedo_dict[torp] += 1
            else:
                bad_torp = torp
        if bad_torp:
            self.__screen.unregister_torpedo(bad_torp)
            del self.__torpedo_dict[bad_torp]

    def __move_all_s_torp(self):
        """
        A function that updates the location of all the special torpedoes
        The function updates the running time of each torpedo, and remove
        the torpedo constitution runs out of time
        """
        bad_s_torp = None
        for s_torp in self.__special_torpedo_dict:
            if self.__special_torpedo_dict[s_torp] < SPECIAL_TORP_LIFE:
                self.__move_object(s_torp)
                self.__special_torpedo_dict[s_torp] += 1
                # Updating the missile's speed according to the asteroid-
                if self.__special_torpedo_dict[s_torp] % 5 == 0:
                    # Search for a new asteroid to follow-
                    if self.__special_torpedo_dict[s_torp] % 20 == 0:
                        choose_astro = self.__get_clooser_astro(s_torp)
                    else:
                        choose_astro = None
                    s_torp.update_speed(choose_astro)
            else:
                bad_s_torp = s_torp
        if bad_s_torp:  # Delete a torpedo that runs out of time -
            self.__screen.unregister_torpedo(bad_s_torp)
            del self.__special_torpedo_dict[bad_s_torp]

    def __draw_all_obj(self):
        """
        A function that draw all objects in the game
        """
        self.__screen.draw_ship(self.__ship.get_x_location(),
                                self.__ship.get_y_location(),
                                self.__ship.get_direction())
        for astero in self.__asteroids_set:
            self.__screen.draw_asteroid(astero,
                                        astero.get_x_location(),
                                        astero.get_y_location())
        for torp in self.__torpedo_dict:
            self.__screen.draw_torpedo(torp,
                                       torp.get_x_location(),
                                       torp.get_y_location(),
                                       torp.get_direction())
        for s_torp in self.__special_torpedo_dict:
            self.__screen.draw_torpedo(s_torp,
                                       s_torp.get_x_location(),
                                       s_torp.get_y_location(),
                                       s_torp.get_direction())

    # Functions related to new asteroids-

    def __get_asteroid_loc(self):
        """
        A function that finds a valid place and speed for a new asteroid.
        :return: An asteroid object, with a valid location and speed
        """
        x_speed = random.randint(MIN_SPEED, MAX_SPEED)
        y_speed = random.randint(MIN_SPEED, MAX_SPEED)
        while True:
            x_loc, y_loc = self.__get_random_loc()
            new_astroid = \
                Asteroid(x_loc, y_loc, x_speed, y_speed, SIZE_OF_NEW_ASTRO)
            # Check that the location does not collide ship or other asteroid
            if new_astroid.has_intersection(self.__ship):
                continue
            break
        self.__screen.register_asteroid(new_astroid, SIZE_OF_NEW_ASTRO)
        return new_astroid

    def __get_small_artro(self, astro, torp):
        """
        A function that receives an asteroid and a torpedo that collided with
        an asteroid larger than one, and splits the asteroid into
        two small asteroids.
        :param astro: An asteroid of at least 2
        :param torp: A torpedo that crashed into an asteroid
        """
        # Calculating the speed of the new asteroid-
        new_x_speed = (torp.get_x_speed() + astro.get_x_speed()) / \
                      ((astro.get_x_speed() ** 2 + astro.get_y_speed() **
                        2) ** 0.5)
        new_y_speed = (torp.get_y_speed() + astro.get_y_speed()) / \
                      ((astro.get_x_speed() ** 2 + astro.get_y_speed() **
                        2) ** 0.5)

        new_astro1 = Asteroid(astro.get_x_location(),
                              astro.get_y_location(),
                              new_x_speed,
                              new_y_speed,
                              astro.get_size() - 1)
        new_astro2 = Asteroid(astro.get_x_location(),
                              astro.get_y_location(),
                              - new_x_speed,
                              - new_y_speed,
                              astro.get_size() - 1)

        self.__asteroids_set.add(new_astro1)
        self.__asteroids_set.add(new_astro2)
        self.__screen.register_asteroid(new_astro1, astro.get_size() - 1)
        self.__screen.register_asteroid(new_astro2, astro.get_size() - 1)

    # Functions related to torpedo-

    def __check_for_regular_hit(self):
        """
        A function that checks for an asteroid hit by a regular torpedo.
        If so, delete both, and if necessary split the asteroid.
        """
        # Variables generated by objects that collided-
        hit_astro = None
        hit_torp = None

        for astero in self.__asteroids_set:
            # Search the usual torpedoes -
            for torp in self.__torpedo_dict:
                if astero.has_intersection(torp):
                    self.__score += SCORING[astero.get_size()]
                    self.__screen.set_score(self.__score)
                    hit_astro = astero
                    hit_torp = torp
                    break

        if hit_torp:
            self.__screen.unregister_asteroid(hit_astro)
            self.__asteroids_set.remove(hit_astro)
            self.__screen.unregister_torpedo(hit_torp)
            del self.__torpedo_dict[hit_torp]

            if hit_astro.get_size() > 1:
                self.__get_small_artro(hit_astro, hit_torp)

    def __check_for_special_hit(self):
        """
        A function that checks for an asteroid hit by a special torpedo.
        If so, delete both, and if necessary split the asteroid.
        """
        # Variables generated by objects that collided-
        hit_astro = None
        hit_s_torp = None

        for astero in self.__asteroids_set:
            for s_trop in self.__special_torpedo_dict:
                if astero.has_intersection(s_trop):
                    self.__score += SCORING[astero.get_size()]
                    self.__screen.set_score(self.__score)
                    hit_astro = astero
                    hit_s_torp = s_trop
                    break

        if hit_s_torp:
            self.__screen.unregister_asteroid(hit_astro)
            self.__asteroids_set.remove(hit_astro)
            self.__screen.unregister_torpedo(hit_s_torp)
            del self.__special_torpedo_dict[hit_s_torp]

            if hit_astro.get_size() > 1:
                self.__get_small_artro(hit_astro, hit_s_torp)

    def __get_shot_speed(self):
        """
        A function that calculates the speed of a torpedo,
        according to the given formula
        :return: Torpedo speed, both axes
        """
        new_x_speed = self.__ship.get_x_speed() + 2 * math. \
            cos(math.radians(self.__ship.get_direction()))
        new_y_speed = self.__ship.get_y_speed() + 2 * math. \
            sin(math.radians(self.__ship.get_direction()))
        return new_x_speed, new_y_speed

    def __get_shot(self):
        """
        A function that checks whether the user firing normal shot
        and, if so, creates it.
        """
        if self.__screen.is_space_pressed() and \
                len(self.__torpedo_dict) < REGULAR_TORP_AMOUNT:
            new_x_speed, new_y_speed = self.__get_shot_speed()

            new_torpedo = Torpedo(self.__ship.get_x_location(),
                                  self.__ship.get_y_location(),
                                  new_x_speed,
                                  new_y_speed,
                                  self.__ship.get_direction())

            self.__screen.register_torpedo(new_torpedo)
            # Restarts the torpedo time, and inserts it into the dictionary-
            self.__torpedo_dict[new_torpedo] = NEW_LIFE_TIME

    def __check_for_special_shot(self):
        """
        A function that checks whether the user firing special shot
        and, if so, creates it.
        """
        if self.__screen.is_special_pressed() \
                and len(self.__special_torpedo_dict) < SPECIAL_TORP_AMOUNT:
            x_speed, y_speed = self.__get_shot_speed()

            new_torpedo = SpecialTorpedo(
                self.__ship.get_x_location(),
                self.__ship.get_y_location(),
                x_speed,
                y_speed,
                self.__ship.get_direction())

            # Chooses an asteroid to track it, and updates the speed by that-
            choose_astro = self.__get_clooser_astro(new_torpedo)
            new_torpedo.update_speed(choose_astro)

            self.__screen.register_torpedo(new_torpedo)
            self.__special_torpedo_dict[new_torpedo] = NEW_LIFE_TIME

    def __get_clooser_astro(self, s_torp):
        """
        A function that selects for a special torpedo,
        after which asteroid to follow.
        :param s_torp: A special torpedo
        :return: The asteroid chosen to follow him.
        """
        choose_astro = None
        distance_to_choose = VERY_LARGE_NUM

        for astro in self.__asteroids_set:
            distance = self.__get_distance(astro, s_torp)
            if distance < distance_to_choose:
                distance_to_choose = distance
                choose_astro = astro
        return choose_astro

    # Functions related to the ship-

    def __check_for_intersection(self):
        """
        A function of whether the ship collided with an asteroid.
        So it brings life to the ship and erases the asteroid
        """
        bad_astros = []
        for astero in self.__asteroids_set:
            if astero.has_intersection(self.__ship):
                self.__screen.remove_life()
                self.__ship.remove_life()
                self.__screen.show_message(CRASH_TITLE, CRASH_MSG)
                self.__screen.unregister_asteroid(astero)
                bad_astros.append(astero)

        for astro in bad_astros:
            self.__asteroids_set.remove(astro)

    def __check_for_teleport(self):
        """
        A function that checks whether the user has requested to move the ship
        to a new location.
        If so, she searches for a legal place and transfers it there.
        """
        if self.__screen.is_teleport_pressed():
            while True:
                x_loc, y_loc = self.__get_random_loc()
                self.__ship.set_x_location(x_loc)
                self.__ship.set_y_location(y_loc)
                # Checking that the place does not collide if no asteroid-
                for astro in self.__asteroids_set:
                    if astro.has_intersection(self.__ship):
                        continue
                break

    def __speed_ship(self):
        """
        A function that checks whether the user wants to speed up the ship,
        If so, the speed is updated according to the given formula.
        :return:
        """
        if self.__screen.is_up_pressed():
            new_x_speed = self.__ship.get_x_speed() + \
                          math.cos(math.radians(self.__ship.get_direction()))
            self.__ship.set_x_speed(new_x_speed)

            new_y_speed = self.__ship.get_y_speed() + \
                          math.sin(math.radians(self.__ship.get_direction()))
            self.__ship.set_y_speed(new_y_speed)

    def __rotate_ship(self):
        """
        A function that checks whether the user wants to rotate the ship.
        If so, turn it around.
        """
        if self.__screen.is_left_pressed():
            self.__ship.rotate(DEG_ROTATE_FER_PRESS)
        if self.__screen.is_right_pressed():
            self.__ship.rotate(-DEG_ROTATE_FER_PRESS)

    # Functions related to loops and end of the game

    def __check_for_end(self):
        """
        A function that checks whether the game is over,
        If so, finish the game, and print a message.
        """

        # The ship ended up life-
        if self.__ship.get_life() == 0:
            self.__screen.show_message(END_TITLE, END_OF_LIFE_MSG)
            self.__screen.end_game()
            sys.exit()

        # The asteroids were over-
        if len(self.__asteroids_set) == 0:
            self.__screen.show_message(END_TITLE, END_OF_ASTRO_MSG)
            self.__screen.end_game()
            sys.exit()

        # The user requested to leave-
        if self.__screen.should_end():
            self.__screen.show_message(END_TITLE, QUIT_MSG)
            self.__screen.end_game()
            sys.exit()

    def _game_loop(self):
        """
        A function that ran a loop of the game
        """
        self.__move_all_object()
        self.__draw_all_obj()

        self.__rotate_ship()
        self.__speed_ship()
        self.__get_shot()
        self.__check_for_teleport()
        self.__check_for_special_shot()

        self.__check_for_intersection()
        self.__check_for_regular_hit()
        self.__check_for_special_hit()

        self.__check_for_end()

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
