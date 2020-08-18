from datetime import datetime #, timedelta
import logging
import math

from pybrawl import Club

class ProcessedClub():
    def __init__(self, club, config):
        self.tag = club.tag
        self.name = club.name
        self.description = club.description
        self.type = club.type
        self.trophies = club.trophies
        self.required_trophies = club.required_trophies
