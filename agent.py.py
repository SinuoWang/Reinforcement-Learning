
"""Q-Learning for solving the Treasure Island game.
This module is the intelligence of the main character in the Treasure Island game. Student is required to fill in this file to complete the assignment.
Only the following methods are required to be filled in this assignment:
    init_params():
        Q-learning parameters initialisation.
    init_plot_config():
        Initialise variables for plotting figures.
    get_action():
        Get action depending on exploration or exploitation
    get_reward():
        Get reward for the selected action. It’s entirely up to you to assign the reward value, as long as it’s reasonable.
    decay_epsilon_greedy():
        For decay epsilon greedy implementation.
    train():
        Train the agent using Q-learning.
"""

import numpy as np
from random import choice
import random
from time import time, sleep
from collections import defaultdict
from environment import Level, Environment
import matplotlib.pyplot as plt

# Helper function
def smooth(data, window_len=500, window='hanning'):
    """Smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the beginning and end part of the output signal.

    Args:
        data: The input signal
        window_len: The dimension of the smoothing window; should be an odd integer
        window: The type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'. Note that flat window will produce a moving average smoothing.

    Example:

        t = linspace(-2,2,0.1)
        data = sin(t) + randn(len(t)) * 0.1
        y = smooth(data)

    See also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if data.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")
    if data.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")
    if window_len < 3:
        return data
    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")
    s = np.r_[data[window_len-1:0:-1], data, data[-2:-window_len-1:-1]]

    # Moving average
    if window == 'flat':
        w = np.ones(window_len,'d')
    else:
        w = eval('np.'+ window +'(window_len)')

    y = np.convolve(w/w.sum(), s, mode='valid')
    return y

class Agent:
    """Q-Learning agent.

    In charge of creating intelligence for the robot to solve the game.
    Attributes:
        epsilon, alpha, gamma, decay_rate:
            Q-Learning related parameters.
        max_episode:
            Maximum number of episode to train.
        q_table:
            Q Table for Q-Learning.
        env:
            Game environment class instance.
    """
    class Status:
        """Status of agent after training.

        Attributes:
            QUIT: Quit the game without showing figures.
            DONE_TRAINING: Done training, showing figures and Q table.
        """
        QUIT, DONE_TRAINING = 1, 2

    def __init__(self, level):
        """Initialise Q-Learning params."""
        if level == "easy":
            _level = Level.EASY
        elif level == "hard":
            _level = Level.HARD
        # Default level
        else:
            _level = Level.EASY
        self.env = Environment(_level)
        self.init_params()
        self.init_q_table()
        self.init_plot_config()
        print("Q-Learning agent initialised.")

    def init_params(self):
        """Initialise Q-Learning parameters.

        This method is required to be filled in.
        """
        # FOR STUDENT: Modify the maximum number of episodes for training.
        self.max_episode = 5000

        # FOR STUDENT: Fill in the code section below.
        self.learning_alpha=0.2
        self.epsilon=1
        self.discounting_gamma=0.9
        self.decay_rate=0.002



    def init_q_table(self):
        """Initialise Q Table.

        Note:
            For the purpose of displaying Q table on the game, it is required the Q table to be a nested dictionary with the format: {state: {action: q_value}}.
        """
        # Init states with the format (x, y).
        # Example: (0, 1), (0, 1)
        # Note: States must be a list of tuple.
        states = []
        grid_size = self.env.get_grid_size()
        for x in range(grid_size):
            for y in range(grid_size):
                states.append((x, y))

        # Init Q Table with the format: {state: {action: q_value}}
        # Example: {(0, 0): {"left": 0.123, ..., "up": 0.456}}
        self.q_table = defaultdict(dict)
        actions = self.env.get_actions()
        for state in states:
            for action in actions.keys():
                self.q_table[state][action] = 0

    def init_plot_config(self):
        """Initialise variables for plotting figures.

        This method is required to be filled in.
        """
        # FOR STUDENT: Fill in the code section below.
        self.accumulate_reward=[]
        self.episode_reward=0

    def plot(self):
        """Plot Q-Learning figures as required in the Task 4.

        This method is required to be filled in.
        """
        # FOR STUDENT: Fill in the code section below.
        x=np.array(self.accumulate_reward)
        y=smooth(x,window_len=1001)
        plt.plot(y)
        plt.show()



    def get_action(self, position):
        """Get action depending on exploration or exploitation.

        This method is required to be filled in.

        Args:
            position: A tuple of position to get action.

        Returns:
            A string of action. Either be "left", "right", "up" or "down".
        """
        # FOR STUDENT: Fill in the code section below.

        x = random.uniform(0,1)


        if x >= self.epsilon:


            # Init Q Table with the format: {state: {action: q_value}}
            # Example: {(0, 0): {"left": 0.123, ..., "up": 0.456}}

            state=position

            #max_action=max(available_table[position],key=available_table[position].get)
            max_q= max(self.q_table[position].values())
            if max_q < 0.0000001:
                max_q=0

            pick=[]
            if self.q_table[position]["up"]>=max_q and "up" in self.env.get_possible_actions(position):
                pick.append("up")

            if self.q_table[position]["down"]>=max_q and "down" in self.env.get_possible_actions(position):
                pick.append("down")

            if self.q_table[position]["left"]>=max_q and "left" in self.env.get_possible_actions(position):
                pick.append("left")

            if self.q_table[position]["right"]>=max_q and "right" in self.env.get_possible_actions(position):
                pick.append("right")

            new_action=random.choice(pick)

            pick.clear()

            #print(new_action)


        else:
             new_action=random.choice(self.env.get_possible_actions(position))


        return new_action





    def get_reward(self, position):
        """Get reward for the selected action.

        This method is required to be filled in.

        Args:
            position: A tuple of position to get action.

        Returns:
            A value of reward at the specified position.
        """
        # FOR STUDENT: Fill in the code section below.
        if position == self.env.get_treasure_position():
           reward = 100

        elif position in self.env.get_bomb_map():
            reward = -100

        elif position in self.env.get_diamond_map():
            reward = 50

        else:
            reward=0

        return reward




    def get_q_table(self):
        """Get Q table."""
        return self.q_table

    def decay_epsilon_greedy(self):
        """Decay epsilon greedy implementation.

        This method is required to be filled in.
        """
        # FOR STUDENT: Fill in the code section below.
        next_decay_epsilon_greedy=(1-self.decay_rate)*self.epsilon
        self.epsilon=next_decay_epsilon_greedy

        return self.epsilon




    def restart(self, position):
        """Condition to restart the game."""
        return position == self.env.get_treasure_position() or position in self.env.get_bomb_map()

    def pause(self):
        """Pause the game.

        Use primarily for toggling displaying Q values.
        """
        self.env.display(self.max_episode, self.max_episode, self.q_table)
        return self.env.update()

    def train(self):
        """Train the agent using Q-Learning.

        This method is required to be filled in.

        Returns:
            DONE_TRAINING: When ran through the input maximum episode.
            QUIT: When hit close button on the game screen.
        """
        print("Training...")
        status = self.Status.DONE_TRAINING
        start = time()
        for episode in range(self.max_episode):
            # Reset the environment before starting a new episode.
            self.env.reset()
            episode_done = False
            while not episode_done:
                sleep(self.env.get_speed())
                self.env.display(episode, self.max_episode, self.q_table)

                # FOR STUDENT: Start fill in this code section.
                # The lines of code below act as a placeholder to generate random moves for the robot. The student must delete all these lines before implementation.



                state=self.env.get_current_position()
                action=self.get_action(state)
                self.env.move(action)
                next_state=self.env.get_current_position()
                reward=self.get_reward(next_state)

                if self.restart(state):
                    self.q_table[state][action] = (1-self.learning_alpha)*self.q_table[state][action]+self.learning_alpha*reward
                    self.decay_epsilon_greedy()

                    self.accumulate_reward.append(self.episode_reward)
                    self.episode_reward=0
                    episode_done=True


                else:
                     self.q_table[state][action] = (1-self.learning_alpha)*self.q_table[state][action]+self.learning_alpha*(reward+self.discounting_gamma*max(list(self.q_table[next_state].values())))
                     self.episode_reward=self.episode_reward+reward




                # End of code section

                if not self.env.update():
                    status = self.Status.QUIT
                    break
            if status == self.Status.QUIT:
                self.plot()
                break


        # if not hitting close button, then the status will remain as initialised.
        if status == self.Status.DONE_TRAINING:
            end = time()
            print(f"Done training. Elapsed time: {(end - start)/60} mins")

            # Keep updating screen for the student to capture screen with Q values.
            while self.pause():
                pass
        elif status == self.Status.QUIT:

            print("Quit game.")




        return status
