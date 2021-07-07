"""Treasure Island environment

This module is for creating Treasure Island game environment. Please note that for this assignment, no modification is required in this file.
"""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg

class Level:
    """Game level

    This game includes two levels: EASY and HARD. Based on the level specified, a corresponding map will be generated in the grid world.

    Attributes:
        EASY: A constant which indicates the level EASY.
        HARD: A constant which indicates the level HARD.
        grid_size: Number of grid in the grid world.
        bomb_map: Map contains all bomb positions.
        diamond_map: Map contains all diamond positions.
    """
    EASY, HARD = 0, 1
    def __init__(self, level):
        """Initialise map corresponding with the specified level."""
        if level == self.EASY:
            self.grid_size = 4
            self.bomb_map = [(0, 1), (0, 2), (2, 0), (2, 3)]
            self.diamond_map = [(1, 2)]
        elif level == self.HARD:
            self.grid_size = 6
            self.bomb_map = [(0, 1), (0, 3), (5, 3), (2, 0), (2, 2), (3, 4), (1, 5), (5, 1), (4, 1)]
            self.diamond_map = [(4, 4), (3, 3), (2, 1)]

    def get_grid_size(self):
        """Get number of grids.

        Returns:
            Number of grids
        """
        return self.grid_size

    def get_map(self):
        """Get map of the grid game corresponding with the specified level.
        
        Returns:
            A copy of diamond map, A copy of bomb map
        """
        return self.diamond_map.copy(), self.bomb_map.copy()

