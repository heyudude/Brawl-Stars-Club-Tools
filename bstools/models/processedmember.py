from datetime import datetime
from html import escape

import logging

from pybrawl import ClubMember
from pybrawl import Player

from bstools.scorecalc import ScoreCalculator

logger = logging.getLogger(__name__)

class ProcessedMember():
    def __init__(self, member, rank):
        self.rank = rank
        self.tag = member.tag
        self.name = escape(member.name)
        #self.exp_level = player.exp_level # TODO
        #self.exp_points = player.exp_points
        self.exp_level = 1
        self.exp_points = 1
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