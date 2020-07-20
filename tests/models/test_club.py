import pybrawl
from bstools import load_config_file
from bstools.models import ProcessedClub

CLUB_TAG = '#FakeClubTag'

__config_file_score__ = '''
[activity]
threshold_kick=99999999
threshold_warn=99999999
[Score]
'''

__fake_club__ = pybrawl.Club(
    tag                = CLUB_TAG,
    name               = "18plussers",
    description        = "Rules, stats, discord link, and info at https://18plussers.com",
    club_score         = 38803,
    required_trophies  = 3000,
    members            = 4,
    member_list        = [
        pybrawl.ClubMember(
            tag       = "#AAAAAA",
            name      = "PresidentPerson",
            role      = "president",
            #explevel  = 12, #to do: how is this stored in CR or BS? It is part of the Player info
            trophies  = 4153,
            last_seen = "20190802T154619.000Z"
        )
    ]
)

def test_process_club(tmpdir):
    config_file = tmpdir.mkdir('test_process_club').join('testfile')
    config_file.write(__config_file_score__)
    config = load_config_file(config_file.realpath())

    Club = ProcessedClub(
        config=config,
        Club=__fake_club__
    )

