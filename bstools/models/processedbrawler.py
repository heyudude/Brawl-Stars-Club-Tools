from datetime import datetime, timedelta

class ProcessedBrawler():

    def __init__(self, brawler):

        #member_tag = player.tag

        #for brawler in player.brawlers:
            #self.player_tag = player.tag
        self.brawler = brawler.id
        self.name = brawler.name.title()
        self.power = brawler.power
        self.rank = brawler.rank
        self.trophies = brawler.trophies
        self.highest_trophies = brawler.highest_trophies
        # TODO  starPowers gadgets
        self.gadgets = brawler.gadgets
        self.star_powers = brawler.star_powers
# EOF
