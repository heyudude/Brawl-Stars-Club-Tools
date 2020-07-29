from datetime import datetime

import bstools
from bstools import bstools, load_config_file, history
from bstools import MemberFactory
from bstools.models import ProcessedCurrentWar, ProcessedMember, WarParticipation
from bstools.scorecalc import ScoreCalculator
import pybrawl

__config_file_score__ = '''
[activity]
threshold_kick=99999999
threshold_warn=99999999
[Score]
collect_battle_played=0
collect_battle_incomplete=-5
collect_battle_won=2
collect_battle_lost=0
war_participation=0
war_non_participation=-1
'''

CLUB_TAG = '#FakeClubTag'

__fake_member_list__ = [
    pybrawl.ClubMember(
        tag       = "#AAAAAA",
        name      = "PresidentPerson",
        role      = "president",
        exp_level = 12,
        exp_points = 100,
        trophies  = 4153
    ),
    pybrawl.ClubMember(
        tag       = "#BBBBBB",
        name      = "CoLeaderPerson",
        role      = "VicePresident",
        exp_level = 12,
        exp_points = 100,
        trophies  = 4418
    ),
    pybrawl.ClubMember(
        tag       = "#CCCCCC",
        name      = "ElderPerson",
        role      = "Vice-President",
        exp_level = 12,
        exp_points = 100,        
        trophies  = 4224
    ),
    pybrawl.ClubMember(
        tag       = "#DDDDDD",
        name      = "MemberPerson",
        role      = "member",
        exp_level = 8,
        exp_points = 100,
        trophies  = 3100
    ),
    pybrawl.ClubMember(
        tag       = "#EEEEEE",
        name      = "MemberPersonToBePromoted",
        role      = "member",
        exp_level = 8,
        exp_points = 100,
        trophies  = 3144
]

__fake_club__ = pybrawl.Club(
    tag                = CLUB_TAG,
    name               = "18Plussers",
    description        = "Rules, stats, discord link, and info at https://18plussers",
    required_trophies  = 3000,
    donations_per_week = 7540,
    members            = 4,
    members        = __fake_member_list__
)

__fake_war_club__ = pybrawl.WarClub(
        tag = CLUB_TAG,
        name = "18plussers",
        club_score = 1813,
        participants = 17,
        battles_played = 13,
        battles_remaining = 0,
        wins = 1,
        crowns = 5
    )

def test_war_score(tmpdir):

    config_file = tmpdir.mkdir('test_war_score').join('testfile')
    config_file.write(__config_file_score__)
    config = load_config_file(config_file.realpath())

    calc = ScoreCalculator(config)

    war_complete = ProcessedCurrentWar(config=config, current_war=__fake_current_war__)
    war_complete.status = 'na'
    war_complete.battles_played = 1
    war_complete.wins = 1
    war_complete.collection_day_battles_played = 3
    war_complete.collection_battle_wins = 2
    war_complete.collection_battle_losses = 0
    assert calc.get_war_score(war_complete)   == 24

    war_incomplete = ProcessedCurrentWar(config=config, current_war=__fake_current_war__)
    war_incomplete.status = 'na'
    war_incomplete.battles_played = 0
    war_incomplete.wins = 0
    war_incomplete.collection_day_battles_played = 3
    war_incomplete.collection_battle_wins = 2
    war_incomplete.collection_battle_losses = 0
    assert calc.get_war_score(war_incomplete) == -26

    war_na = WarParticipation(config=config, member=ProcessedMember(__fake_member_list__[4]), war=__fake_war__)
    assert calc.get_war_score(war_na)         == -1

    war_new = WarParticipation(config=config, member=ProcessedMember(__fake_member_list__[4]), war=__fake_war__)
    war_new.status = 'not-in-Club'
    assert calc.get_war_score(war_new)        == 0

def test_donations_score(tmpdir):
    config_file = tmpdir.mkdir('test_donations_score').join('testfile')
    config_file.write(__config_file_score__)
    config = load_config_file(config_file.realpath())

    calc = ScoreCalculator(config)

    war = ProcessedCurrentWar(config=config, current_war=pybrawl.WarCurrent(state='notInWar'))
    member_history = history.get_member_history(__fake_member_list__, config['bstools']['timestamp'], '{}', war)
    date = datetime(2019, 2, 12, 7, 32, 1, 0)

    member_6 = MemberFactory(config=config, current_war=war, Club=__fake_club__, member_history=member_history, warlog=pybrawl.WarLog(items=[]), days_from_donation_reset=6).get_processed_member(__fake_member_list__[0])
    member_3 = MemberFactory(config=config, current_war=war, Club=__fake_club__, member_history=member_history, warlog=pybrawl.WarLog(items=[]), days_from_donation_reset=3).get_processed_member(__fake_member_list__[0])
    member_0 = MemberFactory(config=config, current_war=war, Club=__fake_club__, member_history=member_history, warlog=pybrawl.WarLog(items=[]), days_from_donation_reset=0).get_processed_member(__fake_member_list__[0])

    assert calc.get_member_donations_score(member_6) == 11
    assert calc.get_member_donations_score(member_3) == 18
    assert calc.get_member_donations_score(member_0) == 31

