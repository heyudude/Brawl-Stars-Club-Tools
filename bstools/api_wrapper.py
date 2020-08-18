import logging
import pybrawl
import json

logger = logging.getLogger(__name__)

class ApiWrapper:
    def __init__(self, config):
        self.config = config

        logger.debug("Creating API instance")
        api_config = pybrawl.Configuration()
        api_config.api_key['authorization'] = config['api']['api_key']
        api_config.access_token = config['api']['api_key'] # TODO document why this addition is needed! 
        #print(api_config.api_key)
        if config['api']['proxy']:
            api_config.proxy = config['api']['proxy']
        if config['api']['proxy_headers']:
            api_config.proxy_headers = config['api']['proxy_headers']

        self.clubs = pybrawl.ClubsApi(pybrawl.ApiClient(api_config))
        self.players = pybrawl.PlayersApi(pybrawl.ApiClient(api_config))

    def get_club_from_api(self): # pragma: no coverage
        try:
            # Get Club data from API 
            club = self.clubs.get_club(self.config['api']['club_id'])
            logger.info('- Found Club: {} ({})'.format(club.tag, club.name))

            return (club)
        except pybrawl.ApiException as e:
            if e.body:
                body = json.loads(e.body)
                if body['reason'] == 'accessDenied':
                    logger.error('403: developer.brawlstars.com claims that your API key is invalid. Please make sure you are setting up bstools with a valid key.')
                elif body['reason'] == 'accessDenied.invalidIp':
                    logger.error('developer.brawlstars.com says: {}'.format(body['message']))
                else:
                    logger.error('error: {}'.format(body))
            else:
                logger.error('error: {}'.format(e))
        except pybrawl.OpenApiException as e:
            logger.error('Apiwrapper error: {}'.format(e))

        # If we've gotten here, something has gone wrong. We need to abort the application.
        exit(0)

    def get_player_from_api(self, player_tag): # pragma: no coverage
        try:
            # Get player data from API 
            player = self.players.get_player(player_tag)
            logger.info('- Found Player: {} ({})'.format(player.tag, player.name))

            return (player)
        except pybrawl.ApiException as e:
            if e.body:
                body = json.loads(e.body)
                if body['reason'] == 'accessDenied':
                    logger.error('403: developer.brawlstars.com claims that your API key is invalid. Please make sure you are setting up bstools with a valid key.')
                elif body['reason'] == 'accessDenied.invalidIp':
                    logger.error('developer.brawlstars.com says: {}'.format(body['message']))
                else:
                    logger.error('error: {}'.format(body))
            else:
                logger.error('error: {}'.format(e))
        except pybrawl.OpenApiException as e:
            logger.error('Apiwrapper error: {}'.format(e))

        # If we've gotten here, something has gone wrong. We need to abort the application.
        exit(0)

    def get_brawlers_for_player(self, member_tag):

        logger.debug("Getting brawlers for player {}".format(member_tag))
        try:
            # Get player data and brawlers from API.
            player = self.players.get_player(member_tag)

            logger.debug("Player: {}".format(player.name))
            for brawler in player.brawlers:
                logger.debug("Brawler: {}".format(brawler.name))
            return 

        except pybrawl.ApiException as e:
            if e.body:
                body = json.loads(e.body)
                if body['reason'] == 'accessDenied':
                    logger.error(
                        'developer.brawlstars.com claims that your API key is invalid. Please make sure you are setting up crtools with a valid key.')
                elif body['reason'] == 'accessDenied.invalidIp':
                    logger.error(
                        'developer.brawlstars.com says: {}'.format(body['message']))
                else:
                    logger.error('error: {}'.format(body))
            else:
                logger.error('error: {}'.format(e))
        except pyroyale.OpenApiException as e:
            logger.error('error: {}'.format(e))

        return False
