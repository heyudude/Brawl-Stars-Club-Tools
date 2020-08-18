from datetime import datetime
from html import escape

import logging

from pybrawl import ClubMember

logger = logging.getLogger(__name__)

class ProcessedMember():
    def __init__(self, member, rank):
        self.rank = rank
        self.tag = member.tag
        self.name = escape(member.name)
        # self.exp_level = member.exp_level # TODO Exp level from player
        self.exp_points = 1 # TODO player.exp_points
        self.trophies = member.trophies
        self.role = member.role
        self.score = 'int'
        self.vacation = False
        self.safe = False
        self.blacklist = False
        self.no_promote = False
        self.last_seen = 0          # TODO last seen not in member / player def as member.last_seen
        self.time_in_club = 0
        self.previous_rank = self.rank

# EOF