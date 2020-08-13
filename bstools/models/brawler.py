from datetime import datetime, timedelta

class GetBrawlers():

    def __init__(self, player):
        # self.in_war = False

        member_tag = player.tag

        for brawler in player.brawlers:
            self.brawler = brawler.id
            self.name = brawler.name
            self.power = brawler.power
            self.rank = brawler.rank
            self.trophies = brawler.trophies
            self.highest_trophies = brawler.highest_trophies
        # TODO  starPowers gadgets
# EOF
