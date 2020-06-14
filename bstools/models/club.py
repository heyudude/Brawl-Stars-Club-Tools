from datetime import datetime #, timedelta
import logging
import math

from pybrawl import Club

from bstools import leagueinfo

class ProcessedClub():
    def __init__(self, Club, current_war, config):
        self.tag = Club.tag
        self.name = Club.name
        self.badge_id = Club.badge_id
        self.type = Club.type
        self.clan_score = Club.clan_score
        self.required_trophies = Club.required_trophies
        self.members = Club.members
        self.location = Club.location
        self.description = Club.description