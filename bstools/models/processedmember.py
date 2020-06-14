from datetime import datetime
from html import escape

import logging

from pybrawl import ClubMember

from bstools import leagueinfo
from bstools.scorecalc import ScoreCalculator

logger = logging.getLogger(__name__)

class ProcessedMember():
    def __init__(self, member):
        self.tag = member.tag
        self.name = escape(member.name)
        self.exp_level = member.exp_level
        self.trophies = member.trophies
        self.role = member.role
        self.last_seen = member.last_seen
        self.club_rank = member.club_rank
        self.previous_club_rank = member.previous_club_rank
        self.score = 'int'
        self.vacation = False
        self.safe = False
        self.blacklist = False
        self.no_promote = False