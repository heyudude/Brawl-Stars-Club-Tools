import pybrawl
from bstools import load_config_file
from bstools.models import ProcessedCurrentWar

CLAN_TAG = '#FakeClubTag'

__fake_war_clan__ = pybrawl.WarClub(
        tag = CLAN_TAG,
        name = "Agrassar",
        clan_score = 1813,
        participants = 17,
        battles_played = 13,
        battles_remaining = 0,
        wins = 1,
        crowns = 5
    )

__fake_war_participants__ = [
    pybrawl.WarParticipant(
        tag                           =  '#AAAAAA',
        cards_earned                  = 1120,
        battles_played                = 1,
        wins                          = 1,
        number_of_battles             = 1,
        collection_day_battles_played = 3
    ),
    pybrawl.WarParticipant(
        tag                           =  '#BBBBBB',
        cards_earned                  = 1120,
        battles_played                = 1,
        wins                          = 1,
        number_of_battles             = 1,
        collection_day_battles_played = 1
    ),
    pybrawl.WarParticipant(
        tag                           =  '#CCCCCC',
        cards_earned                  = 1120,
        battles_played                = 0,
        wins                          = 1,
        number_of_battles             = 1,
        collection_day_battles_played = 1
    )
]

def test_process_current_war_nowar():
    config = load_config_file(False)

    war = ProcessedCurrentWar(config=config, current_war=pybrawl.WarCurrent(state='notInWar'))

    assert war.state_label == 'The Club is not currently engaged in a war.'

def test_process_current_war_collection():
    config = load_config_file(False)

    war = ProcessedCurrentWar(config=config, current_war=pybrawl.WarCurrent(
        state               = 'collectionDay',
        collection_end_time = '20190209T212846.354Z',
        Club                = __fake_war_clan__,
        participants        = __fake_war_participants__
    ))

    assert war.collection_end_time
    assert war.end_label

def test_process_current_war_warday():
    config = load_config_file(False)

    war = ProcessedCurrentWar(config=config, current_war=pybrawl.WarCurrent(
        state        = 'warDay',
        war_end_time = '20190209T212846.354Z',
        Club         = __fake_war_clan__,
        participants = __fake_war_participants__,
        clans        = [__fake_war_clan__]
    ))

    assert war.state_label == 'War Day'
    assert war.collection_end_time_label == 'Complete'
    assert war.end_label

"""
def test_member_war(tmpdir):
    config_file = tmpdir.mkdir('test_member_war').join('testfile')
    config_file.write(__config_file_score__)
    config = load_config_file(config_file.realpath())

    war_current_nowar = bstools.member_war(
        config,
        __fake_clan__.member_list[0],
        pybrawl.WarCurrent(state='notInWar')
    )
    assert war_current_nowar['status'] == 'na'
    assert war_current_nowar['score'] == 0

    war_current_isparticipating = bstools.member_war(
        config,
        __fake_clan__.member_list[0].to_dict(),
        __fake_currentwar_warday__
    )
    assert war_current_isparticipating['status'] == 'good'
    assert war_current_isparticipating['score'] == 0

    war_current_notparticipating = bstools.member_war(
        config,
        __fake_clan__.member_list[3].to_dict(),
        __fake_currentwar_warday__
    )
    assert war_current_notparticipating['status'] == 'ok incomplete'
    assert war_current_notparticipating['score'] == 0

    war_isparticipating_good = bstools.member_war(
        config,
        __fake_clan__.member_list[0].to_dict(),
        __fake_war__
    )
    assert war_isparticipating_good['status'] == 'good'
    assert war_isparticipating_good['score'] == 34

    war_isparticipating_ok = bstools.member_war(
        config,
        __fake_clan__.member_list[1].to_dict(),
        __fake_war__
    )
    print(__fake_clan__.member_list[1].arena)
    assert war_isparticipating_ok['status'] == 'ok'
    assert war_isparticipating_ok['score'] == 24

    war_isparticipating_bad = bstools.member_war(
        config,
        __fake_clan__.member_list[2].to_dict(),
        __fake_war__
    )
    assert war_isparticipating_bad['status'] == 'ok'
    assert war_isparticipating_bad['score'] == 24

    war_notparticipating = bstools.member_war(
        config,
        __fake_clan__.member_list[3].to_dict(),
        __fake_war__
    )
    assert war_notparticipating['status'] == 'bad'
    assert war_notparticipating['score'] == -18

def test_member_warlog(tmpdir):
    config_file = tmpdir.mkdir('test_member_warlog').join('testfile')
    config_file.write(__config_file_score__)
    config = load_config_file(config_file.realpath())

    warlog = bstools.member_warlog(config, __fake_clan__.member_list[0], __fake_warlog__)
    assert warlog[0]['status'] == 'good'

    warlog = bstools.member_warlog(config, __fake_clan__.member_list[1], __fake_warlog__)
    assert warlog[0]['status'] == 'ok'
"""