class Environment:
    """Game environment.
    
    In charge of initilisation, displaying and updating the game screen. 

    Attributes:
        grid_size: 
            Number of grids.
        window_width:
            Game window width in px
        window_height: 
            Game window height in px
        status_font: 
            Font to display game status.
        q_value_font:
            Font to display Q values.
        screen: 
            Used primarily for initialising game screen.
        speed:
            Speed between move. Default: 0.5 second.
        debug_mode:
            If the debug mode is true, all Q values will be displayed on the game screen. Otherwise, normal game screen will be displayed. The debug_mode can be toggled by pressing SPACE on your keyboard.
        scores:
            Game scores.
        game_status:
            Either be "Game over!" or "You won!".
        robot_status:
            Either be "Collected diamond", "Exploded", or "Treasure found".
        current_position:
            The robot's current position. It's a list.
    """
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255,0,0)
    FONT_GAME_STATUS, FONT_GAME_STATUS_SIZE = 'Arial Bold', 25
    GAME_CAPTION = 'ELEC ENG 4107 Treasure Island'
    ACTIONS = {"up": 0, "down": 1, "left": 2, "right": 3}
    FONT_Q_VALUE, FONT_Q_VALUE_SIZE = 'font/cour.ttf', 11
    def __init__(self, level):
        """Init Environment class."""
        self.level = Level(level)
        self.grid_size = self.level.get_grid_size()
        self.window_width = self.grid_size * 100
        self.window_height = self.grid_size * 100 + 100
        self.treasure_position = (self.grid_size - 1, self.grid_size - 1)
        pg.init()
        self.status_font = pg.font.SysFont(self.FONT_GAME_STATUS, self.FONT_GAME_STATUS_SIZE)
        self.q_value_font = pg.font.SysFont(self.FONT_Q_VALUE, self.FONT_Q_VALUE_SIZE)
        self.q_value_font = pg.font.Font(self.FONT_Q_VALUE, self.FONT_Q_VALUE_SIZE)
        self.screen = pg.display.set_mode((self.window_width, self.window_height))
        pg.display.set_caption(self.GAME_CAPTION)

        self.robot = pg.image.load(r'images/robot.png')
        self.robot = pg.transform.scale(self.robot, (80, 80))
        self.bomb = pg.image.load(r'images/bomb.png')
        self.bomb = pg.transform.scale(self.bomb, (80, 80))
        self.treasure = pg.image.load(r'images/treasure.png')
        self.treasure = pg.transform.scale(self.treasure, (80, 80))
        self.diamond = pg.image.load(r'images/diamond.png')
        self.diamond = pg.transform.scale(self.diamond, (80, 80))
        self.simple_bomb = pg.image.load(r'images/simple_bomb.png')
        self.simple_bomb = pg.transform.scale(self.simple_bomb, (50, 50))
        self.simple_diamond = pg.image.load(r'images/simple_diamond.png')
        self.simple_diamond = pg.transform.scale(self.simple_diamond, (50, 50))
        self.simple_treasure = pg.image.load(r'images/simple_treasure.png')
        self.simple_treasure = pg.transform.scale(self.simple_treasure, (50, 50))
        self.simple_robot = pg.image.load(r'images/simple_robot.png')
        self.simple_robot = pg.transform.scale(self.simple_robot, (50, 50))
        self.speed = 0.5
        self.debug_mode = False
        self.reset()
        print("Environment initialised.")

    def reset(self):
        """Reset the environment."""
        self.scores = 0
        self.game_status = ""
        self.robot_status = ""
        self.diamond_map, self.bomb_map = self.level.get_map()
        self.current_position = [0, 0]
    
    def get_speed(self):
        """Get speed between moves.

        Returns:
            Speed value between moves. Note that this value of delay is not a constant. it can be adjusted by pressing the KEYUP/KEYDOWN button.
        """
        return self.speed

    def get_grid_size(self):
        """Get the number of grids."""
        return self.grid_size

    def get_current_position(self):
        """Get robot current position.
        
        Return:
            A tuple of current position.
        """
        return tuple(self.current_position)

    def get_treasure_position(self):
        """Get treasure position.

        Return:
            A tuple of the treasure position.
        """
        return self.treasure_position

    def get_diamond_map(self):
        """Get diamond map.

        Return:
            List of tuples of all diamond positions.
        """
        return self.diamond_map

    def get_bomb_map(self):
        """Get bomb map.

        Return:
            List of tuples of all bomb positions.
        """
        return self.bomb_map

    def get_actions(self):
        """Get predefined actions.

        Return:
            A dictionary in the format {action_string: action_number}. Example: {"left": 1}.
        """
        return self.ACTIONS

    def get_possible_actions(self, position):
        """Get all possible actions at a position.

        For example: If the robot is at (0, 0), it can not move left or up. Therefore, the possible actions in this case are right and down.

        Args:
            position: Tuple of position.
        
        Return:
            List of all possible actions.
        """
        possible_actions = []
        if position[0] != 0:
            possible_actions.append("up")
        if position[0] != self.grid_size - 1:
            possible_actions.append("down")
        if position[1] != 0:
            possible_actions.append("left")
        if position[1] != self.grid_size - 1:
            possible_actions.append("right")
        return possible_actions

    def to_px(self, position):
        """Convert grid position to pixel.

        Args:
            position: 
                Grid position in tuple/list. Example: (2, 3) or [2, 3].

        Returns:
            A tuple (x, y) coordinates in pixels.
        """
        position = list(position)
        if self.debug_mode:
            px = (position[1] * 100 + 25, position[0] * 100 + 75)
        else:
            px = (position[1] * 100 + 10, position[0] * 100 + 60)
        return px

    def display_layout(self):
        """Display grid layout."""
        # Create grids
        for x in range(0, self.window_width, 100):
            for y in range(50, self.window_height - 50, 100):
                rect = pg.Rect(x, y, x + 100, 100)
                pg.draw.rect(self.screen, self.BLACK, rect, 2)

    def display_debug_mode(self, q_table):
        """Display game in debug mode.

        Args:
            q_table: The Q table to be displayed. Note that the Q table must be a dictionary with the format of {state: {action: value}}. Example: {(0, 0): {"left": 0.123, ..., "down": 0.456}}.
        """
        for bomb_position in self.bomb_map:
            self.screen.blit(self.simple_bomb, self.to_px(bomb_position))
        self.screen.blit(self.simple_treasure, self.to_px(self.treasure_position))
        self.screen.blit(self.simple_robot, self.to_px(self.current_position))
        for diamond_position in self.diamond_map:
            self.screen.blit(self.simple_diamond, self.to_px(diamond_position))
        for position, action_values in q_table.items():
            for action, value in action_values.items():
                q_value = self.q_value_font.render('{:.3f}'.format(value), True, (0, 0, 0))
                if action == "up":
                    self.screen.blit(q_value, (position[1] * 100 + 35, position[0] * 100 + 55))
                elif action == "down":
                    self.screen.blit(q_value, (position[1] * 100 + 35, position[0] * 100 + 135))
                elif action == "left":
                    self.screen.blit(q_value, (position[1] * 100 + 5, position[0] * 100 + 95))
                elif action == "right":
                    self.screen.blit(q_value, (position[1] * 100 + 55, position[0] * 100 + 95))

    def display_game_mode(self):
        """Display game in normal mode."""
        for bomb_position in self.bomb_map:
            self.screen.blit(self.bomb, self.to_px(bomb_position))
        self.screen.blit(self.treasure, self.to_px(self.treasure_position))
        self.screen.blit(self.robot, self.to_px(self.current_position))
        for diamond_position in self.diamond_map:
            self.screen.blit(self.diamond, self.to_px(diamond_position))

    def display_info(self, num_episode, max_episode, q_table):
        """Display game information. 

        Contain: Current episode, Max episode, and Q table in the debug mode.

        Args:
            num_episode: 
                Current episode number to display on the game screen.
            max_episode:
                Maximum number of episode to display on the game screen.
            q_table: 
                Q table to display on the game screen in the debug mode.
        """
        episode = self.status_font.render(f'Episode {num_episode}/{max_episode}', True, (0, 0, 0))
        self.screen.blit(episode, (8, self.window_height - 32))
        speed = self.status_font.render('Speed {:.2f}s'.format(self.speed), True, (0, 0, 0))
        self.screen.blit(speed, (self.window_width - 105, self.window_height - 32))

        scores = self.status_font.render(f'Scores: {self.scores}', True, (0, 0, 0))
        self.screen.blit(scores, (8, 17))
        game_status = self.status_font.render(f'{self.game_status}', True, (0, 0, 0))
        self.screen.blit(game_status, (self.window_width - 100, 17))
        robot_status = self.status_font.render(self.robot_status, True, (0, 0, 0))
        self.screen.blit(robot_status, (self.window_width/2 - 80, 17))

    def display(self, num_episode, max_episode, q_table):
        """Display the game.

        Args:
            num_episode: 
                Current episode number to display on the game screen.
            max_episode:
                Maximum number of episode to display on the game screen.
            q_table: 
                Q table to display on the game screen in the debug mode.
         """
        self.screen.fill(self.WHITE)
        self.display_layout()

        if self.debug_mode:
            self.display_debug_mode(q_table)
        else:
            self.display_game_mode()
        self.display_info(num_episode, max_episode, q_table)

    def move(self, action):
        """Move the robot with the specified action.

        Args:
            action:
                A string of action to move the robot. Be either "left", "right", "up", or "down".
        """
        # Display the robot at the grid position
        if action in self.get_possible_actions(self.current_position):
            if action == "up":
                self.current_position[0] -= 1
            elif action == "down":
                self.current_position[0] += 1
            elif action == "left":
                self.current_position[1] -= 1
            elif action == "right":
                self.current_position[1] += 1

    def update(self):
        """Update the game screen."""
        if tuple(self.current_position) in self.diamond_map:
            self.diamond_map.remove(tuple(self.current_position))
            self.robot_status = "Collected diamond"
            self.scores += 1
        elif tuple(self.current_position) in self.bomb_map:
            self.robot_status = "Robot exploded"
            self.game_status = "Game over!"
        elif tuple(self.current_position) == self.treasure_position:
            self.robot_status = "Treasure found"
            self.game_status = "You won!"
            self.scores += 10

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return False
            if event.type == pg.KEYDOWN:
                # Reduce delay between moves
                if event.key == pg.K_x:
                    if self.speed >= 0.05:
                        self.speed -= 0.05

                # Increase delay between moves
                if event.key == pg.K_w:
                    self.speed += 0.05

                # Toggle displaying Q values
                if event.key == pg.K_SPACE:
                    self.debug_mode ^= True

        pg.display.update()
        return True