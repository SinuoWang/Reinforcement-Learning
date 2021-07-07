#!/usr/bin/env python3
"""Main file to run the Treasure Island Game Solver.

Treasure Island is a grid game designed for ELEC ENG 4107 Autonomous System to learn Q-Learning. Mission: Navigate the robot to the treasure without entering any bomb spots. On the journey, try to collect as many diamonds as possible.

"""
from agent import Agent
import argparse

def run(level):
    agent = Agent(level)
    agent.train()
    agent.plot()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ELEC ENG 4107 Treasure Island Solver.')
    parser.add_argument('-lv', "--level", choices=['easy', 'hard'], help='Game level (easy or hard).', required=True)
    args = parser.parse_args()
    run(args.level)