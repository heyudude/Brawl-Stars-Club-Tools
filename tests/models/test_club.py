import pytest
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
    required_trophies  = 3000,
    member_list        = [
        pybrawl.ClubMember(
            tag       = "#AAAAAA",
            name      = "PresidentPerson",
            role      = "president",
            #explevel  = 12, # TODO: how is this stored in CR or BS? It is part of the Player info
            trophies  = 4153
        )
    ]
)

def test_process_club(tmpdir):
    config_file = tmpdir.mkdir('test_process_club').join('testfile')
    config_file.write(__config_file_score__)
    config = load_config_file(config_file.realpath())

    club = ProcessedClub(
        config=config,
        club=__fake_club__
    )


if __name__ == '__main__':
    pytest.main()
