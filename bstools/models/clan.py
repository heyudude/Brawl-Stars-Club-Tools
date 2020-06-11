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
        self.donations_per_week = Club.donations_per_week
        self.clan_war_trophies = Club.clan_war_trophies
        self.clan_chest_level = Club.clan_chest_level
        self.clan_chest_max_level = Club.clan_chest_max_level
        self.members = Club.members
        self.location = Club.location
        self.description = Club.description
        self.clan_chest_status = Club.clan_chest_status
        self.clan_chest_points = Club.clan_chest_points

        self.war_league = leagueinfo.get_war_league_from_score(self.clan_war_trophies)
        self.war_league_name = config['strings']['war-league-' + self.war_league]
        self.current_war_state = current_war.state

