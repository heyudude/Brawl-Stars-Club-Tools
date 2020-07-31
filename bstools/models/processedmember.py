from datetime import datetime
from html import escape

import logging

from pybrawl import ClubMember

from bstools.scorecalc import ScoreCalculator

logger = logging.getLogger(__name__)

class ProcessedMember():
    def __init__(self, member):
        self.tag = member.tag
        self.name = escape(member.name)
        #self.exp_level = member.exp_level # TODO how to get this info not in API from BS
        #self.exp_points = member.exp_points
        self.trophies = member.trophies
        self.role = member.role
        self.score = 'int'
        self.vacation = False
        self.safe = False
        self.blacklist = False
        self.no_promote = False
        self.last_seen = 0 # TODO last seen not in member / player def as member.last_seen
        self.time_in_club = 0