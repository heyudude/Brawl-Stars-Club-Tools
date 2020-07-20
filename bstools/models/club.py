from datetime import datetime #, timedelta
import logging
import math

from pybrawl import Club

class ProcessedClub():
    def __init__(self, Club, current_war, config):
        self.tag = Club.tag
        self.name = Club.name
        self.description = Club.description
        self.trophies = Club.trophies
        self.required_trophies = Club.required_trophies
        self.members = Club.members
