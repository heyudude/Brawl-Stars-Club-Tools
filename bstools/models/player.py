from datetime import datetime #, timedelta
import logging
import math

from pybrawl import Player

class ProcessedPlayer():
    def __init__(self, player, config):
        self.tag = player.tag
        self.name = player.name
        self.trophies = player.trophies
        self.name_color = player.name_color
        self.icon = player.icon
        self.highest_trophies = player.highest_trophies
        self.highest_power_play_points = player.highest_power_play_points
        self.exp_level = player.exp_level
        self.exp_level = player.exp_level
        self.is_qualified_from_championship_challenge = player.is_qualified_from_championship_challenge
        self.v3vs3_victories = player.v3vs3_victories
        self.solo_victories = player.solo_victories
        self.duo_victories = player.duo_victories
        self.best_robo_rumble_time = player.best_robo_rumble_time
        self.best_time_as_big_brawler = player.best_time_as_big_brawler
        self.brawlers = player.brawlers

# EOF